# SEO Changelog

## Current Batch - Search Console SEO Boost

| URL/file | What changed | Why | Expected SEO/user benefit | Risk |
| --- | --- | --- | --- | --- |
| `/guides/pull-up-vs-pull-down-resistors.html` | Refined title, meta description, and lead. | Page already ranks for ESP32 pull-up/pull-down queries; improve CTR while preserving coverage. | Clearer snippet around button wiring, INPUT_PULLUP, floating GPIO fixes, and pressed HIGH/LOW behavior. | Low |
| `/guides/debouncing-buttons.html` | Refined title, meta description, and lead around `millis()` debounce. | Page is close to page one and searchers need a direct debounce answer. | Better match for "ESP32 button debounce" and "millis debounce" intent. | Low |
| `/guides/digital-inputs-floating-pins.html` | Refined title and meta description. | High impressions but weak CTR; searchers need "random input/floating GPIO" answer. | Stronger snippet for random HIGH/LOW readings and pull resistor next steps. | Low |
| `/projects/esp32-led-matrix-display.html` | Refined title, description, meta title, and project story. | Page has page-one potential but needed stronger MAX7219/scroller intent and less generic phrasing. | Better query alignment for ESP32 MAX7219 LED matrix scrolling text projects. | Low |
| `/projects/esp32-ir-remote-control.html` | Refined title, description, meta title, FAQ wording, and one guide title casing. | High impressions with weak CTR; page should clearly promise receive/send behavior and NEC limits. | Better snippet clarity for IRremote, TSOP38238, transistor IR LED driver, and safety boundaries. | Low |
| `/projects/esp32-smart-thermostat.html` | Refined meta description and removed unrelated robot/pump/lock wording from a build-photo note. | Good opportunity page with one clear template-leak example. | More specific low-voltage thermostat positioning and no unrelated visible/source leakage. | Low |
| `/components/bme280.html` | Refined component name and summary. | Major impression opportunity; focus should be ESP32 wiring/code rather than broad BME280 only. | Stronger ESP32+BME280 intent for I2C, weather projects, and address troubleshooting. | Medium-low |
| `/projects.html` | Refined hub description, hero copy, first-step guidance, and featured links. | Projects hub has impressions but weak rank; improve discovery without adding navigation complexity. | Better user path for beginner, sensor, display, IoT, robotics, and smart-home builds. | Low |

## Intentionally Protected

- `/projects/esp32-oled-weather-clock.html` - already working well; preserve generated hero and content.
- `/projects/esp32-lightning-detector.html` - ranking well; no aggressive rewrite.
- `/projects/esp32-smart-mailbox.html` - strong page; no rewrite.
- `/components/dht22.html` - broad query is too competitive; defer to a later ESP32-specific component pass.
