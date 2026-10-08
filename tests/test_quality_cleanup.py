"""Focused regressions for content disclosures and deployment boundaries."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from package_site import public_file
from content_store import get_content_store
from component_page import code_section_html, component_all_faqs, downloads_html
from project_page import wiring_diagram_html, complete_section


class QualityCleanupTests(unittest.TestCase):
    def test_deployment_keeps_public_routes_and_runtime(self):
        for name in ["index.html", "CNAME", ".nojekyll", "search-index.json", "projects.json",
                     "projects/esp32-ai-object-detector.html", "assets/visuals/components/wiring/esp32-cam-wiring.svg"]:
            self.assertTrue(public_file(Path(name)), name)

    def test_deployment_excludes_internal_and_protected_inputs(self):
        for name in ["build-report.json", "ADSENSE_RECOVERY_AUDIT.md", "README.txt",
                     "docs/reports/latest-build.md", "tools/build_all.py",
                     "projects/_archive/old.html", "assets/visuals/manifest.json",
                     "components/component images.zip", "components/esp32-component-master-catalog.csv",
                     "components/esp32-component-master-catalog.backup.csv", "components/esp32-component-master-catalog.md"]:
            self.assertFalse(public_file(Path(name)), name)

    def test_camera_example_really_captures_and_returns_frames(self):
        camera = next(c for c in get_content_store().components() if c["slug"] == "esp32-cam")
        code = camera["code"]["content"]
        for text in ["esp_camera_fb_get()", "esp_camera_fb_return(frame)", "CAMERA_FB_IN_DRAM", "pin_sccb_sda"]:
            self.assertIn(text, code)
        self.assertNotIn("Add component read/write code here", code_section_html(camera))
        self.assertEqual(component_all_faqs(camera), camera["faqs"])
        self.assertIn("Open Espressif camera driver reference", downloads_html(camera))
        self.assertNotIn("Download Datasheet (PDF)", downloads_html(camera))

    def test_empty_download_sections_are_hidden(self):
        for component in get_content_store().components():
            if not component.get("datasheet_url"):
                self.assertEqual(downloads_html(component), "", component["slug"])

    def test_missing_diagram_is_honest_and_real_diagrams_remain(self):
        fallback = wiring_diagram_html("", "Circuit diagram")
        self.assertIn("No separate electrical diagram", fallback)
        self.assertNotIn("<figure", fallback)
        self.assertIn('<img src="/diagram.svg"', wiring_diagram_html("/diagram.svg", "Connections"))

    def test_completion_is_a_check_not_a_claim(self):
        for project in get_content_store().projects():
            if (project.get("project") or {}).get("complete") and not (project.get("project") or {}).get("tutorial_flow"):
                self.assertNotIn("You completed", complete_section(project))
                self.assertNotIn("Project Complete!", complete_section(project))
                self.assertIn("Check your result", complete_section(project))


if __name__ == "__main__":
    unittest.main()
