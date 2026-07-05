import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_categories
from parent_registry import PARENTS
from project_icons import slug_cat
from site_layout import (
    SITE_DOMAIN,
    SITE_NAME,
    breadcrumb_schema,
    category_hero_html,
    category_section_title,
    esc,
    footer_html,
    head_html,
    header_html,
    itemlist_schema,
    modern_card,
    organization_schema,
    short_category,
    sidebar_categories_html,
    site_href,
    webpage_schema,
    UI_JS_SRC,
)

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"

CATEGORY_INTROS = load_categories() or {
    "Agriculture": "Automate irrigation, soil monitoring, and greenhouse control with ESP32 sensor nodes and relay outputs.",
    "Home Automation": "Build smart home projects — climate control, lighting, and appliance automation using ESP32 and common sensors.",
    "Security Projects": "Motion detection, alerts, and access monitoring tutorials with PIR sensors, relays, and Wi-Fi notifications.",
    "IoT Projects": "Connected ESP32 builds that publish sensor data to dashboards, APIs, and local web servers over Wi-Fi.",
    "Sensor Projects": "Learn analog and digital sensing on ESP32 — distance, environmental, and signal processing project guides.",
    "Robotics": "Motor control, teleoperation, and sensor-assisted navigation projects powered by ESP32 microcontrollers.",
    "Industrial Automation": "Machine monitoring, energy tracking, and status nodes for benches, workshops, and small facilities.",
    "LED Projects": "RGB strips, patterns, and addressable LED control with ESP32 — from breadboard demos to Wi-Fi control.",
    "ESP32-CAM": "Explore exciting ESP32-CAM projects including surveillance cameras, face recognition, object detection, home security systems, and IoT camera applications.",
    "AI Projects": "On-device inference and TinyML experiments with ESP32 — audio, vision, and classification tutorials.",
    "Energy Monitoring": "Measure and log power draw with current sensors, displays, and optional cloud logging on ESP32.",
    "Healthcare": "Educational biosignal and wellness logging projects for learning — not for medical diagnosis or treatment.",
    "Environmental": "Air quality, weather, and environmental monitoring builds with gas sensors, BME modules, and fans.",
    "Smart City": "Street lighting, urban sensing, and infrastructure-style automation prototypes using ESP32.",
    "Education": "Classroom-friendly trainer projects that teach GPIO, sensors, and displays in progressive difficulty stages.",
}

SIDEBAR_KEYS = {
    "ESP32-CAM": "esp32-cam",
    "IoT Projects": "iot-projects",
    "Home Automation": "home-automation",
    "LED Projects": "display",
    "Sensor Projects": "display",
}


def category_intro(cat: str) -> str:
    return CATEGORY_INTROS.get(
        cat,
        f"Browse ESP32 {short_category(cat)} tutorials with wiring diagrams, Arduino code, and three skill levels.",
    )


def projects_for_category(cat: str) -> list[dict]:
    items = []
    for p in PARENTS:
        if p["category"] != cat:
            continue
        items.append(
            {
                "href": f"../projects/{p['slug']}.html",
                "title": p["title"],
                "desc": p["description"],
                "category": p["category"],
                "difficulty": "Beginner",
                "slug": p["slug"],
                "featured": False,
            }
        )
    return items


def render_category_page(cat: str, projects: list[dict]) -> str:
    slug = slug_cat(cat)
    title = category_section_title(cat)
    desc = category_intro(cat)
    canon = f"category/{slug}.html"
    cards = "".join(
        modern_card(p, card_class="post-card", thumb_cls="post-thumb", show_desc=True) for p in projects
    )
    list_items = [
        {"name": p["title"], "url": f"{SITE_DOMAIN}/projects/{p['slug']}.html"}
        for p in projects
    ]
    schema = (
        organization_schema()
        + webpage_schema(f"{title} | {SITE_NAME}", desc, canon)
        + breadcrumb_schema(
            [
                ("Home", "/"),
                ("Projects", "projects.html"),
                (short_category(cat), canon),
            ]
        )
        + itemlist_schema(title, list_items)
    )
    badges = (
        f'<span class="badge badge-light">{len(projects)} Projects</span>'
        f'<span class="badge badge-light">3 Difficulty Levels</span>'
        f'<span class="badge badge-light">{esc(short_category(cat))}</span>'
    )
    sidebar_key = SIDEBAR_KEYS.get(cat, slug)
    hero = category_hero_html(title, desc, cat, badges)
    related_category = ""
    if cat == "LED Projects":
        related_category = '<p class="meta">Looking for screen-based builds? Browse <a href="/category/display-projects.html">ESP32 display projects</a>.</p>'
    elif cat == "Display Projects":
        related_category = '<p class="meta">Need LED strips or matrix builds? Browse <a href="/category/led-projects.html">ESP32 LED projects</a>.</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", f"{title} | {SITE_NAME}", desc, canonical_path=canon, extra_schema=schema)}
</head>
<body class="category-page">
<main>
{header_html("projects")}
{hero}
<div class="layout-with-sidebar wrap">
  {sidebar_categories_html(sidebar_key)}
  <div class="main-with-sidebar">
    <section class="section-block">
      {related_category}
      <div class="grid grid-projects category-project-grid">{cards or "<p>No projects in this category yet.</p>"}</div>
      <p class="meta category-back"><a href="{site_href('projects.html')}">← Browse all ESP32 projects</a></p>
    </section>
  </div>
</div>
</main>
{footer_html()}
<script src="{UI_JS_SRC}" defer></script>
</body>
</html>"""


def main():
    CATEGORY_DIR.mkdir(exist_ok=True)
    by_cat = defaultdict(list)
    for p in PARENTS:
        by_cat[p["category"]].append(p)
    written = 0
    for cat in sorted(by_cat):
        projects = projects_for_category(cat)
        slug = slug_cat(cat)
        out = CATEGORY_DIR / f"{slug}.html"
        out.write_text(render_category_page(cat, projects), encoding="utf-8")
        written += 1
    print(f"Wrote {written} category landing pages in category/")


if __name__ == "__main__":
    main()
