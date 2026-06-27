import html
import re
from pathlib import Path


def _first(pattern: str, text: str, flags=re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""


def _all(pattern: str, text: str, flags=re.I | re.S) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(pattern, text, flags)]


def parse_archive_page(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = _first(r"<title>([^<|]+)", raw)
    meta_description = _first(r'<meta name="description" content="([^"]+)"', raw)
    h1 = _first(r"<h1>([^<]+)</h1>", raw) or title
    lead = _first(r'<p class="article-lead">([^<]+)</p>', raw) or _first(
        r'<p class="lead">([^<]+)</p>', raw
    )
    overview_block = _first(r'(<section class="content-section" id="overview"[\s\S]*?</section>)', raw)
    overview_html = overview_block or _first(r'<div class="article-intro">([\s\S]*?)</div>', raw)
    parts = _all(r"<li><span>([^<]+)</span></li>", _first(r'<ul class="parts-grid">([\s\S]*?)</ul>', raw) or raw)
    wiring = []
    wire_section = _first(r'(<section class="content-section schematics-section" id="wiring"[\s\S]*?</section>)', raw)
    if wire_section:
        for row in re.finditer(
            r"<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]*)</td></tr>", wire_section
        ):
            wiring.append(
                {
                    "component": html.unescape(row.group(1).strip()),
                    "pin": html.unescape(row.group(2).strip()),
                    "note": html.unescape(row.group(3).strip()),
                }
            )
    code = _first(r'<pre class="level-code">([\s\S]*?)</pre>', raw)
    if not code:
        code = _first(r"<section[^>]*id=\"code\"[\s\S]*?<pre[^>]*>([\s\S]*?)</pre>", raw)
    code = html.unescape(code.strip()) if code else ""
    apps = _all(r'<section class="detail-panel"><h2>Applications</h2><ul class="detail-list"><li>([^<]+)</li>', raw)
    if not apps:
        apps_block = _first(r"<h2>Applications</h2><ul[^>]*>([\s\S]*?)</ul>", raw)
        if apps_block:
            apps = _all(r"<li>([^<]+)</li>", apps_block)
    upgrades = _all(r"<h2>Future Ideas</h2><ul class=\"detail-list\"><li>([^<]+)</li>", raw)
    faq = []
    faq_block = _first(r'(<section class="content-section" id="faq"[\s\S]*?</section>)', raw)
    if faq_block:
        for item in re.finditer(
            r'<button class="faq-q"[^>]*>([^<]+)<span class="plus">[\s\S]*?<div class="faq-a"><p>([^<]+)</p>',
            faq_block,
        ):
            faq.append({"question": item.group(1).strip(), "answer": item.group(2).strip()})
    category = _first(r'"position": 3, "name": "([^"]+)"', raw)
    if not category:
        category = _first(r'<li><a href="[^"]+#cat-[^"]+">([^<]+)</a></li>', raw)
    return {
        "title": h1,
        "meta_title": title,
        "meta_description": meta_description,
        "lead": lead,
        "category": category,
        "overview_html": overview_html,
        "components": parts,
        "wiring": wiring,
        "code": code,
        "apps": apps,
        "upgrades": upgrades,
        "faqs": faq,
    }
