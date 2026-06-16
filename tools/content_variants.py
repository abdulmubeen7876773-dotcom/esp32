import re

from site_layout import normalize_terms, short_category
from title_generator import CONN, USE_CASES, GENERIC_USE, generate_title

LEAD_TEMPLATES = [
    "Wire {sensor} to an ESP32 and use it to drive {output} for {use}.",
    "This hands-on {cat} project reads {sensor} on {pin} and switches {output} automatically.",
    "Build a practical {use} setup where ESP32 monitors {sensor} and controls {output}.",
    "Step-by-step guide: connect {sensor}, upload the sketch, and test {output} in {use}.",
    "Automate {output} with ESP32 by reacting to live {sensor} readings — ideal for {use}.",
    "Learn how {sensor} data on {pin} triggers {output} for reliable {use} operation.",
    "A compact ESP32 circuit for {use} that links {sensor} input to {output} action.",
    "Monitor {sensor}, set a threshold, and let ESP32 manage {output} without cloud dependency.",
]

INTRO_TEMPLATES = [
    "You'll connect {sensor} to {pin}, configure a threshold, and drive {output} on {outpin}.",
    "The sketch samples {sensor} on {pin}, compares the value, and toggles {output} on {outpin}.",
    "After wiring {sensor} and {output}, the ESP32 runs a simple read-compare-act loop.",
    "This build focuses on stable {cat} behavior: sense with {sensor}, act with {output}.",
    "Expect about {mins} minutes to wire the board, flash firmware, and verify Serial output.",
]

OVERVIEW_TEMPLATES = [
    "This {cat} project uses {sensor} on {pin} to decide when {output} on {outpin} should run — suited for {use}.",
    "Designed for {use}: ESP32 watches {sensor} and activates {output} when conditions cross your threshold.",
    "A beginner-friendly {cat} circuit where {sensor} feeds the ESP32 and {output} handles the physical action.",
    "The firmware keeps logic local on the ESP32, making it dependable for {use} prototypes.",
]

APP_POOL = [
    "{use} monitoring with {sensor}",
    "Hands-on {cat} learning with real GPIO control",
    "Prototype before adding {conn} telemetry",
    "Bench testing {output} automation logic",
    "Low-cost demo for classrooms and makerspaces",
    "Field trial in {use} environments",
    "Night-and-day logging via Serial Monitor",
    "Battery-friendly polling with adjustable delays",
]

ADV_POOL = [
    "Minimal parts list — easy to source locally",
    "Clear {pin} / {outpin} wiring table included",
    "Readable Arduino sketch with tunable threshold",
    "Works offline without Wi-Fi or cloud accounts",
    "Serial logs help you calibrate quickly",
    "Same pattern scales to MQTT, HTTP, or BLE later",
    "Safe starting point for {cat} experiments",
    "Documented steps from wiring to demonstration",
]

FUTURE_POOL = [
    "Publish readings to an MQTT broker or Home Assistant",
    "Add a web dashboard with ESPAsyncWebServer",
    "Store CSV logs on SD card for long-term trends",
    "Send Telegram or email alerts on threshold events",
    "Implement deep sleep between samples to save power",
    "Expose tuning knobs through a captive portal page",
    "Add OLED feedback for live sensor values",
    "Integrate OTA updates for remote firmware fixes",
]

