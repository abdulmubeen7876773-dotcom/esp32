"""Opt-in Cinematic Maker presentation, using production catalogs and controls."""
from html import escape as esc
from cms_loader import load_home_recommendations
from learning_journey import journey_catalog
from project_text import project_title, card_description
from site_layout import (_home_discovery_project_rows, home_learning_adventure,
                         home_v3_top_picks, home_discovery_links)

ICONS = ['<svg viewBox="0 0 120 105" aria-hidden="true"><rect x="20" y="15" width="80" height="58" rx="4" class="cm-device"/><path d="M10 84h100l-10-11H20z" class="cm-metal"/><path d="m46 37-10 7 10 7m28-14 10 7-10 7m-11-18-6 24" class="cm-accent-stroke"/></svg>', '<svg viewBox="0 0 120 105" aria-hidden="true"><path d="M49 62v35m22-35v27" class="cm-wire"/><path d="M40 63V39a20 20 0 0 1 40 0v24z" fill="#f0ae36" stroke="#95621f" stroke-width="2"/><path d="M39 64h42" class="cm-wire"/><path d="M49 39q0-13 10-14" stroke="#fff7da" stroke-width="4" fill="none"/><path d="M60 7V1m-30 20-8-7m68 7 8-7" class="cm-accent-stroke"/></svg>', '<svg viewBox="0 0 120 105" aria-hidden="true"><path d="M27 56v32m66-32v32M27 37V24m66 13V24" class="cm-wire"/><rect x="27" y="31" width="66" height="44" rx="5" class="cm-metal"/><circle cx="60" cy="50" r="18" class="cm-device"/><circle cx="60" cy="47" r="11" fill="#505c61"/></svg>', '<svg viewBox="0 0 120 105" aria-hidden="true"><path d="M40 20a10 10 0 0 1 20 0v42a19 19 0 1 1-20 0z" class="cm-metal"/><path d="M50 35v41" class="cm-accent-stroke"/><circle cx="50" cy="79" r="9" fill="#217c9f"/><path d="M86 35q-24 30 0 30t0-30" fill="#217c9f"/></svg>', '<svg viewBox="0 0 120 105" aria-hidden="true"><rect x="17" y="19" width="86" height="67" rx="4" fill="#245570"/><rect x="25" y="28" width="70" height="49" rx="2" class="cm-device"/><path d="m32 65 18-20 13 13 9-10 17 17" stroke="#edf9ff" stroke-width="3" fill="none"/><circle cx="79" cy="39" r="4" fill="#edf9ff"/></svg>']


