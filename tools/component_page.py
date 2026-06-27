from guide_mission import code_panel, illustration_placeholder
from site_layout import badge_class, esc, site_href, UI_JS_SRC, SEARCH_JS_SRC


def component_section_heading(section_id: str, icon: str, title: str) -> str:
    return (
        f'<h2 id="{section_id}-heading">'
        f'<span class="component-section-icon" aria-hidden="true">{icon}</span>'
        f'<span class="component-section-title">{esc(title)}</span>'
        f"</h2>"
    )


def _paragraphs(text: str) -> str:
    if not text:
        return ""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)


def quick_facts_html(facts: list) -> str:
    if not facts:
        return ""
    cards = []
    for item in facts:
        if isinstance(item, str):
            cards.append(
                f'<li class="component-fact-item"><span class="component-fact-value">{esc(item)}</span></li>'
            )
            continue
        label = item.get("label", "")
        value = item.get("value", "")
        cards.append(
            f"""<li class="component-fact-item">
  <span class="component-fact-label">{esc(label)}</span>
  <span class="component-fact-value">{esc(value)}</span>
</li>"""
        )
    return f"""<section class="component-section" id="quick-facts" aria-labelledby="quick-facts-heading">
  {component_section_heading("quick-facts", "⚡", "Quick Facts")}
  <ul class="component-facts-grid">{"".join(cards)}</ul>
</section>"""


def specs_html(specs: list, library: str = "") -> str:
    if not specs and not library:
        return ""
    items = "".join(f"<li>{esc(s)}</li>" for s in specs)
    library_html = ""
    if library:
        library_html = f'<p class="component-section-lead">Arduino library: <strong>{esc(library)}</strong></p>'
    return f"""<section class="component-section" id="specs" aria-labelledby="specs-heading">
  {component_section_heading("specs", "📋", "Technical Specifications")}
  {library_html}
  <ul class="component-spec-list">{items}</ul>
</section>"""


def pinout_html(component: dict) -> str:
    pinout = component.get("pinout", [])
    pins = component.get("pins", [])
    if not pinout and not pins:
        return ""
    if pinout:
        rows = []
        for row in pinout:
            pin = row.get("pin", "")
            role = row.get("role", "")
            connects = row.get("connects", "")
            note = row.get("note", "")
            note_html = f'<span class="component-pin-note">{esc(note)}</span>' if note else ""
            rows.append(
                f"""<li class="component-pin-row">
  <span class="component-pin-name">{esc(pin)}</span>
  <span class="component-pin-role">{esc(role)}</span>
  <span class="component-pin-connects">{esc(connects)}</span>
  {note_html}
</li>"""
            )
        body = f'<ul class="component-pinout-list">{"".join(rows)}</ul>'
    else:
        body = f'<ul class="component-spec-list">{"".join(f"<li>{esc(p)}</li>" for p in pins)}</ul>'
    return f"""<section class="component-section" id="pinout" aria-labelledby="pinout-heading">
  {component_section_heading("pinout", "📍", "Pinout")}
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
  {component_section_heading("wiring", "🔗", "Wiring")}
  {summary_html}
  {illustration_placeholder(alt, "Wiring Diagram", "🔗")}
  {steps_html}
</section>"""


def code_section_html(component: dict) -> str:
    code = component.get("code") or {}
    content = (code.get("content") or component.get("example_code") or "").strip()
    if not content:
        return ""
    if not code.get("content"):
        code = {"filename": component.get("code_filename", "example.ino"), "content": content}
    return f"""<section class="component-section" id="code" aria-labelledby="code-heading">
  {component_section_heading("code", "⌨️", "Code Example")}
  <p class="component-section-lead">Copy into Arduino IDE. Install the library listed above first.</p>
  {code_panel(code)}
</section>"""


def list_panel_html(section_id: str, icon: str, title: str, items: list, css_class: str) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        text = item.get("text") or item.get("mistake", "")
        rows.append(f"<li>{esc(text)}</li>")
    return f"""<section class="component-section {css_class}" id="{section_id}" aria-labelledby="{section_id}-heading">
  {component_section_heading(section_id, icon, title)}
  <ul class="component-callout-list">{"".join(rows)}</ul>
</section>"""


