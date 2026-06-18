from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PROJECTS_DIR = CONTENT / "projects"
PAGES_DIR = CONTENT / "pages"
GUIDES_DIR = CONTENT / "guides"

DEFAULT_SITE = {
    "site_name": "ESP32 Engine",
    "org_name": "ESP32 Engine",
    "site_domain": "https://esp32engine.com",
    "github_url": "https://github.com/abdulmubeen7876773-dotcom/esp32",
    "contact_issues_url": "https://github.com/abdulmubeen7876773-dotcom/esp32/issues",
    "ga4_measurement_id": "G-WLHZKSEFP3",
    "gsc_verification": "Els4sebtkOekRXaW0BMxMlzn9iBdaqDHmuUCmMvfkCI",
    "pinterest_verification": "f71bc8cce0ff2c76eeea8b5cf86dc70b",
    "indexnow_key": "esp32engineindex20260618",
    "css_version": "20260615-premium1",
    "site_tagline": "Learn | Build | Innovate",
    "youtube_url": "https://www.youtube.com/@ESP32Engine",
    "projects_page_size": 50,
    "og_image_width": 1200,
    "og_image_height": 630,
}


def load_yaml(path: Path) -> dict | list:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100)


def load_site_settings() -> dict:
    data = load_yaml(CONTENT / "site.yaml")
    if not isinstance(data, dict):
        data = {}
    merged = dict(DEFAULT_SITE)
    merged.update(data)
    return merged


def load_categories() -> dict[str, str]:
    data = load_yaml(CONTENT / "categories.yaml")
    if isinstance(data, dict) and "categories" in data:
        items = data["categories"]
    elif isinstance(data, list):
        items = data
    else:
        items = []
    out = {}
    for item in items:
        if isinstance(item, dict) and item.get("name"):
            out[item["name"]] = item.get("intro", "")
    return out


def load_projects() -> list[dict]:
    if not PROJECTS_DIR.exists():
        return []
    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        data.setdefault("slug", path.stem)
        projects.append(data)
    return projects


def load_pages() -> dict[str, dict]:
    pages = {}
    if not PAGES_DIR.exists():
        return pages
    for path in sorted(PAGES_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if isinstance(data, dict):
            slug = data.get("slug") or path.stem
            pages[slug] = data
    return pages


def load_home() -> dict:
    data = load_yaml(CONTENT / "home.yaml")
    return data if isinstance(data, dict) else {}


def load_guides() -> list[dict]:
    if not GUIDES_DIR.exists():
        return []
    guides = []
    for path in sorted(GUIDES_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        data.setdefault("slug", path.stem)
        guides.append(data)
    return guides
