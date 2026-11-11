"""An opt-in project scope changes existing selected dates, never XML neighbours."""
import sys
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_scope import component_sitemap_lastmods, generate_scope


class ProjectLastmodScopeTests(unittest.TestCase):
    def setUp(self):
        self.xml = ('<urlset>\r\n'
                    '<url><loc>https://esp32engine.com/projects/a.html</loc>'
                    '<lastmod>2026-01-01</lastmod><priority>0.8</priority></url>\r\n'
                    '<url><loc>https://esp32engine.com/projects/b.html</loc>'
                    '<lastmod>2026-02-02</lastmod></url>\r\n'
                    '<url><loc>https://esp32engine.com/components/a.html</loc>'
                    '<lastmod>2026-03-03</lastmod></url>\r\n</urlset>')
        self.record = dict(slug="a", date_modified="2026-11-10")

    def test_selected_project_only_and_idempotence(self):
        result = component_sitemap_lastmods(self.xml, [self.record], section="projects")
        self.assertEqual(result, self.xml.replace("2026-01-01", "2026-11-10"))
        self.assertEqual(result, component_sitemap_lastmods(result, [self.record], section="projects"))

    def test_component_default_remains_backward_compatible(self):
        result = component_sitemap_lastmods(self.xml, [self.record])
        self.assertEqual(result, self.xml.replace("2026-03-03", "2026-11-10"))

    def test_missing_duplicate_bad_date_or_bad_section_fails(self):
        for xml, records, section in (
            (self.xml, [dict(slug="missing", date_modified="2026-11-10")], "projects"),
            (self.xml, [self.record, self.record], "projects"),
            (self.xml.replace('</urlset>', self.xml.split('\r\n')[1] + '</urlset>'), [self.record], "projects"),
            (self.xml.replace('<lastmod>2026-01-01</lastmod>', ''), [self.record], "projects"),
            (self.xml, [dict(slug="a", date_modified="2026-02-30")], "projects"),
            (self.xml, [self.record], "guides"),
        ):
            with self.subTest(section=section, records=records):
                with self.assertRaises(ValueError):
                    component_sitemap_lastmods(xml, records, section=section)

    def test_project_date_mode_rejects_false_empty_and_mixed_guides(self):
        for changes in ({"project_lastmods": False}, {"projects": []},
                        {"guides": ["unrelated-guide"]}):
            scope = dict(guides=[], projects=["a"], categories=[], project_lastmods=True)
            scope.update(changes)
            manifest = SimpleNamespace(read_text=lambda **_: json.dumps(scope))
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                generate_scope(manifest)


if __name__ == "__main__":
    unittest.main()
