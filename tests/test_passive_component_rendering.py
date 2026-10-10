from pathlib import Path
import sys, unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_components import component_page_html
from content_store import get_content_store


class PassiveComponentRenderingTest(unittest.TestCase):
    def test_passive_exercise_has_no_code_scaffold_or_broken_code_jump(self):
        component = next(c for c in get_content_store().components()
                         if c['slug'] == 'electrolytic-capacitors')
        self.assertNotIn('code', component)
        page = component_page_html(component)
        self.assertIn('id="wiring"', page)
        self.assertIn('id="troubleshooting"', page)
        self.assertNotIn('class="code-panel', page)
        self.assertNotIn('href="#code"', page)
        self.assertNotIn('Add component read/write code here', page)
        self.assertIn('Charge:', page)

    def test_active_examples_keep_complete_setup_and_loop(self):
        for slug in ('ft232r-usb-ttl', 'a4988-stepper-driver', 'solderless-breadboard'):
            with self.subTest(slug=slug):
                component = next(c for c in get_content_store().components() if c['slug'] == slug)
                self.assertIn('void setup()', component['code']['content'])
                self.assertIn('void loop()', component['code']['content'])
                self.assertIn('class="code-panel', component_page_html(component))


if __name__ == '__main__':
    unittest.main()
