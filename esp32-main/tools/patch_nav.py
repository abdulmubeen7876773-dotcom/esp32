import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_icons import featured_cat_bar

root = Path(__file__).resolve().parent.parent
pat = re.compile(r"<nav class=\"cat-bar\">.*?</nav>", re.S)
new_bar_proj = featured_cat_bar("../")
new_bar_root = featured_cat_bar("")
n = 0
for f in (root / "projects").glob("*.html"):
    t = f.read_text(encoding="utf-8")
    t2 = pat.sub(new_bar_proj, t, count=1)
    t2 = re.sub(r"style\.css\?v=20260615-(gloss|titles|dark)", "style.css?v=20260615-hero", t2)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
        n += 1
for name in ["about.html", "contact.html", "privacy.html", "disclaimer.html"]:
    f = root / name
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    t2 = pat.sub(new_bar_root, t, count=1)
    t2 = re.sub(r"style\.css\?v=20260615-(gloss|titles|dark)", "style.css?v=20260615-hero", t2)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
print(f"Updated {n} project pages")
