import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parent_registry import PARENTS, PARENT_BY_SLUG
from project_page import is_golden_project, render_golden_project_page
from project_text import breadcrumb_label, html_page_title, project_meta_description, project_title
from site_counts import site_counts
from staged_content import LEVELS, LEVEL_LABELS, build_all_levels
from project_icons import pick_icon, thumb_class as icon_thumb_class, featured_cat_bar, slug_cat
from project_images import project_image_path
from rebuild_projects import parse_project, esc
from site_layout import (
    footer_html,
    head_html,
    header_html,
    related_cards_html,
    short_category,
    SITE_NAME,
    CSS_VERSION,
    SITE_DOMAIN,
    OG_IMAGE,
    ORG_NAME,
    breadcrumb_schema,
    organization_schema,
    json_ld_script,
    social_meta,
    analytics_config_script,
    pinterest_verification_meta,
    gsc_verification_meta,
    font_links_html,
    head_extras_html,
    site_href,
    webpage_schema,
    UI_JS_SRC,
    GOOGLE_TAG_HTML,
    index_redirect_script,
)

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
ARCHIVE = PROJECTS / "_archive"
DOMAIN = SITE_DOMAIN


def clean_staged_value(value: object, fallback: str) -> str:
    text = str(value or "").strip()
    if not text or text.upper().startswith("TODO") or "TODO:" in text.upper():
        return fallback
    return text


def load_hardware_from_archive(parent: dict) -> dict:
    base = parent["source_base"]
    matches = sorted(
        PROJECTS.glob(f"{base}-project-*.html"),
        key=lambda p: int(re.search(r"project-(\d+)$", p.stem, re.I).group(1)),
    )
    if not matches and ARCHIVE.exists():
        matches = sorted(
            ARCHIVE.glob(f"{base}-project-*.html"),
            key=lambda p: int(re.search(r"project-(\d+)$", p.stem, re.I).group(1)),
        )
    if not matches:
        return {
            "wiring": [],
            "sensor_pin": "GPIO34",
            "output_pin": "GPIO26",
            "sensor_name": clean_staged_value(parent.get("sensor"), "Project input"),
            "output_name": clean_staged_value(parent.get("output"), "Project output"),
            "category": parent["category"],
        }
    data = parse_project(matches[0])
    if data["category"] in ("ESP32", ""):
        data["category"] = parent["category"]
    return data


def load_hardware(parent: dict) -> dict:
    stored = parent.get("hardware")
    if isinstance(stored, dict):
        wiring = []
        for row in stored.get("wiring", []):
            if isinstance(row, dict):
                wiring.append((row.get("component", ""), row.get("pin", "")))
            elif isinstance(row, (list, tuple)) and len(row) >= 2:
                wiring.append((row[0], row[1]))
        if wiring or stored.get("sensor_pin"):
            return {
                "wiring": wiring,
                "sensor_pin": clean_staged_value(stored.get("sensor_pin"), "GPIO34"),
                "output_pin": clean_staged_value(stored.get("output_pin"), "GPIO26"),
                "sensor_name": clean_staged_value(stored.get("sensor_name") or parent.get("sensor"), "Project input"),
                "output_name": clean_staged_value(stored.get("output_name") or parent.get("output"), "Project output"),
                "category": parent.get("category", "ESP32"),
            }

    return load_hardware_from_archive(parent)


