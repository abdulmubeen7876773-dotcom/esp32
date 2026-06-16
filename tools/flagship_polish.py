import html
import re

from site_layout import normalize_terms, short_category

FLAGSHIP_VARIANTS_PER_BASE = 24

HYPE_LEADS = [
    "Production-ready walkthrough — {sensor} on {pin} drives {output} with a tuned threshold sketch you can deploy today.",
    "Full-stack {cat} build: wire {sensor}, flash firmware, and validate {output} on {outpin} in under {mins} minutes.",
    "Flagship ESP32 tutorial for {use}: calibrated sensing, clean GPIO routing, and Serial-verified {output} control.",
]

EXTRA_BLOG = [
    "Start on a breadboard, confirm readings in Serial Monitor, then move to a permanent perfboard or PCB once thresholds are stable.",
    "Label {pin} and {outpin} on your harness — swapping sensor and output wires is the most common wiring mistake on first builds.",
    "For {use}, log ten minutes of idle readings before picking THRESHOLD so false triggers from noise stay rare.",
    "If {output} buzzes or chatters near the cutoff, add hysteresis in code or raise SAMPLE_DELAY_MS slightly.",
]

WIRING_TIPS = [
    "Keep sensor signal wires short and away from relay coils to reduce ADC noise.",
    "Share GND between ESP32, sensor module, and relay board — never leave grounds floating.",
    "Use the 3.3 V pin for logic-level modules; power heavy loads through a separate 5 V supply and relay.",
    "Double-check {pin} and {outpin} in both the wiring diagram and sketch before uploading.",
    "Add a 100 nF capacitor near the sensor VCC pin if readings jump when Wi-Fi transmits.",
]

EXTRA_APPS = [
    "Deploy as a {use} edge node before adding cloud dashboards",
    "Demo-ready bench setup for workshops and university labs",
    "Baseline firmware for a custom PCB spin with the same GPIO map",
]

EXTRA_FAQS = [
    (
        "What should I see in Serial Monitor on first boot?",
        "Live ADC values every loop plus the configured THRESHOLD — trigger the sensor and confirm {output} toggles on {outpin}.",
    ),
    (
        "Can I run this from USB power only?",
        "Yes for bench tests. Use a rated supply if {output} draws more current than the board 3.3 V regulator allows.",
    ),
]


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def variant_num(slug: str) -> int:
    m = re.search(r"project-(\d+)$", slug or "", re.I)
    return int(m.group(1)) if m else 99


def is_flagship(slug: str) -> bool:
    return variant_num(slug) <= FLAGSHIP_VARIANTS_PER_BASE


def pick(pool: list, variant: int, salt: int = 0) -> str:
    return pool[(variant + salt) % len(pool)]


def fmt(template: str, mapping: dict) -> str:
    try:
        return template.format(**mapping)
    except KeyError:
        return template


def ctx(d: dict, variant: int) -> dict:
    from content_variants import ctx as base_ctx

    return base_ctx(d, variant)


def apply_flagship_polish(d: dict, variant: int) -> None:
    c = ctx(d, variant)
    d["lead"] = normalize_terms(fmt(pick(HYPE_LEADS, variant), c))
    extras = [normalize_terms(fmt(pick(EXTRA_BLOG, variant, i * 2), c)) for i in range(3)]
    d["blog_paras"] = (d.get("blog_paras") or []) + extras
    d["apps"] = (d.get("apps") or [])[:4] + [
        normalize_terms(fmt(pick(EXTRA_APPS, variant, i), c)) for i in range(2)
    ]
    d["advantages"] = (d.get("advantages") or [])[:4] + [
        "Visual wiring diagram plus pin table for fast assembly",
        "Flagship tutorial with extended FAQ and calibration notes",
    ]
    d["future"] = (d.get("future") or [])[:3] + [
        "Add Blynk or ESPHome integration for phone control",
    ]
    extra_faq = [(normalize_terms(fmt(q, c)), normalize_terms(fmt(a, c))) for q, a in EXTRA_FAQS]
    d["faq_extra"] = (d.get("faq_extra") or []) + extra_faq
    d["wiring_tips"] = [normalize_terms(fmt(pick(WIRING_TIPS, variant, i), c)) for i in range(4)]
    d["featured"] = True


def wire_color(name: str, pin: str) -> str:
    pl = (pin or "").lower()
    nl = (name or "").lower()
    if any(k in pl for k in ("gnd", "ground")) or "gnd" in nl:
        return "#64748b"
    if any(k in pl for k in ("3v3", "3.3", "vin", "5v", "vcc")) or "power" in nl:
        return "#a78bfa"
    if "relay" in nl or "motor" in nl or "pump" in nl or "led" in nl or "output" in nl:
        return "#fbbf24"
    return "#38bdf8"


