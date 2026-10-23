"""Opt-in authored guide cards must survive catalog changes without altering defaults."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import guide_mission


class GuideProjectLinkCopyTests(unittest.TestCase):
    def setUp(self):
        self.guide = {"academy": {"unlocked_projects": [{
            "title": "Reviewed OLED project", "description": "Existing <copy> & details",
            "href": "/projects/esp32-oled-weather-clock.html",
        }]}}

    def test_authored_copy_is_escaped_and_does_not_read_catalog_text(self):
        self.guide["academy"]["project_link_copy"] = "authored"
        with patch.object(guide_mission, "project_title", side_effect=AssertionError("catalog used")):
            body = guide_mission.related_projects_section(self.guide)
        self.assertIn("Reviewed OLED project", body)
        self.assertIn("Existing &lt;copy&gt; &amp; details", body)
        self.assertIn('href="/projects/esp32-oled-weather-clock.html"', body)

    def test_default_still_resolves_current_catalog_labels(self):
        with patch.object(guide_mission, "project_title", return_value="Current catalog title"), \
             patch.object(guide_mission, "card_description", return_value="Current catalog description"):
            body = guide_mission.related_projects_section(self.guide)
        self.assertIn("Current catalog title", body)
        self.assertIn("Current catalog description", body)
        self.assertNotIn("Reviewed OLED project", body)

    def test_unknown_mode_fails_instead_of_silently_refreshing_copy(self):
        self.guide["academy"]["project_link_copy"] = "authorred"
        with self.assertRaisesRegex(ValueError, "project_link_copy"):
            guide_mission.related_projects_section(self.guide)


if __name__ == "__main__":
    unittest.main()
