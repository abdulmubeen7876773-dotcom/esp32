"""Explicit selective generation; never rewrite unrelated articles or feed items.

Full validation and build/release reports remain the responsibility of build_all.
Unscoped builds retain their existing behavior.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def component_sitemap_lastmods(sitemap: str, components: list[dict]) -> str:
    """Update existing selected dates without reserializing unrelated XML."""
    from datetime import date

    dates = {}
    for component in components:
        value = str(component.get("date_modified", ""))
        dates[f"https://esp32engine.com/components/{component['slug']}.html"] = date.fromisoformat(value).isoformat()
    seen = {url: 0 for url in dates}

    def update(match):
        block = match.group(0)
        loc = re.search(r"<loc>\s*([^<]+?)\s*</loc>", block)
        if not loc or loc.group(1) not in dates:
            return block
        url = loc.group(1)
        seen[url] += 1
        block, count = re.subn(r"(<lastmod>)[^<]*(</lastmod>)",
                               lambda item: item[1] + dates[url] + item[2], block)
        if count != 1:
            raise ValueError(f"Component update requires one existing lastmod: {url}")
        return block

    result = re.sub(r"<url\b[^>]*>.*?</url>", update, sitemap, flags=re.S)
    if any(count != 1 for count in seen.values()):
        raise ValueError("Component update requires one existing sitemap entry per selected component")
    return result


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
    if set(scope) not in (required, required | {"components"}, required | {"homepage"}, required | {"navigation"}, required | {"pages"}, required | {"guide_catalog_only"}, required | {"components", "component_updates_only"}, required | {"guide_catalog_only", "pages", "refresh_project_counts"}):
        raise ValueError("Scope requires guides, projects and categories; optional selectors include components with component_updates_only, homepage, navigation, pages or guide_catalog_only")
    if "navigation" in scope and (scope["navigation"] is not True or any(scope[k] for k in required)):
        raise ValueError("Navigation-only scope requires true and empty article selections")
    if "homepage" in scope and scope["homepage"] is not True:
        raise ValueError("Homepage-only scope must set homepage to true")
    if "guide_catalog_only" in scope and (scope["guide_catalog_only"] is not True or not scope["guides"] or scope["projects"] or scope["categories"]):
        raise ValueError("Guide catalog scope requires true, selected guides and no projects/categories")
    if "refresh_project_counts" in scope and scope["refresh_project_counts"] is not True:
        raise ValueError("Project count refresh must be true")
    if "component_updates_only" in scope and (scope["component_updates_only"] is not True or not scope["components"] or any(scope[k] for k in required)):
        raise ValueError("Component update scope requires true, selected components and empty guide/project/category selections")
    if any(not isinstance(v, list) or any(not isinstance(s, str) for s in v)
           for k, v in scope.items() if k not in {"homepage", "navigation", "guide_catalog_only", "component_updates_only", "refresh_project_counts"}):
        raise ValueError("Scope values must be lists of names")
    if scope.get("component_updates_only") and len(set(scope["components"])) != len(scope["components"]):
        raise ValueError("Component update scope cannot select a component twice")
    store = get_content_store()
    guides = {g["slug"]: g for g in store.guides()}
    projects = {p["slug"]: p for p in public_projects(store.projects())}
    components = {c["slug"]: c for c in store.components()}
    pages = store.pages()
    unknown_pages = set(scope.get("pages", [])) - set(pages)
    if unknown_pages:
        raise ValueError(f"Unknown pages: {sorted(unknown_pages)}")
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

    if scope.get("navigation"):
        from project_catalog import generate_navigation_scope
        generate_navigation_scope()
        validate_sitemap(scope)
        return

    if scope.get("homepage"):
        if any(scope[k] for k in required):
            raise ValueError("Homepage-only scope cannot also select articles")
        records = [listing.parent_listing_record(p) for p in projects.values()]
        write("index.html", listing.home_html(records))
        validate_sitemap(scope)
        return

    if scope.get("component_updates_only"):
        from build_components import component_page_html, index_html

        # Existing-record edits only: additions/reordering need the broader
        # catalog scope so that other previous/next links can be refreshed.
        catalog = list(components.values())
        for slug in selected_components:
            if not (ROOT / "components" / f"{slug}.html").is_file():
                raise ValueError(f"Component update requires an existing page: {slug}")
        validate_sitemap(scope)
        sitemap = component_sitemap_lastmods(
            (ROOT / "sitemap.xml").read_text(encoding="utf-8"),
            [components[slug] for slug in selected_components])
        for i, component in enumerate(catalog):
            if component["slug"] in selected_components:
                previous = catalog[i - 1] if i else None
                following = catalog[i + 1] if i + 1 < len(catalog) else None
                write(f"components/{component['slug']}.html",
                      component_page_html(component, previous, following))
        write("components.html", index_html(catalog, store.component_categories()))
        write("sitemap.xml", sitemap)
        return

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
    if scope.get("pages"):
        from build_static_pages import cms_page_html

        for slug in scope["pages"]:
            write(f"{slug}.html", cms_page_html(pages[slug]))
    write("guides.html", render_guides_index(store.guides()))
    write("search-index.json", json.dumps(build_index(), ensure_ascii=False, indent=2))
    if scope.get("guide_catalog_only"):
        # A guide review must not import unrelated homepage/project drift.
        # Keep full content/release validation in build_all and normal scopes.
        validate_sitemap(scope)
        if scope.get("refresh_project_counts"):
            import xml.etree.ElementTree as ET
            from urllib.parse import urlsplit

            # Update only the shared count label, never regenerate unrelated bodies.
            count = len(projects)
            for entry in ET.parse(ROOT / "sitemap.xml").findall("{*}url/{*}loc"):
                path = ROOT / urlsplit(entry.text).path.lstrip("/")
                if path.is_dir():
                    path /= "index.html"
                before = path.read_text(encoding="utf-8")
                after, found = re.subn(
                    r'(<a\b[^>]*\bclass="[^"]*\bnav-spotlight-badge\b[^"]*"[^>]*>)\d+ Projects(</a>)',
                    lambda match: match[1] + f"{count} Projects" + match[2], before)
                if found != 1:
                    raise ValueError(f"Expected one project count badge: {path}")
                if after != before:
                    write(path.relative_to(ROOT), after)
        return
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
    for slug in scope.get("pages", []):
        if f"https://esp32engine.com/{slug}.html" not in urls:
            raise ValueError(f"Scoped sitemap is missing {slug}.html")
