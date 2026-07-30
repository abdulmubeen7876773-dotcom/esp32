GUIDE_IMAGE_FALLBACK = "/assets/images/guides/guide-esp32-board-basics.webp"

GUIDE_IMAGE_BY_SLUG = {
    "what-is-esp32": "/assets/images/guides/generated/what-is-esp32-overview-1024.webp",
    "installing-arduino-ide-esp32": "/assets/images/guides/generated/arduino-ide-esp32-setup-1024.webp",
    "blink-led-esp32": "/assets/images/guides/generated/blink-led-breadboard-1024.webp",
    "button-led-control": "/assets/images/academy/academy-mission-04.webp",
    "digital-inputs-floating-pins": "/assets/images/academy/academy-mission-05.webp",
    "pull-up-vs-pull-down-resistors": "/assets/images/academy/academy-mission-06.webp",
    "debouncing-buttons": "/assets/images/academy/academy-mission-07.webp",
    "multiple-buttons-state-detection": "/assets/images/academy/academy-mission-08.webp",
    "pwm-fundamentals": "/assets/images/academy/academy-mission-09.webp",
    "analog-inputs": "/assets/images/academy/academy-mission-10.webp",
    "oled-display-esp32": "/assets/images/academy/academy-mission-11.webp",
    "i2c-communication": "/assets/images/academy/academy-mission-12.webp",
    "analog-inputs-reading-real-world": "/assets/images/guides/generated/analog-input-serial-monitor-1024.webp",
    "connect-oled-esp32": "/assets/images/guides/guide-i2c-communication.webp",
    "environmental-sensors": "/assets/images/guides/generated/environmental-sensor-modules-1024.webp",
    "reading-analog-sensors": "/assets/images/guides/generated/analog-sensor-bench-1024.webp",
    "read-temperature-dht22": "/assets/images/guides/generated/temperature-sensor-serial-output-1024.webp",
    "smart-environment-monitor-capstone": "/assets/images/guides/generated/smart-environment-dashboard-1024.webp",
}

GUIDE_IMAGE_BASE_BY_SLUG = {
    "what-is-esp32": "/assets/images/guides/generated/what-is-esp32-overview",
    "installing-arduino-ide-esp32": "/assets/images/guides/generated/arduino-ide-esp32-setup",
    "blink-led-esp32": "/assets/images/guides/generated/blink-led-breadboard",
    "analog-inputs-reading-real-world": "/assets/images/guides/generated/analog-input-serial-monitor",
    "environmental-sensors": "/assets/images/guides/generated/environmental-sensor-modules",
    "reading-analog-sensors": "/assets/images/guides/generated/analog-sensor-bench",
    "read-temperature-dht22": "/assets/images/guides/generated/temperature-sensor-serial-output",
    "smart-environment-monitor-capstone": "/assets/images/guides/generated/smart-environment-dashboard",
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


def guide_image_srcset(slug: str, widths: tuple[int, ...] = (480, 640, 1024)) -> str:
    base = GUIDE_IMAGE_BASE_BY_SLUG.get(slug)
    if not base:
        return ""
    return ", ".join(f"{base}-{width}.webp {width}w" for width in widths)


def guide_image_alt(guide: dict) -> str:
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip() or "ESP32 guide"
    return f"{headline} guide illustration"