FAQ_SETS = [
    [
        ("Can this run without internet?", "Yes. Sensing and output control happen on the ESP32 locally."),
        ("Which pin is the sensor on?", "Wire the sensor signal to {pin} as shown in the schematic table."),
        ("How do I tune sensitivity?", "Adjust THRESHOLD in code after logging normal and trigger readings in Serial Monitor."),
    ],
    [
        ("What power supply do I need?", "A stable 5 V USB supply is enough for bench tests; use a proper relay supply for heavy loads."),
        ("Can I change GPIO pins?", "Yes — update SENSOR_PIN, OUTPUT_PIN, and the wiring table together."),
        ("Why is my output always on?", "Your threshold may be too low or the sensor wiring might be floating — add a pull-up/down if required."),
    ],
    [
        ("Does this work with 3.3 V sensors?", "Most analog modules work at 3.3 V on ESP32 ADC pins; verify your module datasheet."),
        ("Can I log data to my phone?", "Start with Serial Monitor; later add BLE or Wi-Fi logging using {conn}."),
        ("Is this safe for mains-powered loads?", "Use an isolated relay module and follow electrical safety guidelines for high voltage."),
    ],
    [
        ("How fast does it respond?", "Response time is set by SAMPLE_DELAY_MS in the sketch — lower values react faster."),
        ("Can multiple sensors be added?", "Yes — expand the sketch to read extra pins or an I2C sensor bus."),
        ("Which board should I buy?", "Any ESP32-WROOM DevKit with USB works; 30-pin boards are the easiest for breadboards."),
    ],
]

STEP_ACT = [
    "When triggered, {output} on {outpin} turns on until the reading returns below the threshold.",
    "The ESP32 drives {output} on {outpin} high while the condition stays true, then releases it.",
    "{output} activates on {outpin} for each threshold crossing — watch the Serial log to confirm timing.",
    "GPIO {outpin} mirrors the decision: HIGH activates {output}, LOW idles the circuit.",
]

WRAP_TEMPLATES = [
    "You now have a working {subj} pattern — swap sensors, thresholds, or outputs for your next build.",
    "Reuse this {cat} firmware skeleton: change pins, THRESHOLD, and {output} for new prototypes.",
    "That completes the {subj} walkthrough. Extend it with {conn} when you are ready for remote monitoring.",
]


def gpio_num(pin: str) -> int:
    m = re.search(r"(\d+)", pin or "34")
    return int(m.group(1)) if m else 34


def pick(pool: list, variant: int, salt: int = 0) -> str:
    return pool[(variant + salt) % len(pool)]


def fmt(template: str, mapping: dict) -> str:
    try:
        return template.format(**mapping)
    except KeyError:
        return template


