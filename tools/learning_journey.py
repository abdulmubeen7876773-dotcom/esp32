"""One catalog-defined beginner order; no completion tracking or inferred durations."""
from html import escape
from cms_loader import CONTENT, load_yaml


def journey_catalog():
    return load_yaml(CONTENT / "learning-paths.yaml")


def beginner_route_html(guides, section_id="start-here"):
    route = journey_catalog()["beginner_route"]
    by_slug = {g["slug"]: g for g in guides}
    cards = []
    for number, step in enumerate(route["steps"], 1):
        guide = by_slug[step["slug"]]
        # Existing reading estimates are labeled as reading, not promised completion times.
        reading = guide.get("reading_time", "")
        if reading and "read" not in reading.lower():
            reading = "Reading estimate: " + reading
        meta = guide.get("proficiency_level", "")
        if reading:
            meta += " · " + reading
        cards.append(f'<li class="beginner-step"><p class="meta">Step {number} · {escape(meta)}</p><h3><a href="/guides/{escape(step["slug"])}.html">{escape(step["label"])}</a></h3><p>{escape(step["learn"])}</p><p><strong>Parts:</strong> {escape(step["parts"])}</p><p><strong>Before you start:</strong> {escape(step["ready"])}</p></li>')
    return f'<section class="beginner-route" id="{section_id}" aria-labelledby="{section_id}-heading"><h2 id="{section_id}-heading">{escape(route["title"])}</h2><p>{escape(route["intro"])}</p><ol class="beginner-route-grid">{"".join(cards)}</ol><p>Need background first? Read <a href="/guides/what-is-esp32.html">What is ESP32?</a> and the <a href="/components/esp32-devkit.html">DevKit board guide</a>. After these five steps, choose a <a href="/learning.html#sensor-basics">sensor path</a> or <a href="/learning.html#display-basics">display path</a>.</p></section>'


def beginner_navigation(slug):
    steps = journey_catalog()["beginner_route"]["steps"]
    position = next((i for i, step in enumerate(steps) if step["slug"] == slug), None)
    if position is None:
        return ""
    links = ['<a href="/learning.html#esp32-basics">See all five steps</a>']
    if position:
        previous = steps[position - 1]
        links.append(f'<a href="/guides/{previous["slug"]}.html">Previous: {escape(previous["label"])}</a>')
    if position + 1 < len(steps):
        following = steps[position + 1]
        links.append(f'<a class="beginner-next" href="/guides/{following["slug"]}.html">Next: {escape(following["label"])}</a>')
    else:
        links.append('<a class="beginner-next" href="/learning.html#display-basics">Next: practise display skills</a>')
    return f'<nav class="beginner-navigation" aria-label="Beginner route"><p><strong>Beginner route · Step {position + 1} of {len(steps)}: {escape(steps[position]["label"])}</strong></p><div>{"".join(links)}</div></nav>\n'


def beginner_continue(slug):
    steps = journey_catalog()["beginner_route"]["steps"]
    position = next((i for i, step in enumerate(steps) if step["slug"] == slug), None)
    if position is None:
        return ""
    if position + 1 < len(steps):
        step = steps[position + 1]
        href, label = f'/guides/{step["slug"]}.html', step["label"]
    else:
        href, label = "/learning.html#display-basics", "practise display skills"
    return f'<p class="beginner-continue"><a href="{href}">Continue beginner route: {escape(label)}</a></p>\n'
