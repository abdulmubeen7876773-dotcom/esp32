import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from component_page import component_all_faqs, component_card_html, render_component_page
from content_store import get_content_store
from site_layout import (
    SITE_NAME,
    breadcrumb_schema,
    esc,
    footer_html,
    head_html,
    header_html,
    json_ld_script,
    organization_schema,
    site_href,
    webpage_schema,
    UI_JS_SRC,
    SEARCH_JS_SRC,
)

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_OUT = ROOT / "components"
INDEX_OUT = ROOT / "components.html"


def faq_schema(faqs: list) -> str:
    if not faqs:
        return ""
    entities = []
    for item in faqs:
        q = item.get("question", "")
        a = item.get("answer", "")
        entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json_ld_script({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities})


def component_page_html(c: dict, prev_component: dict | None = None, next_component: dict | None = None) -> str:
    slug = c["slug"]
    path = f"components/{slug}.html"
    title = f"{c['name']} — Component Guide | {SITE_NAME}"
    desc = c.get("summary", "")
    crumbs = breadcrumb_schema([("Home", "/"), ("Components", "components.html"), (c["name"], path)])
    article = json_ld_script(
        {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": c["name"],
            "description": desc,
            "dateModified": c.get("date_modified", "2026-07-05"),
            "author": {"@type": "Person", "name": "Abdul Mubeen", "url": "https://esp32engine.com/author.html"},
            "reviewedBy": {
                "@type": "Organization",
                "name": "ESP32 Engine Editorial Team",
                "url": "https://esp32engine.com/editorial-policy.html",
            },
            "publisher": {"@type": "Organization", "name": "ESP32 Engine", "url": "https://esp32engine.com/"},
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://esp32engine.com/{path}"},
            "proficiencyLevel": c.get("difficulty", "Beginner"),
        }
    )
    schema = organization_schema() + webpage_schema(title, desc, path) + crumbs + article + faq_schema(component_all_faqs(c))
    head = head_html("", title, desc, canonical_path=path, extra_schema=schema)
    return render_component_page(
        c,
        head=head,
        header=header_html("components"),
        footer=footer_html(),
        prev_component=prev_component,
        next_component=next_component,
    )


def component_card(c: dict) -> str:
    return component_card_html(c)


def index_html(components: list, categories: list) -> str:
    title = f"Component Encyclopedia | {SITE_NAME}"
    desc = "8 ESP32 components explained simply — ESP32 DevKit, ESP32-CAM, DHT22, BME280, HC-SR04, PIR sensor, relay module, and OLED display. Wiring diagrams and example code included."
    crumbs = breadcrumb_schema([("Home", "/"), ("Components", "components.html")])
    schema = organization_schema() + webpage_schema(title, desc, "components.html") + crumbs
    used_categories = []
    for c in components:
        cat = c.get("category", "")
        if cat and cat not in used_categories:
            used_categories.append(cat)
    pills = "".join(f'<button type="button" class="category-pill" data-filter="{esc(cat)}">{esc(cat)}</button>' for cat in used_categories)
    cards = "".join(component_card(c) for c in components)
    featured = "".join(component_card(c) for c in components[:3])
    category_count = len(used_categories)
    component_count = len(components)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="components.html", extra_schema=schema)}
</head>
<body class="components-index-page">
<main>
{header_html("components")}
<section class="components-hero-shell">
  <div class="wrap components-hero-grid">
    <div class="components-hero-copy">
  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li aria-current="page">Components</li></ol></nav>
  <h1>Component Encyclopedia</h1>
  <p class="section-sub">What is it? How do I connect it? What can I build? Every part explained simply.</p>
      <div class="components-hero-stats">
        <span><strong>{component_count}</strong><small>Components</small></span>
        <span><strong>{category_count}</strong><small>Categories</small></span>
        <span><strong>3.3 V</strong><small>ESP32 focus</small></span>
      </div>
    </div>
    <div class="components-hero-art">
      <img src="/assets/images/heroes/components-hero.webp" alt="ESP32 components and classroom electronics kits on desks" width="1024" height="576" loading="eager" decoding="async" style="width:100%;height:100%;min-height:300px;object-fit:cover;display:block;">
    </div>
  </div>
</section>
<section class="section-block wrap components-explorer">
  <div class="components-featured">
    <div>
      <p class="section-eyebrow">Featured starting points</p>
      <h2>Start with the parts every ESP32 builder uses.</h2>
    </div>
    <div class="components-featured-grid">{featured}</div>
  </div>
  <div class="components-filter-shell" aria-label="Component filters">
    <label class="components-search"><span>Search components</span><input id="component-search" type="search" placeholder="Search sensors, displays, relays..." autocomplete="off"></label>
    <div class="category-pills"><button type="button" class="category-pill is-active" data-filter="">All</button>{pills}</div>
    <p class="filter-meta meta" id="component-count">{component_count} components</p>
  </div>
  <div class="grid grid-projects" id="component-grid">{cards}</div>
</section>
</main>
{footer_html()}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
<script>
var activeComponentCategory = '';
var componentSearch = document.getElementById('component-search');
var componentCount = document.getElementById('component-count');
function applyComponentFilters() {{
  var q = componentSearch ? componentSearch.value.trim().toLowerCase() : '';
  var shown = 0;
  document.querySelectorAll('#component-grid .component-card').forEach(function(card) {{
    var matchesCategory = !activeComponentCategory || card.dataset.category === activeComponentCategory;
    var haystack = ((card.dataset.name || '') + ' ' + (card.dataset.summary || '') + ' ' + (card.dataset.category || '')).toLowerCase();
    var matchesSearch = !q || haystack.indexOf(q) !== -1;
    var show = matchesCategory && matchesSearch;
    card.style.display = show ? '' : 'none';
    if (show) shown += 1;
  }});
  if (componentCount) componentCount.textContent = shown + (shown === 1 ? ' component' : ' components');
}}
document.querySelectorAll('.category-pill').forEach(function(btn) {{
  btn.addEventListener('click', function() {{
    document.querySelectorAll('.category-pill').forEach(function(b) {{ b.classList.remove('is-active'); }});
    btn.classList.add('is-active');
    activeComponentCategory = btn.dataset.filter || '';
    applyComponentFilters();
  }});
}});
if (componentSearch) componentSearch.addEventListener('input', applyComponentFilters);
</script>
</body>
</html>"""


def main():
    store = get_content_store()
    components = store.components()
    categories = store.component_categories()
    COMPONENTS_OUT.mkdir(exist_ok=True)
    for i, c in enumerate(components):
        out = COMPONENTS_OUT / f"{c['slug']}.html"
        prev_component = components[i - 1] if i > 0 else None
        next_component = components[i + 1] if i + 1 < len(components) else None
        out.write_text(component_page_html(c, prev_component, next_component), encoding="utf-8")
        print(f"Wrote components/{c['slug']}.html")
    INDEX_OUT.write_text(index_html(components, categories), encoding="utf-8")
    print(f"Wrote components.html ({len(components)} components)")


if __name__ == "__main__":
    main()
