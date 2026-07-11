from pathlib import Path

from guide_mission import code_panel, illustration_placeholder
from parent_registry import PARENT_BY_SLUG
from project_text import card_description, project_meta_description, project_slug_from_href, project_title
from site_layout import badge_class, esc, site_href, UI_JS_SRC, SEARCH_JS_SRC


ROOT = Path(__file__).resolve().parent.parent
PROJECT_WIRING_DIR = ROOT / "assets" / "visuals" / "projects" / "wiring"


def project_section_heading(section_id: str, icon: str, title: str) -> str:
    return (
        f'<h2 id="{section_id}-heading">'
        f'<span class="project-section-icon" aria-hidden="true">{icon}</span>'
        f'<span class="project-section-title">{esc(title)}</span>'
        f"</h2>"
    )


def _paragraphs(text: str) -> str:
    if not text:
        return ""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)


def readable_project_icon(icon: str) -> str:
    replacements = {
        "AIR": "Air",
        "ARM": "Arm",
        "CAM": "Camera",
        "ESP": "ESP32",
        "FACE": "Face",
        "FIRE": "Fire",
        "GEST": "Gesture",
        "GROW": "Greenhouse",
        "PART": "Part",
        "IMG": "Photo",
        "LAMP": "Light",
        "LEAK": "Leak",
        "LITE": "Lightning",
        "LORA": "LoRa",
        "MAIL": "Mail",
        "MTRX": "Matrix",
        "PARK": "Parking",
        "PH": "pH",
        "PROJ": "Project",
        "NOTE": "Music",
        "PULSE": "Pulse",
        "SOIL": "Soil",
        "TEMP": "Temperature",
        "VIBE": "Vibration",
        "VOICE": "Voice",
        "VU": "Visualizer",
        "WX": "Weather",
    }
    return replacements.get(str(icon or "").strip(), icon)


def readable_part_icon(icon: str) -> str:
    return readable_project_icon(icon)


def project_meta_badges(p: dict) -> str:
    proj = p.get("project") or {}
    parts = []
    diff = proj.get("difficulty") or p.get("difficulty", "Beginner")
    parts.append(f'<span class="badge {badge_class(diff)}">{esc(diff)}</span>')
    if proj.get("age"):
        parts.append(f'<span class="badge badge-age">{esc(proj["age"])}</span>')
    if proj.get("estimated_time"):
        parts.append(f'<span class="badge badge-time">{esc(proj["estimated_time"])}</span>')
    if proj.get("budget"):
        parts.append(f'<span class="badge badge-budget">{esc(proj["budget"])}</span>')
    parts.append('<span class="badge badge-parent-safe">Parent Safe</span>')
    return f'<div class="project-meta-row">{"".join(parts)}</div>'


def mission_intro_card(p: dict) -> str:
    proj = p.get("project") or {}
    icon = proj.get("icon", "🚀")
    title = proj.get("mission_title") or p.get("title", "")
    icon = readable_project_icon(icon)
    return f"""<header class="project-mission-card">
  <div class="project-mission-glow" aria-hidden="true"></div>
  <span class="project-mission-icon" aria-hidden="true">{esc(icon)}</span>
  <span class="project-mission-label">Project Mission</span>
  <h2 class="project-mission-title">{esc(title)}</h2>
</header>"""


def story_section(p: dict) -> str:
    story = (p.get("project") or {}).get("story", "").strip()
    if not story:
        return ""
    return f"""<section class="project-section project-story-section" id="story" aria-labelledby="story-heading">
  {project_section_heading("story", "📖", "The Story")}
  <div class="project-story">{_paragraphs(story)}</div>
</section>"""


def eli12_section(p: dict) -> str:
    text = (p.get("project") or {}).get("eli12", "").strip()
    if not text:
        return ""
    return f"""<section class="project-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box project-eli12">
    {project_section_heading("eli12", "🧒", "Explain Like I'm 12")}
    <div class="eli12-content">{_paragraphs(text)}</div>
  </div>
</section>"""


