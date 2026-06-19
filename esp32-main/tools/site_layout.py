import html
import json
import re

from cms_loader import load_home, load_site_settings
from project_icons import pick_icon, thumb_class, featured_cat_bar

_cfg = load_site_settings()
CSS_VERSION = _cfg["css_version"]
SITE_DOMAIN = _cfg["site_domain"]
SITE_NAME = _cfg["site_name"]
ORG_NAME = _cfg["org_name"]
SITE_TAGLINE = _cfg.get("site_tagline", "Learn | Build | Innovate")
GITHUB_URL = _cfg["github_url"]
YOUTUBE_URL = _cfg.get("youtube_url", "https://www.youtube.com/@ESP32Engine")
CONTACT_ISSUES_URL = _cfg["contact_issues_url"]
GA4_MEASUREMENT_ID = _cfg["ga4_measurement_id"]
GSC_VERIFICATION = _cfg["gsc_verification"]
PINTEREST_VERIFICATION = _cfg["pinterest_verification"]
INDEXNOW_KEY = _cfg["indexnow_key"]
PROJECTS_PAGE_SIZE = int(_cfg["projects_page_size"])
OG_IMAGE = f"{SITE_DOMAIN}/og-image.jpg"
OG_IMAGE_WIDTH = int(_cfg.get("og_image_width", 1200))
OG_IMAGE_HEIGHT = int(_cfg.get("og_image_height", 630))

HERO_BOARD_SVG = """<svg class="hero-board-svg" viewBox="0 0 240 240" fill="none" aria-hidden="true"><defs><linearGradient id="heroGrad" x1="40" y1="60" x2="200" y2="180"><stop stop-color="#A855F7"/><stop offset="1" stop-color="#6D28D9"/></linearGradient><filter id="heroGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect x="40" y="62" width="160" height="104" rx="16" stroke="url(#heroGrad)" stroke-width="2.5" filter="url(#heroGlow)"/><rect x="62" y="84" width="116" height="60" rx="10" fill="rgba(109,40,217,.12)" stroke="rgba(109,40,217,.35)" stroke-width="1.5"/><path d="M40 86h-16M40 114h-16M40 142h-16M200 86h16M200 114h16M200 142h16M86 62V42M120 62V42M154 62V42M86 166V186M120 166V186M154 166V186" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" opacity=".55"/><circle cx="120" cy="114" r="8" fill="#6D28D9"/><circle cx="120" cy="114" r="16" stroke="#A855F7" stroke-width="1.2" opacity=".35"/><text x="120" y="119" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="Poppins,Inter,sans-serif">ESP32</text></svg>"""

SIDEBAR_CATEGORIES = [
    ("ESP32 Basics", "guides/what-is-esp32.html", "basics"),
    ("ESP32-CAM", "category/esp32-cam.html", "esp32-cam"),
    ("ESP32 Projects", "projects.html", "projects"),
    ("IoT Projects", "category/iot-projects.html", "iot-projects"),
    ("Home Automation", "category/home-automation.html", "home-automation"),
    ("Bluetooth Projects", "category/iot-projects.html", "bluetooth"),
    ("WiFi Projects", "category/iot-projects.html", "wifi"),
    ("Display Projects", "category/led-projects.html", "display"),
]

ICON_GITHUB = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>'
ICON_YOUTUBE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3" stroke-linecap="round"/></svg>'