def prose_subject(title: str) -> str:
    t = title.strip()
    t = re.sub(
        r"^(Build a Smart |Build an |Build a |How to Build an |How to Build a |Create a |Make an |Make a |Step-by-Step: )",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(r"^ESP32\s+", "", t, flags=re.I)
    t = re.sub(r"\s+v\d+$", "", t, flags=re.I)
    return t.strip().lower() or "esp32 project"


def ctx(d: dict, variant: int) -> dict:
    cat = d.get("category") or "ESP32"
    cat_short = short_category(cat)
    use_pool = USE_CASES.get(cat, GENERIC_USE)
    use = pick(use_pool, variant, 2)
    conn = pick(CONN, variant, 5)
    return {
        "sensor": d.get("sensor_name") or "sensor",
        "output": d.get("output_name") or "output",
        "pin": d.get("sensor_pin") or "GPIO34",
        "outpin": d.get("output_pin") or "GPIO26",
        "cat": cat_short,
        "use": use,
        "conn": conn,
        "mins": 5 + (variant % 8),
        "subj": prose_subject(d.get("title") or ""),
    }


def generate_lead(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    return normalize_terms(fmt(pick(LEAD_TEMPLATES, variant), c))


def generate_overview(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    return normalize_terms(fmt(pick(OVERVIEW_TEMPLATES, variant, 1), c))


def generate_blog_paras(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    subj = c["subj"]
    return [
        normalize_terms(
            f"This tutorial walks through {subj} — wiring, firmware, and a quick bench test."
        ),
        normalize_terms(fmt(pick(INTRO_TEMPLATES, variant, 3), c)),
        normalize_terms(
            f"Built for {c['use'].lower()}: extend later with {c['conn']} if you need remote visibility."
        ),
    ]


def generate_apps(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    return [normalize_terms(fmt(pick(APP_POOL, variant, i * 4), c)) for i in range(4)]


def generate_advantages(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    return [normalize_terms(fmt(pick(ADV_POOL, variant, i * 3 + 1), c)) for i in range(4)]


def generate_future(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    out = []
    for i in range(3):
        text = pick(FUTURE_POOL, variant, i * 5)
        if "{conn}" in text:
            text = fmt(text, c)
        out.append(normalize_terms(text))
    return out


def generate_faqs(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    base = FAQ_SETS[variant % len(FAQ_SETS)]
    return [(normalize_terms(fmt(q, c)), normalize_terms(fmt(a, c))) for q, a in base]


def generate_how(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    return normalize_terms(
        f"Open Serial Monitor at 115200 baud, move {c['sensor'].lower()}, and confirm {c['output'].lower()} "
        f"responds on {c['outpin']} when readings cross THRESHOLD."
    )


def generate_wrap(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    return normalize_terms(fmt(pick(WRAP_TEMPLATES, variant, 2), c))


def overview_bullets(d: dict, variant: int) -> list:
    c = ctx(d, variant)
    thresh = 1200 + (variant * 191 + sum(ord(x) for x in d.get("slug", "")[-6:])) % 2800
    delay = 300 + (variant * 97) % 1700
    return [
        f"{c['sensor']} connects to {c['pin']} (ADC input)",
        f"Threshold is set to {thresh} in firmware (adjust after calibration)",
        f"{c['output']} is driven on {c['outpin']} when the condition is met",
        f"The main loop samples every {delay} ms while powered",
    ]


def step_act_text(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    return normalize_terms(fmt(pick(STEP_ACT, variant), c))


def vary_sketch(d: dict, variant: int) -> str:
    c = ctx(d, variant)
    sensor = gpio_num(d.get("sensor_pin"))
    output = gpio_num(d.get("output_pin"))
    slug = d.get("slug") or "project"
    threshold = 1200 + (variant * 191 + sum(ord(x) for x in slug[-8:])) % 2800
    delay_ms = 300 + (variant * 97) % 1700
    invert = variant % 5 == 0
    op = "<" if invert else ">"
    title = d.get("title") or "ESP32 Project"
    return f"""// {title}
const int SENSOR_PIN = {sensor};
const int OUTPUT_PIN = {output};
const int THRESHOLD = {threshold};
const int SAMPLE_DELAY_MS = {delay_ms};

void setup() {{
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  Serial.println("Starting: {prose_subject(title)}");
  Serial.print("Threshold: ");
  Serial.println(THRESHOLD);
}}

void loop() {{
  int reading = analogRead(SENSOR_PIN);
  Serial.print("{c['sensor']}: ");
  Serial.println(reading);
  bool active = reading {op} THRESHOLD;
  digitalWrite(OUTPUT_PIN, active ? HIGH : LOW);
  delay(SAMPLE_DELAY_MS);
}}"""


def assign_varied_content(d: dict, variant: int, used_titles: set) -> None:
    d["variant"] = variant
    d["title"] = generate_title(d, variant, used_titles)
    d["lead"] = generate_lead(d, variant)
    d["overview"] = generate_overview(d, variant)
    d["apps"] = generate_apps(d, variant)
    d["advantages"] = generate_advantages(d, variant)
    d["future"] = generate_future(d, variant)
    faqs = generate_faqs(d, variant)
    d["faq_q"], d["faq_a"] = faqs[0]
    d["faq_extra"] = faqs[1:]
    d["how"] = generate_how(d, variant)
    d["overview_bullets"] = overview_bullets(d, variant)
    d["step_act"] = step_act_text(d, variant)
    d["code"] = vary_sketch(d, variant)
    d["blog_paras"] = generate_blog_paras(d, variant)
    d["wrap_up"] = generate_wrap(d, variant)
