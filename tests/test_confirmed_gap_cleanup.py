"""Focused DHT11 de-duplication and scoped static-page boundaries."""
import copy
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_scope
from content_store import get_content_store
from guide_mission import render_mission_guide


class ConfirmedGapCleanupTests(unittest.TestCase):
    def dht11(self):
        return next(g for g in get_content_store().guides() if g["slug"] == "read-temperature-dht22")

    def test_dht11_retains_one_explanation_notes_and_expected_output(self):
        body = render_mission_guide(self.dht11())
        for text in (
            "The DHT11 is a digital temperature and humidity sensor.",
            "The DHT11 is like a tiny weather reporter.",
            "The linked Aosong DHT11 manual specifies",
            "Open Serial Monitor at 115200 baud. After the startup delay",
            "Documentation review only; compilation and hardware testing were not performed.",
        ):
            self.assertEqual(body.count(text), 1, text)
        self.assertIn("zLHl_6ToUck", body)
        self.assertIn('id="troubleshooting"', body)
        self.assertIn('id="quiz"', body)
        self.assertIn('id="code"', body)
        self.assertNotIn('id="common-mistakes"', body)
        self.assertNotIn('id="engineering"', body)
        self.assertNotIn('id="analogy"', body)
        self.assertNotIn('id="code-explanation"', body)

    def test_legacy_preview_is_still_enabled_by_default(self):
        guide = copy.deepcopy(self.dht11())
        guide.pop("section_order")
        guide["mission"].pop("show_output_preview")
        body = render_mission_guide(guide)
        self.assertIn('aria-label="Expected result preview"', body)
        self.assertIn('id="code-explanation"', body)

    def test_unknown_static_page_fails_before_generation(self):
        manifest = Mock(spec=Path)
        manifest.read_text.return_value = json.dumps(dict(
            guides=[], projects=[], categories=[], pages=["not-a-cms-page"]
        ))
        with self.assertRaisesRegex(ValueError, "Unknown pages"):
            build_scope.generate_scope(manifest)

    def test_selected_static_page_must_be_in_sitemap(self):
        empty = ET.ElementTree(ET.fromstring('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>'))
        with patch("xml.etree.ElementTree.parse", return_value=empty):
            with self.assertRaisesRegex(ValueError, "missing tools.html"):
                build_scope.validate_sitemap({"pages": ["tools"]})
        selected = ET.ElementTree(ET.fromstring(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://esp32engine.com/tools.html</loc></url></urlset>'
        ))
        with patch("xml.etree.ElementTree.parse", return_value=selected):
            build_scope.validate_sitemap({"pages": ["tools"]})


if __name__ == "__main__":
    unittest.main()
