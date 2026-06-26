from pathlib import Path

from site_layout import badge_class, esc, site_href

_ROOT = Path(__file__).resolve().parent.parent


def section_heading(section_id: str, icon: str, title: str) -> str:
    return (
        f'<h2 id="{section_id}-heading">'
        f'<span class="mission-section-icon" aria-hidden="true">{icon}</span>'
        f'<span class="mission-section-title">{esc(title)}</span>'
        f"</h2>"
    )


def illustration_placeholder(alt: str, label: str = "Illustration", icon: str = "🎨") -> str:
    return f"""<figure class="mission-illustration" aria-label="{esc(alt)}">
  <div class="mission-illustration-frame">
    <span class="mission-illustration-icon" aria-hidden="true">{icon}</span>
    <span class="mission-illustration-label">{esc(label)}</span>
    <span class="mission-illustration-alt">{esc(alt)}</span>
  </div>
</figure>"""


def illustration_block(
    alt: str,
    label: str = "Illustration",
    icon: str = "🎨",
    image: str = "",
) -> str:
    if image:
        rel = image.lstrip("/")
        if (_ROOT / rel).is_file():
            return f"""<figure class="mission-illustration mission-illustration--image" aria-label="{esc(alt)}">
  <img src="{esc(image)}" alt="{esc(alt)}" loading="lazy" decoding="async">
</figure>"""
    return illustration_placeholder(alt, label, icon)


def mission_number_label(guide: dict) -> str:
    n = guide.get("mission_number")
    if n is not None:
        return f"Mission {int(n):02d}"
    m = guide.get("mission") or {}
    badge = m.get("badge", "")
    if badge:
        return badge
    return "Mission"


def mission_reading_label(guide: dict) -> str:
    rt = (guide.get("reading_time") or "").strip()
    if rt:
        return (
            rt.replace(" min mission", " minutes")
            .replace(" min read", " minutes")
            .replace(" min", " minutes")
        )
    return "10–15 minutes"


def mission_meta_badges_html(guide: dict, include_trust: bool = True, compact: bool = False) -> str:
    level = guide.get("proficiency_level", "Beginner")
    parts = [
        f'<span class="badge badge-mission">{esc(mission_number_label(guide))}</span>',
        f'<span class="badge {badge_class(level)}">{esc(level)}</span>',
        f'<span class="badge badge-time">{esc(mission_reading_label(guide))}</span>',
    ]
    if include_trust:
        parts.append('<span class="badge badge-parent-safe">Parent Safe</span>')
        parts.append('<span class="badge badge-teacher-friendly">Teacher Friendly</span>')
    cls = "mission-meta-row mission-meta-row-compact" if compact else "mission-meta-row"
    return f'<div class="{cls}">{"".join(parts)}</div>'


def things_list(items: list) -> str:
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(
                f'<li class="mission-thing-item"><span class="mission-thing-icon" aria-hidden="true">📦</span>'
                f'<span class="mission-thing-body">{esc(item)}</span></li>'
            )
            continue
        name = item.get("item") or item.get("name", "")
        note = item.get("note", "")
        link = item.get("link", "")
        icon = item.get("icon", "📦")
        note_html = f'<span class="mission-thing-note">{esc(note)}</span>' if note else ""
        name_html = (
            f'<a href="{esc(link)}" class="mission-thing-name">{esc(name)}</a>'
            if link
            else f'<span class="mission-thing-name">{esc(name)}</span>'
        )
        rows.append(
            f'<li class="mission-thing-item"><span class="mission-thing-icon" aria-hidden="true">{esc(icon)}</span>'
            f'<span class="mission-thing-body">{name_html}{note_html}</span></li>'
        )
    return f'<ul class="mission-things-list">{"".join(rows)}</ul>'


