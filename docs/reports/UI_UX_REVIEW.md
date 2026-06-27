# UI/UX Review — Dark & Light Mode Redesign

**Date:** 2026-06-27  
**CSS version:** `20260627-uiux-v1`  
**Scope:** Styling only — no content, URL, or build architecture changes.

## Summary

ESP32 Engine now uses a token-based theme system with explicit light and dark palettes, stronger contrast, visible borders on interactive surfaces, soft layered shadows, and a header theme toggle persisted in `localStorage`.

## Design Direction Applied

| Goal | Implementation |
|------|----------------|
| Stronger palette | Primary `#0088EE`, secondary `#00B894`, accent `#FFB020` (light); brighter variants in dark mode |
| High contrast text | Body `#0F172A` / muted `#475569` (light); `#F1F5F9` / `#94A3B8` (dark) |
| Card depth | 1.5px borders, `--border-strong`, `--shadow-sm/md/lg` on cards and panels |
| Button states | Hover lift, active scale, `:focus-visible` ring via `--ring` |
| Inputs | Themed backgrounds, 1.5px borders, focus ring on search/filter/newsletter fields |
| Navigation | Active nav link border + background; mobile nav full-width bordered links |
| Badges | Semantic token colors with subtle borders per difficulty/category |
| Theme toggle | Moon/sun icon in header; FOUC-prevention script in `<head>` |
| Mobile | Tighter header actions, stacked section heads, readable base font size |

## Files Changed

- `style.css` — theme tokens, component polish, dark-mode panel overrides
- `ui.js` — theme init, toggle, `theme-color` meta updates
- `tools/site_layout.py` — theme boot script, toggle button in header
- `content/site.yaml` — cache-bust `css_version`

## Page Verification (post-build)

Build: `py -3 tools/build_all.py` — **passed**

| Page | Path | Checks |
|------|------|--------|
| Homepage | `index.html` | Hero gradient tokens, path cards bordered, theme toggle present, CSS v20260627-uiux-v1 |
| Guides index | `guides.html` | Mission cards, category pills, nav/search/theme controls |
| Components index | `components.html` | Component cards with media border, filter inputs styled |
| Projects index | `projects.html` | Project cards, sticky filters, badge tokens |
| DHT22 | `components/dht22.html` | Component hero band, ELI12 panel, pin rows, FAQ accordions — dark overrides applied |
| Blink LED | `guides/blink-led-esp32.html` | Mission hero band, quiz options, code panel (unchanged dark chrome), step cards |
| Weather Station | `projects/esp32-iot-weather-station.html` | Project hero band, parts list, mission card gradient, related cards |

All listed pages include:

- Inline theme boot script before CSS load
- `style.css?v=20260627-uiux-v1`
- `#theme-toggle` button in header
- `ui.js` theme handler

## Light Mode Highlights

- Page background `#F0F4FA` with white elevated surfaces
- Cards lift on hover with primary border accent
- Primary CTA gradient blue → teal with glow shadow
- Footer deep navy `#0F172A` for clear section separation

## Dark Mode Highlights

- Page background `#0B1220`, surfaces `#141E2E` / `#1A2740`
- Content panels (ELI12, safety, output, quiz) use translucent tinted gradients
- Badge and quiz feedback colors adjusted for readability on dark surfaces
- Nav/header use semi-opaque dark glass backgrounds

## Accessibility Notes

- `:focus-visible` rings on buttons, links, inputs, nav items, carousel controls
- `color-scheme: light/dark` set per theme
- Contrast targets WCAG-friendly pairings for body text and badges
- Reduced-motion media query preserved

## Known Limitations

- Hero bands (mission/component/project) keep branded gradients in both modes — text remains white by design
- Code panels retain fixed dark syntax theme in both modes (intentional for code readability)
- Category thumbnail gradients (`.t-*`) simplified in dark mode to token-based media backgrounds

## Manual QA Recommended

1. Toggle theme on homepage and confirm persistence after reload
2. Open search overlay in both modes — input focus ring visible
3. Complete one quiz question on Blink LED — correct/wrong feedback readable in both modes
4. Resize to mobile — nav drawer, theme toggle, and filter stack usable
