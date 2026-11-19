"""Scoped editorial controls must preserve existing guide/category behavior."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from content_store import get_content_store
from guide_mission import render_mission_guide
from build_categories import category_context_html


class BenchmarkGapControlsTests(unittest.TestCase):
    def setUp(self):
        self.guide = copy.deepcopy(next(g for g in get_content_store().guides()
                                        if g['slug'] == 'button-led-control'))

    def test_explicit_opt_out_retains_diagnostic_causes_and_fixes_once(self):
        html = render_mission_guide(self.guide)
        self.assertNotIn('id="common-mistakes"', html)
        self.assertIn('id="troubleshooting"', html)
        self.assertEqual(html.count('<h3>Button always reads PRESSED</h3>'), 1)
        self.assertIn('Rotate the button 90 degrees', html)
        self.assertIn('INPUT_PULLUP', html)

    def test_absent_flag_retains_legacy_fallback(self):
        self.guide['mission'].pop('show_common_mistakes', None)
        html = render_mission_guide(self.guide)
        self.assertIn('id="common-mistakes"', html)
        self.assertIn('id="troubleshooting"', html)

    def test_explicit_true_keeps_authored_mistakes_and_troubleshooting(self):
        self.guide['mission']['show_common_mistakes'] = True
        self.guide['mission']['common_mistakes'] = ['Keep this separate teaching point.']
        html = render_mission_guide(self.guide)
        self.assertIn('Keep this separate teaching point.', html)
        self.assertIn('Rotate the button 90 degrees', html)

    def test_category_without_privacy_has_no_empty_heading(self):
        html = category_context_html('Robotics', [])
        self.assertNotIn('Privacy boundary', html)
        self.assertIn('Limits to understand', html)
        self.assertIn('Common failure checks', html)

    def test_category_with_privacy_retains_real_guidance(self):
        html = category_context_html('AI Projects', [])
        self.assertIn('Privacy boundary', html)
        self.assertIn('get consent', html)


if __name__ == '__main__':
    unittest.main()
