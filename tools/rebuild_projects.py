import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_icons import pick_icon, thumb_class as icon_thumb_class
from title_generator import generate_title

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
DOMAIN = "https://abdulmubeen7876773-dotcom.github.io/esp32"
CSS_VERSION = "20260615-titles"

LEAF_SVG = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 2C12 2 6 8 6 13a6 6 0 0012 0c0-5-6-11-6-11z" fill="#4C7A3D"/><path d="M12 13V21" stroke="#33531F" stroke-width="1.6" stroke-linecap="round"/></svg>'

ICON_CHIP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><line x1="9" y1="2" x2="9" y2="4"/><line x1="15" y1="2" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="22"/><line x1="15" y1="20" x2="15" y2="22"/></svg>'
ICON_DROP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 C12 2 6 10 6 15 a6 6 0 0012 0 C18 10 12 2 12 2z"/></svg>'
ICON_RELAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="10" rx="2"/><circle cx="8" cy="12" r="1.5" fill="currentColor" stroke="none"/><line x1="13" y1="12" x2="18" y2="12"/></svg>'
ICON_MOTOR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'
ICON_POWER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="16" height="10" rx="2"/><line x1="22" y1="10" x2="22" y2="14"/></svg>'
ICON_LEAF = ICON_DROP
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>'


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def first_match(pattern, text, flags=re.I | re.S):
    m = re.search(pattern, text, flags)
    if not m:
        return ""
    return (m.group(1) if m.lastindex else m.group(0)).strip()


def all_matches(pattern, text, flags=re.I | re.S):
    return [m.group(1).strip() for m in re.finditer(pattern, text, flags)]


def part_icon(name: str) -> str:
    n = name.lower()
    if "esp32" in n:
        return ICON_CHIP
    if any(k in n for k in ("sensor", "moisture", "dht", "pir", "bme", "ultrasonic", "microphone", "camera")):
        return ICON_DROP
    if "relay" in n:
        return ICON_RELAY
    if any(k in n for k in ("pump", "motor", "driver", "servo")):
        return ICON_MOTOR
    if "power" in n or "battery" in n or "supply" in n:
        return ICON_POWER
    if "led" in n:
        return ICON_LEAF
    return ICON_CHIP


def short_label(text: str, limit: int = 14) -> str:
    words = re.sub(r"[^A-Za-z0-9 ]", " ", text).split()
    if not words:
        return "SENSOR"
    label = " ".join(words[:3]).upper()
    return label[:limit]


