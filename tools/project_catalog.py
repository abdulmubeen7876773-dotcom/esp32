"""Project discovery presentation and fragment-only navigation migration."""
import re
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = '<link rel="stylesheet" href="/assets/project-catalog.css?v=20261019-reviewed">'


def category_browse(active=""):
    from cms_loader import load_categories
    from project_icons import slug_cat
    categories = load_categories()
    # The catalog, rather than aliases for radio technologies, defines destinations.
    links = ''.join(f'<a href="/category/{slug_cat(c)}.html"' + (' aria-current="page"' if slug_cat(c) == active else '') + f'>{escape(c)}</a>' for c in categories)
    return f'<details class="catalog-categories" id="browse-categories"><summary>Browse topic collections</summary><nav aria-label="Project topic collections">{links}</nav></details>'


def category_layout(body):
    canonical = re.search(r'<link rel="canonical" href="https://esp32engine.com/category/([^"/]+)\.html"', body)
    browse = category_browse(canonical[1] if canonical else '')
    body = re.sub(r'<details class="catalog-categories".*?</details>', browse, body, flags=re.S)
    body = re.sub(r'<aside class="sidebar-categories".*?</aside>', browse, body, flags=re.S)
    body = re.sub(r'<link rel="stylesheet" href="/assets/project-catalog\.css[^"]*">', STYLE, body)
    if STYLE not in body:
        body = body.replace('</head>', STYLE + '\n</head>')
    return body


def listing_html(cat_opts, page_projects, page, total_pages, total_count, text_index=''):
    from site_layout import head_html, header_html, footer_html, pagination_head_links, pagination_nav_html, projects_page_path, projects_page_canonical, SEARCH_JS_SRC, UI_JS_SRC, organization_schema, website_schema
    from rebuild_index import parent_grid_card, parent_listing_record, project_json_record
    from content_store import get_content_store
    from project_text import public_projects
    topics = sorted({p['category'] for p in public_projects(get_content_store().projects())})
    options = ''.join(f'<option value="{escape(c)}">{escape(c)}</option>' for c in topics)
    cards = ''.join(re.sub(r'<span class="badge badge-time">.*?</span>', '', parent_grid_card(p)) for p in page_projects)
    # Interactive filters need the entire library even when static HTML spans pages.
    # Keep paginated cards as the no-JavaScript and malformed-data fallback.
    catalog_data = ''
    if total_pages > 1:
        records = [project_json_record(parent_listing_record(p))
                   for p in public_projects(get_content_store().projects())]
        payload = json.dumps(records, ensure_ascii=False).replace('<', '\\u003c')
        catalog_data = f'<script type="application/json" id="project-catalog-data">{payload}</script>'
    title = f'ESP32 Projects: {total_count} Practical Tutorials | ESP32 Engine' + (f' — Page {page}' if total_pages > 1 else '')
    description = 'Choose an ESP32 project by topic and difficulty. Browse existing builds, compare their requirements and follow the linked tutorials.'
    return f'''<!DOCTYPE html>
<html lang="en"><head>{head_html('',title,description,canonical_path=projects_page_canonical(page),extra_schema=organization_schema()+website_schema())}
{pagination_head_links(page,total_pages,projects_page_path)}{STYLE}</head>
<body class="projects-page catalog-page"><main>{header_html('projects',project_count=total_count)}
<section class="catalog-intro wrap"><p class="catalog-eyebrow">Choose your next build</p><h1>ESP32 projects</h1><p>Explore practical builds by topic and difficulty. Open a tutorial to check its parts, wiring and supported setup.</p></section>
<div class="wrap catalog-content"><section aria-label="Filter projects" class="catalog-filters">
<div class="catalog-controls"><label>Search projects<input id="q" type="search" placeholder="Try OLED, robot or weather"></label>
<label>Topic<select id="cat"><option value="">All topics</option>{options}</select></label>
<label>Difficulty<select id="diff"><option value="">All difficulties</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></label>
<label>Sort<select id="sort"><option value="featured">Featured first</option><option value="title">A–Z</option><option value="category">Topic</option></select></label>
<button type="button" id="projects-reset">Clear filters</button></div><p id="count" role="status" aria-live="polite">{total_count} projects in the catalog</p></section>
<section aria-label="Project results"><div class="grid grid-projects" id="grid">{cards}</div>
<p id="projects-no-results" hidden>No projects match. Clear filters or try a different topic, difficulty or search word.</p>
<div class="section-actions" id="projects-more-wrap" hidden><button type="button" id="projects-load-more" class="btn">Load more</button></div>
{pagination_nav_html(page,total_pages,projects_page_path)}
<noscript><p>Search and filters need JavaScript. Browse the project cards and page links, or choose a topic collection below.</p></noscript></section>
{category_browse()}</div></main>{footer_html()}
{catalog_data}<script src="/project-icons.js" defer></script><script src="{SEARCH_JS_SRC}" defer></script><script src="{UI_JS_SRC}" defer></script><script src="/projects.js?v=20261024-catalog-pages" defer></script></body></html>'''


def generate_navigation_scope():
    """Refresh discovery pages, then migrate only verified navigation fragments."""
    import rebuild_index as listing
    from content_store import get_content_store
    from project_text import public_projects
    from site_layout import sidebar_categories_html
    records = [listing.parent_listing_record(p) for p in public_projects(get_content_store().projects())]
    listing.write_project_listing_pages(records, '', '')
    (ROOT/'index.html').write_text(listing.home_html(records),encoding='utf-8')
    changed = []
    paths = list(ROOT.glob('*.html'))
    for directory in ('guides','projects','components','category'):
        paths.extend((ROOT/directory).glob('*.html'))
    for path in paths:
        before = path.read_text(encoding='utf-8'); after = before
        def nav(match):
            return re.sub(r'<a\b[^>]*>Advanced Projects</a>', '', match[0])
        after = re.sub(r'<nav class="top-nav".*?</nav>',nav,after,flags=re.S)
        if path.parent.name == 'category':
            after = category_layout(after)
        else:
            after = re.sub(r'<aside class="sidebar-categories".*?</aside>',lambda m: sidebar_categories_html(''),after,flags=re.S)
        if before != after:
            path.write_text(after,encoding='utf-8'); changed.append(path.relative_to(ROOT).as_posix())
    print('Navigation-only outputs: ' + ', '.join(changed))
