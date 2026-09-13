# SEO Boost Plan

## 1. Protect Existing Winners

- `/projects/esp32-oled-weather-clock.html` - already strong for "esp32 weather clock"; keep changes limited to image preservation and related links.
- `/projects/esp32-lightning-detector.html` - good average position with specialized AS3935 intent; avoid broad weather-safety rewrites.
- `/projects/esp32-smart-mailbox.html` - strong ranking and CTR; use as a model for project specificity, not a rewrite target.
- `/guides/pull-up-vs-pull-down-resistors.html` - high-value page-one guide; improve CTR carefully without removing the existing technical coverage.

## 2. Page-One Opportunities

- HIGH: `/guides/debouncing-buttons.html` - position near page one, clear query intent, small title/meta improvements can help.
- HIGH: `/guides/pull-up-vs-pull-down-resistors.html` - already around positions 7-9 for specific ESP32 pull resistor queries.
- HIGH: `/guides/digital-inputs-floating-pins.html` - strong impressions, low CTR, naturally supports the input cluster.
- HIGH: `/projects/esp32-led-matrix-display.html` - practical MAX7219 query intent and position close enough to improve with stronger specificity.
- HIGH: `/projects/esp32-ir-remote-control.html` - high impressions and weak CTR; needs clearer receive/send and IRremote intent.
- HIGH: `/components/bme280.html` - high impressions with ESP32+BME280 intent; strengthen component-to-project cluster links.
- MEDIUM: `/projects/esp32-smart-thermostat.html` - strong topic and new image support, but avoid overpromising real HVAC use.
- MEDIUM: `/projects/esp32-iot-weather-station.html` - opportunity page; image work already improves CTR potential.
- MEDIUM: `/guides/button-led-control.html` - beginner intent is real, but ranking gap is larger.
- LOW: broad `/components/dht22.html` - broad "dht22" is too competitive; target ESP32-specific wiring and troubleshooting instead.
- LOW: `/projects.html` - broad "esp32 projects" is competitive; improve discovery copy without stuffing.

## 3. CTR Opportunities

- `/components/bme280.html` - high impressions, very low CTR; title should signal ESP32 wiring/code and weather-station use.
- `/components/dht22.html` - high impressions, very low CTR; keep focus on ESP32 DHT22 wiring/code, not generic sensor encyclopedia.
- `/guides/digital-inputs-floating-pins.html` - low CTR; search snippet should promise the random HIGH/LOW fix.
- `/guides/button-led-control.html` - low CTR; emphasize GPIO27, INPUT_PULLUP, and LED result.
- `/projects/esp32-ir-remote-control.html` - low CTR; clarify receiver, sender, NEC replay, and IRremote.
- `/projects/esp32-smart-thermostat.html` - low CTR; clarify safe low-voltage thermostat prototype and hysteresis.
- `/projects.html` - low position/CTR; needs clearer hub language for beginner, IoT, robotics, display, and sensor projects.

## 4. Internal Linking Opportunities

| Source page | Anchor idea | Target page |
| --- | --- | --- |
| `/guides/digital-inputs-floating-pins.html` | stop random ESP32 input readings | `/guides/pull-up-vs-pull-down-resistors.html` |
| `/guides/pull-up-vs-pull-down-resistors.html` | debounce the stable button input | `/guides/debouncing-buttons.html` |
| `/guides/debouncing-buttons.html` | build the GPIO27 button and LED first | `/guides/button-led-control.html` |
| `/guides/button-led-control.html` | why floating pins cause false presses | `/guides/digital-inputs-floating-pins.html` |
| `/components/bme280.html` | build the BME280 weather station | `/projects/esp32-iot-weather-station.html` |
| `/components/bme280.html` | show readings on an OLED weather clock | `/projects/esp32-oled-weather-clock.html` |
| `/projects/esp32-iot-weather-station.html` | BME280 sensor wiring reference | `/components/bme280.html` |
| `/projects/esp32-smart-thermostat.html` | DHT22 sensor reference | `/components/dht22.html` |
| `/projects/esp32-led-matrix-display.html` | compare OLED vs LED matrix output | `/projects/esp32-oled-weather-clock.html` |
| `/projects/esp32-ir-remote-control.html` | review clean digital input behavior | `/guides/digital-inputs-floating-pins.html` |
| `/projects.html` | start with beginner ESP32 projects | `/guides/blink-led-esp32.html` |
| `/projects.html` | build the OLED weather clock | `/projects/esp32-oled-weather-clock.html` |

