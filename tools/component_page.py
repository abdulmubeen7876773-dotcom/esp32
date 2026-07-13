from component_images import component_image_path
from guide_mission import code_panel, illustration_placeholder
from site_layout import badge_class, esc, site_href, UI_JS_SRC, SEARCH_JS_SRC


FRAMEWORKS = [
    ("arduino", "Arduino", "example.ino"),
    ("platformio", "PlatformIO", "src/main.cpp"),
    ("espidf", "ESP-IDF", "main/main.c"),
]

_ART_RENDER_COUNTS: dict[str, int] = {}


def component_section_heading(section_id: str, icon: str, title: str) -> str:
    icon_text = str(icon or "").strip()
    title_text = str(title or "").strip()
    show_icon = icon_text and not title_text.lower().startswith(icon_text.lower())
    icon_html = f'<span class="component-section-icon" aria-hidden="true">{icon}</span>' if show_icon else ""
    return (
        f'<h2 id="{section_id}-heading">'
        f'{icon_html}'
        f'<span class="component-section-title">{esc(title)}</span>'
        f"</h2>"
    )


def _paragraphs(text: str) -> str:
    if not text:
        return ""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)


def component_art_svg(component: dict) -> str:
    name = component.get("name", "ESP32 component")
    category = component.get("category", "Component")
    slug = "".join(ch if ch.isalnum() else "-" for ch in component.get("slug", "component")).strip("-") or "component"
    _ART_RENDER_COUNTS[slug] = _ART_RENDER_COUNTS.get(slug, 0) + 1
    suffix = f"{slug}-{_ART_RENDER_COUNTS[slug]}"
    board_id = f"ca-board-{suffix}"
    glow_id = f"ca-glow-{suffix}"
    shadow_id = f"ca-shadow-{suffix}"
    initials = "".join(part[0] for part in name.replace("&", " ").split()[:2]).upper() or "C"
    return f"""<svg class="component-art-svg" viewBox="0 0 520 360" role="img" aria-label="{esc(name)} illustration">
  <defs>
    <linearGradient id="{board_id}" x1="120" y1="94" x2="392" y2="252" gradientUnits="userSpaceOnUse">
      <stop stop-color="#2563EB"/><stop offset="1" stop-color="#00B894"/>
    </linearGradient>
    <radialGradient id="{glow_id}" cx="50%" cy="50%" r="60%">
      <stop stop-color="#60A5FA" stop-opacity=".36"/><stop offset="1" stop-color="#60A5FA" stop-opacity="0"/>
    </radialGradient>
    <filter id="{shadow_id}" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="24" stdDeviation="20" flood-color="#0F172A" flood-opacity=".22"/>
    </filter>
  </defs>
  <rect width="520" height="360" rx="34" fill="#F8FAFC"/>
  <circle cx="260" cy="178" r="168" fill="url(#{glow_id})"/>
  <path d="M70 86h74m232 0h74M70 274h86m220 0h74M112 124v46h62m234 66v-46h-64" stroke="#93C5FD" stroke-width="2" stroke-linecap="round" opacity=".55"/>
  <g filter="url(#{shadow_id})">
    <rect x="138" y="92" width="244" height="154" rx="26" fill="url(#{board_id})"/>
    <rect x="174" y="124" width="116" height="78" rx="14" fill="#0F172A" opacity=".88"/>
    <rect x="306" y="126" width="42" height="42" rx="10" fill="#E0F2FE" opacity=".96"/>
    <circle cx="327" cy="183" r="19" fill="#FBBF24"/>
    <text x="232" y="174" text-anchor="middle" fill="#E0F2FE" font-family="Inter,Arial,sans-serif" font-size="26" font-weight="800">{esc(initials)}</text>
    <text x="260" y="282" text-anchor="middle" fill="#475569" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="700">{esc(category)}</text>
    <g stroke="#DBEAFE" stroke-width="5" stroke-linecap="round" opacity=".95">
      <path d="M138 120h-28M138 154h-28M138 188h-28M382 120h28M382 154h28M382 188h28"/>
    </g>
  </g>
</svg>"""


