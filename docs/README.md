# ESP32 Engine — Documentation

Map of all repository documentation. Website content lives in `content/` (YAML); this folder is for humans maintaining the project.

---

## Folder guide

| Folder | Purpose | Put here |
|--------|---------|----------|
| **`editorial/`** | Voice, pedagogy, and content policy | Manifesto, educational framework, writing style guide (planned) |
| **`guides/`** | How-to for editors and authors | Step-by-step workflows — adding guides, components, projects, assets |
| **`engineering/`** | Build system and architecture | Developer architecture, CI notes, tooling design |
| **`reference/`** | Lookups and inventories | Content inventories, roadmaps, file maps |
| **`reviews/`** | Time-bound audits | Sprint reviews, template readiness reports, quality scores |
| **`assets/`** | Documentation about visual assets | Central indexes and specs that complement `assets/visuals/` |

---

## Current documents

### Guides

| Document | Description |
|----------|-------------|
| [guides/CONTENT_EDITOR_GUIDE.md](guides/CONTENT_EDITOR_GUIDE.md) | Edit YAML, run the build, add guides/components/projects |

### Engineering

| Document | Description |
|----------|-------------|
| [engineering/DEVELOPER_ARCHITECTURE.md](engineering/DEVELOPER_ARCHITECTURE.md) | Static-first build pipeline, folder layout, Phase 2 notes |

### Reference

| Document | Description |
|----------|-------------|
| [reference/CONTENT_INVENTORY.md](reference/CONTENT_INVENTORY.md) | Source vs generated file inventory |

### Reviews

| Document | Description |
|----------|-------------|
| [reviews/BLINK_LED_REVIEW.md](reviews/BLINK_LED_REVIEW.md) | Blink LED mission template review |
| [reviews/DHT22_TEMPLATE_REVIEW.md](reviews/DHT22_TEMPLATE_REVIEW.md) | DHT22 component template review |
| [reviews/MISSION01_FINAL_REVIEW.md](reviews/MISSION01_FINAL_REVIEW.md) | Mission 01 golden guide final review |
| [reviews/WEATHER_STATION_PROJECT_REVIEW.md](reviews/WEATHER_STATION_PROJECT_REVIEW.md) | Weather station project template review |

### Editorial

*Empty — reserved for manifesto, educational framework, and writing style guide.*

### Asset documentation (co-located with files)

| Document | Description |
|----------|-------------|
| [../assets/visuals/README.md](../assets/visuals/README.md) | Visual asset naming, sizes, formats, alt text |
| [../assets/visuals/guides/wiring/blink-led-wiring-spec.md](../assets/visuals/guides/wiring/blink-led-wiring-spec.md) | Blink LED wiring diagram production spec |

---

## Related (outside `docs/`)

| Location | Description |
|----------|-------------|
| [../README.md](../README.md) | Repo quick start |
| [../content/manifest.yaml](../content/manifest.yaml) | Content folder map |
| [../static.config.yaml](../static.config.yaml) | Phase 1 static-first config |

---

## Where new docs belong

1. **Editorial policy** (tone, age levels, mission structure) → `docs/editorial/`
2. **“How do I add X?”** → `docs/guides/`
3. **Build, templates, Python tools** → `docs/engineering/`
4. **Inventories, slug lists, roadmaps** → `docs/reference/`
5. **One-off sprint or template audit** → `docs/reviews/`
6. **Illustrator handoff next to an asset file** → `assets/visuals/...` (keep co-located specs there; optional summary in `docs/assets/`)

After adding a doc, link it from this README.
