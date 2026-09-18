import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_categories
from parent_registry import PARENTS
from project_icons import slug_cat
from project_text import card_description, primary_difficulty, project_title, public_projects
from site_layout import (
    SITE_DOMAIN,
    SITE_NAME,
    breadcrumb_schema,
    category_hero_html,
    category_section_title,
    esc,
    footer_html,
    head_html,
    header_html,
    itemlist_schema,
    modern_card,
    organization_schema,
    short_category,
    sidebar_categories_html,
    site_href,
    webpage_schema,
    UI_JS_SRC,
)

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"

CATEGORY_INTROS = load_categories() or {
    "Agriculture": "Automate irrigation, soil monitoring, and greenhouse control with ESP32 sensor nodes and relay outputs.",
    "Home Automation": "Build smart home projects — climate control, lighting, and appliance automation using ESP32 and common sensors.",
    "Security Projects": "Motion detection, alerts, and access monitoring tutorials with PIR sensors, relays, and Wi-Fi notifications.",
    "IoT Projects": "Connected ESP32 builds that publish sensor data to dashboards, APIs, and local web servers over Wi-Fi.",
    "Sensor Projects": "Learn analog and digital sensing on ESP32 — distance, environmental, and signal processing project guides.",
    "Robotics": "Motor control, teleoperation, and sensor-assisted navigation projects powered by ESP32 microcontrollers.",
    "Industrial Automation": "Machine monitoring, energy tracking, and status nodes for benches, workshops, and small facilities.",
    "LED Projects": "RGB strips, patterns, and addressable LED control with ESP32 — from breadboard demos to Wi-Fi control.",
    "ESP32-CAM": "Explore exciting ESP32-CAM projects including surveillance cameras, face recognition, object detection, home security systems, and IoT camera applications.",
    "AI Projects": "On-device inference and TinyML experiments with ESP32 — audio, vision, and classification tutorials.",
    "Energy Monitoring": "Measure and log power draw with current sensors, displays, and optional cloud logging on ESP32.",
    "Healthcare": "Educational biosignal and wellness logging projects for learning — not for medical diagnosis or treatment.",
    "Environmental": "Air quality, weather, and environmental monitoring builds with gas sensors, BME modules, and fans.",
    "Smart City": "Street lighting, urban sensing, and infrastructure-style automation prototypes using ESP32.",
    "Education": "Classroom-friendly trainer projects that teach GPIO, sensors, and displays in progressive difficulty stages.",
}

CATEGORY_TITLE_OVERRIDES = {
    "AI Projects": "ESP32 AI Projects",
    "Home Automation": "ESP32 Home Automation Projects",
}

SIDEBAR_KEYS = {
    "ESP32-CAM": "esp32-cam",
    "IoT Projects": "iot-projects",
    "Home Automation": "home-automation",
    "LED Projects": "display",
    "Sensor Projects": "display",
}