HERO_FLOAT_CARDS = """<div class="hero-float-stack" aria-hidden="true">
<div class="hero-float-card hero-float-card-a"><span class="hero-float-label">GPIO Monitor</span><strong>34</strong><span class="hero-float-sub">Analog Input</span></div>
<div class="hero-float-card hero-float-card-b"><span class="hero-float-label">Wi-Fi Status</span><strong>Online</strong><span class="hero-float-sub">2.4 GHz Connected</span></div>
<div class="hero-float-card hero-float-card-c"><span class="hero-float-label">Relay Output</span><strong>ACTIVE</strong><span class="hero-float-sub">GPIO26 · Pump ON</span></div>
</div>"""


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
    return f"""<a class="{card_class} modern-card project-card-item" href="{esc(link)}"{extra_attrs}><div class="card-media">{card_thumb_html(cat, thumb_cls)}</div><div class="card-body"><div class="card-badges">{feat_badge}<span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge {badge_class(diff)}">{esc(diff.replace(' build',''))}</span><span class="badge badge-time">{esc(rt)}</span></div><h3>{esc(p['title'])}</h3>{desc_html}<div class="card-footer"><span class="btn btn-card">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


def site_href(path: str = "") -> str:
    p = (path or "").strip().lstrip("/")
    if not p or p == "index.html":
        return "/"
    return f"/{p}"


def canonical_url(path: str = "") -> str:
    p = (path or "").strip().lstrip("/")
    if not p or p == "index.html":
        return SITE_DOMAIN.rstrip("/") + "/"
    return f"{SITE_DOMAIN.rstrip('/')}/{p}"


def index_redirect_script() -> str:
    return '<script>if(/\\/index\\.html$/i.test(location.pathname))location.replace(location.pathname.replace(/index\\.html$/i,"")+(location.search||"")+(location.hash||"")||"/");</script>'


def json_ld_script(data) -> str:
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'


def breadcrumb_schema(items: list[tuple[str, str]]) -> str:
    elements = []
    for i, (name, url) in enumerate(items, 1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": url if url.startswith("http") else f"{SITE_DOMAIN.rstrip('/')}{site_href(url)}",
            }
        )
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }
    return json_ld_script(data)


def webpage_schema(title: str, description: str, path: str, page_type: str = "WebPage") -> str:
    data = {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": title,
        "description": description,
        "url": canonical_url(path),
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_DOMAIN + "/"},
        "publisher": {"@type": "Organization", "name": ORG_NAME, "url": SITE_DOMAIN + "/"},
    }
    return json_ld_script(data)


def organization_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ORG_NAME,
        "url": SITE_DOMAIN + "/",
        "logo": OG_IMAGE,
        "sameAs": [GITHUB_URL, YOUTUBE_URL],
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
<meta property="og:image:width" content="{OG_IMAGE_WIDTH}">
<meta property="og:image:height" content="{OG_IMAGE_HEIGHT}">
<meta property="og:image:alt" content="{esc(SITE_NAME)} — ESP32 projects and tutorials">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">"""


def itemlist_schema(name: str, items: list[dict]) -> str:
    elements = []
    for i, item in enumerate(items, 1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": item["name"],
                "url": item["url"],
            }
        )
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "itemListElement": elements,
    }
    return json_ld_script(data)


def analytics_config_script() -> str:
    ga = esc(GA4_MEASUREMENT_ID)
    return f'<script>window.SITE_GA4="{ga}";</script>'


def font_links_html() -> str:
    return """<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap"></noscript>"""


def head_extras_html() -> str:
    return f'<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)}" href="/feed.xml">'


def pagination_head_links(page: int, total_pages: int, page_path_fn) -> str:
    if total_pages <= 1:
        return ""
    links = []
    if page > 1:
        links.append(f'<link rel="prev" href="{esc(page_path_fn(page - 1))}">')
    if page < total_pages:
        links.append(f'<link rel="next" href="{esc(page_path_fn(page + 1))}">')
    return "\n".join(links)


def pagination_nav_html(page: int, total_pages: int, page_path_fn, base: str = "") -> str:
    if total_pages <= 1:
        return ""
    prev_link = ""
    next_link = ""
    if page > 1:
        prev_link = f'<a class="btn btn-secondary btn-sm" rel="prev" href="{esc(base + page_path_fn(page - 1))}">← Previous</a>'
    if page < total_pages:
        next_link = f'<a class="btn btn-secondary btn-sm" rel="next" href="{esc(base + page_path_fn(page + 1))}">Next →</a>'
    nums = []
    for n in range(1, total_pages + 1):
        if n == page:
            nums.append(f'<span class="pagination-current" aria-current="page">{n}</span>')
        else:
            nums.append(f'<a href="{esc(base + page_path_fn(n))}">{n}</a>')
    return f"""<nav class="pagination wrap" aria-label="Project list pages">
  <div class="pagination-actions">{prev_link}{next_link}</div>
  <div class="pagination-nums">{" ".join(nums)}</div>
  <p class="meta pagination-meta">Page {page} of {total_pages}</p>
</nav>"""


