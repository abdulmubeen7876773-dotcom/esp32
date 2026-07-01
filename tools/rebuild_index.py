import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_icons import pick_icon, thumb_class as icon_thumb_class, featured_cat_bar, slug_cat
from parent_registry import PARENTS
from content_store import get_content_store
from site_layout import (
    modern_card,
    footer_html,
    head_html,
    hero_html,
    header_html,
    organization_schema,
    website_schema,
    CSS_VERSION,
    short_category,
    read_time_label,
    home_featured_carousel,
    home_learning_paths_section,
    home_parents_section,
    home_teachers_section,
    home_components_section,
    home_featured_projects_section,
    home_latest_guides_section,
    home_newsletter_section,
    home_v2_declaration,
    home_v2_proof,
    home_v2_invitation,
    home_v2_showcase_js,
    card_media_html,
    home_v3_journey,
    home_v3_roadmap,
    home_v3_academy,
    home_v3_mission_feature,
    home_v3_top_picks,
    home_v3_why,
    home_v3_progress,
    PROJECTS_PAGE_SIZE,
    pagination_head_links,
    pagination_nav_html,
    projects_page_path,
    projects_page_canonical,
    sidebar_categories_html,
    filters_bar_html,
    category_hero_html,
    esc as layout_esc,
    UI_JS_SRC,
    SEARCH_JS_SRC,
)

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
INDEX_OUT = ROOT / "index.html"
PROJECTS_OUT = ROOT / "projects.html"
PROJECTS_JSON_OUT = ROOT / "projects.json"
PROJECT_ICONS_JS_OUT = ROOT / "project-icons.js"

CATEGORIES = [
    "Agriculture",
    "Home Automation",
    "Security Projects",
    "IoT Projects",
    "Sensor Projects",
    "Robotics",
    "Industrial Automation",
    "LED Projects",
    "ESP32-CAM",
    "AI Projects",
    "Energy Monitoring",
    "Healthcare",
    "Environmental",
    "Smart City",
    "Education",
]


def esc(t):
    return html.escape(t or "", quote=True)


def sort_projects(projects: list) -> list:
    return sorted(projects, key=lambda p: (not p.get("featured"), p.get("slug", "")))


def parse_card(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"<h1>([^<]+)</h1>", raw)
    lead_m = re.search(r'<p class="article-lead">([^<]+)</p>', raw) or re.search(r'<p class="lead">([^<]+)</p>', raw)
    category = "ESP32"
    difficulty = "Beginner"
    tags = [t for t in re.findall(r'<span class="tag leaf">([^<]+)</span>', raw) if t.lower() not in ("part",)]
    clay = re.findall(r'<span class="tag clay">([^<]+)</span>', raw)
    if tags:
        category = tags[0]
    if clay:
        difficulty = clay[0].replace(" build", "")
    meta_m = re.search(r'<p class="article-meta">([^<]+)</p>', raw)
    if meta_m:
        parts = [p.strip() for p in meta_m.group(1).split("·")]
        if parts and parts[0] not in ("ESP32", "Project") and category in ("ESP32", ""):
            category = parts[0]
        if len(parts) > 1:
            difficulty = parts[1].replace(" build", "").strip()
    if category in ("ESP32", ""):
        bc = re.search(r'"position": 2, "name": "([^<"]+)"', raw)
        if bc and bc.group(1) not in ("Home",):
            category = bc.group(1)
    if tags and category == "ESP32":
        category = tags[0]
    if clay and difficulty == "Beginner" and clay:
        difficulty = clay[0].replace(" build", "")
    cat_link = re.search(r'index\.html#cat-[^"]+">([^<]+)</a>', raw)
    if cat_link and category in ("ESP32", ""):
        category = cat_link.group(1).strip()
    return {
        "href": f"projects/{path.name}",
        "title": title_m.group(1).strip() if title_m else path.stem,
        "desc": lead_m.group(1).strip() if lead_m else "",
        "category": category,
        "difficulty": difficulty,
        "slug": path.stem,
        "featured": is_flagship(path.stem),
    }


def thumb_class(cat):
    return icon_thumb_class(cat)


def thumb_icon(category, cls="thumb"):
    tc = thumb_class(category)
    return f'<div class="{cls} {tc}">{pick_icon(category)}</div>'


def latest_item(p):
    return f"""<a class="latest-item" href="{esc(p['href'])}">{thumb_icon(p['category'], 'thumb thumb-sm')}<div class="latest-body"><span class="latest-cat">{esc(p['category'])}</span><h3>{esc(p['title'])}</h3></div></a>"""


def pick_diverse_latest(by_cat, projects, count=4):
    picked = []
    seen = set()
    for cat in CATEGORIES:
        items = by_cat.get(cat, [])
        if not items:
            continue
        p = items[0]
        key = re.sub(r"\s+project\s+\d+$", "", p["title"].lower())
        if key in seen:
            continue
        picked.append(p)
        seen.add(key)
        if len(picked) >= count:
            return picked
    for p in projects:
        key = re.sub(r"\s+project\s+\d+$", "", p["title"].lower())
        if key in seen:
            continue
        picked.append(p)
        seen.add(key)
        if len(picked) >= count:
            break
    return picked


