import html
import sys
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parent_registry import PARENTS
from content_store import get_content_store
from site_layout import PROJECTS_PAGE_SIZE, SITE_DOMAIN, esc, header_html, footer_html, head_html, projects_page_path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
CATEGORY = ROOT / "category"
SITEMAP_XML = ROOT / "sitemap.xml"
SITEMAP_HTML = ROOT / "sitemap.html"

STATIC_PAGES = [
    ("", "weekly", "1.0"),
    ("learning.html", "weekly", "0.95"),
    ("components.html", "weekly", "0.95"),
    ("guides.html", "weekly", "0.92"),
    ("projects.html", "weekly", "0.92"),
    ("parents.html", "monthly", "0.7"),
    ("teachers.html", "monthly", "0.7"),
    ("downloads.html", "monthly", "0.6"),
    ("tools.html", "monthly", "0.6"),
    ("news.html", "weekly", "0.6"),
    ("search.html", "monthly", "0.4"),
    ("about.html", "monthly", "0.5"),
    ("contact.html", "monthly", "0.5"),
    ("privacy.html", "monthly", "0.4"),
    ("terms.html", "monthly", "0.4"),
    ("disclaimer.html", "monthly", "0.4"),
    ("sitemap.html", "monthly", "0.3"),
]

TODAY = date.today().isoformat()


def page_loc(page: str) -> str:
    if page == "":
        return f"{SITE_DOMAIN}/"
    return f"{SITE_DOMAIN}/{page}"


def category_pages() -> list[tuple[str, str, str]]:
    cats = sorted({p["category"] for p in PARENTS})
    return [(f"category/{slug_cat(c)}.html", "weekly", "0.85") for c in cats]


def slug_cat(cat: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")


def project_listing_pages() -> list[tuple[str, str, str]]:
    total = len(PARENTS)
    pages = max(1, (total + PROJECTS_PAGE_SIZE - 1) // PROJECTS_PAGE_SIZE)
    out = []
    for n in range(1, pages + 1):
        path = projects_page_path(n)
        priority = "0.9" if n == 1 else "0.85"
        out.append((path, "weekly", priority))
    return out

def parse_title(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    import re

    m = re.search(r"<h1>([^<]+)</h1>", raw)
    return m.group(1).strip() if m else path.stem.replace("-", " ").title()


def guide_pages() -> list[tuple[str, str, str]]:
    store = get_content_store()
    return [(f"guides/{g['slug']}.html", "monthly", "0.88") for g in sorted(store.guides(), key=lambda g: (g.get("phase", 99), g.get("sort_order", 99), g.get("slug", "")))]


def component_pages() -> list[tuple[str, str, str]]:
    return [(f"components/{c['slug']}.html", "monthly", "0.86") for c in get_content_store().components()]


def write_sitemap_xml(project_files: list[Path]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page, freq, priority in STATIC_PAGES + guide_pages() + component_pages() + category_pages() + project_listing_pages():
        if page == "sitemap.html":
            continue
        loc = page_loc(page)
        lines.append(
            f"<url><loc>{html.escape(loc)}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{priority}</priority></url>"
        )
    for path in project_files:
        if "_archive" in path.parts or "-project-" in path.name:
            continue
        loc = f"{SITE_DOMAIN}/projects/{path.name}"
        lines.append(
            f"<url><loc>{html.escape(loc)}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>0.8</priority></url>"
        )
    lines.append("</urlset>")
    SITEMAP_XML.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap_html(project_files: list[Path]) -> None:
    valid = [p for p in project_files if "_archive" not in p.parts and "-project-" not in p.name]
    static_links = "".join(
        f'<li><a href="{esc("/" if not p else "/" + p)}">{esc(("Home" if not p else p.replace(".html", "").replace("-", " ").title()))}</a></li>'
        for p, _, _ in STATIC_PAGES
        if p != "sitemap.html"
    )
    cat_links = "".join(
        f'<li><a href="category/{esc(slug_cat(c))}.html">{esc(c)}</a></li>'
        for c in sorted({p["category"] for p in PARENTS})
    )
    project_links = "".join(
        f'<li><a href="projects/{esc(path.name)}">{esc(parse_title(path))}</a></li>'
        for path in valid
    )
    body = f"""  <h1>Sitemap</h1>
  <p>Browse every page on {SITE_DOMAIN.replace("https://", "")} — main pages, categories, and {len(valid)} ESP32 project tutorials.</p>
  <section class="sitemap-static"><h2>Main Pages</h2><ul>{static_links}</ul></section>
  <section class="sitemap-categories"><h2>Categories ({len({p["category"] for p in PARENTS})})</h2><ul>{cat_links}</ul></section>
  <section class="sitemap-projects"><h2>Projects ({len(valid)})</h2>
  <p class="meta">Search engines: <a href="sitemap.xml">sitemap.xml</a></p>
  <ul class="sitemap-project-list">{project_links}</ul></section>"""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "Sitemap | ESP32 Engine", "Complete sitemap of ESP32 Engine pages, categories, and tutorials.", canonical_path="sitemap.html")}
</head>
<body>
<main>
{header_html("home")}
<section class="section-block wrap page-head static-page sitemap-page">
{body}
</section>
</main>
{footer_html()}
<script src="/ui.js" defer></script>
</body>
</html>"""
    SITEMAP_HTML.write_text(page, encoding="utf-8")


def main():
    project_files = sorted(
        p
        for p in PROJECTS.glob("*.html")
        if p.is_file() and "-project-" not in p.name and "_archive" not in p.parts
    )
    write_sitemap_xml(project_files)
    write_sitemap_html(project_files)
    url_count = (
        len(project_files)
        + len(STATIC_PAGES)
        + len(guide_pages())
        + len(component_pages())
        + len(category_pages())
        + len(project_listing_pages())
        - 1
    )
    print(f"Wrote sitemap.xml ({url_count} URLs) + sitemap.html")


if __name__ == "__main__":
    main()
