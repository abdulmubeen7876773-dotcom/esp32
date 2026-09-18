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
        "covers": "ESP32 AI projects on this site focus on camera-first edge experiments: the ESP32-CAM captures an image, the sketch or library processes that frame locally, then the project turns the result into a visible decision such as a QR payload, color match, camera stream, or face-detection demo. These are bounded computer-vision lessons, not desktop-class AI systems or certified recognition tools.",
        "start": "Begin by understanding what the ESP32-CAM can and cannot do, then verify camera capture before adding QR decoding, color/object detection, or face-detection demos. If a result looks wrong, test lighting, focus, frame size, and power before changing the model or code.",
        "skills": ["ESP32-CAM setup", "image capture", "local frame processing", "camera privacy", "memory and frame-size tradeoffs", "safe AI claim boundaries"],
        "watch": ["Treat recognition results as demonstrations, not safety decisions.", "Keep camera projects privacy-aware and avoid recording people without permission.", "Verify lighting, focus, power stability, and Wi-Fi reliability before judging model behavior."],
        "guides": [("Install Arduino IDE", "/guides/installing-arduino-ide-esp32.html"), ("ESP32 basics", "/guides/what-is-esp32.html")],
        "components": [("ESP32-CAM", "/components/esp32-cam.html"), ("ESP32 DevKit", "/components/esp32-devkit.html")],
        "related": [("ESP32-CAM", "/category/esp32-cam.html"), ("Security Projects", "/category/security-projects.html")],
        "progression": [
            ("Learn the board", "/components/esp32-cam.html", "Review the ESP32-CAM module, camera connector, upload mode, power needs, and why it behaves differently from a standard ESP32 DevKit."),
            ("Prepare the toolchain", "/guides/installing-arduino-ide-esp32.html", "Install the Arduino IDE and ESP32 board support before trying camera examples."),
            ("Capture a frame", "/projects/esp32-camera-capture-server.html", "Use the camera capture server to confirm the OV2640, Wi-Fi, and browser endpoint work."),
            ("Decode data", "/projects/esp32-cam-qr-scanner.html", "Move from raw image capture to a QR scanner that extracts a payload from a frame."),
            ("Detect a target", "/projects/esp32-ai-object-detector.html", "Try the color object detector to learn threshold-based local vision on ESP32-CAM hardware."),
            ("Compare face detection", "/projects/esp32-cam-face-detection.html", "Study face detection as a demonstration of finding face-like regions, not identity-grade face recognition."),
        ],
        "choose": [
            ("Beginner camera setup", "/projects/esp32-camera-capture-server.html", "Choose this first if you need to prove the camera, power supply, and Wi-Fi endpoint."),
            ("Networking and browser viewing", "/projects/esp32-camera-capture-server.html", "Use the capture server to understand how an ESP32-CAM serves images over Wi-Fi."),
            ("QR or data decoding", "/projects/esp32-cam-qr-scanner.html", "Use the QR scanner when the goal is decoding visual data rather than classifying objects."),
            ("Computer-vision experiment", "/projects/esp32-ai-object-detector.html", "Use the color detector for local thresholding and object/color decision logic."),
            ("Privacy-aware face demo", "/projects/esp32-cam-face-detection.html", "Use the face-detection page only as an educational demo, not an access-control or identity system."),
        ],
        "reality": [
            "ESP32-CAM boards have limited RAM and processing headroom compared with a phone, laptop, or cloud model.",
            "Many beginner examples are rule-based, threshold-based, or library-assisted computer vision rather than trained neural-network inference.",
            "Face detection means finding a face-like region. It is not the same as recognizing who a person is.",
            "Lighting, focus, motion blur, camera angle, JPEG size, and frame size materially change results.",
            "Camera and Wi-Fi current peaks can trigger brownouts unless the board has a stable 5 V supply and solid ground.",
        ],
        "troubleshooting": [
            "Camera init failed: confirm the AI-Thinker board profile, OV2640 ribbon seating, camera model, and pin map.",
            "Upload fails: hold GPIO0 low only for flashing, then release it before normal boot.",
            "Brownout or reboot loop: use a stable 5 V supply, short USB cable, and avoid weak breadboard power rails.",
            "Blank or noisy image: check lighting, focus, lens cover, ribbon cable, and selected frame size.",
            "Wi-Fi page does not load: confirm SSID/password, Serial Monitor IP address, and that the browser is on the same network.",
            "Detection is unstable: lower the frame size, improve lighting, simplify the threshold, and test one variable at a time.",
        ],
        "privacy": "Use camera projects in controlled demo spaces, get consent before pointing a camera at people, avoid private rooms, and do not present educational face-detection demos as identity, security, attendance, or surveillance-grade recognition.",
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

