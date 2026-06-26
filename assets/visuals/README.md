# ESP32 Engine — Visual Asset System

Planning-only folder structure for illustrations, photos, wiring diagrams, icons, and mascot assets.

**Do not edit generated HTML.** Add files here, reference them from `content/` YAML, then run `py tools/build_all.py`.

---

## Folder map

```
assets/visuals/
├── heroes/                      Site & landing hero backgrounds (optional)
├── components/
│   ├── photos/                  Real product / module photos
│   ├── pinouts/                 Pin label diagrams (top or angled view)
│   └── illustrations/           Simplified component explainer art
├── guides/
│   ├── wiring/                  Mission wiring diagrams
│   ├── concepts/                “How it works” concept art
│   └── outputs/                 Expected result screenshots / photos
├── projects/
│   ├── heroes/                  Project hero / banner art
│   ├── wiring/                  Full project wiring diagrams
│   └── outputs/                 Finished build photos & Serial Monitor shots
├── icons/
│   ├── categories/              Category pills & cards (IoT, Sensors, …)
│   └── badges/                  Difficulty, time, parent-safe badges (if custom)
└── mascot/                      ESP32 Engine mascot poses & expressions
```

---

## Naming conventions

Use **lowercase**, **hyphens**, no spaces, no dates in filenames.

| Pattern | Example | Use for |
|---------|---------|---------|
| `{slug}-hero.{ext}` | `dht22-hero.webp` | Component / project hero image |
| `{slug}-photo.{ext}` | `esp32-devkit-photo.webp` | Product photo |
| `{slug}-pinout.{ext}` | `dht22-pinout.svg` | Pinout diagram |
| `{slug}-illustration.{ext}` | `dht22-illustration.svg` | Simplified explainer |
| `{guide-slug}-wiring.{ext}` | `blink-led-esp32-wiring.svg` | Guide wiring diagram |
| `{guide-slug}-concept.{ext}` | `blink-led-esp32-concept.svg` | Guide concept diagram |
| `{guide-slug}-output.{ext}` | `blink-led-esp32-output.webp` | Expected output visual |
| `{project-slug}-hero.{ext}` | `esp32-iot-weather-station-hero.webp` | Project hero |
| `{project-slug}-wiring.{ext}` | `esp32-iot-weather-station-wiring.svg` | Project wiring |
| `{project-slug}-output.{ext}` | `esp32-iot-weather-station-output.webp` | Finished build |
| `category-{name}.{ext}` | `category-iot-projects.svg` | Category icon |
| `badge-{name}.{ext}` | `badge-parent-safe.svg` | Custom badge icon |
| `mascot-{pose}.{ext}` | `mascot-waving.svg` | Mascot illustration |

**Slug rule:** Match the content slug in `content/guides/`, `content/components/`, or `content/projects/` exactly.

**Variants:** Add `-@2x` before the extension for retina PNG/WebP only when needed (e.g. `dht22-hero@2x.webp`).

---

## Recommended image sizes

| Asset type | Width × height | Notes |
|------------|----------------|-------|
| Component photo | 800 × 600 px | 4:3 ratio; subject centered, padding ~10% |
| Component pinout | 600 × 400 px | SVG preferred; labels readable at 320px wide |
| Guide wiring diagram | 960 × 540 px | 16:9; breadboard + ESP32 legible on mobile |
| Guide concept | 720 × 480 px | Simple; max 5 labeled elements |
| Guide output | 800 × 450 px | Serial Monitor screenshot or photo crop |
| Project hero | 1200 × 630 px | Also works as OG preview crop |
| Project wiring | 960 × 540 px | Same rules as guide wiring |
| Project output | 800 × 600 px | Finished build, desk context OK |
| Category icon | 64 × 64 px (SVG) | Single color or two-tone |
| Badge icon | 24 × 24 px (SVG) | Must read at 16px |
| Mascot | 512 × 512 px | Transparent background; SVG preferred |

Export **2×** source art when using raster formats, then compress for web.

---

## File formats

| Format | When to use |
|--------|-------------|
| **SVG** | Wiring diagrams, pinouts, icons, mascot, concept art with flat shapes |
| **WebP** | Photos, hero banners, output screenshots (best size/quality) |
| **PNG** | Photos needing transparency; fallback when WebP unsupported |
| **JPEG** | Avoid for UI assets; OK for temporary external photos only |

**Rule of thumb:** Diagrams and icons → **SVG**. Photos and screenshots → **WebP** (with PNG fallback optional). Never use GIF for diagrams.

---

## SVG vs PNG vs WebP (decision tree)

1. **Is it a diagram, icon, or mascot with flat colors?** → SVG  
2. **Is it a photograph or realistic screenshot?** → WebP (quality 80–85)  
3. **Does it need transparency and SVG is impractical?** → PNG  
4. **Is it a temporary CDN placeholder?** → Keep URL in YAML until local asset exists, then replace with `/assets/visuals/...`

---

## Alt text rules

Every image used on the site needs alt text in YAML — never rely on the filename alone.

| Do | Don't |
|----|-------|
| Describe what the learner sees | Start with "Image of…" |
| Include pin names for wiring (`GPIO4`, `VCC`, `GND`) | Use marketing fluff |
| Keep under ~125 characters when possible | Duplicate the section heading verbatim |
| Match kid-friendly tone on missions | Use jargon without context |

