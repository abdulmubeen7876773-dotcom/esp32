import json
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_components, load_guides, load_projects, load_yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REPORTS_DIR = ROOT / "docs" / "reports"


def _load_roadmap(name: str) -> dict:
    path = CONTENT / name
    if not path.exists():
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _is_mission(guide: dict) -> bool:
    return guide.get("format") == "mission" or bool(guide.get("mission"))


def _local_asset_exists(url: str) -> bool:
    if not url or not url.startswith("/"):
        return False
    return (ROOT / url.lstrip("/")).is_file()


def _local_visual_photo(url: str) -> bool:
    return url.startswith("/assets/visuals/") and _local_asset_exists(url)



def _count_complete_missing(expected: list[str], complete_flags: list[bool]) -> dict:
    missing = [label for label, ok in zip(expected, complete_flags) if not ok]
    complete = len(expected) - len(missing)
    return {
        "complete": complete,
        "missing": len(missing),
        "items_missing": missing,
    }


def build_content_dashboard() -> dict:
    guide_roadmap = _load_roadmap("guide-roadmap.yaml")
    component_roadmap = _load_roadmap("component-roadmap.yaml")
    guides = load_guides()
    components = load_components()
    projects = load_projects()

    mission_count = sum(1 for guide in guides if _is_mission(guide))

    illustration_expected: list[str] = []
    illustration_complete: list[bool] = []
    wiring_expected: list[str] = []
    wiring_complete: list[bool] = []

    for guide in guides:
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        mission = guide.get("mission") or {}
        concept = mission.get("concept") or {}
        wiring = mission.get("wiring") or {}

        if isinstance(concept, dict) and (concept.get("illustration_alt") or concept.get("image")):
            illustration_expected.append(f"guides/{slug}: concept")
            image = str(concept.get("image") or "")
            illustration_complete.append(_local_asset_exists(image))

        if isinstance(wiring, dict) and wiring.get("steps"):
            wiring_expected.append(f"guides/{slug}: wiring diagram")
            image = str(wiring.get("image") or "")
            wiring_complete.append(_local_asset_exists(image))

    photo_expected: list[str] = []
    photo_complete: list[bool] = []
    pinout_expected: list[str] = []
    pinout_complete: list[bool] = []

    for comp in components:
        slug = comp.get("slug", "?")
        photo_expected.append(f"components/{slug}: photo")
        image = str(comp.get("image") or "")
        photo_complete.append(_local_visual_photo(image))

        pinout_expected.append(f"components/{slug}: pinout")
        pinout = comp.get("pinout")
        pinout_complete.append(bool(pinout))

        wiring = comp.get("wiring") or {}
        if isinstance(wiring, dict) and (wiring.get("steps") or wiring.get("summary")):
            wiring_expected.append(f"components/{slug}: wiring diagram")
            image = str(wiring.get("image") or "")
            wiring_complete.append(_local_asset_exists(image))

    components_complete = len(components)
    components_planned = int(component_roadmap.get("target_total") or components_complete)
    guides_complete = int(guide_roadmap.get("complete_count") or len(guides))
    guides_planned = int(guide_roadmap.get("target_total") or guides_complete)
    projects_complete = len(projects)
    projects_planned = projects_complete

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "components": {
            "complete": components_complete,
            "planned": components_planned,
        },
        "guides": {
            "complete": guides_complete,
            "planned": guides_planned,
        },
        "projects": {
            "complete": projects_complete,
            "planned": projects_planned,
        },
        "mission_count": mission_count,
        "illustrations": _count_complete_missing(illustration_expected, illustration_complete),
        "photos": _count_complete_missing(photo_expected, photo_complete),
        "pinouts": _count_complete_missing(pinout_expected, pinout_complete),
        "wiring": _count_complete_missing(wiring_expected, wiring_complete),
    }


def write_content_dashboard_md(dashboard: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def asset_section(title: str, key: str) -> list[str]:
        block = dashboard[key]
        lines = [
            f"## {title}",
            "",
            f"- Complete: {block['complete']}",
            f"- Missing: {block['missing']}",
            "",
        ]
        if block["items_missing"]:
            lines.append("Missing items:")
            lines.append("")
            lines.extend(f"- {item}" for item in block["items_missing"])
            lines.append("")
        return lines

    lines = [
        "# Content Dashboard",
        "",
        f"Generated: {dashboard['generated_at']}",
        "",
        "## Components",
        "",
        f"- Complete: {dashboard['components']['complete']}",
        f"- Planned: {dashboard['components']['planned']}",
        "",
        "## Guides",
        "",
        f"- Complete: {dashboard['guides']['complete']}",
        f"- Planned: {dashboard['guides']['planned']}",
        "",
        "## Projects",
        "",
        f"- Complete: {dashboard['projects']['complete']}",
        f"- Planned: {dashboard['projects']['planned']}",
        "",
        "## Mission Count",
        "",
        str(dashboard["mission_count"]),
        "",
    ]
    lines.extend(asset_section("Illustrations", "illustrations"))
    lines.extend(asset_section("Photos", "photos"))
    lines.extend(asset_section("Pinouts", "pinouts"))
    lines.extend(asset_section("Wiring", "wiring"))
    (REPORTS_DIR / "content-dashboard.md").write_text("\n".join(lines), encoding="utf-8")


def generate_content_dashboard() -> dict:
    dashboard = build_content_dashboard()
    (ROOT / "content-dashboard.json").write_text(
        json.dumps(dashboard, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_content_dashboard_md(dashboard)
    print("\n=== content_dashboard.py ===")
    print("Wrote content-dashboard.json")
    print("Wrote docs/reports/content-dashboard.md")
    return dashboard