def component_meta_html(component: dict) -> str:
    difficulty = component.get("difficulty", "Beginner")
    minutes = 8 + min(len(component.get("specs", [])), 6)
    return f"""<div class="component-meta-strip" aria-label="Guide metadata">
  <span><strong>{esc(difficulty)}</strong><small>Difficulty</small></span>
  <span><strong>{minutes} min</strong><small>Reading time</small></span>
  <span><strong>20-35 min</strong><small>Bench time</small></span>
  <span><strong>ESP32</strong><small>Compatible</small></span>
</div>"""


def share_actions_html(component: dict) -> str:
    path = site_href(f"components/{component['slug']}.html")
    return f"""<div class="component-share" aria-label="Share this component guide">
  <a class="component-share-btn" href="https://twitter.com/intent/tweet?url=https://esp32engine.com{esc(path)}&text={esc(component['name'])}" rel="noopener" target="_blank">Share</a>
  <button class="component-share-btn" type="button" data-copy-url="https://esp32engine.com{esc(path)}">Copy link</button>
</div>"""


def toc_html() -> str:
    items = [
        ("eli12", "Overview"),
        ("applications", "Applications"),
        ("quick-facts", "Quick facts"),
        ("how-it-works", "How it works"),
        ("specs", "Specs"),
        ("pinout", "Pinout"),
        ("wiring", "Wiring"),
        ("code", "Code"),
        ("troubleshooting", "Troubleshooting"),
        ("faq", "FAQ"),
    ]
    return '<aside class="component-toc" aria-label="Component page contents"><strong>On this page</strong>' + "".join(
        f'<a href="#{sid}">{label}</a>' for sid, label in items
    ) + "</aside>"


def text_section_html(section_id: str, icon: str, title: str, body: str) -> str:
    body = (body or "").strip()
    if not body:
        return ""
    return f"""<section class="component-section" id="{section_id}" aria-labelledby="{section_id}-heading">
  {component_section_heading(section_id, icon, title)}
  <div class="component-section-prose">{_paragraphs(body)}</div>
</section>"""


def quick_facts_html(facts: list) -> str:
    if not facts:
        return ""
    cards = []
    for item in facts:
        if isinstance(item, str):
            cards.append(f'<li class="component-fact-item"><span class="component-fact-value">{esc(item)}</span></li>')
            continue
        cards.append(
            f"""<li class="component-fact-item">
  <span class="component-fact-label">{esc(item.get("label", ""))}</span>
  <span class="component-fact-value">{esc(item.get("value", ""))}</span>
</li>"""
        )
    return f"""<section class="component-section" id="quick-facts" aria-labelledby="quick-facts-heading">
  {component_section_heading("quick-facts", "01", "Quick Facts")}
  <ul class="component-facts-grid">{"".join(cards)}</ul>
</section>"""


def specs_html(specs: list, library: str = "") -> str:
    if not specs and not library:
        return ""
    structured = specs and all(isinstance(s, dict) for s in specs)
    if structured:
        rows = []
        for item in specs:
            rows.append(
                f"""<tr>
  <th scope="row">{esc(item.get("name", ""))}</th>
  <td>{esc(item.get("value", ""))}</td>
  <td>{esc(item.get("why", item.get("note", "")))}</td>
</tr>"""
            )
        specs_body = f"""<div class="wiring-table-wrap">
  <table class="wiring-table">
    <thead><tr><th scope="col">Specification</th><th scope="col">Value</th><th scope="col">Why it matters</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""
    else:
        items = "".join(f"<li>{esc(s)}</li>" for s in specs)
        specs_body = f'<ul class="component-spec-list">{items}</ul>'
    library_html = f'<p class="component-section-lead">Arduino library: <strong>{esc(library)}</strong></p>' if library else ""
    return f"""<section class="component-section" id="specs" aria-labelledby="specs-heading">
  {component_section_heading("specs", "02", "Technical Specifications")}
  {library_html}
  {specs_body}