CATEGORY_SEO_DETAILS = {
    "AI Projects": {
        "covers": "Practical ESP32 camera and edge-AI learning builds, including capture, QR scanning, face-detection demos, and bounded computer-vision experiments. These pages are about learning the data path from camera input to a visible decision, not claiming production-grade artificial intelligence.",
        "start": "Begin with the ESP32-CAM setup path, then compare camera capture with QR scanning and the color object detector demo. If a result looks wrong, test lighting, focus, frame size, and power before changing the model or code.",
        "skills": ["ESP32-CAM setup", "camera privacy", "image-processing limits", "safe AI claim boundaries"],
        "watch": ["Treat recognition results as demonstrations, not safety decisions.", "Keep camera projects privacy-aware and avoid recording people without permission.", "Verify lighting, focus, power stability, and Wi-Fi reliability before judging model behavior."],
        "guides": [("Install Arduino IDE", "/guides/installing-arduino-ide-esp32.html"), ("ESP32 basics", "/guides/what-is-esp32.html")],
        "components": [("ESP32-CAM", "/components/esp32-cam.html"), ("ESP32 DevKit", "/components/esp32-devkit.html")],
        "related": [("ESP32-CAM", "/category/esp32-cam.html"), ("Security Projects", "/category/security-projects.html")],
    },
    "Agriculture": {
        "covers": "Soil, water, greenhouse, and plant-monitoring projects where ESP32 reads changing outdoor or semi-outdoor conditions and turns them into cautious control decisions.",
        "start": "Start with a single soil or environmental reading, calibrate it in the actual pot or tray, then add relay or pump control only after manual testing.",
        "skills": ["sensor calibration", "wet/dry threshold testing", "relay and pump boundaries", "outdoor enclosure planning"],
        "watch": ["Soil probes drift and corrode, so compare readings against real soil moisture before automating irrigation.", "Keep pumps and water physically separated from USB-powered breadboards.", "Use relays, drivers, fuses, and enclosures for any load that is not powered directly by the ESP32."],
        "guides": [("Environmental sensors", "/guides/environmental-sensors.html"), ("Reading analog sensors", "/guides/reading-analog-sensors.html"), ("Digital inputs", "/guides/digital-inputs-floating-pins.html")],
        "components": [("DHT22", "/components/dht22.html"), ("BME280", "/components/bme280.html"), ("Relay module", "/components/relay-module.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("Environmental", "/category/environmental.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
    "Display Projects": {
        "covers": "Projects that turn sensor, time, status, or network data into compact visual output on OLED or matrix-style displays.",
        "start": "Learn I2C addressing first, connect a small OLED, print simple text, then move to dashboards such as weather clocks or sensor displays.",
        "skills": ["I2C address scanning", "OLED wiring", "text layout", "display refresh timing"],
        "watch": ["Most OLED modules use 3.3 V or 5 V VCC but SDA/SCL must remain ESP32-safe.", "If nothing appears, check address, library constructor, ground, and contrast before rewriting the project.", "Small displays are best for status and trends, not dense technical diagrams."],
        "guides": [("I2C communication", "/guides/i2c-communication.html"), ("Connect an OLED", "/guides/connect-oled-esp32.html"), ("OLED display basics", "/guides/oled-display-esp32.html")],
        "components": [("SSD1306 OLED", "/components/ssd1306-oled.html"), ("ESP32 DevKit", "/components/esp32-devkit.html"), ("BME280", "/components/bme280.html")],
        "related": [("LED Projects", "/category/led-projects.html"), ("Environmental", "/category/environmental.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
    "Education": {
        "covers": "Classroom and self-study projects that make GPIO, inputs, displays, and simple debugging visible on the bench.",
        "start": "Begin with the ESP32 Learning Trainer if you want a repeatable classroom board before moving into sensors.",
        "skills": ["digital input and output", "safe breadboard habits", "serial debugging", "student-friendly experiments"],
        "watch": ["Choose projects where students can predict one input and one output before adding complexity.", "Keep worksheets focused on wiring evidence, Serial Monitor observations, and one safe variation.", "Avoid relays, high-current loads, and unattended hardware in first classroom sessions."],
        "guides": [("ESP32 basics", "/guides/what-is-esp32.html"), ("Blink an LED", "/guides/blink-led-esp32.html"), ("Button input", "/guides/button-led-control.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html"), ("SSD1306 OLED", "/components/ssd1306-oled.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("Display Projects", "/category/display-projects.html")],
    },
    "Energy Monitoring": {
        "covers": "Bench-scale ESP32 projects for measuring, displaying, or logging power-related values with current sensors and safe monitoring boundaries.",
        "start": "Begin with low-voltage measurement concepts and display/logging, then review isolation and safety before adapting anything near mains circuits.",
        "skills": ["current-sensor reads", "calibration against a known load", "displayed measurements", "safety boundaries"],
        "watch": ["Do not place ESP32 breadboards in exposed mains circuits.", "Treat energy readings as educational unless the sensor, installation, and calibration are verified.", "Use qualified review, enclosures, fusing, and isolation for any real AC installation."],
        "guides": [("Analog inputs", "/guides/analog-inputs.html"), ("Reading analog sensors", "/guides/reading-analog-sensors.html"), ("OLED display basics", "/guides/oled-display-esp32.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html"), ("SSD1306 OLED", "/components/ssd1306-oled.html"), ("Relay module", "/components/relay-module.html")],
        "related": [("Industrial Automation", "/category/industrial-automation.html"), ("Smart City", "/category/smart-city.html"), ("Home Automation", "/category/home-automation.html")],
    },
    "Environmental": {
        "covers": "Air, weather, pressure, and room-condition monitoring with sensors that report changing real-world values.",
        "start": "Start with a weather or air-quality build, then add OLED display output once sensor readings are stable.",
        "skills": ["I2C sensor reads", "calibration checks", "threshold decisions", "local status displays"],
        "watch": ["Sensor placement changes readings, especially near fans, heat sources, enclosures, or direct sunlight.", "Air-quality and gas values need calibration and should not replace certified detectors.", "Log several readings before choosing thresholds for alerts or automation."],
        "guides": [("Environmental sensors", "/guides/environmental-sensors.html"), ("I2C communication", "/guides/i2c-communication.html"), ("OLED display", "/guides/oled-display-esp32.html")],
        "components": [("BME280", "/components/bme280.html"), ("DHT22", "/components/dht22.html"), ("SSD1306 OLED", "/components/ssd1306-oled.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
    "ESP32-CAM": {
        "covers": "Camera capture, streaming, QR scanning, and vision projects using the ESP32-CAM module and OV2640 camera.",
        "start": "Verify power and upload settings first, then test a single capture endpoint before adding dashboards or detection.",
        "skills": ["camera pin mapping", "Wi-Fi image serving", "power troubleshooting", "frame-size tradeoffs"],
        "guides": [("ESP32 basics", "/guides/what-is-esp32.html"), ("Install Arduino IDE", "/guides/installing-arduino-ide-esp32.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html")],
        "related": [("Security Projects", "/category/security-projects.html"), ("AI Projects", "/category/ai-projects.html")],
    },
    "Healthcare": {
        "covers": "Educational biosignal and wellness-logging prototypes for learning sensors, timing, and data display. These projects help students understand signal collection, display choices, logging, and noise limits while staying outside medical-device claims.",
        "start": "Use these only as learning projects; they are not medical devices or diagnostic tools. If readings jump, freeze, or look unrealistic, check sensor placement, supply voltage, wiring, library configuration, and whether the module needs calibration or warm-up time.",
        "skills": ["I2C sensor logging", "signal sanity checks", "safe educational scope", "clear data presentation"],
        "watch": ["Do not use these builds for diagnosis, treatment, patient monitoring, or emergency decisions.", "Compare readings only as classroom signals unless the module and setup are medically validated.", "Keep privacy in mind before logging or sharing health-related data."],
        "guides": [("I2C communication", "/guides/i2c-communication.html"), ("Reading analog sensors", "/guides/reading-analog-sensors.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html"), ("SSD1306 OLED", "/components/ssd1306-oled.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("Education", "/category/education.html")],
    },
    "Home Automation": {
        "covers": "ESP32 home automation builds for smart thermostats, climate control, relay-safe switching, door locks, lighting, and sensor-triggered actions.",
        "start": "Begin with a low-voltage sensor-and-output project such as the smart thermostat before moving to relays, locks, or network dashboards.",
        "skills": ["relay control", "sensor thresholds", "manual overrides", "safe low-voltage prototyping", "dashboard-ready status"],
        "guides": [("Digital inputs", "/guides/digital-inputs-floating-pins.html"), ("Read temperature with DHT22", "/guides/read-temperature-dht22.html"), ("PWM fundamentals", "/guides/pwm-fundamentals.html")],
        "components": [("Relay module", "/components/relay-module.html"), ("DHT22", "/components/dht22.html"), ("PIR sensor", "/components/pir-sensor.html"), ("SSD1306 OLED", "/components/ssd1306-oled.html")],
        "related": [("Security Projects", "/category/security-projects.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
    "LED Projects": {
        "covers": "Addressable LEDs, RGB effects, LED matrices, brightness control, and visual feedback projects.",
        "start": "Start with one simple LED or matrix effect, then add patterns, buttons, audio, or Wi-Fi control.",
        "skills": ["PWM brightness", "timing loops", "pattern state", "power-aware LED wiring"],
        "watch": ["Long LED strips need external power and common ground; do not power them from the ESP32 3V3 pin.", "Use current estimates before increasing brightness or pixel count.", "Separate visual-effect code from input logic so timing bugs are easier to find."],
        "guides": [("PWM fundamentals", "/guides/pwm-fundamentals.html"), ("Blink an LED", "/guides/blink-led-esp32.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html")],
        "related": [("Display Projects", "/category/display-projects.html"), ("Education", "/category/education.html")],
    },
    "Robotics": {
        "covers": "Mobile robots, arms, motor outputs, sensor feedback, and control loops using ESP32 as the controller.",
        "start": "Test each motor or servo separately before adding sensors and remote-control logic.",
        "skills": ["motor driver control", "state machines", "sensor feedback", "battery-aware debugging"],
        "watch": ["Motors and servos need their own suitable power path and a common ground with the ESP32 control circuit.", "Test motion with wheels lifted or mechanisms unloaded before running on a table.", "Add sensors only after direction, speed, and stop behavior are predictable."],
        "guides": [("PWM fundamentals", "/guides/pwm-fundamentals.html"), ("Multiple buttons", "/guides/multiple-buttons-state-detection.html")],
        "components": [("HC-SR04", "/components/hc-sr04.html"), ("ESP32 DevKit", "/components/esp32-devkit.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
    "Security Projects": {
        "covers": "Motion alerts, RFID access, camera monitoring, and lock-control prototypes with clear safety boundaries.",
        "start": "Begin with a local sensor or card reader, then add network alerts only after local testing is reliable.",
        "skills": ["PIR detection", "RFID checks", "relay safety", "event logging"],
        "watch": ["Learning projects are not certified security systems and should not be the only protection for people or property.", "Test false positives, missed triggers, and power loss before adding notifications.", "Keep locks, relays, and door hardware separate from USB breadboard wiring unless properly enclosed."],
        "guides": [("Digital inputs", "/guides/digital-inputs-floating-pins.html"), ("Button debouncing", "/guides/debouncing-buttons.html")],
        "components": [("PIR sensor", "/components/pir-sensor.html"), ("Relay module", "/components/relay-module.html")],
        "related": [("ESP32-CAM", "/category/esp32-cam.html"), ("Home Automation", "/category/home-automation.html")],
    },
    "Sensor Projects": {
        "covers": "Analog, digital, ultrasonic, environmental, and threshold-based sensing projects for ESP32.",
        "start": "Start with a single sensor reading in Serial Monitor, then add a display or alert once values make sense.",
        "skills": ["ADC readings", "voltage-divider awareness", "digital sensors", "threshold testing"],
        "guides": [("Reading analog sensors", "/guides/reading-analog-sensors.html"), ("Analog inputs", "/guides/analog-inputs.html"), ("I2C communication", "/guides/i2c-communication.html")],
        "components": [("HC-SR04", "/components/hc-sr04.html"), ("BME280", "/components/bme280.html"), ("DHT22", "/components/dht22.html")],
        "related": [("Environmental", "/category/environmental.html"), ("Smart City", "/category/smart-city.html")],
    },
    "Smart City": {
        "covers": "Street lighting, parking, safety, and infrastructure-style sensor nodes scaled down for learning.",
        "start": "Begin with one local decision such as light level or distance, then add connectivity after the behaviour is proven.",
        "skills": ["threshold automation", "urban sensing", "status outputs", "field-style troubleshooting"],
        "watch": ["Treat these as scale-model or bench prototypes, not public infrastructure equipment.", "Outdoor placement requires weatherproof enclosures, cable strain relief, and power planning.", "Verify thresholds in realistic lighting, distance, and motion conditions before relying on automation."],
        "guides": [("Analog inputs", "/guides/analog-inputs.html"), ("Reading analog sensors", "/guides/reading-analog-sensors.html"), ("PWM fundamentals", "/guides/pwm-fundamentals.html")],
        "components": [("HC-SR04", "/components/hc-sr04.html"), ("PIR sensor", "/components/pir-sensor.html"), ("Relay module", "/components/relay-module.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("Energy Monitoring", "/category/energy-monitoring.html")],
    },
    "Industrial Automation": {
        "covers": "Workshop and bench automation projects for monitoring machines, vibration, RFID movement, CNC status, or small-facility signals with ESP32.",
        "start": "Start with non-invasive monitoring such as vibration or RFID events before attempting control of a machine or load.",
        "skills": ["event logging", "machine-status inputs", "safe relay boundaries", "noise-aware wiring"],
        "watch": ["Do not connect ESP32 GPIO directly to industrial voltages, motors, drives, or machine control circuits.", "Use isolation, proper terminals, enclosures, and qualified review before adapting a bench prototype.", "Keep monitoring and control separate until input readings are stable and failure modes are understood."],
        "guides": [("Digital inputs", "/guides/digital-inputs-floating-pins.html"), ("Reading analog sensors", "/guides/reading-analog-sensors.html"), ("PWM fundamentals", "/guides/pwm-fundamentals.html")],
        "components": [("Relay module", "/components/relay-module.html"), ("ESP32 DevKit", "/components/esp32-devkit.html"), ("PIR sensor", "/components/pir-sensor.html")],
        "related": [("Energy Monitoring", "/category/energy-monitoring.html"), ("Security Projects", "/category/security-projects.html"), ("IoT Projects", "/category/iot-projects.html")],
    },
}


def linked_list(items: list[tuple[str, str]]) -> str:
    return "".join(f'<li><a href="{esc(href)}">{esc(label)}</a></li>' for label, href in items)


def category_context_html(cat: str, projects: list[dict]) -> str:
    details = CATEGORY_SEO_DETAILS.get(cat, {})
    if not details:
        return ""
    skills = "".join(f"<li>{esc(skill)}</li>" for skill in details.get("skills", []))
    watch = "".join(f"<li>{esc(item)}</li>" for item in details.get("watch", []))
    watch_html = f"<div><h3>Before you adapt it</h3><ul>{watch}</ul></div>" if watch else ""
    first_project = projects[0] if projects else None
    first_link = (
        f' A practical first build is <a href="../projects/{esc(first_project["slug"])}.html">{esc(first_project["title"])}</a>.'
        if first_project
        else ""
    )
    return f"""<section class="category-context">
      <h2>What this category covers</h2>
      <p>{esc(details["covers"])} {first_link}</p>
      <p><strong>Start here:</strong> {esc(details["start"])}</p>
      <div class="category-context-grid">
        <div><h3>Skills you practice</h3><ul>{skills}</ul></div>
        <div><h3>Related guides</h3><ul>{linked_list(details.get("guides", []))}</ul></div>
        <div><h3>Useful components</h3><ul>{linked_list(details.get("components", []))}</ul></div>
        <div><h3>Related categories</h3><ul>{linked_list(details.get("related", []))}</ul></div>
{watch_html}
      </div>
    </section>"""


def category_intro(cat: str) -> str:
    return CATEGORY_INTROS.get(
        cat,
        f"Browse ESP32 {short_category(cat)} tutorials with wiring diagrams, Arduino code, and clear difficulty labels.",
    )


def projects_for_category(cat: str) -> list[dict]:
    items = []
    for p in public_projects(PARENTS):
        if p["category"] != cat:
            continue
        items.append(
            {
                "href": f"../projects/{p['slug']}.html",
                "title": project_title(p),
                "desc": card_description(p),
                "category": p["category"],
                "difficulty": primary_difficulty(p),
                "slug": p["slug"],
                "featured": False,
            }
        )
    return items


def render_category_page(cat: str, projects: list[dict]) -> str:
    slug = slug_cat(cat)
    title = CATEGORY_TITLE_OVERRIDES.get(cat, category_section_title(cat))
    desc = category_intro(cat)
    canon = f"category/{slug}.html"
    cards = "".join(
        modern_card(p, card_class="post-card", thumb_cls="post-thumb", show_desc=True) for p in projects
    )
    list_items = [
        {"name": p["title"], "url": f"{SITE_DOMAIN}/projects/{p['slug']}.html"}
        for p in projects
    ]
    schema = (
        organization_schema()
        + webpage_schema(f"{title} | {SITE_NAME}", desc, canon)
        + breadcrumb_schema(
            [
                ("Home", "/"),
                ("Projects", "projects.html"),
                (short_category(cat), canon),
            ]
        )
        + itemlist_schema(title, list_items)
    )
    badges = (
        f'<span class="badge badge-light">{len(projects)} Projects</span>'
        f'<span class="badge badge-light">Clear difficulty labels</span>'
        f'<span class="badge badge-light">{esc(short_category(cat))}</span>'
    )
    sidebar_key = SIDEBAR_KEYS.get(cat, slug)
    hero = category_hero_html(title, desc, cat, badges)
    related_category = ""
    if cat == "LED Projects":
        related_category = '<p class="meta">Looking for screen-based builds? Browse <a href="/category/display-projects.html">ESP32 display projects</a>.</p>'
    elif cat == "Display Projects":
        related_category = '<p class="meta">Need LED strips or matrix builds? Browse <a href="/category/led-projects.html">ESP32 LED projects</a>.</p>'
    context = category_context_html(cat, projects)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", f"{title} | {SITE_NAME}", desc, canonical_path=canon, extra_schema=schema)}
</head>
<body class="category-page">
<main>
{header_html("projects")}
{hero}
<div class="layout-with-sidebar wrap">
  {sidebar_categories_html(sidebar_key)}
  <div class="main-with-sidebar">
    <section class="section-block">
      {related_category}
      {context}
      <div class="grid grid-projects category-project-grid">{cards or "<p>No projects in this category yet.</p>"}</div>
      <p class="meta category-back"><a href="{site_href('projects.html')}">← Browse all ESP32 projects</a></p>
    </section>
  </div>
</div>
</main>
{footer_html()}
<script src="{UI_JS_SRC}" defer></script>
</body>
</html>"""


def render_category_index(by_cat: dict[str, list[dict]]) -> str:
    cards = []
    for cat in sorted(by_cat):
        slug = slug_cat(cat)
        projects = projects_for_category(cat)
        desc = category_intro(cat)
        cards.append(
            f"""<a class="post-card modern-card" href="{site_href(f'category/{slug}.html')}">
  <div class="card-body">
    <div class="card-badges"><span class="badge badge-cat">{esc(short_category(cat))}</span><span class="badge badge-time">{len(projects)} projects</span></div>
    <h3>{esc(CATEGORY_TITLE_OVERRIDES.get(cat, category_section_title(cat)))}</h3>
    <p class="card-desc">{esc(desc)}</p>
    <div class="card-footer"><span class="btn btn-card">Open category<span aria-hidden="true">→</span></span></div>
  </div>
</a>"""
        )
    title = f"ESP32 Project Categories | {SITE_NAME}"
    desc = "Browse ESP32 Engine project categories by topic, with only public reviewed project tutorials included."
    schema = organization_schema() + webpage_schema(title, desc, "category/")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", title, desc, canonical_path="category/", extra_schema=schema)}
</head>
<body class="category-page">
<main>
{header_html("projects")}
<section class="section-block wrap page-head static-page">
  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{site_href()}">Home</a></li><li><a href="{site_href('projects.html')}">Projects</a></li><li aria-current="page">Categories</li></ol></nav>
  <h1>ESP32 Project Categories</h1>
  <p class="section-sub">Choose a topic and browse public ESP32 projects with clear wiring, code, safety notes, and troubleshooting.</p>
  <div class="grid grid-projects category-project-grid">{"".join(cards)}</div>
</section>
</main>
{footer_html()}
<script src="{UI_JS_SRC}" defer></script>
</body>
</html>"""


def main():
    CATEGORY_DIR.mkdir(exist_ok=True)
    by_cat = defaultdict(list)
    for p in public_projects(PARENTS):
        by_cat[p["category"]].append(p)
    written = 0
    for cat in sorted(by_cat):
        projects = projects_for_category(cat)
        slug = slug_cat(cat)
        out = CATEGORY_DIR / f"{slug}.html"
        out.write_text(render_category_page(cat, projects), encoding="utf-8")
        written += 1
    (CATEGORY_DIR / "index.html").write_text(render_category_index(by_cat), encoding="utf-8")
    print(f"Wrote {written} category landing pages in category/")


if __name__ == "__main__":
    main()
