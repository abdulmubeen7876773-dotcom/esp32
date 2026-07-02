GUIDE_IMAGE_FALLBACK = "guide-esp32-board-basics.webp"

GUIDE_IMAGE_BY_SLUG = {
    "analog-inputs": "guide-analog-input.webp",
    "analog-inputs-reading-real-world": "guide-analog-input.webp",
    "blink-led-esp32": "guide-blink-led.webp",
    "button-led-control": "guide-gpio-basics.webp",
    "connect-oled-esp32": "guide-i2c-communication.webp",
    "debouncing-buttons": "guide-state-detection.webp",
    "digital-inputs-floating-pins": "guide-digital-io.webp",
    "i2c-communication": "guide-i2c-communication.webp",
    "installing-arduino-ide-esp32": "guide-esp32-programming-setup.webp",
    "multiple-buttons-state-detection": "guide-state-detection.webp",
    "oled-display-esp32": "guide-i2c-communication.webp",
    "pull-up-vs-pull-down-resistors": "guide-pullup-pulldown.webp",
    "pwm-fundamentals": "guide-led-resistors.webp",
    "reading-analog-sensors": "guide-ldr-light-sensor.webp",
    "what-is-esp32": "guide-esp32-devkit-overview.webp",
}


def guide_image_filename(slug: str) -> str:
    return GUIDE_IMAGE_BY_SLUG.get(slug, GUIDE_IMAGE_FALLBACK)


def guide_image_path(slug: str) -> str:
    return f"/assets/images/guides/{guide_image_filename(slug)}"


def guide_image_alt(guide: dict) -> str:
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip() or "ESP32 guide"
    return f"{headline} guide illustration"
