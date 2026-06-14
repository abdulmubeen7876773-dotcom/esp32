import html
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
OUT = ROOT / "index.html"
DOMAIN = "https://abdulmubeen7876773-dotcom.github.io/esp32"

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


def esc(t):
    return html.escape(t or "", quote=True)


def slug_cat(cat):
    return re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")


def parse_card(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    title = re.search(r"<h1>([^<]+)</h1>", raw)
    lead = re.search(r'<p class="lead">([^<]+)</p>', raw) or re.search(r'<p class="article-lead">([^<]+)</p>', raw)
    tags = re.findall(r'<span class="tag leaf">([^<]+)</span>', raw)
    clay = re.findall(r'<span class="tag clay">([^<]+)</span>', raw)
    cat = tags[0] if tags else "ESP32"
    diff = clay[0].replace(" build", "") if clay else "Beginner"
    return {
        "href": f"projects/{path.name}",
        "title": title.group(1).strip() if title else path.stem,
        "desc": lead.group(1).strip() if lead else "",
        "category": cat,
        "difficulty": diff,
        "slug": path.stem,
    }


def thumb_class(cat):
    return THUMB.get(cat, "t-default")


def thumb_label(title, cat):
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title).split()
    short = " ".join(words[:3]).upper()
    return short[:18] or cat.upper()[:12]


def latest_item(p):
    tc = thumb_class(p["category"])
    return f"""<a class="latest-item" href="{esc(p['href'])}"><div class="thumb {tc}">{esc(thumb_label(p['title'], p['category']))}</div><h3>{esc(p['title'])}</h3></a>"""


def post_card(p):
    tc = thumb_class(p["category"])
    return f"""<a class="post-card" href="{esc(p['href'])}"><div class="post-thumb {tc}">{esc(thumb_label(p['title'], p['category']))}</div><h3>{esc(p['title'])}</h3></a>"""


def grid_card(p):
    return f"""<a class="card project-card" data-title="{esc(p['title'].lower())}" data-category="{esc(p['category'])}" data-difficulty="{esc(p['difficulty'])}" href="{esc(p['href'])}"><span class="tag leaf">{esc(p['category'])}</span><span class="tag clay">{esc(p['difficulty'])}</span><h3>{esc(p['title'])}</h3><p>{esc(p['desc'])}</p></a>"""


def header_html():
    cats = "".join(f'<a class="cat-pill" href="#cat-{slug_cat(c)}">{esc(c.upper())}</a>' for c in CATEGORIES)
    return f"""<header class="site-header"><div class="wrap"><a class="site-logo" href="index.html">ESP32 PROJECT LIBRARY</a><nav class="top-nav"><a href="#latest">Latest</a><a href="#all-projects">All Projects</a><a href="sitemap.xml">Sitemap</a></nav><form class="top-search" onsubmit="event.preventDefault();document.getElementById('q').value=this.querySelector('input').value;document.getElementById('q').dispatchEvent(new Event('input'));document.getElementById('all-projects').scrollIntoView({{behavior:'smooth'}});"><input type="search" placeholder="Search…" aria-label="Search"><button type="submit">Search</button></form></div></header>
<nav class="cat-bar"><div class="wrap"><a class="cat-pill active" href="index.html">HOME</a>{cats}<a class="cat-pill" href="#all-projects">ALL</a></div></nav>"""


def footer_html():
    return """<footer class="site-footer"><div class="wrap"><div><strong>ESP32 Project Library</strong><br>1000 ESP32 tutorials with wiring, code, and guides.</div><div class="foot-links"><a href="#all-projects">Projects</a><a href="sitemap.xml">Sitemap</a><a href="robots.txt">Robots</a></div></div></footer>"""


def main():
    files = sorted(PROJECTS.glob("*.html"))
    if not files:
        print("No projects found", file=sys.stderr)
        sys.exit(1)
    projects = [parse_card(f) for f in files]
    by_cat = defaultdict(list)
    for p in projects:
        by_cat[p["category"]].append(p)
    featured = projects[0]
    latest = projects[:4]
    fc = thumb_class(featured["category"])
    sections = []
    for cat in CATEGORIES:
        items = by_cat.get(cat, [])[:4]
        if not items:
            continue
        cards = "".join(post_card(p) for p in items)
        sections.append(
            f"""<section class="section-block wrap" id="cat-{slug_cat(cat)}"><div class="section-title"><h2>{esc(cat)} Projects</h2><a class="view-all" href="#all-projects" onclick="document.getElementById('cat').value='{esc(cat)}';document.getElementById('cat').dispatchEvent(new Event('change'));return true;">View All »</a></div><div class="post-grid-4">{cards}</div></section>"""
        )
    all_cards = "".join(grid_card(p) for p in projects)
    cat_opts = "".join(f'<option>{esc(c)}</option>' for c in CATEGORIES)
    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 Project Library | Learn ESP32 with 1000 Tutorials</title>
<meta name="description" content="Browse 1000 ESP32 project tutorials — wiring, code, parts lists, and step-by-step guides. Random Nerd Tutorials style project library.">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header_html()}
<section class="hero-split">
  <div class="featured-box">
    <div style="padding:28px">
      <h2>{esc(featured['title'][:70])}</h2>
      <p>{esc(featured['desc'][:160])}</p>
      <a class="featured-btn" href="{esc(featured['href'])}">Read More »</a>
    </div>
  </div>
  <div class="latest-box" id="latest">
    <h2>Latest Posts</h2>
    {"".join(latest_item(p) for p in latest)}
  </div>
</section>
{"".join(sections)}
<section class="section-block wrap" id="all-projects">
  <div class="section-title"><h2>All ESP32 Projects</h2><span class="meta" id="count"></span></div>
  <div class="search-panel">
    <input id="q" placeholder="Search ESP32 projects…">
    <select id="cat"><option value="">All categories</option>{cat_opts}</select>
    <select id="diff"><option value="">All difficulty levels</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select>
  </div>
  <div class="grid" id="grid">{all_cards}</div>
</section>
{footer_html()}
<script>
const q=document.getElementById('q'),cat=document.getElementById('cat'),diff=document.getElementById('diff'),cards=[...document.querySelectorAll('.project-card')],count=document.getElementById('count');
function f(){{let s=q.value.toLowerCase(),c=cat.value,d=diff.value,n=0;cards.forEach(x=>{{let ok=(!s||x.dataset.title.includes(s))&&(!c||x.dataset.category===c)&&(!d||x.dataset.difficulty===d);x.classList.toggle('hidden',!ok);if(ok)n++;}});count.textContent=n+' projects found';}}
[q,cat,diff].forEach(e=>e.addEventListener('input',f));f();
</script>
</body>
</html>
"""
    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote index.html with {len(projects)} projects, {len(sections)} category sections")


if __name__ == "__main__":
    main()
