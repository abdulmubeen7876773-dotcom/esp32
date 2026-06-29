import html
import json
import re

from cms_loader import load_home, load_site_settings
from project_icons import pick_icon, thumb_class, featured_cat_bar

_cfg = load_site_settings()
CSS_VERSION = _cfg["css_version"]
JS_VERSION = _cfg.get("js_version", CSS_VERSION)
UI_JS_SRC = f"/ui.js?v={JS_VERSION}"
SEARCH_JS_SRC = f"/search.js?v={JS_VERSION}"
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
GOOGLE_TAG_HTML = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA4_MEASUREMENT_ID}');
</script>"""

HERO_BOARD_SVG = """<svg class="hero-board-svg" viewBox="0 0 280 280" fill="none" aria-hidden="true"><defs><linearGradient id="heroGrad" x1="50" y1="70" x2="230" y2="210"><stop stop-color="#2563EB"/><stop offset="1" stop-color="#1D4ED8"/></linearGradient><filter id="heroGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect x="50" y="72" width="180" height="116" rx="20" stroke="url(#heroGrad)" stroke-width="3" filter="url(#heroGlow)"/><rect x="78" y="98" width="124" height="64" rx="12" fill="rgba(37,99,235,.08)" stroke="rgba(37,99,235,.28)" stroke-width="1.5"/><path d="M50 98h-20M50 130h-20M50 162h-20M230 98h20M230 130h20M230 162h20M98 72V48M140 72V48M182 72V48M98 188V212M140 188V212M182 188V212" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" opacity=".55"/><circle cx="140" cy="130" r="10" fill="#2563EB"/><circle cx="140" cy="130" r="20" stroke="#2563EB" stroke-width="1.5" opacity=".35"/><text x="140" y="136" text-anchor="middle" fill="#1D4ED8" font-size="18" font-weight="700" font-family="Poppins,Inter,sans-serif">ESP32</text><circle cx="210" cy="60" r="6" fill="#FBBF24" opacity=".9"/><circle cx="70" cy="220" r="5" fill="#EF4444" opacity=".75"/><path d="M200 220l20-16 12 20" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".65"/></svg>"""

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
ICON_THEME = '<span class="theme-icon theme-icon-moon" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="theme-icon theme-icon-sun" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" stroke-linecap="round"/></svg></span>'

LOGO_HTML = (
    '<img class="site-logo-img" src="/assets/visuals/brand/esp32engine-logo-header.png" '
    'alt="ESP32 Engine" width="132" height="56" decoding="async">'
)

HERO_FLOAT_CARDS = """<div class="hero-float-stack" aria-hidden="true">
<div class="hero-float-card hero-float-card-a"><span class="hero-float-label">🌡 Temperature</span><strong>24°C</strong><span class="hero-float-sub">DHT22 Sensor</span></div>
<div class="hero-float-card hero-float-card-b"><span class="hero-float-label">📡 Wi-Fi</span><strong>Connected!</strong><span class="hero-float-sub">Your project is live</span></div>
<div class="hero-float-card hero-float-card-c"><span class="hero-float-label">💡 LED</span><strong>ON</strong><span class="hero-float-sub">You did it!</span></div>
</div>"""

NAV_ITEMS = [
    ("home", "Home", ""),
    ("learning", "Learning", "learning.html"),
    ("guides", "Guides", "guides.html"),
    ("components", "Components", "components.html"),
    ("projects", "Projects", "projects.html"),
    ("parents", "Parents", "parents.html"),
    ("teachers", "Teachers", "teachers.html"),
    ("tools", "Tools", "tools.html"),
    ("about", "About", "about.html"),
]


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


def card_media_html(
    category: str,
    slug: str = "",
    featured_image: str = "",
) -> str:
    tc = thumb_class(category)
    icon = pick_icon(category)
    label = short_category(category)
    if featured_image and not str(featured_image).startswith("TODO"):
        return (
            f'<div class="card-media card-media--has-image">'
            f'<img class="card-media-img" src="{esc(featured_image)}" alt="" loading="lazy" decoding="async" '
            f'onerror="this.closest(&#39;.card-media&#39;).classList.add(&#39;is-fallback&#39;)">'
            f'<div class="card-media-fallback {tc}">{icon}</div>'
            f"</div>"
        )
    return (
        f'<div class="card-media card-media--placeholder {tc}">'
        f'<span class="card-media-icon" aria-hidden="true">{icon}</span>'
        f'<span class="card-media-label">{esc(label)}</span>'
        f"</div>"
    )


TOP_PROJECT_SLUGS = [
    "esp32-iot-weather-station",
    "esp32-smart-thermostat",
    "esp32-line-following-robot",
]
TOP_GUIDE_SLUGS = ["blink-led-esp32", "read-temperature-dht22", "what-is-esp32"]
TOP_COMPONENT_SLUGS = ["dht22", "bme280", "esp32-devkit"]


def _pick_by_slug(items: list, slugs: list[str], key: str = "slug") -> list:
    by_slug = {i.get(key, ""): i for i in items}
    return [by_slug[s] for s in slugs if s in by_slug]


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
    media = card_media_html(cat, slug, p.get("featured_image") or p.get("image") or "")
    return f"""<a class="{card_class} modern-card project-card-item" href="{esc(link)}"{extra_attrs}><div class="card-media-wrap">{media}</div><div class="card-body"><div class="card-badges">{feat_badge}<span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge {badge_class(diff)}">{esc(diff.replace(' build',''))}</span><span class="badge badge-time">{esc(rt)}</span></div><h3>{esc(p['title'])}</h3>{desc_html}<div class="card-footer"><span class="btn btn-card">Read More<span aria-hidden="true">→</span></span></div></div></a>"""


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
            "target": f"{SITE_DOMAIN}/search.html?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    return json_ld_script(data)


def social_meta(
    title: str,
    description: str,
    url: str,
    og_type: str = "website",
    image: str = "",
) -> str:
    t = esc(title)
    d = esc(description)
    u = esc(url)
    img_src = image or OG_IMAGE
    if img_src.startswith("/"):
        img_src = SITE_DOMAIN.rstrip("/") + img_src
    img = esc(img_src)
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
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Poppins:wght@600;700;800&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Poppins:wght@600;700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Poppins:wght@600;700;800&display=swap"></noscript>"""


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
    og_image: str = "",
) -> str:
    t = esc(title)
    d = esc(description)
    canon = canonical_url(canonical_path)
    gsc = gsc_verification_meta() if include_gsc else ""
    pinterest = pinterest_verification_meta()
    extras = head_extras_html()
    redirect = index_redirect_script() if include_index_redirect else ""
    return f"""{GOOGLE_TAG_HTML}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#2563EB">
<meta name="robots" content="{esc(robots)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{extras}
{social_meta(title, description, canon, og_type, og_image)}
{pinterest}
{gsc}
{redirect}
<script>(function(){{try{{var t=localStorage.getItem("theme");if(t==="dark"||t==="light"){{document.documentElement.setAttribute("data-theme",t);return;}}if(window.matchMedia("(prefers-color-scheme: dark)").matches){{document.documentElement.setAttribute("data-theme","dark");return;}}document.documentElement.setAttribute("data-theme","light");}}catch(e){{document.documentElement.setAttribute("data-theme","light");}}}})();</script>
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
    return """<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-overlay-backdrop" data-close-search></div>
  <div class="search-overlay-panel" role="dialog" aria-label="Search everything">
    <form class="search-overlay-form" id="global-search-form" action="/search.html" method="get">
      <label class="visually-hidden" for="global-search">Search</label>
      <input id="global-search" name="q" type="search" placeholder="Search components, projects, guides…" autocomplete="off">
      <button type="submit" class="btn btn-primary">Search</button>
      <button type="button" class="search-close" data-close-search aria-label="Close search">×</button>
    </form>
    <div class="search-results" id="search-results-live" hidden></div>
  </div>
