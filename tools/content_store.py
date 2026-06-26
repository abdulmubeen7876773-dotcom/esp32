from pathlib import Path

import yaml

from cms_loader import (
    COMPONENTS_DIR,
    CONTENT,
    DEFAULT_SITE,
    GUIDES_DIR,
    PAGES_DIR,
    PROJECTS_DIR,
    load_component_categories,
    load_components,
    load_guides,
    load_home,
    load_learning_paths,
    load_pages,
    load_projects,
    load_site_settings,
    load_yaml,
)

ROOT = Path(__file__).resolve().parent.parent
STATIC_CONFIG_PATH = ROOT / "static.config.yaml"
MANIFEST_PATH = CONTENT / "manifest.yaml"

GENERATED_JSON = ("search-index.json", "projects.json")
GENERATED_JS = ("project-icons.js",)
GENERATED_XML = ("sitemap.xml", "feed.xml")


def load_static_config() -> dict:
    if not STATIC_CONFIG_PATH.exists():
        return {"phase": 1, "runtime": "static", "content": {"backend": "files"}}
    data = load_yaml(STATIC_CONFIG_PATH)
    return data if isinstance(data, dict) else {}


def load_manifest() -> dict:
    data = load_yaml(MANIFEST_PATH)
    return data if isinstance(data, dict) else {}


def assert_phase1_static() -> None:
    cfg = load_static_config()
    if cfg.get("phase") != 1:
        return
    backend = (cfg.get("content") or {}).get("backend", "files")
    if backend != "files":
        raise SystemExit(
            "Phase 1 requires content.backend=files in static.config.yaml. "
            "API backend is Phase 2+."
        )


class FileContentStore:
    def site_settings(self) -> dict:
        return load_site_settings()

    def home(self) -> dict:
        return load_home()

    def guides(self) -> list[dict]:
        return load_guides()

    def components(self) -> list[dict]:
        return load_components()

    def projects(self) -> list[dict]:
        return load_projects()

    def pages(self) -> dict[str, dict]:
        return load_pages()

    def learning_paths(self) -> list[dict]:
        return load_learning_paths()

    def component_categories(self) -> list[str]:
        return load_component_categories()


_store: FileContentStore | None = None


def get_content_store() -> FileContentStore:
    global _store
    cfg = load_static_config()
    backend = (cfg.get("content") or {}).get("backend", "files")
    if backend != "files":
        raise NotImplementedError(
            f"Content backend '{backend}' is not implemented. Phase 1 uses files only."
        )
    if _store is None:
        _store = FileContentStore()
    return _store


def content_inventory() -> dict:
    store = get_content_store()
    return {
        "guides": len(store.guides()),
        "components": len(store.components()),
        "projects": len(store.projects()),
        "pages": len(store.pages()),
        "learning_paths": len(store.learning_paths()),
    }


def validate_content() -> list[str]:
    errors: list[str] = []
    store = get_content_store()

    for guide in store.guides():
        slug = guide.get("slug", "?")
        if not guide.get("title"):
            errors.append(f"guides/{slug}: missing title")
        if not guide.get("meta_description"):
            errors.append(f"guides/{slug}: missing meta_description")
        if guide.get("format") == "mission" or guide.get("mission"):
            if not guide.get("mission"):
                errors.append(f"guides/{slug}: mission format but no mission block")

    for comp in store.components():
        slug = comp.get("slug", "?")
        if not comp.get("name"):
            errors.append(f"components/{slug}: missing name")
        if not comp.get("summary"):
            errors.append(f"components/{slug}: missing summary")
        if not comp.get("slug"):
            errors.append(f"components/{slug}: missing slug")

    for proj in store.projects():
        slug = proj.get("slug", "?")
        if not proj.get("title"):
            errors.append(f"projects/{slug}: missing title")
        if not proj.get("category"):
            errors.append(f"projects/{slug}: missing category")
        if not proj.get("description"):
            errors.append(f"projects/{slug}: missing description")
        if not proj.get("source_base"):
            errors.append(f"projects/{slug}: missing source_base")

    for slug, page in store.pages().items():
        if not page.get("meta_description"):
            errors.append(f"pages/{slug}: missing meta_description")

    if not store.site_settings().get("site_domain"):
        errors.append("content/site.yaml: missing site_domain")

    return errors
