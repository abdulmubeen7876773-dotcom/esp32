COMPONENT_IMAGE_BY_SLUG = {
    "bme280": "/assets/images/components/component-01.webp",
    "dht22": "/assets/images/components/component-02.webp",
    "esp32-devkit": "/assets/images/components/component-03.webp",
    "hc-sr04": "/assets/images/components/component-04.webp",
    "pir-sensor": "/assets/images/components/component-05.webp",
    "relay-module": "/assets/images/components/component-06.webp",
    "ssd1306-oled": "/assets/images/components/component-07.webp",
}


def component_image_path(slug: str) -> str:
    return COMPONENT_IMAGE_BY_SLUG.get(slug, "")