def post_card(p):
    return modern_card(p, "post-card", "post-thumb")


LEVELS = ["Beginner", "Intermediate", "Advanced"]


def parent_listing_record(parent: dict) -> dict:
    desc = parent["description"]
    if len(desc) > 120:
        desc = desc[:117].rstrip() + "…"
    return {
        "href": f"projects/{parent['slug']}.html",
        "title": parent["title"],
        "desc": desc,
        "description": parent.get("description", desc),
        "category": parent["category"],
        "slug": parent["slug"],
        "featured": bool(parent.get("featured")),
        "featured_image": parent.get("featured_image") or parent.get("image") or "",
        "levels": LEVELS,
        "readMin": 12,
    }


def portal_carousel_card(p: dict) -> str:
    tc = icon_thumb_class(p["category"])
    icon = pick_icon(p["category"])
    return f"""<a class="carousel-card product-card" href="{esc(p['href'])}">
<span class="product-card-glow" aria-hidden="true"></span>
<span class="carousel-card-thumb {tc}">{icon}</span>
<span class="carousel-card-body">
<span class="card-badges"><span class="badge badge-cat">{esc(short_category(p['category']))}</span><span class="badge badge-beginner">3 Levels</span></span>
<strong>{esc(p['title'])}</strong>
<span class="carousel-card-meta">Beginner · Intermediate · Advanced</span>
</span></a>"""


def parent_grid_card(p: dict) -> str:
    levels_html = "".join(
        f'<span class="badge badge-{lv.lower()}">{esc(lv)}</span>' for lv in p.get("levels", LEVELS)
    )
    attrs = (
        f' data-title="{esc(p["title"].lower())}"'
        f' data-category="{esc(p["category"])}"'
        f' data-levels="{esc(",".join(p.get("levels", LEVELS)))}"'
        f' data-featured="{1 if p.get("featured") else 0}"'
    )
    tc = icon_thumb_class(p["category"])
    icon = pick_icon(p["category"])
    media = card_media_html(
        p["category"],
        p.get("slug", ""),
        p.get("featured_image") or p.get("image") or "",
    )
    desc = esc(p.get("desc", ""))
    rt = esc(read_time_label("Beginner", p.get("slug", "")))
    feat = '<span class="badge badge-featured">Featured</span>' if p.get("featured") else ""
    return f"""<a class="card project-card modern-card project-card-item" href="{esc(p['href'])}"{attrs}>
<div class="card-media-wrap">{media}</div>
<div class="card-body"><div class="card-badges">{feat}<span class="badge badge-cat">{esc(short_category(p['category']))}</span>{levels_html}<span class="badge badge-time">{rt}</span></div>
<h3>{esc(p['title'])}</h3>
<p class="card-desc">{desc}</p>
<div class="card-footer"><span class="btn btn-card">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


def project_json_record(p: dict) -> dict:
    desc = p.get("desc", "")
    if len(desc) > 120:
        desc = desc[:117].rstrip() + "…"
    return {
        "href": p["href"],
        "title": p["title"],
        "desc": desc,
        "category": p["category"],
        "slug": p["slug"],
        "levels": p.get("levels", LEVELS),
        "readMin": p.get("readMin", 12),
        "featured": bool(p.get("featured")),
        "featured_image": p.get("featured_image") or p.get("image") or "",
    }


def write_projects_json(projects: list) -> None:
    records = [project_json_record(p) for p in projects]
    PROJECTS_JSON_OUT.write_text(json.dumps(records, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def write_project_icons_js(projects: list) -> None:
    cats = set(CATEGORIES)
    for p in projects:
        cats.add(p["category"])
    icons = {"__default__": pick_icon("ESP32")}
    thumbs = {}
    for cat in sorted(cats, key=str.casefold):
        icons[cat] = pick_icon(cat)
        thumbs[cat] = icon_thumb_class(cat)
    body = "window.PROJECT_ICONS=" + json.dumps(icons, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + ";\n"
    body += "window.PROJECT_THUMBS=" + json.dumps(thumbs, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + ";\n"
    PROJECT_ICONS_JS_OUT.write_text(body, encoding="utf-8")


def projects_text_index(projects: list) -> str:
    items = "".join(
        f'<li><a href="{esc(p["href"])}">{esc(p["title"])}</a> <span class="meta">({esc(p["category"])})</span></li>'
        for p in projects
    )
    return f'<div id="project-text-index" class="project-text-index hidden" aria-label="Plain text project index"><ul>{items}</ul></div>'


def home_html(projects):
    store = get_content_store()
    home = store.home()
    desc = home.get(
        "meta_description",
        "Build, connect, and automate with ESP32. 15 parent projects with Beginner, Intermediate, and Advanced stages for makers, students, and engineers.",
    )
    title = home.get("meta_title", "ESP32 Engine — Build, Connect & Automate with ESP32")
    schema = organization_schema() + website_schema()
    guides = store.guides()
    components = store.components()
    catalog = store.projects()
    project_count = len(projects)
    guide_count = len(guides)
    component_count = len(components)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="/", extra_schema=schema, include_index_redirect=True)}
<link rel="preload" as="image" href="/assets/images/heroes/home-hero.webp" type="image/webp" fetchpriority="high">
</head>
<body class="home-page">
<main>
{header_html("home", project_count=project_count)}
{home_v2_declaration()}
{home_v2_proof()}
{home_v3_journey()}
{home_v3_roadmap(guides)}
{home_v3_academy()}
{home_v3_top_picks(catalog, guides, components)}
{home_v3_mission_feature(guides)}
{home_v3_why()}
{home_v3_progress(project_count, guide_count, component_count)}
{home_v2_invitation()}
</main>
{footer_html()}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
{home_v2_showcase_js()}
</body>
</html>
"""