CATEGORY_DEEP_DETAILS = {
    "Agriculture": {
        "progression": [
            ("Read one sensor", "/projects/esp32-soil-moisture-monitor.html", "Start by proving soil readings in the actual pot, tray, or bed before any automated decision."),
            ("Compare sensor types", "/projects/esp32-soil-ph-monitor.html", "Use the soil pH monitor to see why calibration and probe care matter before trusting plant data."),
            ("Add climate context", "/projects/esp32-greenhouse-automation-controller.html", "Move from one soil value to a greenhouse controller that watches temperature and vent behaviour."),
            ("Make it connected", "/projects/esp32-smart-irrigation-system.html", "Use the irrigation project only after manual thresholds, pump wiring, and fail-safe behaviour are understood."),
        ],
        "choose": [
            ("Soil moisture first", "/projects/esp32-soil-moisture-monitor.html", "Best first build because it exposes ADC drift, wet/dry calibration, and threshold decisions."),
            ("Plant chemistry lesson", "/projects/esp32-soil-ph-monitor.html", "Choose this when the learning goal is calibration and slow-changing readings, not instant automation."),
            ("Greenhouse airflow", "/projects/esp32-greenhouse-automation-controller.html", "Use this when you want a low-voltage vent or fan-control model."),
            ("Watering automation", "/projects/esp32-smart-irrigation-system.html", "Choose this only after confirming pump power, common ground, and manual override behaviour."),
        ],
        "reality": [
            "Soil and greenhouse sensors vary with placement, probe condition, pot size, drainage, and sunlight.",
            "GPIO pins should switch a driver or relay input, not a pump, fan, or valve directly.",
            "Outdoor or damp setups need enclosures, strain relief, and separation between water and USB breadboards.",
        ],
        "troubleshooting": [
            "Soil readings never change: test the sensor in air, dry soil, and wet soil, then record the real ADC range before setting thresholds.",
            "Pump or vent does not move: verify the external supply, driver/relay input, common ground, and load current rating.",
            "Automatic watering cycles too often: add hysteresis or a minimum off-time after confirming the probe is not touching a wet pocket.",
        ],
    },
    "Display Projects": {
        "progression": [
            ("Learn I2C", "/guides/i2c-communication.html", "Understand SDA, SCL, pull-ups, and why many display problems are address or bus problems."),
            ("Wire the OLED", "/guides/connect-oled-esp32.html", "Connect a small SSD1306 display and confirm the address before drawing complex screens."),
            ("Print sensor data", "/guides/oled-display-esp32.html", "Move from simple text to readable labels, units, and refresh timing."),
            ("Build a clock", "/projects/esp32-oled-weather-clock.html", "Combine I2C display output with weather/time data in a complete visible project."),
        ],
        "choose": [
            ("Blank OLED fix", "/guides/connect-oled-esp32.html", "Use this when the hardware lights up but no pixels appear."),
            ("Display layout practice", "/guides/oled-display-esp32.html", "Use this when you need text, units, and screen updates that remain readable."),
            ("Time and weather screen", "/projects/esp32-oled-weather-clock.html", "Use this for a complete display build with NTP, timezone, and sensor context."),
            ("Matrix text output", "/projects/esp32-led-matrix-display.html", "Use this when the desired visual is a larger scrolling display instead of OLED status text."),
        ],
        "reality": [
            "Most ESP32 OLED examples use GPIO 21 for SDA and GPIO 22 for SCL unless the sketch says otherwise.",
            "SSD1306 modules often use address 0x3C, but some use 0x3D, so scanning the bus is more reliable than guessing.",
            "Small displays are good for status, units, and trends; they are not good places for dense wiring instructions.",
        ],
        "troubleshooting": [
            "Blank screen: run an I2C scanner, check 0x3C versus 0x3D, verify SDA/SCL order, and confirm the correct library constructor.",
            "Text flickers or smears: clear only the intended display area or reduce the refresh rate.",
            "Sensor values show but labels overlap: shorten labels, use fixed-width numeric fields, and avoid updating every loop iteration.",
        ],
    },
    "ESP32-CAM": {
        "progression": [
            ("Understand the module", "/components/esp32-cam.html", "Review the AI-Thinker pin map, camera ribbon, SD/flash constraints, and power needs."),
            ("Set up the IDE", "/guides/installing-arduino-ide-esp32.html", "Install ESP32 board support before choosing the ESP32-CAM board profile."),
            ("Serve a frame", "/projects/esp32-camera-capture-server.html", "Confirm capture, Wi-Fi, and browser viewing before adding detection logic."),
            ("Try vision tasks", "/projects/esp32-cam-qr-scanner.html", "Move into QR scanning, face detection, or color/object demos only after capture is stable."),
        ],
        "choose": [
            ("First camera test", "/projects/esp32-camera-capture-server.html", "Best first project because it isolates power, board profile, ribbon, and Wi-Fi endpoint issues."),
            ("QR workflow", "/projects/esp32-cam-qr-scanner.html", "Choose this when the input is a printed visual code, not a general object."),
            ("Privacy demo", "/projects/esp32-cam-face-detection.html", "Use this as a face-region demonstration, not identity recognition."),
            ("Security camera model", "/projects/esp32-security-camera-system.html", "Use this for local-network camera viewing with explicit non-certified security limits."),
        ],
        "reality": [
            "ESP32-CAM boards are more power-sensitive than ordinary ESP32 DevKit breadboard circuits.",
            "GPIO0 is for flashing mode only; leaving it grounded after upload prevents normal boot.",
            "The AI-Thinker camera pin map is board-specific and should not be generalized to all ESP32 boards.",
        ],
        "troubleshooting": [
            "Camera init failed: check AI-Thinker board selection, the OV2640 ribbon cable, the pin map, and stable 5 V power.",
            "Upload works but sketch will not run: remove the GPIO0-to-GND jumper and reset the board.",
            "Image is noisy or black: check lens cap, ribbon seating, lighting, frame size, and whether the board browns out during Wi-Fi activity.",
        ],
    },
    "Education": {
        "progression": [
            ("Explain the board", "/guides/what-is-esp32.html", "Start with pins, power, USB upload, and the difference between inputs and outputs."),
            ("Blink an LED", "/guides/blink-led-esp32.html", "Use one visible output before asking students to debug input wiring."),
            ("Add a button", "/guides/button-led-control.html", "Introduce pull-up or pull-down logic with one input and one output."),
            ("Use a trainer project", "/projects/esp32-learning-trainer.html", "Move to a repeatable classroom board once the single experiments make sense."),
        ],
        "choose": [
            ("First lesson", "/guides/blink-led-esp32.html", "Use this when learners need one predictable output and instant feedback."),
            ("Input reasoning", "/guides/digital-inputs-floating-pins.html", "Use this when learners see random button values or do not understand pull resistors."),
            ("Classroom board", "/projects/esp32-learning-trainer.html", "Use this for repeated lessons with the same inputs, outputs, and wiring reference."),
            ("Sound and timing", "/projects/esp32-digital-piano.html", "Use this when students are ready for buttons, timing, and audible feedback."),
        ],
        "reality": [
            "Beginner lessons work best when each experiment changes one variable at a time.",
            "Students should predict the Serial Monitor or LED behaviour before uploading new code.",
            "High-current loads, relays, and loose USB power setups are poor first-session material.",
        ],
        "troubleshooting": [
            "Nothing uploads: confirm the selected board, USB data cable, COM port, and boot button timing.",
            "Button readings jump: add or enable a pull-up/pull-down resistor and keep wires short.",
            "Classroom results differ: standardize board type, pin numbers, jumper colours, and library versions before comparing answers.",
        ],
    },
    "Energy Monitoring": {
        "progression": [
            ("Review analog input", "/guides/analog-inputs.html", "Understand ADC range and why raw readings need scaling before discussing energy values."),
            ("Read real-world signals", "/guides/reading-analog-sensors.html", "Practice smoothing and calibration on safe low-voltage signals."),
            ("Build a low-voltage meter", "/projects/esp32-smart-energy-meter.html", "Use a safe demo circuit to learn measurement display and logging."),
            ("Study AC boundaries", "/projects/esp32-ac-power-monitor.html", "Only then read the isolated AC-monitoring prototype and its safety limits."),
        ],
        "choose": [
            ("Low-voltage classroom build", "/projects/esp32-smart-energy-meter.html", "Choose this for display, logging, and calibration without exposed mains wiring."),
            ("AC current concept", "/projects/esp32-ac-power-monitor.html", "Choose this for isolated educational current monitoring with strict boundaries."),
            ("Industrial-style monitoring", "/projects/esp32-machine-monitoring-node.html", "Use this when the goal is event/status logging around equipment rather than power metering."),
        ],
        "reality": [
            "ESP32 ADC readings are educational unless the sensor, reference, calibration, and load are verified.",
            "Mains energy monitoring is not a breadboard beginner task.",
            "AC work needs isolation, enclosure, fusing, strain relief, and qualified review before real use.",
        ],
        "troubleshooting": [
            "Readings drift: repeat calibration with a known load and keep sensor wiring away from noisy switching loads.",
            "OLED or dashboard values look wrong: check scaling constants, ADC attenuation, and units before changing hardware.",
            "Circuit feels unsafe or unclear: stop and keep the project at low-voltage simulation level.",
        ],
    },
    "Environmental": {
        "progression": [
            ("Learn sensor placement", "/guides/environmental-sensors.html", "Start with why temperature, humidity, pressure, air, and UV readings change by location."),
            ("Understand I2C", "/guides/i2c-communication.html", "Use I2C basics before wiring BME280, OLED, or similar modules together."),
            ("Build weather sensing", "/projects/esp32-iot-weather-station.html", "Combine BME280-style readings with network or display output."),
            ("Add alerts carefully", "/projects/esp32-air-quality-monitor.html", "Move into air-quality thresholds only after understanding sensor warm-up and calibration limits."),
        ],
        "choose": [
            ("Weather and pressure", "/projects/esp32-iot-weather-station.html", "Use this for BME280 environmental data and connected logging."),
            ("Indoor air lesson", "/projects/esp32-air-quality-monitor.html", "Use this when the goal is relative air-quality changes, not certified safety detection."),
            ("Lightning demo", "/projects/esp32-lightning-detector.html", "Use this for AS3935 event behaviour and noise tuning."),
            ("UV estimate", "/projects/esp32-uv-index-monitor.html", "Use this for outdoor-sensor placement and educational calibration discussions."),
        ],
        "reality": [
            "Environmental sensors measure the conditions at the sensor, not the whole room, greenhouse, or city.",
            "Gas and air-quality modules need warm-up, calibration, and clear non-safety wording.",
            "Sensor placement near heat, fans, cases, sunlight, or damp surfaces can dominate the reading.",
        ],
        "troubleshooting": [
            "BME280 not found: scan for 0x76 or 0x77, check SDA/SCL, and confirm it is not a BMP280 when humidity is expected.",
            "Air-quality values jump: allow warm-up time, improve airflow, and compare relative trends rather than absolute claims.",
            "Readings differ from another device: compare placement, enclosure heat, sampling interval, and calibration assumptions.",
        ],
    },
    "Healthcare": {
        "progression": [
            ("Review sensing limits", "/guides/reading-analog-sensors.html", "Start with noise, sampling, and why raw biological signals need careful interpretation."),
            ("Display safely", "/guides/oled-display-esp32.html", "Learn to show values without implying diagnosis or certified accuracy."),
            ("View a waveform", "/projects/esp32-ecg-monitor.html", "Use the ECG project as an educational waveform viewer only."),
            ("Log a wellness signal", "/projects/esp32-pulse-oximeter-logger.html", "Use pulse-ox logging to discuss sensor placement and non-medical limitations."),
        ],
        "choose": [
            ("Waveform concept", "/projects/esp32-ecg-monitor.html", "Choose this to teach filtering, sampling, and display of a signal shape."),
            ("Wellness logging demo", "/projects/esp32-pulse-oximeter-logger.html", "Choose this to teach I2C sensor reads, logging, and data caution."),
            ("Classroom path", "/category/education.html", "Use education projects first if students are not ready for health-data boundaries."),
        ],
        "reality": [
            "These are educational electronics pages, not medical devices, monitors, diagnostic tools, or emergency systems.",
            "Body-signal modules are sensitive to placement, motion, loose wires, lighting, and sensor libraries.",
            "Health-related data deserves privacy even when the project is only a classroom demo.",
        ],
        "troubleshooting": [
            "Values freeze or look impossible: check sensor contact, supply voltage, I2C address, and library example compatibility.",
            "Waveform is noisy: reduce motion, shorten leads, verify ground/reference connections, and test with the module example first.",
            "A reading seems medically concerning: do not interpret the project; use appropriate medical advice or certified equipment.",
        ],
    },
    "Home Automation": {
        "progression": [
            ("Read the room", "/projects/esp32-home-climate-automation.html", "Start with sensor readings and local control before adding remote commands."),
            ("Control temperature", "/projects/esp32-smart-thermostat.html", "Use thermostat logic to learn thresholds, hysteresis, and manual override."),
            ("Add alerts", "/projects/esp32-water-leak-detector.html", "Use leak detection for safe low-voltage sensing and event response."),
            ("Use relays carefully", "/projects/esp32-smart-power-strip.html", "Study the simulator before adapting any relay project to real loads."),
        ],
        "choose": [
            ("Climate automation", "/projects/esp32-home-climate-automation.html", "Choose this for sensors, fan/relay decisions, and indoor thresholds."),
            ("Simple thermostat", "/projects/esp32-smart-thermostat.html", "Choose this when you need clear temperature-control logic and test steps."),
            ("Access control", "/projects/esp32-smart-door-lock.html", "Choose this for lock-control concepts with safety and fallback thinking."),
            ("Sound-triggered relay", "/projects/esp32-voice-controlled-relay.html", "Choose this for input-to-relay behaviour without voice-assistant claims."),
        ],
        "reality": [
            "Home automation pages should start as low-voltage bench prototypes.",
            "Relay contacts and relay input power are different parts of the system; GPIO cannot power household loads.",
            "A safe home build needs manual override, fail-safe default state, and enclosure planning.",
        ],
        "troubleshooting": [
            "Relay clicks but load does not respond: check the load supply path, COM/NO/NC wiring, and whether the demo is intentionally low-voltage.",
            "Temperature control chatters: add hysteresis and verify the sensor is not beside the fan, heater, or ESP32 regulator.",
            "Automation triggers at the wrong time: log raw sensor values first, then adjust thresholds after real observations.",
        ],
    },
    "Industrial Automation": {
        "progression": [
            ("Monitor one signal", "/projects/esp32-vibration-monitor.html", "Start with a non-invasive vibration or status signal before controlling equipment."),
            ("Track events", "/projects/esp32-rfid-inventory-tracker.html", "Use RFID movement logging to practice reliable event records."),
            ("Prototype motion safely", "/projects/esp32-cnc-controller.html", "Use the CNC controller as a low-voltage motion-control demo, not a production controller."),
            ("Add networking", "/projects/esp32-machine-monitoring-node.html", "Move status data to a dashboard only after local readings are stable."),
        ],
        "choose": [
            ("Condition monitoring", "/projects/esp32-vibration-monitor.html", "Choose this for machine-health style sensing without touching machine control wiring."),
            ("Inventory movement", "/projects/esp32-rfid-inventory-tracker.html", "Choose this for tag reads, event logs, and repeatable scan tests."),
            ("Motion-control concept", "/projects/esp32-cnc-controller.html", "Choose this only for bench-scale step/dir learning with safe drivers."),
            ("Status dashboard", "/projects/esp32-machine-monitoring-node.html", "Choose this for machine-state reporting rather than direct control."),
        ],
        "reality": [
            "ESP32 learning circuits must not be connected directly to industrial voltages, motor drives, or safety interlocks.",
            "Production machinery needs isolation, certified enclosures, emergency-stop design, and qualified review.",
            "Long wires and motors introduce noise, so input debouncing, shielding, and grounding matter more than in desk demos.",
        ],
        "troubleshooting": [
            "False vibration events: test mounting, threshold, sampling interval, and nearby motor noise separately.",
            "RFID misses scans: check antenna distance, tag orientation, SPI wiring, and whether the code reports failed reads.",
            "Motion output is erratic: confirm driver power, common ground, step/dir pins, and current limits before connecting a mechanism.",
        ],
    },
    "IoT Projects": {
        "covers": "ESP32 IoT projects on this site focus on practical connectivity patterns: Wi-Fi sensor nodes, MQTT dashboards, BLE advertising, LoRa packets, and local browser or network workflows that make hardware data visible beyond the USB cable.",
        "start": "Start with a Wi-Fi sensor project that prints clear Serial Monitor logs, then add MQTT, BLE, or LoRa only after the local reading and network connection are reliable.",
        "skills": ["Wi-Fi setup", "MQTT topics", "BLE advertising", "LoRa packet flow", "network debugging", "sensor data publishing"],
        "watch": ["Keep credentials out of shared sketches and screenshots.", "Use local test brokers or LAN pages before depending on cloud services.", "Plan reconnection, power stability, and enclosure needs before remote deployment."],
        "guides": [("ESP32 basics", "/guides/what-is-esp32.html"), ("Environmental sensors", "/guides/environmental-sensors.html"), ("I2C communication", "/guides/i2c-communication.html")],
        "components": [("ESP32 DevKit", "/components/esp32-devkit.html"), ("BME280", "/components/bme280.html"), ("DHT22", "/components/dht22.html")],
        "related": [("Sensor Projects", "/category/sensor-projects.html"), ("Home Automation", "/category/home-automation.html"), ("Smart City", "/category/smart-city.html")],
        "progression": [
            ("Connect to Wi-Fi", "/projects/esp32-iot-weather-station.html", "Start with a weather station because it combines sensor data and a clear network result."),
            ("Publish data", "/projects/esp32-mqtt-sensor-dashboard.html", "Use MQTT when you need a broker, topic names, and repeatable payloads."),
            ("Try local wireless", "/projects/esp32-ble-beacon.html", "Use BLE beacons to compare short-range advertising with Wi-Fi dashboards."),
            ("Go remote", "/projects/esp32-lora-remote-sensor-node.html", "Use LoRa when the lesson is low-rate long-range sensor packets."),
        ],
        "choose": [
            ("Wi-Fi sensor project", "/projects/esp32-iot-weather-station.html", "Best first connected sensor because the data is understandable and easy to verify."),
            ("MQTT dashboard", "/projects/esp32-mqtt-sensor-dashboard.html", "Choose this for broker, topic, retain, and payload debugging practice."),
            ("BLE beacon", "/projects/esp32-ble-beacon.html", "Choose this when the goal is advertising packets rather than internet dashboards."),
            ("LoRa node", "/projects/esp32-lora-remote-sensor-node.html", "Choose this for remote sensing where messages are small and infrequent."),
        ],
        "reality": [
            "IoT failures are often network, broker, credential, or power issues rather than sensor-code issues.",
            "Local dashboards and MQTT brokers are better first steps than cloud accounts for beginners.",
            "Battery and remote deployments need sleep, reconnection, and physical weather protection planning.",
        ],
        "troubleshooting": [
            "Wi-Fi does not connect: verify SSID/password, 2.4 GHz network support, signal strength, and Serial Monitor logs.",
            "MQTT publishes nothing: check broker address, port, topic spelling, client ID conflicts, and whether the broker is reachable from the same network.",
            "Remote node drops offline: measure supply voltage during radio transmit and add reconnection/backoff logging.",
        ],
    },
    "LED Projects": {
        "progression": [
            ("Blink one LED", "/guides/blink-led-esp32.html", "Start with one output so timing and polarity are easy to see."),
            ("Control brightness", "/guides/pwm-fundamentals.html", "Use PWM before moving to RGB fades, strips, or matrix effects."),
            ("Drive a matrix", "/projects/esp32-led-matrix-display.html", "Use matrix text when you want structured display output rather than room lighting."),
            ("Add music or patterns", "/projects/esp32-neopixel-music-visualizer.html", "Move into reactive LED effects only after power and timing are predictable."),
        ],
        "choose": [
            ("RGB patterns", "/projects/esp32-rgb-led-pattern-controller.html", "Choose this for simple colour states and button or code-controlled patterns."),
            ("Matrix display", "/projects/esp32-led-matrix-display.html", "Choose this for scrolling text and module timing."),
            ("Music visualizer", "/projects/esp32-neopixel-music-visualizer.html", "Choose this for amplitude-reactive LEDs and timing tradeoffs."),
            ("Display category", "/category/display-projects.html", "Use display projects if the output should show text or numbers instead of light effects."),
        ],
        "reality": [
            "Addressable LEDs can draw far more current than an ESP32 3V3 pin or USB regulator can safely provide.",
            "Long strips need external power, injection points, common ground, and brightness limits.",
            "Timing-sensitive LED libraries can conflict with blocking code or heavy network work.",
        ],
        "troubleshooting": [
            "First LED works but strip glitches: check common ground, data direction arrow, level compatibility, and power at the far end.",
            "ESP32 resets at high brightness: lower brightness, use an external supply, and estimate total LED current.",
            "Patterns stutter: remove long delays, separate animation state from input reading, and test one effect at a time.",
        ],
    },
    "Robotics": {
        "progression": [
            ("Learn PWM", "/guides/pwm-fundamentals.html", "Understand speed or servo-style pulse control before adding mechanical movement."),
            ("Measure distance", "/projects/esp32-distance-monitoring-system.html", "Use ultrasonic sensing to learn obstacle distance and level-shift cautions."),
            ("Follow a line", "/projects/esp32-line-following-robot.html", "Build a robot that turns sensor readings into motor decisions."),
            ("Add remote control", "/projects/esp32-wifi-robot-controller.html", "Move to browser or Wi-Fi control after motor direction and stop behaviour are reliable."),
        ],
        "choose": [
            ("Line follower", "/projects/esp32-line-following-robot.html", "Choose this for autonomous behaviour from floor sensors and motor outputs."),
            ("Wi-Fi robot", "/projects/esp32-wifi-robot-controller.html", "Choose this when the lesson is manual remote driving and network latency."),
            ("Robot arm", "/projects/esp32-robot-arm-controller.html", "Choose this for servo angles, power separation, and repeatable motion limits."),
            ("Distance sensing", "/projects/esp32-distance-monitoring-system.html", "Choose this for obstacle data before moving a robot toward objects."),
        ],
        "reality": [
            "Motors and servos need driver boards and external power; GPIO pins provide control signals, not motor current.",
            "Lift wheels or unload mechanisms for first tests so wrong direction or runaway code is safe to stop.",
            "Ultrasonic modules may expose 5 V echo signals, so check level reduction before connecting to ESP32 GPIO.",
        ],
        "troubleshooting": [
            "Robot spins instead of driving straight: test each motor direction separately and swap either motor leads or logic direction, not both.",
            "Servo jitters or resets the ESP32: use a separate servo supply, common ground, and reasonable movement limits.",
            "Distance readings are random: check trigger/echo wiring, level shifting, target angle, and library timing.",
        ],
    },
    "Security Projects": {
        "progression": [
            ("Read digital inputs", "/guides/digital-inputs-floating-pins.html", "Start by understanding stable input states before trusting alerts."),
            ("Debounce events", "/guides/debouncing-buttons.html", "Use debounce concepts for switches, doors, and repeated event triggers."),
            ("Detect motion", "/projects/esp32-motion-security-alert.html", "Build a PIR alert that logs and explains false positives."),
            ("Add identity input", "/projects/esp32-rfid-access-control-system.html", "Move to RFID only after local event behaviour is reliable."),
        ],
        "choose": [
            ("Motion alert", "/projects/esp32-motion-security-alert.html", "Choose this for PIR warm-up, trigger timing, and notification logic."),
            ("RFID access", "/projects/esp32-rfid-access-control-system.html", "Choose this for card UID checks and safe lock-control boundaries."),
            ("Camera demo", "/projects/esp32-security-camera-system.html", "Choose this for local-network viewing, not certified surveillance."),
            ("Door lock", "/projects/esp32-smart-door-lock.html", "Use this when the lesson includes actuator safety and manual fallback."),
        ],
        "reality": [
            "These projects are educational prototypes and not certified alarm, access-control, or surveillance systems.",
            "PIR sensors can trigger from heat, sunlight, pets, airflow, and warm-up behaviour.",
            "Locks and relays need fail-safe thinking, separate power, and physical fallback before any real doorway use.",
        ],
        "troubleshooting": [
            "PIR triggers constantly: allow warm-up, move it away from heat sources or windows, and log timestamps before changing code.",
            "RFID card is not detected: check SPI wiring, antenna distance, tag orientation, and library example output.",
            "Relay or lock behaves backward: verify active LOW/HIGH input logic, NO/NC contacts, and the load supply path.",
        ],
    },
    "Sensor Projects": {
        "progression": [
            ("Read analog values", "/guides/analog-inputs.html", "Start with ADC limits, input range, and why raw numbers need context."),
            ("Use real sensors", "/guides/reading-analog-sensors.html", "Practice calibration and smoothing before building a finished monitor."),
            ("Measure distance", "/projects/esp32-distance-monitoring-system.html", "Use HC-SR04-style sensing with echo-voltage caution."),
            ("Build environment projects", "/projects/esp32-iot-weather-station.html", "Move into BME280, DHT22, or other sensors once reading patterns are understood."),
        ],
        "choose": [
            ("Soil sensing", "/projects/esp32-soil-moisture-monitor.html", "Choose this for ADC calibration, wet/dry testing, and threshold behaviour."),
            ("Distance sensing", "/projects/esp32-distance-monitoring-system.html", "Choose this for timing-based sensing and echo wiring checks."),
            ("Gesture input", "/projects/esp32-gesture-recognition.html", "Choose this for I2C events and controlled sensor placement."),
            ("Weather sensing", "/projects/esp32-iot-weather-station.html", "Choose this for BME280-style temperature, pressure, humidity, and networking."),
        ],
        "reality": [
            "ESP32 sensor work begins with voltage compatibility and pin capability, not code.",
            "GPIO34, GPIO35, GPIO36, and GPIO39 are input-only and are useful for readings, not outputs.",
            "ADC sensors, I2C sensors, and pulse-timing sensors fail in different ways, so troubleshooting must match the interface.",
        ],
        "troubleshooting": [
            "ADC readings are noisy: check input voltage range, ground, wire length, sampling interval, and whether averaging hides real changes.",
            "I2C sensor missing: scan the bus, check SDA/SCL, and verify the module voltage and address.",
            "Digital sensor never changes: check pull-up/pull-down behaviour and confirm the pin is configured as input.",
        ],
    },
    "Smart City": {
        "progression": [
            ("Sense one condition", "/guides/analog-inputs.html", "Start with one threshold such as light, distance, or motion before calling it automation."),
            ("Control a visible output", "/guides/pwm-fundamentals.html", "Use PWM or relay-safe output lessons before scaling the idea to infrastructure models."),
            ("Build street lighting", "/projects/esp32-smart-street-light.html", "Use a street-light prototype to connect sensing, output, and threshold logic."),
            ("Add parking or safety nodes", "/projects/esp32-smart-parking-sensor.html", "Move to distance or alert nodes after the single-threshold project is stable."),
        ],
        "choose": [
            ("Street-light model", "/projects/esp32-smart-street-light.html", "Choose this for light-based decisions and visible output control."),
            ("Parking sensor", "/projects/esp32-smart-parking-sensor.html", "Choose this for ultrasonic distance and clear occupied/free states."),
            ("Fire alarm demo", "/projects/esp32-fire-alarm-system.html", "Choose this as an educational alert project, not a certified life-safety system."),
            ("Energy context", "/category/energy-monitoring.html", "Use energy-monitoring pages when the goal is measuring infrastructure loads."),
        ],
        "reality": [
            "Smart-city pages are scale-model learning projects, not public infrastructure equipment.",
            "Outdoor deployment changes power, enclosures, cable strain relief, weatherproofing, and sensor calibration.",
            "Safety or emergency examples must be labelled as educational and should not replace certified systems.",
        ],
        "troubleshooting": [
            "Street light turns on in daylight: test the raw light reading in the final enclosure and add hysteresis.",
            "Parking distance flickers: check echo wiring, target angle, timeout handling, and averaging.",
            "Alert project sounds at the wrong time: separate sensor warm-up, threshold choice, and output wiring in the test sequence.",
        ],
    },
}

