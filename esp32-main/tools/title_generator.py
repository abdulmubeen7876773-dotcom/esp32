import re

from site_layout import normalize_terms

WORD_CASE = {
    "iot": "IoT",
    "esp32": "ESP32",
    "wifi": "WiFi",
    "mqtt": "MQTT",
    "ota": "OTA",
    "gpio": "GPIO",
    "adc": "ADC",
    "i2c": "I2C",
    "spi": "SPI",
    "uart": "UART",
    "nfc": "NFC",
    "rfid": "RFID",
    "lcd": "LCD",
    "oled": "OLED",
    "bme280": "BME280",
    "dht11": "DHT11",
    "dht22": "DHT22",
    "mq135": "MQ135",
}


def title_word(w: str) -> str:
    return WORD_CASE.get(w.lower(), w.capitalize())


GENERIC_USE = [
    "Home Lab", "Prototype", "Workshop", "Maker Bench", "Starter Kit", "Weekend Build",
    "Classroom Demo", "Field Test", "Bench Setup", "Compact Node", "Portable Unit",
    "Battery-Powered", "Solar-Ready", "Indoor Setup", "Outdoor Ready", "Modular Build",
    "Budget Build", "Advanced Build", "Quick Start", "Hands-On Lab", "Reference Design",
    "Mini System", "Smart Node", "Edge Device", "IoT Node", "Dev Board", "Custom PCB",
    "Breadboard", "Production Test", "Pilot Unit", "Scaled Demo", "Real-World Test",
    "Embedded Lab", "Firmware Test", "Sensor Node", "Control Unit", "Gateway Node",
    "Monitoring Kit", "Automation Box", "Telemetry Unit", "Alert Node",
]

