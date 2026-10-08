"""Optional concise article sections shared by mission and component renderers."""
import re
from html import unescape
from site_layout import esc


def jump_links(body: str) -> str:
    """Build navigation only from sections actually rendered; headings take focus."""
    items = re.findall(r'<h2[^>]* id="([^"]+)"[^>]*>(.*?)</h2>', body, re.S)
    links = []
    for heading_id, heading in items:
        # Ignore decorative icons when deriving the accessible link name.
        heading = re.sub(r'<span[^>]*aria-hidden="true"[^>]*>.*?</span>', '', heading, flags=re.S)
        label = unescape(re.sub(r'<[^>]+>', '', heading)).strip()
        links.append(f'<a href="#{esc(heading_id)}">{esc(label)}</a>')
    return '<details class="article-contents"><summary>Jump to a section</summary><nav class="article-jump-links" aria-label="On this page">' + ''.join(links) + '</nav></details>'


def setup_section(setup: dict, css: str = "mission-section") -> str:
    if not setup:
        return ""
    rows = ''.join(f'<dt>{esc(item["label"])}</dt><dd>{esc(item["value"])}</dd>' for item in setup.get("items", []))
    return f'<section class="{css}" id="setup" aria-labelledby="setup-heading"><h2 id="setup-heading">Before you start</h2><dl class="article-setup">{rows}</dl></section>'


def examples_section(examples: list, css: str = "mission-section") -> str:
    # Import at call time to avoid a cycle with the guide renderer.
    from guide_mission import code_panel, _rich_content
    if not examples:
        return ""
    parts = []
    for example in examples:
        title = example.get("title", "Arduino example")
        parts.append(f'<h3>{esc(title)}</h3>' + _rich_content(example.get("wiring", "")) + code_panel(example) + _rich_content(example.get("notes", "")))
    return f'<section class="{css}" id="code" aria-labelledby="code-heading"><h2 id="code-heading">Wiring and matching Arduino code</h2>' + ''.join(parts) + '</section>'


def sources_section(sources: list, css: str = "mission-section") -> str:
    if not sources:
        return ""
    items = ''.join(f'<li><a href="{esc(item["url"])}">{esc(item["title"])}</a> — {esc(item["note"])}</li>' for item in sources)
    return f'<section class="{css}" id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Technical references</h2><ul>{items}</ul></section>'


def comparison_section(rows: list) -> str:
    if not rows:
        return ""
    labels = ["Setup / Arduino mode", "Resistor and button wiring", "Released", "Pressed"]
    head = ''.join(f'<th scope="col">{label}</th>' for label in labels)
    body = ''.join('<tr><th scope="row">' + esc(row["mode"]) + '</th>' + ''.join(f'<td>{esc(row[key])}</td>' for key in ("wiring", "default_state", "active_state")) + '</tr>' for row in rows)
    return '<section class="mission-section" id="input-comparison" aria-labelledby="input-comparison-heading"><h2 id="input-comparison-heading">Pull-up and pull-down wiring compared</h2><div class="wiring-table-wrap" tabindex="0" role="region" aria-label="Pull resistor comparison; scroll horizontally on small screens"><table class="wiring-table"><caption>GPIO27 with a normally open button; all supply connections are 3.3 V.</caption><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div></section>'


def prepare_article(body: str) -> str:
    """Give fragment targets focus and make wide tables keyboard-scrollable."""
    body = re.sub(r'<h2 id="([^"]+)"', r'<h2 tabindex="-1" id="\1"', body)
    body = body.replace('<pre class="code-block">', '<pre class="code-block" tabindex="0" role="region" aria-label="Arduino code; scroll horizontally if needed">')
    return body.replace('<div class="wiring-table-wrap">', '<div class="wiring-table-wrap" tabindex="0" role="region" aria-label="Scrollable data table">')
