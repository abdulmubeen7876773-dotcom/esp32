import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import footer_html

root = Path(__file__).resolve().parent.parent
pat = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.S)
for name in ["about.html", "contact.html", "privacy.html", "disclaimer.html", "404.html"]:
    f = root / name
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    t2 = re.sub(r"style\.css\?v=20260615-[a-z]+", "style.css?v=20260615-premium", t)
    t2 = pat.sub(footer_html(""), t2, count=1)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
        print(f"Updated {name}")