USE_CASES = {
    "Agriculture": [
        "Greenhouse", "Farm Field", "Garden Bed", "Hydroponic Rack", "Crop Monitoring",
        "Drip Irrigation", "Sprinkler Zone", "Plant Nursery", "Vertical Farm", "Soil Bed",
        "Irrigation Line", "Polytunnel", "Orchard Row", "Balcony Garden", "Rooftop Farm",
        "Seedling Tray", "Compost Zone", "Water Tank", "Pump Station", "Field Plot",
        "Smart Farm", "Agri IoT", "Crop Care", "Harvest Zone", "Fertigation Line",
        "Rainwater Tank", "Livestock Barn", "Aquaponics", "Irrigation Valve", "Moisture Zone",
        "Plant Care", "Farm Gate", "Green Patch", "Soil Plot", "Watering Lane",
    ],
    "Home Automation": [
        "Living Room", "Bedroom", "Kitchen", "Garage", "Smart Home", "Apartment",
        "Climate Zone", "HVAC Room", "Hallway", "Home Office", "Guest Room",
        "Utility Room", "Basement", "Attic Fan", "Window Zone", "Door Entry",
        "Lighting Zone", "Fan Control", "Thermostat", "Humidity Room", "Air Comfort",
        "Home Hub", "Room Node", "Family Home", "Flat Automation", "Comfort Control",
        "Daily Routine", "Night Mode", "Morning Setup", "Energy Save", "Remote Home",
        "Vacation Mode", "Smart Flat", "House Panel", "Room Monitor",
    ],
    "Security Projects": [
        "Front Door", "Backyard", "Driveway", "Perimeter", "Window Alert", "Gate Entry",
        "Garage Door", "Night Watch", "Intrusion Zone", "Motion Zone", "Secure Room",
        "Office Door", "Warehouse Bay", "Parking Lot", "Fence Line", "Hall Monitor",
        "Alarm Panel", "Entry Sensor", "Guard Post", "Safe Room", "Locker Area",
        "Shop Front", "Storage Room", "Access Point", "Surveillance", "Panic Alert",
        "Doorbell Cam", "PIR Zone", "Secure Cabinet", "Asset Guard", "Site Security",
        "Remote Alert", "Perimeter Scan", "Entry Watch", "Motion Guard",
    ],
    "IoT Projects": [
        "Cloud Dashboard", "Remote Monitor", "Telemetry Hub", "MQTT Node", "Data Logger",
        "Weather Node", "Sensor Hub", "Internet Gateway", "Live Dashboard", "API Client",
        "Web Portal", "Mobile Sync", "Fleet Monitor", "Edge Upload", "Real-Time Feed",
        "IoT Cloud", "Network Node", "Smart Upload", "Field Gateway", "Signal Bridge",
        "Device Sync", "Metrics Node", "Status Panel", "Online Monitor", "Stream Node",
        "Connected Hub", "Remote Panel", "Sensor Cloud", "Link Node", "Publish Node",
        "Subscribe Hub", "Data Stream", "Live Metrics", "Cloud Node", "IoT Bridge",
    ],
    "Sensor Projects": [
        "Distance Check", "Level Monitor", "Analog Read", "Digital Trigger", "Threshold Alert",
        "Signal Logger", "Value Tracker", "Range Finder", "Touch Detect", "Light Sense",
        "Sound Level", "Vibration Pickup", "Pressure Read", "Flow Monitor", "Heat Detect",
        "Motion Trace", "Pulse Count", "ADC Logger", "GPIO Scan", "Edge Trigger",
        "Sample Loop", "Calibration Test", "Raw Data Log", "Sensor Sweep", "Input Scan",
        "Field Sensor", "Probe Read", "Meter Node", "Gauge Monitor", "Sense Module",
        "Input Logger", "Signal Plot", "Value Chart", "Sense Lab", "Probe Test",
    ],
    "Robotics": [
        "Line Follower", "Obstacle Bot", "RC Rover", "Motor Driver", "Servo Arm",
        "Wheel Base", "Remote Rover", "Mini Bot", "Track Robot", "Gripper Arm",
        "Mobile Base", "Drive Unit", "Steering Bot", "Autonomous Cart", "Motor Control",
        "Robot Car", "PWM Drive", "Encoder Bot", "Chassis Control", "Bot Platform",
        "Motor Test", "Drive Train", "Wheel Control", "Arm Node", "Rover Link",
        "Bot Brain", "Motor Hub", "Steering Node", "Drive Bot", "RC Platform",
        "Robot Node", "Motor Lab", "Servo Test", "Bot Control", "Rover Drive",
    ],
    "Industrial Automation": [
        "Machine Line", "Factory Node", "Conveyor Belt", "Motor Panel", "Process Unit",
        "Plant Floor", "Assembly Line", "Quality Check", "Load Monitor", "Shift Logger",
        "Equipment Hub", "Line Sensor", "Batch Control", "Tool Monitor", "Safety Interlock",
        "PLC Bridge", "Status Tower", "Machine Health", "Output Line", "Process Monitor",
        "Industrial IoT", "Line Tracker", "Factory Gate", "Machine Alert", "Ops Panel",
        "Plant Node", "Line Control", "Machine Watch", "Factory Link", "Process Node",
        "Line Logger", "Machine Sync", "Plant Monitor", "Ops Node", "Industrial Hub",
    ],
    "LED Projects": [
        "RGB Strip", "Neon Panel", "Matrix Display", "Pattern Light", "Color Fade",
        "Stage Light", "Desk Glow", "Ambient Lamp", "Signal Tower", "Status LED",
        "Pixel Strip", "Light Show", "Color Wheel", "Night Lamp", "Bar Graph LED",
        "Festival Light", "Glow Panel", "Pulse Light", "Rainbow Strip", "Mood Light",
        "LED Wall", "Color Node", "Light Pattern", "Display Strip", "Glow Board",
        "Pixel Node", "RGB Panel", "Light Lab", "Color Pulse", "Strip Control",
        "LED Scene", "Glow Strip", "Color Mix", "Light Node", "RGB Demo",
    ],
    "ESP32-CAM": [
        "Video Stream", "Snapshot Node", "Motion Capture", "Remote Cam", "Web Stream",
        "Timelapse Cam", "Door Cam", "Security Cam", "Live Feed", "Image Server",
        "Frame Capture", "Stream Server", "Vision Node", "Camera Hub", "Photo Trigger",
        "Face Detect", "Room Cam", "Yard Cam", "Cam Portal", "JPEG Stream",
        "Vision Stream", "Cam Server", "Live Cam", "Frame Hub", "Capture Node",
        "Remote Vision", "Cam Link", "Stream Hub", "Photo Node", "Video Node",
        "Cam Monitor", "Image Hub", "Live Vision", "Cam Logger", "Stream Cam",
    ],
    "AI Projects": [
        "TinyML Demo", "Sound Classifier", "Edge Inference", "Voice Trigger", "Pattern Detect",
        "Signal Classify", "On-Device AI", "Micro Model", "Audio AI", "Feature Extract",
        "Smart Detect", "Edge Model", "AI Sensor", "Classify Node", "Inference Hub",
        "Model Test", "AI Lab", "Edge Classify", "Signal AI", "Audio Model",
        "Tiny Model", "AI Node", "Smart Edge", "Classify Lab", "Inference Test",
        "Edge AI", "Model Node", "Audio Classify", "AI Demo", "Signal Model",
        "Tiny Inference", "AI Edge", "Classify Demo", "Model Hub", "Smart Classify",
    ],
    "Energy Monitoring": [
        "Power Meter", "Load Monitor", "Current Sense", "Voltage Track", "Energy Logger",
        "Solar Panel", "Battery Monitor", "Grid Watch", "Watt Logger", "Usage Tracker",
        "Power Node", "Energy Hub", "Load Logger", "Meter Node", "Power Track",
        "Energy Scan", "Usage Node", "Watt Monitor", "Load Sense", "Power Logger",
        "Energy Plot", "Meter Hub", "Current Logger", "Voltage Node", "Power Lab",
        "Energy Test", "Load Track", "Usage Logger", "Watt Node", "Meter Scan",
        "Power Scan", "Energy Node", "Load Hub", "Usage Track", "Watt Hub",
    ],
    "Healthcare": [
        "Vital Logger", "Pulse Monitor", "SpO2 Tracker", "Patient Node", "Health Logger",
        "Bedside Monitor", "Wearable Node", "Clinic Demo", "Wellness Track", "Bio Signal",
        "Heart Rate", "Health Hub", "Vital Node", "Care Monitor", "Pulse Logger",
        "Health Scan", "Patient Monitor", "Vital Track", "Care Node", "Wellness Node",
        "Bio Logger", "Pulse Node", "Health Track", "Care Logger", "Vital Hub",
        "Patient Logger", "Wellness Hub", "Bio Monitor", "Care Track", "Health Node",
        "Pulse Track", "Vital Scan", "Care Hub", "Wellness Logger", "Bio Track",
    ],
    "Environmental": [
        "Air Quality", "Gas Monitor", "Climate Node", "Pollution Track", "Ventilation",
        "Indoor Air", "Outdoor Air", "CO2 Logger", "Smoke Alert", "Fresh Air",
        "Air Logger", "Gas Node", "Climate Track", "Air Hub", "Vent Control",
        "Air Scan", "Gas Logger", "Climate Logger", "Air Node", "Pollution Node",
        "Fresh Air Hub", "Air Track", "Gas Track", "Climate Hub", "Air Monitor",
        "Vent Node", "Gas Hub", "Air Sense", "Climate Monitor", "Pollution Logger",
        "Air Lab", "Gas Scan", "Climate Sense", "Air Probe", "Vent Logger",
    ],
    "Smart City": [
        "Street Light", "Traffic Node", "Parking Sensor", "City Lamp", "Public IoT",
        "Urban Node", "Smart Pole", "Crosswalk", "City Monitor", "Street Sensor",
        "Urban Hub", "City Logger", "Street Node", "Smart City", "Public Node",
        "City Link", "Street Hub", "Urban Logger", "City Node", "Street Track",
        "Smart Pole Node", "City Sense", "Urban Track", "Street Logger", "City Hub",
        "Public Hub", "Street Scan", "Urban Monitor", "City Track", "Street Link",
        "Smart Urban", "City Sensor", "Street Sense", "Urban Node II", "City Grid",
    ],
    "Education": [
        "Student Lab", "Training Kit", "Learning Board", "Class Demo", "STEM Lab",
        "Workshop Kit", "Tutorial Build", "Practice Board", "Study Project", "Lab Exercise",
        "Course Demo", "Beginner Lab", "School Project", "Training Node", "Lesson Build",
        "Lab Kit", "Study Node", "Class Kit", "Learning Node", "STEM Demo",
        "Practice Lab", "Tutorial Node", "Workshop Demo", "Student Node", "Course Lab",
        "Study Kit", "Class Node", "Training Demo", "Lesson Node", "Lab Demo",
        "Learning Hub", "STEM Node", "Practice Node", "School Lab", "Study Demo",
    ],
}

