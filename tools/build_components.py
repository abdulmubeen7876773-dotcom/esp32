import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store
from site_layout import (
    SITE_NAME,
    badge_class,
    breadcrumb_schema,
    esc,
    footer_html,
    head_html,
    header_html,
    json_ld_script,
    organization_schema,
    site_href,
    webpage_schema,
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

    img = c.get("image", "")
    img_html = f'<img src="{esc(img)}" alt="{esc(c["name"])}" loading="eager">' if img else f'<span style="font-size:5rem">{esc(c.get("icon", "🔌"))}</span>'

    specs = "".join(f"<li>{esc(s)}</li>" for s in c.get("specs", []))
    pins = "".join(f"<li>{esc(p)}</li>" for p in c.get("pins", []))
    apps = "".join(f"<li>{esc(a)}</li>" for a in c.get("applications", []))
    projects = "".join(
        f'<li><a href="{esc(p["href"])}">{esc(p["title"])}</a></li>' for p in c.get("related_projects", [])
    )
    guides = "".join(
        f'<li><a href="{esc(g["href"])}">{esc(g["title"])}</a></li>' for g in c.get("related_guides", [])
    )
    faqs = c.get("faqs", [])
    faq_html = ""
    if faqs:
        items = "".join(
            f'<div class="faq-item"><button type="button" class="faq-q">{esc(f["question"])}<span class="plus">+</span></button>'
            f'<div class="faq-a"><p>{esc(f["answer"])}</p></div></div>'
            for f in faqs
        )
        faq_html = f'<h2 id="faq">FAQ</h2><div class="faq-list">{items}</div>'

    code = c.get("example_code", "").strip()
    code_html = f'<pre class="code-block"><code>{esc(code)}</code></pre>' if code else ""
    ds = c.get("datasheet_url", "")
    ds_html = f'<p><a class="btn btn-secondary" href="{esc(ds)}" rel="noopener noreferrer" target="_blank">Download Datasheet</a></p>' if ds else ""

    body = f"""<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('components.html')}">Components</a></li><li aria-current="page">{esc(c["name"])}</li></ol></nav>
<section class="component-hero wrap">
  <div><span class="badge badge-cat">{esc(c.get("category", ""))}</span> <span class="badge {badge_class(c.get("difficulty", "Beginner"))}">{esc(c.get("difficulty", "Beginner"))}</span>
  <h1>{esc(c["name"])}</h1>
  <p class="section-sub">{esc(c.get("summary", ""))}</p></div>
  <div class="component-hero-img">{img_html}</div>
</section>
<section class="wrap static-page">
  <div class="eli12-box"><h3>Explain Like I'm 12</h3><p>{esc(c.get("eli12", ""))}</p></div>
  <h2 id="specs">Specifications</h2><ul>{specs}</ul>
  <h2 id="pinout">Pinout &amp; Wiring</h2><ul>{pins}</ul>
  <h2 id="library">Library</h2><p>{esc(c.get("library", "Built-in Arduino"))}</p>
  <h2 id="code">Example Code</h2>{code_html}
  <h2 id="output">Expected Output</h2><p>{esc(c.get("output", ""))}</p>
  <h2 id="applications">Applications</h2><ul>{apps}</ul>
  {"<h2 id='projects'>Projects Using This Component</h2><ul>" + projects + "</ul>" if projects else ""}
  {"<h2 id='guides'>Related Guides</h2><ul>" + guides + "</ul>" if guides else ""}
  <h2 id="datasheet">Datasheet</h2>{ds_html}
  {faq_html}
</section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path=path, extra_schema=schema)}
</head>
<body>
<main>
{header_html("components")}
{body}
</main>
{footer_html()}
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
</body>
</html>"""


def component_card(c: dict) -> str:
    img = c.get("image", "")
    img_html = f'<img src="{esc(img)}" alt="{esc(c["name"])}" loading="lazy">' if img else f'<span style="font-size:3rem">{esc(c.get("icon", "🔌"))}</span>'
    return (
        f'<a class="component-card" href="{site_href(f"components/{c["slug"]}.html")}" data-category="{esc(c.get("category", ""))}">'
        f'<div class="component-card-img">{img_html}</div>'
        f'<div class="component-card-body">'
        f'<span class="badge badge-cat">{esc(c.get("category", ""))}</span>'
        f'<span class="badge {badge_class(c.get("difficulty", "Beginner"))}">{esc(c.get("difficulty", "Beginner"))}</span>'
        f'<h3>{esc(c["name"])}</h3>'
        f'<span class="btn btn-card">View Guide<span aria-hidden="true">→</span></span>'
        f"</div></a>"
    )


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
<script src="/search.js" defer></script>
<script src="/ui.js" defer></script>
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