def parent_safety_section(p: dict) -> str:
    text = (p.get("project") or {}).get("parent_safety", "").strip()
    if not text:
        return ""
    return f"""<section class="project-section project-safety-section" id="safety" aria-labelledby="safety-heading">
  <aside class="project-safety" aria-label="Parent safety note">
    <div class="project-safety-head">
      <span class="project-safety-icon" aria-hidden="true">👨‍👩‍👧</span>
      <h2 id="safety-heading">For Parents & Teachers</h2>
    </div>
    <div class="project-safety-body">{_paragraphs(text)}</div>
  </aside>
</section>"""

def education_support_section(p: dict) -> str:
    proj = p.get("project") or {}
    fields = [
        ("recommended_age", "Recommended age"),
        ("adult_supervision", "Adult supervision"),
        ("classroom_use", "Classroom use"),
        ("parent_prompt", "Parent prompt"),
        ("screen_free_activity", "Screen-free activity"),
        ("next_challenge", "Next challenge"),
    ]
    cards = []
    for key, label in fields:
        value = proj.get(key)
        if value:
            cards.append(
                f'<li class="project-education-card"><strong>{esc(label)}</strong><span>{esc(value)}</span></li>'
            )
    list_fields = [
        ("skills_practiced", "Skills practiced"),
        ("learning_outcomes", "Learning outcomes"),
        ("mini_experiments", "Mini experiments"),
    ]
    for key, label in list_fields:
        items = proj.get(key) or []
        if isinstance(items, list) and items:
            item_html = "".join(f"<li>{esc(item)}</li>" for item in items)
            cards.append(
                f'<li class="project-education-card"><strong>{esc(label)}</strong><ul>{item_html}</ul></li>'
            )
    if not cards:
        return ""
    return f"""<section class="project-section project-education-support" id="learning-support" aria-labelledby="learning-support-heading">
  {project_section_heading("learning-support", "Learning", "Learning Support")}
  <ul class="project-education-grid">{"".join(cards)}</ul>
</section>"""


def project_safety_standards_section(p: dict) -> str:
    title_blob = " ".join(
        [
            p.get("title", ""),
            p.get("category", ""),
            p.get("description", ""),
            str((p.get("project") or {}).get("what_you_build", "")),
        ]
    ).lower()
    notes = [
        "Unplug USB before changing jumper wires. Recheck 3.3 V, 5 V, and GND before reconnecting power.",
        "Do not power motors, pumps, LED strips, or servos from the ESP32 3.3 V pin. Use a suitable external supply and common ground.",
        "Breadboards are for low-current prototypes. Move high-current or unattended builds to proper terminals, enclosure, strain relief, and fusing.",
    ]
    if any(word in title_blob for word in ("relay", "lock", "power strip", "ac ", "mains", "pump", "irrigation")):
        notes.append("Relay and mains-voltage projects require isolation, correct relay ratings, enclosed wiring, and qualified adult supervision.")
    if any(word in title_blob for word in ("robot", "motor", "servo", "arm", "cnc")):
        notes.append("Motors and servos can reset the ESP32 when they draw surge current. Use a separate motor supply, driver module, and flyback protection where needed.")
    if any(word in title_blob for word in ("battery", "portable", "lora", "tracker")):
        notes.append("Li-ion battery builds need a protected cell, proper charger, fuse, and enclosure. Never charge unknown or damaged cells.")
    items = "".join(f"<li>{esc(note)}</li>" for note in notes)
    return f"""<section class="project-section project-safety-section" id="safety-standards" aria-labelledby="safety-standards-heading">
  {project_section_heading("safety-standards", "Safety", "Safety Standards")}
  <ul class="project-callout-list">{items}</ul>
</section>"""


