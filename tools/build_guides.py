import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_guides
from site_layout import (
    OG_IMAGE,
    ORG_NAME,
    SITE_DOMAIN,
    SITE_NAME,
    breadcrumb_schema,
    canonical_url,
    esc,
    footer_html,
    head_html,
    header_html,
    itemlist_schema,
    json_ld_script,
    organization_schema,
    site_href,
    webpage_schema,
)

ROOT = Path(__file__).resolve().parent.parent
GUIDES_OUT = ROOT / "guides"
GUIDES_INDEX = ROOT / "guides.html"


def normalize_body(body: str) -> str:
    body = (body or "").strip()
    if not body:
        return ""
    if body.startswith("  "):
        return body
    return "\n".join(f"  {line}" if line.strip() else line for line in body.splitlines())


def sorted_guides(guides: list[dict]) -> list[dict]:
    return sorted(guides, key=lambda g: (g.get("phase", 99), g.get("sort_order", 99), g.get("slug", "")))


def guide_card_html(g: dict, compact: bool = False) -> str:
    slug = g["slug"]
    href = site_href(f"guides/{slug}.html")
    headline = g.get("headline") or g.get("title", "").split("|")[0].strip()
    desc = g.get("lead") or g.get("meta_description", "")
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "…"
    phase = g.get("phase")
    phase_badge = f'<span class="badge badge-cat">Phase {phase}</span>' if phase else ""
    reading = g.get("reading_time", "")
    meta = f'<span class="meta">{esc(reading)}</span>' if reading and not compact else ""
    cls = "guide-index-card" if not compact else "guide-home-card"
    return (
        f'<a class="{cls}" href="{esc(href)}">'
        f'<div class="guide-card-badges">{phase_badge}<span class="badge badge-beginner">{esc(g.get("proficiency_level", "Beginner"))}</span></div>'
        f"<h3>{esc(headline)}</h3>"
        f"<p>{esc(desc)}</p>"
        f'{meta}<span class="card-read-more">Read Guide<span aria-hidden="true">→</span></span></a>'
    )


def faq_section_html(faqs: list[dict]) -> str:
    items = []
    for item in faqs:
        q = item.get("question") or item.get("q", "")
        a = item.get("answer") or item.get("a", "")
        items.append(
            f'<div class="faq-item"><button type="button" class="faq-q">{esc(q)}<span class="plus">+</span></button>'
            f'<div class="faq-a"><p>{esc(a)}</p></div></div>'
        )
    return f"""  <h2 id="faqs">Frequently Asked Questions</h2>
  <div class="faq-list guide-faq">{"".join(items)}</div>"""


def related_section_html(related: list[dict]) -> str:
    if not related:
        return ""
    links = []
    for item in related:
        href = item.get("href", "")
        title = item.get("title", "")
        desc = item.get("description", "")
        desc_html = f'<span class="meta">{esc(desc)}</span>' if desc else ""
        links.append(f'<li><a href="{esc(href)}"><strong>{esc(title)}</strong></a> {desc_html}</li>')
    return f"""  <h2 id="related-guides">Related Guides</h2>
  <ul class="guide-related-list">{"".join(links)}</ul>"""


def guide_schema(guide: dict, faqs: list[dict]) -> str:
    slug = guide["slug"]
    path = f"guides/{slug}.html"
    url = canonical_url(path)
    title = guide.get("headline") or guide.get("title", "").split("|")[0].strip()
    desc = guide["meta_description"]
    faq_entities = []
    for item in faqs:
        q = item.get("question") or item.get("q", "")
        a = item.get("answer") or item.get("a", "")
        faq_entities.append(
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        )
    article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "datePublished": guide.get("date_published", "2026-06-18"),
        "dateModified": guide.get("date_modified", "2026-06-18"),
        "image": OG_IMAGE,
        "author": {"@type": "Organization", "name": ORG_NAME, "url": SITE_DOMAIN + "/"},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "proficiencyLevel": guide.get("proficiency_level", "Beginner"),
        "keywords": guide.get("keywords", "ESP32, microcontroller, IoT, Wi-Fi"),
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}
    crumbs = breadcrumb_schema(
        [
            ("Home", "/"),
            ("ESP32 Guides", "guides.html"),
            (title, path),
        ]
    )
    return organization_schema() + json_ld_script(article) + json_ld_script(faq) + crumbs


def guide_faq_script() -> str:
    return """<script>
document.querySelectorAll(".guide-faq .faq-q").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var item = btn.closest(".faq-item");
    if (!item) return;
    var open = item.classList.contains("open");
    item.closest(".faq-list").querySelectorAll(".faq-item.open").forEach(function(el) {
      el.classList.remove("open");
      var a = el.querySelector(".faq-a");
      if (a) a.style.display = "none";
    });
    item.classList.toggle("open", !open);
    var ans = item.querySelector(".faq-a");
    if (ans) ans.style.display = open ? "none" : "block";
  });
});
</script>"""


