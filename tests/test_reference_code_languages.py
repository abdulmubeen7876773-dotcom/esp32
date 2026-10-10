"""Guard readable/copied Python code without changing the Arduino default."""
import sys
import unittest
from pathlib import Path
from html import unescape
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from guide_mission import code_panel
from article_sections import examples_section, prepare_article


class ReferenceCodeLanguageTests(unittest.TestCase):
    def test_python_text_and_accessible_language(self):
        source = 'print("<tag>& value")\n# keep this Python comment'
        body = prepare_article(examples_section([
            {"filename": "code.py", "language": "python", "content": source}
        ]))
        code = re.search(r'<code class="language-python">(.*?)</code>', body, re.S)[1]
        self.assertEqual(unescape(code), source)
        self.assertNotIn("<tag>", body)
        self.assertIn('aria-label="Python code;', body)
        self.assertIn("CircuitPython code and USB connection", body)

    def test_default_arduino_labels_and_highlighting(self):
        body = prepare_article(examples_section([
            {"filename": "sketch.ino", "content": "#include <Arduino.h>"}
        ]))
        self.assertIn('class="language-arduino"', body)
        self.assertIn('class="tok-pre"', body)
        self.assertIn('aria-label="Arduino code;', body)
        self.assertIn("Wiring and matching Arduino code", body)

    def test_unknown_language_is_rejected(self):
        with self.assertRaises(ValueError):
            code_panel({"content": "x", "language": 'python" onclick="x'})


if __name__ == "__main__":
    unittest.main()