def wiring_table(rows: list[tuple[str, str, str]]) -> str:
    body = []
    for comp, pin, note in rows:
        body.append(f"<tr><td>{esc(comp)}</td><td>{esc(pin)}</td><td>{esc(note)}</td></tr>")
    return (
        '<div class="wiring-table-wrap">'
        '<table class="wiring-table">'
        "<thead><tr><th>Component Pin</th><th>ESP32 Pin</th><th>Notes</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def project_wiring_diagram(parent: dict) -> str:
    slug = parent["slug"]
    image = ROOT / "assets" / "visuals" / "projects" / "wiring" / f"{slug}-wiring.svg"
    if not image.exists():
        return ""
    src = f"/assets/visuals/projects/wiring/{slug}-wiring.svg"
    alt = f"{parent['title']} wiring diagram"
    return (
        '<figure class="mission-illustration mission-illustration--image">'
        f'<img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" decoding="async" width="1200" height="800">'
        "</figure>"
    )


def accordion_item(level_id: str, section_id: str, title: str, body_html: str, open_default: bool = False) -> str:
    open_attr = " open" if open_default else ""
    return (
        f'<details class="accordion-item" id="sec-{level_id}-{section_id}" data-section="{section_id}"{open_attr}>'
        f'<summary class="accordion-header">{esc(title)}</summary>'
        f'<div class="accordion-content">{body_html}</div>'
        f"</details>"
    )


def footer_accordion(section_id: str, title: str, body_html: str) -> str:
    return (
        f'<details class="accordion-item" id="{section_id}" data-section="{section_id}">'
        f'<summary class="accordion-header">{esc(title)}</summary>'
        f'<div class="accordion-content">{body_html}</div>'
        f"</details>"
    )


def steps_html(items: list[str]) -> str:
    steps = []
    for i, text in enumerate(items, 1):
        steps.append(
            f'<div class="step"><span class="step-no">{i:02d}</span><p>{esc(text)}</p></div>'
        )
    return f'<div class="steps steps-compact">{"".join(steps)}</div>'


def faq_for_parent(parent: dict) -> list[tuple[str, str]]:
    title = parent["title"]
    sensor = clean_staged_value(parent.get("sensor"), "project-specific input hardware")
    output = clean_staged_value(parent.get("output"), "project-specific output hardware")
    cat = parent.get("category", "ESP32")
    return [
        (
            f"What hardware do I need for {title}?",
            f"You need an ESP32 DevKit, {sensor}, {output}, a breadboard, jumper wires, and a USB cable for power and programming.",
        ),
        (
            f"Does {title} require Wi-Fi?",
            "Only the Advanced stage uses Wi-Fi. Beginner and Intermediate builds run offline on the ESP32 with USB power.",
        ),
        (
            f"Which difficulty level should I start with for {title}?",
            f"Start with Beginner if you are new to {cat}. Use Intermediate for OLED feedback and Advanced for dashboards or connected monitoring.",
        ),
        (
            f"Why might Google or a learner choose this {title} tutorial?",
            f"This page teaches the complete path from wiring to code to troubleshooting, not just a parts list. It explains what the ESP32 measures, what it controls, and how to test each stage safely.",
        ),
        (
            f"What should I learn before building {title}?",
            "You should be comfortable uploading an Arduino sketch, reading Serial Monitor output, recognizing 3.3 V and GND, and changing wiring only when USB power is unplugged.",
        ),
    ]


def faq_accordion_html(parent: dict) -> str:
    faq_html = []
    for fq, fa in faq_for_parent(parent):
        faq_html.append(
            f'<div class="faq-item"><button type="button" class="faq-q">{esc(fq)}<span class="plus">+</span></button><div class="faq-a"><p>{esc(fa)}</p></div></div>'
        )
    return f'<div class="faq-list">{"".join(faq_html)}</div>'


def build_head(parent: dict, hardware: dict) -> str:
    url = f"{DOMAIN}/projects/{parent['slug']}.html"
    title = parent["title"]
    desc = parent["description"]
    cat = parent["category"]
    cat_slug = slug_cat(cat)
    cat_url = f"{DOMAIN}/category/{cat_slug}.html"
    levels = build_all_levels(parent, hardware)
    beginner_how = levels["beginner"]["how"]
    faq_schema = []
    for q, a in faq_for_parent(parent):
        faq_schema.append(
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        )
    image = project_image_path(parent["slug"]) or parent.get("og_image") or parent.get("hero_image") or parent.get("featured_image") or OG_IMAGE
    absolute_image = image if image.startswith("http") else f"{DOMAIN}{image}"
    article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "datePublished": "2026-06-14",
        "dateModified": "2026-06-18",
        "image": absolute_image,
        "author": {"@type": "Person", "name": "Abdul Mubeen", "url": DOMAIN + "/author.html"},
        "reviewedBy": {"@type": "Organization", "name": "ESP32 Engine Editorial Team", "url": DOMAIN + "/editorial-policy.html"},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "proficiencyLevel": "Beginner",
        "dependencies": f"ESP32 DevKit, {clean_staged_value(parent.get('sensor'), 'project input hardware')}, {clean_staged_value(parent.get('output'), 'project output hardware')}",
    }
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to build {title} (Beginner)",
        "description": desc,
        "step": [
            {
                "@type": "HowToStep",
                "position": i + 1,
                "name": (step[:100] + "…") if len(step) > 100 else step,
                "text": step,
            }
            for i, step in enumerate(beginner_how)
        ],
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": cat, "item": cat_url},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }
    social = social_meta(f"{title} | {SITE_NAME}", desc, url, "article", image)
    return f"""<title>{esc(title)} | {esc(SITE_NAME)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{social}
{json_ld_script(article)}
{json_ld_script(howto)}
{json_ld_script(faq)}
{json_ld_script(crumbs)}"""


