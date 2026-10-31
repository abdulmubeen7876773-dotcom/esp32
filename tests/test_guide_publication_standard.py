"""Regression checks for explicit sketch selection and guide-only generation."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from content_store import get_content_store
from build_guides import render_guide
import build_scope
import rebuild_index

class GuidePublicationTests(unittest.TestCase):
    def test_copy_selects_sketch_not_board_index_url(self):
        guide = next(g for g in get_content_store().guides() if g['slug'] == 'esp32-arduino-ide')
        page = render_guide(guide)
        self.assertEqual(page.count('data-copy '), 1)
        # Keyboard-scroll attributes are allowed; the URL must remain a plain
        # pre/code block rather than being mistaken for the copyable sketch.
        self.assertRegex(page, r'<pre\b[^>]*><code>https://espressif.github.io')
        self.assertIn('esp32_first_upload.ino', page)

    def test_copy_rejects_conceptual_snippet(self):
        guide = copy.deepcopy(next(g for g in get_content_store().guides() if g['slug'] == 'esp32-gpio-button'))
        guide['copy_code_blocks'] = {'0': 'not_a_sketch.ino'}
        with self.assertRaisesRegex(ValueError, 'complete Arduino sketch'):
            render_guide(guide)

    def test_existing_dht11_opt_in_keeps_output_uncopyable(self):
        guide = next(g for g in get_content_store().guides() if g['slug'] == 'esp32-dht22')
        page = render_guide(guide)
        self.assertEqual(page.count('data-copy '), 1)
        self.assertIn('dht11_reference.ino', page)
        self.assertIn('Temperature: 24.0', page)

    def test_guide_catalog_scope_cannot_write_home_or_projects(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'guides').mkdir()
            manifest = root / 'scope.json'
            manifest.write_text(json.dumps({'guides': ['esp32-gpio-button'], 'projects': [], 'categories': [], 'guide_catalog_only': True}))
            with patch.object(build_scope, 'ROOT', root), patch.object(build_scope, 'validate_sitemap') as validate, patch.object(rebuild_index, 'home_html', side_effect=AssertionError('Home must not render')), patch.object(rebuild_index, 'write_project_listing_pages', side_effect=AssertionError('Projects must not render')):
                build_scope.generate_scope(manifest)
                validate.assert_called_once()
            self.assertEqual({p.name for p in root.iterdir()}, {'scope.json', 'guides', 'guides.html', 'search-index.json'})

    def test_invalid_mixed_scope_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / 'scope.json'
            manifest.write_text(json.dumps({'guides': ['esp32-gpio-button'], 'projects': ['unrelated'], 'categories': [], 'guide_catalog_only': True}))
            with self.assertRaisesRegex(ValueError, 'no projects/categories'):
                build_scope.generate_scope(manifest)

if __name__ == '__main__':
    unittest.main()
