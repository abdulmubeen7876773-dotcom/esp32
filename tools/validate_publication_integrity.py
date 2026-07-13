from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from cms_loader import load_projects  # noqa: E402
from project_text import is_golden_project, primary_difficulty, project_title  # noqa: E402


PUBLIC_FILES = [
    ROOT / "index.html",
    ROOT / "projects.html",
    ROOT / "projects.json",
    ROOT / "search-index.json",
    ROOT / "sitemap.xml",
    ROOT / "sitemap.html",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    projects = load_projects()
    public = [p for p in projects if is_golden_project(p)]
    staged = [p for p in projects if not is_golden_project(p)]
    public_slugs = {p["slug"] for p in public}
    staged_slugs = {p["slug"] for p in staged}
    errors: list[str] = []

    for project in public:
        diff = primary_difficulty(project)
        if diff not in {"Beginner", "Intermediate", "Advanced"}:
            errors.append(f"content/projects/{project['slug']}.yaml: invalid difficulty {diff!r}")

    for slug in staged_slugs:
        staged_page = ROOT / "projects" / f"{slug}.html"
        if staged_page.exists():
            errors.append(f"{staged_page.relative_to(ROOT)}: staged project page is generated")

    scan_files = PUBLIC_FILES + list((ROOT / "category").glob("*.html"))
    for path in scan_files:
        text = read(path)
        if not text:
            continue
        for slug in staged_slugs:
            if slug in text:
                errors.append(f"{path.relative_to(ROOT)}: staged project slug leaked: {slug}")

    search_path = ROOT / "search-index.json"
    if search_path.exists():
        index = json.loads(read(search_path))
        project_items = [item for item in index if item.get("type") == "Project"]
        indexed_slugs = {item.get("slug") for item in project_items}
        if indexed_slugs != public_slugs:
            errors.append(
                "search-index.json: project set mismatch "
                f"(expected {len(public_slugs)}, found {len(indexed_slugs)})"
            )
        for item in project_items:
            if item.get("slug") == "esp32-voice-controlled-relay":
                title = item.get("title", "")
                if title != "ESP32 Sound-Triggered Relay Demo":
                    errors.append(f"search-index.json: outdated voice relay title {title!r}")

    projects_json = ROOT / "projects.json"
    if projects_json.exists():
        rows = json.loads(read(projects_json))
        if len(rows) != len(public):
            errors.append(f"projects.json: expected {len(public)} public projects, found {len(rows)}")
        for row in rows:
            levels = row.get("levels") or []
            if len(levels) != 1:
                errors.append(f"projects.json: {row.get('slug')} has unsupported level list {levels!r}")

    sitemap = read(ROOT / "sitemap.xml")
    for bad in ("google", "pinterest", "search?q=", "esp32-tinyml-sound-classifier"):
        if bad in sitemap.lower():
            errors.append(f"sitemap.xml: invalid public entry contains {bad!r}")

    human = read(ROOT / "sitemap.html").lower()
    for bad in ("href=\"/google", "href=\"google", "href=\"/pinterest", "href=\"pinterest"):
        if bad in human:
            errors.append(f"sitemap.html: verification file leaked: {bad}")

    projects_html = read(ROOT / "projects.html")
    for bad in ("3 Levels Each", "Beginner, Intermediate, and Advanced stages", "3 levels"):
        if bad in projects_html:
            errors.append(f"projects.html: unsupported multi-level claim {bad!r}")
    if "ESP32 Project Library" in projects_html and '<li><a href="/">Home</a></li><li aria-current="page">Projects</li>' not in projects_html:
        errors.append("projects.html: project library breadcrumb is not Home > Projects")

    generated_voice = read(ROOT / "projects" / "esp32-voice-controlled-relay.html").lower()
    for bad in ("google assistant", "wake-word recognition", "voice recognition"):
        if bad in generated_voice:
            errors.append(f"projects/esp32-voice-controlled-relay.html: unsupported claim {bad!r}")

    generated_energy = read(ROOT / "projects" / "esp32-smart-energy-meter.html").lower()
    for bad in ("production-ready", "deploy today"):
        if bad in generated_energy:
            errors.append(f"projects/esp32-smart-energy-meter.html: misleading claim {bad!r}")
    if "billing grade" in generated_energy and "not billing grade" not in generated_energy:
        errors.append("projects/esp32-smart-energy-meter.html: unsupported billing-grade claim")
    if "billing-grade" in generated_energy and "not billing-grade" not in generated_energy:
        errors.append("projects/esp32-smart-energy-meter.html: unsupported billing-grade claim")
    if "not for direct mains" not in generated_energy and "not direct mains" not in generated_energy:
        errors.append("projects/esp32-smart-energy-meter.html: missing direct mains limitation")

    if errors:
        print("Publication integrity validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(
        "Publication integrity validation passed: "
        f"{len(public)} public projects, {len(staged)} staged projects."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