def render_guide(guide: dict) -> str:
    slug = guide["slug"]
    page_title = guide["title"]
    desc = guide["meta_description"]
    lead = guide.get("lead", desc)
    faqs = guide.get("faqs", [])
    related = guide.get("related_guides", [])
    body = normalize_body(guide.get("body_html", ""))
    canon = f"guides/{slug}.html"
    schema = guide_schema(guide, faqs)
    headline = guide.get("headline") or page_title.split("|")[0].strip()
    phase = guide.get("phase")
    phase_label = f"Phase {phase} · " if phase else ""
    breadcrumb = f"""  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('guides.html')}">Guides</a></li><li aria-current="page">{esc(headline)}</li></ol></nav>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", page_title, desc, canonical_path=canon, og_type="article", extra_schema=schema)}
</head>
<body>
<main>
{header_html("guides")}
<section class="section-block wrap page-head static-page guide-page">
{breadcrumb}
  <p class="hero-eyebrow">{esc(phase_label)}ESP32 Guide</p>
  <h1>{esc(headline)}</h1>
  <p class="article-lead">{esc(lead)}</p>
  <p class="meta guide-meta">{esc(guide.get("reading_time", "14 min read"))} · Updated {esc(guide.get("date_modified", "2026-06-18"))}</p>
{body}
{faq_section_html(faqs)}
  <h2 id="conclusion">Conclusion</h2>
  <p>{esc(guide.get("conclusion", ""))}</p>
{related_section_html(related)}
</section>
</main>
{footer_html()}
<script src="/ui.js" defer></script>
{guide_faq_script()}
</body>
</html>"""


def phase_section(phase: int, guides: list[dict]) -> str:
    phase_guides = [g for g in guides if g.get("phase") == phase]
    if not phase_guides:
        return ""
    cards = "".join(guide_card_html(g) for g in phase_guides)
    titles = {1: "Foundations", 2: "Development Setup"}
    subtitle = titles.get(phase, f"Phase {phase}")
    return f"""  <section class="guide-phase-block" id="phase-{phase}">
    <h2>Phase {phase} — {esc(subtitle)}</h2>
    <div class="guide-index-grid">{cards}</div>
  </section>"""


def render_guides_index(guides: list[dict]) -> str:
    guides = sorted_guides(guides)
    title = f"ESP32 Guides — Step-by-Step Learning | {SITE_NAME}"
    desc = (
        "Browse ESP32 Engine Phase 1 and Phase 2 guides — chip fundamentals, Arduino IDE setup, "
        "FAQs, and hands-on paths into our project tutorials."
    )
    list_items = [
        {
            "name": g.get("headline") or g.get("title", "").split("|")[0].strip(),
            "url": canonical_url(f"guides/{g['slug']}.html"),
        }
        for g in guides
    ]
    schema = (
        organization_schema()
        + webpage_schema(title, desc, "guides.html")
        + breadcrumb_schema([("Home", "/"), ("ESP32 Guides", "guides.html")])
        + itemlist_schema("ESP32 Engine Learning Guides", list_items)
    )
    phases_html = phase_section(1, guides) + phase_section(2, guides)
    body = f"""  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li aria-current="page">Guides</li></ol></nav>
  <p class="hero-eyebrow">Learning Path</p>
  <h1>ESP32 Guides</h1>
  <p class="article-lead">Start with Phase 1 fundamentals, complete Phase 2 tooling setup, then jump into hands-on project builds with wiring tables and staged difficulty levels.</p>
{phases_html}
  <p class="meta guide-index-footer"><a href="{site_href('projects.html')}">Browse all ESP32 projects →</a></p>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="guides.html", extra_schema=schema)}
</head>
<body>
<main>
{header_html("guides")}
<section class="section-block wrap page-head static-page guide-index-page">
{body}
</section>
</main>
{footer_html()}
<script src="/ui.js" defer></script>
</body>
</html>"""


def main():
    guides = load_guides()
    if not guides:
        print("No guides found in content/guides/")
        return
    GUIDES_OUT.mkdir(exist_ok=True)
    for guide in guides:
        slug = guide["slug"]
        out = GUIDES_OUT / f"{slug}.html"
        out.write_text(render_guide(guide), encoding="utf-8")
        print(f"Wrote guides/{slug}.html")
    GUIDES_INDEX.write_text(render_guides_index(guides), encoding="utf-8")
    print(f"Wrote guides.html ({len(guides)} articles)")


if __name__ == "__main__":
    main()
