# ESP32 Engine Visual Style Guide

## Purpose

ESP32 Engine visuals should feel like one premium educational electronics platform, not a collection of unrelated project images. Every hero, thumbnail, diagram, component image, and share card must use the same visual language: real hardware, clean learning context, precise diagrams, restrained color, and a modern engineering finish.

The goal is simple: when a learner sees any ESP32 Engine asset, it should immediately feel trustworthy, practical, and part of the same brand.

## Visual Principles

1. Real hardware first. Projects should show finished builds with the ESP32 clearly visible.
2. Educational clarity over decoration. Every visual should help the learner understand the project, component, or wiring.
3. Premium but quiet. Use soft lighting, controlled depth, clean backgrounds, and restrained accent colors.
4. Consistent systems. Aspect ratios, shadows, labels, wire colors, icons, and diagram strokes must stay predictable.
5. No broken or empty states. If final artwork does not exist, use a branded placeholder that still feels intentional.

## Brand Visual Language

### Color Palette

Use existing ESP32 Engine brand colors as the source of truth.

| Role | Color | Usage |
| --- | --- | --- |
| ESP32 Blue | `#0099FF` | Primary glow, active labels, Wi-Fi, signal accents |
| Signal Teal | `#00C896` | Sensors, successful states, secondary accents |
| Deep Navy | `#0A0E1A` | Dark backgrounds, hero depth, diagram panels |
| Ink | `#111827` | Light mode titles and high-contrast text |
| Slate | `#64748B` | Metadata, secondary labels, diagram captions |
| Soft Blue | `#EFF8FF` | Light section backgrounds and placeholder panels |
| Soft Gray | `#F6F8FB` | Neutral surfaces and diagram canvas backgrounds |
| Amber | `#FFD54F` | LEDs, warning states, tiny status highlights only |
| Red | `#FF6B6B` | Alarms, error states, security alerts only |

Do not introduce random project colors. Category-specific accents may tint small labels or glows, but the base system remains blue, teal, navy, white, and slate.

### Lighting

Project and component imagery should use:

- Soft diffused key light from top-left.
- Subtle cool blue rim light behind or beside the ESP32 board.
- Very small warm practical glow only for LEDs or displays.
- Low contrast shadows with visible detail, never harsh studio shadows.
- Consistent color grading: clean whites, cool highlights, neutral shadows.

### Backgrounds

Approved backgrounds:

- Matte graphite work surface.
- Soft white or light gray lab bench.
- Very pale blue gradient surface.
- Subtle printed PCB trace or grid pattern at low opacity.

Avoid:

- Random stock desks.
- Busy tool benches.
- Gaming neon backgrounds.
- Crypto-style glowing grids.
- Heavy texture, dust, clutter, or fingerprints.

### Camera and Perspective

Use one repeatable product photography language:

- Primary camera angle: 3/4 top-down, 35 to 45 degrees.
- Lens feel: 50mm to 70mm equivalent, mild depth of field.
- Project hero crop: finished build centered, ESP32 visible, supporting components arranged around it.
- Component photo crop: isolated part at slight 3/4 angle with clean shadow.
- Diagrams: flat orthographic SVG, no perspective distortion.

### Radius, Shadow, and Safe Area

| Asset Type | Radius | Shadow | Safe Area |
| --- | --- | --- | --- |
| Project hero image | 24px in UI, source image full bleed | Soft ambient, below-right | 8% minimum |
| Project thumbnail | 18px in UI, source image full bleed | Soft card shadow | 10% minimum |
| Component card image | 16px in UI | Soft contact shadow | 12% minimum |
| Diagram canvas | 16px in UI | Minimal or none | 6% minimum |
| Open Graph image | No rounded corners in source | Built-in composition depth | 9% minimum |
| Icon | No shadow in SVG source | Shadow only in UI if needed | 16% minimum |

## Asset Dimensions

