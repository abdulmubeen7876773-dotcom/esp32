import html
import re

from project_icons import pick_icon, thumb_class


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
    return f"""<a class="{card_class} modern-card" href="{esc(link)}"{extra_attrs}>{card_thumb_html(cat, thumb_cls)}<div class="card-body"><div class="card-badges"><span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge {badge_class(diff)}">{esc(diff.replace(' build',''))}</span></div><h3>{esc(p['title'])}</h3>{desc_html}<div class="card-footer"><span class="read-time">{read_time_label(diff, slug)}</span></div></div></a>"""


def stats_html() -> str:
    return """<section class="stats-bar wrap"><div class="stats-grid"><div class="stat-item"><strong>1000+ Projects</strong></div><div class="stat-item"><strong>50+</strong><span>Categories</span></div><div class="stat-item"><strong>100K+</strong><span>Monthly Readers</span></div><div class="stat-item"><strong>Beginner → Advanced</strong><span>Skill Levels</span></div></div></section>"""


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
