import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_categories
from parent_registry import PARENTS
from project_icons import pick_icon, slug_cat, thumb_class
from site_layout import (
    SITE_DOMAIN,
    SITE_NAME,
    category_section_title,
    esc,
    footer_html,
    head_html,
    header_html,
    itemlist_schema,
    modern_card,
    organization_schema,
    short_category,
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
    "ESP32-CAM": "Camera capture, streaming, and image server projects using ESP32-CAM modules and OTA updates.",
    "AI Projects": "On-device inference and TinyML experiments with ESP32 — audio, vision, and classification tutorials.",
    "Energy Monitoring": "Measure and log power draw with current sensors, displays, and optional cloud logging on ESP32.",
    "Healthcare": "Educational biosignal and wellness logging projects for learning — not for medical diagnosis or treatment.",
    "Environmental": "Air quality, weather, and environmental monitoring builds with gas sensors, BME modules, and fans.",
    "Smart City": "Street lighting, urban sensing, and infrastructure-style automation prototypes using ESP32.",
    "Education": "Classroom-friendly trainer projects that teach GPIO, sensors, and displays in progressive difficulty stages.",
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
    title = f"{category_section_title(cat)} | {SITE_NAME}"
    desc = (
        f"Explore {len(projects)} ESP32 {short_category(cat)} tutorials on {SITE_NAME}. "
        f"Each project includes Beginner, Intermediate, and Advanced build stages."
    )
    canon = f"category/{slug}.html"
    tc = thumb_class(cat)
    icon = pick_icon(cat)
    cards = "".join(
        modern_card(p, card_class="post-card", thumb_cls="post-thumb", show_desc=True) for p in projects
    )
    list_items = [
        {"name": p["title"], "url": f"{SITE_DOMAIN}/projects/{p['slug']}.html"}
        for p in projects
    ]
    schema = organization_schema() + itemlist_schema(category_section_title(cat), list_items)
    body = f"""  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="../index.html">Home</a></li><li><a href="../projects.html">Projects</a></li><li aria-current="page">{esc(short_category(cat))}</li></ol></nav>
  <div class="category-hero">
    <div class="category-hero-icon {tc}" aria-hidden="true">{icon}</div>
    <div>
      <p class="hero-eyebrow">Category</p>
      <h1>{esc(category_section_title(cat))}</h1>
      <p class="hero-sub">{esc(category_intro(cat))}</p>
      <p class="meta">{len(projects)} project{"s" if len(projects) != 1 else ""} · 3 difficulty stages each</p>
    </div>
  </div>
  <div class="post-grid category-project-grid">{cards or "<p>No projects in this category yet.</p>"}</div>
  <p class="meta category-back"><a href="../projects.html">← Browse all ESP32 projects</a></p>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("..", title, desc, canonical_path=canon, extra_schema=schema)}
</head>
<body>
<main>
{header_html("projects", "../")}
<section class="section-block wrap page-head static-page category-page">
{body}
</section>
</main>
{footer_html("../")}
<script src="../ui.js" defer></script>
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
