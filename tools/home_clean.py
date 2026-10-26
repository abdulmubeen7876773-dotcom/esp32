"""Opt-in Clean Premium homepage; production controls and catalogs stay shared."""
from html import escape as esc
from learning_journey import journey_catalog
from home_cinematic import ICONS
from site_layout import home_learning_adventure


def clean_home(home, guides, projects, components, counts):
    config = home['clean_premium']
    guide_slugs = {g['slug'] for g in guides}
    project_map = {p['slug']: p for p in projects}
    route = journey_catalog()['beginner_route']
    steps, notes, cards = [], [], []
    for n, step in enumerate(route['steps']):
        assert step['slug'] in guide_slugs
        icon = ICONS[n]
        if n == 1:
            icon = icon.replace('#f0ae36', '#e34d36').replace('#95621f', '#a52e22')
        steps.append(f'''<li><a href="/guides/{esc(step['slug'])}.html"><span class="cp-number">{n+1}</span><span class="cp-step-icon">{icon}</span><h3>{esc(step['label'])}</h3><p>{esc(config['route_captions'][n])}</p></a></li>''')
        notes.append(f'''<li><strong>{esc(step['label'])}</strong><p>{esc(step['learn'])}</p><p><strong>Parts:</strong> {esc(step['parts'])}</p><p><strong>Before you start:</strong> {esc(step['ready'])}</p></li>''')
    for item in config['projects']:
        assert item['slug'] in project_map
        cards.append(f'''<a class="cp-project-card" href="/projects/{esc(item['slug'])}.html"><img src="{esc(item['image'])}" alt="{esc(item['alt'])}" width="1408" height="792" loading="lazy" decoding="async"><div><h3>{esc(item['label'])}</h3><p>{esc(item['description'])}</p><span class="cp-arrow" aria-hidden="true">→</span></div></a>''')
    return f'''<div class="cp-content" id="home-content">
<a class="cp-skip" href="#start-here-heading">Skip to beginner journey</a>
<section class="cp-hero" aria-labelledby="cp-title"><div class="cp-shell cp-hero-grid"><div class="cp-hero-copy"><p class="cp-eyebrow">{esc(home['hero_eyebrow'])}</p><h1 id="cp-title">{esc(home['hero_title'])}<br>{esc(home['hero_accent'])}</h1><p class="cp-lead">{esc(home['hero_sub'])}</p><div class="cp-actions"><a class="cp-primary" href="/guides/installing-arduino-ide-esp32.html">Start building <span aria-hidden="true">→</span></a><a class="cp-secondary" href="/projects.html">Browse projects</a></div></div><div class="cp-hero-visual"><img src="{esc(config['hero_image'])}" alt="{esc(config['hero_alt'])}" width="1672" height="941" fetchpriority="high" decoding="async"><p>Illustrative hardware · follow the tutorial for wiring</p></div></div></section>
<section class="cp-journey" id="start-here" aria-labelledby="start-here-heading"><div class="cp-shell"><p class="cp-eyebrow">Get started</p><h2 id="start-here-heading" tabindex="-1">Your ESP32 beginner journey</h2><p class="cp-intro">Follow these five steps, from first upload to your first display.</p><ol class="cp-steps">{''.join(steps)}</ol><details class="cp-details"><summary>Parts, prerequisites and what you will learn</summary><p>{esc(route['intro'])}</p><ol>{''.join(notes)}</ol><p>New to the board? Read <a href="/guides/what-is-esp32.html">What is ESP32?</a>. For an ordered path, explore <a href="/learning.html#esp32-basics">ESP32 basics</a>.</p></details></div></section>
<section class="cp-projects cp-shell" aria-labelledby="cp-project-title"><div class="cp-section-top"><div><p class="cp-eyebrow">Featured projects</p><h2 id="cp-project-title">Build something amazing</h2><p class="cp-intro">Put your new skills to work with a useful next build.</p></div><a class="cp-text-link" href="/projects.html">View all projects <span aria-hidden="true">→</span></a></div><div class="cp-project-grid">{''.join(cards)}</div><p class="cp-image-note">Generated project visuals are illustrative, not wiring instructions or evidence of tested builds.</p></section>
<section class="cp-promos cp-shell" aria-label="Keep exploring"><a class="cp-promo cp-hardware" href="/components.html"><div><span class="cp-promo-icon" aria-hidden="true">▦</span><h2>Find your next component</h2><p>Understand boards, sensors, displays and their power requirements.</p><span class="cp-text-link">Explore components →</span></div><svg viewBox="0 0 150 130" aria-hidden="true"><rect x="31" y="10" width="66" height="108" rx="7" fill="#17634e"/><rect x="42" y="20" width="44" height="35" fill="#c9d9ce"/><rect x="50" y="70" width="28" height="28" fill="#102e26"/><path d="M24 25h-8m8 15h-8m8 15h-8m8 15h-8m8 15h-8m88-60h8m-8 15h8m-8 15h8m-8 15h8m-8 15h8" stroke="#9eaf9d" stroke-width="6"/></svg></a><a class="cp-promo cp-learning" href="/learning.html"><div><span class="cp-promo-icon" aria-hidden="true">↗</span><h2>Explore learning paths</h2><p>Build your skills with ordered lessons and clear prerequisites.</p><span class="cp-text-link">Choose your path →</span></div><div class="cp-books" aria-hidden="true"><span>Basics</span><span>Sensors</span><span>Displays</span><span>Wi-Fi &amp; IoT</span></div></a></section>
<section class="cp-shell cp-further" aria-label="More ways to learn"><details class="cp-details cp-finder"><summary>Need a suggestion? Open the project finder</summary>{home_learning_adventure(projects)}</details><p>Already comfortable with the basics? <a href="/projects.html?difficulty=Advanced#grid">Explore advanced projects</a>.</p><div class="cp-support"><a href="/parents.html">For parents</a><a href="/teachers.html">For teachers</a><a href="/guides.html">All guides</a></div></section>
</div>'''
