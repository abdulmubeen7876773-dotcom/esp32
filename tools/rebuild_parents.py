import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parent_registry import PARENTS, PARENT_BY_SLUG
from staged_content import LEVELS, LEVEL_LABELS, build_all_levels
from project_icons import pick_icon, thumb_class as icon_thumb_class, featured_cat_bar, slug_cat
from rebuild_projects import parse_project, esc
from staged_content import build_all_levels
from site_layout import (
    footer_html,
    header_html,
    related_cards_html,
    short_category,
    SITE_NAME,
    CSS_VERSION,
    SITE_DOMAIN,
    OG_IMAGE,
    ORG_NAME,
    json_ld_script,
    social_meta,
    analytics_config_script,
    pinterest_verification_meta,
    gsc_verification_meta,
    font_links_html,
    head_extras_html,
    site_href,
)

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
ARCHIVE = PROJECTS / "_archive"
DOMAIN = SITE_DOMAIN


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
            "sensor_name": parent.get("sensor", "Sensor"),
            "output_name": parent.get("output", "Output"),
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
                "sensor_pin": stored.get("sensor_pin", "GPIO34"),
                "output_pin": stored.get("output_pin", "GPIO26"),
                "sensor_name": stored.get("sensor_name") or parent.get("sensor", "Sensor"),
                "output_name": stored.get("output_name") or parent.get("output", "Output"),
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
    sensor = parent.get("sensor", "sensor module")
    output = parent.get("output", "output module")
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
    article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "datePublished": "2026-06-14",
        "dateModified": "2026-06-18",
        "image": OG_IMAGE,
        "author": {"@type": "Organization", "name": ORG_NAME, "url": DOMAIN + "/"},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "proficiencyLevel": "Beginner",
        "dependencies": f"ESP32 DevKit, {parent.get('sensor', 'sensor')}, {parent.get('output', 'output')}",
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
    social = social_meta(f"{title} | {SITE_NAME}", desc, url, "article")
    return f"""<title>{esc(title)} | {esc(SITE_NAME)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{social}
{json_ld_script(article)}
{json_ld_script(howto)}
{json_ld_script(faq)}
{json_ld_script(crumbs)}"""


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
        f'<div class="trouble-item"><h4>{esc(q)}</h4><p>{esc(a)}</p></div>'
        for q, a in level["troubleshooting"]
    )
    code_esc = esc(level["code"])
    fname = parent["slug"] + f"_{level['level']}.ino"

    def acc(section_id: str, title: str, body_html: str) -> str:
        return accordion_item(lv, section_id, title, body_html, section_id == "overview")

    sections = [
        acc("overview", "Overview", f"<p>{esc(level['overview'])}</p>"),
        acc("components", "Components", f'<ul class="parts-grid parts-grid-compact">{comps}</ul>'),
        acc("wiring", "Wiring", wiring_table(level["wiring"])),
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


def render_page(parent: dict, hardware: dict, related: list) -> str:
    levels = build_all_levels(parent, hardware)
    cat = parent["category"]
    cat_slug = slug_cat(cat)
    tc = icon_thumb_class(cat)
    icon = pick_icon(cat)
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
      <h3>Difficulty</h3>
      <ul class="side-list side-toc side-levels">
        <li><a href="#beginner" data-level-link="beginner">Beginner</a></li>
        <li><a href="#intermediate" data-level-link="intermediate">Intermediate</a></li>
        <li><a href="#advanced" data-level-link="advanced">Advanced</a></li>
      </ul>
      <h3 class="sidebar-divider">Sections</h3>
      {section_toc_html("beginner")}
      <h3 class="sidebar-divider">Category</h3>
      <ul class="side-list"><li><a href="{site_href(f'category/{cat_slug}.html')}">{esc(cat)}</a></li></ul>
    </div>
  </aside>
  <article class="article-main parent-article">
    <header class="article-header">
      {breadcrumb}
      <div class="parent-hero-row project-hero-banner">
        <div class="parent-hero-text">
          <h1>{esc(parent['title'])}</h1>
          <div class="article-badges"><span class="badge badge-cat">{esc(short_category(cat))}</span>{level_badges}</div>
          <p class="article-lead">{esc(parent['description'])}</p>
        </div>
        <div class="article-thumb project-hero-image {tc} parent-thumb">{icon}</div>
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
        {footer_accordion("related", "Related Projects", related_section)}
      </div>
    </div>
  </article>
  <aside class="sidebar-right">
    <div class="sidebar-sticky">
      <div class="promo-box"><strong>ESP32 Engine</strong><p class="promo-text">15 parent projects with Beginner, Intermediate, and Advanced stages.</p><p class="promo-link"><a href="{site_href('projects.html')}">Browse all projects »</a></p></div>
    </div>
  </aside>
</div>
</main>
{footer_html()}
<script src="/ui.js" defer></script>
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
    for parent in PARENTS:
        hardware = load_hardware(parent)
        related = build_related(PARENTS, parent)
        out = PROJECTS / f"{parent['slug']}.html"
        out.write_text(render_page(parent, hardware, related), encoding="utf-8")
        written.append(parent["slug"])
    print(f"Archived {moved} legacy variant pages to projects/_archive/")
    print(f"Wrote {len(written)} parent project pages with 3 difficulty stages each")


if __name__ == "__main__":
    main()
