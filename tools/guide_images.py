GUIDE_IMAGE_FALLBACK = "/assets/images/guides/guide-esp32-board-basics.webp"

GUIDE_IMAGE_BY_SLUG = {
    "what-is-esp32": "/assets/images/academy/academy-mission-01.webp",
    "installing-arduino-ide-esp32": "/assets/images/academy/academy-mission-02.webp",
    "blink-led-esp32": "/assets/images/academy/academy-mission-03.webp",
    "button-led-control": "/assets/images/academy/academy-mission-04.webp",
    "digital-inputs-floating-pins": "/assets/images/academy/academy-mission-05.webp",
    "pull-up-vs-pull-down-resistors": "/assets/images/academy/academy-mission-06.webp",
    "debouncing-buttons": "/assets/images/academy/academy-mission-07.webp",
    "multiple-buttons-state-detection": "/assets/images/academy/academy-mission-08.webp",
    "pwm-fundamentals": "/assets/images/academy/academy-mission-09.webp",
    "analog-inputs": "/assets/images/academy/academy-mission-10.webp",
    "oled-display-esp32": "/assets/images/academy/academy-mission-11.webp",
    "i2c-communication": "/assets/images/academy/academy-mission-12.webp",
    "analog-inputs-reading-real-world": "/assets/images/guides/guide-analog-input.webp",
    "connect-oled-esp32": "/assets/images/guides/guide-i2c-communication.webp",
    "environmental-sensors": "/assets/images/guides/guide-esp32-board-basics.webp",
    "reading-analog-sensors": "/assets/images/guides/guide-ldr-light-sensor.webp",
    "smart-environment-monitor-capstone": "/assets/images/guides/guide-esp32-board-basics.webp",
}


def guide_image_filename(slug: str) -> str:
    return GUIDE_IMAGE_BY_SLUG.get(slug, GUIDE_IMAGE_FALLBACK)


def guide_image_path(slug: str) -> str:
    image = guide_image_filename(slug)
    if image.startswith("/"):
        return image
    return f"/assets/images/guides/{image}"


def guide_image_alt(guide: dict) -> str:
    headline = guide.get("headline") or guide.get("title", "").split("|")[0].strip() or "ESP32 guide"
    return f"{headline} guide illustration"