def projects_page_path(page: int) -> str:
    return "projects.html" if page == 1 else f"projects-page-{page}.html"


def projects_page_canonical(page: int) -> str:
    return projects_page_path(page)


def gsc_verification_meta() -> str:
    if not GSC_VERIFICATION:
        return ""
    return f'<meta name="google-site-verification" content="{esc(GSC_VERIFICATION)}">'


def pinterest_verification_meta() -> str:
    if not PINTEREST_VERIFICATION:
        return ""
    return f'<meta name="p:domain_verify" content="{esc(PINTEREST_VERIFICATION)}">'


def head_html(
    base: str,
    title: str,
    description: str,
    canonical_path: str = "",
    og_type: str = "website",
    extra_schema: str = "",
    include_gsc: bool = True,
    robots: str = "index,follow,max-image-preview:large",
    include_index_redirect: bool = False,
) -> str:
    t = esc(title)
    d = esc(description)
    canon = canonical_url(canonical_path)
    gsc = gsc_verification_meta() if include_gsc else ""
    pinterest = pinterest_verification_meta()
    extras = head_extras_html()
    redirect = index_redirect_script() if include_index_redirect else ""
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#6D28D9">
<meta name="robots" content="{esc(robots)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{extras}
{social_meta(title, description, canon, og_type)}
{pinterest}
{gsc}
{redirect}
<script>document.documentElement.classList.add("js")</script>
{analytics_config_script()}
{font_links_html()}
<link rel="preload" href="/style.css?v={CSS_VERSION}" as="style">
<link rel="stylesheet" href="/style.css?v={CSS_VERSION}">
{extra_schema}"""


def sidebar_categories_html(active: str = "") -> str:
    items = []
    for label, href, key in SIDEBAR_CATEGORIES:
        cls = ' class="is-active"' if active == key else ""
        items.append(
            f'<a href="{site_href(href)}"{cls}><span class="sidebar-cat-dot" aria-hidden="true"></span>{esc(label)}</a>'
        )
    return f"""<aside class="sidebar-categories" aria-label="Browse categories">
  <div class="sidebar-categories-inner">
    <h2 class="sidebar-title">Categories</h2>
    <nav class="sidebar-cat-nav">{"".join(items)}</nav>
  </div>
</aside>"""


def search_overlay_html() -> str:
    return f"""<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-overlay-backdrop" data-close-search></div>
  <div class="search-overlay-panel" role="dialog" aria-label="Search projects">
    <form class="search-overlay-form" action="/projects.html" method="get">
      <label class="visually-hidden" for="global-search">Search projects</label>
      <input id="global-search" name="q" type="search" placeholder="Search ESP32 projects, guides, categories…" autocomplete="off">
      <button type="submit" class="btn btn-primary">Search</button>
      <button type="button" class="search-close" data-close-search aria-label="Close search">×</button>
    </form>
  </div>
</div>"""


def header_html(active: str = "home", base: str = ""):
    nav_home = ' class="active"' if active == "home" else ""
    nav_guides = ' class="active"' if active == "guides" else ""
    nav_proj = ' class="active"' if active == "projects" else ""
    nav_about = ' class="active"' if active == "about" else ""
    nav_contact = ' class="active"' if active == "contact" else ""
    return f"""<div class="site-nav-sticky">
<header class="site-header"><div class="wrap header-inner">
  <a class="site-logo" href="{site_href()}"><span class="logo-mark" aria-hidden="true"></span><span class="logo-text">ESP32<span class="logo-accent">Engine</span></span><span class="logo-tagline">{esc(SITE_TAGLINE)}</span></a>
  <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="top-nav" aria-label="Main">
    <a href="{site_href()}"{nav_home}>Home</a>
    <a href="{site_href('guides.html')}"{nav_guides}>Guides</a>
    <a href="{site_href('projects.html')}"{nav_proj}>Projects</a>
    <a href="{site_href('about.html')}"{nav_about}>About</a>
    <a href="{site_href('contact.html')}"{nav_contact}>Contact</a>
  </nav>
  <div class="header-actions">
    <button type="button" class="icon-btn" id="search-open" aria-label="Search">{ICON_SEARCH}</button>
    <a class="icon-btn" href="{esc(GITHUB_URL)}" rel="noopener noreferrer" target="_blank" aria-label="GitHub">{ICON_GITHUB}</a>
    <a class="icon-btn" href="{esc(YOUTUBE_URL)}" rel="noopener noreferrer" target="_blank" aria-label="YouTube">{ICON_YOUTUBE}</a>
  </div>
