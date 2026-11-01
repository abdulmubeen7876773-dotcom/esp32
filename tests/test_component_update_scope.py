"""Existing-component updates must not regenerate unrelated public outputs."""
import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_scope
# Load renderer modules against the real store before replacing it with the
# small test catalog; module initialization also reads the project registry.
import build_components
import build_search_index
import build_static_pages
import build_guides
import rebuild_index


class ComponentUpdateScopeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "components").mkdir()
        self.catalog = [{"slug": slug, "date_modified": "2026-11-01"}
                        for slug in ("a", "b", "c")]
        self.store = SimpleNamespace(
            guides=lambda: [], projects=lambda: [], components=lambda: self.catalog,
            pages=lambda: {"about": {}, "learning": {}}, component_categories=lambda: [])
        for slug in ("a", "b", "c"):
            (self.root / "components" / f"{slug}.html").write_text(f"old {slug}")
        for path in ("components.html", "index.html", "learning.html", "about.html",
                     "search-index.json", "feed.xml", "ui.js"):
            (self.root / path).write_text("preserve " + path)
        self.xml = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + ''.join(f'<url><loc>https://esp32engine.com/components/{slug}.html</loc>'
                              '<lastmod>2026-01-01</lastmod><priority>0.86</priority></url>\n'
                              for slug in ("a", "b", "c")) + '</urlset>')
        (self.root / "sitemap.xml").write_text(self.xml, encoding="utf-8")

    def manifest(self, **changes):
        data = dict(guides=[], projects=[], categories=[], components=["b"],
                    component_updates_only=True)
        data.update(changes)
        path = self.root / "scope.json"
        path.write_text(json.dumps(data))
        return path

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def rendering(self):
        stack = ExitStack()
        stack.enter_context(patch.object(build_scope, "ROOT", self.root))
        stack.enter_context(patch("content_store.get_content_store", return_value=self.store))
        self.page = stack.enter_context(patch("build_components.component_page_html",
                                              side_effect=lambda c, prev, nxt: "new " + c["slug"]))
        self.index = stack.enter_context(patch("build_components.index_html", return_value="new catalog"))
        stack.enter_context(patch("build_search_index.build_index", side_effect=AssertionError("No search generation")))
        stack.enter_context(patch("rebuild_index.home_html", side_effect=AssertionError("No Home generation")))
        stack.enter_context(patch("build_static_pages.cms_page_html", side_effect=AssertionError("No CMS generation")))
        stack.enter_context(patch("build_guides.render_guide", side_effect=AssertionError("No guide generation")))
        return stack

    def test_exact_boundary_real_neighbours_and_idempotence(self):
        manifest = self.manifest()
        before = self.snapshot()
        with self.rendering():
            build_scope.generate_scope(manifest)
            self.page.assert_called_once_with(self.catalog[1], self.catalog[0], self.catalog[2])
            self.index.assert_called_once_with(self.catalog, [])
            first = self.snapshot()
            changed = {p for p in first if first[p] != before[p]}
            self.assertEqual(changed, {"components/b.html", "components.html", "sitemap.xml"})
            build_scope.generate_scope(manifest)
            self.assertEqual(first, self.snapshot())

    def test_rejects_mixed_empty_duplicate_and_false_modes(self):
        for changes in ({"guides": ["unrelated"]}, {"projects": ["unrelated"]},
                        {"categories": ["unrelated"]}, {"components": []},
                        {"components": ["b", "b"]}, {"component_updates_only": False}):
            with self.subTest(changes=changes), self.rendering():
                manifest = self.manifest(**changes)
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    build_scope.generate_scope(manifest)
                self.assertEqual(before, self.snapshot())
                self.page.assert_not_called()

    def test_unknown_or_unpublished_page_cannot_write_outputs(self):
        for changes in ({"components": ["unknown"]}, {"components": ["b"]}):
            with self.subTest(changes=changes), self.rendering():
                manifest = self.manifest(**changes)
                if changes["components"] == ["b"]:
                    (self.root / "components/b.html").unlink()
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    build_scope.generate_scope(manifest)
                self.assertEqual(before, self.snapshot())

    def test_sitemap_changes_only_selected_date_and_preserves_xml_bytes(self):
        xml = self.xml.replace('\n', '\r\n')
        result = build_scope.component_sitemap_lastmods(xml, [self.catalog[1]])
        selected = ('<loc>https://esp32engine.com/components/b.html</loc>'
                    '<lastmod>2026-01-01</lastmod>')
        self.assertEqual(result, xml.replace(selected, selected.replace('2026-01-01', '2026-11-01')))
        self.assertEqual(result, build_scope.component_sitemap_lastmods(result, [self.catalog[1]]))

    def test_bad_sitemap_or_source_date_fails_before_any_output_write(self):
        for xml, date in ((self.xml.replace('<lastmod>2026-01-01</lastmod>', ''), '2026-11-01'),
                          (self.xml.replace('</urlset>', self.xml.split('\n')[2] + '</urlset>'), '2026-11-01'),
                          (self.xml.replace('/b.html', '/not-b.html'), '2026-11-01'),
                          (self.xml, '2026-02-30')):
            with self.subTest(date=date, xml=xml), self.rendering():
                manifest = self.manifest()
                (self.root / "sitemap.xml").write_text(xml, encoding="utf-8")
                self.catalog[1]["date_modified"] = date
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    build_scope.generate_scope(manifest)
                self.assertEqual(before, self.snapshot())
                self.page.assert_not_called()

    def test_existing_broad_component_scope_retains_dependencies(self):
        manifest = self.manifest()
        data = json.loads(manifest.read_text())
        del data["component_updates_only"]
        manifest.write_text(json.dumps(data))
        with self.rendering(), patch("build_search_index.build_index", return_value=[]) as search, \
                patch("rebuild_index.home_html", return_value="new Home") as home, \
                patch("build_static_pages.cms_page_html", return_value="new CMS") as cms:
            build_scope.generate_scope(manifest)
            self.assertEqual(self.page.call_count, 3)
            search.assert_called_once()
            home.assert_called_once()
            self.assertEqual(cms.call_count, 2)


if __name__ == "__main__":
    unittest.main()
