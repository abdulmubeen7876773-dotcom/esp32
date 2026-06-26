# ESP32 Engine — Content Editor Guide

**Read this when you come back after a break.** You do not need to remember how the site works — just follow the steps below.

---

## Source of truth (edit only these folders)

All normal content editing happens in three folders under `content/`:

| Folder | What you edit | Build output |
|--------|---------------|--------------|
| **`content/guides/`** | Mission journeys and reference guides | `guides/*.html`, `guides.html` |
| **`content/components/`** | Component encyclopedia entries | `components/*.html`, `components.html` |
| **`content/projects/`** | Project metadata and wiring | `projects/*.html`, `projects.json`, `feed.xml` |

Also edit when needed:

- `content/pages/*.yaml` — static pages (about, parents, teachers, etc.)
- `content/home.yaml` — homepage hero text
- `content/site.yaml` — domain, analytics, CSS version
- `assets/visuals/` — illustrations, photos, wiring diagrams, icons, mascot (see section 9)

**Never edit generated files** — see section 6 below.

---

## The one rule

**Only edit YAML inside `content/`.**  
Run `py tools/build_all.py` to regenerate HTML, sitemap, feed, and search index.

---

## Quick checklist (every time you publish)

1. Edit or add a YAML file in `content/guides/`, `content/components/`, or `content/projects/`
2. Run the build:
   ```
   py tools/build_all.py
   ```
3. Push to GitHub (`main` branch)
4. Wait 1–2 minutes — GitHub Actions rebuilds and deploys

That is the entire workflow.

---

## 1. How to add a new guide

Guides live in **`content/guides/`**.

### Mission guide (recommended — kid-friendly journey format)

1. Copy an existing mission file:
   - `content/guides/blink-led-esp32.yaml` ← best template
2. Save as `content/guides/your-slug.yaml` (use lowercase and hyphens)
3. Change these fields at the top:

   | Field | Example |
   |-------|---------|
   | `slug` | `my-new-mission` |
   | `title` | `My New Mission \| ESP32 Engine` |
   | `headline` | `My New Mission` |
   | `meta_description` | Short sentence for Google |
   | `sort_order` | Next number (e.g. `4`) |
   | `mission_number` | Next mission number |

4. Fill in the `mission:` block (story, eli12, wiring, code, quiz, etc.)
5. Run `py tools/build_all.py`
6. Your page will be at: `/guides/your-slug.html`

**Tip:** Link to components with full paths like `/components/dht22.html`.

**Images:** When wiring or concept art exists, add files under `assets/visuals/guides/` and set paths in the mission block — see section 9.

### Reference guide (long article format)

1. Copy `content/guides/what-is-esp32.yaml`
2. Remove `format: mission` and the `mission:` block
3. Add an `intro:` block with `story`, `eli12`, and `safety` for kid-friendly opening
4. Write technical content in `body_html:` using HTML tags (`<h2>`, `<p>`, `<ul>`, etc.)
5. Rebuild

---

## 2. How to add a new component

Components live in **`content/components/`**.

1. Copy `content/components/dht22.yaml`
2. Save as `content/components/your-part.yaml`
3. Update:

   | Field | What to write |
   |-------|---------------|
   | `slug` | `your-part` (matches filename) |
   | `name` | Display name |
   | `category` | One of: Sensors, Displays, Motors, Communication, Power, Storage, Audio, Boards, Cameras, Input Devices, Others |
   | `difficulty` | Beginner, Intermediate, or Advanced |
   | `summary` | One sentence |
   | `eli12` | Simple explanation for kids |
   | `specs`, `pins`, `example_code`, etc. | Fill in the rest |

4. Run `py tools/build_all.py`
5. Page appears at: `/components/your-part.html`

**Images:** Product photo → `assets/visuals/components/photos/`. Pinout → `components/pinouts/`. See section 9.

**Categories list:** see `content/component-categories.yaml` if you need to add a new category.

---

## 3. How to add a new project

Projects live in **`content/projects/`**.

