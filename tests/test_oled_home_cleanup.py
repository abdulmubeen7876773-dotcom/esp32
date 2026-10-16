"""Keep page-specific repetition controls from weakening other tutorials."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from cms_loader import load_home_recommendations
from content_store import get_content_store
from guide_mission import render_mission_guide
from project_text import public_projects
from site_layout import home_learning_adventure, home_project_discovery, home_v3_top_picks


class OledHomeCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store = get_content_store()
        cls.guide = next(g for g in cls.store.guides() if g["slug"] == "connect-oled-esp32")

    def test_oled_has_one_explanation_and_consistent_navigation(self):
        body = render_mission_guide(self.guide)
        self.assertEqual(body.count("I2C lets multiple devices share two wires"), 1)
        self.assertEqual(body.count("The OLED is a tiny TV screen"), 1)
        self.assertNotIn('id="engineering"', body)
        self.assertNotIn('id="analogy"', body)
        self.assertNotIn('id="next-mission"', body)
        previous = body.split('id="previous-mission"', 1)[1].split("</section>", 1)[0]
        self.assertIn('/guides/read-temperature-dht22.html', previous)
        self.assertIn("Read Temperature with DHT11", previous)
        self.assertNotIn("Start here.", previous)
        self.assertEqual(body.count('/guides/oled-display-esp32.html'), 1)
        self.assertIn('youtube-nocookie.com/embed/lyu31EtokpQ', body)
        self.assertIn('youtube.com/watch?v=lyu31EtokpQ', body)

    def test_default_fallbacks_and_explicit_explanations_remain_available(self):
        guide = copy.deepcopy(self.guide)
        guide["mission"].pop("repeat_explanations")
        guide["academy"].pop("show_next_mission")
        body = render_mission_guide(guide)
        self.assertIn('id="engineering"', body)
        self.assertIn('id="analogy"', body)
        self.assertIn('id="next-mission"', body)
        guide["mission"]["repeat_explanations"] = False
        guide["mission"]["engineering_explanation"] = "A separate technical explanation."
        guide["mission"]["real_life_analogy"] = "A distinct authored analogy."
        body = render_mission_guide(guide)
        self.assertIn("A separate technical explanation.", body)
        self.assertIn("A distinct authored analogy.", body)

    def test_project_discovery_and_fallback_keep_destinations(self):
        projects = public_projects(self.store.projects())
        discovery = home_project_discovery(projects)
        self.assertNotIn("Popular Starting Points", discovery)
        self.assertIn('/projects/esp32-soil-moisture-monitor.html', discovery)
        self.assertIn('id="advanced-projects"', discovery)
        finder = home_learning_adventure(projects)
        self.assertIn('id="popular-projects"', finder)
        fallback = finder.split("<noscript>", 1)[1].split("</noscript>", 1)[0]
        for goals in load_home_recommendations()["recommendations"].values():
            for slugs in goals.values():
                for slug in slugs:
                    self.assertIn(f'/projects/{slug}.html', fallback)
        refs = home_v3_top_picks(projects, self.store.guides(), self.store.components(), include_projects=False)
        self.assertNotIn('href="/projects/', refs)
        self.assertIn('/guides/digital-inputs-floating-pins.html', refs)
        self.assertIn('/components/dht22.html', refs)
        legacy = home_v3_top_picks(projects, self.store.guides(), self.store.components())
        self.assertIn('href="/projects/', legacy)
        self.assertIn("Launch picks", legacy)


if __name__ == "__main__":
    unittest.main()