def component_cards_section(items: list) -> str:
    linked = [i for i in items if isinstance(i, dict) and i.get("link")]
    if not linked:
        return ""
    cards = []
    for item in linked:
        icon = item.get("icon", "🔌")
        name = item.get("item") or item.get("name", "")
        note = item.get("note", "")
        link = item.get("link", "")
        cards.append(
            f"""<a class="mission-component-card" href="{esc(link)}">
  <span class="mission-component-icon" aria-hidden="true">{esc(icon)}</span>
  <div class="mission-component-body">
    <h3>{esc(name)}</h3>
    <p>{esc(note)}</p>
    <span class="mission-component-cta">View component guide<span aria-hidden="true">→</span></span>
  </div>
</a>"""
        )
    return f"""<section class="mission-section mission-components" id="components" aria-labelledby="components-heading">
  {section_heading("components", "🔌", "Component Spotlight")}
  <p class="mission-section-lead">Learn more about your ESP32 board.</p>
  <div class="mission-component-grid">{"".join(cards)}</div>
</section>"""


def safety_block(items: list) -> str:
    if not items:
        return ""
    lines = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text", "")
        lines.append(f"<li>{esc(text)}</li>")
    return f"""<section class="mission-section mission-safety-section" id="safety" aria-labelledby="safety-heading">
  <aside class="mission-safety" aria-label="Safety first">
    <div class="mission-safety-head">
      <span class="mission-safety-icon" aria-hidden="true">⚠️</span>
      <h2 id="safety-heading">Safety First</h2>
    </div>
    <ul>{"".join(lines)}</ul>
  </aside>
</section>"""


def code_panel(code: dict) -> str:
    filename = code.get("filename", "sketch.ino")
    content = (code.get("content") or "").strip("\n")
    return f"""<div class="code-panel">
  <div class="code-panel-head">
    <div class="code-panel-chrome" aria-hidden="true">
      <span class="code-dot code-dot-red"></span>
      <span class="code-dot code-dot-yellow"></span>
      <span class="code-dot code-dot-green"></span>
    </div>
    <span class="code-panel-filename">{esc(filename)}</span>
    <button type="button" class="btn-copy" data-copy aria-label="Copy code to clipboard">
      <svg class="btn-copy-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
      <span class="btn-copy-label">Copy</span>
    </button>
  </div>
  <pre class="code-block"><code>{esc(content)}</code></pre>
</div>"""


def quiz_block(questions: list) -> str:
    if not questions:
        return ""
    blocks = []
    for i, q in enumerate(questions):
        options = q.get("options", [])
        correct = int(q.get("correct", 0))
        explanation = q.get("explanation", "")
        qid = f"quiz-q-{i}"
        opts_html = "".join(
            f'<button type="button" class="quiz-option" data-index="{j}" data-correct="{1 if j == correct else 0}">{esc(opt)}</button>'
            for j, opt in enumerate(options)
        )
        blocks.append(
            f"""<div class="quiz-question" data-quiz-q="{i}" data-explanation="{esc(explanation)}">
  <p class="quiz-q-text" id="{qid}"><span class="quiz-q-num">Q{i + 1}.</span> {esc(q.get("question", ""))}</p>
  <div class="quiz-options" role="group" aria-labelledby="{qid}">{opts_html}</div>
  <p class="quiz-feedback" role="status" aria-live="polite" hidden></p>
</div>"""
        )
    return f"""<section class="mission-section mission-quiz" id="quiz" aria-labelledby="quiz-heading">
  {section_heading("quiz", "❓", "Mini Quiz")}
  <p class="mission-section-lead">Quick check — no grades, just confidence!</p>
  <div class="mission-quiz-list">{"".join(blocks)}</div>
</section>"""


def next_mission_cards(missions: list) -> str:
    if not missions:
        return ""
    cards = []
    for i, m in enumerate(missions):
        slug = m.get("slug", "")
        href = site_href(f"guides/{slug}.html") if slug else site_href("guides.html")
        label = "Up Next" if i == 0 else "Also Try"
        cards.append(
            f"""<a class="next-mission-card" href="{esc(href)}">
  <span class="next-mission-label">{esc(label)}</span>
  <h3>{esc(m.get("title", ""))}</h3>
  <p>{esc(m.get("description", ""))}</p>
  <span class="btn btn-card">Start Mission<span aria-hidden="true">→</span></span>
</a>"""
        )
    return f"""<section class="mission-section mission-next" id="next-mission" aria-labelledby="next-heading">
  {section_heading("next", "🚀", "Continue Your Journey")}
  <div class="next-mission-grid">{"".join(cards)}</div>
</section>"""