CONN = [
    "WiFi Link", "Bluetooth Pairing", "MQTT Push", "Cloud Sync", "Web Dashboard",
    "Mobile Alerts", "OTA Updates", "Local Server", "Serial Debug", "REST API",
    "Telegram Bot", "Home Assistant", "Node-RED Flow", "Blynk App", "Firebase Log",
    "GPIO Interrupt", "Deep Sleep Mode", "Timer Trigger", "Email Alert", "LCD Status",
    "OLED Display", "SD Card Log", "NTP Timestamp", "JSON Export", "UART Bridge",
    "I2C Bus", "SPI Display", "PWM Output", "ADC Sampling", "Dual-Core Task",
    "FreeRTOS Task", "Watchdog Timer", "EEPROM Store", "Flash Config", "Secure Boot",
]

TEMPLATES = [
    "ESP32 {core} with {sensor}",
    "ESP32 {core} — {sensor} & {output}",
    "ESP32 {core} for {use}",
    "{sensor}-Based ESP32 {core}",
    "ESP32 {core} with {output} Control",
    "ESP32 {core} using {conn}",
    "How to Build an ESP32 {core} with {sensor}",
    "Build an ESP32 {core} with {sensor}",
    "ESP32 {core} — Wiring, Code & Demo",
    "ESP32 {core} with {sensor} for {use}",
    "ESP32 {core} and {output} for {use}",
    "ESP32 {core} with {conn} Integration",
    "ESP32 {core} — {use} Tutorial",
    "ESP32 {core} with Live {conn} Updates",
    "ESP32 {core} — {sensor} Monitor",
    "ESP32 {core} for {use} Automation",
    "ESP32 {core} with {sensor} and {output}",
    "ESP32 {core} — Beginner {use} Build",
    "ESP32 {core} with {output} for {use}",
    "ESP32 {core} — Step-by-Step Guide",
]


