"""Explicit selective generation; never rewrite unrelated articles or feed items.

Full validation and build/release reports remain the responsibility of build_all.
Unscoped builds retain their existing behavior.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def generate_scope(manifest: Path):
    from content_store import get_content_store
    from build_guides import render_guide, render_guides_index
    from rebuild_parents import render_golden_parent
    from build_search_index import build_index
    from project_text import public_projects
    import rebuild_index as listing
    import build_categories as categories
    from build_feed import feed_item

    scope = json.loads(manifest.read_text(encoding="utf-8"))
    required = {"guides", "projects", "categories"}
    if set(scope) not in (required, required | {"components"}):
        raise ValueError("Scope requires guides, projects and categories; components is optional")
    if any(not isinstance(v, list) or any(not isinstance(s, str) for s in v)
           for v in scope.values()):
        raise ValueError("Scope values must be lists of names")
    store = get_content_store()
    guides = {g["slug"]: g for g in store.guides()}
    projects = {p["slug"]: p for p in public_projects(store.projects())}
    components = {c["slug"]: c for c in store.components()}
    selected_components = scope.get("components", [])
    unknown_components = set(selected_components) - set(components)
    if unknown_components:
        raise ValueError(f"Unknown components: {sorted(unknown_components)}")
    for key, available in (("guides", guides), ("projects", projects),
                           ("categories", listing.CATEGORIES)):
        unknown = set(scope[key]) - set(available)
        if unknown:
            raise ValueError(f"Unknown {key}: {sorted(unknown)}")

    def write(relative, body):
        path = ROOT / relative
        if not path.exists() or path.read_text(encoding="utf-8") != body:
            path.write_text(body, encoding="utf-8")
        print(f"Scoped output: {relative}")

    if selected_components:
        from build_components import component_page_html, index_html
        from build_static_pages import cms_page_html

        # Catalog additions also change adjacent previous/next links. Use the
        # existing renderer for the catalog, writing only differing outputs.
        catalog = list(components.values())
        for i, component in enumerate(catalog):
            previous = catalog[i - 1] if i else None
            following = catalog[i + 1] if i + 1 < len(catalog) else None
            write(f"components/{component['slug']}.html",
                  component_page_html(component, previous, following))
        write("components.html", index_html(catalog, store.component_categories()))
        write("search-index.json", json.dumps(build_index(), ensure_ascii=False, indent=2))
        records = [listing.parent_listing_record(p) for p in projects.values()]
        write("index.html", listing.home_html(records))
        for slug in ("about", "learning"):
            write(f"{slug}.html", cms_page_html(store.pages()[slug]))

        # A component-only release must not regenerate unrelated guides,
        # project listings or RSS. Legacy three-key scopes retain their path.
        if not any(scope[k] for k in required):
            validate_sitemap(scope)
            return

    for slug in scope["guides"]:
        write(f"guides/{slug}.html", render_guide(guides[slug]))
    for slug in scope["projects"]:
        write(f"projects/{slug}.html", render_golden_parent(projects[slug]))
    write("guides.html", render_guides_index(store.guides()))
    write("search-index.json", json.dumps(build_index(), ensure_ascii=False, indent=2))
    records = [listing.parent_listing_record(p) for p in projects.values()]
    write("projects.json", json.dumps([listing.project_json_record(p) for p in records],
                                      ensure_ascii=False, separators=(",", ":")))
    options = "".join(f'<option value="{listing.esc(c)}">{listing.esc(c)}</option>'
                      for c in listing.CATEGORIES)
    # Use the established pagination generator, not a one-page assumption.
    listing.write_project_listing_pages(records, options, listing.projects_text_index(records))
    write("index.html", listing.home_html(records))
    for category in scope["categories"]:
        write(f"category/{categories.slug_cat(category)}.html",
              categories.render_category_page(category, categories.projects_for_category(category)))

    # Replace only selected existing RSS items. Keep unrelated historical dates.
    feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
    for slug in scope["projects"]:
        pattern = r"    <item>.*?    </item>"
        found = [item for item in re.findall(pattern, feed, re.S)
                 if f"/projects/{slug}.html</link>" in item]
        if len(found) != 1:
            raise ValueError(f"Scoped RSS requires one existing item: {slug}")
        feed = feed.replace(found[0], feed_item(projects[slug]))
    write("feed.xml", feed)

    # Already-reviewed sitemap is authoritative for this selective release.
    # Verify all selected URLs exist instead of replacing unrelated lastmod dates.
    validate_sitemap(scope)


def validate_sitemap(scope: dict):
    import xml.etree.ElementTree as ET
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)}
    for kind in ("guides", "projects", "components"):
        for slug in scope.get(kind, []):
            if f"https://esp32engine.com/{kind}/{slug}.html" not in urls:
                raise ValueError(f"Scoped sitemap is missing {kind}/{slug}.html")
