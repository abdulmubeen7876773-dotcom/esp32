import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import footer_html, CSS_VERSION, head_html

root = Path(__file__).resolve().parent.parent
pat = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.S)
css_pat = re.compile(r"style\.css\?v=[^\"']+")
for name in ["about.html", "contact.html", "privacy.html", "disclaimer.html", "404.html"]:
    f = root / name
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    t2 = css_pat.sub(f"style.css?v={CSS_VERSION}", t)
    if "fonts.googleapis.com" not in t2:
        t2 = re.sub(
            r"(<meta name=\"viewport\"[^>]*>)",
            r'\1\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">',
            t2,
            count=1,
        )
    if "theme-color" not in t2:
        t2 = re.sub(r"(<meta charset=\"utf-8\">)", r'\1\n<meta name="theme-color" content="#020617">', t2, count=1)
    if "ui.js" not in t2:
        t2 = t2.replace("</body>", '<script src="ui.js" defer></script>\n</body>')
    t2 = pat.sub(footer_html(""), t2, count=1)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
        print(f"Updated {name}")
