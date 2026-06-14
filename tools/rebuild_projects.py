import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
DOMAIN = "https://abdulmubeen7876773-dotcom.github.io/esp32"

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
    tags = all_matches(r'<span class="tag leaf">([^<]+)</span>', raw)
    clay_tags = all_matches(r'<span class="tag clay">([^<]+)</span>', raw)
    plain_tags = all_matches(r'<span class="tag">([^<]+)</span>', raw)
    category = tags[0] if tags else "ESP32"
    difficulty = clay_tags[0] if clay_tags else "Beginner"
    project_tag = plain_tags[0] if plain_tags else "Project"
    title = first_match(r"<h1>([^<]+)</h1>", raw)
    lead = first_match(r'<p class="lead">([^<]+)</p>', raw)
    overview = first_match(r'<section id="overview"[^>]*>.*?<p class="lead">([^<]+)</p>', raw)
    blog_section_match = first_match(r'<section id="blog"[\s\S]*?</section>', raw)
    blog_paras = all_matches(r"<p>([^<]+)</p>", blog_section_match) if blog_section_match else []
    components = []
    comp_block = first_match(r'<section id="components"[\s\S]*?</section>', raw)
    if comp_block:
        for name in all_matches(r'<h3>([^<]+)</h3>', comp_block):
            if name.lower() not in ("applications", "advantages"):
                components.append(name)
    wiring = []
    wire_block = first_match(r'<section id="wiring"[\s\S]*?</section>', raw)
    if wire_block:
        for row in re.finditer(r"<tr><td>([^<]+)</td><td[^>]*>([^<]+)</td></tr>", wire_block):
            wiring.append((row.group(1).strip(), row.group(2).strip()))
    how = first_match(r'<section id="how"[\s\S]*?<div class="box"><p>([^<]+)</p>', raw)
    code = first_match(r"<section id=\"code\"[\s\S]*?<pre>([\s\S]*?)</pre>", raw)
    code = html.unescape(code.strip())
    apps_block = first_match(r'<h2>Applications</h2><ul class="list">([\s\S]*?)</ul>', raw)
    apps = all_matches(r"<li>([^<]+)</li>", apps_block) if apps_block else []
    adv_block = first_match(r'<h2>Advantages</h2><ul class="list">([\s\S]*?)</ul>', raw)
    advantages = all_matches(r"<li>([^<]+)</li>", adv_block) if adv_block else []
    future = []
    fut_block = first_match(r'<h2>Future improvements</h2>[\s\S]*?<div class="grid">([\s\S]*?)</div></section>', raw)
    if fut_block:
        future = all_matches(r"<h3>([^<]+)</h3>", fut_block)
    related = []
    rel_block = first_match(r'<h2>Related ESP32 projects</h2>[\s\S]*?<div class="grid">([\s\S]*?)</div></section>', raw)
    if rel_block:
        for m in re.finditer(
            r'<a class="card" href="([^"]+)"><span class="tag leaf">([^<]+)</span><h3>([^<]+)</h3><p>([^<]+)</p></a>',
            rel_block,
        ):
            related.append({"href": m.group(1), "cat": m.group(2), "title": m.group(3), "desc": m.group(4)})
    faq_q = first_match(r'<section id="faq"[\s\S]*?<h3>([^<]+)</h3>', raw)
    faq_a = first_match(r'<section id="faq"[\s\S]*?<h3>[^<]+</h3><p>([^<]+)</p>', raw)
    slug = first_match(r'<div class="meta">([^<]+)</div>', raw) or path.stem
    head = first_match(r"<head>([\s\S]*?)</head>", raw)
    head = re.sub(r'<link rel="stylesheet"[^>]*>', "", head)
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


