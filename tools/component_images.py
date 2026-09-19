COMPONENT_IMAGE_BY_SLUG = {
    "bme280": "/assets/visuals/components/photos/bme280-photo.svg",
    "dht22": "/assets/visuals/components/photos/dht22-photo.webp",
    "esp32-cam": "/assets/visuals/components/photos/esp32-cam-photo.webp",
    "esp32-devkit": "/assets/visuals/components/photos/esp32-devkit-photo.webp",
    "hc-sr04": "/assets/visuals/components/photos/hc-sr04-photo.webp",
    "pir-sensor": "/assets/visuals/components/photos/pir-sensor-photo.webp",
    "relay-module": "/assets/visuals/components/photos/relay-module-photo.webp",
    "ssd1306-oled": "/assets/visuals/components/photos/ssd1306-oled-photo.webp",
}


def component_image_path(slug: str) -> str:
    return COMPONENT_IMAGE_BY_SLUG.get(slug, "")
