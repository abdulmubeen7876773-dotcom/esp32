import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_icons import pick_icon, thumb_class as icon_thumb_class, featured_cat_bar, category_cards_html, slug_cat
from parent_registry import PARENTS
from site_layout import modern_card, stats_html, footer_html, read_time_label, read_time_minutes, category_section_title, head_html, hero_html, header_html, organization_schema, website_schema, CSS_VERSION, short_category

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
        "category": parent["category"],
        "slug": parent["slug"],
        "levels": LEVELS,
        "readMin": 12,
    }


def parent_grid_card(p: dict) -> str:
    levels_html = "".join(
        f'<span class="badge badge-{lv.lower()}">{esc(lv)}</span>' for lv in p.get("levels", LEVELS)
    )
    attrs = (
        f' data-title="{esc(p["title"].lower())}"'
        f' data-category="{esc(p["category"])}"'
        f' data-levels="{esc(",".join(p.get("levels", LEVELS)))}"'
    )
    tc = icon_thumb_class(p["category"])
    icon = pick_icon(p["category"])
    desc = esc(p.get("desc", ""))
    return f"""<a class="card project-card modern-card parent-card compact-card" href="{esc(p['href'])}"{attrs}>
<div class="card-thumb {tc}">{icon}</div>
<div class="card-body"><div class="card-badges"><span class="badge badge-cat">{esc(short_category(p['category']))}</span>{levels_html}</div>
<h3>{esc(p['title'])}</h3>
<p class="card-desc">{desc}</p>
<div class="card-footer"><span class="card-read-more">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


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
    for cat in cats:
        icons[cat] = pick_icon(cat)
        thumbs[cat] = icon_thumb_class(cat)
    body = "window.PROJECT_ICONS=" + json.dumps(icons, ensure_ascii=False, separators=(",", ":")) + ";\n"
    body += "window.PROJECT_THUMBS=" + json.dumps(thumbs, ensure_ascii=False, separators=(",", ":")) + ";\n"
    PROJECT_ICONS_JS_OUT.write_text(body, encoding="utf-8")


def projects_text_index(projects: list) -> str:
    items = "".join(
        f'<li><a href="{esc(p["href"])}">{esc(p["title"])}</a> <span class="meta">({esc(p["category"])})</span></li>'
        for p in projects
    )
    return f'<div id="project-text-index" class="project-text-index hidden" aria-label="Plain text project index"><ul>{items}</ul></div>'


def home_featured_section(projects: list) -> str:
    cards = "".join(parent_grid_card(p) for p in projects)
    return f"""<section class="section-block wrap reveal compact-section" id="featured">
  <div class="section-title"><h2>ESP32 Projects</h2><a class="view-all" href="projects.html">View All »</a></div>
  <div class="post-grid-4 grid-compact home-project-grid" id="home-grid" data-initial="6">{cards}</div>
  <div class="section-actions" id="home-more-wrap"><button type="button" class="btn btn-secondary btn-sm" id="home-load-more">Load More Projects</button></div>
</section>"""


def projects_listing_html(cat_opts, preview_cards="", text_index=""):
    desc = "Browse 15 ESP32 parent projects — each with Beginner, Intermediate, and Advanced build stages, wiring tables, and Arduino code."
    schema = organization_schema() + website_schema()
    initial = preview_cards or '<p class="meta grid-loading">Loading project library…</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "ESP32 Projects — 15 Parent Tutorials with 3 Skill Levels | ESP32 Library", desc, canonical_path="projects.html", extra_schema=schema)}
</head>
<body>
<main>
{header_html("projects")}
<section class="section-block wrap page-head page-head-compact">
  <p class="hero-eyebrow">Project Directory</p>
  <h1>Browse ESP32 Projects</h1>
  <p class="hero-sub">15 guides with Beginner, Intermediate, and Advanced stages.</p>
</section>
<div class="filters-sticky">
  <div class="wrap">
    <div class="search-panel search-panel-compact">
      <input id="q" placeholder="Search ESP32 projects…" aria-label="Search projects">
      <select id="cat" aria-label="Filter by category"><option value="">All categories</option>{cat_opts}</select>
      <select id="diff" aria-label="Filter by difficulty stage"><option value="">All difficulty stages</option><option value="Beginner">Beginner</option><option value="Intermediate">Intermediate</option><option value="Advanced">Advanced</option></select>
    </div>
    <p class="meta filter-meta" id="count">Loading projects…</p>
  </div>
</div>
<section class="section-block wrap section-block-compact">
  <div class="grid grid-compact" id="grid">{initial}</div>
  <div class="section-actions" id="projects-more-wrap"><button type="button" class="btn btn-secondary btn-sm" id="projects-load-more">Load More</button></div>
  {text_index}
  <noscript><p class="meta">JavaScript is required for card view and filters. Use the plain-text project index above or the <a href="sitemap.html">sitemap</a>.</p></noscript>
</section>
</main>
{footer_html()}
<script src="project-icons.js" defer></script>
<script src="ui.js" defer></script>
<script src="projects.js" defer></script>
</body>
</html>
"""


def home_html(projects, latest):
    desc = "Build, connect, and automate with ESP32. 15 parent projects with Beginner, Intermediate, and Advanced stages for makers, students, and engineers."
    latest_html = "".join(latest_item(p) for p in latest[:3])
    schema = organization_schema() + website_schema()
    featured = home_featured_section(projects)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "ESP32 Project Library — Build, Connect & Automate with ESP32", desc, canonical_path="index.html", extra_schema=schema, include_gsc=True)}
</head>
<body>
<main>
{header_html("home")}
{hero_html(latest_html)}
{stats_html()}
{category_cards_html()}
{featured}
<section class="section-block wrap browse-cta reveal">
  <div class="cta-box cta-box-compact">
    <h2>Browse all {len(projects)} ESP32 projects</h2>
    <p>Search by category or difficulty — wiring tables and Arduino code included.</p>
    <a class="btn btn-primary btn-sm" href="projects.html">View all projects</a>
  </div>
</section>
</main>
{footer_html()}
<script src="ui.js" defer></script>
</body>
</html>
"""


def main():
    projects = [parent_listing_record(p) for p in PARENTS]
    by_cat = defaultdict(list)
    for p in projects:
        by_cat[p["category"]].append(p)
    latest = projects[:3]
    cat_opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in CATEGORIES)
    preview = "\n".join(parent_grid_card(p) for p in projects)
    text_index = projects_text_index(projects)
    INDEX_OUT.write_text(home_html(projects, latest), encoding="utf-8")
    write_projects_json(projects)
    write_project_icons_js(projects)
    PROJECTS_OUT.write_text(projects_listing_html(cat_opts, preview, text_index), encoding="utf-8")
    print(f"Wrote index.html + projects.html + projects.json ({len(projects)} parent projects)")
    import build_sitemap

    build_sitemap.main()


if __name__ == "__main__":
    main()