def render_page(d: dict) -> str:
    parts_html = []
    for comp in d["components"]:
        if comp.lower() in ("jumper wires", "breadboard"):
            continue
        desc = f"Connected according to the wiring map — part of the {esc(d['category'])} build."
        parts_html.append(
            f'<div class="part-row"><div class="part-icon">{part_icon(comp)}</div><div class="part-name">{esc(comp)}</div><div class="part-desc">{desc}</div></div>'
        )
    wiring_rows = []
    for name, pin in d["wiring"]:
        pin_class = "pin" if "gpio" in pin.lower() else ""
        wiring_rows.append(f"<tr><td>{esc(name)}</td><td class=\"{pin_class}\">{esc(pin)}</td><td>Signal / power</td></tr>")
    related_html = []
    for r in d["related"]:
        related_html.append(
            f'<a class="card" href="{esc(r["href"])}"><span class="tag leaf">{esc(r["cat"])}</span><h3>{esc(r["title"])}</h3><p>{esc(r["desc"])}</p></a>'
        )
    future_html = []
    for f in d["future"]:
        future_html.append(
            f'<div class="chip-card"><div class="chip-label">Next step</div><h3>{esc(f)}</h3><p>This can be added as a future enhancement to extend the project.</p></div>'
        )
    overview_p2 = d["blog_paras"][0] if d["blog_paras"] else d["overview"]
    code_fname = re.sub(r"[^a-z0-9]+", "_", d["slug"].lower()).strip("_")[:40] + ".ino"
    code_esc = esc(d["code"])
    blog_section = ""
    if len(d["blog_paras"]) > 1:
        blog_bits = "".join(f"<p>{esc(p)}</p>" for p in d["blog_paras"][1:])
        blog_section = f"""
  <section id="guide" class="wrap blog">
    <div class="section-head"><h2>Complete project blog guide</h2><p>300–600 word SEO article included for this project page.</p></div>
    {blog_bits}
  </section>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{d['head']}
<link rel="stylesheet" href="../style.css">
</head>
<body>

<nav>
  <div class="nav-inner wrap">
    <a class="brand" href="../index.html">{LEAF_SVG}ESP32 Project Library</a>
    <div class="nav-links">
      <a href="#overview">Overview</a>
      <a href="#components">Components</a>
      <a href="#wiring">Wiring</a>
      <a href="#how-it-works">How it works</a>
      <a href="#code">Code</a>
      <a href="#applications">Applications</a>
      <a href="#future">Future</a>
      <a href="#faq">FAQ</a>
    </div>
  </div>
</nav>

<header class="hero wrap">
  <div class="hero-tags">
    <span class="tag leaf">{esc(d['category'])}</span>
    <span class="tag clay">{esc(d['difficulty'])} build</span>
    <span class="tag">{esc(d['project_tag'])}</span>
  </div>
  <h1>{esc(d['title'])}</h1>
  <p class="lead">{esc(d['lead'])}</p>
  <p style="margin-top:24px"><a class="btn light" href="../index.html">← Back to library</a></p>
  {hero_diagram(d)}
</header>

<main>

  <section id="overview" class="wrap">
    <div class="section-head"><h2>Overview</h2></div>
    <div class="overview-grid">
      <div>
        <p>{esc(d['overview'])}</p>
        <p>{esc(overview_p2)}</p>
      </div>
      <div class="stat-row">
        <div class="stat"><div class="v">{esc(d['category'])}</div><div class="k">Category</div></div>
        <div class="stat"><div class="v">{esc(d['difficulty'])}</div><div class="k">Difficulty</div></div>
        <div class="stat"><div class="v">{d['core_parts']}</div><div class="k">Core parts</div></div>
        <div class="stat"><div class="v">{d['gpio_count']}</div><div class="k">GPIO pins used</div></div>
      </div>
    </div>
  </section>
{blog_section}
  <section id="components" class="wrap">
    <div class="section-head"><h2>Components required</h2><p>Core hardware needed for this ESP32 build.</p></div>
    <div class="parts-list">{''.join(parts_html)}</div>
  </section>

  <section id="wiring" class="wrap">
    <div class="section-head"><h2>Wiring connections</h2><p>Follow these signal and power connections carefully.</p></div>
    <div class="wiring-grid">
      <table class="pin-table">
        <thead><tr><th>Component</th><th>ESP32 pin</th><th>Signal type</th></tr></thead>
        <tbody>{''.join(wiring_rows)}</tbody>
      </table>
      {wiring_diagram(d)}
    </div>
  </section>

  <section id="how-it-works" class="wrap">
    <div class="section-head"><h2>How it works</h2><p>One loop, repeated continuously while the board is powered.</p></div>
    {build_steps(d)}
  </section>

  <section id="code" class="wrap">
    <div class="section-head"><h2>Source code</h2><p>Starting code from the dataset — adjust pins and threshold for your exact hardware.</p></div>
    <div class="code-block">
      <div class="code-bar"><span class="fname">{esc(code_fname)}</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div>
      <pre id="code-content">{code_esc}</pre>
    </div>
  </section>

  <section id="applications" class="wrap">
    <div class="section-head"><h2>Where it fits — and why it helps</h2></div>
    <div class="two-col">
      <div class="col-card"><h3>Applications</h3><ul class="item-list">{item_list(d['apps'], 'Practical use case for this ESP32 build.')}</ul></div>
      <div class="col-card"><h3>Advantages</h3><ul class="item-list">{item_list(d['advantages'], 'Key benefit of this project approach.')}</ul></div>
    </div>
  </section>

  <section id="future" class="wrap">
    <div class="section-head"><h2>Future improvements</h2><p>Natural next layers to add on top of the core build.</p></div>
    <div class="chip-grid">{''.join(future_html)}</div>
  </section>

  <section id="related" class="wrap">
    <div class="section-head"><h2>Related ESP32 projects</h2><p>Similar tutorials in this library.</p></div>
    <div class="grid">{''.join(related_html)}</div>
  </section>

  <section id="faq" class="wrap">
    <div class="section-head"><h2>FAQ</h2></div>
    <div class="faq-list">
      <div class="faq-item open">
        <button class="faq-q" onclick="toggleFaq(this)">{esc(d['faq_q'])}<span class="plus">+</span></button>
        <div class="faq-a"><p>{esc(d['faq_a'])}</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="toggleFaq(this)">How do I choose the threshold?<span class="plus">+</span></button>
        <div class="faq-a"><p>Log raw sensor readings under normal and trigger conditions, then pick a value between them. Adjust the threshold constant in the sketch until the output activates at the level you want.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="toggleFaq(this)">Can this project scale to more sensors or outputs?<span class="plus">+</span></button>
        <div class="faq-a"><p>Yes. Add extra GPIO pins for additional sensors or relay channels, then run the same read-compare-act loop for each zone in the firmware.</p></div>
      </div>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <a class="brand" href="../index.html">{LEAF_SVG}ESP32 Project Library</a>
    <div class="meta">{esc(d['category'])} · {esc(d['difficulty'])} · {esc(d['slug'])}</div>
  </div>
</footer>

<script src="../project.js"></script>
</body>
</html>
"""


def main():
    files = sorted(PROJECTS.glob("*.html"))
    if not files:
        print("No project files found", file=sys.stderr)
        sys.exit(1)
    for i, path in enumerate(files, 1):
        data = parse_project(path)
        path.write_text(render_page(data), encoding="utf-8")
        if i % 100 == 0:
            print(f"Rebuilt {i}/{len(files)}")
    print(f"Done — rebuilt {len(files)} project pages")


if __name__ == "__main__":
    main()