def project_review_references_section(p: dict) -> str:
    proj = p.get("project") or {}
    refs = [
        ("Author & Editorial Team", site_href("author.html")),
        ("Editorial Policy", site_href("editorial-policy.html")),
        ("Testing Methodology", site_href("testing-methodology.html")),
        ("Espressif ESP32 Documentation", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/"),
        ("Arduino ESP32 Core", "https://docs.espressif.com/projects/arduino-esp32/en/latest/"),
    ]
    for ref in proj.get("references", []):
        if isinstance(ref, dict) and ref.get("title") and ref.get("href"):
            refs.append((ref["title"], ref["href"]))
    links = []
    for label, href in refs:
        attrs = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
        links.append(f'<li><a href="{esc(href)}"{attrs}>{esc(label)}</a></li>')
    updated = p.get("date_modified", "2026-06-29")
    level = proj.get("difficulty", "Beginner")
    time = proj.get("estimated_time", "Varies by build")
    return f"""<section class="project-section project-references" id="review-references" aria-labelledby="review-references-heading">
  {project_section_heading("review-references", "Review", "Review, Testing, and References")}
  <div class="project-prose">
    <p><strong>Author:</strong> Abdul Mubeen and the ESP32 Engine editorial team. <strong>Last updated:</strong> {esc(updated)}. <strong>Reviewed:</strong> wiring logic, Arduino code structure, beginner safety, and learning sequence.</p>
    <p><strong>Educational level:</strong> {esc(level)}. <strong>Estimated completion time:</strong> {esc(time)}. This project is for learning and prototyping; production or unattended hardware needs additional engineering review.</p>
  </div>
  <ul class="project-callout-list">{"".join(links)}</ul>
</section>"""


def components_list(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(
                f'<li class="project-part-item"><span class="project-part-icon" aria-hidden="true">📦</span>'
                f'<span class="project-part-body">{esc(item)}</span></li>'
            )
            continue
        name = item.get("item") or item.get("name", "")
        note = item.get("note", "")
        link = item.get("link", "")
        icon = readable_part_icon(item.get("icon", "📦"))
        note_html = f'<span class="project-part-note">{esc(note)}</span>' if note else ""
        name_html = (
            f'<a href="{esc(link)}" class="project-part-name">{esc(name)}</a>'
            if link
            else f'<span class="project-part-name">{esc(name)}</span>'
        )
        rows.append(
            f'<li class="project-part-item"><span class="project-part-icon" aria-hidden="true">{esc(icon)}</span>'
            f'<span class="project-part-body">{name_html}{note_html}</span></li>'
        )
    return f'<ul class="project-parts-list">{"".join(rows)}</ul>'


def related_components_section(items: list) -> str:
    linked = [i for i in items if isinstance(i, dict) and i.get("link")]
    if not linked:
        return ""
    cards = []
    for item in linked:
        icon = item.get("icon", "🔌")
        name = item.get("item") or item.get("name", "")
        note = item.get("note", "")
        link = item.get("link", "")
        icon = readable_project_icon(icon)
        cards.append(
            f"""<a class="project-component-card" href="{esc(link)}">
  <span class="project-component-icon" aria-hidden="true">{esc(icon)}</span>
  <div class="project-component-body">
    <h3>{esc(name)}</h3>
    <p>{esc(note)}</p>
    <span class="project-component-cta">View component<span aria-hidden="true">→</span></span>
  </div>
</a>"""
        )
    return f"""<section class="project-section project-related-components" id="related-components" aria-labelledby="related-components-heading">
  {project_section_heading("related-components", "🔌", "Related Components")}
  <div class="project-component-grid">{"".join(cards)}</div>
</section>"""


def project_wiring_image(slug: str) -> str:
    image = PROJECT_WIRING_DIR / f"{slug}-wiring.svg"
    if image.exists():
        return f"/assets/visuals/projects/wiring/{slug}-wiring.svg"
    return ""


def wiring_diagram_html(src: str, alt: str) -> str:
    if not src:
        return illustration_placeholder(alt, "Wiring Diagram", "🔗")
    return f"""<figure class="mission-illustration mission-illustration--image">
  <img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" decoding="async" width="1200" height="800">
</figure>"""


def wiring_section(p: dict, wiring: dict) -> str:
    if not wiring:
        return ""
    alt = wiring.get("illustration_alt", "Wiring diagram")
    image = wiring.get("image") or project_wiring_image(p.get("slug", ""))
    summary = (wiring.get("summary") or "").strip()
    steps = wiring.get("steps", [])
    summary_html = _paragraphs(summary) if summary else ""
    steps_html = ""
    if steps:
        items = []
        for i, step in enumerate(steps, 1):
            items.append(
                f"""<li class="project-step-wrap">
  <div class="project-step">
    <span class="project-step-num">{i}</span>
    <p class="project-step-text">{esc(step)}</p>
  </div>
</li>"""
            )
        steps_html = f'<ol class="project-steps-list">{"".join(items)}</ol>'
    return f"""<section class="project-section" id="wiring" aria-labelledby="wiring-heading">
  {project_section_heading("wiring", "🔗", "Wiring")}
  {summary_html}
  {wiring_diagram_html(image, alt)}
  {steps_html}
</section>"""


def code_section(p: dict) -> str:
    proj = p.get("project") or {}
    code = proj.get("code") or {}
    content = (code.get("content") or p.get("example_code") or "").strip()
    if not content:
        return ""
    if not code.get("content"):
        code = {"filename": p.get("code_filename", "project.ino"), "content": content}
    return f"""<section class="project-section" id="code" aria-labelledby="code-heading">
  {project_section_heading("code", "⌨️", "Code")}
  <p class="project-section-lead">Copy into Arduino IDE. Install any libraries noted in the component guides first.</p>
  {code_panel(code)}
</section>"""


def output_section(text: str) -> str:
    if not text.strip():
        return ""
    return f"""<section class="project-section project-output" id="output" aria-labelledby="output-heading">
  {project_section_heading("output", "✨", "Expected Output")}
  <div class="project-output-body">{_paragraphs(text)}</div>
</section>"""


def callout_list_section(section_id: str, icon: str, title: str, items: list, css_class: str) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        rows.append(f"<li>{esc(item.get('text', ''))}</li>")
    return f"""<section class="project-section {css_class}" id="{section_id}" aria-labelledby="{section_id}-heading">
  {project_section_heading(section_id, icon, title)}
  <ul class="project-callout-list">{"".join(rows)}</ul>
</section>"""


def prose_section(section_id: str, icon: str, title: str, text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return f"""<section class="project-section" id="{section_id}" aria-labelledby="{section_id}-heading">
  {project_section_heading(section_id, icon, title)}
  <div class="project-prose">{_paragraphs(text)}</div>
</section>"""


def simple_list_section(section_id: str, icon: str, title: str, items: list, css_class: str = "") -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text") or item.get("name", "")
        note = "" if isinstance(item, str) else item.get("note", "")
        note_html = f'<span class="project-part-note">{esc(note)}</span>' if note else ""
        rows.append(f"<li>{esc(text)}{note_html}</li>")
    extra = f" {css_class}" if css_class else ""
    return f"""<section class="project-section{extra}" id="{section_id}" aria-labelledby="{section_id}-heading">
  {project_section_heading(section_id, icon, title)}
  <ul class="project-callout-list">{"".join(rows)}</ul>
</section>"""


def table_section(section_id: str, icon: str, title: str, columns: list, rows: list) -> str:
    if not rows:
        return ""
    head = "".join(f"<th>{esc(col)}</th>" for col in columns)
    body = []
    for row in rows:
        if isinstance(row, dict):
            cells = [row.get(col.lower().replace(" ", "_"), row.get(col, "")) for col in columns]
        else:
            cells = list(row)
        body.append("<tr>" + "".join(f"<td>{esc(str(cell))}</td>" for cell in cells[: len(columns)]) + "</tr>")
    return f"""<section class="project-section" id="{section_id}" aria-labelledby="{section_id}-heading">
  {project_section_heading(section_id, icon, title)}
  <div class="wiring-table-wrap"><table class="wiring-table">
    <thead><tr>{head}</tr></thead>
    <tbody>{"".join(body)}</tbody>
  </table></div>
</section>"""


def faq_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        q = item.get("question", "")
        a = item.get("answer", "")
        if q and a:
            rows.append(
                f"""<details class="accordion-item project-faq-item">
  <summary class="accordion-header">{esc(q)}</summary>
  <div class="accordion-content">{_paragraphs(a)}</div>
</details>"""
            )
    if not rows:
        return ""
    return f"""<section class="project-section project-faqs" id="faqs" aria-labelledby="faqs-heading">
  {project_section_heading("faqs", "FAQ", "FAQs")}
  <div class="project-faq-list">{"".join(rows)}</div>
</section>"""


def build_photos_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        title = item.get("title", "") if isinstance(item, dict) else str(item)
        note = item.get("note", "") if isinstance(item, dict) else ""
        rows.append(
            f"""<li class="project-part-item"><span class="project-part-icon" aria-hidden="true">Photo</span>
<span class="project-part-body"><span class="project-part-name">{esc(title)}</span><span class="project-part-note">{esc(note)}</span></span></li>"""
        )
    return f"""<section class="project-section" id="build-photos" aria-labelledby="build-photos-heading">
  {project_section_heading("build-photos", "Photos", "Build Photos")}
  <ul class="project-parts-list">{"".join(rows)}</ul>
</section>"""


def troubleshooting_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        rows.append(
            f"""<li class="project-trouble-item">
  <strong class="project-trouble-problem">{esc(item.get("problem", ""))}</strong>
  <span class="project-trouble-fix">{esc(item.get("fix", ""))}</span>
</li>"""
        )
    return f"""<section class="project-section project-troubleshooting" id="troubleshooting" aria-labelledby="troubleshooting-heading">
  {project_section_heading("troubleshooting", "🔧", "Troubleshooting")}
  <ul class="project-trouble-list">{"".join(rows)}</ul>
</section>"""


def upgrade_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text", "")
        rows.append(f"<li>{esc(text)}</li>")
    return f"""<section class="project-section project-upgrades" id="upgrades" aria-labelledby="upgrades-heading">
  {project_section_heading("upgrades", "⬆️", "Upgrade Ideas")}
  <ul class="project-upgrade-list">{"".join(rows)}</ul>
</section>"""


def related_links_section(section_id: str, icon: str, title: str, items: list) -> str:
    if not items:
        return ""
    cards = []
    for item in items:
        href = item.get("href", "")
        if href and not href.startswith("/"):
            href = f"/projects/{href}" if section_id == "projects" else href
        label = item.get("title", "")
        desc = item.get("description", "")
        if section_id == "projects":
            slug = project_slug_from_href(href) or item.get("slug", "")
            if slug in PARENT_BY_SLUG:
                project = PARENT_BY_SLUG[slug]
                href = f"/projects/{slug}.html"
                label = project_title(project)
                desc = card_description(project)
        desc_html = f'<p>{esc(desc)}</p>' if desc else ""
        cards.append(
            f"""<a class="project-related-card" href="{esc(href)}">
  <h3>{esc(label)}</h3>
  {desc_html}
  <span class="project-related-cta">Open<span aria-hidden="true">→</span></span>
</a>"""
        )
    return f"""<section class="project-section project-related-{section_id}" id="related-{section_id}" aria-labelledby="related-{section_id}-heading">
  {project_section_heading(f"related-{section_id}", icon, title)}
  <div class="project-related-grid">{"".join(cards)}</div>
</section>"""


def complete_section(p: dict) -> str:
    complete = (p.get("project") or {}).get("complete") or {}
    summary = (complete.get("summary") or "").strip()
    skills = complete.get("skills", [])
    if not summary and not skills:
        return ""
    skills_html = "".join(f"<li>{esc(s)}</li>" for s in skills)
    return f"""<section class="project-section project-complete" id="complete" aria-labelledby="complete-heading">
  <div class="mission-complete-panel project-complete-panel">
    <span class="mission-complete-badge" aria-hidden="true">🏆</span>
    <h2 id="complete-heading">Project Complete!</h2>
    <div class="project-complete-body">{_paragraphs(summary)}</div>
    {"<ul class='mission-skills'>" + skills_html + "</ul>" if skills_html else ""}
  </div>
</section>"""


def render_project_body(p: dict) -> str:
    proj = p.get("project") or {}
    components = proj.get("components") or proj.get("things_you_need") or []
    return f"""<article class="project-journey">
{mission_intro_card(p)}
{story_section(p)}
{eli12_section(p)}
{parent_safety_section(p)}
{education_support_section(p)}
{project_safety_standards_section(p)}
<section class="project-section" id="build" aria-labelledby="build-heading">
  {project_section_heading("build", "Build", "What You Will Build")}
  <div class="project-prose">{_paragraphs(proj.get("what_you_build", ""))}</div>
</section>
{simple_list_section("objectives", "Goals", "Learning Objectives", proj.get("learning_objectives", []))}
<section class="project-section" id="components" aria-labelledby="components-heading">
  {project_section_heading("components", "Parts", "Components List")}
  {components_list(components)}
</section>
{table_section("bom", "Parts", "Bill of Materials", ["Part", "Qty", "Estimated Cost", "Notes"], proj.get("bom", []))}
{related_components_section(components)}
{wiring_section(p, proj.get("wiring") or {})}
{table_section("gpio-map", "GPIO", "GPIO Mapping", ["Signal", "ESP32 Pin", "Direction", "Notes"], proj.get("gpio_map", []))}
{prose_section("circuit", "Circuit", "Circuit Explanation", proj.get("circuit_explanation", ""))}
{prose_section("engineering", "Engineering", "Engineering Explanation", proj.get("engineering_explanation", ""))}
{simple_list_section("libraries", "Libraries", "Libraries", proj.get("libraries", []))}
{code_section(p)}
{prose_section("code-explanation", "Code", "Code Explanation", proj.get("code_explanation", ""))}
{output_section(proj.get("expected_output") or p.get("output", ""))}
{build_photos_section(proj.get("build_photos", []))}
{troubleshooting_section(proj.get("troubleshooting", []))}
{callout_list_section("mistakes", "Mistakes", "Common Mistakes", proj.get("common_mistakes", []), "project-mistakes")}
{simple_list_section("testing", "Testing", "Testing Checklist", proj.get("testing_checklist", []), "project-testing")}
{simple_list_section("engineer-tips", "Tips", "Engineering Tips", proj.get("engineer_tips", []), "project-engineer-tips")}
{simple_list_section("performance", "Performance", "Performance Tips", proj.get("performance_tips", []), "project-performance")}
{upgrade_section(proj.get("upgrade_ideas", []))}
{simple_list_section("applications", "Uses", "Real-World Applications", proj.get("real_world_applications", []), "project-applications")}
{simple_list_section("downloads", "Downloads", "Downloads", proj.get("downloads", []), "project-downloads")}
{related_links_section("guides", "Guides", "Related Guides", proj.get("related_guides", []))}
{related_links_section("projects", "Projects", "Related Projects", proj.get("related_projects", []))}
{faq_section(proj.get("faqs", []))}
{project_review_references_section(p)}
{complete_section(p)}
</article>"""

def project_hero_html(p: dict, category: str) -> str:
    proj = p.get("project") or {}
    icon = readable_project_icon(proj.get("icon", "🚀"))
    title = project_title(p)
    desc = project_meta_description(p)
    hero_image = p.get("hero_image") or p.get("featured_image") or ""
    category_slug = p.get("category_slug") or category.lower().replace("&", "and").replace(" ", "-")
    hero_art = ""
    if hero_image:
        hero_art = (
            f'\n    <div class="project-hero-art">'
            f'<img src="{esc(hero_image)}" alt="" loading="eager" decoding="async"></div>'
        )
    return f"""<div class="project-hero-band">
  <section class="wrap project-hero">
    <nav class="breadcrumb breadcrumb-light" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href("projects.html")}">Projects</a></li><li><a href="{site_href(f"category/{category_slug}.html")}">{esc(category)}</a></li><li aria-current="page">{esc(title)}</li></ol></nav>
    <div class="project-hero-inner">
      <p class="hero-eyebrow project-hero-eyebrow">Build Project</p>
      <div class="project-hero-badges">
        <span class="badge badge-cat">{esc(category)}</span>
      </div>
      <h1 class="project-hero-title">{esc(title)}</h1>
      <p class="project-hero-summary">{esc(desc)}</p>
      {project_meta_badges(p)}
      <span class="project-hero-icon" aria-hidden="true">{esc(icon)}</span>
    </div>{hero_art}
  </section>
</div>"""


def is_golden_project(p: dict) -> bool:
    return p.get("format") == "golden" or bool(p.get("project"))


def render_golden_project_page(p: dict, *, head: str, header: str, footer: str) -> str:
    category = p.get("category", "ESP32 Projects")
    body = f"""{project_hero_html(p, category)}
<section class="section-block wrap project-guide-shell">
{render_project_body(p)}
</section>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body class="project-guide-page">
<main>
{header}
{body}
</main>
{footer}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
<script src="/mission-guide.js" defer></script>
</body>
</html>"""