def projects_listing_html(
    cat_opts,
    page_projects: list,
    page: int,
    total_pages: int,
    total_count: int,
    text_index: str = "",
):
    page_label = f" — Page {page}" if total_pages > 1 else ""
    desc = (
        f"Browse {total_count} ESP32 project tutorials — wiring tables, Arduino code, "
        f"and Beginner, Intermediate, and Advanced stages.{f' Page {page} of {total_pages}.' if total_pages > 1 else ''}"
    )
    schema = organization_schema() + website_schema()
    preview = "\n".join(parent_grid_card(p) for p in page_projects)
    canon = projects_page_canonical(page)
    title = f"ESP32 Projects — {total_count} Tutorials | ESP32 Engine{page_label}"
    page_links = pagination_head_links(page, total_pages, lambda n: projects_page_path(n))
    pagination = pagination_nav_html(page, total_pages, projects_page_path)
    filters = filters_bar_html(True).replace(
        '<select id="cat" aria-label="Filter by category"><option value="">All categories</option></select>',
        f'<select id="cat" aria-label="Filter by category"><option value="">All categories</option>{cat_opts}</select>',
    )
    hero = category_hero_html(
        "ESP32 Project Library",
        f"Browse {total_count} hands-on ESP32 tutorials with wiring diagrams, Arduino code, and Beginner, Intermediate, and Advanced build stages.",
        "IoT Projects",
        f'<span class="badge badge-light">{total_count} Projects</span><span class="badge badge-light">3 Levels Each</span><span class="badge badge-light">Free &amp; Open</span>',
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path=canon, extra_schema=schema)}
{page_links}
</head>
<body class="projects-page">
<main>
{header_html("projects", project_count=total_count)}
{hero}
<div class="layout-with-sidebar wrap">
  {sidebar_categories_html("projects")}
  <div class="main-with-sidebar">
    <div class="filters-sticky">{filters}</div>
    <section class="section-block">
      <div class="grid grid-projects" id="grid">{preview}</div>
      <div class="section-actions" id="projects-more-wrap"><button type="button" class="btn btn-secondary" id="projects-load-more">Load More</button></div>
      {text_index}
      {pagination}
      <noscript><p class="meta">JavaScript is required for filters. Use the <a href="sitemap.html">sitemap</a>.</p></noscript>
    </section>
  </div>
</div>
</main>
{footer_html()}
<script src="/project-icons.js" defer></script>
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
<script src="/projects.js" defer></script>
</body>
</html>
"""


def cleanup_old_project_pages():
    for path in ROOT.glob("projects-page-*.html"):
        path.unlink()


def write_project_listing_pages(projects: list, cat_opts: str, text_index: str) -> int:
    total = len(projects)
    total_pages = max(1, (total + PROJECTS_PAGE_SIZE - 1) // PROJECTS_PAGE_SIZE)
    cleanup_old_project_pages()
    for page in range(1, total_pages + 1):
        start = (page - 1) * PROJECTS_PAGE_SIZE
        chunk = projects[start : start + PROJECTS_PAGE_SIZE]
        html_out = projects_listing_html(cat_opts, chunk, page, total_pages, total, text_index if page == 1 else "")
        out = ROOT / projects_page_path(page)
        out.write_text(html_out, encoding="utf-8")
    return total_pages


def main():
    projects = [parent_listing_record(p) for p in PARENTS]
    cat_opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in CATEGORIES)
    text_index = projects_text_index(projects)
    INDEX_OUT.write_text(home_html(projects), encoding="utf-8")
    write_projects_json(projects)
    write_project_icons_js(projects)
    pages = write_project_listing_pages(projects, cat_opts, text_index)
    print(f"Wrote index.html + projects listing ({len(projects)} projects, {pages} page(s)) + projects.json")
    import build_categories
    import build_feed
    import build_sitemap
    import ping_indexnow

    build_categories.main()
    build_feed.main()
    build_sitemap.main()
    ping_indexnow.main()


if __name__ == "__main__":
    main()
