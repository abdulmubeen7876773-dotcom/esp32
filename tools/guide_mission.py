from site_layout import badge_class, esc, site_href


def illustration_placeholder(alt: str, label: str = "Illustration") -> str:
    return f"""<figure class="mission-illustration" aria-label="{esc(alt)}">
  <div class="mission-illustration-frame">
    <span class="mission-illustration-icon" aria-hidden="true">🎨</span>
    <span class="mission-illustration-label">{esc(label)}</span>
    <span class="mission-illustration-alt">{esc(alt)}</span>
  </div>
</figure>"""


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
            rows.append(f"<li>{esc(item)}</li>")
            continue
        name = item.get("item") or item.get("name", "")
        note = item.get("note", "")
        link = item.get("link", "")
        note_html = f' <span class="meta">— {esc(note)}</span>' if note else ""
        if link:
            rows.append(f'<li><a href="{esc(link)}">{esc(name)}</a>{note_html}</li>')
        else:
            rows.append(f"<li>{esc(name)}{note_html}</li>")
    return f'<ul class="mission-things-list">{"".join(rows)}</ul>'


def safety_block(items: list) -> str:
    if not items:
        return ""
    lines = []
    for item in items:
        text = item if isinstance(item, str) else item.get("text", "")
        lines.append(f"<li>{esc(text)}</li>")
    return f"""<aside class="mission-safety" aria-label="Safety first">
  <div class="mission-safety-head"><span aria-hidden="true">⚠️</span><strong>Safety First</strong></div>
  <ul>{"".join(lines)}</ul>
</aside>"""


def code_panel(code: dict) -> str:
    filename = code.get("filename", "sketch.ino")
    content = (code.get("content") or "").strip("\n")
    return f"""<div class="code-panel">
  <div class="code-panel-head">
    <span class="code-panel-filename">{esc(filename)}</span>
    <button type="button" class="btn-copy" data-copy aria-label="Copy code">Copy</button>
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
        opts_html = "".join(
            f'<button type="button" class="quiz-option" data-index="{j}" data-correct="{1 if j == correct else 0}">{esc(opt)}</button>'
            for j, opt in enumerate(options)
        )
        blocks.append(
            f"""<div class="quiz-question" data-quiz-q="{i}" data-explanation="{esc(explanation)}">
  <p class="quiz-q-text"><span class="quiz-q-num">Q{i + 1}.</span> {esc(q.get("question", ""))}</p>
  <div class="quiz-options" role="group">{opts_html}</div>
  <p class="quiz-feedback" hidden></p>
</div>"""
        )
    return f"""<section class="mission-section mission-quiz" id="quiz" aria-labelledby="quiz-heading">
  <h2 id="quiz-heading">Mini Quiz</h2>
  <p class="mission-section-lead">Quick check — no grades, just confidence!</p>
  <div class="mission-quiz-list">{"".join(blocks)}</div>
</section>"""


def next_mission_cards(missions: list) -> str:
    if not missions:
        return ""
    cards = []
    for m in missions:
        slug = m.get("slug", "")
        href = site_href(f"guides/{slug}.html") if slug else site_href("guides.html")
        cards.append(
            f"""<a class="next-mission-card" href="{esc(href)}">
  <span class="next-mission-label">Next Mission</span>
  <h3>{esc(m.get("title", ""))}</h3>
  <p>{esc(m.get("description", ""))}</p>
  <span class="btn btn-card">Start Mission<span aria-hidden="true">→</span></span>
</a>"""
        )
    return f"""<section class="mission-section mission-next" id="next-mission" aria-labelledby="next-heading">
  <h2 id="next-heading">Continue Your Journey</h2>
  <div class="next-mission-grid">{"".join(cards)}</div>
</section>"""


def mission_card_html(guide: dict) -> str:
    m = guide.get("mission") or {}
    icon = m.get("icon", "🚀")
    title = m.get("title", "")
    label = mission_number_label(guide)
    return f"""<div class="mission-card">
  <span class="mission-card-icon" aria-hidden="true">{esc(icon)}</span>
  <span class="mission-card-badge">{esc(label)}</span>
  <h2 class="mission-card-title">{esc(title)}</h2>
  {mission_meta_badges_html(guide, compact=True)}