def project_learning_context(parent: dict, hardware: dict) -> str:
    title = parent["title"]
    sensor = clean_staged_value(parent.get("sensor"), hardware.get("sensor_name", "input sensor"))
    output = clean_staged_value(parent.get("output"), hardware.get("output_name", "output device"))
    cat = parent.get("category", "ESP32")
    return f"""<div class="steps steps-compact">
  <div class="step"><span class="step-no">01</span><p>{esc(title)} starts with a real input: {esc(sensor)}. The first learning goal is to prove the ESP32 can read that signal reliably before anything is automated.</p></div>
  <div class="step"><span class="step-no">02</span><p>The second goal is decision logic. The sketch compares the live reading with a threshold, then explains why thresholds need testing instead of guessing.</p></div>
  <div class="step"><span class="step-no">03</span><p>The final goal is a controlled output: {esc(output)}. You learn how a {esc(cat.lower())} project turns sensor data into a visible or useful action.</p></div>
</div>"""


def project_quality_notes(parent: dict, hardware: dict) -> str:
    title = parent["title"]
    s_pin = hardware.get("sensor_pin", "GPIO34")
    o_pin = hardware.get("output_pin", "GPIO26")
    updated = parent.get("date_modified", "2026-07-05")
    return f"""<div class="trouble-list">
  <div class="trouble-item"><h3>Editorial accuracy</h3><p>{esc(title)} is written as an educational build. Last updated: {esc(updated)}. Pin choices, code structure, and troubleshooting steps are selected so beginners can test the circuit on a bench before moving to a permanent enclosure.</p></div>
  <div class="trouble-item"><h3>Safety boundary</h3><p>Keep the ESP32 side low-voltage. Unplug USB before rewiring. If the project interacts with mains power, motors, pumps, batteries, or outdoor wiring, use an isolated relay/module and get adult or qualified supervision.</p></div>
  <div class="trouble-item"><h3>Verification method</h3><p>First confirm the input on {esc(s_pin)} in Serial Monitor. Then confirm the output pin {esc(o_pin)} changes only when the condition is true. This separates sensor problems from output-driver problems.</p></div>
</div>"""


