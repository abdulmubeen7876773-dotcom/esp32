import re
from pathlib import Path

from site_layout import badge_class, esc, site_href

_ROOT = Path(__file__).resolve().parent.parent

_ARDUINO_KEYWORDS = frozenset(
    {
        "void", "int", "if", "else", "for", "while", "return", "boolean", "char",
        "long", "float", "double", "byte", "uint8_t", "uint16_t", "uint32_t",
        "true", "false",
    }
)
_ARDUINO_BUILTINS = frozenset(
    {
        "pinMode", "digitalWrite", "digitalRead", "analogRead", "analogWrite",
        "delay", "delayMicroseconds", "Serial", "print", "println", "begin",
        "setup", "loop",
    }
)
_ARDUINO_CONSTANTS = frozenset({"HIGH", "LOW", "INPUT", "OUTPUT", "INPUT_PULLUP"})
_TOKEN_RE = re.compile(r"\#[a-zA-Z_]\w*|\b[A-Za-z_][A-Za-z0-9_]*\b|\b\d+(?:\.\d+)?\b")


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
    academy = guide.get("academy") or {}
    if academy.get("mission_id"):
        return str(academy["mission_id"])
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
    academy = guide.get("academy") or {}
    parts = [
        f'<span class="badge badge-mission">{esc(mission_number_label(guide))}</span>',
        f'<span class="badge badge-cat">{esc(academy.get("level", "Academy"))}</span>' if academy.get("level") else "",
        f'<span class="badge {badge_class(level)}">{esc(level)}</span>',
        f'<span class="badge badge-time">{esc(mission_reading_label(guide))}</span>',
    ]
    if include_trust:
        parts.append('<span class="badge badge-parent-safe">Parent Safe</span>')
        parts.append('<span class="badge badge-teacher-friendly">Teacher Friendly</span>')
    cls = "mission-meta-row mission-meta-row-compact" if compact else "mission-meta-row"
    return f'<div class="{cls}">{"".join(parts)}</div>'


def academy_link_list(items: list, fallback_prefix: str = "guides") -> str:
    rows = []
    for item in items:
        if isinstance(item, str):
            title = item.replace("-", " ").title()
            href = site_href(f"{fallback_prefix}/{item}.html")
            desc = ""
        else:
            title = item.get("title") or item.get("name") or item.get("slug", "")
            href = item.get("href", "")
            slug = item.get("slug", "")
            desc = item.get("description", "")
            if not href and slug:
                href = site_href(f"{fallback_prefix}/{slug}.html")
        desc_html = f'<span class="meta">{esc(desc)}</span>' if desc else ""
        if href:
            rows.append(f'<li><a href="{esc(href)}"><strong>{esc(title)}</strong></a> {desc_html}</li>')
        else:
            rows.append(f"<li><strong>{esc(title)}</strong> {desc_html}</li>")
    return f'<ul class="guide-related-list">{"".join(rows)}</ul>' if rows else ""


def academy_overview_section(guide: dict) -> str:
    academy = guide.get("academy") or {}
    if not academy:
        return ""
    current = academy.get("mission_id") or mission_number_label(guide)
    previous = academy.get("previous_mission")
    next_item = academy.get("next_mission")
    previous_html = academy_link_list([previous], "guides") if previous else "<p>Start here.</p>"
    next_html = academy_link_list([next_item], "guides") if next_item else "<p>This path continues through projects and advanced topics.</p>"
    prereq_html = academy_link_list(academy.get("prerequisites", []), "guides") or "<p>No prerequisites.</p>"
    skills = academy.get("skills_learned", [])
    skills_html = "".join(f"<li>{esc(s)}</li>" for s in skills)
    outcome = academy.get("expected_outcome", "")
    challenge = academy.get("mini_challenge", "")
    return f"""<section class="mission-section academy-overview" id="academy-path" aria-labelledby="academy-path-heading">
  {section_heading("academy-path", "PATH", "Academy Path")}
  <div class="mission-build-panel">
    <p><strong>Current mission:</strong> {esc(current)} · {esc(academy.get("level", "ESP32 Academy"))}</p>
    <p><strong>Expected outcome:</strong> {esc(outcome)}</p>
    <p><strong>Mini challenge:</strong> {esc(challenge)}</p>
  </div>
  <h3>Required Knowledge</h3>
  {prereq_html}
  <h3>Skills You Unlock</h3>
  {"<ul class='mission-bullets'>" + skills_html + "</ul>" if skills_html else "<p>Skills are listed in the mission complete section.</p>"}
  <div class="next-mission-grid">
    <div class="next-mission-card"><span class="next-mission-label">Previous</span>{previous_html}</div>
    <div class="next-mission-card"><span class="next-mission-label">Next</span>{next_html}</div>
  </div>
</section>"""