def mission_card_html(guide: dict) -> str:
    m = guide.get("mission") or {}
    icon = m.get("icon", "🚀")
    title = m.get("title", "")
    label = mission_number_label(guide)
    return f"""<header class="mission-card">
  <div class="mission-card-glow" aria-hidden="true"></div>
  <span class="mission-card-icon" aria-hidden="true">{esc(icon)}</span>
  <span class="mission-card-badge">{esc(label)}</span>
  <h2 class="mission-card-title">{esc(title)}</h2>
</header>"""


def reference_intro_card(guide: dict) -> str:
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip()
    return f"""<div class="reference-intro-card">
  <span class="reference-intro-label">Reference Guide</span>
  <h2 class="reference-intro-title">{esc(headline)}</h2>
</div>"""


def wiring_steps_html(steps: list) -> str:
    items = []
    for i, step in enumerate(steps, 1):
        items.append(
            f"""<li class="mission-step-wrap">
  <div class="mission-step">
    <span class="mission-num">{i}</span>
    <p class="mission-step-text">{esc(step)}</p>
  </div>
</li>"""
        )
    return f'<ol class="mission-steps-list">{"".join(items)}</ol>'


def render_friendly_intro(guide: dict, *, is_mission: bool) -> str:
    m = guide.get("mission") or {}
    intro = guide.get("intro") or {}

    if is_mission:
        header = mission_card_html(guide)
        story = (m.get("story") or "").strip()
        eli12 = (m.get("eli12") or "").strip()
        safety_html = ""
    else:
        header = reference_intro_card(guide)
        story = (intro.get("story") or guide.get("lead") or "").strip()
        eli12 = (intro.get("eli12") or "").strip()
        safety = intro.get("safety", [])
        if not safety:
            safety = [
                {"text": "Work at a clear desk with good lighting."},
                {"text": "Children should have an adult nearby when plugging in USB cables."},
                {"text": "Disconnect power before changing wiring."},
            ]
        safety_html = safety_block(safety)

    story_html = ""
    if story:
        story_html = f"""<section class="mission-section guide-intro-story" id="story" aria-labelledby="story-heading">
  {section_heading("story", "📖", "The Story")}
  <div class="mission-story">{_paragraphs(story)}</div>
</section>"""

    eli12_html = ""
    if eli12:
        eli12_html = f"""<section class="mission-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box mission-eli12">
    {section_heading("eli12", "🧒", "Explain Like I'm 12")}
    <div class="eli12-content">{_paragraphs(eli12)}</div>
  </div>
</section>"""

    return f"""<div class="guide-friendly-intro">
{header}
{story_html}
{eli12_html}
{safety_html}
</div>"""