def related_guides_for_parent(parent: dict) -> list[dict]:
    title = parent["title"]
    cat = parent.get("category", "")
    guides = [
        {
            "href": site_href("guides/blink-led-esp32.html"),
            "title": "Mission 01 - Blink LED",
            "description": "Start here if you need a first upload and output test before building projects.",
        },
        {
            "href": site_href("guides/analog-inputs.html"),
            "title": "Mission 08 - Analog Inputs",
            "description": "Useful for sensor projects that read changing values instead of simple ON/OFF states.",
        },
    ]
    lower = f"{title} {cat}".lower()
    if any(word in lower for word in ("weather", "climate", "air", "environment", "greenhouse", "uv")):
        guides.append(
            {
                "href": site_href("guides/environmental-sensors.html"),
                "title": "Mission 11 - Reading Environmental Sensors",
                "description": "Learn how temperature, humidity, pressure, and live sensor data behave in real rooms.",
            }
        )
    if any(word in lower for word in ("oled", "display", "clock", "dashboard")):
        guides.append(
            {
                "href": site_href("guides/oled-display-esp32.html"),
                "title": "Mission 09 - OLED Display with ESP32",
                "description": "Display ESP32 readings locally instead of relying only on Serial Monitor.",
            }
        )
    if any(word in lower for word in ("wifi", "iot", "mqtt", "home", "automation", "energy")):
        guides.append(
            {
                "href": site_href("guides/i2c-communication.html"),
                "title": "Mission 10 - I2C Communication",
                "description": "Understand shared communication buses used by OLED screens and sensor modules.",
            }
        )
    if any(word in lower for word in ("robot", "motor", "servo", "street light", "piano", "matrix")):
        guides.append(
            {
                "href": site_href("guides/pwm-fundamentals.html"),
                "title": "Mission 07 - PWM Fundamentals",
                "description": "Use PWM concepts for brightness, speed, and smooth output control.",
            }
        )
    return guides[:4]


def related_guides_html(parent: dict) -> str:
    cards = []
    for item in related_guides_for_parent(parent):
        cards.append(
            f"""<a class="related-card" href="{esc(item['href'])}">
  <span class="tag clay">Guide</span>
  <h3>{esc(item['title'])}</h3>
  <p>{esc(item['description'])}</p>
</a>"""
        )
    return f'<div class="related-grid">{"".join(cards)}</div>'


