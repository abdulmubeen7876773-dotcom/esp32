import html
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import SITE_DOMAIN, esc, header_html, footer_html, head_html, CSS_VERSION

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
SITEMAP_XML = ROOT / "sitemap.xml"
SITEMAP_HTML = ROOT / "sitemap.html"

STATIC_PAGES = [
    ("index.html", "weekly", "1.0"),
    ("projects.html", "weekly", "0.9"),
    ("about.html", "monthly", "0.5"),
    ("contact.html", "monthly", "0.5"),
    ("privacy.html", "monthly", "0.4"),
    ("disclaimer.html", "monthly", "0.4"),
    ("sitemap.html", "monthly", "0.3"),
]

TODAY = date.today().isoformat()


def parse_title(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    import re

    m = re.search(r"<h1>([^<]+)</h1>", raw)
    return m.group(1).strip() if m else path.stem.replace("-", " ").title()


def write_sitemap_xml(project_files: list[Path]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page, freq, priority in STATIC_PAGES:
        if page == "sitemap.html":
            continue
        loc = f"{SITE_DOMAIN}/{page}"
        lines.append(
            f"<url><loc>{html.escape(loc)}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{priority}</priority></url>"
        )
    for path in project_files:
        loc = f"{SITE_DOMAIN}/projects/{path.name}"
        lines.append(
            f"<url><loc>{html.escape(loc)}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>0.8</priority></url>"
        )
    lines.append("</urlset>")
    SITEMAP_XML.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap_html(project_files: list[Path]) -> None:
    static_links = "".join(
        f'<li><a href="{esc(p)}">{esc(p.replace(".html", "").replace("-", " ").title())}</a></li>'
        for p, _, _ in STATIC_PAGES
        if p != "sitemap.html"
    )
    project_links = "".join(
        f'<li><a href="projects/{esc(path.name)}">{esc(parse_title(path))}</a></li>'
        for path in project_files
    )
    body = f"""  <h1>Sitemap</h1>
  <p>Browse every page on ESP32 Project Library — main pages and all project tutorials.</p>
  <section class="sitemap-static"><h2>Main Pages</h2><ul>{static_links}</ul></section>
  <section class="sitemap-projects"><h2>All Projects ({len(project_files)})</h2>
  <p class="meta">Search engines: <a href="sitemap.xml">sitemap.xml</a></p>
  <ul class="sitemap-project-list">{project_links}</ul></section>"""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "Sitemap | ESP32 Project Library", "Complete sitemap of ESP32 Project Library pages and tutorials.", canonical_path="sitemap.html")}
</head>
<body>
<main>
{header_html("home")}
<section class="section-block wrap page-head static-page sitemap-page">
{body}
</section>
</main>
{footer_html()}
<script src="ui.js" defer></script>
</body>
</html>"""
    SITEMAP_HTML.write_text(page, encoding="utf-8")


def main():
    project_files = sorted(PROJECTS.glob("*.html"))
    write_sitemap_xml(project_files)
    write_sitemap_html(project_files)
    print(f"Wrote sitemap.xml ({len(project_files) + len(STATIC_PAGES) - 1} URLs) + sitemap.html")


if __name__ == "__main__":
    main()
