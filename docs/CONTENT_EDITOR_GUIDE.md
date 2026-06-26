# ESP32 Engine — Content Editor Guide

**Read this when you come back after a break.** You do not need to remember how the site works — just follow the steps below.

---

## The one rule

**Only edit files inside `content/`.**  
Everything else is built automatically.

---

## Quick checklist (every time you publish)

1. Edit or add a YAML file in `content/`
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

### Reference guide (long article format)

1. Copy `content/guides/what-is-esp32.yaml`
2. Remove `format: mission` and the `mission:` block
3. Write content in `body_html:` using HTML tags (`<h2>`, `<p>`, `<ul>`, etc.)
4. Rebuild

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

**Categories list:** see `content/component-categories.yaml` if you need to add a new category.

---

## 3. How to add a new project

Projects live in **`content/projects/`**.

1. Copy `content/projects/esp32-iot-weather-station.yaml`
2. Save as `content/projects/esp32-your-project.yaml`
3. Update at minimum:

   | Field | Example |
   |-------|---------|
   | `slug` | `esp32-your-project` |
   | `title` | `ESP32 Your Project` |
   | `category` | IoT Projects, Robotics, Agriculture, etc. |
   | `description` | One paragraph summary |
   | `sensor` | Main sensor used |
   | `output` | Main output (relay, OLED, etc.) |
   | `source_base` | Same as slug or legacy base name |
   | `featured` | `true` or `false` |

4. Run `py tools/build_all.py`
5. Page appears at: `/projects/esp32-your-project.html`

**Note:** The build generates Beginner, Intermediate, and Advanced stages automatically from project metadata.

---

## 4. How to update the search index

**You do not edit the search index by hand.**

Search reads from **`search-index.json`**, which is rebuilt from all content files every time you run:

```
py tools/build_all.py
```

When you add or edit a guide, component, project, or page in `content/`, the search index updates automatically.

To verify: open `search-index.json` after building and search for your new title.

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
2. Generates all HTML pages
3. Updates `search-index.json`, `projects.json`, `sitemap.xml`, `feed.xml`
4. Prints `Build complete` when done

**If build fails:** read the error message — it usually names the file and field that needs fixing.

---

## 6. What files should NEVER be hand-edited

These are **generated**. Your edits will be overwritten on the next build.

| Do not edit | Why |
|-------------|-----|
| `*.html` (root and subfolders) | Built from `content/` |
| `guides/*.html` | Built from `content/guides/` |
| `components/*.html` | Built from `content/components/` |
| `projects/*.html` | Built from `content/projects/` |
| `category/*.html` | Built automatically |
| `search-index.json` | Built from all content |
| `projects.json` | Built from projects |
| `project-icons.js` | Built automatically |
| `sitemap.xml` | Built automatically |
| `feed.xml` | Built automatically |

### Safe to edit

| Folder / file | Purpose |
|---------------|---------|
| `content/**` | **All site content** |
| `style.css` | Visual design |
| `ui.js`, `search.js`, `mission-guide.js` | Client behavior |
| `static.config.yaml` | Architecture settings |
| `tools/` | Build scripts (developers only) |

---

## 7. How to deploy to GitHub Pages

### First-time setup (once)

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Source: **Deploy from branch**
4. Branch: **`main`** / **root**
5. Custom domain: `esp32engine.com` (CNAME file is already in the repo)

### Every publish after that

```
git add content/
git commit -m "Add new guide: my-mission"
git push origin main
```

GitHub Actions (`.github/workflows/build-site.yml`) will:
- Validate content
- Run `py tools/build_all.py`
- Commit generated HTML/JSON
- GitHub Pages serves the updated site

**You can also build locally first** to preview, then push both `content/` and generated files.

---

## 8. Coming back after 10+ days

Forget everything? Just do this:

1. Open `content/` — find the folder for what you want to change
2. Copy the nearest existing YAML file
3. Edit text fields
4. Run:
   ```
   py tools/build_all.py
   ```
5. Push to `main`

The live site keeps running while you are away. No server to restart. No database to maintain.

---

## Where to get help

| Question | Look here |
|----------|-----------|
| What goes where? | `content/manifest.yaml` |
| Architecture details? | `docs/DEVELOPER_ARCHITECTURE.md` |
| Build failed? | Error output from `py tools/build_all.py` |
| Example mission guide? | `content/guides/blink-led-esp32.yaml` |
| Example component? | `content/components/dht22.yaml` |
| Example project? | `content/projects/esp32-iot-weather-station.yaml` |