**Examples:**

- Wiring: `DHT22 module — VCC to 3.3 V, GND to GND, DATA to GPIO4 on ESP32`
- Photo: `DHT22 temperature and humidity sensor module, three pins labeled`
- Output: `Serial Monitor showing Temperature 24.3 C and Humidity 55 percent`

Store alt text in YAML (`illustration_alt`, `image_alt`, or `alt` fields). If an image is purely decorative, use empty alt in templates only when explicitly marked decorative.

---

## Placeholder rules

Until a real asset exists:

1. **Keep `illustration_alt` filled in YAML** — templates render a labeled placeholder frame using this text.
2. **Do not add broken image paths** — omit `image:` or `image:` path until the file exists under `assets/visuals/`.
3. **Placeholders are temporary** — track missing art in roadmaps (`content/guide-roadmap.yaml`, `content/component-roadmap.yaml`).
4. **One placeholder per section** — wiring, concept, and output each get their own future file; do not reuse one diagram for all three.
5. **Emoji in content YAML is not a substitute** for production wiring art.

When the asset is ready: add file → update YAML path → rebuild → verify in browser.

---

## Wiring diagram style rules

All wiring diagrams (guides & projects) should look like one family:

- **Layout:** ESP32 DevKit on the left, breadboard center, components on the right (or module-only for 3-pin sensors).
- **Lines:** 2px stroke, rounded corners, color-coded:
  - Power (3.3 V): `#0099FF`
  - Ground: `#64748B`
  - Signal / data: `#00C896`
- **Labels:** Pin names on both ends; use `GPIO4` not just `4`.
- **Background:** White or `#F7FAFC`; no dark mode variants yet.
- **Typography:** Sans-serif labels, 14px minimum at export size.
- **No photos inside wiring SVGs** — vector only.
- **Kid clarity:** Long leg (+) / short leg (−) labels for LEDs; VCC/GND/DATA for modules.
- **Export:** Master in SVG; optional WebP preview for docs only.

File location: `assets/visuals/guides/wiring/` or `assets/visuals/projects/wiring/`.

---

## Component photo rules

- Neutral background (white or light gray `#F0F4F8`).
- Module fills ~70% of frame; pins visible.
- No watermarks, no retailer logos.
- Prefer your own photo or licensed stock; document source in commit message if external.
- Match slug filename: `assets/visuals/components/photos/dht22-photo.webp`.
- Optional subfolder per slug: `components/photos/dht22/hero.webp` if multiple angles needed.

---

## Mascot usage rules

- **Purpose:** Friendly guide for kids on homepage, empty states, and celebration moments — not every section header.
- **Location:** `assets/visuals/mascot/`
- **Formats:** SVG master; WebP/PNG for complex shading if needed.
- **poses:** `mascot-waving`, `mascot-thinking`, `mascot-celebrating`, `mascot-wiring` (safe, no bare wires to mains).
- **Size on page:** Max 120px wide inline; up to 240px in hero empty states.
- **Accessibility:** Decorative mascot → `aria-hidden="true"`. Mascot conveying info → meaningful alt text.
- **Do not** replace component photos or wiring diagrams with the mascot.

---

## Replacing temporary online images

Several live components use external CDN URLs (SparkFun, Shopify, etc.). Migrate to local assets in this order:

1. **Add file** under `assets/visuals/components/photos/{slug}-photo.webp`
2. **Update YAML** in `content/components/{slug}.yaml`:

   ```yaml
   image: /assets/visuals/components/photos/dht22-photo.webp
   image_alt: DHT22 temperature and humidity sensor module, three pins labeled
   ```

3. **Run** `py tools/build_all.py`
4. **Verify** component hero and index card
5. **Commit** both the asset and YAML change together
6. **Remove** the old `https://…` URL from YAML — do not leave dual references

Same pattern for guides and projects when `image:` or `illustration:` fields are wired to templates:

```yaml
# Guide mission block (future / when template supports image path)
wiring:
  illustration_alt: Breadboard — ESP32 GPIO2 to resistor to LED anode, cathode to GND
  image: /assets/visuals/guides/wiring/blink-led-esp32-wiring.svg

concept:
  illustration_alt: ESP32 GPIO pin through resistor to LED anode, cathode to ground
  image: /assets/visuals/guides/concepts/blink-led-esp32-concept.svg
```

Until templates read `image:`, keep `illustration_alt` populated and add the file path in YAML as documentation-ready (build ignores unknown fields safely).

---

## Workflow checklist

1. Create or export asset using rules above
2. Save to the correct `assets/visuals/…` folder
3. Update the matching `content/` YAML with path + alt text
4. Run `py tools/build_all.py`
5. Spot-check mobile width (375px) and keyboard focus if interactive
6. Commit assets + YAML together

---

## Related docs

- `docs/guides/CONTENT_EDITOR_GUIDE.md` — YAML fields and build workflow
- `docs/reference/CONTENT_INVENTORY.md` — what is source vs generated
- `content/guide-roadmap.yaml` / `content/component-roadmap.yaml` — planned art needs