</div></header>
</div>
{search_overlay_html()}"""


def category_hero_html(title: str, description: str, category: str, badges: str = "") -> str:
    from project_icons import pick_icon, thumb_class

    tc = thumb_class(category)
    icon = pick_icon(category)
    badge_html = f'<div class="hero-badges">{badges}</div>' if badges else ""
    return f"""<section class="category-banner reveal">
  <div class="wrap category-banner-inner">
    <div class="category-banner-content">
      <nav class="breadcrumb breadcrumb-light" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('projects.html')}">Projects</a></li><li aria-current="page">{esc(short_category(category))}</li></ol></nav>
      <p class="hero-eyebrow">{esc(SITE_TAGLINE)}</p>
      <h1>{esc(title)}</h1>
      <p class="hero-sub">{esc(description)}</p>
      {badge_html}
    </div>
    <div class="category-banner-visual {tc}" aria-hidden="true">{icon}</div>
  </div>
</section>"""


def filters_bar_html(show_sort: bool = True) -> str:
    sort = ""
    if show_sort:
        sort = """<select id="sort" aria-label="Sort projects">
      <option value="featured">Sort: Featured</option>
      <option value="title">Sort: A–Z</option>
      <option value="category">Sort: Category</option>
    </select>"""
    return f"""<div class="filters-bar">
  <div class="search-panel">
    <input id="q" type="search" placeholder="Search projects…" aria-label="Search projects">
    {sort}
    <select id="cat" aria-label="Filter by category"><option value="">All categories</option></select>
    <select id="diff" aria-label="Filter by difficulty"><option value="">All levels</option><option value="Beginner">Beginner</option><option value="Intermediate">Intermediate</option><option value="Advanced">Advanced</option></select>
  </div>
  <p class="filter-meta meta" id="count"></p>
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
<script src="/ui.js" defer></script>
</body>
</html>
"""


def hero_html(latest_items: str = "") -> str:
    home = load_home()
    eyebrow = home.get("hero_eyebrow", "ESP32 &amp; IoT Technology Portal")
    heading = home.get("hero_title", "One ESP32. Unlimited Possibilities.")
    sub = home.get(
        "hero_sub",
        "Build IoT systems, smart automation, robotics, wireless devices, monitoring solutions, and real-world embedded projects.",
    )
    stats = [
        ("15+", "Parent Projects"),
        ("45+", "Difficulty Levels"),
        ("10+", "Categories"),
        ("100%", "Free Learning"),
    ]
    stat_items = "".join(
        f'<div class="hero-stat-pill"><strong>{esc(val)}</strong><span>{esc(label)}</span></div>'
        for val, label in stats
    )
    return f"""<section class="hero-home reveal" aria-labelledby="hero-heading">
  <div class="wrap hero-home-inner">
    <div class="hero-home-content">
      <p class="hero-eyebrow">{esc(eyebrow)}</p>
      <h1 id="hero-heading">{esc(heading)}</h1>
      <p class="hero-sub">{esc(sub)}</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="/projects.html">Explore Projects</a>
        <a class="btn btn-secondary btn-lg" href="/guides.html">Start Learning</a>
      </div>
      <div class="hero-stat-row">{stat_items}</div>
    </div>
    <div class="hero-home-visual" aria-hidden="true">
      <div class="hero-visual-frame">{HERO_BOARD_SVG}{HERO_FLOAT_CARDS}</div>
    </div>
  </div>