1. Copy `content/projects/esp32-iot-weather-station.yaml`
2. Save as `content/projects/esp32-your-project.yaml`
3. For golden projects, set `format: golden` and fill the `project:` block (see that file for the full template)
4. For staged projects, update at minimum:

   | Field | Example |
   |-------|---------|
   | `slug` | `esp32-your-project` |
   | `title` | `ESP32 Your Project` |
   | `category` | IoT Projects, Robotics, Agriculture, etc. |
   | `description` | One paragraph summary |
   | `sensor` | Main sensor used |
   | `output` | Main output (relay, OLED, etc.) |
   | `source_base` | Legacy archive filename prefix (for fallback wiring) |
   | `featured` | `true` or `false` |
   | `hardware` | Wiring table — edit pins and components directly |

4. Edit the `hardware:` block to set wiring, sensor pin, and output pin
5. Run `py tools/build_all.py`
6. Page appears at: `/projects/esp32-your-project.html`

**Images:** Project hero, wiring, and output art → `assets/visuals/projects/`. See section 9.

**Note:** Golden projects (`format: golden`) use the single-scroll template. Other projects still generate Beginner, Intermediate, and Advanced stages from YAML + `hardware:`.

---

## 4. How to update the search index

**You do not edit the search index by hand.**

Search reads from **`search-index.json`**, which is rebuilt from all content files every time you run:

```
py tools/build_all.py
```

When you add or edit a guide, component, project, or page in `content/`, the search index updates automatically.

---

## 5. How to rebuild the site

From the project folder:

```
py tools/build_all.py
```

**Requirements (one-time on your computer):**
- Python 3.10+
- Run once: `pip install -r requirements.txt`

**What the build does:**
1. Validates your YAML content
2. Generates all HTML pages from `content/guides/`, `content/components/`, `content/projects/`
3. Updates `search-index.json`, `projects.json`, `project-icons.js`, `sitemap.xml`, `feed.xml`
4. Prints `Build complete` when done

**If build fails:** read the error message — it usually names the file and field that needs fixing.

---

## 6. What files should NEVER be hand-edited

These are **generated**. Your edits will be overwritten on the next build.

| Do not edit | Built from |
|-------------|------------|
| `*.html` (root and subfolders) | `content/` YAML |
| `guides/*.html` | `content/guides/` |
| `components/*.html` | `content/components/` |
| `projects/*.html` (parent pages) | `content/projects/` |
| `category/*.html` | Build scripts |
| `search-index.json` | All content |
| `projects.json` | `content/projects/` |
| `project-icons.js` | Project categories |
| `sitemap.xml` | All public URLs |
| `feed.xml` | `content/projects/` |

### Safe to edit

| Folder / file | Purpose |
|---------------|---------|
| `content/guides/` | **Guide source** |
| `content/components/` | **Component source** |
| `content/projects/` | **Project source** |
| `content/pages/`, `content/home.yaml`, `content/site.yaml` | Other site content |
| `assets/visuals/` | **Visual assets** (photos, diagrams, icons, mascot) |
| `style.css` | Visual design |
| `ui.js`, `search.js`, `mission-guide.js` | Client behavior |
| `static.config.yaml` | Architecture settings |
| `tools/` | Build scripts (developers only) |

---

## 7. How to deploy to GitHub Pages

### Every publish

```
git add content/
git commit -m "Add new guide: my-mission"
git push origin main
```

GitHub Actions (`.github/workflows/build-site.yml`) validates content, runs `py tools/build_all.py`, and commits generated artifacts.

**You can also build locally first** to preview, then push both `content/` and generated files.

---

## 8. Coming back after 10+ days

1. Open `content/guides/`, `content/components/`, or `content/projects/`
2. Copy the nearest existing YAML file
3. Edit text fields
4. Run `py tools/build_all.py`
5. Push to `main`

---

## 9. Visual assets (images & diagrams)

All production art lives under **`assets/visuals/`**. Full rules: **`assets/visuals/README.md`**.

### Where to put files