</div>"""


def nav_spotlight_html(project_count: int = 50) -> str:
    links = [
        ("Smart Thermostat", "projects/esp32-smart-thermostat.html"),
        ("BME280 Sensor", "components/bme280.html"),
        ("Line Following Robot", "projects/esp32-line-following-robot.html"),
        (f"{project_count} Projects", "projects.html"),
    ]
    items = "".join(
        f'<a class="nav-spotlight-link{" nav-spotlight-badge" if label.endswith("Projects") else ""}" href="{site_href(href)}">{esc(label)}</a>'
        for label, href in links
    )
    return f"""<div class="nav-spotlight" aria-label="New and popular content">
  <div class="wrap nav-spotlight-scroll">
    <div class="nav-spotlight-inner">
    <span class="nav-spotlight-label">Explore</span>
    {items}
    </div>
  </div>
</div>"""


def header_html(active: str = "home", base: str = "", project_count: int | None = None):
    if project_count is None:
        from content_store import get_content_store
        project_count = len(get_content_store().projects())
    nav_links = []
    for key, label, href in NAV_ITEMS:
        cls = ' class="active"' if active == key else ""
        nav_links.append(f'<a href="{site_href(href)}"{cls}>{esc(label)}</a>')
    return f"""<div class="site-nav-sticky">
<header class="site-header"><div class="wrap header-inner">
  <a class="site-logo" href="{site_href()}">{LOGO_HTML}</a>
  <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="top-nav" aria-label="Main">
    {"".join(nav_links)}
  </nav>
  <div class="header-actions">
    <button type="button" class="icon-btn theme-toggle" id="theme-toggle" aria-label="Switch to dark mode">{ICON_THEME}</button>
    <button type="button" class="icon-btn" id="search-open" aria-label="Search">{ICON_SEARCH}</button>
    <a class="icon-btn" href="{esc(GITHUB_URL)}" rel="noopener noreferrer" target="_blank" aria-label="GitHub">{ICON_GITHUB}</a>
    <a class="icon-btn" href="{esc(YOUTUBE_URL)}" rel="noopener noreferrer" target="_blank" aria-label="YouTube">{ICON_YOUTUBE}</a>
  </div>
</div></header>
{nav_spotlight_html(project_count)}
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
<body class="{esc(active)}-page">
<main>
{header_html(active)}
<section class="section-block wrap page-head static-page">
{body}
</section>
</main>
{footer_html()}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
</body>
</html>
"""


def hero_title_html(title: str) -> str:
    marker = "ESP32"
    idx = title.find(marker)
    if idx == -1:
        return esc(title)
    return f'{esc(title[:idx])}<span class="hero-highlight">{marker}</span>{esc(title[idx + len(marker):])}'


def hero_html(latest_items: str = "") -> str:
    home = load_home()
    eyebrow = home.get("hero_eyebrow", "Your ESP32 Adventure Starts Here")
    heading = home.get("hero_title", "Build Amazing Things with ESP32")
    sub = home.get(
        "hero_sub",
        "Learn electronics through fun projects, simple explanations and interactive guides.",
    )
    return f"""<section class="hero-home reveal" aria-labelledby="hero-heading">
  <div class="wrap hero-home-inner">
    <div class="hero-home-content">
      <p class="hero-eyebrow">{esc(eyebrow)}</p>
      <h1 id="hero-heading">{hero_title_html(heading)}</h1>
      <p class="hero-sub">{esc(sub)}</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="{site_href('learning.html')}">Start Learning</a>
        <a class="btn btn-secondary btn-lg" href="{site_href('components.html')}">Browse Components</a>
      </div>
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


def home_learning_paths_section() -> str:
    from cms_loader import load_learning_paths
    paths = load_learning_paths()
    cards = []
    for p in paths:
        steps = p.get("steps_label") or f"{p.get('lessons', 0)} steps"
        cards.append(
            f'<a class="path-card" href="{esc(site_href(p.get("href", "learning.html")))}">'
            f'<span class="path-icon" aria-hidden="true">{esc(p.get("icon", "🚀"))}</span>'
            f'<h3>{esc(p["title"])}</h3>'
            f'<p>{esc(p.get("description", ""))}</p>'
            f'<div class="path-meta">'
            f'<span class="badge badge-cat">{esc(str(steps))}</span>'
            f'<span class="badge {badge_class(p.get("difficulty", "Beginner"))}">{esc(p.get("difficulty", "Beginner"))}</span>'
            f'</div></a>'
        )
    return f"""<section class="section-premium wrap reveal" id="learning-paths">
  <div class="section-head">
    <div><p class="section-eyebrow">Choose your adventure</p><h2>Learning Paths</h2><p class="section-sub">Pick a path that matches your level. Every journey has fun missions and real builds.</p></div>
    <a class="btn btn-secondary btn-sm" href="{site_href('learning.html')}">All paths</a>
  </div>
  <div class="learning-path-grid">{"".join(cards)}</div>
</section>"""


def home_components_section() -> str:
    from cms_loader import load_components
    components = load_components()[:6]
    cards = []
    for c in components:
        img = c.get("image", "")
        img_html = f'<img src="{esc(img)}" alt="{esc(c["name"])}" loading="lazy">' if img else f'<span style="font-size:3rem">{esc(c.get("icon", "🔌"))}</span>'
        cards.append(
            f'<a class="component-card" href="{site_href(f"components/{c["slug"]}.html")}">'
            f'<div class="component-card-img">{img_html}</div>'
            f'<div class="component-card-body">'
            f'<span class="badge badge-cat">{esc(c.get("category", ""))}</span>'
            f'<span class="badge {badge_class(c.get("difficulty", "Beginner"))}">{esc(c.get("difficulty", "Beginner"))}</span>'
            f'<h3>{esc(c["name"])}</h3>'
            f'<span class="btn btn-card">View Guide<span aria-hidden="true">→</span></span>'
            f'</div></a>'
        )
    return f"""<section class="section-premium wrap reveal" id="components">
  <div class="section-head">
    <div><p class="section-eyebrow">Component encyclopedia</p><h2>Popular Components</h2><p class="section-sub">Learn what each part does, how to wire it, and what you can build.</p></div>
    <a class="btn btn-secondary btn-sm" href="{site_href('components.html')}">Browse all</a>
  </div>
  <div class="grid grid-projects">{"".join(cards)}</div>
</section>"""


def home_featured_projects_section(projects: list, card_fn) -> str:
    featured_titles = [
        "ESP32 IoT Weather Station",
        "ESP32 WiFi Robot Controller",
        "ESP32 Smart Irrigation System",
        "ESP32 Motion Security Alert",
        "ESP32 Home Climate Automation",
        "ESP32 TinyML Sound Classifier",
    ]
    by_title = {p["title"]: p for p in projects}
    featured = [by_title[t] for t in featured_titles if t in by_title]
    if not featured:
        featured = projects[:6]
    cards = "".join(card_fn(p) for p in featured)
    return f"""<section class="section-premium wrap reveal" id="featured">
  <div class="section-head">
    <div><p class="section-eyebrow">Build something cool</p><h2>Featured Projects</h2><p class="section-sub">Weather stations, robots, smart homes and more — pick a project and start building.</p></div>
    <a class="btn btn-secondary btn-sm" href="{site_href('projects.html')}">All projects</a>
  </div>
  <div class="carousel-shell">
    <div class="carousel-track" id="carousel-featured" tabindex="0" role="region" aria-label="Featured ESP32 projects">{cards}</div>
  </div>
</section>"""


def home_parents_section() -> str:
    return f"""<section class="section-premium wrap reveal audience-section audience-parents" id="for-parents">
  <div class="audience-panel">
    <div class="audience-icon" aria-hidden="true">👨‍👩‍👧</div>
    <div class="audience-content">
      <p class="section-eyebrow">For Parents</p>
      <h2>Safe, Simple Learning for Young Makers</h2>
      <p>ESP32 Engine helps children learn electronics through guided projects, safety notes, and simple explanations parents can trust.</p>
      <a class="btn btn-primary" href="{site_href('parents.html')}">Guide for Parents</a>
    </div>
  </div>
</section>"""