| Asset | Size | Ratio | Format | Target Path |
| --- | ---: | --- | --- | --- |
| Site/home hero art | 2400 x 1350 | 16:9 | WebP + PNG fallback if needed | `assets/visuals/heroes/{name}-hero.webp` |
| Project hero | 1600 x 900 | 16:9 | WebP | `assets/visuals/projects/heroes/{project-slug}-hero.webp` |
| Project thumbnail | 1200 x 750 | 8:5 | WebP | `assets/visuals/projects/thumbs/{project-slug}-thumb.webp` |
| Finished project photo | 1600 x 1200 | 4:3 | WebP | `assets/visuals/projects/outputs/{project-slug}-output.webp` |
| Project wiring diagram | 1600 x 1000 | 8:5 | SVG | `assets/visuals/projects/wiring/{project-slug}-wiring.svg` |
| Guide concept image | 1400 x 900 | 14:9 | WebP or SVG | `assets/visuals/guides/concepts/{guide-slug}-concept.webp` |
| Guide output image | 1400 x 900 | 14:9 | WebP | `assets/visuals/guides/outputs/{guide-slug}-output.webp` |
| Guide wiring diagram | 1600 x 1000 | 8:5 | SVG | `assets/visuals/guides/wiring/{guide-slug}-wiring.svg` |
| Component photo | 1600 x 1200 | 4:3 | WebP | `assets/visuals/components/photos/{component-slug}-photo.webp` |
| Component transparent | 1600 x 1200 | 4:3 | PNG | `assets/visuals/components/photos/{component-slug}-transparent.png` |
| Component labeled view | 1600 x 1200 | 4:3 | SVG | `assets/visuals/components/illustrations/{component-slug}-labeled.svg` |
| Component pinout | 1600 x 1200 | 4:3 | SVG | `assets/visuals/components/pinouts/{component-slug}-pinout.svg` |
| Component wiring | 1600 x 1000 | 8:5 | SVG | `assets/visuals/components/wiring/{component-slug}-wiring.svg` |
| Open Graph image | 1200 x 630 | 1.91:1 | PNG or WebP | `assets/visuals/social/og/{page-slug}-og.png` |
| Social square image | 1080 x 1080 | 1:1 | PNG or WebP | `assets/visuals/social/square/{page-slug}-square.png` |
| Category icon | 512 x 512 | 1:1 | SVG | `assets/visuals/icons/categories/{category-slug}.svg` |
| Badge icon | 256 x 256 | 1:1 | SVG | `assets/visuals/icons/badges/{badge-slug}.svg` |

## Folder Structure

```text
assets/visuals/
  brand/
  heroes/
  projects/
    heroes/
    thumbs/
    outputs/
    wiring/
  components/
    photos/
    illustrations/
    pinouts/
    wiring/
  guides/
    concepts/
    outputs/
    wiring/
  icons/
    categories/
    badges/
  social/
    og/
    square/
  mascot/
```

The existing folders remain valid. Add missing folders only when the related asset type is produced.

## Naming Convention

Use lowercase kebab-case, tied to the canonical page slug.

```text
{slug}-hero.webp
{slug}-thumb.webp
{slug}-output.webp
{slug}-wiring.svg
{slug}-photo.webp
{slug}-transparent.png
{slug}-labeled.svg
{slug}-pinout.svg
{slug}-og.png
{slug}-square.png
```

Rules:

- No spaces.
- No version labels like `final`, `new`, or `updated`.
- No camera filenames.
- No mixed suffixes for the same asset role.
- If an asset is replaced, keep the same filename so templates and metadata stay stable.

## Project Hero Images

Every project hero should include:

- Finished real-world project.
- ESP32 board clearly visible.
- Main sensor, actuator, display, or module visible.
- Clean workspace with minimal supporting tools.
- Premium background with subtle depth.
- Same 3/4 top-down camera language.
- Consistent cool-blue grading with small warm highlights only where the electronics require it.

Composition:

- Put the ESP32 in the central third or lower central third.
- Put the primary output or visible result in the upper third.
- Leave safe area on the left or right for possible UI crops.
- Keep wires tidy and readable.
- Avoid hands unless a project specifically needs scale.
- Avoid text overlays inside the photo.

## Project Thumbnails

Project thumbnails should be cropped or generated from the same visual system as the hero.

Standards:

- 8:5 ratio.
- Clear subject at small card size.
- ESP32 visible when possible.
- Strong silhouette and readable component layout.
- No random stock image crops.
- No screenshots unless the project is primarily software/dashboard driven.

For homepage Top Picks, use the real thumbnail if it exists. If it does not exist, use the branded category placeholder for that exact project category. Never render a broken image or an empty card.

## Component Images

Each component page should eventually include five assets:

1. Isolated component photo.
2. Transparent component cutout.
3. Labeled component illustration.
4. Pinout diagram.
5. Wiring example with ESP32.

Component photo standards:

- One component per image.
- Slight 3/4 angle on a clean matte surface.
- Soft contact shadow.
- Pin side visible when important.
- No unrelated parts in frame.

Transparent cutout standards:

- True transparent PNG.
- Clean edge mask.
- Natural contact shadow removed.
- Component centered with 12% safe area.

Labeled and pinout standards:

- Flat SVG style.
- Labels outside the component body with leader lines.
- Labels use Inter or system sans, 28px source size minimum.
- GPIO/pin names use JetBrains Mono or system monospace.
- High contrast in light and dark UI contexts.

## Wiring Diagrams

All wiring diagrams use one SVG language.

Canvas:

- `viewBox="0 0 1600 1000"` for project and guide diagrams.
- Background `#F6F8FB` for light export.
- Optional dark mode variant only if needed later.
- 64px safe margin.

Linework:

- Main component strokes: 2px to 3px.
- Wire strokes: 6px with round caps.
- Leader lines: 2px, dashed only for optional paths.
- Connector points: 12px circles or rounded pads.

Wire colors:

