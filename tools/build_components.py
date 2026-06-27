import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from component_page import component_card_html, render_component_page
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


def component_page_html(c: dict) -> str:
    slug = c["slug"]
    path = f"components/{slug}.html"
    title = f"{c['name']} — Component Guide | {SITE_NAME}"
    desc = c.get("summary", "")
    crumbs = breadcrumb_schema([("Home", "/"), ("Components", "components.html"), (c["name"], path)])
    schema = organization_schema() + webpage_schema(title, desc, path) + crumbs + faq_schema(c.get("faqs", []))
    head = head_html("", title, desc, canonical_path=path, extra_schema=schema)
    return render_component_page(c, head=head, header=header_html("components"), footer=footer_html())


def component_card(c: dict) -> str:
    return component_card_html(c)


def index_html(components: list, categories: list) -> str:
    title = f"Component Encyclopedia | {SITE_NAME}"
    desc = "Explore ESP32 components — sensors, displays, motors, and more. Simple explanations, wiring diagrams, and example code."
    crumbs = breadcrumb_schema([("Home", "/"), ("Components", "components.html")])
    schema = organization_schema() + webpage_schema(title, desc, "components.html") + crumbs
    pills = "".join(f'<button type="button" class="category-pill" data-filter="{esc(cat)}">{esc(cat)}</button>' for cat in categories)
    cards = "".join(component_card(c) for c in components)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="components.html", extra_schema=schema)}
</head>
<body>
<main>
{header_html("components")}
<section class="section-block wrap page-head">
  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li aria-current="page">Components</li></ol></nav>
  <h1>Component Encyclopedia</h1>
  <p class="section-sub">What is it? How do I connect it? What can I build? Every part explained simply.</p>
  <div class="category-pills"><button type="button" class="category-pill is-active" data-filter="">All</button>{pills}</div>
  <div class="grid grid-projects" id="component-grid">{cards}</div>
</section>
</main>
{footer_html()}
<script src="{SEARCH_JS_SRC}" defer></script>
<script src="{UI_JS_SRC}" defer></script>
<script>
document.querySelectorAll('.category-pill').forEach(function(btn) {{
  btn.addEventListener('click', function() {{
    document.querySelectorAll('.category-pill').forEach(function(b) {{ b.classList.remove('is-active'); }});
    btn.classList.add('is-active');
    var cat = btn.dataset.filter;
    document.querySelectorAll('#component-grid .component-card').forEach(function(card) {{
      card.style.display = !cat || card.dataset.category === cat ? '' : 'none';
    }});
  }});
}});
</script>
</body>
</html>"""


def main():
    store = get_content_store()
    components = store.components()
    categories = store.component_categories()
    COMPONENTS_OUT.mkdir(exist_ok=True)
    for c in components:
        out = COMPONENTS_OUT / f"{c['slug']}.html"
        out.write_text(component_page_html(c), encoding="utf-8")
        print(f"Wrote components/{c['slug']}.html")
    INDEX_OUT.write_text(index_html(components, categories), encoding="utf-8")
    print(f"Wrote components.html ({len(components)} components)")


if __name__ == "__main__":
    main()