## 5. Content Gaps

- Add concise answer-first language to pages whose first snippet can better match search intent.
- Add project-specific troubleshooting where a page still uses generic troubleshooting or broad copy.
- Clarify safety boundaries on relay, IR, and lightning projects without adding fear or legal filler.
- Improve hub copy on `/projects.html` so users can quickly choose beginner, sensor, display, IoT, robotics, and smart-home paths.
- Keep broad component pages ESP32-specific rather than trying to rank for generic component keywords alone.

## 6. Generic Template Leakage

- `/projects/esp32-smart-thermostat.html` contains a build-photo note that says "robot, pump, or lock state"; this should be thermostat-specific.
- `/projects/esp32-led-matrix-display.html` includes generic phrasing such as "The tutorial focuses on the engineering path"; replace with MAX7219/SPI/display-specific value.
- Several project pages still include generic card/list language in source imports, but only priority URLs should be cleaned in this batch.

## 7. Technical SEO Findings

- Priority pages checked have one H1, self-referencing canonicals, `index,follow,max-image-preview:large`, and sitemap presence exactly once.
- `robots.txt` allows crawling and only blocks `/projects/_archive/`.
- Sitemap currently has 110 URLs and no duplicate URLs in the inspected sample.
- Generated hero images on the recently updated 10 pages are preserved; no duplicate hero block was present after the latest image swap.
- Structured data is generated centrally for guides, projects, and components; preserve existing schema conventions.
- Component FAQ sections are very large on some pages. Do not remove useful FAQ content in this batch, but avoid adding generic FAQ bloat.
- No accidental noindex was found on the inspected priority pages.

## 8. Desktop Performance Opportunity

- Desktop rankings lag mobile, but the inspected generated pages use the same canonical content and content order across viewports.
- The shared header/search and hero bands can push answer-first content lower on desktop, especially project pages with large hero blocks.
- Do not redesign in this batch. Use concise title/meta/lead improvements so the above-the-fold copy answers intent faster without changing layout.
- Existing image dimensions and generated WebP hero work should be preserved to avoid layout shift and duplicate images.
- Projects hub should help desktop users choose a path faster through copy and existing discovery structure, not a more complex navigation system.

## Phase 2 Priority Tiers

### TIER A - QUICK WINS

- `/guides/pull-up-vs-pull-down-resistors.html`
- `/guides/debouncing-buttons.html`
- `/projects/esp32-led-matrix-display.html`
- `/projects/esp32-ir-remote-control.html`
- `/projects/esp32-smart-thermostat.html`
- `/guides/digital-inputs-floating-pins.html`
- `/components/bme280.html`

### TIER B - GROWTH PAGES

- `/projects/esp32-iot-weather-station.html`
- `/guides/button-led-control.html`
- `/components/dht22.html`
- `/projects.html`
- Component and category discovery modules related to sensors, displays, IoT, and robotics

### TIER C - PROTECT

- `/projects/esp32-oled-weather-clock.html`
- `/projects/esp32-lightning-detector.html`
- `/projects/esp32-smart-mailbox.html`

## Implementation Guardrails

- Preserve URLs, canonicals, schema conventions, sitemap structure, navigation, and current generated images.
- Avoid broad rewrites of ranking pages.
- Prefer small title/meta/lead and project-specific text improvements.
- Add internal links only where the source page naturally supports the target.
- Do not add new pages or generate new images in this batch.
