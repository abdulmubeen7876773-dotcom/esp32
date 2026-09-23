GUIDE_IMAGE_FALLBACK = "/assets/images/guides/guide-esp32-board-basics.webp"

GUIDE_IMAGE_BY_SLUG = {
    "analog-inputs": "/assets/images/generated/guides/analog-inputs-1200.webp",
    "analog-inputs-reading-real-world": "/assets/images/generated/guides/analog-inputs-reading-real-world-1200.webp",
    "blink-led-esp32": "/assets/images/generated/guides/blink-led-esp32-1200.webp",
    "button-led-control": "/assets/images/generated/guides/button-led-control-1200.webp",
    "connect-oled-esp32": "/assets/images/generated/guides/connect-oled-esp32-1200.webp",
    "debouncing-buttons": "/assets/images/generated/guides/debouncing-buttons-1200.webp",
    "digital-inputs-floating-pins": "/assets/images/generated/guides/digital-inputs-floating-pins-1200.webp",
    "environmental-sensors": "/assets/images/generated/guides/environmental-sensors-1200.webp",
    "esp32-arduino-ide": "/assets/images/generated/guides/installing-arduino-ide-esp32-1200.webp",
    "i2c-communication": "/assets/images/generated/guides/i2c-communication-1200.webp",
    "installing-arduino-ide-esp32": "/assets/images/generated/guides/installing-arduino-ide-esp32-1200.webp",
    "multiple-buttons-state-detection": "/assets/images/generated/guides/multiple-buttons-state-detection-1200.webp",
    "oled-display-esp32": "/assets/images/generated/guides/oled-display-esp32-1200.webp",
    "pull-up-vs-pull-down-resistors": "/assets/images/generated/guides/pull-up-vs-pull-down-resistors-1200.webp",
    "esp32-pwm": "/assets/images/generated/guides/pwm-fundamentals-1200.webp",
    "pwm-fundamentals": "/assets/images/generated/guides/pwm-fundamentals-1200.webp",
    "read-temperature-dht22": "/assets/images/generated/guides/read-temperature-dht22-1200.webp",
    "reading-analog-sensors": "/assets/images/generated/guides/reading-analog-sensors-1200.webp",
    "smart-environment-monitor-capstone": "/assets/images/generated/guides/smart-environment-monitor-capstone-1200.webp",
    "what-is-esp32": "/assets/images/generated/guides/what-is-esp32-1200.webp",
}

GUIDE_IMAGE_BASE_BY_SLUG = {
    "analog-inputs": "/assets/images/generated/guides/analog-inputs",
    "analog-inputs-reading-real-world": "/assets/images/generated/guides/analog-inputs-reading-real-world",
    "blink-led-esp32": "/assets/images/generated/guides/blink-led-esp32",
    "button-led-control": "/assets/images/generated/guides/button-led-control",
    "connect-oled-esp32": "/assets/images/generated/guides/connect-oled-esp32",
    "debouncing-buttons": "/assets/images/generated/guides/debouncing-buttons",
    "digital-inputs-floating-pins": "/assets/images/generated/guides/digital-inputs-floating-pins",
    "environmental-sensors": "/assets/images/generated/guides/environmental-sensors",
    "esp32-arduino-ide": "/assets/images/generated/guides/installing-arduino-ide-esp32",
    "i2c-communication": "/assets/images/generated/guides/i2c-communication",
    "installing-arduino-ide-esp32": "/assets/images/generated/guides/installing-arduino-ide-esp32",
    "multiple-buttons-state-detection": "/assets/images/generated/guides/multiple-buttons-state-detection",
    "oled-display-esp32": "/assets/images/generated/guides/oled-display-esp32",
    "pull-up-vs-pull-down-resistors": "/assets/images/generated/guides/pull-up-vs-pull-down-resistors",
    "esp32-pwm": "/assets/images/generated/guides/pwm-fundamentals",
    "pwm-fundamentals": "/assets/images/generated/guides/pwm-fundamentals",
    "read-temperature-dht22": "/assets/images/generated/guides/read-temperature-dht22",
    "reading-analog-sensors": "/assets/images/generated/guides/reading-analog-sensors",
    "smart-environment-monitor-capstone": "/assets/images/generated/guides/smart-environment-monitor-capstone",
    "what-is-esp32": "/assets/images/generated/guides/what-is-esp32",
}


def guide_image_filename(slug: str) -> str:
    return GUIDE_IMAGE_BY_SLUG.get(slug, GUIDE_IMAGE_FALLBACK)


def guide_image_path(slug: str) -> str:
    image = guide_image_filename(slug)
    if image.startswith("/"):
        return image
    return f"/assets/images/guides/{image}"


def guide_image_variant_path(slug: str, width: int) -> str:
    base = GUIDE_IMAGE_BASE_BY_SLUG.get(slug)
    if not base:
        return guide_image_path(slug)
    return f"{base}-{width}.webp"


def guide_image_srcset(slug: str, widths: tuple[int, ...] = (640, 1024, 1200)) -> str:
    base = GUIDE_IMAGE_BASE_BY_SLUG.get(slug)
    if not base:
        return ""
    return ", ".join(f"{base}-{width}.webp {width}w" for width in widths)


def guide_image_alt(guide: dict) -> str:
    slug = guide.get("slug", "")
    custom = {'button-led-control': 'Button Led Control guide illustration', 'read-temperature-dht22': 'Read Temperature Dht22 guide illustration', 'digital-inputs-floating-pins': 'Digital Inputs Floating Pins guide illustration', 'pull-up-vs-pull-down-resistors': 'Pull Up Vs Pull Down Resistors guide illustration', 'debouncing-buttons': 'Debouncing Buttons guide illustration', 'multiple-buttons-state-detection': 'Multiple Buttons State Detection guide illustration', 'esp32-pwm': 'ESP32 PWM guide illustration with LED brightness waveform', 'pwm-fundamentals': 'Pwm Fundamentals guide illustration', 'analog-inputs': 'Analog Inputs guide illustration', 'analog-inputs-reading-real-world': 'Analog Inputs Reading Real World guide illustration', 'oled-display-esp32': 'Oled Display Esp32 guide illustration', 'reading-analog-sensors': 'Reading Analog Sensors guide illustration', 'i2c-communication': 'I2C Communication guide illustration', 'environmental-sensors': 'ESP32 environmental sensors guide with sensor modules on a workbench', 'smart-environment-monitor-capstone': 'ESP32 smart environment monitor capstone with sensor readings and display dashboard', 'what-is-esp32': 'ESP32 board overview workspace for a beginner guide', 'esp32-arduino-ide': 'Arduino IDE setup screen with ESP32 board and USB cable', 'installing-arduino-ide-esp32': 'Arduino IDE setup screen with ESP32 board and USB cable', 'blink-led-esp32': 'ESP32 blink LED guide with LED circuit on a breadboard', 'connect-oled-esp32': 'ESP32 OLED display guide with SSD1306 screen and I2C wiring'}.get(slug)
    if custom:
        return custom
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip() or "ESP32 guide"
    return f"{headline} guide illustration"
