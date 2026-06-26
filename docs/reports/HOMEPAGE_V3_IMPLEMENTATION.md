# Homepage v3 Implementation Report

**Date:** 2026-06-27  
**Branch:** main  
**Build:** Static-first Phase 1

---

## Summary

Homepage v3 expands the four-section v2 landing page into a ten-section educational platform homepage. The design principle: guide the user from curiosity to confidence — each section has a unique emotional purpose and a visually distinct layout.

---

## Section Structure

| # | Section | Class | Background | Emotion |
|---|---|---|---|---|
| 1 | Hero | `.v2-declaration` | Dark `#0A0E1A` | Curiosity |
| 2 | Project Showcase | `.v2-proof` | Dark `#0A0E1A` | Desire |
| 3 | Choose Your Journey | `.v3-journey` | White `#FFFFFF` | Belonging |
| 4 | Learning Roadmap | `.v3-roadmap` | Off-white `#F7FAFC` | Confidence |
| 5 | Featured Mission | `.v3-mission-feature` | Blue-teal gradient | Momentum |
| 6 | Featured Component | `.v3-component-feature` | White `#FFFFFF` | Understanding |
| 7 | Featured Project | `.v3-project-feature` | Dark `#0D1117` | Ambition |
| 8 | Why ESP32 Engine | `.v3-why` | White `#FFFFFF` | Trust |
| 9 | Community Progress | `.v3-progress` | Deep dark `#0A0E1A` | Social proof |
| 10 | Final CTA | `.v2-invitation` | Dark `#0A0E1A` | Action |

Background rhythm: dark, dark, **white**, **off-white**, **dark-gradient**, **white**, **dark**, **white**, **dark**, dark — no two adjacent sections share the same layout pattern.

---

## New Sections (v3)

### Section 3 — Choose Your Journey
**Layout:** Full-width link rows (NOT cards). Row pattern: `num · badge · title + desc · meta · arrow`.

- Three paths: Beginner (guides), Builder (projects), Engineer (learning)
- Each row is a `<a>` link with animated left-border reveal on hover
- No cards: rows extend edge-to-edge within the content width
- Arrow translates right on hover; title turns primary blue

### Section 4 — Learning Roadmap
**Layout:** Three-pillar grid + horizontal mission arc.

- LEARN / BUILD / SHIP pillars with numbered labels (01, 02, 03)
- Horizontal mission arc: 12 nodes, milestone labels at 1/4/8/12
- Live missions (01–03) render as `<a>` links to real guide pages
- CTA at arc header: "Explore all guides →"
- Background `#F7FAFC` contrasts with white sections above and below

### Section 5 — Featured Mission
**Layout:** Two-column — content left, SVG illustration right.

- Badges: "Mission 01", "Beginner", time estimate
- Custom `_V3_LED_SVG`: ESP32 + wire + resistor + glowing LED circuit diagram
- Build list: 3 bullet outcomes (what the learner ships)
- Single CTA: "Start Mission 01 →" (ghost button on dark gradient)
- Background: `linear-gradient(145deg, #061E38, #083456, #055040)`

### Section 6 — Featured Component
**Layout:** Two-column — image panel left, specs right.

- Showcases DHT22 Temperature & Humidity Sensor
- Real component image from Shopify CDN (`loading="lazy"`)
- Spec list: 3 rows with label/value pairs, border-separated
- CTA: "Learn about DHT22 →" (accent soft → blue on hover)
- Background: White — product catalog clarity

### Section 7 — Featured Project
**Layout:** Two-column reversed — SVG illustration left, content right.

- Showcases ESP32 Mini Weather Station
- Reuses `_V2_SVG_WEATHER` illustration from v2
- Level chips: Beginner / Intermediate / Advanced (color-coded)
- Parts chips: ESP32 DevKit, DHT22 Sensor, 220 Ω Resistor
- CTA: "Start this project →" (primary blue, shadow glow)
- Background: `#0D1117` — dramatic, GitHub dark feel