def render_mission_guide(guide: dict) -> str:
    m = guide.get("mission") or {}
    intro_html = render_friendly_intro(guide, is_mission=True)

    build = m.get("what_you_build", "").strip()
    build_html = ""
    if build:
        build_html = f"""<section class="mission-section" id="build" aria-labelledby="build-heading">
  {section_heading("build", "🛠", "What You'll Build")}
  <div class="mission-prose">{_paragraphs(build)}</div>
</section>"""

    things = m.get("things_you_need", [])
    things_html = ""
    if things:
        things_html = f"""<section class="mission-section" id="parts" aria-labelledby="parts-heading">
  {section_heading("parts", "🧰", "Things You'll Need")}
  {things_list(things)}
</section>"""

    safety_html = safety_block(m.get("safety", []))
    components_html = component_cards_section(things)

    concept = m.get("concept") or {}
    concept_body = (concept.get("body") or "").strip()
    concept_html = ""
    if concept_body or concept.get("illustration_alt"):
        concept_html = f"""<section class="mission-section" id="concept" aria-labelledby="concept-heading">
  {section_heading("concept", "💡", concept.get("title", "The Concept"))}
  {illustration_placeholder(concept.get("illustration_alt", "Concept diagram"), "Concept Illustration", "💡")}
  <div class="mission-prose">{_paragraphs(concept_body)}</div>
</section>"""

    wiring = m.get("wiring") or {}
    wiring_steps = wiring.get("steps", [])
    wiring_html = ""
    if wiring_steps or wiring.get("illustration_alt"):
        wiring_html = f"""<section class="mission-section" id="wiring" aria-labelledby="wiring-heading">
  {section_heading("wiring", "🔗", "Wiring Diagram")}
  <p class="mission-section-lead">Follow these steps in order. Unplug USB before you change any wires.</p>
  {illustration_block(wiring.get("illustration_alt", "Wiring diagram"), "Wiring Diagram", "🔗", wiring.get("image", ""))}
  {wiring_steps_html(wiring_steps)}
</section>"""

    code = m.get("code") or {}
    code_html = ""
    if code.get("content"):
        code_html = f"""<section class="mission-section" id="code" aria-labelledby="code-heading">
  {section_heading("code", "⌨️", "Code")}
  <p class="mission-section-lead">Copy this into Arduino IDE, then click Upload.</p>
  {code_panel(code)}
</section>"""

    output = m.get("expected_output", "").strip()
    output_html = ""
    if output:
        output_html = f"""<section class="mission-section mission-output" id="output" aria-labelledby="output-heading">
  {section_heading("output", "✨", "Expected Output")}
  <div class="mission-output-body">{_paragraphs(output)}</div>
</section>"""

    quiz_html = quiz_block(m.get("quiz", []))

    challenge = m.get("challenge", "").strip()
    challenge_html = ""
    if challenge:
        challenge_html = f"""<section class="mission-section mission-challenge" id="challenge" aria-labelledby="challenge-heading">
  {section_heading("challenge", "🎯", "Challenge Yourself")}
  <div class="mission-challenge-box">{_paragraphs(challenge)}</div>
</section>"""

    complete = m.get("complete") or {}
    complete_summary = (complete.get("summary") or "").strip()
    skills = complete.get("skills", [])
    skills_html = "".join(f"<li>{esc(s)}</li>" for s in skills)
    complete_html = f"""<section class="mission-section mission-complete" id="complete" aria-labelledby="complete-heading">
  <div class="mission-complete-panel">
    <span class="mission-complete-badge" aria-hidden="true">🏆</span>
    <h2 id="complete-heading">Mission Complete!</h2>
    <div class="mission-complete-body">{_paragraphs(complete_summary)}</div>
    {"<ul class='mission-skills'>" + skills_html + "</ul>" if skills_html else ""}
  </div>
</section>"""

    next_html = next_mission_cards(m.get("next_missions", []))

    return f"""<article class="mission-journey">
{intro_html}
{build_html}
{things_html}
{safety_html}
{components_html}
{concept_html}
{wiring_html}
{code_html}
{output_html}
{quiz_html}
{challenge_html}
{complete_html}
{next_html}
</article>"""


def mission_index_card(guide: dict) -> str:
    slug = guide["slug"]
    href = site_href(f"guides/{slug}.html")
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip()
    desc = guide.get("lead") or guide.get("meta_description", "")
    if len(desc) > 120:
        desc = desc[:117].rstrip() + "…"
    m = guide.get("mission") or {}
    icon = m.get("icon", "🚀")
    return f"""<a class="mission-index-card" href="{esc(href)}">
  <span class="mission-index-icon" aria-hidden="true">{esc(icon)}</span>
  {mission_meta_badges_html(guide)}
  <h3>{esc(headline)}</h3>
  <p>{esc(desc)}</p>
  <span class="btn btn-card">Start Mission<span aria-hidden="true">→</span></span>
</a>"""


def _paragraphs(text: str) -> str:
    if not text:
        return ""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)
