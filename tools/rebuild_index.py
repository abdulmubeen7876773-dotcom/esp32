import html
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_images import pick_image

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
INDEX_OUT = ROOT / "index.html"
PROJECTS_OUT = ROOT / "projects.html"
CSS_VERSION = "20260615-imgs"

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

THUMB = {
    "Agriculture": "t-agriculture",
    "Home Automation": "t-home",
    "Security Projects": "t-security",
    "IoT Projects": "t-iot",
    "Sensor Projects": "t-iot",
    "Robotics": "t-default",
    "Industrial Automation": "t-default",
    "LED Projects": "t-led",
    "ESP32-CAM": "t-cam",
    "AI Projects": "t-ai",
    "Energy Monitoring": "t-default",
    "Healthcare": "t-default",
    "Environmental": "t-agriculture",
    "Smart City": "t-iot",
    "Education": "t-default",
}

FILTER_SCRIPT = """
const q=document.getElementById('q'),cat=document.getElementById('cat'),diff=document.getElementById('diff'),cards=[...document.querySelectorAll('.project-card')],count=document.getElementById('count');
function slug(s){return s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
function f(){let s=q.value.toLowerCase(),c=cat.value,d=diff.value,n=0;cards.forEach(x=>{let ok=(!s||x.dataset.title.includes(s))&&(!c||x.dataset.category===c)&&(!d||x.dataset.difficulty===d);x.classList.toggle('hidden',!ok);if(ok)n++;});count.textContent=n+' projects found';}
[q,cat,diff].forEach(e=>e.addEventListener('input',f));
if(location.hash.startsWith('#cat-')){const h=location.hash.slice(5);for(const o of cat.options){if(slug(o.text)===h){cat.value=o.text;break;}}}
f();
"""


def esc(t):
    return html.escape(t or "", quote=True)


def slug_cat(cat):
    return re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")


def parse_card(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"<h1>([^<]+)</h1>", raw)
    lead_m = re.search(r'<p class="article-lead">([^<]+)</p>', raw) or re.search(r'<p class="lead">([^<]+)</p>', raw)
    meta_m = re.search(r'<p class="article-meta">([^<]+)</p>', raw)
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
    return THUMB.get(cat, "t-default")


def thumb_label(title, cat):
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title).split()
    short = " ".join(words[:3]).upper()
    return short[:18] or cat.upper()[:12]


def thumb_img(slug, title, cls="thumb"):
    url = pick_image(slug)
    return f'<div class="{cls}"><img src="{esc(url)}" alt="{esc(title)}" loading="lazy"></div>'


def latest_item(p):
    return f"""<a class="latest-item" href="{esc(p['href'])}">{thumb_img(p['slug'], p['title'], 'thumb thumb-sm')}<div class="latest-body"><span class="latest-cat">{esc(p['category'])}</span><h3>{esc(p['title'])}</h3></div></a>"""


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


def footer_html():
    return """<footer class="site-footer"><div class="wrap footer-grid"><div class="footer-brand"><strong>ESP32 Project Library</strong><p>1000 ESP32 tutorials with wiring diagrams, source code, and step-by-step build guides.</p></div><div class="footer-col"><h4>Explore</h4><a href="index.html">Home</a><a href="projects.html">All Projects</a><a href="sitemap.xml">Sitemap</a></div><div class="footer-col"><h4>Company</h4><a href="about.html">About Us</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy Policy</a><a href="disclaimer.html">Disclaimer</a></div></div><div class="wrap footer-bottom"><p>© 2026 ESP32 Project Library. All rights reserved.</p></div></footer>"""


def post_card(p):
    return f"""<a class="post-card" href="{esc(p['href'])}">{thumb_img(p['slug'], p['title'], 'post-thumb')}<h3>{esc(p['title'])}</h3></a>"""


def grid_card(p):
    return f"""<a class="card project-card" data-title="{esc(p['title'].lower())}" data-category="{esc(p['category'])}" data-difficulty="{esc(p['difficulty'])}" href="{esc(p['href'])}">{thumb_img(p['slug'], p['title'], 'card-thumb')}<div class="card-body"><span class="tag leaf">{esc(p['category'])}</span><span class="tag clay">{esc(p['difficulty'])}</span><h3>{esc(p['title'])}</h3><p>{esc(p['desc'])}</p></div></a>"""


