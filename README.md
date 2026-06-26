# ESP32 Engine

The world's friendliest ESP32 learning platform — static-first, no server required at runtime.

**Live site:** [esp32engine.com](https://esp32engine.com)

---

## Quick start

**Edit content** in `content/`, then rebuild:

```bash
py tools/build_all.py
```

Push to `main` and GitHub Actions rebuilds + deploys automatically.

**First time on this machine:**

```bash
pip install -r requirements.txt
py tools/build_all.py
```

---

## Documentation

| Guide | For |
|-------|-----|
| [docs/CONTENT_EDITOR_GUIDE.md](docs/CONTENT_EDITOR_GUIDE.md) | Adding guides, components, projects — no coding needed |
| [docs/DEVELOPER_ARCHITECTURE.md](docs/DEVELOPER_ARCHITECTURE.md) | Build pipeline, static architecture, Phase 2 path |
| [content/manifest.yaml](content/manifest.yaml) | Content folder map |
| [static.config.yaml](static.config.yaml) | Phase 1 static-first config |

---

## Architecture (Phase 1)

- **Content:** YAML files in `content/` (version-controlled)
- **Build:** Python scripts in `tools/` (run locally or in CI)
- **Deploy:** Static HTML + JSON on GitHub Pages
- **Search:** Client-side via `search-index.json`
- **No:** database, auth, admin panel, or runtime server

---

## Coming back after a break?

1. Edit YAML in `content/`
2. Run `py tools/build_all.py`
3. Push to `main`

See [docs/CONTENT_EDITOR_GUIDE.md](docs/CONTENT_EDITOR_GUIDE.md) for step-by-step instructions.