</section>"""


def pinout_html(component: dict) -> str:
    pinout = component.get("pinout", [])
    pins = component.get("pins", [])
    if not pinout and not pins:
        return ""
    if pinout:
        rows = []
        for row in pinout:
            note = row.get("note", "")
            note_html = f'<span class="component-pin-note">{esc(note)}</span>' if note else ""
            rows.append(
                f"""<li class="component-pin-row">
  <span class="component-pin-name">{esc(row.get("pin", ""))}</span>
  <span class="component-pin-role">{esc(row.get("role", ""))}</span>
  <span class="component-pin-connects">{esc(row.get("connects", ""))}</span>
  {note_html}
</li>"""
            )
        body = f'<ul class="component-pinout-list">{"".join(rows)}</ul>'
    else:
        body = f'<ul class="component-spec-list">{"".join(f"<li>{esc(p)}</li>" for p in pins)}</ul>'
    return f"""<section class="component-section" id="pinout" aria-labelledby="pinout-heading">
  {component_section_heading("pinout", "03", "Pinout")}
  {body}
</section>"""


def wiring_html(wiring: dict) -> str:
    if not wiring:
        return ""
    alt = wiring.get("illustration_alt", "Wiring diagram")
    summary = (wiring.get("summary") or "").strip()
    steps = wiring.get("steps", [])
    summary_html = _paragraphs(summary) if summary else ""
    steps_html = ""
    if steps:
        items = []
        for i, step in enumerate(steps, 1):
            items.append(
                f"""<li class="component-step-wrap">
  <div class="component-step">
    <span class="component-step-num">{i}</span>
    <p class="component-step-text">{esc(step)}</p>
  </div>
</li>"""
            )
        steps_html = f'<ol class="component-steps-list">{"".join(items)}</ol>'
    return f"""<section class="component-section" id="wiring" aria-labelledby="wiring-heading">
  {component_section_heading("wiring", "04", "Wiring Diagram")}
  {summary_html}
  <div class="component-wiring-art">{illustration_placeholder(alt, "Wiring Diagram", "Wire")}</div>
  {steps_html}
</section>"""


def _framework_code(component: dict, framework: str, base_code: dict) -> dict:
    content = base_code.get("content", "")
    if framework == "arduino":
        return {"filename": base_code.get("filename", "example.ino"), "content": content}
    if framework == "platformio":
        wrapped = content if "#include <Arduino.h>" in content else "#include <Arduino.h>\n" + content
        return {"filename": "src/main.cpp", "content": wrapped}
    return {
        "filename": "main/main.c",
        "content": (
            "// ESP-IDF starter structure for this component.\n"
            "// Keep the wiring from the pinout section, then move the read/write logic into app_main().\n\n"
            "#include <stdio.h>\n"
            "#include \"freertos/FreeRTOS.h\"\n"
            "#include \"freertos/task.h\"\n\n"
            "void app_main(void) {\n"
            f"  printf(\"{component.get('name', 'Component')} ready\\n\");\n"
            "  while (true) {\n"
            "    // Add component read/write code here.\n"
            "    vTaskDelay(pdMS_TO_TICKS(1000));\n"
            "  }\n"
            "}\n"
        ),
    }


def code_section_html(component: dict) -> str:
    code = component.get("code") or {}
    content = (code.get("content") or component.get("example_code") or "").strip()
    if not content:
        return ""
    if not code.get("content"):
        code = {"filename": component.get("code_filename", "example.ino"), "content": content}
    tabs = []
    panels = []
    for index, (key, label, _) in enumerate(FRAMEWORKS):
        active = " is-active" if index == 0 else ""
        hidden = "" if index == 0 else " hidden"
        tabs.append(f'<button class="component-code-tab{active}" type="button" data-code-tab="{key}" aria-selected="{str(index == 0).lower()}">{label}</button>')
        panels.append(f'<div class="component-code-panel{active}" data-code-panel="{key}"{hidden}>{code_panel(_framework_code(component, key, code))}</div>')
    notes = (code.get("notes") or code.get("explanation") or "").strip()
    notes_html = f'<div class="component-section-prose">{_paragraphs(notes)}</div>' if notes else ""
    return f"""<section class="component-section" id="code" aria-labelledby="code-heading">
  {component_section_heading("code", "05", "Code Examples")}
  <p class="component-section-lead">Use the same wiring with Arduino IDE, PlatformIO, or ESP-IDF. Start with Arduino, then graduate when you need a larger project structure.</p>
  <div class="component-code-tabs" role="tablist" aria-label="Code framework options">{"".join(tabs)}</div>
  {"".join(panels)}
  {notes_html}