</div>"""


def reference_intro_card(guide: dict) -> str:
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip()
    return f"""<div class="reference-intro-card">
  <span class="reference-intro-label">Reference Guide</span>
  <h2 class="reference-intro-title">{esc(headline)}</h2>
</div>"""


def render_friendly_intro(guide: dict, *, is_mission: bool) -> str:
    m = guide.get("mission") or {}
    intro = guide.get("intro") or {}

    if is_mission:
        header = mission_card_html(guide)
        story = (m.get("story") or "").strip()
        eli12 = (m.get("eli12") or "").strip()
        safety = m.get("safety", [])
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

    story_html = ""
    if story:
        story_html = f"""<section class="mission-section guide-intro-story" id="story" aria-labelledby="story-heading">
  <h2 id="story-heading">The Story</h2>
  <div class="mission-story">{_paragraphs(story)}</div>
</section>"""

    eli12_html = ""
    if eli12:
        eli12_html = f"""<section class="mission-section" id="eli12" aria-labelledby="eli12-heading">
  <div class="eli12-box mission-eli12">
    <h2 id="eli12-heading">Explain Like I'm 12</h2>
    {_paragraphs(eli12)}
  </div>
</section>"""

    safety_html = safety_block(safety)

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
  <h2 id="build-heading">What You'll Build</h2>
  {_paragraphs(build)}
</section>"""

    things = m.get("things_you_need", [])
    things_html = ""
    if things:
        things_html = f"""<section class="mission-section" id="parts" aria-labelledby="parts-heading">
  <h2 id="parts-heading">Things You'll Need</h2>
  {things_list(things)}
</section>"""

    concept = m.get("concept") or {}
    concept_body = (concept.get("body") or "").strip()
    concept_html = ""
    if concept_body or concept.get("illustration_alt"):
        concept_html = f"""<section class="mission-section" id="concept" aria-labelledby="concept-heading">
  <h2 id="concept-heading">{esc(concept.get("title", "The Concept"))}</h2>
  {illustration_placeholder(concept.get("illustration_alt", "Concept diagram"), "Concept Illustration")}
  {_paragraphs(concept_body)}
</section>"""

    wiring = m.get("wiring") or {}
    wiring_steps = wiring.get("steps", [])
    wiring_html = ""
    if wiring_steps or wiring.get("illustration_alt"):
        steps = "".join(f"<li>{esc(s)}</li>" for s in wiring_steps)
        wiring_html = f"""<section class="mission-section" id="wiring" aria-labelledby="wiring-heading">
  <h2 id="wiring-heading">Wiring</h2>
  {illustration_placeholder(wiring.get("illustration_alt", "Wiring diagram"), "Wiring Diagram")}
  <ol class="mission-steps">{steps}</ol>
</section>"""

    code = m.get("code") or {}
    code_html = ""
    if code.get("content"):
        code_html = f"""<section class="mission-section" id="code" aria-labelledby="code-heading">
  <h2 id="code-heading">Code</h2>
  <p class="mission-section-lead">Copy this into Arduino IDE, then click Upload.</p>
  {code_panel(code)}
</section>"""

    output = m.get("expected_output", "").strip()
    output_html = ""
    if output:
        output_html = f"""<section class="mission-section mission-output" id="output" aria-labelledby="output-heading">
  <h2 id="output-heading">Expected Output</h2>
  {_paragraphs(output)}
</section>"""

    quiz_html = quiz_block(m.get("quiz", []))

    challenge = m.get("challenge", "").strip()
    challenge_html = ""
    if challenge:
        challenge_html = f"""<section class="mission-section mission-challenge" id="challenge" aria-labelledby="challenge-heading">
  <h2 id="challenge-heading">Challenge Yourself</h2>
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
    {_paragraphs(complete_summary)}
    {"<ul class='mission-skills'>" + skills_html + "</ul>" if skills_html else ""}
  </div>
</section>"""

    next_html = next_mission_cards(m.get("next_missions", []))

    return f"""<article class="mission-journey">
{intro_html}
{build_html}
{things_html}
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