</section>"""


def stats_html() -> str:
    return ""


def home_featured_carousel(projects: list, card_fn) -> str:
    featured = projects[:8]
    cards = "".join(card_fn(p) for p in featured)
    return f"""<section class="section-premium wrap reveal" id="featured">
  <div class="section-head">
    <div><p class="section-eyebrow">Editor's pick</p><h2>Featured Projects</h2></div>
    <div class="carousel-controls">
      <a class="btn btn-secondary btn-sm" href="/projects.html">View all</a>
      <button type="button" class="carousel-btn" data-carousel="featured" data-dir="-1" aria-label="Scroll left">‹</button>
      <button type="button" class="carousel-btn" data-carousel="featured" data-dir="1" aria-label="Scroll right">›</button>
    </div>
  </div>
  <div class="carousel-shell">
    <div class="carousel-track" id="carousel-featured" tabindex="0" role="region" aria-label="Featured ESP32 projects">{cards}</div>
  </div>
</section>"""


def home_latest_categories_section(projects: list) -> str:
    from project_icons import pick_icon, thumb_class, slug_cat

    latest = list(reversed(projects[-6:]))
    tutorial_rows = []
    for p in latest:
        tc = thumb_class(p["category"])
        icon = pick_icon(p["category"])
        tutorial_rows.append(
            f'<a class="tutorial-row" href="{esc(p["href"])}">'
            f'<span class="tutorial-icon {tc}">{icon}</span>'
            f'<span class="tutorial-meta"><strong>{esc(p["title"])}</strong>'
            f'<span class="tutorial-cat">{esc(short_category(p["category"]))} · 3 levels</span></span>'
            f'<span class="tutorial-arrow" aria-hidden="true">→</span></a>'
        )
    cats = [
        ("IoT", "IoT Projects"),
        ("Automation", "Home Automation"),
        ("Sensors", "Sensor Projects"),
        ("Robotics", "Robotics"),
        ("Smart Home", "Home Automation"),
        ("Security", "Security Projects"),
        ("Industrial", "Industrial Automation"),
        ("Communication", "IoT Projects"),
        ("Monitoring", "Energy Monitoring"),
        ("Energy", "Energy Monitoring"),
    ]
    cat_cards = []
    for label, cat in cats:
        slug = slug_cat(cat)
        tc = thumb_class(cat)
        icon = pick_icon(cat)
        cat_cards.append(
            f'<a class="pop-cat tech-cat-card" href="/category/{slug}.html">'
            f'<span class="pop-cat-icon {tc}">{icon}</span><span>{label}</span></a>'
        )
    return f"""<section class="portal-section wrap reveal portal-duo" id="latest">
  <div class="portal-duo-col portal-latest">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Fresh guides</p>
      <h2>Latest Tutorials</h2>
    </div>
    <div class="tutorial-list">{"".join(tutorial_rows)}</div>
  </div>
  <div class="portal-duo-col portal-categories" id="categories">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Top domains</p>
      <h2>Popular Categories</h2>
    </div>
    <div class="pop-cat-grid">{"".join(cat_cards)}</div>
  </div>
</section>"""


def home_roadmap_stats_section(project_count: int) -> str:
    stats = [
        ("15+", "Parent Projects"),
        ("45+", "Difficulty Levels"),
        ("10+", "Categories"),
        ("100%", "Free Learning"),
    ]
    stat_cards = "".join(
        f'<div class="portal-stat"><strong>{esc(val)}</strong><span>{esc(label)}</span></div>'
        for val, label in stats
    )
    return f"""<section class="portal-section wrap reveal portal-duo portal-roadmap-stats" id="roadmap">
  <div class="portal-duo-col roadmap-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Structured learning</p>
      <h2>ESP32 Learning Roadmap</h2>
    </div>
    <div class="roadmap-track roadmap-track-premium">
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">01</span><div><strong class="badge badge-beginner">Beginner</strong><span>Sensors, serial output, threshold logic</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">02</span><div><strong class="badge badge-intermediate">Intermediate</strong><span>OLED, calibration, manual/auto modes</span></div></div>
      <div class="roadmap-connector roadmap-connector-premium" aria-hidden="true"></div>
      <div class="roadmap-node roadmap-node-premium"><span class="roadmap-num">03</span><div><strong class="badge badge-advanced">Advanced</strong><span>Wi-Fi dashboards, alerts, logging</span></div></div>
    </div>
    <a class="roadmap-link" href="/projects.html">Browse all {project_count} projects →</a>
  </div>
  <div class="portal-duo-col stats-panel">
    <div class="section-head-portal section-head-portal-inline">
      <p class="section-eyebrow">Library at a glance</p>
      <h2>Project Statistics</h2>
    </div>
    <div class="portal-stats-grid">{stat_cards}</div>
    <div class="stats-highlights">
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⚡</span><span>Wiring tables on every guide</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">⌨</span><span>Copy-paste Arduino sketches</span></div>
      <div class="stats-highlight"><span class="stats-highlight-icon" aria-hidden="true">📱</span><span>Mobile-friendly layouts</span></div>
    </div>
  </div>
