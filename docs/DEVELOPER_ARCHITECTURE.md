# ESP32 Engine — Developer Architecture

Phase 1 is **static-first**: version-controlled YAML → Python build → static HTML/JSON → GitHub Pages. No runtime server.

---

## System overview

```
┌─────────────────────────────────────────────────────────┐
│  content/          Source of truth (YAML, git)          │
│    guides/ components/ projects/ pages/ site.yaml      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼  py tools/build_all.py
                           │  (local or GitHub Actions)
┌──────────────────────────┴──────────────────────────────┐
│  Generated artifacts (deploy to GitHub Pages)           │
│    *.html  search-index.json  projects.json  sitemap.xml │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼  browser only
┌──────────────────────────┴──────────────────────────────┐
│  Client runtime (no server)                             │
│    ui.js  search.js  mission-guide.js  projects.js      │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration files

| File | Role |
|------|------|
| `static.config.yaml` | Phase 1 contract — files backend, no auth/DB/API |
| `content/manifest.yaml` | Content directory map and edit rules |
| `content/site.yaml` | Domain, analytics, CSS cache version |

---

## Content layer

**Loader:** `tools/cms_loader.py` — reads YAML from disk  
**Store:** `tools/content_store.py` — public interface for all build scripts  
**Validation:** `tools/validate_content.py` — runs before every build

```python
from content_store import get_content_store

store = get_content_store()
store.guides()       # list[dict]
store.components()   # list[dict]
store.projects()     # list[dict]
store.pages()        # dict[str, dict]
store.site_settings()
```

All build scripts use `get_content_store()` — not direct file reads.

---

## Build pipeline

Entry point: **`tools/build_all.py`**

| Step | Script | Output |
|------|--------|--------|
| 1 | `validate_content.py` | Pass/fail on YAML |
| 2 | `rebuild_parents.py` | `projects/*.html` |
| 3 | `build_static_pages.py` | `about.html`, `learning.html`, etc. |
| 4 | `build_guides.py` | `guides/*.html`, `guides.html` |
| 5 | `build_components.py` | `components/*.html`, `components.html` |
| 6 | `build_search_index.py` | `search-index.json`, `search.html` |
| 7 | `rebuild_index.py` | `index.html`, `projects.html`, `projects.json` |

`rebuild_index.py` also triggers `build_categories.py`, `build_feed.py`, `build_sitemap.py`.

---

## Template layer (unchanged in Phase 2)

| Module | Purpose |
|--------|---------|
| `tools/site_layout.py` | Header, footer, head/meta, cards, homepage sections |
| `tools/guide_mission.py` | Mission journey guide template (14 sections) |
| `tools/build_guides.py` | Routes mission vs legacy guide formats |

HTML structure and CSS classes live here. **Do not duplicate in content YAML.**

---

## Search architecture

- **Build time:** `build_search_index.py` aggregates guides, components, projects, pages into `search-index.json`
- **Runtime:** `search.js` fetches `/search-index.json` and filters in the browser
- **No server query** — fully client-side

Adding content to `content/` and rebuilding automatically updates search.

---

## Guide formats

| Format | Flag | Template |
|--------|------|----------|
| Mission journey | `format: mission` + `mission:` block | `guide_mission.py` |
| Legacy article | `body_html:` only | `build_guides.py` → `render_legacy_guide()` |

Mission sections: card, story, eli12, build, parts, safety, concept, wiring, code, output, quiz, challenge, complete, next missions.

---

## Generated vs source

**Never commit hand-edits to generated files** — they are overwritten every build.

Generated (see `static.config.yaml` → `generated_artifacts`):
- All `*.html` except none are hand-maintained
- `search-index.json`, `projects.json`, `project-icons.js`
- `sitemap.xml`, `feed.xml`

Source:
- `content/**`
- `style.css`, client JS in repo root
- `tools/**`

---

## CI / deploy

**Workflow:** `.github/workflows/build-site.yml`

Triggers on push to `main` when `content/`, `tools/`, or client assets change.

```
pip install -r requirements.txt
python tools/build_all.py
git auto-commit generated artifacts
```

**Hosting:** GitHub Pages from repo root  
**Domain:** `CNAME` → `esp32engine.com`

---

## Phase 1 exclusions (by design)

These are **not** in Phase 1:

- Backend API
- Database
- Authentication
- Admin panel (Decap CMS removed)
- Server-side rendering at request time

Python is a **build tool only** — not a runtime dependency on the live site.

---

## Phase 2: adding a backend without rewriting

The site is designed so Phase 2 swaps the **data source**, not the **templates**.

### What stays the same

- `tools/site_layout.py`
- `tools/guide_mission.py`
- `tools/build_guides.py` (or a thin SSR/API consumer)
- All HTML/CSS/JS in the deployed bundle
- URL structure (`/guides/`, `/components/`, etc.)

### What changes

1. Set in `static.config.yaml`:
   ```yaml
   phase: 2
   content:
     backend: api
   ```

2. Implement `tools/content_api.py`:
   ```python
   class ApiContentStore:
       def guides(self) -> list[dict]: ...
       def components(self) -> list[dict]: ...
       # same methods as FileContentStore
   ```

3. Update `get_content_store()` in `content_store.py` to return `ApiContentStore` when `backend: api`.

4. Build can either:
   - **Option A:** Keep static generation — CI pulls from API, writes same HTML/JSON (minimal live-site change)
   - **Option B:** Add ISR/SSR later — templates already produce consistent HTML shapes

### Data contract

YAML files in `content/` define the schema. Phase 2 API responses should match the same dict shapes `cms_loader` returns today. That keeps templates and search index builder working unchanged.

---

## Dependencies

**Build only:**
```
PyYAML>=6.0
```

**Runtime (CDN/static):**
- Google Fonts (Inter, Poppins, JetBrains Mono)
- No npm build step in Phase 1

---

## Local development

```bash
pip install -r requirements.txt
py tools/build_all.py
```

Open `index.html` via a local static server (or push to a preview branch on GitHub Pages).

Validate content only:
```bash
py tools/validate_content.py
```

---

## Key paths (quick reference)

```
content/guides/*.yaml          → guides/*.html
content/components/*.yaml      → components/*.html
content/projects/*.yaml        → projects/*.html
content/pages/*.yaml           → *.html (root)
content/site.yaml              → global settings in all pages
tools/content_store.py         → data access abstraction
tools/build_all.py             → single build command
static.config.yaml             → phase and architecture config
search-index.json              → generated search data
```
