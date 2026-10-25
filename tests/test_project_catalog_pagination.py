"""Multi-page discovery includes all records without losing static fallback."""
import json
import re
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from cms_loader import load_projects
from project_text import public_projects
from project_catalog import listing_html
from rebuild_index import parent_listing_record


class CatalogPaginationTests(unittest.TestCase):
    def test_each_paginated_view_has_complete_interactive_catalog_and_static_slice(self):
        records = [parent_listing_record(p) for p in public_projects(load_projects())]
        self.assertGreater(len(records), 50)
        for page, chunk in [(1, records[:50]), (2, records[50:])]:
            markup = listing_html('', chunk, page, 2, len(records))
            payload = re.search(r'id="project-catalog-data">(.*?)</script>', markup, re.S)
            self.assertIsNotNone(payload)
            data = json.loads(payload.group(1))
            self.assertEqual({p['slug'] for p in data}, {p['slug'] for p in records})
            self.assertEqual(markup.count('class="card project-card modern-card project-card-item"'), len(chunk))
            self.assertIn('Project list pages', markup)
            self.assertIn('<noscript>', markup)

    def test_single_page_keeps_existing_static_controller_path(self):
        records = [parent_listing_record(p) for p in public_projects(load_projects())][:2]
        markup = listing_html('', records, 1, 1, 2)
        self.assertNotIn('id="project-catalog-data"', markup)
        self.assertEqual(markup.count('class="card project-card modern-card project-card-item"'), 2)

    def test_embedded_titles_round_trip_without_closing_script_element(self):
        projects = public_projects(load_projects())
        projects[0] = dict(projects[0], title='Literal <script>demo</script> title')
        records = [parent_listing_record(p) for p in projects]
        with patch('content_store.get_content_store') as store:
            store.return_value.projects.return_value = projects
            markup = listing_html('', records[:50], 1, 2, len(records))
        payload = re.search(r'id="project-catalog-data">(.*?)</script>', markup, re.S).group(1)
        self.assertNotIn('<', payload)
        self.assertEqual(json.loads(payload)[0]['title'], projects[0]['title'])


if __name__ == '__main__':
    unittest.main()
