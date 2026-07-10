import re

LEVELS = ["beginner", "intermediate", "advanced"]
LEVEL_LABELS = {"beginner": "Beginner", "intermediate": "Intermediate", "advanced": "Advanced"}
ADC2_PINS = {0, 2, 4, 12, 13, 14, 15, 25, 26, 27}
ADC1_SAFE_PINS = {32, 33, 34, 35, 36, 39}
I2C_COMPONENT_HINTS = {
    "bme",
    "bmp",
    "oled",
    "ssd1306",
    "display",
    "as3935",
    "apds",
    "vl53",
    "tof",
    "rtc",
    "i2c",
}


def gpio_num(pin: str) -> int:
    m = re.search(r"(\d+)", pin or "34")
    return int(m.group(1)) if m else 34


def clean_label(text: str) -> str:
    t = re.sub(r"\s+(signal|control|module|device)$", "", text or "", flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    return t or "Component"


def _text_blob(parent: dict, hardware: dict) -> str:
    return " ".join(
        str(v or "")
        for v in (
            parent.get("slug"),
            parent.get("title"),
            parent.get("sensor"),
            parent.get("output"),
            hardware.get("sensor_name"),
            hardware.get("output_name"),
        )
    ).lower()


def project_kind(parent: dict, hardware: dict) -> str:
    blob = _text_blob(parent, hardware)
    if "distance" in blob or "ultrasonic" in blob or "hc-sr04" in blob:
        return "ultrasonic"
    if "max3010" in blob or "pulse oximeter" in blob or "spo2" in blob:
        return "i2c_pulse"
    if "ws2812" in blob or "neopixel" in blob or "rgb led pattern" in blob:
        return "neopixel"
    if "push button" in blob or "button" in blob:
        return "button"
    if "pir" in blob or "motion sensor" in blob:
        return "digital"
    return "analog"


def is_i2c_component(label: str) -> bool:
    low = (label or "").lower()
    return any(hint in low for hint in I2C_COMPONENT_HINTS)


def sanitize_wiring_rows(rows: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    cleaned: list[tuple[str, str, str]] = []
    pending_invalid_i2c = False
    for comp, pin, note in rows:
        comp_low = (comp or "").lower()
        pin_low = (pin or "").lower()
        is_bus_row = "sda" in comp_low or "scl" == comp_low.strip() or "scl" in comp_low
        uses_i2c_pin = pin_low in {"gpio21", "gpio22"}
        if is_bus_row and uses_i2c_pin and not is_i2c_component(comp):
            pending_invalid_i2c = True
            continue
        if pending_invalid_i2c and uses_i2c_pin and comp_low.strip() in {"scl", "sda"}:
            continue
        pending_invalid_i2c = False
        cleaned.append((comp, pin, note))
    return cleaned


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
    return sanitize_wiring_rows(rows)


def ultrasonic_wiring(level: str) -> list[tuple[str, str, str]]:
    rows = [
        ("HC-SR04 TRIG", "GPIO5", "Digital trigger output"),
        ("HC-SR04 ECHO", "GPIO18", "Digital echo input via 10 kOhm / 20 kOhm divider"),
        ("Buzzer +", "GPIO25", "Alert output"),
        ("HC-SR04 VCC", "5V", "Sensor power"),
        ("GND", "GND", "Common ground"),
    ]
    if level in {"intermediate", "advanced"}:
        rows.extend(
            [
                ("OLED SDA", "GPIO21", "I2C data for 0.96\" display"),
                ("OLED SCL", "GPIO22", "I2C clock"),
            ]
        )
    if level == "advanced":
        rows.append(("Wi-Fi", "Built-in", "2.4 GHz - no extra wiring"))
    return rows


def level_wiring(level: str, hardware: dict, parent: dict) -> list[tuple[str, str, str]]:
    kind = project_kind(parent, hardware)
    if kind == "ultrasonic":
        return ultrasonic_wiring(level)[:10]
    if kind == "i2c_pulse":
        rows = [
            ("MAX30102 SDA", "GPIO21", "I2C data"),
            ("MAX30102 SCL", "GPIO22", "I2C clock"),
            ("MAX30102 VCC", "3.3V", "Sensor power"),
            ("GND", "GND", "Common ground"),
        ]
        if level in {"intermediate", "advanced"}:
            rows.extend([("OLED SDA", "GPIO21", "Shared I2C data"), ("OLED SCL", "GPIO22", "Shared I2C clock")])
        if level == "advanced":
            rows.append(("Wi-Fi", "Built-in", "2.4 GHz - no extra wiring"))
        return rows[:10]
    if kind == "neopixel":
        rows = [
            ("WS2812B DIN", "GPIO13", "One-wire LED data output"),
            ("Push button", "GPIO14", "Digital input using INPUT_PULLUP"),
            ("LED strip 5V", "5V external", "Use a separate 5 V supply for the strip"),
            ("GND", "GND", "Common ground between ESP32 and LED supply"),
        ]
        if level == "advanced":
            rows.append(("Wi-Fi", "Built-in", "2.4 GHz - no extra wiring"))
        return rows[:10]
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
    if project_kind(parent, hardware) == "ultrasonic":
        parts = base + [
            "HC-SR04 ultrasonic distance sensor",
            "10 kOhm resistor",
            "20 kOhm resistor",
            "Active buzzer",
        ]
        if level in {"intermediate", "advanced"}:
            parts.append("0.96\" I2C OLED display")
        return parts
    if project_kind(parent, hardware) == "i2c_pulse":
        parts = base + ["MAX30102 pulse oximeter module"]
        if level in {"intermediate", "advanced"}:
            parts.append("0.96\" I2C OLED display")
        return parts
    if project_kind(parent, hardware) == "neopixel":
        return base + [
            "WS2812B LED strip or NeoPixel ring",
            "Tactile push button",
            "External 5 V LED supply",
            "330 ohm data resistor",
            "1000 uF capacitor across LED 5 V and GND",
        ]
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
    if project_kind(parent, {}) == "ultrasonic":
        if level == "beginner":
            return (
                f"This beginner stage of {title} uses an HC-SR04 ultrasonic sensor. "
                "The ESP32 sends a trigger pulse, measures the echo pulse width, converts it to centimeters, "
                "and sounds a buzzer when an object is closer than the configured limit."
            )
        if level == "intermediate":
            return (
                "The intermediate stage keeps the HC-SR04 timing circuit and adds OLED feedback so distance, "
                "threshold, and alert state are visible without a computer."
            )
        return (
            f"The advanced stage connects {title} to Wi-Fi while keeping distance measurement local. "
            "GPIO5 drives TRIG, GPIO18 reads the divided ECHO signal, and the dashboard reports measured centimeters."
        )
    if project_kind(parent, {}) == "i2c_pulse":
        return (
            f"This stage of {title} reads a MAX30102 module over the ESP32 I2C bus on GPIO21/GPIO22. "
            "It logs raw red/IR samples for education only; it is not a medical instrument."
        )
    if project_kind(parent, {}) == "neopixel":
        return (
            f"This stage of {title} drives WS2812B LEDs from one data pin and uses a push button for pattern changes. "
            "The LED strip uses a separate 5 V supply with common ground."
        )
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
    kind = project_kind(parent, hardware)
    if kind == "ultrasonic":
        return [
            "GPIO5 sends a 10 microsecond pulse to the HC-SR04 TRIG pin.",
            "The HC-SR04 drives ECHO high for the sound travel time; GPIO18 reads that pulse through a 10 kOhm / 20 kOhm divider.",
            "The sketch converts pulse width to distance in centimeters.",
            "GPIO25 drives the buzzer when distance is below DISTANCE_LIMIT_CM.",
        ]
    if kind == "i2c_pulse":
        return [
            "Wire MAX30102 SDA to GPIO21 and SCL to GPIO22.",
            "The sketch starts the I2C bus and checks that the sensor responds.",
            "Raw red and IR values are printed to Serial Monitor for educational logging.",
            "Keep the project clearly labeled as non-medical and do not use it for diagnosis or monitoring.",
        ]
    if kind == "neopixel":
        return [
            "GPIO13 sends WS2812B data to the LED strip DIN pin.",
            "GPIO14 reads the push button using INPUT_PULLUP.",
            "Each button press advances the color pattern.",
            "The ESP32 and LED supply share GND, but the LED current comes from the external 5 V supply.",
        ]
    if kind in {"button", "digital"}:
        active_text = "LOW when pressed" if kind == "button" else "HIGH when motion is detected"
        return [
            f"The ESP32 reads the {parent.get('sensor', 'digital input')} on {s_pin}.",
            f"The input is treated as a digital signal: {active_text}.",
            f"When the active state is detected, {o_pin} drives the {parent.get('output', 'output')} HIGH.",
            "Serial Monitor at 115200 baud shows live state changes for debugging.",
        ]
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
    sensor_num = gpio_num(s_pin)
    kind = project_kind(parent, hardware)
    if kind == "ultrasonic":
        common = [
            (
                "Serial Monitor shows no distance",
                "Check TRIG on GPIO5, ECHO on GPIO18, common ground, and 115200 baud.",
            ),
            (
                "Readings jump or show zero",
                "Keep the target flat, stay within the sensor range, and verify the ECHO divider uses 10 kOhm and 20 kOhm resistors.",
            ),
        ]
        if level == "beginner":
            return common + [("Buzzer never sounds", "Move an object closer than DISTANCE_LIMIT_CM and verify buzzer + is on GPIO25.")]
        return common + [
            ("OLED stays blank", "Confirm I2C address (usually 0x3C), SDA on GPIO21, SCL on GPIO22, and 3.3 V power."),
            ("Wi-Fi dashboard works but distance freezes", "Avoid blocking handlers; keep the distance read in the main loop or a timed task."),
        ]
    if kind == "i2c_pulse":
        return [
            ("Sensor not found", "Confirm MAX30102 SDA on GPIO21, SCL on GPIO22, 3.3 V power, and common ground."),
            ("Values do not change", "Place a finger gently on the sensor window and shield it from strong room light."),
            ("Medical readings look wrong", "Do not use this build for medical readings; it logs educational raw samples only."),
        ]
    if kind == "neopixel":
        return [
            ("LEDs stay dark", "Check the external 5 V supply, common ground, strip direction arrow, and GPIO13 to DIN."),
            ("Colors flicker", "Add a 330 ohm data resistor and a 1000 uF capacitor across LED 5 V and GND."),
            ("Button skips patterns", "Add debounce timing or verify the button connects GPIO14 to GND when pressed."),
        ]
    if kind in {"button", "digital"}:
        common = [
            (
                "Serial Monitor shows no state changes",
                f"Verify the signal wire is on {s_pin}, GND is shared, and the input module is powered correctly.",
            ),
            (
                "Output never turns on",
                f"Confirm {hardware.get('output_pin', 'GPIO26')} is wired to the output input or LED resistor, then test with a simple blink sketch.",
            ),
        ]
        if kind == "button":
            common.append(("Button reads backward", "This sketch uses INPUT_PULLUP, so an open button reads HIGH and a pressed button reads LOW."))
        return common
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
    advanced = common + [
        (
            "Wi-Fi connection fails",
            "Use 2.4 GHz SSID, check password in sketch, and ensure router allows new devices.",
        ),
        (
            "Dashboard loads but values frozen",
            "Confirm loop still reads sensor; avoid blocking HTTP handlers — use async or periodic refresh.",
        ),
    ]
    if sensor_num in ADC2_PINS:
        advanced.append(
            (
                "Analog readings become unreliable after Wi-Fi connects",
                f"{s_pin} is on ESP32 ADC2. ADC2 analog reads can be unreliable while Wi-Fi is active. For a Wi-Fi-enabled version, move the analog sensor to an ADC1 pin such as GPIO34, GPIO35, GPIO36, or GPIO39 and update the code.",
            )
        )
    return advanced


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
    kind = project_kind(parent, hardware)
    if kind == "ultrasonic":
        wifi = '#include <WiFi.h>\n#include <WebServer.h>\n\n' if level == "advanced" else ""
        server_decl = (
            'const char* WIFI_SSID = "YOUR_SSID";\nconst char* WIFI_PASS = "YOUR_PASSWORD";\nWebServer server(80);\n\n'
            if level == "advanced"
            else ""
        )
        server_setup = (
            '  WiFi.begin(WIFI_SSID, WIFI_PASS);\n'
            '  while (WiFi.status() != WL_CONNECTED) delay(300);\n'
            '  server.on("/", []() {\n'
            '    server.send(200, "text/plain", "Distance: " + String(readDistanceCm()) + " cm");\n'
            '  });\n'
            '  server.begin();\n'
            '  Serial.println(WiFi.localIP());\n'
            if level == "advanced"
            else ""
        )
        server_loop = "  server.handleClient();\n" if level == "advanced" else ""
        return f"""// {title} - HC-SR04 distance monitor
{wifi}const int TRIG_PIN = 5;
const int ECHO_PIN = 18;
const int BUZZER_PIN = 25;
const int DISTANCE_LIMIT_CM = 20;
const int SAMPLE_DELAY_MS = 250;
{server_decl}long readDistanceCm() {{
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return -1;
  return duration / 58;
}}

void setup() {{
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
{server_setup}}}

void loop() {{
{server_loop}  long distanceCm = readDistanceCm();
  Serial.print("Distance cm: ");
  Serial.println(distanceCm);
  bool tooClose = distanceCm > 0 && distanceCm < DISTANCE_LIMIT_CM;
  digitalWrite(BUZZER_PIN, tooClose ? HIGH : LOW);
  delay(SAMPLE_DELAY_MS);
}}"""
    if kind == "i2c_pulse":
        return f"""// {title} - MAX30102 educational logger
#include <Wire.h>
#include "MAX30105.h"

MAX30105 sensor;

void setup() {{
  Serial.begin(115200);
  Wire.begin(21, 22);
  if (!sensor.begin(Wire, I2C_SPEED_STANDARD)) {{
    Serial.println("MAX30102 not found. Check SDA/SCL wiring.");
    while (true) delay(1000);
  }}
  sensor.setup();
  Serial.println("Educational raw red/IR logging only - not medical data.");
}}

void loop() {{
  long red = sensor.getRed();
  long ir = sensor.getIR();
  Serial.print("Red: ");
  Serial.print(red);
  Serial.print(" IR: ");
  Serial.println(ir);
  delay(250);
}}"""
    if kind == "neopixel":
        return f"""// {title} - WS2812B pattern controller
#include <Adafruit_NeoPixel.h>

const int LED_PIN = 13;
const int BUTTON_PIN = 14;
const int LED_COUNT = 16;
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int pattern = 0;
bool lastButton = HIGH;

void showPattern() {{
  uint32_t colors[] = {{
    strip.Color(255, 0, 0),
    strip.Color(0, 255, 0),
    strip.Color(0, 0, 255),
    strip.Color(255, 180, 0)
  }};
  strip.fill(colors[pattern % 4]);
  strip.show();
}}

void setup() {{
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  strip.begin();
  strip.setBrightness(40);
  showPattern();
}}

void loop() {{
  bool button = digitalRead(BUTTON_PIN);
  if (lastButton == HIGH && button == LOW) {{
    pattern++;
    showPattern();
    Serial.print("Pattern: ");
    Serial.println(pattern % 4);
    delay(200);
  }}
  lastButton = button;
}}"""
    if kind in {"button", "digital"}:
        active_expr = "!digitalRead(INPUT_PIN)" if kind == "button" else "digitalRead(INPUT_PIN) == HIGH"
        mode = "INPUT_PULLUP" if kind == "button" else "INPUT"
        active_label = "pressed" if kind == "button" else "active"
        return f"""// {title} - digital input monitor
const int INPUT_PIN = {sensor};
const int OUTPUT_PIN = {output};
const int SAMPLE_DELAY_MS = 50;

void setup() {{
  Serial.begin(115200);
  pinMode(INPUT_PIN, {mode});
  pinMode(OUTPUT_PIN, OUTPUT);
  digitalWrite(OUTPUT_PIN, LOW);
}}

void loop() {{
  bool active = {active_expr};
  Serial.print("{sensor_label}: ");
  Serial.println(active ? "{active_label}" : "idle");
  digitalWrite(OUTPUT_PIN, active ? HIGH : LOW);
  delay(SAMPLE_DELAY_MS);
}}"""
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


def _merge_imported_level(level: str, parent: dict, hardware: dict, imported: dict) -> dict:
    base = build_level(level, parent, hardware)
    if imported.get("overview_html"):
        base["overview_html"] = imported["overview_html"]
    if imported.get("components"):
        base["components"] = imported["components"]
    if imported.get("wiring"):
        rows = imported["wiring"]
        if rows and isinstance(rows[0], dict):
            base["wiring"] = [(r.get("component", ""), r.get("pin", ""), r.get("note", "")) for r in rows]
        else:
            base["wiring"] = rows
        base["wiring"] = sanitize_wiring_rows(base["wiring"])
    if imported.get("how"):
        base["how"] = imported["how"]
    if imported.get("apps"):
        base["apps"] = imported["apps"]
    if imported.get("troubleshooting"):
        base["troubleshooting"] = [
            (t["problem"], t["fix"]) if isinstance(t, dict) else t
            for t in imported["troubleshooting"]
        ]
    if imported.get("upgrades"):
        base["upgrades"] = imported["upgrades"]
    if imported.get("code"):
        base["code"] = imported["code"]
    kind = project_kind(parent, hardware)
    if kind in {"ultrasonic", "button", "digital", "i2c_pulse", "neopixel"}:
        # Imported legacy pages often used the generic analog threshold sketch.
        # Regenerate these archetypes so wiring, code, and explanation agree.
        corrected = build_level(level, parent, hardware)
        base["overview"] = corrected["overview"]
        base["overview_html"] = ""
        base["components"] = corrected["components"]
        base["wiring"] = corrected["wiring"]
        base["how"] = corrected["how"]
        base["troubleshooting"] = corrected["troubleshooting"]
        base["code"] = corrected["code"]
    return base


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
    imported_levels = parent.get("levels") or {}
    result = {}
    for lv in LEVELS:
        raw = imported_levels.get(lv) if isinstance(imported_levels, dict) else None
        if isinstance(raw, dict) and raw.get("code"):
            result[lv] = _merge_imported_level(lv, parent, hardware, raw)
        else:
            result[lv] = build_level(lv, parent, hardware)
    return result