</section>"""


def list_panel_html(section_id: str, icon: str, title: str, items: list, css_class: str) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text") or item.get("mistake", "")
        rows.append(f"<li>{esc(text)}</li>")
    return f"""<section class="component-section {css_class}" id="{section_id}" aria-labelledby="{section_id}-heading">
  {component_section_heading(section_id, icon, title)}
  <ul class="component-callout-list">{"".join(rows)}</ul>
</section>"""


def troubleshooting_html(items: list) -> str:
    if not items:
        return ""
    structured = items and all(isinstance(item, dict) and item.get("cause") for item in items)
    if structured:
        rows = []
        for item in items:
            rows.append(
                f"""<tr>
  <th scope="row">{esc(item.get("problem", ""))}</th>
  <td>{esc(item.get("cause", ""))}</td>
  <td>{esc(item.get("fix", ""))}</td>
</tr>"""
            )
        body = f"""<div class="wiring-table-wrap">
  <table class="wiring-table">
    <thead><tr><th scope="col">Problem</th><th scope="col">Possible cause</th><th scope="col">Solution</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""
        return f"""<section class="component-section component-troubleshooting" id="troubleshooting" aria-labelledby="troubleshooting-heading">
  {component_section_heading("troubleshooting", "06", "Troubleshooting")}
  {body}
</section>"""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        rows.append(
            f"""<li class="component-trouble-item">
  <strong class="component-trouble-problem">{esc(item.get("problem", ""))}</strong>
  <span class="component-trouble-fix">{esc(item.get("fix", ""))}</span>
</li>"""
        )
    return f"""<section class="component-section component-troubleshooting" id="troubleshooting" aria-labelledby="troubleshooting-heading">
  {component_section_heading("troubleshooting", "06", "Troubleshooting")}
  <ul class="component-trouble-list">{"".join(rows)}</ul>
</section>"""


def related_links_html(section_id: str, icon: str, title: str, items: list, css_class: str) -> str:
    if not items:
        return ""
    cards = []
    for item in items:
        desc = item.get("description", "")
        desc_html = f'<p>{esc(desc)}</p>' if desc else ""
        cards.append(
            f"""<a class="component-related-card" href="{esc(item.get("href", ""))}">
  <h3>{esc(item.get("title", ""))}</h3>
  {desc_html}
  <span class="component-related-cta">Open<span aria-hidden="true">-></span></span>
</a>"""
        )
    return f"""<section class="component-section {css_class}" id="{section_id}" aria-labelledby="{section_id}-heading">
  {component_section_heading(section_id, icon, title)}
  <div class="component-related-grid">{"".join(cards)}</div>
</section>"""


def faq_section_html(faqs: list) -> str:
    if not faqs:
        return ""
    items = []
    for item in faqs:
        q = item.get("question", "")
        a = item.get("answer", "")
        items.append(
            f'<div class="faq-item"><button type="button" class="faq-q" aria-expanded="false">{esc(q)}<span class="plus" aria-hidden="true">+</span></button>'
            f'<div class="faq-a" hidden><p>{esc(a)}</p></div></div>'
        )
    return f"""<section class="component-section component-faq-section" id="faq" aria-labelledby="faq-heading">
  {component_section_heading("faq", "07", "FAQ")}
  <div class="faq-list component-faq">{"".join(items)}</div>
</section>"""