def parse_project(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    tags = [t for t in all_matches(r'<span class="tag leaf">([^<]+)</span>', raw) if t.lower() not in ("part",)]
    clay_tags = all_matches(r'<span class="tag clay">([^<]+)</span>', raw)
    plain_tags = all_matches(r'<span class="tag">([^<]+)</span>', raw)
    category = tags[0] if tags else "ESP32"
    difficulty = clay_tags[0].replace(" build", "") if clay_tags else "Beginner"
    meta_m = re.search(r'<p class="article-meta">([^<]+)</p>', raw)
    if meta_m:
        parts = [p.strip() for p in meta_m.group(1).split("·")]
        if parts and parts[0] not in ("ESP32", "Project") and category in ("ESP32", ""):
            category = parts[0]
        if len(parts) > 1:
            difficulty = parts[1].replace(" build", "").strip()
    if category in ("ESP32", ""):
        bc = re.search(r'"position": 2, "name": "([^"]+)"', raw)
        if bc and bc.group(1) not in ("Home",):
            category = bc.group(1)
    project_tag = plain_tags[0] if plain_tags else "Project"
    title = first_match(r"<h1>([^<]+)</h1>", raw)
    lead = first_match(r'<p class="lead">([^<]+)</p>', raw) or first_match(r'<p class="article-lead">([^<]+)</p>', raw)
    overview = first_match(r'<section id="overview"[^>]*>.*?<p class="lead">([^<]+)</p>', raw)
    blog_section_match = first_match(r'<section id="blog"[\s\S]*?</section>', raw)
    if blog_section_match:
        blog_paras = all_matches(r"<p>([^<]+)</p>", blog_section_match)
    else:
        article = first_match(r'<div class="article-content">([\s\S]*?)</div>\s*</article>', raw)
        blog_paras = all_matches(r"<p>([^<]+)</p>", article) if article else []
    components = []
    comp_block = first_match(r'<section id="components"[\s\S]*?</section>', raw)
    if comp_block:
        for name in all_matches(r'<h3>([^<]+)</h3>', comp_block):
            if name.lower() not in ("applications", "advantages"):
                components.append(name)
    if not components:
        parts_block = first_match(r'<ul class="parts-list">([\s\S]*?)</ul>', raw)
        if parts_block:
            components = all_matches(r"<strong>([^<]+)</strong>", parts_block)
    wiring = []
    wire_block = first_match(r'<section id="wiring"[\s\S]*?</section>', raw)
    if not wire_block:
        wire_block = first_match(r'<table class="pin-table">([\s\S]*?)</table>', raw)
    if wire_block:
        for row in re.finditer(r"<tr><td>([^<]+)</td><td[^>]*>(?:<strong>)?([^<]+)(?:</strong>)?</td></tr>", wire_block):
            wiring.append((row.group(1).strip(), row.group(2).strip()))
    how = first_match(r'<section id="how"[\s\S]*?<div class="box"><p>([^<]+)</p>', raw)
    if not how:
        how = first_match(r'<div class="step"><span class="step-no">04</span>[\s\S]*?<p>([^<]+)</p>', raw)
    code = first_match(r'<pre id="code-content">([\s\S]*?)</pre>', raw)
    if not code:
        code = first_match(r"<section id=\"code\"[\s\S]*?<pre>([\s\S]*?)</pre>", raw)
    code = html.unescape(code.strip())
    apps_block = first_match(r'<h2>Applications</h2><ul[^>]*>([\s\S]*?)</ul>', raw)
    apps = all_matches(r"<li>([^<]+)</li>", apps_block) if apps_block else []
    adv_block = first_match(r'<h2>Advantages</h2><ul[^>]*>([\s\S]*?)</ul>', raw)
    advantages = all_matches(r"<li>([^<]+)</li>", adv_block) if adv_block else []
    future = []
    fut_block = first_match(r'<h2>Future improvements</h2>[\s\S]*?<div class="grid">([\s\S]*?)</div></section>', raw)
    if fut_block:
        future = all_matches(r"<h3>([^<]+)</h3>", fut_block)
    related = []
    rel_block = first_match(r'<h2>Related ESP32 projects</h2>[\s\S]*?<div class="grid">([\s\S]*?)</div></section>', raw)
    if not rel_block:
        rel_block = first_match(r'<h3>Related Projects</h3>[\s\S]*?<ul class="side-list">([\s\S]*?)</ul>', raw)
    if rel_block:
        for m in re.finditer(
            r'<a class="card" href="([^"]+)"><span class="tag leaf">([^<]+)</span><h3>([^<]+)</h3><p>([^<]+)</p></a>',
            rel_block,
        ):
            related.append({"href": m.group(1), "cat": m.group(2), "title": m.group(3), "desc": m.group(4)})
        for m in re.finditer(r'<a href="([^"]+)">([^<]+)</a>', rel_block):
            if not any(r["href"] == m.group(1) for r in related):
                related.append({"href": m.group(1), "cat": category, "title": m.group(2).strip(), "desc": ""})
    faq_q = first_match(r'<section id="faq"[\s\S]*?<h3>([^<]+)</h3>', raw)
    faq_a = first_match(r'<section id="faq"[\s\S]*?<h3>[^<]+</h3><p>([^<]+)</p>', raw)
    slug = first_match(r'<div class="meta">([^<]+)</div>', raw) or path.stem
    head = first_match(r"<head>([\s\S]*?)</head>", raw)
    head = re.sub(r'<link rel="stylesheet"[^>]*>', "", head)
    head = re.sub(r'<link rel="preconnect"[^>]*>', "", head)
    head = re.sub(r'<meta charset="utf-8">', "", head, flags=re.I)
    head = re.sub(r'<meta name="viewport"[^>]*>', "", head, flags=re.I)
    head = re.sub(r"\s+", " ", head).strip()
    sensor_pin = wiring[0][1] if wiring else "GPIO34"
    output_pin = wiring[1][1] if len(wiring) > 1 else "GPIO26"
    sensor_name = wiring[0][0] if wiring else "Sensor"
    output_name = wiring[1][0] if len(wiring) > 1 else "Output device"
    core_parts = len([c for c in components if c.lower() not in ("jumper wires", "breadboard", "5v power supply")])
    gpio_count = len([p for _, p in wiring if "gpio" in p.lower()])
    return {
        "path": path,
        "head": head,
        "category": category,
        "difficulty": difficulty,
        "project_tag": project_tag,
        "title": title,
        "lead": lead,
        "overview": overview or lead,
        "blog_paras": blog_paras[:3],
        "components": components,
        "wiring": wiring,
        "how": how,
        "code": code,
        "apps": apps[:5],
        "advantages": advantages[:5],
        "future": future[:4],
        "related": related[:3],
        "faq_q": faq_q or "Can this project work offline?",
        "faq_a": faq_a or "Yes. The core logic runs locally on the ESP32, so the project keeps working without Wi-Fi.",
        "slug": slug,
        "sensor_pin": sensor_pin,
        "output_pin": output_pin,
        "sensor_name": sensor_name,
        "output_name": output_name,
        "core_parts": max(core_parts, 3),
        "gpio_count": max(gpio_count, 2),
    }


def hero_diagram(d: dict) -> str:
    sensor = short_label(d["sensor_name"], 16)
    output = short_label(d["output_name"].replace(" control", ""), 12)
    return f"""
  <div class="diagram-wrap">
    <svg viewBox="0 0 1000 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Control loop diagram">
      <path d="M60 160 A70 70 0 0 1 130 90" stroke="#2C6E8E" stroke-width="9" fill="none" stroke-linecap="round"/>
      <path d="M130 90 A70 70 0 0 1 200 160" stroke="#B5703A" stroke-width="9" fill="none" stroke-linecap="round"/>
      <line class="needle" x1="130" y1="160" x2="130" y2="98" stroke="#202B1B" stroke-width="4" stroke-linecap="round"/>
      <circle cx="130" cy="160" r="6" fill="#202B1B"/>
      <text x="130" y="208" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" fill="#5C6A55">{esc(sensor)}</text>
      <path d="M220 160 L300 160" stroke="#C9D2BA" stroke-width="3" fill="none" stroke-dasharray="6 6"/>
      <circle class="pulse pulse-1" cx="220" cy="160" r="5" fill="#2C6E8E"/>
      <rect x="300" y="110" width="160" height="100" rx="10" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
      <text x="380" y="166" text-anchor="middle" font-family="Fraunces, serif" font-weight="700" font-size="22" fill="#33531F">ESP32</text>
      <circle class="esp-led" cx="442" cy="124" r="5" fill="#4C7A3D"/>
      <text x="380" y="190" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#5C6A55">CONTROL LOOP</text>
      <path d="M460 160 L560 160" stroke="#C9D2BA" stroke-width="3" fill="none" stroke-dasharray="6 6"/>
      <circle class="pulse pulse-2" cx="460" cy="160" r="5" fill="#E0A24A"/>
      <rect x="560" y="120" width="110" height="80" rx="10" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
      <circle class="relay-led" cx="650" cy="135" r="6" fill="#D6DCC9"/>
      <text x="615" y="168" text-anchor="middle" font-family="Fraunces, serif" font-weight="700" font-size="17" fill="#33531F">OUTPUT</text>
      <line class="power-wire" x1="670" y1="160" x2="745" y2="160" stroke="#C9D2BA" stroke-width="3"/>
      <rect x="745" y="125" width="90" height="70" rx="10" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
      <text x="790" y="167" text-anchor="middle" font-family="Fraunces, serif" font-weight="700" font-size="13" fill="#33531F">{esc(output)}</text>
      <circle class="drop drop1" cx="850" cy="160" r="5" fill="#2C6E8E"/>
      <circle class="drop drop2" cx="850" cy="160" r="5" fill="#2C6E8E"/>
      <circle class="drop drop3" cx="850" cy="160" r="5" fill="#2C6E8E"/>
      <g class="plant">
        <rect x="880" y="225" width="50" height="34" rx="4" fill="#B5703A"/>
        <path class="plant-leaf" d="M905 225 C905 200 875 195 870 175 C895 175 910 195 905 225 Z" fill="#7FA56B"/>
        <path class="plant-leaf" d="M905 225 C905 195 935 188 942 168 C915 170 900 192 905 225 Z" fill="#7FA56B"/>
        <line x1="905" y1="225" x2="905" y2="195" stroke="#33531F" stroke-width="3" stroke-linecap="round"/>
      </g>
    </svg>
    <div class="diagram-caption">
      <span><span class="dot"></span>Live loop — sense, decide, act</span>
      <span>Sensor → ESP32 → Output → Result</span>
    </div>
  </div>"""


def wiring_diagram(d: dict) -> str:
    s_pin = esc(d["sensor_pin"])
    o_pin = esc(d["output_pin"])
    return f"""
      <div class="wiring-diagram">
        <svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Wiring diagram">
          <rect x="130" y="40" width="140" height="160" rx="10" fill="#EAEFE2" stroke="#C9D2BA" stroke-width="2"/>
          <text x="200" y="125" text-anchor="middle" font-family="Fraunces, serif" font-weight="700" font-size="20" fill="#33531F">ESP32</text>
          <circle cx="130" cy="80" r="4" fill="#2C6E8E"/>
          <circle cx="130" cy="160" r="4" fill="#E0A24A"/>
          <text x="142" y="84" font-family="IBM Plex Mono, monospace" font-size="11" fill="#2C6E8E">{s_pin}</text>
          <text x="142" y="164" font-family="IBM Plex Mono, monospace" font-size="11" fill="#B5703A">{o_pin}</text>
          <line x1="60" y1="80" x2="130" y2="80" stroke="#2C6E8E" stroke-width="2" stroke-dasharray="5 4"/>
          <line x1="60" y1="160" x2="130" y2="160" stroke="#B5703A" stroke-width="2" stroke-dasharray="5 4"/>
          <rect x="10" y="55" width="60" height="50" rx="6" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
          <text x="40" y="84" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="9" fill="#202B1B">SENSOR</text>
          <rect x="10" y="135" width="60" height="50" rx="6" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
          <text x="40" y="164" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="9" fill="#202B1B">OUTPUT</text>
          <line x1="270" y1="120" x2="340" y2="120" stroke="#C9D2BA" stroke-width="2"/>
          <rect x="340" y="95" width="50" height="50" rx="6" fill="#F5F8EF" stroke="#C9D2BA" stroke-width="2"/>
          <text x="365" y="124" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#202B1B">5V</text>
        </svg>
      </div>"""


def build_steps(d: dict) -> str:
    how = d["how"] or "The ESP32 reads a sensor, compares the value to a threshold, and drives the output."
    return f"""
    <div class="steps">
      <div class="step"><span class="step-no">01</span><h3>Read</h3><p>The ESP32 samples the input sensor on {esc(d['sensor_pin'])}, producing a raw reading.</p></div>
      <div class="step"><span class="step-no">02</span><h3>Compare</h3><p>That reading is checked against a threshold configured in the sketch.</p></div>
      <div class="step"><span class="step-no">03</span><h3>Decide</h3><p>When the condition is met, the ESP32 sets {esc(d['output_pin'])} high; otherwise it stays low.</p></div>
      <div class="step"><span class="step-no">04</span><h3>Act</h3><p>{esc(how)}</p></div>
    </div>"""


def item_list(items: list[str], default_desc: str) -> str:
    rows = []
    for item in items:
        rows.append(
            f'<li><span class="ico">{ICON_LEAF}</span><span class="txt"><b>{esc(item)}</b><span>{esc(default_desc)}</span></span></li>'
        )
    return "\n".join(rows)


THUMB = {
    "Agriculture": "t-agriculture",
    "Home Automation": "t-home",
    "Security Projects": "t-security",
    "IoT Projects": "t-iot",
    "Sensor Projects": "t-iot",
    "Robotics": "t-default",
    "Industrial Automation": "t-default",
    "LED Projects": "t-led",
    "ESP32-CAM": "t-cam",
    "AI Projects": "t-ai",
    "Energy Monitoring": "t-default",
    "Healthcare": "t-default",
    "Environmental": "t-agriculture",
    "Smart City": "t-iot",
    "Education": "t-default",
}


def thumb_class(cat: str) -> str:
    return icon_thumb_class(cat)


def thumb_label(title: str, cat: str) -> str:
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title).split()
    short = " ".join(words[:3]).upper()
    return short[:20] or cat.upper()[:12]