def home_teachers_section() -> str:
    return f"""<section class="section-premium wrap reveal audience-section audience-teachers" id="for-teachers">
  <div class="audience-panel">
    <div class="audience-icon" aria-hidden="true">🏫</div>
    <div class="audience-content">
      <p class="section-eyebrow">For Teachers</p>
      <h2>Ready for Classroom Learning</h2>
      <p>Use structured lessons, project ideas, and printable resources to teach electronics, coding, and IoT step by step.</p>
      <a class="btn btn-primary" href="{site_href('teachers.html')}">Guide for Teachers</a>
    </div>
  </div>
</section>"""


def home_latest_guides_section(guides: list) -> str:
    from guide_mission import mission_meta_badges_html

    mission_guides = [g for g in guides if g.get("format") == "mission" or g.get("mission")]
    ordered = sorted(mission_guides or guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99)))[:4]
    cards = []
    for g in ordered:
        slug = g["slug"]
        headline = g.get("headline") or g.get("title", "").split("|")[0].strip()
        cards.append(
            f'<a class="mission-index-card guide-home-mission-card" href="{site_href(f"guides/{slug}.html")}">'
            f'{mission_meta_badges_html(g)}'
            f'<h3>{esc(headline)}</h3>'
            f'<span class="btn btn-card">Start Mission<span aria-hidden="true">→</span></span></a>'
        )
    return f"""<section class="section-premium wrap reveal" id="latest-guides">
  <div class="section-head">
    <div><p class="section-eyebrow">Interactive journeys</p><h2>Mission Journeys</h2><p class="section-sub">Hands-on missions with stories, safety tips, and step-by-step builds — not boring articles.</p></div>
    <a class="btn btn-secondary btn-sm" href="{site_href('guides.html')}">All guides</a>
  </div>
  <div class="guide-home-grid">{"".join(cards)}</div>
</section>"""