### Section 8 — Why ESP32 Engine
**Layout:** Full-width 2-column rows (statement + detail). NOT icon grid.

- 6 differentiators as statement rows: bold left, detail right
- Rows separated by `1px solid #F1F5F9` dividers — contract / guarantee feel
- No cards, no icons — purely typographic authority
- Background: White

### Section 9 — Community Progress
**Layout:** 4-column large stat numbers, centered.

- Stats: 15 Projects / 5 Missions / 6 Components / 100% Free
- Numbers computed from actual content data at build time
- Radial glow atmosphere at center
- Note line below: "More missions, projects, and components added every month."
- Background: `#0A0E1A` — strong contrast from Why (white) above

---

## Visual Differentiation

Each section uses a different layout pattern:

| Section | Layout Pattern |
|---|---|
| Hero | 2-col grid: text + ESP32 SVG |
| Showcase | Full-bleed horizontal scroll |
| Journey | Full-width link rows (numbered) |
| Roadmap | 3-pillar grid + arc timeline |
| Mission Feature | 2-col: content + circuit SVG, gradient bg |
| Component Feature | 2-col: image panel + spec list |
| Project Feature | 2-col reversed: SVG + content, dark bg |
| Why | Full-width statement rows (no icons) |
| Progress | 4-col stat numbers, centered |
| Final CTA | Centered text + single button |

---

## Files Changed

| File | Change |
|---|---|
| `tools/site_layout.py` | Added `_V3_LED_SVG` constant + 7 new functions: `home_v3_journey`, `home_v3_roadmap`, `home_v3_mission_feature`, `home_v3_component_feature`, `home_v3_project_feature`, `home_v3_why`, `home_v3_progress` |
| `tools/rebuild_index.py` | Updated `home_html()` to call all 10 sections; added v3 imports; removed `home_v2_engine` call |
| `style.css` | Appended ~650 lines of `.v3-*` CSS: 7 section blocks + responsive (960px/768px) + dark mode overrides |
| `index.html` | Regenerated by build — do not edit directly |

---

## CSS Architecture

All v3 styles use the `.v3-` prefix. No existing CSS rules modified. Existing `.v2-*` rules preserved for backward compatibility.

New CSS blocks added to `style.css`:
- `.v3-journey` + journey rows — Choose Your Journey
- `.v3-roadmap` + arc track — Learning Roadmap
- `.v3-mission-feature` + mission pills/build list — Featured Mission
- `.v3-component-feature` + spec list — Featured Component
- `.v3-project-feature` + level/part chips — Featured Project
- `.v3-why` + statement rows — Why ESP32 Engine
- `.v3-progress` + stat grid — Community Progress
- `@media (max-width: 960px)` — tablet: collapses 2-col sections to 1-col, hides visuals
- `@media (max-width: 768px)` — mobile: hides journey row numbers
- `@media (prefers-color-scheme: dark)` — dark mode for white-background sections

---

## Design Rules Compliance

| Rule | Status |
|---|---|
| Each section unique emotional purpose | ✅ |
| No repeated cards | ✅ (Journey = rows; Why = statement rows; Progress = numbers) |
| No filler | ✅ |
| No long text | ✅ (max ~3 sentences per section) |
| Every section visually different | ✅ (10 distinct layout patterns) |
| Guide from curiosity to confidence | ✅ (emotional arc mapped to section order) |
| Only homepage modified | ✅ |
| Product, not landing page | ✅ (specific content, real data, real links) |
| Dark mode | ✅ |
| Responsive | ✅ |
| Build passes | ✅ |
| Validators pass | ✅ |
| Components/Guides/Projects/Templates untouched | ✅ |

---

## Build Output

```
Content inventory: 5 guides, 6 components, 15 projects, 11 pages
Content validation passed.
Wrote index.html + projects listing (15 projects, 1 page(s)) + projects.json
Build complete.
```
