"""Catalog structure and safe selective-generation boundaries."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_scope import generate_scope
from project_catalog import category_layout, category_browse
from site_layout import NAV_ITEMS


class ProjectCatalogTests(unittest.TestCase):
    def test_primary_navigation_is_one_set_of_destinations(self):
        self.assertEqual([item[0] for item in NAV_ITEMS], ['home','guides','projects','components','learning'])

    def test_category_links_and_current_page_are_accurate(self):
        links = category_browse('display-projects')
        self.assertIn('/category/display-projects.html" aria-current="page">Display Projects', links)
        self.assertIn('/category/led-projects.html">LED Projects', links)
        self.assertEqual(links.count('/category/iot-projects.html'), 1)

    def test_category_navigation_transform_preserves_article_and_is_idempotent(self):
        original = '<head><link rel="stylesheet" href="/assets/project-catalog.css?v=20261018"></head><aside class="sidebar-categories">old aliases</aside><article>Keep this exact content.</article>'
        updated = category_layout(original)
        self.assertIn('<article>Keep this exact content.</article>', updated)
        self.assertNotIn('old aliases', updated)
        self.assertEqual(updated.count('/assets/project-catalog.css'), 1)
        self.assertNotIn('v=20261018', updated)
        self.assertEqual(category_layout(updated), updated)

    def test_navigation_scope_rejects_invalid_or_mixed_selection(self):
        for selected, flag in [([],False),(['connect-oled-esp32'],True)]:
            manifest = Mock(spec=Path)
            manifest.read_text.return_value = json.dumps(dict(guides=selected,projects=[],categories=[],navigation=flag))
            with self.assertRaises(ValueError):
                generate_scope(manifest)


if __name__ == '__main__':
    unittest.main()
