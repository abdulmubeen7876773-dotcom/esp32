import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store
from guide_mission import mission_index_card, render_friendly_intro, render_mission_guide
from site_layout import (
    OG_IMAGE,
    ORG_NAME,
    SITE_DOMAIN,
    SITE_NAME,
    badge_class,
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


def is_mission_guide(guide: dict) -> bool:
    return guide.get("format") == "mission" or bool(guide.get("mission"))


def legacy_guide_card_html(g: dict) -> str:
    slug = g["slug"]
    href = site_href(f"guides/{slug}.html")
    headline = g.get("headline") or g.get("title", "").split("|")[0].strip()
    desc = g.get("lead") or g.get("meta_description", "")
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "…"
    reading = g.get("reading_time", "")
    return (
        f'<a class="guide-index-card reference-guide-card" href="{esc(href)}">'
        f'<span class="badge badge-reference">Reference Guide</span>'
        f'<span class="badge {badge_class(g.get("proficiency_level", "Beginner"))}">{esc(g.get("proficiency_level", "Beginner"))}</span>'
        f"<h3>{esc(headline)}</h3>"
        f"<p>{esc(desc)}</p>"
        f'<span class="meta">{esc(reading)}</span>'
        f'<span class="card-read-more">Read Guide<span aria-hidden="true">→</span></span></a>'
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
    for item in (guide.get("mission") or {}).get("quiz", []):
        faq_entities.append(
            {
                "@type": "Question",
                "name": item.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.get("explanation", item.get("options", [""])[int(item.get("correct", 0))]),
                },
            }
        )
    article = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "learningResourceType": "Mission",
        "headline": title,
        "description": desc,
        "datePublished": guide.get("date_published", "2026-06-26"),
        "dateModified": guide.get("date_modified", "2026-06-26"),
        "image": OG_IMAGE,
        "author": {"@type": "Organization", "name": ORG_NAME, "url": SITE_DOMAIN + "/"},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "proficiencyLevel": guide.get("proficiency_level", "Beginner"),
        "keywords": guide.get("keywords", "ESP32, learning, mission"),
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities} if faq_entities else ""
    crumbs = breadcrumb_schema(
        [
            ("Home", "/"),
            ("Guides", "guides.html"),
            (title, path),
        ]
    )
    schema = organization_schema() + json_ld_script(article) + crumbs
    if faq:
        schema += json_ld_script(faq)
    return schema


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


def render_legacy_guide(guide: dict) -> str:
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
    breadcrumb = f"""  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('guides.html')}">Guides</a></li><li aria-current="page">{esc(headline)}</li></ol></nav>"""
    intro = render_friendly_intro(guide, is_mission=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", page_title, desc, canonical_path=canon, og_type="article", extra_schema=schema)}
</head>
<body class="reference-guide-page">
<main>
{header_html("guides")}
<section class="section-block wrap page-head static-page guide-page">
{breadcrumb}
  <p class="hero-eyebrow">Background reading</p>
  <h1>{esc(headline)}</h1>
  <p class="article-lead">{esc(lead)}</p>
  <p class="meta guide-meta">{esc(guide.get("reading_time", "14 min read"))} · Updated {esc(guide.get("date_modified", "2026-06-26"))}</p>
{intro}
  <div class="guide-technical-content">
{body}
  </div>
{faq_section_html(faqs)}
  <h2 id="conclusion">Conclusion</h2>
  <p>{esc(guide.get("conclusion", ""))}</p>
{related_section_html(related)}
</section>
</main>
{footer_html()}
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
{guide_faq_script()}
</body>
</html>"""


def render_mission_page(guide: dict) -> str:
    slug = guide["slug"]
    page_title = guide["title"]
    desc = guide["meta_description"]
    lead = guide.get("lead", desc)
    canon = f"guides/{slug}.html"
    schema = guide_schema(guide, guide.get("faqs", []))
    headline = guide.get("headline") or page_title.split("|")[0].strip()
    breadcrumb = f"""<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('guides.html')}">Guides</a></li><li aria-current="page">{esc(headline)}</li></ol></nav>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", page_title, desc, canonical_path=canon, og_type="article", extra_schema=schema)}
</head>
<body class="mission-guide-page">
<main>
{header_html("guides")}
<section class="section-block wrap mission-guide-shell">
{breadcrumb}
  <p class="hero-eyebrow">Interactive Mission</p>
  <h1>{esc(headline)}</h1>
  <p class="article-lead">{esc(lead)}</p>
{render_mission_guide(guide)}
</section>
</main>
{footer_html()}
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
<script src="/mission-guide.js" defer></script>
</body>
</html>"""


def render_guide(guide: dict) -> str:
    if is_mission_guide(guide):
        return render_mission_page(guide)
    return render_legacy_guide(guide)


def render_guides_index(guides: list[dict]) -> str:
    guides = sorted_guides(guides)
    missions = [g for g in guides if is_mission_guide(g)]
    legacy = [g for g in guides if not is_mission_guide(g)]
    title = f"ESP32 Missions — Learn by Building | {SITE_NAME}"
    desc = (
        "Step-by-step ESP32 missions for kids and beginners. Each guide is a journey — "
        "story, wiring, code, quiz, and your next challenge."
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
        + breadcrumb_schema([("Home", "/"), ("Guides", "guides.html")])
        + itemlist_schema("ESP32 Engine Missions", list_items)
    )
    mission_cards = "".join(mission_index_card(g) for g in missions)
    missions_html = ""
    if missions:
        missions_html = f"""  <section class="guide-missions-block" id="missions">
    <h2>Mission Journeys</h2>
    <p class="section-sub">{len(missions)} hands-on missions with stories, safety tips, wiring, code, and quizzes — start here if you're new.</p>
    <div class="mission-index-grid">{mission_cards}</div>
  </section>"""
    legacy_html = ""
    if legacy:
        legacy_cards = "".join(legacy_guide_card_html(g) for g in legacy)
        legacy_html = f"""  <section class="guide-phase-block" id="reference">
    <h2>Reference Guides</h2>
    <p class="section-sub">{len(legacy)} background articles for deeper reading after your first missions.</p>
    <div class="guide-index-grid reference-guide-grid">{legacy_cards}</div>
  </section>"""
    body = f"""  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li aria-current="page">Guides</li></ol></nav>
  <p class="hero-eyebrow">Learn by doing</p>
  <h1>ESP32 Learning Guides</h1>
  <p class="article-lead">Start with Mission Journeys — fun step-by-step builds for kids and beginners. Reference Guides are here when you want extra background.</p>
  <p class="guide-count-summary meta">{len(missions)} mission journeys · {len(legacy)} reference guides</p>
{missions_html}
{legacy_html}
  <p class="meta guide-index-footer"><a href="{site_href('learning.html')}">View learning paths →</a> · <a href="{site_href('projects.html')}">Browse projects →</a></p>"""
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
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
</body>
</html>"""


def main():
    guides = get_content_store().guides()
    if not guides:
        print("No guides found in content/guides/")
        return
    GUIDES_OUT.mkdir(exist_ok=True)
    for guide in guides:
        slug = guide["slug"]
        out = GUIDES_OUT / f"{slug}.html"
        out.write_text(render_guide(guide), encoding="utf-8")
        kind = "mission" if is_mission_guide(guide) else "legacy"
        print(f"Wrote guides/{slug}.html ({kind})")
    GUIDES_INDEX.write_text(render_guides_index(guides), encoding="utf-8")
    print(f"Wrote guides.html ({len(guides)} guides)")


if __name__ == "__main__":
    main()