def troubleshooting_html(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        problem = item.get("problem", "")
        fix = item.get("fix", "")
        rows.append(
            f"""<li class="component-trouble-item">
  <strong class="component-trouble-problem">{esc(problem)}</strong>
  <span class="component-trouble-fix">{esc(fix)}</span>
</li>"""
        )
    return f"""<section class="component-section component-troubleshooting" id="troubleshooting" aria-labelledby="troubleshooting-heading">
  {component_section_heading("troubleshooting", "🔧", "Troubleshooting")}
  <ul class="component-trouble-list">{"".join(rows)}</ul>
</section>"""


def related_links_html(section_id: str, icon: str, title: str, items: list, css_class: str) -> str:
    if not items:
        return ""
    cards = []
    for item in items:
        href = item.get("href", "")
        label = item.get("title", "")
        desc = item.get("description", "")
        desc_html = f'<p>{esc(desc)}</p>' if desc else ""
        cards.append(
            f"""<a class="component-related-card" href="{esc(href)}">
  <h3>{esc(label)}</h3>
  {desc_html}
  <span class="component-related-cta">Open<span aria-hidden="true">→</span></span>
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
  {component_section_heading("faq", "❓", "FAQ")}
  <div class="faq-list component-faq">{"".join(items)}</div>
</section>"""


def downloads_html(component: dict) -> str:
    url = component.get("datasheet_url", "")
    note = (component.get("datasheet_note") or "Official manufacturer PDF for teachers and advanced builders.").strip()
    if not url:
        return f"""<section class="component-section component-downloads" id="downloads" aria-labelledby="downloads-heading">
  {component_section_heading("downloads", "📥", "Downloads")}
  <div class="component-download-panel">
    <p class="component-section-lead">{esc(note)}</p>
    <p class="component-download-placeholder">Datasheet coming soon.</p>
  </div>
</section>"""
    return f"""<section class="component-section component-downloads" id="downloads" aria-labelledby="downloads-heading">
  {component_section_heading("downloads", "📥", "Downloads")}
  <div class="component-download-panel">
    <p class="component-section-lead">{esc(note)}</p>
    <a class="btn btn-secondary component-download-btn" href="{esc(url)}" rel="noopener noreferrer" target="_blank">Download Datasheet (PDF)</a>
  </div>
</section>"""


def eli12_html(text: str) -> str:
    if not text.strip():
        return ""
    return f"""<section class="component-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box component-eli12">
    {component_section_heading("eli12", "🧒", "Explain Like I'm 12")}
    <div class="eli12-content">{_paragraphs(text)}</div>
  </div>
</section>"""


def output_html(text: str) -> str:
    if not text.strip():
        return ""
    return f"""<section class="component-section component-output" id="output" aria-labelledby="output-heading">
  {component_section_heading("output", "✨", "Expected Output")}
  <div class="component-output-body">{_paragraphs(text)}</div>
</section>"""


def derive_quick_facts(component: dict) -> list:
    return component.get("quick_facts", [])


def component_card_html(c: dict) -> str:
    img = c.get("image", "")
    img_html = f'<img src="{esc(img)}" alt="{esc(c["name"])}" loading="lazy">' if img else f'<span style="font-size:3rem">{esc(c.get("icon", "🔌"))}</span>'
    return (
        f'<a class="component-card" href="{site_href(f"components/{c["slug"]}.html")}" data-category="{esc(c.get("category", ""))}">'
        f'<div class="component-card-img">{img_html}</div>'
        f'<div class="component-card-body">'
        f'<span class="badge badge-cat">{esc(c.get("category", ""))}</span>'
        f'<span class="badge {badge_class(c.get("difficulty", "Beginner"))}">{esc(c.get("difficulty", "Beginner"))}</span>'
        f'<h3>{esc(c["name"])}</h3>'
        f'<span class="btn btn-card">View Guide<span aria-hidden="true">→</span></span>'
        f"</div></a>"
    )
def derive_wiring(component: dict) -> dict:
    wiring = component.get("wiring") or {}
    if wiring:
        return wiring
    pins = component.get("pins", [])
    if pins:
        return {
            "illustration_alt": f"Wiring diagram for {component.get('name', 'component')}",
            "summary": "Connect each pin as shown in the pinout section above.",
        }
    return {}


def render_component_body(component: dict) -> str:
    library = component.get("library", "")
    return f"""<article class="component-journey">
{eli12_html(component.get("eli12", ""))}
{quick_facts_html(derive_quick_facts(component))}
{specs_html(component.get("specs", []), library)}
{pinout_html(component)}
{wiring_html(derive_wiring(component))}
{code_section_html(component)}
{output_html(component.get("output", ""))}
{list_panel_html("mistakes", "⚠️", "Common Mistakes", component.get("common_mistakes", []), "component-mistakes")}
{troubleshooting_html(component.get("troubleshooting", []))}
{related_links_html("guides", "📖", "Related Guides", component.get("related_guides", []), "component-guides")}
{related_links_html("projects", "🚀", "Related Projects", component.get("related_projects", []), "component-projects")}
{faq_section_html(component.get("faqs", []))}
{downloads_html(component)}
</article>"""


def component_hero_html(component: dict) -> str:
    name = component["name"]
    img = component.get("image", "")
    icon = component.get("icon", "🔌")
    if img:
        media = f'<img src="{esc(img)}" alt="{esc(name)}" loading="eager" width="320" height="240">'
    else:
        media = f'<span class="component-hero-fallback" aria-hidden="true">{esc(icon)}</span>'
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
</script>"""


def render_component_page(component: dict, *, head: str, header: str, footer: str) -> str:
    body = f"""{component_hero_html(component)}
<section class="section-block wrap component-guide-shell">
{render_component_body(component)}
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
