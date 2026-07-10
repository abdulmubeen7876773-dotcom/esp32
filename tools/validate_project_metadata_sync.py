import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store
from project_icons import slug_cat
from project_text import (
    breadcrumb_label,
    card_description,
    html_page_title,
    is_golden_project,
    normalize_text,
    project_meta_description,
    project_title,
)

ROOT = Path(__file__).resolve().parent.parent


def strip_tags(value: str) -> str:
    return normalize_text(html.unescape(re.sub(r"<[^>]+>", "", value or "")))


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return strip_tags(match.group(1)) if match else ""


def meta_content(text: str, attr: str, value: str) -> str:
    pattern = rf'<meta\b(?=[^>]*\b{attr}="{re.escape(value)}")(?=[^>]*\bcontent="([^"]*)")[^>]*>'
    return html.unescape(re.search(pattern, text, re.I | re.S).group(1)).strip() if re.search(pattern, text, re.I | re.S) else ""


def json_ld_objects(text: str) -> list[dict]:
    objects: list[dict] = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            objects.append(data)
    return objects


def schema_by_type(objects: list[dict], schema_type: str) -> dict:
    for obj in objects:
        obj_type = obj.get("@type")
        if obj_type == schema_type or (isinstance(obj_type, list) and schema_type in obj_type):
            return obj
    return {}


def card_block(text: str, href: str) -> str:
    match = re.search(
        rf'<a\b(?=[^>]*class="[^"]*project-card-item[^"]*")(?=[^>]*href="{re.escape(href)}")[^>]*>.*?</a>',
        text,
        re.I | re.S,
    )
    return match.group(0) if match else ""


