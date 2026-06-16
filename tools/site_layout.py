import html
import json
import re

from project_icons import pick_icon, thumb_class, featured_cat_bar

CSS_VERSION = "20260617-parent1"
SITE_DOMAIN = "https://abdulmubeen7876773-dotcom.github.io/esp32"
SITE_NAME = "ESP32 Project Library"
ORG_NAME = "ESP32 Project Library"
GITHUB_URL = "https://github.com/abdulmubeen7876773-dotcom/esp32"
CONTACT_ISSUES_URL = "https://github.com/abdulmubeen7876773-dotcom/esp32/issues"
GA4_MEASUREMENT_ID = "G-WLHZKSEFP3"
GSC_VERIFICATION = "Els4sebtkOekRXaW0BMxMlzn9iBdaqDHmuUCmMvfkCI"
OG_IMAGE = f"{SITE_DOMAIN}/og-image.svg"

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
    c = re.sub(r"\s+", " ", (cat or "ESP32").strip())
    while re.search(r"\bProjects\s+Projects\b", c, re.I):
        c = re.sub(r"\bProjects\s+Projects\b", "Projects", c, flags=re.I)
    if c.lower().endswith(" projects"):
        return c
    return f"{c} Projects"


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
    feat_badge = '<span class="badge badge-featured">Featured</span>' if p.get("featured") else ""
    return f"""<a class="{card_class} modern-card" href="{esc(link)}"{extra_attrs}>{card_thumb_html(cat, thumb_cls)}<div class="card-body"><div class="card-badges">{feat_badge}<span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge {badge_class(diff)}">{esc(diff.replace(' build',''))}</span><span class="badge badge-time">{esc(rt)}</span></div><h3>{esc(p['title'])}</h3>{desc_html}<div class="card-footer"><span class="card-read-more">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


def canonical_url(base: str, path: str) -> str:
    p = (path or "index.html").lstrip("/")
    if base.startswith("http"):
        root = base.rstrip("/")
    else:
        root = SITE_DOMAIN.rstrip("/") + ("/" + base.strip("/") if base.strip("/") else "")
    return f"{root}/{p}" if p else root + "/"


def json_ld_script(data) -> str:
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'


def organization_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ORG_NAME,
        "url": SITE_DOMAIN + "/",
        "logo": OG_IMAGE,
        "sameAs": [GITHUB_URL],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer support",
            "url": CONTACT_ISSUES_URL,
        },
    }
    return json_ld_script(data)


def website_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_DOMAIN + "/",
        "publisher": {"@type": "Organization", "name": ORG_NAME},
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_DOMAIN}/projects.html?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    return json_ld_script(data)


def social_meta(title: str, description: str, url: str, og_type: str = "website") -> str:
    t = esc(title)
    d = esc(description)
    u = esc(url)
    img = esc(OG_IMAGE)
    return f"""<meta property="og:type" content="{esc(og_type)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">"""


def analytics_config_script() -> str:
    ga = esc(GA4_MEASUREMENT_ID)
    return f'<script>window.SITE_GA4="{ga}";</script>'


def gsc_verification_meta() -> str:
    if not GSC_VERIFICATION:
        return ""
    return f'<meta name="google-site-verification" content="{esc(GSC_VERIFICATION)}">'


def head_html(
    base: str,
    title: str,
    description: str,
    canonical_path: str = "",
    og_type: str = "website",
    extra_schema: str = "",
    include_gsc: bool = False,
) -> str:
    t = esc(title)
    d = esc(description)
    canon = canonical_url(base, canonical_path or "index.html")
    favicon = f"{base}favicon.svg"
    gsc = gsc_verification_meta() if include_gsc else ""
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#020617">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{esc(canon)}">
<link rel="icon" href="{favicon}" type="image/svg+xml">
{social_meta(title, description, canon, og_type)}
{gsc}
<script>document.documentElement.classList.add("js")</script>
{analytics_config_script()}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css?v={CSS_VERSION}">
{extra_schema}"""


def header_html(active: str = "home", base: str = ""):
    nav_home = ' class="active"' if active == "home" else ""
    nav_proj = ' class="active"' if active == "projects" else ""
    nav_about = ' class="active"' if active == "about" else ""
    nav_contact = ' class="active"' if active == "contact" else ""
    search_action = (
        "event.preventDefault();location.href='projects.html?q='+encodeURIComponent(this.querySelector('input').value);"
        if active == "home"
        else "event.preventDefault();var el=document.getElementById('q');if(el){el.value=this.querySelector('input').value;if(window.filterProjects){window.filterProjects();}else{el.dispatchEvent(new Event('input'));el.dispatchEvent(new Event('change'));}}"
    )
    return f"""<div class="site-nav-sticky">
<header class="site-header"><div class="wrap header-inner"><a class="site-logo" href="{base}index.html"><span class="logo-mark" aria-hidden="true"></span>ESP32<span class="logo-accent">Library</span></a><button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button><nav class="top-nav" aria-label="Main"><a href="{base}index.html"{nav_home}>Home</a><a href="{base}projects.html"{nav_proj}>Projects</a><a href="{base}about.html"{nav_about}>About</a><a href="{base}contact.html"{nav_contact}>Contact</a></nav><form class="top-search" onsubmit="{search_action}"><input type="search" placeholder="Search projects…" aria-label="Search"><button type="submit" aria-label="Search">Search</button></form></div></header>
{featured_cat_bar(base, active == "home", active == "projects")}
</div>"""


def static_page_shell(active: str, title: str, description: str, body: str, canonical_path: str, schema: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, description, canonical_path=canonical_path, extra_schema=schema)}
</head>
<body>
<main>
{header_html(active)}
<section class="section-block wrap page-head static-page">
{body}
</section>
</main>
{footer_html()}
<script src="ui.js" defer></script>
</body>
</html>
"""


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
      <p class="hero-sub">Explore 15 ESP32 parent projects — each with Beginner, Intermediate, and Advanced build paths for IoT, automation, robotics, sensors, and edge AI.</p>
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
    return """<section class="stats-bar wrap reveal" aria-label="Site statistics"><div class="stats-grid"><div class="stat-item"><strong>15</strong><span>Parent Projects</span></div><div class="stat-item"><strong>45</strong><span>Build Stages</span></div><div class="stat-item"><strong>15</strong><span>Categories</span></div><div class="stat-item"><strong>Open Source</strong><span>Examples</span></div></div></section>"""


def footer_html(base: str = "") -> str:
    return f"""<footer class="site-footer"><div class="wrap footer-grid footer-grid-wide"><div class="footer-brand"><strong>ESP32 Project Library</strong><p>15 parent ESP32 tutorials with Beginner, Intermediate, and Advanced stages — wiring tables, Arduino code, and troubleshooting for makers and students.</p></div><div class="footer-col"><h4>Explore</h4><a href="{base}index.html">Home</a><a href="{base}projects.html">All Projects</a><a href="{base}sitemap.html">Sitemap</a></div><div class="footer-col"><h4>Company</h4><a href="{base}about.html">About</a><a href="{base}contact.html">Contact</a></div><div class="footer-col"><h4>Legal</h4><a href="{base}privacy.html">Privacy Policy</a><a href="{base}disclaimer.html">Disclaimer</a></div></div><div class="wrap footer-bottom"><p>© 2026 ESP32 Project Library. All rights reserved.</p></div></footer>"""


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
