import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_icons import pick_icon, thumb_class as icon_thumb_class, featured_cat_bar, category_cards_html, slug_cat
from site_layout import modern_card, stats_html, footer_html, read_time_label, read_time_minutes, category_section_title, head_html, hero_html, CSS_VERSION

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


def grid_card(p):
    attrs = f' data-title="{esc(p["title"].lower())}" data-category="{esc(p["category"])}" data-difficulty="{esc(p["difficulty"])}"'
    return modern_card(p, "card project-card", "card-thumb", extra_attrs=attrs, show_desc=True)


def project_json_record(p: dict) -> dict:
    desc = p.get("desc", "")
    if len(desc) > 100:
        desc = desc[:97].rstrip() + "…"
    diff = p.get("difficulty", "Beginner").replace(" build", "")
    return {
        "href": p["href"],
        "title": p["title"],
        "desc": desc,
        "category": p["category"],
        "difficulty": diff,
        "slug": p["slug"],
        "readMin": read_time_minutes(diff, p.get("slug", "")),
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


def projects_listing_html(cat_opts):
    desc = "Browse 1,000+ ESP32 projects with wiring diagrams, source code, and step-by-step tutorials for IoT, automation, robotics, and embedded systems."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "ESP32 Projects — Browse 1,000+ Tutorials | ESP32 Library", desc)}
</head>
<body>
<main>
{header_html("projects")}
<section class="section-block wrap page-head">
  <p class="hero-eyebrow">Project Directory</p>
  <h1>Browse ESP32 Projects</h1>
  <p class="hero-sub">Explore 1,000+ ESP32 projects — IoT tutorials, automation systems, robotics builds, and real-world engineering solutions.</p>
  <div class="search-panel">
    <input id="q" placeholder="Search ESP32 projects…" aria-label="Search projects">
    <select id="cat" aria-label="Filter by category"><option value="">All categories</option>{cat_opts}</select>
    <select id="diff" aria-label="Filter by difficulty"><option value="">All difficulty levels</option><option value="Beginner">Beginner</option><option value="Intermediate">Intermediate</option><option value="Advanced">Advanced</option></select>
  </div>
  <p class="meta" id="count" style="margin-top:12px">Loading projects…</p>
  <div class="grid" id="grid"><p class="meta grid-loading">Loading project library…</p></div>
  <noscript><p class="meta">Enable JavaScript to browse the project library, or open individual tutorials from the <a href="sitemap.xml">sitemap</a>.</p></noscript>
</section>
</main>
{footer_html()}
<script src="project-icons.js" defer></script>
<script src="ui.js" defer></script>
<script src="projects.js" defer></script>
</body>
</html>
"""


def header_html(active="home"):
    nav_home = ' class="active"' if active == "home" else ""
    nav_proj = ' class="active"' if active == "projects" else ""
    search_action = (
        "event.preventDefault();location.href='projects.html?q='+encodeURIComponent(this.querySelector('input').value);"
        if active == "home"
        else "event.preventDefault();var el=document.getElementById('q');if(el){el.value=this.querySelector('input').value;if(window.filterProjects){window.filterProjects();}else{el.dispatchEvent(new Event('input'));el.dispatchEvent(new Event('change'));}}"
    )
    return f"""<div class="site-nav-sticky">
<header class="site-header"><div class="wrap header-inner"><a class="site-logo" href="index.html"><span class="logo-mark" aria-hidden="true"></span>ESP32<span class="logo-accent">Library</span></a><button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button><nav class="top-nav" aria-label="Main"><a href="index.html"{nav_home}>Home</a><a href="projects.html"{nav_proj}>Projects</a><a href="about.html">About</a><a href="sitemap.xml">Sitemap</a></nav><form class="top-search" onsubmit="{search_action}"><input type="search" placeholder="Search projects…" aria-label="Search"><button type="submit" aria-label="Search">Search</button></form></div></header>
{featured_cat_bar("", active == "home", active == "projects")}
</div>"""


def home_html(projects, sections, latest):
    desc = "Build, connect, and automate with ESP32. 1,000+ IoT projects, tutorials, and open-source examples for makers, students, and engineers."
    latest_html = "".join(latest_item(p) for p in latest)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", "ESP32 Project Library — Build, Connect & Automate with ESP32", desc)}
</head>
<body>
<main>
{header_html("home")}
{hero_html(latest_html)}
{stats_html()}
{category_cards_html()}
{"".join(sections)}
<section class="section-block wrap browse-cta reveal">
  <div class="cta-box">
    <h2>Browse all {len(projects)} ESP32 projects</h2>
    <p>Use search and category filters to find the exact tutorial you need — wiring, code, and step-by-step guides included.</p>
    <a class="btn btn-primary" href="projects.html">View all projects</a>
  </div>
</section>
</main>
{footer_html()}
<script src="ui.js" defer></script>
</body>
</html>
"""


def main():
    files = sorted(PROJECTS.glob("*.html"))
    if not files:
        print("No projects found", file=sys.stderr)
        sys.exit(1)
    projects = [parse_card(f) for f in files]
    by_cat = defaultdict(list)
    for p in projects:
        by_cat[p["category"]].append(p)
    latest = pick_diverse_latest(by_cat, projects, 4)
    sections = []
    for cat in CATEGORIES:
        items = by_cat.get(cat, [])[:4]
        if not items:
            continue
        cards = "".join(post_card(p) for p in items)
        sections.append(
            f"""<section class="section-block wrap reveal" id="cat-{slug_cat(cat)}"><div class="section-title"><h2>{esc(category_section_title(cat))}</h2><a class="view-all" href="projects.html#cat-{slug_cat(cat)}">View All »</a></div><div class="post-grid-4">{cards}</div></section>"""
        )
    cat_opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in CATEGORIES)
    INDEX_OUT.write_text(home_html(projects, sections, latest), encoding="utf-8")
    write_projects_json(projects)
    write_project_icons_js(projects)
    PROJECTS_OUT.write_text(projects_listing_html(cat_opts), encoding="utf-8")
    print(f"Wrote index.html + projects.html shell + projects.json ({len(projects)} projects, {len(sections)} category sections)")


if __name__ == "__main__":
    main()