def authority_references_html(parent: dict) -> str:
    refs = [
        ("Espressif ESP32 Documentation", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/"),
        ("Arduino ESP32 Core Documentation", "https://docs.espressif.com/projects/arduino-esp32/en/latest/"),
        ("ESP32 Arduino GitHub", "https://github.com/espressif/arduino-esp32"),
    ]
    items = "".join(
        f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a></li>'
        for label, url in refs
    )
    return f"""<p>This project is written for practical learning, then cross-checked against the ESP32 platform documentation where pin behavior, Arduino support, and board-level constraints matter.</p>
<ul class="detail-list">{items}</ul>"""


SECTION_NAV = [
    ("overview", "Overview"),
    ("components", "Components"),
    ("wiring", "Wiring"),
    ("code", "Arduino Code"),
    ("how", "How It Works"),
    ("apps", "Applications"),
    ("troubleshooting", "Troubleshooting"),
    ("upgrades", "Upgrades"),
    ("faq", "FAQ"),
]

SIDEBAR_NAV = [
    ("overview", "Overview"),
    ("components", "Components"),
    ("wiring", "Wiring"),
    ("code", "Arduino Code"),
    ("apps", "Applications"),
    ("faq", "FAQ"),
]


def section_toc_html(active_level: str = "beginner") -> str:
    items = []
    for sec_id, label in SIDEBAR_NAV:
        items.append(
            f'<li><a href="#sec-{active_level}-{sec_id}" data-section="{sec_id}">{esc(label)}</a></li>'
        )
    return f'<ul class="side-list side-toc side-sections" id="section-toc">{"".join(items)}</ul>'


def mobile_nav_select(active_level: str = "beginner") -> str:
    opts = ['<option value="">Jump to section…</option>']
    for sec_id, label in SECTION_NAV:
        opts.append(f'<option value="sec-{active_level}-{sec_id}">{esc(label)}</option>')
    opts.append('<option value="related">Related Projects</option>')
    return (
        f'<div class="mobile-section-nav"><label class="visually-hidden" for="mobile-nav-select">Jump to section</label>'
        f'<select id="mobile-nav-select" class="mobile-nav-select" aria-label="Jump to section">{"".join(opts)}</select></div>'
    )


def render_difficulty_content(level: dict, parent: dict) -> str:
    lv = level["level"]
    comps = "".join(f"<li><span>{esc(c)}</span></li>" for c in level["components"])
    apps = "".join(f"<li>{esc(a)}</li>" for a in level["apps"])
    upgrades = "".join(f"<li>{esc(u)}</li>" for u in level["upgrades"])
    trouble = "".join(
        f'<div class="trouble-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>'
        for q, a in level["troubleshooting"]
    )
    code_esc = esc(level["code"])
    fname = parent["slug"] + f"_{level['level']}.ino"

    def acc(section_id: str, title: str, body_html: str) -> str:
        return accordion_item(lv, section_id, title, body_html, section_id == "overview")

    overview_body = (
        level["overview_html"]
        if level.get("overview_html")
        else f"<p>{esc(level['overview'])}</p>"
    )
    sections = [
        acc("overview", "Overview", overview_body),
        acc("components", "Components", f'<ul class="parts-grid parts-grid-compact">{comps}</ul>'),
        acc("wiring", "Wiring", project_wiring_diagram(parent) + wiring_table(level["wiring"])),
        acc("code", "Arduino Code", f'<div class="code-block"><div class="code-bar"><span>{esc(fname)}</span><button type="button" class="copy-btn">Copy</button></div><pre class="level-code">{code_esc}</pre></div>'),
        acc("how", "How It Works", steps_html(level["how"])),
        acc("apps", "Applications", f'<ul class="detail-list">{apps}</ul>'),
        acc("troubleshooting", "Troubleshooting", f'<div class="trouble-list">{trouble}</div>'),
        acc("upgrades", "Upgrades", f'<ul class="detail-list">{upgrades}</ul>'),
        acc("faq", "FAQ", faq_accordion_html(parent)),
    ]
    return (
        f'<div class="difficulty-content level-{lv}-panel" data-level="{lv}" id="level-{lv}" role="tabpanel" aria-labelledby="tab-{lv}">'
        f'{"".join(sections)}'
        f"</div>"
    )


def render_golden_parent(parent: dict) -> str:
    slug = parent["slug"]
    path = f"projects/{slug}.html"
    title = html_page_title(parent)
    desc = project_meta_description(parent)
    proj = parent.get("project") or {}
    crumbs = breadcrumb_schema(
        [
            ("Home", "/"),
            ("Projects", "projects.html"),
            (breadcrumb_label(parent), path),
        ]
    )
    url = f"{SITE_DOMAIN}/{path}"
    image = project_image_path(parent["slug"]) or parent.get("og_image") or parent.get("hero_image") or parent.get("featured_image") or OG_IMAGE
    absolute_image = image if str(image).startswith("http") else f"{SITE_DOMAIN}{image}"
    article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": project_title(parent),
        "description": desc,
        "datePublished": parent.get("date_published", "2026-06-14"),
        "dateModified": parent.get("date_modified", "2026-06-29"),
        "image": absolute_image,
        "author": {"@type": "Person", "name": "Abdul Mubeen", "url": SITE_DOMAIN + "/author.html"},
        "reviewedBy": {"@type": "Organization", "name": "ESP32 Engine Editorial Team", "url": SITE_DOMAIN + "/editorial-policy.html"},
        "publisher": {"@type": "Organization", "name": ORG_NAME, "logo": {"@type": "ImageObject", "url": OG_IMAGE}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "proficiencyLevel": proj.get("difficulty", "Beginner"),
        "timeRequired": proj.get("estimated_time", ""),
        "keywords": ", ".join(parent.get("keywords", [])),
    }
    howto_steps = (proj.get("wiring") or {}).get("steps", [])
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to build {project_title(parent)}",
        "description": desc,
        "totalTime": proj.get("estimated_time", ""),
        "supply": [{"@type": "HowToSupply", "name": item.get("item", "")} for item in proj.get("components", []) if isinstance(item, dict)],
        "tool": [{"@type": "HowToTool", "name": "Arduino IDE"}, {"@type": "HowToTool", "name": "USB cable"}],
        "step": [
            {"@type": "HowToStep", "position": i + 1, "name": step[:80], "text": step}
            for i, step in enumerate(howto_steps)
        ],
    }
    faq_items = [
        {"@type": "Question", "name": item.get("question", ""), "acceptedAnswer": {"@type": "Answer", "text": item.get("answer", "")}}
        for item in proj.get("faqs", [])
        if isinstance(item, dict) and item.get("question") and item.get("answer")
    ]
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}
    schema = (
        organization_schema()
        + webpage_schema(title, desc, path)
        + crumbs
        + json_ld_script(article)
        + json_ld_script(howto)
        + (json_ld_script(faq_schema) if faq_items else "")
    )
    og_image = project_image_path(parent["slug"]) or parent.get("og_image") or parent.get("hero_image") or parent.get("featured_image")
    head = head_html("", title, desc, canonical_path=path, og_type="article", extra_schema=schema, og_image=og_image)
    return render_golden_project_page(
        parent,
        head=head,
        header=header_html("projects"),
        footer=footer_html(),
    )


