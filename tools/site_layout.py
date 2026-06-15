import html
import re

from project_icons import pick_icon, thumb_class

CSS_VERSION = "20260615-saas4"

HERO_BOARD_SVG = """<svg class="hero-board-svg" viewBox="0 0 200 200" fill="none" aria-hidden="true"><rect x="30" y="55" width="140" height="90" rx="12" stroke="url(#heroGrad)" stroke-width="2.5"/><rect x="48" y="72" width="104" height="56" rx="6" fill="rgba(56,189,248,.12)" stroke="rgba(56,189,248,.35)" stroke-width="1.5"/><path d="M30 75h-12M30 100h-12M30 125h-12M170 75h12M170 100h12M170 125h12M70 55V38M100 55V38M130 55V38M70 145V162M100 145V162M130 145V162" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity=".7"/><circle cx="100" cy="100" r="6" fill="#22d3ee" opacity=".9"/><text x="100" y="105" text-anchor="middle" fill="#f8fafc" font-size="14" font-weight="700" font-family="Space Grotesk,Inter,sans-serif">ESP32</text><defs><linearGradient id="heroGrad" x1="30" y1="55" x2="170" y2="145"><stop stop-color="#38bdf8"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs></svg>"""


def esc(t):
    return html.escape(t or "", quote=True)


def normalize_terms(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"\bIot\b", "IoT", text)
    text = re.sub(r"\biot\b", "IoT", text)
    return text


def category_section_title(cat: str) -> str:
    if cat.endswith(" Projects"):
        return cat
    return f"{cat} Projects"


def read_time_minutes(difficulty: str, slug: str = "") -> int:
    d = difficulty.replace(" build", "").strip().lower()
    base = {"beginner": 5, "intermediate": 8, "advanced": 12}.get(d, 6)
    if slug:
        base += sum(ord(c) for c in slug[-5:]) % 4
    return base


def read_time_label(difficulty: str, slug: str = "") -> str:
    return f"{read_time_minutes(difficulty, slug)} min read"


def badge_class(difficulty: str) -> str:
    d = difficulty.replace(" build", "").strip().lower()
    if d == "advanced":
        return "badge-advanced"
    if d == "intermediate":
        return "badge-intermediate"
    return "badge-beginner"


def short_category(cat: str) -> str:
    c = (cat or "ESP32").replace(" Projects", "")
    if c == "Home Automation":
        return "Smart Home"
    return c


def card_thumb_html(category: str, cls: str = "post-thumb") -> str:
    tc = thumb_class(category)
    return f'<div class="{cls} {tc}">{pick_icon(category)}</div>'


def modern_card(
    p: dict,
    card_class: str = "post-card",
    thumb_cls: str = "post-thumb",
    href: str | None = None,
    extra_attrs: str = "",
    show_desc: bool = False,
) -> str:
    link = href if href is not None else p["href"]
    cat = p.get("category", "ESP32")
    diff = p.get("difficulty", "Beginner")
    slug = p.get("slug", "")
    desc = p.get("desc", "")
    desc_html = ""
    if show_desc and desc:
        short = desc if len(desc) <= 100 else desc[:97].rstrip() + "…"
        desc_html = f'<p class="card-desc">{esc(short)}</p>'
    rt = read_time_label(diff, slug)
    return f"""<a class="{card_class} modern-card" href="{esc(link)}"{extra_attrs}>{card_thumb_html(cat, thumb_cls)}<div class="card-body"><div class="card-badges"><span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge {badge_class(diff)}">{esc(diff.replace(' build',''))}</span><span class="badge badge-time">{esc(rt)}</span></div><h3>{esc(p['title'])}</h3>{desc_html}<div class="card-footer"><span class="card-read-more">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


def head_html(base: str, title: str, description: str) -> str:
    t = esc(title)
    d = esc(description)
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#020617">
<script>document.documentElement.classList.add("js")</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css?v={CSS_VERSION}">"""


def hero_html(latest_items: str = "") -> str:
    latest_block = ""
    if latest_items:
        latest_block = f"""<aside class="hero-latest" aria-label="Latest projects"><h2>Latest Projects</h2>{latest_items}</aside>"""
    return f"""<section class="hero-premium" aria-labelledby="hero-heading">
  <div class="hero-glow hero-glow-a" aria-hidden="true"></div>
  <div class="hero-glow hero-glow-b" aria-hidden="true"></div>
  <div class="wrap hero-premium-grid">
    <div class="hero-content">
      <p class="hero-eyebrow">ESP32 Project Library</p>
      <h1 id="hero-heading">Build, Connect &amp; Automate with ESP32</h1>
      <p class="hero-sub">Explore 1,000+ hands-on ESP32 projects — IoT systems, smart home automation, robotics, sensors, and AI at the edge. Built for makers, students, engineers, and developers.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="projects.html">Browse Projects</a>
        <a class="btn btn-secondary" href="#categories">Explore Categories</a>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="hero-board-float">{HERO_BOARD_SVG}</div>
    </div>
    {latest_block}
  </div>
</section>"""


def stats_html() -> str:
    return """<section class="stats-bar wrap reveal" aria-label="Site statistics"><div class="stats-grid"><div class="stat-item"><strong>1000+</strong><span>Projects</span></div><div class="stat-item"><strong>50+</strong><span>Categories</span></div><div class="stat-item"><strong>Beginner → Advanced</strong><span>Skill Levels</span></div><div class="stat-item"><strong>Open Source</strong><span>Examples</span></div></div></section>"""


def footer_html(base: str = "") -> str:
    return f"""<footer class="site-footer"><div class="wrap footer-grid footer-grid-wide"><div class="footer-brand"><strong>ESP32 Project Library</strong><p>1,000+ ESP32 tutorials with wiring diagrams, source code, parts lists, and step-by-step build guides for makers, students, and engineers.</p></div><div class="footer-col"><h4>Explore</h4><a href="{base}index.html">Home</a><a href="{base}projects.html">All Projects</a><a href="{base}sitemap.xml">Sitemap</a></div><div class="footer-col"><h4>Company</h4><a href="{base}about.html">About</a><a href="{base}contact.html">Contact</a></div><div class="footer-col"><h4>Legal</h4><a href="{base}privacy.html">Privacy Policy</a><a href="{base}disclaimer.html">Disclaimer</a></div></div><div class="wrap footer-bottom"><p>© 2026 ESP32 Project Library. All rights reserved.</p></div></footer>"""


def related_cards_html(related: list, base: str = "") -> str:
    if not related:
        return f'<p class="meta"><a href="{base}projects.html">Browse all ESP32 projects →</a></p>'
    cards = []
    for r in related[:4]:
        cat = r.get("cat") or r.get("category") or "ESP32"
        href = r["href"]
        if base and not href.startswith("..") and not href.startswith("http"):
            href = base + href if not href.startswith(base) else href
        cards.append(
            f"""<a class="related-card" href="{esc(href)}">{card_thumb_html(cat, "related-thumb")}<div class="related-body"><span class="badge badge-cat">{esc(short_category(cat))}</span><h3>{esc(r['title'])}</h3></div></a>"""
        )
    return f'<div class="related-grid">{"".join(cards)}</div>'