def build_head(d: dict) -> str:
    url = f"{DOMAIN}/projects/{d['path'].name}"
    t = esc(d["title"])
    desc = esc(d["lead"])
    cat = esc(d["category"])
    return f"""<title>{t} | ESP32 Project Guide</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Article", "headline": "{t}", "description": "{desc}", "datePublished": "2026-06-14", "dateModified": "2026-06-14", "author": {{"@type": "Organization", "name": "ESP32 Project Library"}}, "mainEntityOfPage": {{"@type": "WebPage", "@id": "{url}"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{{"@type": "Question", "name": "{esc(d['faq_q'])}", "acceptedAnswer": {{"@type": "Answer", "text": "{esc(d['faq_a'])}"}}}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/index.html"}}, {{"@type": "ListItem", "position": 2, "name": "{cat}", "item": "{DOMAIN}/projects.html"}}, {{"@type": "ListItem", "position": 3, "name": "{t}", "item": "{url}"}}]}}</script>"""


def build_blog_paras(d: dict) -> list:
    t = d["title"]
    return [
        f"This tutorial explains how to build {t} from wiring to working firmware.",
        f"In this project, the ESP32 reads {d['sensor_name']} on {d['sensor_pin']} and drives {d['output_name']} on {d['output_pin']} when the threshold is crossed.",
        f"{t} is designed as a practical {d['category'].lower()} build you can test on a breadboard and later expand with Wi-Fi or cloud features.",
    ]


