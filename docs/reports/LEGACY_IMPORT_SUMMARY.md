# Legacy Import Summary

**Date:** 2026-06-27
**Source plan:** `D:/jsnjd/docs/reports/CONTENT_MIGRATION_PLAN.md`

## Counts

| Metric | Count |
|--------|------:|
| Projects imported (new YAML) | 35 |
| Projects enriched (existing) | 15 |
| Guides imported (new YAML) | 0 |
| Guides enriched (metadata) | 5 |
| Components enriched (metadata) | 7 |

## Validation

| Script | Result |
|--------|--------|
| `py tools/validate_content.py` | Passed (50 projects, 7 components, 5 guides) |
| `py tools/validate_project_quality.py` | Not present in repo |
| `py tools/validate_component_quality.py` | Not present in repo |
| `py tools/validate_guide_quality.py` | Not present in repo |

## Import tiers

| Tier | Action |
|------|--------|
| Tier 1 (15) | Enriched from archive HTML — beginner level + hardware preserved |
| Tier 2 (22) | Imported from batch PHP — full 3-level content + Arduino code |
| Tier 3 (6) | Imported from batch PHP |
| Tier 4 (7) | Imported from batch PHP (slug aliases applied) |
| WordPress guides (2) | Skipped — SQL post_content extraction failed |
| Components (7) | Metadata tags applied; BME280 golden component included |

## Slug alias merges

- `esp32-rfid-access-control` → `esp32-rfid-access-control-system`
- `esp32-security-camera` → `esp32-security-camera-system`
- `esp32-greenhouse-controller` → `esp32-greenhouse-automation-controller`
- `esp32-lora-remote-sensor` → `esp32-lora-remote-sensor-node`

## Skipped items

- Guide debouncing-buttons-esp32: post_content not extracted from SQL window
- Guide digital-outputs-esp32: post_content not extracted from SQL window

## Duplicate merges

- None

## Missing assets

- All projects: no dedicated featured images in recovered sources
- Tier 1 archive pages: wiring diagrams are SVG-only (tabular wiring falls back to `hardware:` block)
- WordPress guides: bodies not recovered from SQL in this pass

## Items needing polish

- esp32-air-quality-monitor
- esp32-camera-capture-server
- esp32-distance-monitoring-system
- esp32-home-climate-automation
- esp32-iot-weather-station (golden — no legacy overlay)
- esp32-learning-trainer
- esp32-machine-monitoring-node
- esp32-motion-security-alert
- esp32-pulse-oximeter-logger
- esp32-rgb-led-pattern-controller
- esp32-smart-energy-meter
- esp32-smart-irrigation-system
- esp32-smart-street-light
- esp32-tinyml-sound-classifier
- esp32-wifi-robot-controller
- guide:installing-arduino-ide-esp32
- guide:what-is-esp32
- component:bme280
- component:esp32-devkit
- component:hc-sr04
- component:pir-sensor
- component:relay-module
- component:ssd1306-oled
