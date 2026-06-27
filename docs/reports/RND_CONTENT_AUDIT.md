# R&D Content Audit — ESP32 Engine

**Audit date:** 2026-06-27  
**Method:** Read-only. Sources checked: `content/guides/`, `content/projects/`, `content/components/`, `projects/_archive/`, `content/guide-roadmap.yaml`, `content/component-roadmap.yaml`, full git log (`git log --all`), deleted-file history (`--diff-filter=D`).  
**Scope:** Every guide, project, and component ever created, archived, deleted, or planned.

---

## Executive Summary

| Item | Count |
|---|---:|
| Guides ever created (YAML) | **5** |
| Projects ever created (parent YAML) | **15** |
| Components ever created (YAML) | **6** |
| Currently live guides | **5** |
| Currently live projects | **15** |
| Currently live components | **6** |
| Archived (old variant HTML pages) | **1,000** |
| Guide or project YAML files deleted | **0** |
| Docs files deleted (recoverable) | **4** |
| Other non-content files deleted | **5** |
| Anything missing completely | **0** |

**No guide or project YAML content has ever been deleted.** All 5 guides, 15 projects, and 6 components created during R&D are currently live. The 1,000 archived HTML pages in `projects/_archive/` are accessible but not publicly linked.

---

## 1. Guides — Full History

### 1.1 Currently Live (5 guides)

| Slug | Format | Status | First committed |
|---|---|---|---|
| `what-is-esp32` | legacy | Complete | `c3b1beab` — Deploy Phase 1 and Phase 2 ESP32 guides (2026-06-18) |
| `installing-arduino-ide-esp32` | legacy | Complete | `c3b1beab` — Deploy Phase 1 and Phase 2 ESP32 guides (2026-06-18) |
| `blink-led-esp32` | mission | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `read-temperature-dht22` | mission | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `connect-oled-esp32` | mission | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |

**File locations (all present):**
```
content/guides/what-is-esp32.yaml
content/guides/installing-arduino-ide-esp32.yaml
content/guides/blink-led-esp32.yaml
content/guides/read-temperature-dht22.yaml
content/guides/connect-oled-esp32.yaml
```

### 1.2 Archived / Deleted Guides

None. Zero guide YAML files have ever been deleted from the repository.

### 1.3 Planned But Not Yet Created (95 missions)

`content/guide-roadmap.yaml` plans 100 missions total (5 complete, 95 `Coming Soon`).

The next 7 unbuilt missions in sequence:

| Slug | Title | Level | Prerequisite |
|---|---|---|---|
| `blink-two-leds` | Blink Two LEDs in Pattern | First Spark | blink-led-esp32 |
| `button-led-control` | Button Controls an LED | First Spark | blink-two-leds |
| `serial-monitor-hello` | Hello Serial Monitor | First Spark | button-led-control |
| `serial-read-number` | Read Numbers on Serial | First Spark | serial-monitor-hello |
| `onboard-led-blink` | Use the Onboard LED | First Spark | serial-read-number |
| `pwm-dim-led` | Dim an LED with PWM | First Spark | onboard-led-blink |
| `rgb-led-colors` | Mix Colors on RGB LED | First Spark | pwm-dim-led |

Full planned roadmap: 100 missions across 8 levels — First Spark (12), Sensors (13), Displays (12), Motors (13), Communication (13), IoT Projects (13), AI Projects (12), Advanced ESP32 (12).

---

## 2. Projects — Full History

### 2.1 Currently Live (15 parent projects)