def assign_titles(all_data: list) -> None:
    from collections import defaultdict

    groups = defaultdict(list)
    for d in all_data:
        base = re.sub(r"-project-\d+$", "", d["slug"], flags=re.I)
        groups[base].append(d)
    used_global = set()
    for items in groups.values():
        items.sort(key=lambda x: int(re.search(r"project-(\d+)$", x["slug"], re.I).group(1)))
        for i, d in enumerate(items):
            d["title"] = generate_title(d, i, used_global)
            d["blog_paras"] = build_blog_paras(d)
            d["head"] = build_head(d)
            if d.get("code"):
                lines = d["code"].splitlines()
                if lines and lines[0].startswith("//"):
                    lines[0] = f"// {d['title']}"
                else:
                    lines.insert(0, f"// {d['title']}")
                d["code"] = "\n".join(lines)
    title_map = {d["slug"]: d["title"] for d in all_data}
    for d in all_data:
        for r in d.get("related", []):
            href_slug = Path(r["href"]).stem
            if href_slug in title_map:
                r["title"] = title_map[href_slug]


def rnt_header():
    return """<header class="site-header"><div class="wrap"><a class="site-logo" href="../index.html">ESP32 PROJECT LIBRARY</a><nav class="top-nav"><a href="../index.html">Home</a><a href="../projects.html">All Projects</a><a href="../sitemap.xml">Sitemap</a></nav></div></header>
<nav class="cat-bar"><div class="wrap"><a class="cat-pill" href="../index.html">HOME</a><a class="cat-pill" href="../projects.html#cat-agriculture">AGRICULTURE</a><a class="cat-pill" href="../projects.html#cat-iot-projects">IOT</a><a class="cat-pill" href="../projects.html#cat-esp32-cam">ESP32-CAM</a><a class="cat-pill" href="../projects.html#cat-home-automation">HOME AUTO</a><a class="cat-pill" href="../projects.html">ALL PROJECTS</a></div></nav>"""