</section>"""


def home_why_section() -> str:
    items = [
        ("🎯", "Beginner Friendly", "Start with breadboard builds and clear wiring tables."),
        ("🔧", "Real Hardware Projects", "Every guide maps to sensors, relays, and ESP32 pins."),
        ("📊", "Multiple Difficulty Levels", "Beginner, Intermediate, and Advanced on every project."),
        ("⚡", "Practical Learning", "Copy-paste Arduino code with troubleshooting steps."),
        ("📡", "Modern ESP32 Techniques", "Wi-Fi, OLED, MQTT, and IoT dashboards."),
        ("🚀", "Production Ready Concepts", "Patterns you can ship beyond the prototype stage."),
    ]
    cards = "".join(
        f'<div class="why-card-premium reveal"><span class="why-icon" aria-hidden="true">{icon}</span><strong>{esc(title)}</strong><p>{esc(desc)}</p></div>'
        for icon, title, desc in items
    )
    return f"""<section class="portal-section wrap reveal" id="why">
  <div class="section-head-portal">
    <div class="section-head-portal-text">
      <p class="section-eyebrow">Built for makers</p>
      <h2>Why This Platform</h2>
    </div>
  </div>
  <div class="why-grid-premium">{cards}</div>
</section>"""


def home_guides_section(guides: list) -> str:
    tracks = [
        ("Beginner Guides", "Foundations, chip basics, and your first breadboard builds.", site_href("guides/what-is-esp32.html"), "Phase 1"),
        ("Intermediate Guides", "OLED feedback, calibration, and multi-sensor workflows.", site_href("guides.html"), "Phase 2"),
        ("ESP-IDF Tutorials", "Native SDK concepts for production firmware.", site_href("guides.html"), "Coming soon"),
        ("Arduino Tutorials", "IDE setup, board packages, and sketch workflows.", site_href("guides/installing-arduino-ide-esp32.html"), "Setup"),
    ]
    track_cards = "".join(
        f'<a class="guide-track-card" href="{esc(href)}"><span class="guide-track-badge">{esc(badge)}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p><span class="btn btn-card">Browse<span aria-hidden="true">→</span></span></a>'
        for title, desc, href, badge in tracks
    )
    ordered = sorted(guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99), g.get("slug", "")))
    article_cards = []
    for g in ordered:
        slug = g["slug"]
        headline = g.get("headline") or g.get("title", "").split("|")[0].strip()
        desc = g.get("lead") or g.get("meta_description", "")
        if len(desc) > 110:
            desc = desc[:107].rstrip() + "…"
        phase = g.get("phase")
        phase_badge = f'<span class="badge badge-cat">Phase {phase}</span>' if phase else ""
        article_cards.append(
            f'<a class="guide-home-card" href="{site_href(f"guides/{slug}.html")}">'
            f'<div class="guide-card-badges">{phase_badge}</div>'
            f"<h3>{esc(headline)}</h3>"
            f"<p>{esc(desc)}</p>"
            f'<span class="btn btn-card">Read Guide<span aria-hidden="true">→</span></span></a>'
        )
    return f"""<section class="section-premium wrap reveal" id="guides">
  <div class="section-head">
    <div><p class="section-eyebrow">Learning paths</p><h2>ESP32 Guides &amp; Tutorials</h2><p class="section-sub">Structured paths from chip fundamentals to Arduino IDE setup and beyond.</p></div>
    <a class="btn btn-secondary btn-sm" href="{site_href('guides.html')}">All guides</a>
  </div>
  <div class="guide-tracks-grid">{track_cards}</div>
  <div class="guide-home-grid">{"".join(article_cards)}</div>