| Slug | Category | First committed |
|---|---|---|
| `esp32-air-quality-monitor` | Environmental | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-camera-capture-server` | ESP32-CAM | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-distance-monitoring-system` | Sensor Projects | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-home-climate-automation` | Home Automation | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-iot-weather-station` | IoT Projects | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-learning-trainer` | Education | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-machine-monitoring-node` | Industrial Automation | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-motion-security-alert` | Security Projects | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-pulse-oximeter-logger` | Healthcare | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-rgb-led-pattern-controller` | LED Projects | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-smart-energy-meter` | Energy Monitoring | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-smart-irrigation-system` | Agriculture | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-smart-street-light` | Smart City | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-tinyml-sound-classifier` | AI Projects | `3c1bf512` — CMS conversion (2026-06-18) |
| `esp32-wifi-robot-controller` | Robotics | `3c1bf512` — CMS conversion (2026-06-18) |

**File locations (all present):**
```
content/projects/esp32-air-quality-monitor.yaml
content/projects/esp32-camera-capture-server.yaml
content/projects/esp32-distance-monitoring-system.yaml
content/projects/esp32-home-climate-automation.yaml
content/projects/esp32-iot-weather-station.yaml
content/projects/esp32-learning-trainer.yaml
content/projects/esp32-machine-monitoring-node.yaml
content/projects/esp32-motion-security-alert.yaml
content/projects/esp32-pulse-oximeter-logger.yaml
content/projects/esp32-rgb-led-pattern-controller.yaml
content/projects/esp32-smart-energy-meter.yaml
content/projects/esp32-smart-irrigation-system.yaml
content/projects/esp32-smart-street-light.yaml
content/projects/esp32-tinyml-sound-classifier.yaml
content/projects/esp32-wifi-robot-controller.yaml
```

### 2.2 Archived (Old Variant Architecture)

Before commit `0b9301d3` (2026-06-26), each project had multiple numbered variant HTML pages rather than a single parent page. These were moved to `projects/_archive/` during the architecture migration.

**Archive totals:**
- **1,000 HTML files** in `projects/_archive/`
- **30 unique variant slugs** (2 per parent project)
- **33 HTML files per variant** (numbered `-project-002` through `-project-066` in steps of 2)

**All 30 archived variant slugs:**

| Archive variant slug | Maps to parent |
|---|---|
| `esp32-air-quality-monitor-for-low-power-use` | `esp32-air-quality-monitor` |
| `esp32-air-quality-monitor-with-wifi-control` | `esp32-air-quality-monitor` |
| `esp32-camera-capture-server-with-ota-update` | `esp32-camera-capture-server` |
| `esp32-camera-capture-server-with-web-dashboard` | `esp32-camera-capture-server` |
| `esp32-distance-monitoring-system-for-beginners` | `esp32-distance-monitoring-system` |
| `esp32-distance-monitoring-system-with-oled-status` | `esp32-distance-monitoring-system` |
| `esp32-esp32-learning-trainer-for-beginners` ¹ | `esp32-learning-trainer` |
| `esp32-esp32-learning-trainer-with-oled-status` ¹ | `esp32-learning-trainer` |
| `esp32-home-climate-automation-with-local-web-server` | `esp32-home-climate-automation` |
| `esp32-home-climate-automation-with-mobile-alerts` | `esp32-home-climate-automation` |
| `esp32-iot-weather-station-with-ota-update` | `esp32-iot-weather-station` |
| `esp32-iot-weather-station-with-web-dashboard` | `esp32-iot-weather-station` |
| `esp32-machine-monitoring-node-with-local-web-server` | `esp32-machine-monitoring-node` |
| `esp32-machine-monitoring-node-with-mobile-alerts` | `esp32-machine-monitoring-node` |
| `esp32-motion-security-alert-for-low-power-use` | `esp32-motion-security-alert` |
| `esp32-motion-security-alert-with-wifi-control` | `esp32-motion-security-alert` |
| `esp32-pulse-oximeter-logger-with-local-web-server` | `esp32-pulse-oximeter-logger` |
| `esp32-pulse-oximeter-logger-with-mobile-alerts` | `esp32-pulse-oximeter-logger` |
| `esp32-rgb-led-pattern-controller-for-low-power-use` | `esp32-rgb-led-pattern-controller` |
| `esp32-rgb-led-pattern-controller-with-wifi-control` | `esp32-rgb-led-pattern-controller` |
| `esp32-smart-energy-meter-with-bluetooth-setup` | `esp32-smart-energy-meter` |
| `esp32-smart-energy-meter-with-cloud-logging` | `esp32-smart-energy-meter` |
| `esp32-smart-irrigation-controller-with-bluetooth-setup` ² | `esp32-smart-irrigation-system` |
| `esp32-smart-irrigation-controller-with-cloud-logging` ² | `esp32-smart-irrigation-system` |
| `esp32-smart-street-light-with-ota-update` | `esp32-smart-street-light` |
| `esp32-smart-street-light-with-web-dashboard` | `esp32-smart-street-light` |
| `esp32-tinyml-sound-classifier-for-beginners` | `esp32-tinyml-sound-classifier` |
| `esp32-tinyml-sound-classifier-with-oled-status` | `esp32-tinyml-sound-classifier` |
| `esp32-wifi-robot-controller-with-bluetooth-setup` | `esp32-wifi-robot-controller` |
| `esp32-wifi-robot-controller-with-cloud-logging` | `esp32-wifi-robot-controller` |

¹ **Duplicate prefix bug:** Archive slug `esp32-esp32-learning-trainer-*` had a doubled `esp32-` prefix. Fixed to `esp32-learning-trainer` in the parent architecture.

² **Renamed during migration:** Archive used `esp32-smart-irrigation-controller` but the parent YAML uses `esp32-smart-irrigation-system`.

### 2.3 Deleted Project Files

None. Zero project YAML files have ever been deleted from the repository.

---

## 3. Components — Full History

### 3.1 Currently Live (6 components)

| Slug | Category | Status in Roadmap | First committed |
|---|---|---|---|
| `dht22` | Sensors | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `esp32-devkit` | Development Boards | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `hc-sr04` | Sensors | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `pir-sensor` | Sensors | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `relay-module` | Actuators | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |
| `ssd1306-oled` | Displays | Complete | `11da48c5` — Build ESP32 Engine static learning platform (2026-06-26) |

### 3.2 Planned But Not Yet Created (204 components)

`content/component-roadmap.yaml` plans 210 components across 9 categories. 6 are complete, 204 are `Coming Soon`.

**Category breakdown:**

| Category | Planned | Complete | Remaining |
|---|---:|---:|---:|
| Sensors | 50 | 3 (dht22, hc-sr04, pir-sensor) | 47 |
| Displays | 20 | 1 (ssd1306-oled) | 19 |
| Communication Modules | 20 | 0 | 20 |
| Actuators | 20 | 1 (relay-module) | 19 |
| Development Boards | 20 | 1 (esp32-devkit) | 19 |
| Power Components | 20 | 0 | 20 |
| Input Devices | 20 | 0 | 20 |
| Output Devices | 20 | 0 | 20 |
| Miscellaneous | 20 | 0 | 20 |
| **Total** | **210** | **6** | **204** |

---

## 4. Deleted Files — Recoverable from Git

### 4.1 Deleted Documentation (recoverable)

All four files were deleted in a single commit: `7a8f890c` — Homepage v2 implementation (2026-06-27).

| File | Description | Added in | Deleted in | Recovery command |
|---|---|---|---|---|
| `docs/BLINK_LED_REVIEW.md` | Production readiness review of the Blink LED mission page — full UX, accessibility, teaching, and engineering audit checklist | `e21c192a` Golden Blink LED mission template | `7a8f890c` | `git show e21c192a:docs/BLINK_LED_REVIEW.md` |
| `docs/CONTENT_EDITOR_GUIDE.md` | CMS editing guide — how to add guides, projects, and components; build workflow; YAML syntax reference | `11da48c5` Build ESP32 Engine static learning platform | `7a8f890c` | `git show 11da48c5:docs/CONTENT_EDITOR_GUIDE.md` |
| `docs/CONTENT_INVENTORY.md` | Content inventory report — executive summary of all source YAML files, generated HTML pages, archive, sitemap, and search index items | `0b9301d3` Clean static content source architecture | `7a8f890c` | `git show 0b9301d3:docs/CONTENT_INVENTORY.md` |
| `docs/DEVELOPER_ARCHITECTURE.md` | Developer architecture documentation — static-first Phase 1 system diagram, build pipeline, file responsibilities, deployment guide | `11da48c5` Build ESP32 Engine static learning platform | `7a8f890c` | `git show 11da48c5:docs/DEVELOPER_ARCHITECTURE.md` |

**To restore all four in one command block:**
```bash
git show e21c192a:docs/BLINK_LED_REVIEW.md      > docs/BLINK_LED_REVIEW.md
git show 11da48c5:docs/CONTENT_EDITOR_GUIDE.md  > docs/CONTENT_EDITOR_GUIDE.md
git show 0b9301d3:docs/CONTENT_INVENTORY.md     > docs/CONTENT_INVENTORY.md
git show 11da48c5:docs/DEVELOPER_ARCHITECTURE.md > docs/DEVELOPER_ARCHITECTURE.md
```

### 4.2 Deleted Non-Content Files (recoverable)

| File | Description | Deleted in | Recovery |
|---|---|---|---|
| `admin/config.yml` | Decap CMS configuration | `c86b4ec6` — Fix SEO audit issues | Recoverable from git |
| `admin/index.html` | Decap CMS admin UI entry point | `c86b4ec6` — Fix SEO audit issues | Recoverable from git |
| `tools/project_images.py` | Old image-URL based thumbnail script (replaced by SVG icon system) | `055cc93e` — Replace external photos with SVG icons | Recoverable from git |

> **Note:** `admin/` was intentionally removed in `c86b4ec6`. The commit message says "remove admin/" as part of SEO audit fixes. Restoring it would reopen the Decap CMS endpoint, which may not be desired.

---

## 5. Missing Completely

**None.** Every file, YAML record, and page that was ever created is either:
- Currently live, OR
- In `projects/_archive/`, OR
- Recoverable from git history

There are no gaps where content was permanently lost.

---

## 6. Docs Directory — Current State

| File | Status |
|---|---|
| `docs/README.md` | Present |
| `docs/DHT22_TEMPLATE_REVIEW.md` | Present |
| `docs/MISSION01_FINAL_REVIEW.md` | Present |
| `docs/WEATHER_STATION_PROJECT_REVIEW.md` | Present |
| `docs/reports/HOMEPAGE_IMPLEMENTATION.md` | Present |
| `docs/reports/HOMEPAGE_V3_IMPLEMENTATION.md` | Present |
| `docs/assets/` | Empty directory (`.gitkeep`) |
| `docs/editorial/` | Empty directory (`.gitkeep`) |
| `docs/engineering` | Untracked stub |
| `docs/guides` | Untracked stub |
| `docs/reference` | Untracked stub |
| `docs/reviews` | Untracked stub |
| `docs/BLINK_LED_REVIEW.md` | **Deleted** — recoverable from `e21c192a` |
| `docs/CONTENT_EDITOR_GUIDE.md` | **Deleted** — recoverable from `11da48c5` |
| `docs/CONTENT_INVENTORY.md` | **Deleted** — recoverable from `0b9301d3` |
| `docs/DEVELOPER_ARCHITECTURE.md` | **Deleted** — recoverable from `11da48c5` |

---

## 7. Architecture Migration Summary

The repo went through one significant architectural migration on 2026-06-26 (`0b9301d3`).

**Before migration:** Each project had 2 named variant slugs × 33 numbered HTML pages each = 66 HTML files per project. All generated from a flat structure. No structured CMS YAML.

**After migration:** Each of the 15 projects has 1 parent YAML in `content/projects/` that generates 1 canonical project page in `projects/`. The 1,000 old variant pages are archived in `projects/_archive/` with a `noindex` meta tag, keeping the URLs alive but out of search.

**Two slugs were renamed during migration:**

| Old slug (archive) | New slug (content YAML) | Change |
|---|---|---|
| `esp32-esp32-learning-trainer` | `esp32-learning-trainer` | Removed duplicate `esp32-` prefix |
| `esp32-smart-irrigation-controller` | `esp32-smart-irrigation-system` | Name changed |

No content was lost in this migration. The hardware wiring data from archive pages was exported to `content/projects/*.yaml` via `tools/legacy/export_project_hardware.py`.

---

## 8. Git Commit Timeline (Content-Relevant)

| Date | Commit | Content created |
|---|---|---|
| 2026-06-18 | `3c1bf512` Convert to YAML CMS | 15 project YAMLs (stub) |
| 2026-06-18 | `c3b1beab` Deploy Phase 1 and Phase 2 guides | `what-is-esp32.yaml`, `installing-arduino-ide-esp32.yaml`, 2 guide HTML pages |
| 2026-06-18 | `c86b4ec6` Fix SEO audit issues | Deleted `admin/` |
| 2026-06-26 | `11da48c5` Build static learning platform | `blink-led-esp32.yaml`, `read-temperature-dht22.yaml`, `connect-oled-esp32.yaml`, 6 component YAMLs, `CONTENT_EDITOR_GUIDE.md`, `DEVELOPER_ARCHITECTURE.md` |
| 2026-06-26 | `0b9301d3` Clean architecture | `CONTENT_INVENTORY.md`, project YAML updates, legacy tools moved |
| 2026-06-26 | `53feb31c` Add roadmaps | `guide-roadmap.yaml` (100 missions), `component-roadmap.yaml` (210 components) |
| 2026-06-26 | `e21c192a` Golden Blink LED template | `BLINK_LED_REVIEW.md`, Blink LED mission YAML polished |
| 2026-06-26 | `d8afa2b3` Golden DHT22 template | DHT22 component YAML polished |
| 2026-06-26 | `d2e73ae4` Golden weather station template | Weather station project YAML polished |
| 2026-06-27 | `7a8f890c` Homepage v2 | Deleted `BLINK_LED_REVIEW.md`, `CONTENT_EDITOR_GUIDE.md`, `CONTENT_INVENTORY.md`, `DEVELOPER_ARCHITECTURE.md` |
| 2026-06-27 | `eb8ee076` Homepage v3 | No content changes |