def render_page(d: dict) -> str:
    tc = thumb_class(d["category"])
    icon = pick_icon(d["category"])
    parts_li = []
    for comp in d["components"]:
        if comp.lower() not in ("jumper wires", "breadboard"):
            parts_li.append(f"<li><strong>{esc(comp)}</strong></li>")
    wiring_rows = []
    for name, pin in d["wiring"]:
        wiring_rows.append(f"<tr><td>{esc(name)}</td><td><strong>{esc(pin)}</strong></td></tr>")
    related_side = []
    for r in d["related"]:
        related_side.append(f'<li><a href="{esc(r["href"])}">{esc(r["title"])}</a></li>')
    related_main = []
    for r in d["related"]:
        related_main.append(
            f'<li><a href="{esc(r["href"])}">{esc(r["title"])}</a> — {esc(r["desc"][:100])}…</li>'
        )
    blog_bits = "".join(f"<p>{esc(p)}</p>" for p in d["blog_paras"][:4])
    apps_li = "".join(f"<li>{esc(a)}</li>" for a in d["apps"])
    adv_li = "".join(f"<li>{esc(a)}</li>" for a in d["advantages"])
    future_li = "".join(f"<li>{esc(f)}</li>" for f in d["future"])
    code_fname = re.sub(r"[^a-z0-9]+", "_", d["slug"].lower()).strip("_")[:40] + ".ino"
    code_esc = esc(d["code"])
    how = d["how"] or "The ESP32 reads the sensor and drives the output when the threshold is met."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{d['head']}