def academy_unlocks_section(guide: dict) -> str:
    academy = guide.get("academy") or {}
    if not academy:
        return ""
    components = academy.get("unlocked_components", [])
    projects = academy.get("unlocked_projects", [])
    future = academy.get("future_paths", [])
    if not components and not projects and not future:
        return ""
    return f"""<section class="mission-section academy-unlocks" id="unlocks" aria-labelledby="unlocks-heading">
  {section_heading("unlocks", "KEY", "What This Unlocks")}
  <h3>Unlocked Components</h3>
  {academy_link_list(components, "components") or "<p>No new components in this mission.</p>"}
  <h3>Unlocked Projects</h3>
  {academy_link_list(projects, "projects") or "<p>Complete the next mission to unlock projects.</p>"}
  <h3>Continue Learning</h3>
  {academy_link_list(future, "guides") or "<p>Continue with the next mission.</p>"}
</section>"""


def mission_list_section(section_id: str, icon: str, title: str, items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text", "")
        rows.append(f"<li>{esc(text)}</li>")
    return f"""<section class="mission-section" id="{section_id}" aria-labelledby="{section_id}-heading">
  {section_heading(section_id, icon, title)}
  <ul class="mission-bullets">{"".join(rows)}</ul>
</section>"""


def mission_prose_section(section_id: str, icon: str, title: str, text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return f"""<section class="mission-section" id="{section_id}" aria-labelledby="{section_id}-heading">
  {section_heading(section_id, icon, title)}
  <div class="mission-prose">{_rich_content(text)}</div>
</section>"""


def gpio_table_section(rows: list) -> str:
    if not rows:
        return ""
    body = []
    for row in rows:
        signal = row.get("signal", "")
        pin = row.get("esp32_pin", "")
        mode = row.get("mode", "")
        notes = row.get("notes", "")
        body.append(f"<tr><td>{esc(signal)}</td><td>{esc(pin)}</td><td>{esc(mode)}</td><td>{esc(notes)}</td></tr>")
    return f"""<section class="mission-section" id="gpio-table" aria-labelledby="gpio-table-heading">
  {section_heading("gpio-table", "GPIO", "GPIO Table")}
  <div class="wiring-table-wrap"><table class="wiring-table">
    <thead><tr><th>Signal</th><th>ESP32 Pin</th><th>Mode</th><th>Notes</th></tr></thead>
    <tbody>{"".join(body)}</tbody>
  </table></div>
</section>"""


def comparison_table_section(rows: list) -> str:
    if not rows:
        return ""
    body = []
    for row in rows:
        mode = row.get("mode", "")
        default = row.get("default_state", "")
        wiring = row.get("wiring", "")
        use = row.get("when_to_use", "")
        body.append(f"<tr><td>{esc(mode)}</td><td>{esc(default)}</td><td>{esc(wiring)}</td><td>{esc(use)}</td></tr>")
    return f"""<section class="mission-section" id="input-comparison" aria-labelledby="input-comparison-heading">
  {section_heading("input-comparison", "COMPARE", "INPUT vs INPUT_PULLUP")}
  <div class="wiring-table-wrap"><table class="wiring-table">
    <thead><tr><th>Mode</th><th>Default State</th><th>Typical Wiring</th><th>When to Use</th></tr></thead>
    <tbody>{"".join(body)}</tbody>
  </table></div>
</section>"""


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


def component_cards_section(items: list, lead: str = "") -> str:
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
    lead_text = lead or "Learn more about the parts in your circuit."
    return f"""<section class="mission-section mission-components" id="components" aria-labelledby="components-heading">
  {section_heading("components", "🔌", "Component Spotlight")}
  <p class="mission-section-lead">{esc(lead_text)}</p>
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


def highlight_arduino(source: str) -> str:
    lines = [_highlight_code_line(line) for line in source.split("\n")]
    return "\n".join(lines)


def _highlight_code_line(line: str) -> str:
    if not line:
        return ""
    comment = ""
    code = line
    if "//" in line:
        idx = line.index("//")
        code, comment = line[:idx], line[idx:]
    if code.strip().startswith("#"):
        return f'<span class="tok-pre">{esc(line)}</span>'
    highlighted = _highlight_tokens(code)
    if comment:
        highlighted += f'<span class="tok-com">{esc(comment)}</span>'
    return highlighted


def _highlight_tokens(code: str) -> str:
    parts = []
    last = 0
    for match in _TOKEN_RE.finditer(code):
        parts.append(esc(code[last : match.start()]))
        word = match.group(0)
        if word.startswith("#"):
            parts.append(f'<span class="tok-pre">{esc(word)}</span>')
        elif word in _ARDUINO_CONSTANTS:
            parts.append(f'<span class="tok-const">{esc(word)}</span>')
        elif word in _ARDUINO_BUILTINS:
            parts.append(f'<span class="tok-fn">{esc(word)}</span>')
        elif word in _ARDUINO_KEYWORDS:
            parts.append(f'<span class="tok-kw">{esc(word)}</span>')
        elif word[0].isdigit():
            parts.append(f'<span class="tok-num">{esc(word)}</span>')
        else:
            parts.append(esc(word))
        last = match.end()
    parts.append(esc(code[last:]))
    return "".join(parts)


def code_panel(code: dict) -> str:
    filename = code.get("filename", "sketch.ino")
    content = (code.get("content") or "").strip("\n")
    highlighted = highlight_arduino(content)
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
  <pre class="code-block"><code class="language-arduino">{highlighted}</code></pre>
</div>"""


def quiz_block(questions: list) -> str:
    if not questions:
        return ""
    blocks = []
    for i, q in enumerate(questions):
        options = q.get("options", [])
        correct = int(q.get("correct", 0))
        explanation = q.get("explanation", "")
        correct_fb = q.get("correct_feedback", "")
        wrong_fb = q.get("wrong_feedback", "")
        qid = f"quiz-q-{i}"
        opts_html = "".join(
            f'<button type="button" class="quiz-option" data-index="{j}" data-correct="{1 if j == correct else 0}">{esc(opt)}</button>'
            for j, opt in enumerate(options)
        )
        blocks.append(
            f"""<div class="quiz-question" data-quiz-q="{i}" data-explanation="{esc(explanation)}" data-correct-feedback="{esc(correct_fb)}" data-wrong-feedback="{esc(wrong_fb)}">
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
  <div class="mission-story">{_rich_content(story)}</div>
</section>"""

    eli12_html = ""
    if eli12:
        eli12_html = f"""<section class="mission-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box mission-eli12">
    {section_heading("eli12", "🧒", "Explain Like I'm 12")}
    <div class="eli12-content">{_rich_content(eli12)}</div>
  </div>
</section>"""

    return f"""<div class="guide-friendly-intro">
{header}
{story_html}
{eli12_html}
{safety_html}
</div>"""


def _output_preview(text: str) -> str:
    if not text.strip():
        return ""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    return blocks[0] if blocks else ""


def code_section(code: dict, output: str) -> str:
    if not code.get("content"):
        return ""
    notes = (code.get("notes") or code.get("explain") or "").strip()
    notes_html = ""
    if notes:
        notes_html = f'<div class="mission-code-notes">{_rich_content(notes)}</div>'
    preview = _output_preview(output)
    preview_html = ""
    if preview:
        preview_html = f"""<aside class="mission-code-preview" aria-label="Expected result preview">
  <h3 class="mission-code-preview-title"><span class="mission-code-preview-icon" aria-hidden="true">✨</span> What you'll see</h3>
  <div class="mission-code-preview-body">{_rich_content(preview)}</div>
</aside>"""
    return f"""<section class="mission-section" id="code" aria-labelledby="code-heading">
  {section_heading("code", "⌨️", "Code")}
  <p class="mission-section-lead">Copy this into Arduino IDE, then click Upload.</p>
  <div class="mission-code-layout">
    <div class="mission-code-main">{code_panel(code)}</div>
    {preview_html}
  </div>
  {notes_html}
</section>"""


def challenge_section(challenge: str, items: list) -> str:
    if items:
        rows = []
        for item in items:
            icon = item.get("icon", "🎯") if isinstance(item, dict) else "🎯"
            text = item.get("text", item) if isinstance(item, dict) else str(item)
            rows.append(
                f'<li class="mission-challenge-item">'
                f'<span class="mission-challenge-icon" aria-hidden="true">{esc(icon)}</span>'
                f'<span class="mission-challenge-text">{esc(text)}</span></li>'
            )
        body = f'<ul class="mission-challenge-list">{"".join(rows)}</ul>'
    elif challenge.strip():
        body = f'<div class="mission-challenge-box">{_rich_content(challenge)}</div>'
    else:
        return ""
    return f"""<section class="mission-section mission-challenge" id="challenge" aria-labelledby="challenge-heading">
  {section_heading("challenge", "🎯", "Challenge Yourself")}
  <p class="mission-section-lead">No wrong answers — experiment and have fun!</p>
  {body}
</section>"""


def common_problems_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(f"<li>{esc(item)}</li>")
            continue
        title = item.get("problem") or item.get("title", "")
        cause = item.get("cause", "")
        fix = item.get("fix", "")
        cause_html = f"<p><strong>Likely cause:</strong> {esc(cause)}</p>" if cause else ""
        fix_html = f"<p><strong>Fix:</strong> {esc(fix)}</p>" if fix else ""
        rows.append(f"<li><h3>{esc(title)}</h3>{cause_html}{fix_html}</li>")
    return f"""<section class="mission-section" id="troubleshooting" aria-labelledby="troubleshooting-heading">
  {section_heading("troubleshooting", "!", "Common Problems")}
  <p class="mission-section-lead">Most ESP32 problems are wiring, power, library, or timing issues. Check these first.</p>
  <ul class="mission-bullets">{"".join(rows)}</ul>
</section>"""


def mission_faq_section(items: list) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        q = item.get("question") or item.get("q", "")
        a = item.get("answer") or item.get("a", "")
        rows.append(f"<li><h3>{esc(q)}</h3><p>{esc(a)}</p></li>")
    return f"""<section class="mission-section" id="faqs" aria-labelledby="faqs-heading">
  {section_heading("faqs", "?", "FAQs")}
  <ul class="mission-bullets">{"".join(rows)}</ul>
</section>"""


def render_mission_guide(guide: dict) -> str:
    m = guide.get("mission") or {}
    intro_html = render_friendly_intro(guide, is_mission=True)
    academy_html = academy_overview_section(guide)
    objectives_html = mission_list_section("objectives", "OBJ", "Learning Objectives", m.get("learning_objectives", []))

    build = m.get("what_you_build", "").strip()
    build_html = ""
    if build:
        build_html = f"""<section class="mission-section mission-build" id="build" aria-labelledby="build-heading">
  {section_heading("build", "BUILD", "What You'll Build")}
  <div class="mission-build-panel">{_rich_content(build)}</div>
</section>"""

    things = m.get("things_you_need", [])
    things_html = ""
    if things:
        things_html = f"""<section class="mission-section" id="parts" aria-labelledby="parts-heading">
  {section_heading("parts", "PARTS", "Things You'll Need")}
  {things_list(things)}
</section>"""

    safety_html = safety_block(m.get("safety", []))
    components_html = component_cards_section(things, m.get("component_spotlight_lead", ""))

    concept = m.get("concept") or {}
    concept_body = (concept.get("body") or "").strip()
    concept_html = ""
    if concept_body or concept.get("illustration_alt"):
        concept_html = f"""<section class="mission-section" id="concept" aria-labelledby="concept-heading">
  {section_heading("concept", "IDEA", concept.get("title", "The Concept"))}
  {illustration_block(concept.get("illustration_alt", "Concept diagram"), "Concept Illustration", "IDEA", concept.get("image", ""))}
  <div class="mission-prose">{_rich_content(concept_body)}</div>
</section>"""
    engineering_html = mission_prose_section("engineering", "ENG", "Engineering Explanation", m.get("engineering_explanation", ""))
    analogy_html = mission_prose_section("analogy", "REAL", "Real-Life Analogy", m.get("real_life_analogy", ""))
    floating_recap_html = mission_prose_section("floating-recap", "RECAP", "Floating Pin Recap", m.get("floating_pin_recap", ""))
    internal_resistor_html = mission_prose_section("internal-resistor", "INT", "Internal Pull-Up Resistor", m.get("internal_resistor_explanation", ""))
    external_resistor_html = mission_prose_section("external-resistor", "EXT", "External Pull-Up and Pull-Down Resistors", m.get("external_resistor_explanation", ""))
    comparison_html = comparison_table_section(m.get("comparison_table", []))

    wiring = m.get("wiring") or {}
    wiring_steps = wiring.get("steps", [])
    wiring_html = ""
    if wiring_steps or wiring.get("illustration_alt"):
        wiring_html = f"""<section class="mission-section" id="wiring" aria-labelledby="wiring-heading">
  {section_heading("wiring", "WIRE", "Breadboard Wiring")}
  <p class="mission-section-lead">Follow these steps in order. Unplug USB before you change any wires.</p>
  {illustration_block(wiring.get("illustration_alt", "Wiring diagram"), "Wiring Diagram", "WIRE", wiring.get("image", ""))}
  {wiring_steps_html(wiring_steps)}
</section>"""
    gpio_html = gpio_table_section(m.get("gpio_table", []))

    code = m.get("code") or {}
    output = m.get("expected_output", "").strip()
    code_html = code_section(code, output)
    code_explanation_html = mission_list_section("code-explanation", "CODE", "Line-by-Line Code Explanation", m.get("code_explanation", []))

    output_html = ""
    if output:
        output_html = f"""<section class="mission-section mission-output" id="output" aria-labelledby="output-heading">
  {section_heading("output", "OUT", "Expected Serial Monitor Output")}
  <div class="mission-output-body">{_rich_content(output)}</div>
</section>"""
    experiment_html = mission_prose_section("experiment", "EXP", "Experiment: Leave the Input Floating", m.get("experiment", ""))

    quiz_html = quiz_block(m.get("quiz", []))
    challenge_html = challenge_section(
        m.get("challenge", "").strip(),
        m.get("challenge_items", []),
    )
    common_problems_html = common_problems_section(m.get("common_problems", []))
    faq_html = mission_faq_section(guide.get("faqs", []))

    complete = m.get("complete") or {}
    complete_summary = (complete.get("summary") or "").strip()
    complete_subtitle = (complete.get("subtitle") or "").strip()
    skills = complete.get("skills", [])
    skills_html = "".join(f"<li>{esc(s)}</li>" for s in skills)
    subtitle_html = (
        f'<p class="mission-complete-subtitle">{esc(complete_subtitle)}</p>'
        if complete_subtitle
        else ""
    )
    complete_html = f"""<section class="mission-section mission-complete" id="complete" aria-labelledby="complete-heading">
  <div class="mission-complete-panel">
    <span class="mission-complete-badge" aria-hidden="true">DONE</span>
    <h2 id="complete-heading">Mission Complete!</h2>
    {subtitle_html}
    <div class="mission-complete-body">{_rich_content(complete_summary)}</div>
    {"<ul class='mission-skills'>" + skills_html + "</ul>" if skills_html else ""}
  </div>
</section>"""

    next_html = next_mission_cards(m.get("next_missions", []))
    unlocks_html = academy_unlocks_section(guide)

    return f"""<article class="mission-journey">
{intro_html}
{academy_html}
{objectives_html}
{build_html}
{things_html}
{safety_html}
{components_html}
{concept_html}
{engineering_html}
{analogy_html}
{floating_recap_html}
{internal_resistor_html}
{external_resistor_html}
{comparison_html}
{wiring_html}
{gpio_html}
{code_html}
{code_explanation_html}
{output_html}
{experiment_html}
{quiz_html}
{challenge_html}
{common_problems_html}
{faq_html}
{complete_html}
{unlocks_html}
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


def _rich_content(text: str) -> str:
    if not text:
        return ""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    html_parts = []
    for block in blocks:
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if lines and all(ln.startswith("- ") for ln in lines):
            items = "".join(f"<li>{esc(ln[2:])}</li>" for ln in lines)
            html_parts.append(f'<ul class="mission-bullets">{items}</ul>')
        else:
            html_parts.append(f"<p>{esc(block)}</p>")
    return "".join(html_parts)