def dedupe_core(core: str) -> str:
    words = core.split()
    out = []
    seen = set()
    for w in words:
        lw = w.lower()
        if lw in seen:
            continue
        seen.add(lw)
        out.append(w)
    return " ".join(out) or "IoT Project"


def dedupe_title_phrases(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"(\bfor\s+[^—()]+?)\s+\1", r"\1", title, flags=re.I)
    title = re.sub(r"(\bwith\s+[^—()]+?)\s+\1", r"\1", title, flags=re.I)
    title = re.sub(r"(\s+—\s+[^—()]+?)\s+\1", r"\1", title, flags=re.I)
    title = re.sub(
        r"\s+—\s+Beginner\s+([^—|]+?)\s+Build\s+for\s+\1\s*$",
        r" — Beginner \1 Build",
        title,
        flags=re.I,
    )
    title = re.sub(r"\bBuild\s+for\s+([^—|]+?)\s+for\s+\1\b", r"for \1", title, flags=re.I)
    return re.sub(r"\s+", " ", title).strip()


def strip_redundant_smart(text: str) -> str:
    text = re.sub(r"\bSmart\s+Smart\b", "Smart", text, flags=re.I)
    text = re.sub(r"\bESP32\s+Smart\s+Smart\b", "ESP32 Smart", text, flags=re.I)
    return text