def component_quality_faqs(component: dict) -> list[dict]:
    name = component.get("name", "this component")
    category = component.get("category", "ESP32 component")
    difficulty = component.get("difficulty", "Beginner")
    return [
        {
            "question": f"Glossary - What does {name} mean in an ESP32 project?",
            "answer": f"{name} is a {category.lower()} part used with the ESP32. Learn its job first, then connect power, ground, and signal pins exactly as the wiring table shows.",
        },
        {
            "question": "Glossary - What is a signal pin?",
            "answer": "A signal pin is the wire that carries information between the ESP32 and the component. It may be digital, analog, I2C, SPI, PWM, or another protocol depending on the part.",
        },
        {
            "question": f"Parent tips - Is {name} safe for a beginner?",
            "answer": f"For a {difficulty.lower()} ESP32 lesson, this component is suitable when an adult checks the wiring, keeps the project at low voltage, and unplugs USB before moving jumper wires.",
        },
        {
            "question": "Parent tips - What should I watch during the build?",
            "answer": "Watch for reversed power pins, loose jumper wires, and children touching the circuit while it is powered. Most beginner ESP32 mistakes are wiring mistakes, not broken parts.",
        },
        {
            "question": f"Teacher tips - How can {name} fit into a classroom lesson?",
            "answer": f"Use {name} to connect one visible hardware behavior to one software concept. Ask students to predict the reading or output first, then test it on real hardware.",
        },
        {
            "question": "Teacher tips - How should students be assessed?",
            "answer": "Assess whether students can explain the wiring, identify the ESP32 pins used, run the example, describe the expected output, and troubleshoot one intentional mistake.",
        },
        {
            "question": f"Challenge yourself - What is a useful next step after {name} works?",
            "answer": "Change one variable at a time: move to another valid GPIO, adjust the timing, display the value on an OLED, or combine the component with a related project.",
        },
        {
            "question": "Challenge yourself - How can I prove I understand it?",
            "answer": "Disconnect one wire, predict the failure, observe the output, then explain why the failure happened before reconnecting the circuit.",
        },
        {
            "question": "Mini quiz - What should you check before changing wires?",
            "answer": "Unplug USB power first. Then check the pin labels, voltage level, and ground connection before powering the ESP32 again.",
        },
        {
            "question": "Mini quiz - Why is common ground important?",
            "answer": "Common ground gives the ESP32 and the component the same voltage reference. Without it, signal readings can be wrong or unstable.",
        },
    ]


def component_all_faqs(component: dict) -> list[dict]:
    existing = list(component.get("faqs", []) or [])
    seen = {str(item.get("question", "")).strip().lower() for item in existing if isinstance(item, dict)}
    for item in component_quality_faqs(component):
        key = item["question"].strip().lower()
        if key not in seen:
            existing.append(item)
            seen.add(key)
    return existing


def downloads_html(component: dict) -> str:
    url = component.get("datasheet_url", "")
    note = (component.get("datasheet_note") or "Official manufacturer PDF for teachers and advanced builders.").strip()
    if not url:
        action = '<p class="component-download-placeholder">No separate datasheet is needed for this beginner guide.</p>'
    else:
        action = f'<a class="btn btn-secondary component-download-btn" href="{esc(url)}" rel="noopener noreferrer" target="_blank">Download Datasheet (PDF)</a>'
    return f"""<section class="component-section component-downloads" id="downloads" aria-labelledby="downloads-heading">
  {component_section_heading("downloads", "08", "Downloads")}
  <div class="component-download-panel">
    <p class="component-section-lead">{esc(note)}</p>
    {action}
  </div>
</section>"""


