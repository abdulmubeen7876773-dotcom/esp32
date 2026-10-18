"""Guard production behavior and catalog continuity in the cinematic homepage."""
import copy
import json
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from content_store import get_content_store
from project_text import public_projects
from rebuild_index import home_html, parent_listing_record
from build_scope import generate_scope


class Markup(HTMLParser):
    def __init__(self, body):
        super().__init__()
        self.ids, self.hrefs, self.h1, self.images = [], [], 0, []
        self.feed(body)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a":
            self.hrefs.append(attrs.get("href"))
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            self.images.append(attrs)


class CinematicHomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store = get_content_store()
        cls.records = [parent_listing_record(p) for p in public_projects(cls.store.projects())]
        cls.body = home_html(cls.records)

    def test_production_metadata_controls_and_discovery_survive(self):
        body = self.body
        page = Markup(body)
        self.assertEqual(page.h1, 1)
        self.assertEqual(len(page.ids), len(set(page.ids)))
        for fragment in ("advanced-projects", "popular-projects", "start-here", "featured-projects"):
            self.assertIn(fragment, page.ids)
        for destination in ("/guides.html", "/projects.html", "/components.html", "/privacy.html", "/contact.html"):
            self.assertIn(destination, page.hrefs)
        for marker in ('id="header-search-input"', 'id="search-open"', 'id="theme-toggle"', 'class="nav-toggle"',
                       'id="home-recommendation-data"', "data-cookie-settings", "data-ad-privacy", "<noscript>"):
            self.assertIn(marker, body)
        self.assertIn('/ui.js?v=20261008-google-cmp', body)
        self.assertIn('<link rel="canonical" href="https://esp32engine.com/">', body)
        self.assertNotIn("noindex", body)
        self.assertNotIn("friendly-workshop", body)
        self.assertNotIn("Design prototype", body)

    def test_exact_beginner_order_and_qualified_visuals(self):
        route = self.body.split('<ol class="cm-journey-line">', 1)[1].split("</ol>", 1)[0]
        self.assertEqual(Markup(route).hrefs, [
            "/guides/installing-arduino-ide-esp32.html", "/guides/blink-led-esp32.html",
            "/guides/button-led-control.html", "/guides/read-temperature-dht22.html",
            "/guides/connect-oled-esp32.html"])
        self.assertIn("DHT11 sensor", route)
        self.assertNotIn("<img", route)
        self.assertIn("Parts:", self.body)
        self.assertIn("Before you start:", self.body)
        self.assertIn("not wiring diagrams or hardware-test evidence", self.body)
        for img in Markup(self.body).images:
            self.assertTrue(img.get("width") and img.get("height"))

    def test_legacy_default_does_not_load_cinematic_styles(self):
        home = copy.deepcopy(self.store.home())
        home.pop("design")
        with patch.object(self.store, "home", return_value=home):
            body = home_html(self.records)
        self.assertNotIn('class="home-page cinematic-maker"', body)
        self.assertNotIn('/assets/cinematic-home.css', body)
        self.assertIn('id="home-primary-paths-heading"', body)

    def test_homepage_scope_rejects_invalid_or_mixed_selection(self):
        for scope in [dict(guides=[], projects=[], categories=[], homepage=False),
                      dict(guides=["connect-oled-esp32"], projects=[], categories=[], homepage=True)]:
            manifest = Mock(spec=Path)
            manifest.read_text.return_value = json.dumps(scope)
            with self.assertRaises(ValueError):
                generate_scope(manifest)


if __name__ == "__main__":
    unittest.main()