| Content type | Folder | Example file |
|--------------|--------|--------------|
| Component product photo | `assets/visuals/components/photos/` | `dht22-photo.webp` |
| Component pinout | `assets/visuals/components/pinouts/` | `dht22-pinout.svg` |
| Component illustration | `assets/visuals/components/illustrations/` | `dht22-illustration.svg` |
| Guide wiring diagram | `assets/visuals/guides/wiring/` | `blink-led-esp32-wiring.svg` |
| Guide concept diagram | `assets/visuals/guides/concepts/` | `blink-led-esp32-concept.svg` |
| Guide expected output | `assets/visuals/guides/outputs/` | `blink-led-esp32-output.webp` |
| Project hero art | `assets/visuals/projects/heroes/` | `esp32-iot-weather-station-hero.webp` |
| Project wiring | `assets/visuals/projects/wiring/` | `esp32-iot-weather-station-wiring.svg` |
| Project output photo | `assets/visuals/projects/outputs/` | `esp32-iot-weather-station-output.webp` |
| Category icons | `assets/visuals/icons/categories/` | `category-iot-projects.svg` |
| Badge icons | `assets/visuals/icons/badges/` | `badge-parent-safe.svg` |
| Mascot | `assets/visuals/mascot/` | `mascot-waving.svg` |

Use **lowercase hyphens** and match the content **slug** in filenames.

### How YAML references images

Paths are always **site-root absolute** (start with `/assets/visuals/`).

**Component — hero photo (live today):**

```yaml
image: /assets/visuals/components/photos/dht22-photo.webp
image_alt: DHT22 temperature and humidity sensor module, three pins labeled
```

**Component — pinout & wiring (add when art exists):**

```yaml
pinout:
  image: /assets/visuals/components/pinouts/dht22-pinout.svg
  alt: DHT22 pinout — pin 1 VCC, pin 2 DATA, pin 3 GND

wiring:
  illustration_alt: DHT22 module — VCC to 3.3 V, GND to GND, DATA to GPIO4
  image: /assets/visuals/components/illustrations/dht22-wiring.svg
```

**Guide mission — wiring, concept, output:**

```yaml
mission:
  concept:
    illustration_alt: ESP32 GPIO through resistor to LED anode, cathode to ground
    image: /assets/visuals/guides/concepts/blink-led-esp32-concept.svg
  wiring:
    illustration_alt: ESP32 GPIO2 to resistor to LED anode, cathode to GND
    image: /assets/visuals/guides/wiring/blink-led-esp32-wiring.svg
  expected_output: Serial Monitor or LED behavior description
  output_image: /assets/visuals/guides/outputs/blink-led-esp32-output.webp
  output_image_alt: LED blinking on a breadboard next to ESP32 DevKit
```

**Golden project:**

```yaml
project:
  hero_image: /assets/visuals/projects/heroes/esp32-iot-weather-station-hero.webp
  hero_image_alt: Mini weather station with ESP32 and DHT22 on a breadboard
  wiring:
    illustration_alt: DHT22 VCC, GND, and DATA connected to ESP32
    image: /assets/visuals/projects/wiring/esp32-iot-weather-station-wiring.svg
  output_image: /assets/visuals/projects/outputs/esp32-iot-weather-station-output.webp
  output_image_alt: Serial Monitor showing temperature and humidity readings
```

### Placeholders (no file yet)

- Always fill **`illustration_alt`** (or `image_alt`) so placeholders are accessible.
- **Do not** point YAML at a missing file path.
- When templates show a gray diagram frame, that means art is planned — add the file, then set `image:`.

### Replacing temporary CDN URLs

Some components still use `https://cdn…` photos. To migrate:

1. Add WebP/PNG under `assets/visuals/components/photos/`
2. Change `image:` to `/assets/visuals/…`
3. Add `image_alt:`
4. Run `py tools/build_all.py` and verify the component page
5. Commit asset + YAML together

### After adding or changing assets

```
py tools/build_all.py
git add assets/visuals/ content/
git commit -m "Add DHT22 wiring diagram asset"
git push origin main
```

---

## Where to get help

| Question | Look here |
|----------|-----------|
| What goes where? | `content/manifest.yaml` |
| Full file inventory? | `docs/CONTENT_INVENTORY.md` |
| Architecture details? | `docs/DEVELOPER_ARCHITECTURE.md` |
| Build failed? | Error output from `py tools/build_all.py` |
| Example mission guide? | `content/guides/blink-led-esp32.yaml` |
| Example component? | `content/components/dht22.yaml` |
| Example project? | `content/projects/esp32-iot-weather-station.yaml` |
| Visual asset rules? | `assets/visuals/README.md` |