def wiring_diagram_enhanced(d: dict) -> str:
    wiring = d.get("wiring") or []
    if not wiring:
        wiring = [(d.get("sensor_name", "Sensor"), d.get("sensor_pin", "GPIO34"))]
        if d.get("output_pin"):
            wiring.append((d.get("output_name", "Output"), d.get("output_pin")))
    rows = wiring[:6]
    svg_rows = []
    y0 = 28
    for i, (name, pin) in enumerate(rows):
        y = y0 + i * 34
        col = wire_color(name, pin)
        label = esc(name[:22])
        pin_l = esc(pin)
        svg_rows.append(
            f'<rect x="16" y="{y - 14}" width="108" height="28" rx="6" fill="#1e293b" stroke="{col}" stroke-width="1.5"/>'
            f'<text x="70" y="{y + 4}" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" fill="#f8fafc">{label}</text>'
            f'<line x1="124" y1="{y}" x2="168" y2="{y}" stroke="{col}" stroke-width="2" stroke-dasharray="4 3"/>'
            f'<text x="176" y="{y + 4}" font-family="ui-monospace,monospace" font-size="10" fill="{col}">{pin_l}</text>'
        )
    rows_h = max(len(rows) * 34 + 20, 120)
    esp_h = min(rows_h + 40, 260)
    esp_y = esp_h / 2
    return f"""
      <figure class="wiring-diagram" aria-label="Wiring diagram">
        <svg viewBox="0 0 520 {esp_h}" xmlns="http://www.w3.org/2000/svg" role="img">
          <defs>
            <linearGradient id="espGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <filter id="glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          </defs>
          <rect width="520" height="{esp_h}" rx="12" fill="#0f172a" stroke="rgba(56,189,248,.25)" stroke-width="1"/>
          {''.join(svg_rows)}
          <rect x="248" y="{esp_y - 52}" width="120" height="104" rx="12" fill="url(#espGrad)" stroke="#38bdf8" stroke-width="2" filter="url(#glow)"/>
          <text x="308" y="{esp_y - 8}" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="18" fill="#f8fafc">ESP32</text>
          <text x="308" y="{esp_y + 14}" text-anchor="middle" font-family="ui-monospace,monospace" font-size="9" fill="#94a3b8">DevKit</text>
          <circle cx="360" cy="{esp_y - 36}" r="4" fill="#22d3ee"/>
          <circle cx="360" cy="{esp_y + 36}" r="4" fill="#fbbf24"/>
          <line x1="368" y1="{esp_y - 36}" x2="420" y2="{esp_y - 36}" stroke="#22d3ee" stroke-width="2"/>
          <line x1="368" y1="{esp_y + 36}" x2="420" y2="{esp_y + 36}" stroke="#fbbf24" stroke-width="2"/>
          <rect x="420" y="{esp_y - 50}" width="84" height="28" rx="6" fill="#1e293b" stroke="#22d3ee" stroke-width="1.5"/>
          <text x="462" y="{esp_y - 32}" text-anchor="middle" font-size="8" fill="#94a3b8">INPUT</text>
          <rect x="420" y="{esp_y + 22}" width="84" height="28" rx="6" fill="#1e293b" stroke="#fbbf24" stroke-width="1.5"/>
          <text x="462" y="{esp_y + 40}" text-anchor="middle" font-size="8" fill="#94a3b8">OUTPUT</text>
        </svg>
        <figcaption class="diagram-caption">Signal flow: components → GPIO pins → ESP32 logic</figcaption>
      </figure>"""


def hero_diagram_dark(d: dict) -> str:
    sensor = esc((d.get("sensor_name") or "SENSOR")[:16].upper())
    output = esc((d.get("output_name") or "OUTPUT")[:12].upper())
    return f"""
  <div class="diagram-wrap diagram-hero">
    <svg viewBox="0 0 1000 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Control loop diagram">
      <rect width="1000" height="240" rx="14" fill="#0f172a" stroke="rgba(56,189,248,.2)" stroke-width="1"/>
      <path d="M80 140 A50 50 0 0 1 130 90" stroke="#38bdf8" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M130 90 A50 50 0 0 1 180 140" stroke="#fbbf24" stroke-width="6" fill="none" stroke-linecap="round"/>
      <circle cx="130" cy="140" r="5" fill="#f8fafc"/>
      <text x="130" y="175" text-anchor="middle" font-family="ui-monospace,monospace" font-size="10" fill="#94a3b8">{sensor}</text>
      <line x1="200" y1="140" x2="280" y2="140" stroke="#64748b" stroke-width="2" stroke-dasharray="5 4"/>
      <rect x="280" y="95" width="140" height="90" rx="10" fill="#111827" stroke="#38bdf8" stroke-width="2"/>
      <text x="350" y="145" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="20" fill="#f8fafc">ESP32</text>
      <circle cx="405" cy="108" r="4" fill="#22d3ee"/>
      <line x1="420" y1="140" x2="500" y2="140" stroke="#64748b" stroke-width="2" stroke-dasharray="5 4"/>
      <rect x="500" y="105" width="100" height="70" rx="8" fill="#111827" stroke="#fbbf24" stroke-width="2"/>
      <text x="550" y="148" text-anchor="middle" font-size="11" fill="#fbbf24">GPIO OUT</text>
      <line x1="600" y1="140" x2="680" y2="140" stroke="#64748b" stroke-width="2"/>
      <rect x="680" y="100" width="120" height="80" rx="8" fill="#111827" stroke="#22d3ee" stroke-width="1.5"/>
      <text x="740" y="148" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="600" font-size="14" fill="#f8fafc">{output}</text>
      <text x="500" y="215" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#64748b">Sense → Compare threshold → Actuate output</text>
    </svg>
  </div>"""


def wiring_tips_html(d: dict) -> str:
    tips = d.get("wiring_tips") or []
    if not tips:
        return ""
    items = "".join(f"<li>{esc(t)}</li>" for t in tips)
    return f'<div class="wiring-tips"><h3>Wiring tips</h3><ul>{items}</ul></div>'