for category_name, deep_details in CATEGORY_DEEP_DETAILS.items():
    CATEGORY_SEO_DETAILS.setdefault(category_name, {}).update(deep_details)


def linked_list(items: list[tuple[str, str]]) -> str:
    return "".join(f'<li><a href="{esc(href)}">{esc(label)}</a></li>' for label, href in items)


def category_context_html(cat: str, projects: list[dict]) -> str:
    details = CATEGORY_SEO_DETAILS.get(cat, {})
    if not details:
        return ""
    skills = "".join(f"<li>{esc(skill)}</li>" for skill in details.get("skills", []))
    watch = "".join(f"<li>{esc(item)}</li>" for item in details.get("watch", []))
    watch_html = f"<div><h3>Before you adapt it</h3><ul>{watch}</ul></div>" if watch else ""
    progression = details.get("progression", [])
    progression_html = ""
    if progression:
        items = "".join(
            f'<li><a href="{esc(href)}">{esc(label)}</a><span>{esc(note)}</span></li>'
            for label, href, note in progression
        )
        progression_html = f"""<section class="category-context category-context--deep">
      <h2>Learning progression</h2>
      <ol class="category-learning-steps">{items}</ol>
    </section>"""
    choose = details.get("choose", [])
    choose_html = ""
    if choose:
        items = "".join(
            f'<li><a href="{esc(href)}">{esc(label)}</a><span>{esc(note)}</span></li>'
            for label, href, note in choose
        )
        choose_html = f"""<section class="category-context category-context--deep">
      <h2>Choose the right project</h2>
      <ul class="category-learning-steps">{items}</ul>
    </section>"""
    reality = details.get("reality", [])
    troubleshooting = details.get("troubleshooting", [])
    privacy = details.get("privacy", "")
    reality_html = ""
    if reality or troubleshooting or privacy:
        reality_items = "".join(f"<li>{esc(item)}</li>" for item in reality)
        trouble_items = "".join(f"<li>{esc(item)}</li>" for item in troubleshooting)
        privacy_html = f"<p>{esc(privacy)}</p>" if privacy else ""
        reality_html = f"""<section class="category-context category-context--deep">
      <h2>Technical reality and troubleshooting</h2>
      <div class="category-context-grid">
        <div><h3>Limits to understand</h3><ul>{reality_items}</ul></div>
        <div><h3>Common failure checks</h3><ul>{trouble_items}</ul></div>
        <div><h3>Privacy boundary</h3>{privacy_html}</div>
      </div>
    </section>"""
    first_project = projects[0] if projects else None
    first_link = (
        f' A practical first build is <a href="../projects/{esc(first_project["slug"])}.html">{esc(first_project["title"])}</a>.'
        if first_project
        else ""
    )
    base_html = f"""<section class="category-context">
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
    return base_html + progression_html + choose_html + reality_html


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