def main() -> int:
    store = get_content_store()
    projects = [p for p in store.projects() if is_golden_project(p)]
    by_slug = {p["slug"]: p for p in projects}
    errors: list[tuple[str, str, str, str]] = []

    def expect(slug: str, location: str, expected: str, actual: str) -> None:
        expected_n = normalize_text(expected)
        actual_n = normalize_text(actual)
        if expected_n != actual_n:
            errors.append((slug, location, expected_n, actual_n))

    search_path = ROOT / "search-index.json"
    search_rows = json.loads(search_path.read_text(encoding="utf-8")) if search_path.exists() else []
    search_by_slug = {
        row.get("slug"): row for row in search_rows if row.get("type") == "Project" and row.get("slug")
    }

    projects_json_path = ROOT / "projects.json"
    project_json_rows = json.loads(projects_json_path.read_text(encoding="utf-8")) if projects_json_path.exists() else []
    project_json_by_slug = {row.get("slug"): row for row in project_json_rows if row.get("slug")}

    for project in projects:
        slug = project["slug"]
        expected_title = project_title(project)
        expected_page_title = html_page_title(project)
        expected_desc = project_meta_description(project)
        expected_card_desc = card_description(project)

        if not project.get("meta_description"):
            expect(slug, "content/projects source meta_description", expected_desc, "")

        page_path = ROOT / "projects" / f"{slug}.html"
        if not page_path.exists():
            expect(slug, "projects/{slug}.html", "generated page exists", "missing")
            continue
        page = page_path.read_text(encoding="utf-8")
        schemas = json_ld_objects(page)

        expect(slug, f"projects/{slug}.html <h1>", expected_title, first_match(r"<h1[^>]*>(.*?)</h1>", page))
        expect(slug, f"projects/{slug}.html <title>", expected_page_title, first_match(r"<title>(.*?)</title>", page))
        expect(slug, f"projects/{slug}.html meta description", expected_desc, meta_content(page, "name", "description"))
        expect(slug, f"projects/{slug}.html og:title", expected_page_title, meta_content(page, "property", "og:title"))
        expect(slug, f"projects/{slug}.html og:description", expected_desc, meta_content(page, "property", "og:description"))
        expect(slug, f"projects/{slug}.html twitter:title", expected_page_title, meta_content(page, "name", "twitter:title"))
        expect(slug, f"projects/{slug}.html twitter:description", expected_desc, meta_content(page, "name", "twitter:description"))

        webpage = schema_by_type(schemas, "WebPage")
        if webpage:
            expect(slug, f"projects/{slug}.html WebPage.name", expected_page_title, webpage.get("name", ""))
            expect(slug, f"projects/{slug}.html WebPage.description", expected_desc, webpage.get("description", ""))
        article = schema_by_type(schemas, "TechArticle")
        if article:
            expect(slug, f"projects/{slug}.html TechArticle.headline", expected_title, article.get("headline", ""))
            expect(slug, f"projects/{slug}.html TechArticle.description", expected_desc, article.get("description", ""))
        howto = schema_by_type(schemas, "HowTo")
        if howto:
            expect(slug, f"projects/{slug}.html HowTo.name", f"How to build {expected_title}", howto.get("name", ""))
            expect(slug, f"projects/{slug}.html HowTo.description", expected_desc, howto.get("description", ""))
        crumbs = schema_by_type(schemas, "BreadcrumbList")
        if crumbs:
            items = crumbs.get("itemListElement", [])
            actual_crumb = items[-1].get("name", "") if items else ""
            expect(slug, f"projects/{slug}.html breadcrumb", breadcrumb_label(project), actual_crumb)

        related_blocks = re.findall(r'<a class="project-related-card" href="/projects/([^"]+)\.html">(.*?)</a>', page, re.S)
        for related_slug, block in related_blocks:
            target = by_slug.get(related_slug)
            if not target:
                continue
            expect(slug, f"projects/{slug}.html related project {related_slug} title", project_title(target), first_match(r"<h3>(.*?)</h3>", block))
            expect(slug, f"projects/{slug}.html related project {related_slug} description", card_description(target), first_match(r"<p>(.*?)</p>", block))

        search_row = search_by_slug.get(slug, {})
        expect(slug, "search-index.json title", expected_title, search_row.get("title", ""))
        expect(slug, "search-index.json desc", expected_desc, search_row.get("desc", ""))

        project_json = project_json_by_slug.get(slug, {})
        expect(slug, "projects.json title", expected_title, project_json.get("title", ""))
        expect(slug, "projects.json desc", card_description(project, 120), project_json.get("desc", ""))

    listing_pages = [ROOT / "projects.html"] + sorted((ROOT / "projects").glob("page-*.html"))
    listing_text = "\n".join(path.read_text(encoding="utf-8") for path in listing_pages if path.exists())
    for project in projects:
        slug = project["slug"]
        block = card_block(listing_text, f"projects/{slug}.html")
        if block:
            expect(slug, "projects listing card title", project_title(project), first_match(r"<h3>(.*?)</h3>", block))
            expect(slug, "projects listing card description", card_description(project, 120), first_match(r'<p class="card-desc">(.*?)</p>', block))

        category_path = ROOT / "category" / f"{slug_cat(project.get('category', ''))}.html"
        if category_path.exists():
            category_page = category_path.read_text(encoding="utf-8")
            block = card_block(category_page, f"../projects/{slug}.html")
            if block:
                expect(slug, f"{category_path.relative_to(ROOT)} card title", project_title(project), first_match(r"<h3>(.*?)</h3>", block))
                expect(slug, f"{category_path.relative_to(ROOT)} card description", card_description(project, 100), first_match(r'<p class="card-desc">(.*?)</p>', block))

    home_path = ROOT / "index.html"
    if home_path.exists():
        home = home_path.read_text(encoding="utf-8")
        data = first_match(r'<script type="application/json" id="home-recommendation-data">(.*?)</script>', home)
        if data:
            try:
                payload = json.loads(html.unescape(data))
            except json.JSONDecodeError:
                payload = {}
            for group in payload.values():
                card_sets = group.values() if isinstance(group, dict) else [group]
                for cards in card_sets:
                    if not isinstance(cards, list):
                        continue
                    for card in cards:
                        if not isinstance(card, dict):
                            continue
                        slug = str(card.get("href", "")).rsplit("/", 1)[-1].replace(".html", "")
                        project = by_slug.get(slug)
                        if project:
                            expect(slug, "homepage recommendation data title", project_title(project), card.get("title", ""))
                            expect(slug, "homepage recommendation data desc", card_description(project, 118), card.get("desc", ""))

    if errors:
        print("Project metadata drift found:")
        for slug, location, expected, actual in errors:
            print(f"- {slug} | {location}")
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
        return 1

    print(f"Project metadata sync passed for {len(projects)} Golden projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