<link rel="stylesheet" href="../style.css?v={CSS_VERSION}">
<style>html,body{{background:#0f172a;color:#e2e8f0}}</style>
</head>
<body>
{rnt_header()}
<div class="wrap article-shell">
  <aside class="sidebar-left">
    <h3>Learn ESP32</h3>
    <ul class="side-list">
      <li><a href="#overview">Project Overview</a></li>
      <li><a href="#parts">Parts Required</a></li>
      <li><a href="#wiring">Schematics</a></li>
      <li><a href="#code">Code</a></li>
      <li><a href="#demo">Demonstration</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
    <h3 style="margin-top:20px">Category</h3>
    <ul class="side-list"><li><a href="../projects.html#cat-{re.sub(r'[^a-z0-9]+', '-', d['category'].lower()).strip('-')}">{esc(d['category'])}</a></li></ul>
  </aside>
  <article class="article-main">
    <h1>{esc(d['title'])}</h1>
    <p class="article-meta">{esc(d['category'])} · {esc(d['difficulty'].replace(' build',''))} · {esc(d['project_tag'])}</p>
    <p class="article-lead">{esc(d['lead'])}</p>
    <div class="article-feature"><div class="article-thumb {tc}">{icon}</div></div>
    <div class="article-content">
      {blog_bits}
      <h2 id="overview">Project Overview</h2>
      <p>{esc(d['overview'])}</p>
      <ul>
        <li>The ESP32 connects to your circuit and reads the input sensor;</li>
        <li>Sensor values are compared against a threshold in the sketch;</li>
        <li>When the condition is met, the output device is activated on {esc(d['output_pin'])};</li>
        <li>The loop repeats while the board is powered.</li>
      </ul>
      <h2 id="parts">Parts Required</h2>
      <p>Here's a list of parts needed to build this project:</p>
      <ul class="parts-list">{''.join(parts_li)}</ul>
      <h2 id="wiring">Schematics</h2>
      <p>Follow the wiring connections below. Double-check GPIO pins before uploading the code.</p>
      <table class="pin-table"><thead><tr><th>Connection</th><th>Pin</th></tr></thead><tbody>{''.join(wiring_rows)}</tbody></table>
      <h2>How It Works</h2>
      {build_steps(d)}
      <h2 id="code">Code</h2>
      <p>Upload the following sketch to your ESP32 board using the Arduino IDE. Adjust pins and threshold for your hardware.</p>
      <div class="code-block"><div class="code-bar"><span>{esc(code_fname)}</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre id="code-content">{code_esc}</pre></div>
      <h2>Applications</h2>
      <ul>{apps_li}</ul>
      <h2>Advantages</h2>
      <ul>{adv_li}</ul>
      <h2>Future Improvements</h2>
      <ul>{future_li}</ul>
      <h2 id="demo">Demonstration</h2>
      <p>After uploading the code, open the Serial Monitor at 115200 baud. Verify that sensor readings change when you trigger the input condition. When the threshold is crossed, the output on {esc(d['output_pin'])} should activate — {esc(how)}</p>
      <h2>Wrapping Up</h2>
      <p>In this tutorial we've shown you how to build {esc(d['title'])}. You can use this pattern in your own ESP32 projects by changing the sensor, threshold, and output device.</p>
      <h2>Recommended Reading</h2>
      <ul>{''.join(related_main) if related_main else '<li><a href="../projects.html">Browse all ESP32 projects</a></li>'}</ul>
      <h2 id="faq">FAQ</h2>
      <div class="faq-list">
        <div class="faq-item open"><button class="faq-q" onclick="toggleFaq(this)">{esc(d['faq_q'])}<span class="plus">+</span></button><div class="faq-a"><p>{esc(d['faq_a'])}</p></div></div>
        <div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">How do I choose the threshold?<span class="plus">+</span></button><div class="faq-a"><p>Log raw readings in Serial Monitor, then pick a value between your normal and trigger readings.</p></div></div>
        <div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">Can this work without Wi-Fi?<span class="plus">+</span></button><div class="faq-a"><p>Yes. The core read-compare-act loop runs locally on the ESP32 without internet.</p></div></div>
      </div>
    </div>
  </article>
  <aside class="sidebar-right">
    <div class="promo-box"><strong>ESP32 Project Library</strong><p style="font-size:.88rem;color:#666;margin:.5em 0 0">1000 tutorials with wiring diagrams, code, and step-by-step guides.</p><p style="margin-top:10px"><a href="../projects.html">Browse all projects »</a></p></div>
    <h3>Related Projects</h3>
    <ul class="side-list">{''.join(related_side) if related_side else '<li><a href="../projects.html">All projects</a></li>'}</ul>
  </aside>
</div>
<footer class="site-footer"><div class="wrap footer-grid"><div class="footer-brand"><strong>ESP32 Project Library</strong><p>1000 ESP32 tutorials with wiring diagrams, source code, and step-by-step build guides.</p></div><div class="footer-col"><h4>Explore</h4><a href="../index.html">Home</a><a href="../projects.html">All Projects</a><a href="../sitemap.xml">Sitemap</a></div><div class="footer-col"><h4>Company</h4><a href="../about.html">About Us</a><a href="../contact.html">Contact</a><a href="../privacy.html">Privacy Policy</a><a href="../disclaimer.html">Disclaimer</a></div></div><div class="wrap footer-bottom"><p>© 2026 ESP32 Project Library. All rights reserved.</p></div></footer>
<script src="../project.js"></script>
</body>
</html>
"""


def main():
    files = sorted(PROJECTS.glob("*.html"))
    if not files:
        print("No project files found", file=sys.stderr)
        sys.exit(1)
    all_data = [parse_project(path) for path in files]
    assign_titles(all_data)
    for i, data in enumerate(all_data, 1):
        data["path"].write_text(render_page(data), encoding="utf-8")
        if i % 100 == 0:
            print(f"Rebuilt {i}/{len(all_data)}")
    print(f"Done — rebuilt {len(all_data)} project pages with unique titles")


if __name__ == "__main__":
    main()