def polish_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\bESP32(?:\s+ESP32)+\b", "ESP32", title, flags=re.I)
    title = re.sub(r"\bSmart(?:\s+Smart)+\b", "Smart", title, flags=re.I)
    title = re.sub(r"\bBuild(?:\s+a\s+Build)\b", "Build", title, flags=re.I)
    title = re.sub(r"^Build a Smart ESP32 Smart ", "ESP32 Smart ", title, flags=re.I)
    title = re.sub(r"^Build a Smart ESP32 ", "ESP32 ", title, flags=re.I)
    title = re.sub(r"^Build an ESP32 ESP32 ", "ESP32 ", title, flags=re.I)
    title = re.sub(r"^Build an ESP32 ", "ESP32 ", title, flags=re.I)
    title = re.sub(r"^Build a Smart ", "ESP32 ", title, flags=re.I)
    title = re.sub(r"^Build a ", "ESP32 ", title, flags=re.I)
    if not re.match(r"^ESP32\b", title, re.I) and not re.match(
        r"^(How to|Build |Create |Make |Step-by-Step)", title, re.I
    ):
        title = f"ESP32 {title}"
    title = strip_redundant_smart(title)
    title = dedupe_title_phrases(title)
    return normalize_terms(title[:92].rstrip(" ,-("))


def clean_part(name: str) -> str:
    n = (name or "Sensor").strip()
    n = re.sub(r"\s+(signal|control|module|device)$", "", n, flags=re.I)
    fixes = {"Mq135": "MQ135", "Mq 135": "MQ135", "Dht11": "DHT11", "Dht22": "DHT22", "Esp32": "ESP32"}
    for old, new in fixes.items():
        n = re.sub(re.escape(old), new, n, flags=re.I)
    if n.lower().endswith(" sensor"):
        n = n[:-7].strip()
    if not n:
        return "Sensor"
    return " ".join(title_word(w) for w in n.split())


def words_overlap(a: str, b: str) -> bool:
    aw = {w for w in a.lower().split() if len(w) > 2}
    bw = {w for w in b.lower().split() if len(w) > 2}
    return len(aw & bw) >= 2


def slug_core(slug: str) -> str:
    s = re.sub(r"^esp32-", "", slug, flags=re.I)
    s = re.sub(r"-project-\d+$", "", s, flags=re.I)
    words = [w for w in s.split("-") if w and w not in ("esp32", "for", "with", "and", "the")]
    skip = {
        "low", "power", "use", "beginners", "setup", "update", "logging", "control",
        "alerts", "server", "dashboard", "status", "local", "web", "mobile", "ota",
        "bluetooth", "cloud", "wifi", "oled", "smart",
    }
    core_words = [title_word(w) for w in words if w not in skip]
    if not core_words:
        core_words = [title_word(w) for w in words[:4]]
    phrase = " ".join(core_words[:5])
    phrase = re.sub(r"^(Smart|ESP32|Esp32)\s+", "", phrase, flags=re.I)
    phrase = dedupe_core(phrase)
    return phrase or "IoT Project"


def generate_title(d: dict, variant: int, used: set) -> str:
    cat = d.get("category") or "ESP32"
    pool = USE_CASES.get(cat, GENERIC_USE)
    core = slug_core(d.get("slug", ""))
    sensor = clean_part(d.get("sensor_name", "Sensor"))
    output = clean_part(d.get("output_name", "Output"))
    tpl = TEMPLATES[(variant * 11 + 2) % len(TEMPLATES)]
    use = pool[(variant * 3 + 5) % len(pool)]
    if words_overlap(use, core):
        use = pool[(variant * 3 + 16) % len(pool)]
    conn = CONN[(variant * 7 + 3) % len(CONN)]
    title = tpl.format(use=use, core=core, sensor=sensor, output=output, conn=conn)
    title = polish_title(title)
    base = title
    key = title.lower()
    attempt = 0
    suffixes = [
        f" for {use}",
        f" with {conn}",
        f" — {use}",
        f" ({conn})",
        f" — {sensor} Monitor",
        f" for {use} Labs",
        f" with {output}",
        f" — {conn} Ready",
    ]
    while key in used:
        suffix = suffixes[attempt % len(suffixes)]
        fragment = suffix.strip(" —()").lower()
        if fragment and (fragment in base.lower() or base.lower().endswith(fragment)):
            attempt += 1
            continue
        use_tail = re.sub(r"^for\s+", "", fragment, flags=re.I)
        if use_tail and use_tail in base.lower():
            attempt += 1
            continue
        title = polish_title(f"{base}{suffix}")
        key = title.lower()
        attempt += 1
        if attempt > 12:
            title = polish_title(f"{base} — Build {variant + 1}")
            key = title.lower()
            break
    used.add(key)
    return title