def component_reference_section(component: dict) -> str:
    datasheet = component.get("datasheet_url", "")
    refs = [
        ("Testing Methodology", site_href("testing-methodology.html")),
        ("Editorial Policy", site_href("editorial-policy.html")),
        ("Author & Editorial Team", site_href("author.html")),
        ("Espressif ESP32 Documentation", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/"),
        ("Arduino ESP32 Core", "https://docs.espressif.com/projects/arduino-esp32/en/latest/"),
    ]
    if datasheet:
        refs.append(("Component datasheet or manufacturer reference", datasheet))
    items = []
    for label, url in refs:
        external = url.startswith("http")
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
        items.append(f'<li><a href="{esc(url)}"{attrs}>{esc(label)}</a></li>')
    updated = component.get("date_modified", "2026-07-05")
    return f"""<section class="component-section component-references" id="references" aria-labelledby="references-heading">
  {component_section_heading("references", "Review", "Review, Testing, and References")}
  <div class="component-section-prose">
    <p><strong>Author:</strong> Abdul Mubeen and the ESP32 Engine editorial team. <strong>Last updated:</strong> {esc(updated)}. <strong>Reviewed:</strong> wiring, code, beginner safety, and ESP32 compatibility. <strong>Educational level:</strong> {esc(component.get("difficulty", "Beginner"))}.</p>
    <p>Use this component page as an educational starting point. Check official documentation before using the part in production, high-current, outdoor, battery, or safety-critical hardware.</p>
  </div>
  <ul class="component-callout-list">{"".join(items)}</ul>
</section>"""


def eli12_html(text: str) -> str:
    if not text.strip():
        return ""
    return f"""<section class="component-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box component-eli12">
    {component_section_heading("eli12", "00", "Plain-English Overview")}
    <div class="eli12-content">{_paragraphs(text)}</div>
  </div>
</section>"""


def output_html(text: str) -> str:
    if not text.strip():
        return ""
    return f"""<section class="component-section component-output" id="output" aria-labelledby="output-heading">
  {component_section_heading("output", "OK", "Expected Output")}
  <div class="component-output-body">{_paragraphs(text)}</div>
</section>"""


def derive_quick_facts(component: dict) -> list:
    facts = component.get("quick_facts", [])
    if facts:
        return facts
    return [
        {"label": "Category", "value": component.get("category", "Component")},
        {"label": "Level", "value": component.get("difficulty", "Beginner")},
        {"label": "Use with", "value": "ESP32"},
    ]


def component_card_html(c: dict) -> str:
    img = component_image_path(c["slug"]) or c.get("image", "")
    img_html = f'<img src="{esc(img)}" alt="{esc(c["name"])}" width="1376" height="768" loading="lazy" decoding="async">' if img else component_art_svg(c)
    facts = derive_quick_facts(c)
    first_fact = facts[0].get("value", "") if facts and isinstance(facts[0], dict) else "ESP32 ready"
    summary = c.get("summary", "")
    return (
        f'<a class="component-card" href="{site_href(f"components/{c["slug"]}.html")}" data-category="{esc(c.get("category", ""))}" data-name="{esc(c["name"].lower())}" data-summary="{esc(summary.lower())}">'
        f'<div class="component-card-img">{img_html}</div>'
        f'<div class="component-card-body">'
        f'<div class="component-card-badges"><span class="badge badge-cat">{esc(c.get("category", ""))}</span>'
        f'<span class="badge {badge_class(c.get("difficulty", "Beginner"))}">{esc(c.get("difficulty", "Beginner"))}</span></div>'
        f'<h3>{esc(c["name"])}</h3>'
        f'<p>{esc(summary)}</p>'
        f'<div class="component-card-specs"><span>{esc(first_fact)}</span><span>3.3 V friendly</span></div>'
        f'<span class="btn btn-card">View Guide<span aria-hidden="true">-></span></span>'
        f"</div></a>"
    )


def derive_wiring(component: dict) -> dict:
    wiring = component.get("wiring") or {}
    if wiring:
        return wiring
    if component.get("pins", []):
        return {
            "illustration_alt": f"Wiring diagram for {component.get('name', 'component')}",
            "summary": "Connect each pin as shown in the pinout section above.",
        }
    return {}


def render_component_body(component: dict) -> str:
    library = component.get("library", "")
    return f"""<article class="component-journey">
{eli12_html(component.get("eli12", ""))}
{list_panel_html("applications", "A", "Where You Use It", component.get("applications", []), "component-applications")}
{quick_facts_html(derive_quick_facts(component))}
{text_section_html("how-it-works", "H", "How It Works", component.get("how_it_works", ""))}
{specs_html(component.get("specs", []), library)}
{pinout_html(component)}
{wiring_html(derive_wiring(component))}
{code_section_html(component)}
{output_html(component.get("output", ""))}
{list_panel_html("mistakes", "!", "Common Mistakes", component.get("common_mistakes", []), "component-mistakes")}
{troubleshooting_html(component.get("troubleshooting", []))}
{related_links_html("guides", "G", "Related Guides", component.get("related_guides", []), "component-guides")}
{related_links_html("projects", "P", "Related Projects", component.get("related_projects", []), "component-projects")}
{related_links_html("related-components", "C", "Related Components", component.get("related_components", []), "component-related-components")}
{faq_section_html(component_all_faqs(component))}
{component_reference_section(component)}
{downloads_html(component)}
</article>"""


def component_hero_html(component: dict) -> str:
    name = component["name"]
    img = component_image_path(component["slug"]) or component.get("image", "")
    icon = component.get("icon", "C")
    media_img = f'<img src="{esc(img)}" alt="{esc(name)}" loading="eager" width="320" height="240">' if img else f'<span class="component-hero-fallback" aria-hidden="true">{esc(icon)}</span>'
    media = f'<div class="component-hero-photo">{media_img}</div><div class="component-hero-illustration" aria-hidden="true">{component_art_svg(component)}</div>'
    return f"""<div class="component-hero-band">
  <section class="wrap component-hero">
    <nav class="breadcrumb breadcrumb-light" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href("components.html")}">Components</a></li><li aria-current="page">{esc(name)}</li></ol></nav>
    <div class="component-hero-grid">
      <div class="component-hero-copy">
        <p class="hero-eyebrow component-hero-eyebrow">Component Guide</p>
        <div class="component-hero-badges">
          <span class="badge badge-cat">{esc(component.get("category", ""))}</span>
          <span class="badge {badge_class(component.get("difficulty", "Beginner"))}">{esc(component.get("difficulty", "Beginner"))}</span>
        </div>
        <h1 class="component-hero-title">{esc(name)}</h1>
        <p class="component-hero-summary">{esc(component.get("summary", ""))}</p>
        {component_meta_html(component)}
        {share_actions_html(component)}
      </div>
      <div class="component-hero-media">{media}</div>
    </div>
  </section>
</div>"""


def component_faq_script() -> str:
    return """<script>
document.querySelectorAll(".component-faq .faq-q").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var item = btn.closest(".faq-item");
    if (!item) return;
    var open = item.classList.contains("open");
    item.closest(".faq-list").querySelectorAll(".faq-item.open").forEach(function(el) {
      el.classList.remove("open");
      var a = el.querySelector(".faq-a");
      if (a) a.hidden = true;
    });
    item.classList.toggle("open", !open);
    var ans = item.querySelector(".faq-a");
    if (ans) ans.hidden = open;
    btn.setAttribute("aria-expanded", open ? "false" : "true");
  });
});
document.querySelectorAll(".component-code-tab").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var key = btn.dataset.codeTab;
    document.querySelectorAll(".component-code-tab").forEach(function(tab) {
      var active = tab === btn;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });
    document.querySelectorAll(".component-code-panel").forEach(function(panel) {
      var active = panel.dataset.codePanel === key;
      panel.classList.toggle("is-active", active);
      panel.hidden = !active;
    });
  });
});
document.querySelectorAll("[data-copy-url]").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var value = btn.dataset.copyUrl;
    if (navigator.clipboard) navigator.clipboard.writeText(value);
    btn.textContent = "Copied";
    setTimeout(function(){ btn.textContent = "Copy link"; }, 1600);
  });
});
</script>"""


def render_component_page(component: dict, *, head: str, header: str, footer: str, prev_component: dict | None = None, next_component: dict | None = None) -> str:
    prev_next = ""
    if prev_component or next_component:
        prev = f'<a class="component-prevnext-card" href="{site_href(f"components/{prev_component["slug"]}.html")}"><span>Previous</span><strong>{esc(prev_component["name"])}</strong></a>' if prev_component else "<span></span>"
        nxt = f'<a class="component-prevnext-card is-next" href="{site_href(f"components/{next_component["slug"]}.html")}"><span>Next</span><strong>{esc(next_component["name"])}</strong></a>' if next_component else "<span></span>"
        prev_next = f'<nav class="component-prevnext" aria-label="Previous and next component">{prev}{nxt}</nav>'
    body = f"""{component_hero_html(component)}
<section class="section-block wrap component-guide-shell">
{toc_html()}
{render_component_body(component)}
{prev_next}
</section>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body class="component-guide-page">
<main>
{header}
{body}
</main>
{footer}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
<script src="/mission-guide.js" defer></script>
{component_faq_script()}
</body>
</html>"""