def header_html(active="home"):
    cats = "".join(
        f'<a class="cat-pill" href="projects.html#cat-{slug_cat(c)}">{esc(c.upper())}</a>' for c in CATEGORIES
    )
    nav_home = ' class="active"' if active == "home" else ""
    nav_proj = ' class="active"' if active == "projects" else ""
    pill_home = " active" if active == "home" else ""
    pill_proj = " active" if active == "projects" else ""
    search_action = (
        "event.preventDefault();location.href='projects.html?q='+encodeURIComponent(this.querySelector('input').value);"
        if active == "home"
        else "event.preventDefault();document.getElementById('q').value=this.querySelector('input').value;document.getElementById('q').dispatchEvent(new Event('input'));"
    )
    return f"""<header class="site-header"><div class="wrap"><a class="site-logo" href="index.html">ESP32 PROJECT LIBRARY</a><nav class="top-nav"><a href="index.html"{nav_home}>Home</a><a href="projects.html"{nav_proj}>All Projects</a><a href="sitemap.xml">Sitemap</a></nav><form class="top-search" onsubmit="{search_action}"><input type="search" placeholder="Search…" aria-label="Search"><button type="submit">Search</button></form></div></header>
<nav class="cat-bar"><div class="wrap"><a class="cat-pill{pill_home}" href="index.html">HOME</a>{cats}<a class="cat-pill{pill_proj}" href="projects.html">ALL PROJECTS</a></div></nav>"""


def projects_listing_html(projects, cat_opts):
    all_cards = "".join(grid_card(p) for p in projects)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>All ESP32 Projects | ESP32 Project Library</title>
<meta name="description" content="Browse and search 1000 ESP32 project tutorials with filters for category and difficulty.">
<link rel="stylesheet" href="style.css?v={CSS_VERSION}">
<style>html,body{{background:#0f172a;color:#e2e8f0}}</style>
</head>
<body>
{header_html("projects")}
<section class="section-block wrap page-head">
  <h1>All ESP32 Projects</h1>
  <p class="meta">Search and filter {len(projects)} tutorial pages — wiring, code, parts lists, and step-by-step guides.</p>
  <div class="search-panel">
    <input id="q" placeholder="Search ESP32 projects…">
    <select id="cat"><option value="">All categories</option>{cat_opts}</select>
    <select id="diff"><option value="">All difficulty levels</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select>
  </div>
  <p class="meta" id="count" style="margin-top:12px"></p>
  <div class="grid" id="grid">{all_cards}</div>
</section>
{footer_html()}
<script>
{FILTER_SCRIPT}
const params=new URLSearchParams(location.search);if(params.get('q')){{q.value=params.get('q');f();}}
</script>
</body>
</html>
"""


def home_html(projects, sections, latest):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 Project Library | Learn ESP32 with 1000 Tutorials</title>
<meta name="description" content="Build, connect, and automate with ESP32 — 1000 IoT tutorials with wiring, code, and step-by-step guides.">
<link rel="stylesheet" href="style.css?v={CSS_VERSION}">
<style>html,body{{background:#0f172a;color:#e2e8f0}}</style>
</head>
<body>
{header_html("home")}
<section class="hero-split">
  <div class="featured-box hero-hook">
    <div class="hero-inner">
      <h1>Build, Connect, Automate — All with ESP32</h1>
      <p>Step into the world of smart technology with ESP32 projects that combine innovation, connectivity, and automation. Learn how to create powerful IoT applications, intelligent monitoring systems, and real-world solutions while mastering one of the most versatile microcontrollers available today.</p>
    </div>
  </div>
  <div class="latest-box" id="latest">
    <h2>Latest Posts</h2>
    {"".join(latest_item(p) for p in latest)}
  </div>
</section>
{"".join(sections)}
<section class="section-block wrap browse-cta">
  <div class="cta-box">
    <h2>Browse all {len(projects)} ESP32 projects</h2>
    <p>Use search and category filters on the projects page to find the exact tutorial you need.</p>
    <a class="featured-btn" href="projects.html">View all projects »</a>
  </div>
</section>
{footer_html()}
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
            f"""<section class="section-block wrap" id="cat-{slug_cat(cat)}"><div class="section-title"><h2>{esc(cat)} Projects</h2><a class="view-all" href="projects.html#cat-{slug_cat(cat)}">View All »</a></div><div class="post-grid-4">{cards}</div></section>"""
        )
    cat_opts = "".join(f'<option>{esc(c)}</option>' for c in CATEGORIES)
    INDEX_OUT.write_text(home_html(projects, sections, latest), encoding="utf-8")
    PROJECTS_OUT.write_text(projects_listing_html(projects, cat_opts), encoding="utf-8")
    print(f"Wrote index.html (home) + projects.html ({len(projects)} projects, {len(sections)} category sections)")


if __name__ == "__main__":
    main()
