import re

LEVELS = ["beginner", "intermediate", "advanced"]
LEVEL_LABELS = {"beginner": "Beginner", "intermediate": "Intermediate", "advanced": "Advanced"}


def gpio_num(pin: str) -> int:
    m = re.search(r"(\d+)", pin or "34")
    return int(m.group(1)) if m else 34


def clean_label(text: str) -> str:
    t = re.sub(r"\s+(signal|control|module|device)$", "", text or "", flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    return t or "Component"


def base_wiring(hardware: dict) -> list[tuple[str, str, str]]:
    rows = []
    for comp, pin in hardware.get("wiring", [])[:6]:
        comp_clean = clean_label(comp)
        note = "Analog input" if "gpio3" in pin.lower() or gpio_num(pin) >= 32 else "Digital I/O"
        if "gnd" in comp.lower() or pin.upper() == "GND":
            note = "Common ground"
        elif "vcc" in comp.lower() or "3.3" in pin or "5v" in pin.lower():
            note = "Power rail"
        elif "sda" in comp.lower() or "scl" in comp.lower():
            note = "I2C bus"
        rows.append((comp_clean, pin, note))
    if not rows:
        s_pin = hardware.get("sensor_pin", "GPIO34")
        o_pin = hardware.get("output_pin", "GPIO26")
        rows = [
            (clean_label(hardware.get("sensor_name", "Sensor")), s_pin, "Sensor input"),
            (clean_label(hardware.get("output_name", "Output")), o_pin, "Actuator output"),
            ("VCC", "3.3V", "Sensor power"),
            ("GND", "GND", "Common ground"),
        ]
    return rows


def level_wiring(level: str, hardware: dict, parent: dict) -> list[tuple[str, str, str]]:
    rows = list(base_wiring(hardware))
    if level == "beginner":
        return rows[:6]
    if level == "intermediate":
        extra = [
            ("OLED SDA", "GPIO21", "I2C data for 0.96\" display"),
            ("OLED SCL", "GPIO22", "I2C clock"),
            ("Mode button", "GPIO0", "Boot button — manual/auto toggle"),
        ]
        seen = {r[1] for r in rows}
        for e in extra:
            if e[1] not in seen:
                rows.append(e)
        return rows[:9]
    extra = [
        ("OLED SDA", "GPIO21", "Status display"),
        ("OLED SCL", "GPIO22", "I2C clock"),
        ("Alert LED", "GPIO2", "Notification indicator"),
    ]
    seen = {r[1] for r in rows}
    for e in extra:
        if e[1] not in seen:
            rows.append(e)
    rows.append(("Wi-Fi", "Built-in", "2.4 GHz — no extra wiring"))
    return rows[:10]


def level_components(level: str, hardware: dict, parent: dict) -> list[str]:
    base = [
        "ESP32 DevKit (30-pin)",
        "Breadboard",
        "Jumper wires",
        "USB cable (5 V power)",
    ]
    sensor = parent.get("sensor", "sensor module")
    output = parent.get("output", "output module")
    if level == "beginner":
        return base + [
            sensor.title(),
            output.title(),
            "1-channel relay module (if driving AC/high current)",
        ]
    if level == "intermediate":
        return base + [
            sensor.title(),
            output.title(),
            "Relay module",
            "0.96\" I2C OLED display",
            "Tactile push button",
            "10 kΩ resistor (pull-up if needed)",
        ]
    return base + [
        sensor.title(),
        output.title(),
        "Relay module",
        "I2C OLED display",
        "microSD module (optional logging)",
        "Stable 5 V supply for field deployment",
    ]


def level_overview(level: str, parent: dict) -> str:
    title = parent["title"]
    sensor = parent.get("sensor", "sensor")
    output = parent.get("output", "output")
    if level == "beginner":
        return (
            f"This beginner stage of {title} focuses on the essentials: read {sensor} data, "
            f"compare it to a simple threshold, and switch the {output} on or off. "
            f"No Wi-Fi required — perfect for your first working prototype on a breadboard."
        )
    if level == "intermediate":
        return (
            f"The intermediate stage adds calibration, an OLED status screen, and manual/auto mode. "
            f"You will tune thresholds from real readings, show live values on the display, "
            f"and harden the sketch with clearer error handling before adding connectivity."
        )
    return (
        f"The advanced stage connects {title} to your network: live dashboard or mobile-friendly "
        f"monitoring, alert notifications, CSV-style logging, and automation rules you can adjust remotely."
    )


def level_how(level: str, parent: dict, hardware: dict) -> list[str]:
    s_pin = hardware.get("sensor_pin", "GPIO34")
    o_pin = hardware.get("output_pin", "GPIO26")
    if level == "beginner":
        return [
            f"The ESP32 reads the {parent.get('sensor', 'sensor')} on {s_pin}.",
            "Firmware compares the reading against THRESHOLD in the sketch.",
            f"When the condition is met, {o_pin} drives the {parent.get('output', 'output')} HIGH.",
            "Serial Monitor at 115200 baud shows live values for calibration.",
        ]
    if level == "intermediate":
        return [
            f"On boot, the sketch loads saved calibration offsets and shows status on the OLED.",
            f"Sensor samples on {s_pin}; display updates every loop with current value and mode.",
            "Press the mode button to toggle manual override vs automatic threshold control.",
            f"Watchdog-style checks prevent relay chatter when readings hover near the cutoff.",
        ]
    return [
        "ESP32 joins Wi-Fi and exposes readings through a lightweight web page or MQTT topic.",
        f"Local {s_pin} sensing still runs on-device — cloud is optional for resilience.",
        "Rules engine evaluates thresholds, quiet hours, and repeat-alert intervals.",
        "Logs append timestamped events you can download or forward to Home Assistant.",
    ]


def level_apps(level: str, parent: dict) -> list[str]:
    cat = parent.get("category", "ESP32")
    if level == "beginner":
        return [
            f"First {cat.lower()} prototype on a breadboard",
            "Classroom demo of sense → decide → act",
            "Bench testing before permanent wiring",
        ]
    if level == "intermediate":
        return [
            "Field trial with visible OLED feedback",
            "Manual override for maintenance or testing",
            "Calibrated setup for daily use",
        ]
    return [
        "Remote monitoring from phone or laptop",
        "Automated alerts when limits are crossed",
        "Long-term trend logging for optimization",
    ]


def level_troubleshooting(level: str, parent: dict, hardware: dict) -> list[tuple[str, str]]:
    s_pin = hardware.get("sensor_pin", "GPIO34")
    common = [
        (
            "Serial Monitor shows no output",
            "Check USB cable, correct COM port, and baud rate 115200. Press EN/RST on the board after upload.",
        ),
        (
            f"Sensor readings stuck at 0 or 4095",
            f"Verify {s_pin} wiring, sensor VCC at 3.3 V, and that the module GND ties to ESP32 GND.",
        ),
    ]
    if level == "beginner":
        return common + [
            (
                "Output never turns on",
                "Lower THRESHOLD after logging normal vs trigger readings in Serial Monitor.",
            ),
        ]
    if level == "intermediate":
        return common + [
            (
                "OLED stays blank",
                "Confirm I2C address (usually 0x3C), SDA on GPIO21, SCL on GPIO22, and 3.3 V power.",
            ),
            (
                "Relay chatters near threshold",
                "Add hysteresis in code or increase SAMPLE_DELAY_MS slightly.",
            ),
        ]
    return common + [
        (
            "Wi-Fi connection fails",
            "Use 2.4 GHz SSID, check password in sketch, and ensure router allows new devices.",
        ),
        (
            "Dashboard loads but values frozen",
            "Confirm loop still reads sensor; avoid blocking HTTP handlers — use async or periodic refresh.",
        ),
    ]


def level_upgrades(level: str, parent: dict) -> list[str]:
    if level == "beginner":
        return [
            "Move to intermediate stage for OLED and manual/auto mode",
            "Add deep sleep between samples to save power",
            "Enclose in project box with labeled terminals",
        ]
    if level == "intermediate":
        return [
            "Jump to advanced stage for Wi-Fi dashboard and alerts",
            "Store calibration in EEPROM or Preferences library",
            "Add physical override switch on a dedicated GPIO",
        ]
    return [
        "Integrate with Home Assistant or MQTT broker",
        "Add OTA firmware updates for remote fixes",
        "Ship on custom PCB with regulated power supply",
    ]


def level_code(level: str, parent: dict, hardware: dict) -> str:
    title = parent["title"]
    sensor = gpio_num(hardware.get("sensor_pin", "GPIO34"))
    output = gpio_num(hardware.get("output_pin", "GPIO26"))
    sensor_label = parent.get("sensor", "sensor")
    if level == "beginner":
        return f"""// {title} — Beginner
const int SENSOR_PIN = {sensor};
const int OUTPUT_PIN = {output};
const int THRESHOLD = 1800;
const int SAMPLE_DELAY_MS = 500;

void setup() {{
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  Serial.println("Beginner stage ready");
}}

void loop() {{
  int reading = analogRead(SENSOR_PIN);
  Serial.print("{sensor_label}: ");
  Serial.println(reading);
  bool active = reading > THRESHOLD;
  digitalWrite(OUTPUT_PIN, active ? HIGH : LOW);
  delay(SAMPLE_DELAY_MS);
}}"""
    if level == "intermediate":
        return f"""// {title} — Intermediate
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int SENSOR_PIN = {sensor};
const int OUTPUT_PIN = {output};
const int BUTTON_PIN = 0;
const int THRESHOLD = 1800;
const int HYSTERESIS = 80;
bool autoMode = true;

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {{
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Wire.begin(21, 22);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.display();
}}

void loop() {{
  if (!digitalRead(BUTTON_PIN)) {{
    autoMode = !autoMode;
    delay(250);
  }}
  int reading = analogRead(SENSOR_PIN);
  bool active = autoMode ? (reading > THRESHOLD) : false;
  if (autoMode && reading < THRESHOLD - HYSTERESIS) active = false;
  digitalWrite(OUTPUT_PIN, active ? HIGH : LOW);
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(autoMode ? "AUTO" : "MANUAL");
  display.print("  Val:");
  display.println(reading);
  display.display();
  delay(300);
}}"""
    return f"""// {title} — Advanced
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASSWORD";
const int SENSOR_PIN = {sensor};
const int OUTPUT_PIN = {output};
const int THRESHOLD = 1800;
WebServer server(80);
unsigned long lastAlert = 0;

void handleRoot() {{
  int v = analogRead(SENSOR_PIN);
  String body = "<h1>{title}</h1><p>Reading: " + String(v) + "</p>";
  body += "<p>Output: " + String(digitalRead(OUTPUT_PIN) ? "ON" : "OFF") + "</p>";
  server.send(200, "text/html", body);
}}

void setup() {{
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(300);
  server.on("/", handleRoot);
  server.begin();
  Serial.println(WiFi.localIP());
}}

void loop() {{
  server.handleClient();
  int reading = analogRead(SENSOR_PIN);
  bool active = reading > THRESHOLD;
  digitalWrite(OUTPUT_PIN, active ? HIGH : LOW);
  if (active && millis() - lastAlert > 60000UL) {{
    Serial.println("ALERT: threshold crossed");
    lastAlert = millis();
  }}
  delay(200);
}}"""


def build_level(level: str, parent: dict, hardware: dict) -> dict:
    return {
        "level": level,
        "label": LEVEL_LABELS[level],
        "overview": level_overview(level, parent),
        "components": level_components(level, hardware, parent),
        "wiring": level_wiring(level, hardware, parent),
        "how": level_how(level, parent, hardware),
        "apps": level_apps(level, parent),
        "troubleshooting": level_troubleshooting(level, parent, hardware),
        "upgrades": level_upgrades(level, parent),
        "code": level_code(level, parent, hardware),
    }


def build_all_levels(parent: dict, hardware: dict) -> dict[str, dict]:
    return {lv: build_level(lv, parent, hardware) for lv in LEVELS}
