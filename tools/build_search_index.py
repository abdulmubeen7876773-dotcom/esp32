import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import assert_phase1_static, get_content_store

ROOT = Path(__file__).resolve().parent.parent
INDEX_OUT = ROOT / "search-index.json"
SEARCH_PAGE = ROOT / "search.html"


def entry(type_label: str, title: str, desc: str, href: str, **extra) -> dict:
    row = {"type": type_label, "title": title, "desc": desc, "href": href}
    row.update(extra)
    return row


def build_index() -> list:
    store = get_content_store()
    items = []
    for c in store.components():
        items.append(
            entry(
                "Component",
                c["name"],
                c.get("summary", ""),
                f"/components/{c['slug']}.html",
                slug=c["slug"],
                category=c.get("category", ""),
            )
        )
    for g in store.guides():
        title = g.get("headline") or g.get("title", "").split("|")[0].strip()
        desc = g.get("lead") or g.get("meta_description", "")
        items.append(
            entry(
                "Guide",
                title,
                desc,
                f"/guides/{g['slug']}.html",
                slug=g["slug"],
                category=g.get("phase", "Guide"),
            )
        )
    for p in store.projects():
        cat = p.get("category", "")
        desc = p.get("description", p.get("desc", ""))
        snippet = f"{cat} · {desc}" if cat and desc else (desc or cat)
        items.append(
            entry(
                "Project",
                p["title"],
                snippet,
                f"/projects/{p['slug']}.html",
                slug=p["slug"],
                category=cat,
            )
        )
    for slug, page in store.pages().items():
        title = page.get("title", slug).split("|")[0].strip()
        desc = page.get("meta_description", "")
        if slug not in ("privacy", "terms", "disclaimer"):
            items.append(entry("Page", title, desc, f"/{slug}.html"))
    items.append(entry("Page", "All Projects", "Browse ESP32 project library", "/projects.html"))
    items.append(entry("Page", "Component Encyclopedia", "Sensors, displays, motors and more", "/components.html"))
    items.append(entry("Download", "GitHub Repository", "Code templates and project source", "https://github.com/abdulmubeen7876773-dotcom/esp32"))
    return items


def search_page_html() -> str:
    from site_layout import SITE_NAME, footer_html, head_html, header_html, organization_schema, webpage_schema

    title = f"Search | {SITE_NAME}"
    desc = "Search components, projects, guides, downloads, and news on ESP32 Engine."
    schema = organization_schema() + webpage_schema(title, desc, "search.html")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="search.html", extra_schema=schema)}
</head>
<body>
<main>
{header_html("home")}
<section class="section-block wrap page-head">
  <h1>Search</h1>
  <form class="search-overlay-form" action="/search.html" method="get" style="max-width:640px">
    <input id="search-page-input" name="q" type="search" placeholder="Search everything…" autocomplete="off" style="flex:1;padding:0.85rem 1rem;border-radius:14px;border:2px solid var(--border);font-size:1.125rem">
    <button type="submit" class="btn btn-primary">Search</button>
  </form>
  <div class="search-results" id="search-page-results"></div>
</section>
</main>
{footer_html()}
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
</body>
</html>"""


def main():
    assert_phase1_static()
    items = build_index()
    INDEX_OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    SEARCH_PAGE.write_text(search_page_html(), encoding="utf-8")
    print(f"Wrote search-index.json ({len(items)} items) + search.html")


if __name__ == "__main__":
    main()