| Wire | Color | Meaning |
| --- | --- | --- |
| Red | `#EF4444` | 3.3 V or 5 V power |
| Black | `#111827` | GND |
| Blue | `#2563EB` | General signal |
| Teal | `#00A884` | I2C SDA |
| Amber | `#F59E0B` | I2C SCL or clock |
| Purple | `#7C3AED` | Data bus or one-wire data |
| Orange | `#EA580C` | PWM, motor, relay control |
| Gray | `#64748B` | Optional, mechanical, or inactive connection |

Labels:

- Always label ESP32 GPIO numbers and component pin names.
- Use both electrical name and board label where useful, for example `GPIO21 / SDA`.
- Put power labels near rails.
- Use short labels, never paragraphs.
- Keep labels outside wires whenever possible.

Breadboard:

- Consistent 830-point breadboard shape when used.
- Power rails must be visibly separated and labeled.
- Do not show wires crossing pin labels.
- Use right-angle or gentle-curved wire paths, not chaotic freehand paths.

## Pinout Diagrams

Pinouts are teaching tools, not decorative posters.

Standards:

- Component centered.
- Pins grouped by function.
- Power pins first, then communication, then optional pins.
- Color pin groups with restrained accent colors.
- Include a small warning note only when a pin is not 5 V tolerant, boot-sensitive, input-only, or power-limited.
- Use SVG for crisp scaling.

## Open Graph and Social Images

Open Graph images must look like editorial covers for a premium technical library.

OG standards:

- 1200 x 630.
- Left side: page title, category, ESP32 Engine logo.
- Right side: project/component visual or diagram detail.
- Background: deep navy or soft blue depending on page tone.
- Include subtle PCB traces at low opacity.
- Keep all text inside a 90px safe margin.
- No tiny code snippets, cluttered wiring, or long descriptions.

Social square standards:

- 1080 x 1080.
- Centered object or diagram detail.
- Short title only.
- Same color grading and logo placement as OG.

## Category Icons

Category icons should be simple, geometric, and technical.

Standards:

- SVG only.
- 512 x 512 viewBox.
- 2px to 3px source stroke scaled proportionally.
- Rounded line caps and joins.
- No emoji.
- No filled cartoon illustration.
- Use ESP32 Blue as the primary stroke and Signal Teal as a small secondary accent.
- Icons must work at 20px in navigation and 64px in cards.

## Illustration Standards

Use illustration when photography would be unclear, such as conceptual guides, wiring flows, or abstract categories.

Rules:

- Flat technical style with restrained depth.
- Light gradients are allowed for surfaces, not for random decoration.
- No hand-drawn style.
- No 3D cartoon style.
- No mixed icon packs.
- Use the same stroke widths, radii, shadows, and label styles as wiring diagrams.

## Placeholder System

Until final artwork exists, use premium branded placeholders.

Placeholder requirements:

- Correct aspect ratio for the asset role.
- Project or component title included only when helpful.
- Category icon or simplified hardware silhouette.
- Subtle PCB trace or dot-grid motif.
- ESP32 Blue and Signal Teal accents.
- Soft blue or deep navy background.
- Same border radius and safe area as final assets.

Placeholder naming:

```text
{slug}-placeholder.svg
{category-slug}-placeholder.svg
```

Never use:

- Broken image icons.
- Empty gray boxes.
- Random Unsplash-style photos.
- Mixed AI styles from asset to asset.

## Homepage Asset Rules

The homepage is approved and should not be redesigned for asset integration.

Asset behavior:

- Top Picks should display actual project imagery when available.
- If a Top Picks project lacks a real thumbnail, use the matching category placeholder.
- Showcase visuals should remain consistent with the same board, lighting, and diagram style.
- Do not add new homepage sections for artwork.
- Do not change homepage content to make an image fit.

## Accessibility

- Every content image needs useful `alt` text.
- Decorative glows and patterns should be hidden from assistive technology.
- Diagram labels must meet WCAG AA contrast against the canvas.
- Avoid text embedded in raster images when HTML text can do the job.
- Pin labels embedded in SVG must remain readable at mobile sizes.
- Focus states and hover states belong to UI code, not baked into images.

## Performance

- Use SVG for diagrams, icons, pinouts, and simple placeholders.
- Use WebP for project and component photography.
- Keep project thumbnails under 180 KB where possible.
- Keep project heroes under 350 KB where possible.
- Keep OG images under 500 KB where possible.
- Avoid animated images.
- Do not ship high-resolution transparent PNGs where WebP or SVG will work.

## Asset QA Checklist

Before publishing a new visual:

- The asset uses the approved dimensions and naming.
- The ESP32 or relevant component is clearly visible.
- The visual matches the brand color and lighting system.
- The crop works at mobile card size.
- The alt text is accurate.
- The file size is acceptable.
- The image has no random watermarks, logos, or stock-photo artifacts.
- The same asset role does not use a different radius, shadow, or style elsewhere.
- Dark mode and light mode presentation both look intentional.