def render_page(parent: dict, hardware: dict, related: list) -> str:
    levels = build_all_levels(parent, hardware)
    cat = parent["category"]
    cat_slug = slug_cat(cat)
    tc = icon_thumb_class(cat)
    icon = pick_icon(cat)
    hero_image = project_image_path(parent["slug"]) or parent.get("hero_image") or parent.get("featured_image")
    if hero_image:
        hero_media = (
            f'<img class="project-hero-art-img" src="{esc(hero_image)}" alt="" width="1376" height="768" loading="eager" decoding="async">'
        )
    else:
        hero_media = icon
    radios = []
    labels = []
    for i, lv in enumerate(LEVELS):
        checked = " checked" if i == 0 else ""
        radios.append(
            f'<input type="radio" name="difficulty-level" id="level-radio-{lv}" class="level-radio"{checked} aria-hidden="true" tabindex="-1">'
        )
        labels.append(
            f'<label for="level-radio-{lv}" class="difficulty-tab" id="tab-{lv}" data-level="{lv}" role="tab">{LEVEL_LABELS[lv]}</label>'
        )
    content_html = "".join(render_difficulty_content(levels[lv], parent) for lv in LEVELS)
    related_section = related_cards_html(related)
    breadcrumb = f"""<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href(f'category/{cat_slug}.html')}">{esc(cat)}</a></li><li aria-current="page">{esc(parent['title'][:50])}</li></ol></nav>"""
    level_badges = "".join(
        f'<span class="badge badge-{lv}">{LEVEL_LABELS[lv]}</span>' for lv in LEVELS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{index_redirect_script()}
{GOOGLE_TAG_HTML}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#6D28D9">
<meta name="robots" content="index,follow,max-image-preview:large">
{pinterest_verification_meta()}
{gsc_verification_meta()}
<script>document.documentElement.classList.add("js")</script>
{analytics_config_script()}
{font_links_html()}
{head_extras_html()}
{build_head(parent, hardware)}
<link rel="preload" href="/style.css?v={CSS_VERSION}" as="style">
<link rel="stylesheet" href="/style.css?v={CSS_VERSION}">
<style>.level-radio{{position:absolute;opacity:0;width:0;height:0;margin:0;padding:0;pointer-events:none}}.difficulty-switcher .difficulty-content{{display:none!important}}.difficulty-switcher #level-radio-beginner:checked~.difficulty-sections #level-beginner{{display:block!important}}.difficulty-switcher #level-radio-intermediate:checked~.difficulty-sections #level-intermediate{{display:block!important}}.difficulty-switcher #level-radio-advanced:checked~.difficulty-sections #level-advanced{{display:block!important}}details.accordion-item>summary{{list-style:none;cursor:pointer}}details.accordion-item>summary::-webkit-details-marker{{display:none}}</style>
</head>
<body>
<div class="site-nav-sticky">
{header_html("projects")}
</div>
<main>
<div class="wrap article-shell parent-project-shell">
  <aside class="sidebar-left">
    <div class="sidebar-sticky">
      <p class="sidebar-label">Difficulty</p>
      <ul class="side-list side-toc side-levels">
        <li><a href="#beginner" data-level-link="beginner">Beginner</a></li>
        <li><a href="#intermediate" data-level-link="intermediate">Intermediate</a></li>
        <li><a href="#advanced" data-level-link="advanced">Advanced</a></li>
      </ul>
      <p class="sidebar-label sidebar-divider">Sections</p>
      {section_toc_html("beginner")}
      <p class="sidebar-label sidebar-divider">Category</p>
      <ul class="side-list"><li><a href="{site_href(f'category/{cat_slug}.html')}">{esc(cat)}</a></li></ul>
    </div>
  </aside>
  <article class="article-main parent-article">
    <header class="article-header">
      {breadcrumb}
      <div class="parent-hero-row project-hero-banner">
        <div class="parent-hero-text">
          <h1>{esc(parent['title'])}</h1>
          <h2 class="visually-hidden">Project tutorial sections</h2>
          <div class="article-badges"><span class="badge badge-cat">{esc(short_category(cat))}</span>{level_badges}</div>
          <p class="article-lead">{esc(parent['description'])}</p>
        </div>
        <div class="article-thumb project-hero-image {tc} parent-thumb">{hero_media}</div>
      </div>
    </header>
    <div class="difficulty-switcher">
      {''.join(radios)}
      <div class="difficulty-tabs" role="tablist" aria-label="Difficulty level">
        {''.join(labels)}
      </div>
      {mobile_nav_select("beginner")}
      <div class="difficulty-sections">
        {content_html}
      </div>
    </div>
    <div class="article-content parent-footer-sections">
      <div class="footer-accordions">
        {footer_accordion("learning-context", "What You Learn", project_learning_context(parent, hardware))}
        {footer_accordion("quality-notes", "Safety and Accuracy Notes", project_quality_notes(parent, hardware))}
        {footer_accordion("related-guides", "Related Guides", related_guides_html(parent))}
        {footer_accordion("authority-references", "Engineering References", authority_references_html(parent))}
        {footer_accordion("related", "Related Projects", related_section)}
      </div>
    </div>
  </article>
  <aside class="sidebar-right">
    <div class="sidebar-sticky">
      <div class="promo-box"><strong>ESP32 Engine</strong><p class="promo-text">{site_counts()['total_projects']} projects with practical wiring, code, and troubleshooting.</p><p class="promo-link"><a href="{site_href('projects.html')}">Browse all projects »</a></p></div>
    </div>
  </aside>
</div>
</main>
{footer_html()}
<script src="{UI_JS_SRC}" defer></script>
<script src="/project.js?v={CSS_VERSION}" defer></script>
</body>
</html>"""


def build_related(all_parents: list[dict], current: dict) -> list[dict]:
    cat = current["category"]
    related = []
    for p in all_parents:
        if p["slug"] == current["slug"]:
            continue
        if p["category"] != cat:
            continue
        related.append(
            {
                "href": f"{p['slug']}.html",
                "cat": p["category"],
                "title": p["title"],
                "desc": p["description"][:100],
            }
        )
        if len(related) >= 4:
            break
    if len(related) < 4:
        for p in all_parents:
            if p["slug"] == current["slug"]:
                continue
            if any(r["href"] == f"{p['slug']}.html" for r in related):
                continue
            related.append(
                {
                    "href": f"{p['slug']}.html",
                    "cat": p["category"],
                    "title": p["title"],
                    "desc": p["description"][:100],
                }
            )
            if len(related) >= 4:
                break
    return related


def archive_legacy_pages() -> int:
    ARCHIVE.mkdir(exist_ok=True)
    moved = 0
    for f in PROJECTS.glob("*-project-*.html"):
        dest = ARCHIVE / f.name
        if dest.exists():
            dest.unlink()
        f.rename(dest)
        moved += 1
    return moved


def main():
    moved = archive_legacy_pages()
    written = []
    golden = 0
    staged = 0
    for parent in PARENTS:
        out = PROJECTS / f"{parent['slug']}.html"
        if is_golden_project(parent):
            out.write_text(render_golden_parent(parent), encoding="utf-8")
            golden += 1
        else:
            if out.exists():
                out.unlink()
            staged += 1
            continue
        written.append(parent["slug"])
    print(f"Archived {moved} legacy variant pages to projects/_archive/")
    print(f"Wrote {len(written)} public project pages ({golden} golden, {staged} staged hidden)")


if __name__ == "__main__":
    main()