def home_newsletter_section() -> str:
    return f"""<section class="section-premium wrap reveal" id="newsletter">
  <div class="newsletter-panel">
    <div>
      <h2>Join the ESP32 Adventure!</h2>
      <p>Get new projects, fun challenges, and learning tips delivered to your inbox.</p>
    </div>
    <form class="newsletter-form" action="{site_href('contact.html')}" method="get">
      <input type="email" name="email" placeholder="Your email" aria-label="Email address" required>
      <button type="submit" class="btn btn-lg">Subscribe</button>
    </form>
  </div>
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


_V2_ARROW_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

_V2_HERO_BOARD_SVG = """<svg class="v2-hero-board-svg" viewBox="0 0 320 320" fill="none" aria-hidden="true"><defs><linearGradient id="v2hGrad" x1="60" y1="80" x2="260" y2="240"><stop stop-color="#0099FF" stop-opacity=".9"/><stop offset="1" stop-color="#00C896" stop-opacity=".9"/></linearGradient><filter id="v2hGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="v2hSoft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><ellipse cx="160" cy="160" rx="110" ry="88" fill="rgba(0,153,255,0.06)" filter="url(#v2hSoft)"/><rect x="60" y="80" width="200" height="130" rx="18" stroke="url(#v2hGrad)" stroke-width="2.5" fill="rgba(0,153,255,0.04)" filter="url(#v2hGlow)"/><rect x="90" y="108" width="140" height="74" rx="10" fill="rgba(0,153,255,0.05)" stroke="rgba(0,153,255,0.18)" stroke-width="1.5"/><path d="M60 108h-22M60 128h-22M60 148h-22M60 168h-22M60 188h-22" stroke="#0099FF" stroke-width="2" stroke-linecap="round" opacity=".4"/><path d="M260 108h22M260 128h22M260 148h22M260 168h22M260 188h22" stroke="#0099FF" stroke-width="2" stroke-linecap="round" opacity=".4"/><path d="M110 80V56M140 80V56M170 80V56M200 80V56M230 80V56" stroke="#00C896" stroke-width="2" stroke-linecap="round" opacity=".35"/><path d="M110 210V234M140 210V234M170 210V234M200 210V234M230 210V234" stroke="#00C896" stroke-width="2" stroke-linecap="round" opacity=".35"/><rect x="120" y="120" width="80" height="50" rx="6" fill="rgba(0,153,255,0.1)" stroke="rgba(0,153,255,0.35)" stroke-width="1.5"/><circle cx="160" cy="145" r="14" fill="rgba(0,200,150,0.12)" stroke="#00C896" stroke-width="1.5"/><text x="160" y="150" text-anchor="middle" fill="#0099FF" font-size="13" font-weight="700" font-family="Poppins,Inter,sans-serif" opacity=".9">ESP32</text><circle cx="240" cy="95" r="5" fill="#00C896" opacity=".8"/><circle cx="224" cy="95" r="5" fill="#FFD54F" opacity=".65"/><rect x="150" y="228" width="20" height="10" rx="3" stroke="rgba(0,153,255,0.35)" stroke-width="1.5" fill="none"/></svg>"""

_V2_HERO_FLOAT_CARDS = """<div class="v2-hero-float-stack" aria-hidden="true">
<div class="v2-hero-float-card v2-hero-float-card-a"><span class="v2-float-label">Temperature</span><strong>24.3°C</strong><span class="v2-float-sub">DHT22 Sensor</span></div>
<div class="v2-hero-float-card v2-hero-float-card-b"><span class="v2-float-label">Wi-Fi</span><strong>Connected</strong><span class="v2-float-sub">Your project is live</span></div>
<div class="v2-hero-float-card v2-hero-float-card-c"><span class="v2-float-label">LED</span><strong>ON</strong><span class="v2-float-sub">Mission complete</span></div>
</div>"""

_V2_SVG_WEATHER = """<svg viewBox="0 0 280 280" fill="none" aria-hidden="true"><defs><linearGradient id="v2wG" x1="0" y1="0" x2="280" y2="280"><stop stop-color="#0099FF" stop-opacity=".8"/><stop offset="1" stop-color="#00C896" stop-opacity=".6"/></linearGradient><filter id="v2wGl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect x="70" y="30" width="140" height="100" rx="8" stroke="url(#v2wG)" stroke-width="2" fill="rgba(0,153,255,0.07)" filter="url(#v2wGl)"/><rect x="82" y="46" width="116" height="2" rx="1" fill="rgba(0,153,255,0.5)"/><text x="140" y="90" text-anchor="middle" fill="#0099FF" font-size="30" font-weight="700" font-family="JetBrains Mono,monospace">24°C</text><text x="140" y="112" text-anchor="middle" fill="rgba(0,200,150,0.75)" font-size="11" font-family="Inter,sans-serif">Humidity: 62% · UV: Low</text><line x1="105" y1="130" x2="105" y2="165" stroke="rgba(0,153,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/><line x1="140" y1="130" x2="140" y2="165" stroke="rgba(0,153,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/><line x1="175" y1="130" x2="175" y2="165" stroke="rgba(0,153,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/><rect x="88" y="165" width="104" height="64" rx="6" stroke="rgba(0,200,150,0.55)" stroke-width="1.5" fill="rgba(0,200,150,0.05)"/><text x="140" y="193" text-anchor="middle" fill="rgba(0,200,150,0.7)" font-size="10" font-family="JetBrains Mono,monospace">DHT22</text><text x="140" y="210" text-anchor="middle" fill="rgba(0,200,150,0.45)" font-size="9" font-family="Inter,sans-serif">Temperature &amp; Humidity</text><line x1="105" y1="229" x2="105" y2="250" stroke="rgba(0,153,255,0.25)" stroke-width="1.5"/><line x1="140" y1="229" x2="140" y2="250" stroke="rgba(0,153,255,0.25)" stroke-width="1.5"/><line x1="175" y1="229" x2="175" y2="250" stroke="rgba(0,153,255,0.25)" stroke-width="1.5"/><path d="M220 80 Q230 70 240 80" stroke="rgba(0,153,255,0.5)" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M214 74 Q228 58 242 74" stroke="rgba(0,153,255,0.3)" stroke-width="1.5" fill="none" stroke-linecap="round"/><circle cx="228" cy="87" r="3" fill="rgba(0,153,255,0.65)"/></svg>"""

_V2_SVG_IRRIGATION = """<svg viewBox="0 0 280 280" fill="none" aria-hidden="true"><defs><linearGradient id="v2iG" x1="0" y1="0" x2="280" y2="280"><stop stop-color="#00C896" stop-opacity=".9"/><stop offset="1" stop-color="#0099FF" stop-opacity=".5"/></linearGradient><filter id="v2iGl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><line x1="140" y1="240" x2="140" y2="150" stroke="#00C896" stroke-width="2.5" stroke-linecap="round" opacity=".55"/><path d="M140 175 C140 175 115 160 112 140 C128 142 140 155 140 175Z" fill="rgba(0,200,150,0.16)" stroke="#00C896" stroke-width="1.8" stroke-linejoin="round" opacity=".8"/><path d="M140 155 C140 155 165 140 168 120 C152 122 140 135 140 155Z" fill="rgba(0,200,150,0.16)" stroke="#00C896" stroke-width="1.8" stroke-linejoin="round" opacity=".8"/><path d="M140 130 C140 130 155 110 152 92 C138 96 130 112 140 130Z" fill="rgba(0,200,150,0.2)" stroke="#00C896" stroke-width="1.8" stroke-linejoin="round" opacity=".8"/><rect x="115" y="225" width="50" height="18" rx="4" stroke="rgba(0,200,150,0.55)" stroke-width="1.5" fill="rgba(0,200,150,0.08)" filter="url(#v2iGl)"/><text x="140" y="239" text-anchor="middle" fill="rgba(0,200,150,0.65)" font-size="9" font-family="JetBrains Mono,monospace">SOIL SENSOR</text><line x1="70" y1="243" x2="210" y2="243" stroke="rgba(0,200,150,0.18)" stroke-width="2" stroke-dasharray="4,4"/><ellipse cx="65" cy="80" rx="8" ry="11" fill="rgba(0,153,255,0.3)" stroke="rgba(0,153,255,0.55)" stroke-width="1.5"/><ellipse cx="88" cy="65" rx="6" ry="9" fill="rgba(0,153,255,0.22)" stroke="rgba(0,153,255,0.45)" stroke-width="1.2"/><ellipse cx="50" cy="55" rx="5" ry="7" fill="rgba(0,153,255,0.16)" stroke="rgba(0,153,255,0.35)" stroke-width="1"/><path d="M75 85 Q100 100 115 200" stroke="rgba(0,153,255,0.15)" stroke-width="1.5" fill="none" stroke-dasharray="3,4"/><rect x="175" y="155" width="80" height="52" rx="6" stroke="rgba(0,200,150,0.38)" stroke-width="1.5" fill="rgba(0,200,150,0.05)"/><text x="215" y="175" text-anchor="middle" fill="#00C896" font-size="9" font-family="Inter,sans-serif">Soil: 45%</text><text x="215" y="190" text-anchor="middle" fill="rgba(0,200,150,0.55)" font-size="9" font-family="Inter,sans-serif">Valve: OPEN</text><text x="215" y="201" text-anchor="middle" fill="rgba(0,200,150,0.38)" font-size="8" font-family="JetBrains Mono,monospace">Auto Mode</text></svg>"""

_V2_SVG_SECURITY = """<svg viewBox="0 0 280 280" fill="none" aria-hidden="true"><defs><linearGradient id="v2sG" x1="0" y1="0" x2="280" y2="280"><stop stop-color="#FF6B6B" stop-opacity=".9"/><stop offset="1" stop-color="#FFD54F" stop-opacity=".5"/></linearGradient><filter id="v2sGl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M140 30 L205 56 L205 116 C205 158 173 190 140 204 C107 190 75 158 75 116 L75 56 Z" stroke="url(#v2sG)" stroke-width="2.5" fill="rgba(255,107,107,0.06)" filter="url(#v2sGl)"/><path d="M110 116 L132 138 L170 96" stroke="#FF6B6B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/><path d="M70 200 Q75 180 90 170" stroke="rgba(255,107,107,0.28)" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M58 215 Q65 185 88 168" stroke="rgba(255,107,107,0.18)" stroke-width="1.5" fill="none" stroke-linecap="round"/><path d="M45 230 Q55 190 86 165" stroke="rgba(255,107,107,0.1)" stroke-width="1.5" fill="none" stroke-linecap="round"/><circle cx="75" cy="200" r="12" stroke="rgba(255,107,107,0.48)" stroke-width="1.5" fill="rgba(255,107,107,0.08)"/><circle cx="75" cy="200" r="5" fill="rgba(255,107,107,0.4)"/><rect x="185" y="170" width="68" height="56" rx="8" stroke="rgba(255,107,107,0.38)" stroke-width="1.5" fill="rgba(255,107,107,0.05)"/><text x="219" y="192" text-anchor="middle" fill="#FF6B6B" font-size="9" font-family="Inter,sans-serif" font-weight="600">ALERT</text><text x="219" y="207" text-anchor="middle" fill="rgba(255,107,107,0.55)" font-size="8" font-family="JetBrains Mono,monospace">Motion: YES</text><text x="219" y="218" text-anchor="middle" fill="rgba(255,107,107,0.38)" font-size="8" font-family="Inter,sans-serif">SMS Sent</text><circle cx="219" cy="232" r="4" fill="#FF6B6B" opacity=".75"/></svg>"""

_V2_SVG_CLIMATE = """<svg viewBox="0 0 280 280" fill="none" aria-hidden="true"><defs><linearGradient id="v2cG" x1="0" y1="0" x2="280" y2="280"><stop stop-color="#A855F7" stop-opacity=".9"/><stop offset="1" stop-color="#0099FF" stop-opacity=".5"/></linearGradient><filter id="v2cGl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M50 150 L140 60 L230 150 L230 240 L50 240 Z" stroke="url(#v2cG)" stroke-width="2.5" fill="rgba(168,85,247,0.05)" stroke-linejoin="round" filter="url(#v2cGl)"/><rect x="118" y="200" width="44" height="40" rx="3" stroke="rgba(168,85,247,0.38)" stroke-width="1.5" fill="rgba(168,85,247,0.05)"/><rect x="72" y="175" width="36" height="30" rx="3" stroke="rgba(168,85,247,0.32)" stroke-width="1.5" fill="rgba(168,85,247,0.07)"/><line x1="90" y1="175" x2="90" y2="205" stroke="rgba(168,85,247,0.25)" stroke-width="1"/><line x1="72" y1="190" x2="108" y2="190" stroke="rgba(168,85,247,0.25)" stroke-width="1"/><rect x="172" y="175" width="36" height="30" rx="3" stroke="rgba(168,85,247,0.32)" stroke-width="1.5" fill="rgba(168,85,247,0.07)"/><line x1="190" y1="175" x2="190" y2="205" stroke="rgba(168,85,247,0.25)" stroke-width="1"/><line x1="172" y1="190" x2="208" y2="190" stroke="rgba(168,85,247,0.25)" stroke-width="1"/><rect x="104" y="120" width="72" height="50" rx="8" stroke="rgba(168,85,247,0.48)" stroke-width="1.5" fill="rgba(168,85,247,0.08)"/><text x="140" y="143" text-anchor="middle" fill="#A855F7" font-size="16" font-weight="700" font-family="JetBrains Mono,monospace">22°C</text><text x="140" y="159" text-anchor="middle" fill="rgba(168,85,247,0.55)" font-size="9" font-family="Inter,sans-serif">AUTO · COOL</text><circle cx="35" cy="75" r="4" fill="rgba(168,85,247,0.48)"/><circle cx="245" cy="75" r="4" fill="rgba(0,153,255,0.48)"/><text x="35" y="65" text-anchor="middle" fill="rgba(168,85,247,0.38)" font-size="8" font-family="Inter,sans-serif">WiFi</text><text x="245" y="65" text-anchor="middle" fill="rgba(0,153,255,0.38)" font-size="8" font-family="Inter,sans-serif">Cloud</text><line x1="35" y1="79" x2="55" y2="100" stroke="rgba(168,85,247,0.18)" stroke-width="1" stroke-dasharray="3,3"/><line x1="245" y1="79" x2="225" y2="100" stroke="rgba(0,153,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/></svg>"""


_V2_TRUST_ICON_PROJECTS = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 7h14M5 12h14M5 17h10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M4 4h16v16H4z" stroke="currentColor" stroke-width="1.8" rx="3"/></svg>'
_V2_TRUST_ICON_GUIDES = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 4h9a3 3 0 0 1 3 3v13H9a3 3 0 0 0-3-3V4Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 8h6M9 12h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
_V2_TRUST_ICON_COMPONENTS = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M4 10h3M4 14h3M17 10h3M17 14h3M10 4v3M14 4v3M10 17v3M14 17v3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
_V2_TRUST_ICON_FREE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 7 9 18l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_V2_TRUST_ICON_RESPONSIVE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="5" width="11" height="14" rx="2" stroke="currentColor" stroke-width="1.8"/><rect x="17" y="9" width="3" height="7" rx="1" stroke="currentColor" stroke-width="1.8"/><path d="M8 16h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
_V2_TRUST_ICON_HARDWARE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 8h8v8H8z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>'

_V2_TRUST_STRIP = """<div class="v2-trust-strip" aria-label="ESP32 Engine platform highlights">
  <div class="wrap v2-trust-strip-inner">
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_PROJECTS + """<strong>50+</strong><span>Projects</span></span>
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_GUIDES + """<strong>40+</strong><span>Guides</span></span>
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_COMPONENTS + """<strong>7</strong><span>Components</span></span>
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_FREE + """<strong>100%</strong><span>Free</span></span>
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_RESPONSIVE + """<span>Responsive</span></span>
    <span class="v2-trust-item">""" + _V2_TRUST_ICON_HARDWARE + """<span>Real Hardware</span></span>
  </div>
</div>"""


def home_v2_declaration() -> str:
    """Section 1 — Homepage v2: The Declaration (full-viewport hero)."""
    return f"""<section class="v2-declaration" aria-labelledby="v2-hero-heading">
  <div class="wrap v2-declaration-inner">
    <div class="v2-declaration-content reveal">
      <p class="v2-eyebrow">ESP32 Engine</p>
      <h1 id="v2-hero-heading" class="v2-declaration-headline">Build things that exist<br>in the real world.</h1>
      <p class="v2-declaration-sub">ESP32 Engine is where engineers, makers, and curious minds learn to build hardware that actually works.</p>
      <a class="v2-btn-hero" href="{site_href('learning.html')}">Start Building {_V2_ARROW_ICON}</a>
    </div>
    <div class="v2-declaration-visual" aria-hidden="true">
      <div class="v2-hero-visual-frame">
        {_V2_HERO_BOARD_SVG}
        {_V2_HERO_FLOAT_CARDS}
      </div>
    </div>
  </div>
</section>"""


def home_v2_proof() -> str:
    """Section 2 — Homepage v2: Proof of Possibility (full-bleed showcase, links to live projects)."""
    panels = [
        ("v2-panel-weather", _V2_SVG_WEATHER, "esp32-iot-weather-station", "Weather Station — ESP32 + DHT22"),
        ("v2-panel-irrigation", _V2_SVG_IRRIGATION, "esp32-smart-irrigation-system", "Smart Irrigation — Soil Sensor + Relay"),
        ("v2-panel-security", _V2_SVG_SECURITY, "esp32-motion-security-alert", "Motion Security — ESP32 + PIR"),
        ("v2-panel-climate", _V2_SVG_CLIMATE, "esp32-smart-thermostat", "Smart Thermostat — DHT22 + Relay"),
    ]
    panel_html = ""
    for cls, svg, slug, tag in panels:
        href = site_href(f"projects/{slug}.html")
        panel_html += (
            f'<a class="{cls} v2-showcase-panel v2-showcase-link" href="{esc(href)}" role="group" aria-label="{esc(tag)}">'
            f'<div class="v2-showcase-glow" aria-hidden="true"></div>'
            f'<div class="v2-showcase-illustration" aria-hidden="true">{svg}</div>'
            f'<div class="v2-showcase-info"><span class="v2-showcase-tag">{esc(tag)}</span></div>'
            f"</a>"
        )
    dots = "".join(
        f'<button class="v2-showcase-dot{" is-active" if i == 0 else ""}" '
        f'aria-label="Panel {i + 1}" data-panel="{i}"></button>'
        for i in range(len(panels))
    )
    return f"""<section class="v2-proof" aria-labelledby="v2-proof-heading">
  {_V2_TRUST_STRIP}
  <div class="v2-proof-header">
    <div class="wrap">
      <h2 id="v2-proof-heading" class="v2-proof-heading">What engineers build here.</h2>
    </div>
  </div>
  <div class="v2-showcase-track" id="v2-showcase-track" role="region" aria-label="Project showcase">{panel_html}</div>
  <div class="v2-showcase-dots" role="group" aria-label="Showcase navigation">{dots}</div>
</section>"""


def home_v2_engine(guides: list) -> str:
    """Section 3 — Homepage v2: The Engine (methodology)."""
    from guide_mission import mission_meta_badges_html  # noqa: F401 – kept for parity

    mission_guides = [g for g in guides if g.get("format") == "mission" or g.get("mission")]
    ordered = sorted(mission_guides or guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99)))[:3]

    pillars = [
        ("LEARN", "Focused Theory", "Only what you need for the next step — no filler, no detours."),
        ("BUILD", "A Guided Project", "Build something real from scratch, wire to final firmware."),
        ("SHIP", "A Working Circuit", "A physical project you understand completely. Ship it."),
    ]
    pillar_html = "".join(
        f'<div class="v2-pillar">'
        f'<p class="v2-pillar-label">{label}</p>'
        f'<h3 class="v2-pillar-title">{title}</h3>'
        f'<p class="v2-pillar-desc">{desc}</p>'
        f'</div>'
        for label, title, desc in pillars
    )

    arc_nodes = []
    milestone_positions = {1, 4, 8, 12}
    for i in range(1, 13):
        is_live = i <= len(ordered)
        is_milestone = i in milestone_positions
        label = f"Mission {i:02d}"
        if is_live:
            guide = ordered[i - 1]
            slug = guide["slug"]
            headline = (guide.get("headline") or guide.get("title", "")).split("|")[0].strip()
            short = (headline[:24] + "…") if len(headline) > 24 else headline
            href = site_href(f"guides/{slug}.html")
            arc_nodes.append(
                f'<a class="v2-arc-node is-milestone" href="{esc(href)}" title="{esc(headline)}">'
                f'<div class="v2-arc-dot"></div>'
                f'<span class="v2-arc-node-label">{esc(label)}</span>'
                f'</a>'
            )
        elif is_milestone:
            arc_nodes.append(
                f'<span class="v2-arc-node">'
                f'<div class="v2-arc-dot"></div>'
                f'<span class="v2-arc-node-label">{esc(label)}</span>'
                f'</span>'
            )
        else:
            arc_nodes.append('<span class="v2-arc-node"><div class="v2-arc-dot"></div></span>')

    return f"""<section class="v2-engine reveal" aria-labelledby="v2-engine-heading">
  <div class="wrap">
    <p class="v2-engine-eyebrow">How it works</p>
    <h2 id="v2-engine-heading" class="v2-engine-heading">Missions, not modules.</h2>
    <p class="v2-engine-sub">Every mission ends with something real you built. Not a quiz. Not a certificate. A working project.</p>
    <div class="v2-engine-pillars">{pillar_html}</div>
    <div class="v2-mission-arc">
      <p class="v2-arc-label-row">Mission path — start here, ship something every step</p>
      <div class="v2-arc-track">
        <div class="v2-arc-spine" aria-hidden="true"></div>
        {"".join(arc_nodes)}
      </div>
    </div>
  </div>
</section>"""


def home_v2_invitation() -> str:
    """Section 4 — Homepage v2: The Invitation (final CTA)."""
    return f"""<section class="v2-invitation" aria-labelledby="v2-invite-heading">
  <div class="wrap v2-invitation-inner reveal">
    <h2 id="v2-invite-heading" class="v2-invitation-heading">Your first project<br>ships in two hours.</h2>
    <p class="v2-invitation-sub">No prior experience needed.<br>A USB cable and curiosity are enough.</p>
    <div>
      <a class="v2-btn-invitation" href="{site_href('guides/blink-led-esp32.html')}">Start Mission 01 — Free {_V2_ARROW_ICON}</a>
    </div>
    <p class="v2-no-account">No account required to begin.</p>
  </div>
</section>"""


def home_v2_showcase_js() -> str:
    """Minimal inline JS for showcase drag-scroll and dot indicator (homepage only)."""
    return """<script>
(function(){
  var track=document.getElementById('v2-showcase-track');
  if(!track)return;
  var dots=document.querySelectorAll('.v2-showcase-dot');
  var panels=track.querySelectorAll('.v2-showcase-panel');
  function updateDots(){
    var idx=Math.round(track.scrollLeft/track.offsetWidth);
    dots.forEach(function(d,i){d.classList.toggle('is-active',i===idx);});
  }
  track.addEventListener('scroll',updateDots,{passive:true});
  dots.forEach(function(dot){
    dot.addEventListener('click',function(){
      var p=parseInt(dot.getAttribute('data-panel'),10);
      track.scrollTo({left:p*track.offsetWidth,behavior:'smooth'});
    });
  });
  var startX,startScroll,dragging=false;
  track.addEventListener('mousedown',function(e){startX=e.pageX;startScroll=track.scrollLeft;dragging=true;track.classList.add('is-dragging');});
  document.addEventListener('mousemove',function(e){if(!dragging)return;track.scrollLeft=startScroll-(e.pageX-startX);});
  document.addEventListener('mouseup',function(){dragging=false;track.classList.remove('is-dragging');});
})();
</script>"""


# ── Homepage v3 Constants ─────────────────────────────────────────────────

_V3_LED_SVG = """<svg viewBox="0 0 280 240" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="200" cy="168" r="60" fill="rgba(255,213,79,0.06)"/>
  <rect x="20" y="50" width="130" height="80" rx="8" fill="rgba(0,200,150,0.05)" stroke="rgba(0,200,150,0.3)" stroke-width="1.5"/>
  <rect x="55" y="70" width="60" height="40" rx="4" fill="rgba(0,200,150,0.12)" stroke="rgba(0,200,150,0.4)" stroke-width="1"/>
  <text x="85" y="94" text-anchor="middle" fill="rgba(0,200,150,0.75)" font-size="10" font-family="JetBrains Mono,monospace" font-weight="700">ESP32</text>
  <line x1="150" y1="75" x2="160" y2="75" stroke="rgba(0,200,150,0.5)" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="150" y1="90" x2="160" y2="90" stroke="rgba(0,200,150,0.5)" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="150" y1="105" x2="160" y2="105" stroke="rgba(0,200,150,0.5)" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M160 75 Q200 75 200 115" stroke="#FFD54F" stroke-width="2" stroke-dasharray="5,3" fill="none" stroke-linecap="round"/>
  <rect x="190" y="110" width="20" height="10" rx="3" fill="rgba(255,213,79,0.18)" stroke="#FFD54F" stroke-width="1.25"/>
  <line x1="200" y1="120" x2="200" y2="148" stroke="#FFD54F" stroke-width="2" stroke-dasharray="5,3" stroke-linecap="round"/>
  <path d="M160 105 Q245 105 245 168" stroke="rgba(255,255,255,0.12)" stroke-width="1.5" stroke-dasharray="4,3" fill="none" stroke-linecap="round"/>
  <circle cx="200" cy="168" r="34" fill="rgba(255,213,79,0.05)"/>
  <circle cx="200" cy="168" r="22" fill="rgba(255,213,79,0.09)"/>
  <circle cx="200" cy="168" r="13" fill="rgba(255,213,79,0.22)" stroke="#FFD54F" stroke-width="1.5"/>
  <circle cx="200" cy="168" r="6" fill="rgba(255,225,80,0.6)"/>
  <line x1="200" y1="155" x2="200" y2="148" stroke="#FFD54F" stroke-width="2" stroke-linecap="round"/>
  <line x1="200" y1="181" x2="200" y2="190" stroke="rgba(255,255,255,0.18)" stroke-width="1.5" stroke-linecap="round"/>
  <text x="164" y="73" fill="rgba(0,200,150,0.55)" font-size="7.5" font-family="JetBrains Mono,monospace">GPIO2</text>
  <text x="164" y="103" fill="rgba(255,255,255,0.2)" font-size="7.5" font-family="JetBrains Mono,monospace">GND</text>
  <text x="213" y="119" fill="rgba(255,213,79,0.55)" font-size="7.5" font-family="JetBrains Mono,monospace">220Ω</text>
  <text x="200" y="222" text-anchor="middle" fill="rgba(255,213,79,0.4)" font-size="8" font-family="JetBrains Mono,monospace" letter-spacing="2">● BLINK</text>
</svg>"""


def home_v3_journey() -> str:
    """Section 3 — Homepage v3: Choose Your Journey (row links, not cards). White bg."""
    PATHS = [
        {
            "num": "01", "level": "Beginner", "cls": "beginner",
            "title": "First Circuits",
            "desc": "Start from zero. Blink an LED, read a sensor, display data. No experience needed — just curiosity.",
            "meta": "3 missions · 10–15 min each",
            "href": "guides.html",
        },
        {
            "num": "02", "level": "Builder", "cls": "intermediate",
            "title": "Real Projects",
            "desc": "Build weather stations, robots, access control, and IoT dashboards with wiring tables and Arduino code.",
            "meta": "50 projects · 3 difficulty levels",
            "href": "projects.html",
        },
        {
            "num": "03", "level": "Engineer", "cls": "advanced",
            "title": "Advanced Systems",
            "desc": "IoT dashboards, TinyML on-device AI, automated control systems, and production-grade firmware.",
            "meta": "5+ IoT builds · Advanced concepts",
            "href": "learning.html",
        },
    ]
    arrow = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    rows = "".join(
        f'<li><a class="v3-journey-row" href="{esc(p["href"])}">'
        f'<span class="v3-journey-num">{p["num"]}</span>'
        f'<span class="v3-journey-badge v3-journey-badge-{p["cls"]}">{esc(p["level"])}</span>'
        f'<span class="v3-journey-body">'
        f'<span class="v3-journey-title">{esc(p["title"])}</span>'
        f'<span class="v3-journey-desc">{esc(p["desc"])}</span>'
        f'</span>'
        f'<span class="v3-journey-meta">{esc(p["meta"])}</span>'
        f'<span class="v3-journey-arrow">{arrow}</span>'
        f'</a></li>'
        for p in PATHS
    )
    return f"""<section class="v3-journey reveal" aria-label="Choose Your Learning Journey">
  <div class="wrap">
    <header class="v3-journey-header">
      <p class="v3-journey-eyebrow">Choose Your Journey</p>
      <h2 class="v3-journey-heading">Three paths.<br>One destination: maker.</h2>
    </header>
    <ul class="v3-journey-list">{rows}</ul>
  </div>
</section>"""


def home_v3_roadmap(guides: list) -> str:
    """Section 4 — Homepage v3: Learning Roadmap (LEARN/BUILD/SHIP + mission arc). Off-white bg."""
    mission_guides = [g for g in guides if g.get("format") == "mission" or g.get("mission")]
    ordered = sorted(mission_guides or guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99)))[:3]

    PILLARS = [
        ("01", "Learn", "Only what you need for the next step — focused theory through guided missions, not textbook chapters."),
        ("02", "Build", "Build something real from wire to firmware. Every project ends with a working circuit you fully understand."),
        ("03", "Ship", "Go beyond the breadboard — publish data to the web, add a display, and grow toward connected devices."),
    ]
    pillar_html = "".join(
        f'<div class="v3-roadmap-pillar">'
        f'<p class="v3-roadmap-pillar-num">{num}</p>'
        f'<h3 class="v3-roadmap-pillar-title">{title}</h3>'
        f'<p class="v3-roadmap-pillar-desc">{esc(desc)}</p>'
        f'</div>'
        for num, title, desc in PILLARS
    )

    arc_nodes = []
    milestone_positions = {1, 4, 8, 12}
    for i in range(1, 13):
        is_live = i <= len(ordered)
        is_milestone = i in milestone_positions
        label = f"Mission {i:02d}"
        if is_live:
            guide = ordered[i - 1]
            slug = guide["slug"]
            headline = (guide.get("headline") or guide.get("title", "")).split("|")[0].strip()
            href = site_href(f"guides/{slug}.html")
            arc_nodes.append(
                f'<a class="v3-arc-node is-live" href="{esc(href)}" title="{esc(headline)}">'
                f'<span class="v3-arc-dot"></span>'
                f'<span class="v3-arc-node-label">{esc(label)}</span>'
                f'</a>'
            )
        elif is_milestone:
            arc_nodes.append(
                f'<span class="v3-arc-node">'
                f'<span class="v3-arc-dot"></span>'
                f'<span class="v3-arc-node-label">{esc(label)}</span>'
                f'</span>'
            )
        else:
            arc_nodes.append('<span class="v3-arc-node"><span class="v3-arc-dot"></span></span>')

    cta_arrow = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f"""<section class="v3-roadmap reveal" aria-labelledby="v3-roadmap-heading">
  <div class="wrap">
    <p class="v3-roadmap-eyebrow">The Method</p>
    <h2 id="v3-roadmap-heading" class="v3-roadmap-heading">Learn. Build. Ship.</h2>
    <p class="v3-roadmap-sub">Every project on ESP32 Engine follows a three-phase progression — from understanding the parts to shipping something real.</p>
    <div class="v3-roadmap-pillars">{pillar_html}</div>
    <div class="v3-roadmap-separator"></div>
    <div class="v3-roadmap-arc-header">
      <span class="v3-roadmap-arc-title">Mission Track — 12 missions planned</span>
      <a class="v3-roadmap-arc-cta" href="/guides.html">Explore all guides {cta_arrow}</a>
    </div>
    <div class="v3-arc-track">
      <div class="v3-arc-spine" aria-hidden="true"></div>
      {"".join(arc_nodes)}
    </div>
  </div>
</section>"""


def home_v3_top_picks(projects: list, guides: list, components: list) -> str:
    """Section — Top 3 projects, guides, and components from live catalog."""
    arrow = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

    def project_rows():
        rows = []
        for p in _pick_by_slug(projects, TOP_PROJECT_SLUGS):
            desc = p.get("description") or p.get("desc") or ""
            if len(desc) > 88:
                desc = desc[:85].rstrip() + "…"
            feat = '<span class="v3-pick-badge">Featured</span>' if p.get("featured") else ""
            image = p.get("featured_image") or p.get("image") or ""
            image_html = ""
            if image:
                image_html = (
                    f'<span class="v3-pick-art" aria-hidden="true">'
                    f'<img src="{esc(image)}" alt="" loading="lazy" decoding="async"></span>'
                )
            rows.append(
                f'<a class="v3-pick-row" href="{site_href(f"projects/{p["slug"]}.html")}">'
                f"{image_html}"
                f'<span class="v3-pick-row-main">'
                f'{feat}<strong>{esc(p["title"])}</strong>'
                f'<span class="v3-pick-row-desc">{esc(desc)}</span>'
                f"</span>"
                f'<span class="v3-pick-row-meta">{esc(short_category(p.get("category", "")))} {arrow}</span>'
                f"</a>"
            )
        return "".join(rows)

    def guide_rows():
        rows = []
        for g in _pick_by_slug(guides, TOP_GUIDE_SLUGS):
            title = (g.get("headline") or g.get("title", "")).split("|")[0].strip()
            desc = g.get("lead") or g.get("meta_description") or ""
            if len(desc) > 88:
                desc = desc[:85].rstrip() + "…"
            mission = ""
            if g.get("format") == "mission" or g.get("mission"):
                num = g.get("mission_number") or g.get("sort_order") or ""
                mission = f'<span class="v3-pick-badge">Mission {num}</span>' if num else '<span class="v3-pick-badge">Mission</span>'
            rows.append(
                f'<a class="v3-pick-row" href="{site_href(f"guides/{g["slug"]}.html")}">'
                f'<span class="v3-pick-row-main">'
                f'{mission}<strong>{esc(title)}</strong>'
                f'<span class="v3-pick-row-desc">{esc(desc)}</span>'
                f"</span>"
                f'<span class="v3-pick-row-meta">Guide {arrow}</span>'
                f"</a>"
            )
        return "".join(rows)

    def component_rows():
        rows = []
        for c in _pick_by_slug(components, TOP_COMPONENT_SLUGS):
            summary = c.get("summary") or ""
            if len(summary) > 88:
                summary = summary[:85].rstrip() + "…"
            rows.append(
                f'<a class="v3-pick-row" href="{site_href(f"components/{c["slug"]}.html")}">'
                f'<span class="v3-pick-row-main">'
                f'<strong>{esc(c.get("name", c["slug"]))}</strong>'
                f'<span class="v3-pick-row-desc">{esc(summary)}</span>'
                f"</span>"
                f'<span class="v3-pick-row-meta">{esc(c.get("category", "Component"))} {arrow}</span>'
                f"</a>"
            )
        return "".join(rows)

    return f"""<section class="v3-top-picks reveal" aria-labelledby="v3-top-picks-heading">
  <div class="wrap">
    <p class="v3-top-picks-eyebrow">Launch picks</p>
    <h2 id="v3-top-picks-heading" class="v3-top-picks-heading">Top projects, guides, and components</h2>
    <p class="v3-top-picks-sub">Hand-picked from the live catalog — start with any row below.</p>
    <div class="v3-top-picks-grid">
      <div class="v3-top-picks-col">
        <h3 class="v3-top-picks-col-title">Projects</h3>
        <div class="v3-pick-list">{project_rows()}</div>
        <a class="v3-top-picks-more" href="{site_href("projects.html")}">All projects {arrow}</a>
      </div>
      <div class="v3-top-picks-col">
        <h3 class="v3-top-picks-col-title">Guides</h3>
        <div class="v3-pick-list">{guide_rows()}</div>
        <a class="v3-top-picks-more" href="{site_href("guides.html")}">All guides {arrow}</a>
      </div>
      <div class="v3-top-picks-col">
        <h3 class="v3-top-picks-col-title">Components</h3>
        <div class="v3-pick-list">{component_rows()}</div>
        <a class="v3-top-picks-more" href="{site_href("components.html")}">All components {arrow}</a>
      </div>
    </div>
  </div>
</section>"""


def home_v3_mission_feature(guides: list) -> str:
    """Section 5 — Homepage v3: Featured Mission (Mission 01 spotlight). Blue-teal gradient bg."""
    mission_guides = [g for g in guides if g.get("format") == "mission" or g.get("mission")]
    ordered = sorted(mission_guides or guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99)))
    featured = ordered[0] if ordered else None
    slug = featured["slug"] if featured else "blink-led-esp32"
    headline = (featured.get("headline") or featured.get("title", "Blink an LED with ESP32")).split("|")[0].strip() if featured else "Blink an LED with ESP32"
    lead = (featured.get("lead") or "Your first real ESP32 project — one LED, a few wires, and code you write yourself.") if featured else "Your first real ESP32 project — one LED, a few wires, and code you write yourself."
    time_label = (featured.get("reading_time") or "10–15 min") if featured else "10–15 min"
    href = site_href(f"guides/{slug}.html")
    BUILD_POINTS = [
        "A working LED circuit on a breadboard",
        "A blink program you write and fully understand",
        "The confidence and habits to tackle the next mission",
    ]
    build_items = "".join(f'<li class="v3-mission-build-item">{esc(b)}</li>' for b in BUILD_POINTS)
    arrow = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f"""<section class="v3-mission-feature reveal" aria-labelledby="v3-mission-feature-heading">
  <div class="wrap v3-mission-feature-inner">
    <div class="v3-mission-content">
      <div class="v3-mission-badges">
        <span class="v3-mission-pill v3-mission-pill-accent">Mission 01</span>
        <span class="v3-mission-pill">Beginner</span>
        <span class="v3-mission-pill">{esc(time_label)}</span>
      </div>
      <h2 id="v3-mission-feature-heading" class="v3-mission-feature-heading">{esc(headline)}</h2>
      <p class="v3-mission-feature-desc">{esc(lead)}</p>
      <ul class="v3-mission-build-list">{build_items}</ul>
      <a class="v3-btn-mission" href="{esc(href)}">Start Mission 01 {arrow}</a>
    </div>
    <div class="v3-mission-visual" aria-hidden="true">
      <div class="v3-mission-visual-frame">{_V3_LED_SVG}</div>
    </div>
  </div>
</section>"""


def home_v3_component_feature() -> str:
    """Section 6 — Homepage v3: Featured Component (BME280 spotlight). White bg."""
    SPECS = [
        ("Measures", "Temperature, humidity, and pressure"),
        ("Voltage", "3.3 V — direct ESP32 compatible"),
        ("Best for", "Weather stations, altitude tracking"),
    ]
    spec_items = "".join(
        f'<li class="v3-spec-item">'
        f'<span class="v3-spec-label">{esc(label)}</span>'
        f'<span class="v3-spec-value">{esc(val)}</span>'
        f'</li>'
        for label, val in SPECS
    )
    arrow = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f"""<section class="v3-component-feature reveal" aria-label="Featured Component: BME280">
  <div class="wrap v3-component-feature-inner">
    <div class="v3-component-image-panel">
      <img src="https://cdn-learn.adafruit.com/assets/assets/000/097/111/medium800/adafruit_products_BME280_top_angle.jpg"
           alt="BME280 environmental sensor breakout board"
           loading="lazy" width="200" height="200"/>
    </div>
    <div class="v3-component-content">
      <p class="v3-component-eyebrow">Featured Component</p>
      <h2 class="v3-component-name">BME280 Environmental Sensor</h2>
      <p class="v3-component-summary">One I2C chip reads temperature, humidity, and barometric pressure — the upgrade path when you want real weather data from a single module.</p>
      <ul class="v3-spec-list">{spec_items}</ul>
      <a class="v3-btn-component" href="/components/bme280.html">Learn about BME280 {arrow}</a>
    </div>
  </div>
</section>"""


def home_v3_project_feature() -> str:
    """Section 7 — Homepage v3: Featured Project (Weather Station spotlight). Dark bg."""
    LEVELS = [("Beginner", "is-beginner"), ("Intermediate", "is-intermediate"), ("Advanced", "is-advanced")]
    PARTS = ["ESP32 DevKit", "DHT22 Sensor", "220 Ω Resistor"]
    level_chips = "".join(
        f'<span class="v3-project-level-chip {cls}">{esc(lv)}</span>'
        for lv, cls in LEVELS
    )
    part_chips = "".join(
        f'<span class="v3-project-part">{esc(part)}</span>'
        for part in PARTS
    )
    arrow = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f"""<section class="v3-project-feature reveal" aria-label="Featured Project: ESP32 Weather Station">
  <div class="wrap v3-project-feature-inner">
    <div class="v3-project-visual" aria-hidden="true">
      <div class="v3-project-visual-frame">{_V2_SVG_WEATHER}</div>
    </div>
    <div class="v3-project-content">
      <p class="v3-project-eyebrow">Featured Project</p>
      <h2 class="v3-project-name">ESP32 Mini Weather Station</h2>
      <p class="v3-project-desc">Build a sensor that reads temperature and humidity — then displays live data on your screen. The same circuit used in classroom weather stations.</p>
      <div class="v3-project-levels">{level_chips}</div>
      <p style="font-size:0.8125rem;color:rgba(230,237,243,0.4);margin-bottom:0.75rem;text-transform:uppercase;letter-spacing:0.07em;font-weight:600;">Parts you’ll use</p>
      <div class="v3-project-parts">{part_chips}</div>
      <a class="v3-btn-project" href="/projects/esp32-iot-weather-station.html">Start this project {arrow}</a>
    </div>
  </div>
</section>"""


def home_v3_why() -> str:
    """Section 8 — Homepage v3: Why ESP32 Engine (statement rows, not icon cards). White bg."""
    REASONS = [
        ("Open forever", "No paywalls. No login required. No premium tier. Every guide, project, and component page is free."),
        ("Three levels every time", "Every project has Beginner, Intermediate, and Advanced stages — so you’re never stuck and never bored."),
        ("Built for parents", "Safety notes, simple explanations, and age-appropriate language. Designed for supervised learning from age 10+."),
        ("Ready for classrooms", "Structured missions, printable notes, and content aligned to hands-on STEM learning standards."),
        ("Works on any device", "Every page is mobile-first — follow a guide on your phone while you build at the bench."),
        ("Made for real making", "Every guide has wiring tables, copy-paste Arduino code, a troubleshooting section, and a real working output."),
    ]
    rows = "".join(
        f'<li class="v3-why-row">'
        f'<p class="v3-why-statement">{esc(stmt)}</p>'
        f'<p class="v3-why-detail">{esc(detail)}</p>'
        f'</li>'
        for stmt, detail in REASONS
    )
    return f"""<section class="v3-why reveal" aria-labelledby="v3-why-heading">
  <div class="wrap">
    <header class="v3-why-header">
      <p class="v3-why-eyebrow">Why ESP32 Engine</p>
      <h2 id="v3-why-heading" class="v3-why-heading">Built differently.<br>On purpose.</h2>
    </header>
    <ul class="v3-why-list">{rows}</ul>
  </div>
</section>"""


def home_v3_progress(
    project_count: int = 15, guide_count: int = 5, component_count: int = 7
) -> str:
    """Section 9 — Homepage v3: Community Progress (large stat numbers). Deep dark bg."""
    STATS = [
        (str(project_count), "Projects"),
        (str(guide_count), "Missions"),
        (str(component_count), "Components"),
        ("100%", "Free"),
    ]
    stats_html = "".join(
        f'<div class="v3-progress-stat">'
        f'<span class="v3-progress-num">{num}</span>'
        f'<span class="v3-progress-label">{esc(label)}</span>'
        f'</div>'
        for num, label in STATS
    )
    return f"""<section class="v3-progress reveal" aria-label="Platform Progress">
  <div class="wrap v3-progress-inner">
    <p class="v3-progress-eyebrow">Platform Today</p>
    <div class="v3-progress-grid">{stats_html}</div>
    <div class="v3-progress-divider"></div>
    <p class="v3-progress-note">More missions, projects, and components added every month.</p>
  </div>
</section>"""


def footer_html(base: str = "") -> str:
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <strong>{SITE_NAME}</strong>
      <p class="footer-tagline">{esc(SITE_TAGLINE)}</p>
      <p>The world's friendliest ESP32 learning platform — built for kids, trusted by parents, loved by makers.</p>
      <div class="footer-social">
        <a href="{esc(GITHUB_URL)}" rel="noopener noreferrer" target="_blank" aria-label="GitHub">{ICON_GITHUB}</a>
        <a href="{esc(YOUTUBE_URL)}" rel="noopener noreferrer" target="_blank" aria-label="YouTube">{ICON_YOUTUBE}</a>
      </div>
    </div>
    <div class="footer-col"><h4>Learn</h4><a href="{site_href('learning.html')}">Learning Paths</a><a href="{site_href('guides.html')}">Guides</a><a href="{site_href('components.html')}">Components</a><a href="{site_href('projects.html')}">Projects</a></div>
    <div class="footer-col"><h4>Resources</h4><a href="{site_href('parents.html')}">For Parents</a><a href="{site_href('teachers.html')}">For Teachers</a><a href="{site_href('downloads.html')}">Downloads</a><a href="{site_href('tools.html')}">Tools</a></div>
    <div class="footer-col"><h4>Company</h4><a href="{site_href('about.html')}">About</a><a href="{site_href('news.html')}">News</a><a href="{site_href('contact.html')}">Contact</a><a href="{site_href('privacy.html')}">Privacy</a></div>
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