def cinematic_home(home, guides, projects, components, counts):
    config = home["cinematic"]
    project_map = {p["slug"]: p for p in projects}
    component_map = {c["slug"]: c for c in components}
    def story(item, large=False):
        catalog = project_map if item["kind"] == "projects" else component_map
        record = catalog[item["slug"]]
        title = project_title(record) if item["kind"] == "projects" else record["name"]
        description = card_description(record, 150) if item["kind"] == "projects" else record["summary"]
        if not large and len(description) > 110:
            description = description[:107].rsplit(" ", 1)[0] + "…"
        href = f'/{item["kind"]}/{record["slug"]}.html'
        image = f'<img src="{esc(item["image"])}" alt="{esc(item["alt"])}" width="{item["width"]}" height="{item["height"]}" loading="lazy" decoding="async">'
        if large:
            return f'<a class="cm-feature-story" href="{href}" aria-label="{esc(title)}">{image}<div><span class="cm-eyebrow">{esc(item["eyebrow"])}</span><h3>{esc(item["label"])}</h3><p>{esc(description)}</p><span class="cm-story-arrow" aria-hidden="true">↗</span></div></a>'
        return f'<a href="{href}" aria-label="{esc(title)}">{image}<h3>{esc(item["label"])} <span aria-hidden="true">↗</span></h3><p>{esc(description)}</p></a>'

    route = journey_catalog()["beginner_route"]
    guide_map = {g["slug"]: g for g in guides}
    steps, notes = [], []
    for n, step in enumerate(route["steps"]):
        assert step["slug"] in guide_map
        steps.append(f'<li><a href="/guides/{esc(step["slug"])}.html"><span class="cm-step-number">{n+1:02}</span><strong>{esc(step["label"])}</strong>{ICONS[n]}<span class="cm-step-caption">{esc(config["route_captions"][step["slug"]])}</span></a></li>')
        notes.append(f'<li><strong>{esc(step["label"])}</strong><p>{esc(step["learn"])}</p><p><strong>Parts:</strong> {esc(step["parts"])}</p><p><strong>Before you start:</strong> {esc(step["ready"])}</p></li>')

    shown = {item["slug"] for item in [config["feature"], *config["stories"]] if item["kind"] == "projects"}
    discovery = []
    for block in load_home_recommendations()["project_discovery"]:
        slugs = [s for s in block["slugs"] if s not in shown]
        identifier = "cm-" + block["id"]
        discovery.append(f'<section class="home-discovery-block" id="{identifier}" aria-labelledby="{identifier}-heading"><div class="home-discovery-head"><h3 id="{identifier}-heading">{esc(block["title"])}</h3><p>{esc(block["description"])}</p></div><div class="home-discovery-list">{_home_discovery_project_rows(projects,slugs)}</div></section>')
    parts = []
    for item in config["parts"]:
        record = component_map[item["slug"]]
        parts.append(f'<a href="/components/{esc(record["slug"])}.html"><span class="cm-part-symbol" aria-hidden="true">{esc(item["symbol"])}</span><strong>{esc(item["label"])}</strong><span>{esc(item["caption"])}</span></a>')
    return f'''<div class="cm-content" id="home-content">
<a class="cm-skip" href="#start-here">Skip to beginner route</a>
<section class="cm-hero" aria-labelledby="cm-hero-title"><img class="cm-hero-photo" src="{esc(config["hero_image"])}" alt="{esc(config["hero_alt"])}" width="1983" height="793" fetchpriority="high" decoding="async"><div class="cm-hero-shade"></div><div class="cm-container cm-hero-copy"><p class="cm-eyebrow">{esc(home["hero_eyebrow"])}</p><h1 id="cm-hero-title">{esc(home["hero_title"])}<br> <span>{esc(home["hero_accent"])}</span></h1><p class="cm-hero-description">{esc(home["hero_sub"])}</p><div class="cm-hero-actions"><a class="cm-primary" href="/guides/installing-arduino-ide-esp32.html">{esc(home["hero_action"])} <span aria-hidden="true">→</span></a><a class="cm-text-link" href="/projects.html">Explore projects ↗</a></div></div></section>
<section class="cm-journey cm-container" id="start-here" aria-labelledby="start-here-heading"><p class="cm-eyebrow">Get started</p><h2 id="start-here-heading">From first upload to first display.</h2><p class="cm-intro">Five connected steps. Start with a USB upload, then build one skill at a time.</p><ol class="cm-journey-line">{"".join(steps)}</ol><a class="cm-section-link" href="/learning.html#esp32-basics">Follow the beginner route ↗</a><details class="cm-route-notes"><summary>Parts, prerequisites and what you will learn</summary><p>{esc(route["intro"])}</p><ol>{"".join(notes)}</ol><p>Need background? Read <a href="/guides/what-is-esp32.html">What is ESP32?</a> and the <a href="/components/esp32-devkit.html">DevKit guide</a>.</p><p>After these five steps, choose a <a href="/learning.html#sensor-basics">sensor path</a> or a <a href="/learning.html#display-basics">display path</a>.</p></details></section>
<section class="cm-projects cm-container" id="featured-projects" aria-labelledby="cm-projects-title"><div class="cm-section-top"><div><p class="cm-eyebrow">Featured projects</p><h2 id="cm-projects-title">A small board. A useful build.</h2></div><a class="cm-section-link" href="/projects.html">More projects ↗</a></div><div class="cm-project-editorial">{story(config["feature"],True)}<div class="cm-side-stories">{"".join(story(item) for item in config["stories"])}</div></div><p class="cm-image-note">Illustrative visuals, not wiring diagrams or hardware-test evidence. Use each tutorial’s connection instructions.</p></section>
<section class="cm-connections" aria-labelledby="cm-connections-title"><div class="cm-container cm-connection-inner"><div><p class="cm-eyebrow">Know your hardware</p><h2 id="cm-connections-title">Understand<br>every connection.</h2><p>Explore the board, parts and power requirements before you wire a circuit.</p><a class="cm-section-link" href="/components.html">Explore components ↗</a></div><div class="cm-parts-line" aria-label="Example learning topics">{"".join(parts)}</div></div></section>
<div class="cm-container cm-more"><details class="cm-disclosure" id="advanced-projects"><summary>More beginner, intermediate and advanced builds</summary><div class="home-project-discovery-grid">{"".join(discovery)}</div></details><details class="cm-disclosure"><summary>Help me choose: project finder</summary>{home_learning_adventure(projects)}</details><details class="cm-disclosure"><summary>Guides and component references</summary>{home_v3_top_picks(projects,guides,components,include_projects=False)}</details><div class="cm-support"><a href="/parents.html">For parents: supervision and learning at home ↗</a><a href="/teachers.html">For teachers: learning paths and classroom guidance ↗</a></div></div>
{home_discovery_links(counts)}
</div>'''