</section>"""


def home_community_section() -> str:
    return f"""<section class="portal-section wrap reveal" id="community">
  <div class="community-panel">
    <div class="community-panel-icon" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none" width="40" height="40"><circle cx="32" cy="22" r="8" stroke="currentColor" stroke-width="2"/><path d="M12 52c0-11 9-18 20-18s20 7 20 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="48" cy="24" r="5" stroke="currentColor" stroke-width="1.8"/><path d="M52 44c0-6-4-10-9-10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="16" cy="24" r="5" stroke="currentColor" stroke-width="1.8"/><path d="M12 44c0-6 4-10 9-10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </div>
    <div class="community-panel-body">
      <p class="section-eyebrow">Stay connected</p>
      <h2>Newsletter &amp; Community</h2>
      <p class="community-lead">Get project updates, share builds, and connect with makers learning ESP32.</p>
    </div>
    <div class="community-panel-actions">
      <a class="btn btn-primary" href="{esc(GITHUB_URL)}" rel="noopener noreferrer" target="_blank">Star on GitHub</a>
      <a class="btn btn-secondary" href="/contact.html">Join Discussion</a>
    </div>
  </div>
</section>"""


def home_cta_banner(project_count: int) -> str:
    return f"""<section class="portal-cta wrap reveal">
  <div class="portal-cta-inner">
    <div class="portal-cta-text">
      <h2>Start Building with ESP32 Today</h2>
      <p>{project_count} parent projects · 3 difficulty levels · wiring &amp; code included</p>
    </div>
    <div class="portal-cta-actions">
      <a class="btn btn-primary" href="/projects.html">Explore Projects</a>
      <a class="btn btn-secondary" href="/category/iot-projects.html">Browse IoT</a>
    </div>
  </div>
</section>"""


def footer_html(base: str = "") -> str:
    from project_icons import slug_cat

    cat_links = "".join(
        f'<a href="{site_href(f"category/{slug_cat(cat)}.html")}">{esc(short_category(cat))}</a>'
        for _, cat in [
            ("IoT", "IoT Projects"),
            ("CAM", "ESP32-CAM"),
            ("Home", "Home Automation"),
            ("Robotics", "Robotics"),
            ("Sensors", "Sensor Projects"),
        ]
    )
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <strong>{SITE_NAME}</strong>
      <p class="footer-tagline">{esc(SITE_TAGLINE)}</p>
      <p>Premium ESP32 tutorials with wiring tables, Arduino code, and three difficulty levels for makers and engineers.</p>
      <div class="footer-social">
        <a href="{esc(GITHUB_URL)}" rel="noopener noreferrer" target="_blank" aria-label="GitHub">{ICON_GITHUB}</a>
        <a href="{esc(YOUTUBE_URL)}" rel="noopener noreferrer" target="_blank" aria-label="YouTube">{ICON_YOUTUBE}</a>
      </div>
    </div>
    <div class="footer-col"><h4>Explore</h4><a href="{site_href()}">Home</a><a href="{site_href('guides.html')}">Guides</a><a href="{site_href('projects.html')}">All Projects</a><a href="{site_href('sitemap.html')}">Sitemap</a></div>
    <div class="footer-col"><h4>Categories</h4>{cat_links}</div>
    <div class="footer-col"><h4>Company</h4><a href="{site_href('about.html')}">About</a><a href="{site_href('contact.html')}">Contact</a><a href="{site_href('privacy.html')}">Privacy Policy</a><a href="{site_href('terms.html')}">Terms</a><a href="{site_href('disclaimer.html')}">Disclaimer</a></div>
  </div>
  <div class="wrap footer-bottom"><p>© 2026 {SITE_NAME}. All rights reserved.</p></div>
</footer>"""


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
