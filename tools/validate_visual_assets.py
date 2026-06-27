import json
import re
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_components, load_guides, load_projects, load_yaml

ROOT = Path(__file__).resolve().parent.parent
VISUALS_ROOT = ROOT / "assets" / "visuals"
MANIFEST_PATH = VISUALS_ROOT / "manifest.json"
REPORT_PATH = ROOT / "docs" / "reports" / "visual-assets-report.md"

VALID_EXTENSIONS = {".svg", ".webp", ".png", ".jpg", ".jpeg"}
SKIP_FILENAMES = {"manifest.json", "README.md", ".gitkeep"}
SKIP_SUFFIXES = {".md"}

PRODUCTION_DIRS = (
    VISUALS_ROOT / "components" / "photos",
    VISUALS_ROOT / "components" / "illustrations",
    VISUALS_ROOT / "components" / "wiring",
    VISUALS_ROOT / "guides" / "wiring",
    VISUALS_ROOT / "guides" / "concepts",
    VISUALS_ROOT / "guides" / "outputs",
    VISUALS_ROOT / "projects" / "wiring",
    VISUALS_ROOT / "projects" / "heroes",
    VISUALS_ROOT / "projects" / "outputs",
    VISUALS_ROOT / "icons" / "categories",
    VISUALS_ROOT / "icons" / "badges",
)


def _text(value) -> str:
    return str(value or "").strip()


def _is_mission(guide: dict) -> bool:
    return guide.get("format") == "mission" or bool(guide.get("mission"))


def _is_golden_project(project: dict) -> bool:
    return project.get("format") == "golden" or bool(project.get("project"))


def _category_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "unknown"


def _local_path(url: str) -> Path | None:
    if not url or not url.startswith("/"):
        return None
    return ROOT / url.lstrip("/")


def _file_exists(url: str) -> bool:
    path = _local_path(url)
    return bool(path and path.is_file())


def _filename_from_url(url: str) -> str:
    if not url:
        return ""
    if url.startswith("http"):
        return Path(url.split("?", 1)[0]).name or "external"
    return Path(url).name


def _valid_format(path: str) -> bool:
    if path.startswith("http"):
        return True
    ext = Path(path).suffix.lower()
    return ext in VALID_EXTENSIONS


def _make_entry(
    *,
    asset_id: str,
    asset_type: str,
    related_page: str,
    related_slug: str,
    alt_text: str,
    path: str,
    source: str,
    status: str,
) -> dict:
    filename = _filename_from_url(path) if path else ""
    if not filename and path:
        filename = Path(path).name
    if not filename:
        filename = asset_id.split(":")[-1]
    return {
        "id": asset_id,
        "filename": filename,
        "path": path or "",
        "type": asset_type,
        "related_page": related_page,
        "related_slug": related_slug,
        "alt_text": alt_text,
        "status": status,
        "source": source,
    }


def _resolve_status(path: str, alt_text: str, *, explicit_reference: bool = False) -> str:
    if path.startswith("http"):
        return "placeholder"
    if path.startswith("/assets/visuals/"):
        if _file_exists(path):
            return "complete"
        if explicit_reference:
            return "missing"
        return "placeholder"
    if alt_text:
        return "placeholder"
    return "missing"


def ensure_production_folders() -> None:
    for folder in PRODUCTION_DIRS:
        folder.mkdir(parents=True, exist_ok=True)
        keep = folder / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")


def _add_entry(entries: dict[str, dict], entry: dict) -> None:
    entries[entry["id"]] = entry


def collect_content_assets() -> dict[str, dict]:
    entries: dict[str, dict] = {}

    for comp in load_components():
        slug = comp.get("slug", "?")
        source = f"content/components/{slug}.yaml"
        page = f"/components/{slug}.html"
        name = _text(comp.get("name")) or slug
        alt = _text(comp.get("image_alt")) or f"{name} component photo"
        image = _text(comp.get("image"))
        if image.startswith("/assets/visuals/"):
            photo_path = image
        elif image.startswith("http"):
            photo_path = f"/assets/visuals/components/photos/{slug}-photo.webp"
        else:
            photo_path = f"/assets/visuals/components/photos/{slug}-photo.webp"
        if image.startswith("http"):
            photo_status = "placeholder"
        else:
            photo_status = _resolve_status(
                photo_path, alt, explicit_reference=image.startswith("/assets/visuals/")
            )
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"components/{slug}:photo",
                asset_type="component_photo",
                related_page=page,
                related_slug=slug,
                alt_text=alt,
                path=photo_path if not image.startswith("http") else photo_path,
                source=source,
                status=photo_status,
            ),
        )

        wiring = comp.get("wiring") or {}
        if isinstance(wiring, dict) and (_text(wiring.get("illustration_alt")) or wiring.get("steps")):
            w_alt = _text(wiring.get("illustration_alt")) or f"Wiring diagram for {name}"
            w_path = _text(wiring.get("image")) or f"/assets/visuals/components/wiring/{slug}-wiring.svg"
            _add_entry(
                entries,
                _make_entry(
                    asset_id=f"components/{slug}:wiring",
                    asset_type="component_wiring",
                    related_page=page,
                    related_slug=slug,
                    alt_text=w_alt,
                    path=w_path,
                    source=source,
                    status=_resolve_status(
                        w_path, w_alt, explicit_reference=bool(_text(wiring.get("image")))
                    ),
                ),
            )

        if comp.get("pinout") or comp.get("pins"):
            p_alt = f"Pinout diagram for {name}"
            p_path = f"/assets/visuals/components/illustrations/{slug}-pinout.svg"
            _add_entry(
                entries,
                _make_entry(
                    asset_id=f"components/{slug}:pinout",
                    asset_type="component_pinout",
                    related_page=page,
                    related_slug=slug,
                    alt_text=p_alt,
                    path=p_path,
                    source=source,
                    status=_resolve_status(p_path, p_alt),
                ),
            )

        illustration_path = f"/assets/visuals/components/illustrations/{slug}-illustration.svg"
        illustration_alt = f"Simplified illustration of {name}"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"components/{slug}:illustration",
                asset_type="component_illustration",
                related_page=page,
                related_slug=slug,
                alt_text=illustration_alt,
                path=illustration_path,
                source=source,
                status=_resolve_status(illustration_path, illustration_alt),
            ),
        )

    for guide in load_guides():
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        source = f"content/guides/{slug}.yaml"
        page = f"/guides/{slug}.html"
        mission = guide.get("mission") or {}

        concept = mission.get("concept") or {}
        if isinstance(concept, dict) and _text(concept.get("illustration_alt")):
            c_alt = _text(concept.get("illustration_alt"))
            c_path = _text(concept.get("image")) or f"/assets/visuals/guides/concepts/{slug}-concept.svg"
            _add_entry(
                entries,
                _make_entry(
                    asset_id=f"guides/{slug}:concept",
                    asset_type="concept_illustration",
                    related_page=page,
                    related_slug=slug,
                    alt_text=c_alt,
                    path=c_path,
                    source=source,
                    status=_resolve_status(
                        c_path, c_alt, explicit_reference=bool(_text(concept.get("image")))
                    ),
                ),
            )

        wiring = mission.get("wiring") or {}
        if isinstance(wiring, dict) and (_text(wiring.get("illustration_alt")) or wiring.get("steps")):
            w_alt = _text(wiring.get("illustration_alt")) or f"Wiring diagram for {slug}"
            w_path = _text(wiring.get("image")) or f"/assets/visuals/guides/wiring/{slug}-wiring.svg"
            _add_entry(
                entries,
                _make_entry(
                    asset_id=f"guides/{slug}:wiring",
                    asset_type="wiring_diagram",
                    related_page=page,
                    related_slug=slug,
                    alt_text=w_alt,
                    path=w_path,
                    source=source,
                    status=_resolve_status(
                        w_path, w_alt, explicit_reference=bool(_text(wiring.get("image")))
                    ),
                ),
            )

        output_path = f"/assets/visuals/guides/outputs/{slug}-output.webp"
        output_alt = f"Expected output for {slug}"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"guides/{slug}:output",
                asset_type="guide_output",
                related_page=page,
                related_slug=slug,
                alt_text=output_alt,
                path=output_path,
                source=source,
                status=_resolve_status(output_path, output_alt),
            ),
        )

    for project in load_projects():
        slug = project.get("slug", "?")
        source = f"content/projects/{slug}.yaml"
        page = f"/projects/{slug}.html"
        if not _is_golden_project(project):
            continue
        proj = project.get("project") or {}
        title = _text(project.get("title")) or slug

        hero_path = f"/assets/visuals/projects/heroes/{slug}-hero.webp"
        hero_alt = f"Hero image for {title}"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"projects/{slug}:hero",
                asset_type="project_hero",
                related_page=page,
                related_slug=slug,
                alt_text=hero_alt,
                path=hero_path,
                source=source,
                status=_resolve_status(hero_path, hero_alt),
            ),
        )

        wiring = proj.get("wiring") or {}
        if isinstance(wiring, dict) and (_text(wiring.get("illustration_alt")) or wiring.get("steps")):
            w_alt = _text(wiring.get("illustration_alt")) or f"Wiring diagram for {title}"
            w_path = _text(wiring.get("image")) or f"/assets/visuals/projects/wiring/{slug}-wiring.svg"
            _add_entry(
                entries,
                _make_entry(
                    asset_id=f"projects/{slug}:wiring",
                    asset_type="project_wiring",
                    related_page=page,
                    related_slug=slug,
                    alt_text=w_alt,
                    path=w_path,
                    source=source,
                    status=_resolve_status(
                        w_path, w_alt, explicit_reference=bool(_text(wiring.get("image")))
                    ),
                ),
            )

        illustration_path = f"/assets/visuals/projects/{slug}-illustration.svg"
        illustration_alt = f"Project illustration for {title}"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"projects/{slug}:illustration",
                asset_type="project_illustration",
                related_page=page,
                related_slug=slug,
                alt_text=illustration_alt,
                path=illustration_path,
                source=source,
                status=_resolve_status(illustration_path, illustration_alt),
            ),
        )

        output_path = f"/assets/visuals/projects/outputs/{slug}-output.webp"
        output_alt = f"Finished build output for {title}"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"projects/{slug}:output",
                asset_type="project_output",
                related_page=page,
                related_slug=slug,
                alt_text=output_alt,
                path=output_path,
                source=source,
                status=_resolve_status(output_path, output_alt),
            ),
        )

    categories_data = load_yaml(ROOT / "content" / "categories.yaml")
    categories: list = []
    if isinstance(categories_data, dict):
        categories = categories_data.get("categories") or []
    elif isinstance(categories_data, list):
        categories = categories_data

    for item in categories:
        if not isinstance(item, dict):
            continue
        name = _text(item.get("name"))
        if not name:
            continue
        cat_slug = _category_slug(name)
        icon_path = f"/assets/visuals/icons/categories/category-{cat_slug}.svg"
        icon_alt = f"{name} category icon"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"icons/categories:{cat_slug}",
                asset_type="icon",
                related_page="/projects.html",
                related_slug=cat_slug,
                alt_text=icon_alt,
                path=icon_path,
                source="content/categories.yaml",
                status=_resolve_status(icon_path, icon_alt),
            ),
        )

    return entries


def collect_disk_assets(entries: dict[str, dict]) -> None:
    if not VISUALS_ROOT.exists():
        return
    known_paths = {_text(e.get("path")) for e in entries.values() if _text(e.get("path"))}
    for path in sorted(VISUALS_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_FILENAMES or path.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = "/" + path.relative_to(ROOT).as_posix()
        if rel in known_paths:
            continue
        asset_type = "icon" if "/icons/" in rel else "project_illustration"
        if "/components/photos/" in rel:
            asset_type = "component_photo"
        elif "/components/wiring/" in rel:
            asset_type = "component_wiring"
        elif "/components/illustrations/" in rel:
            asset_type = "component_illustration"
        elif "/guides/wiring/" in rel:
            asset_type = "wiring_diagram"
        elif "/guides/concepts/" in rel:
            asset_type = "concept_illustration"
        elif "/guides/outputs/" in rel:
            asset_type = "guide_output"
        elif "/projects/wiring/" in rel:
            asset_type = "project_wiring"
        elif "/projects/heroes/" in rel:
            asset_type = "project_hero"
        elif "/projects/outputs/" in rel:
            asset_type = "project_output"
        _add_entry(
            entries,
            _make_entry(
                asset_id=f"disk:{rel}",
                asset_type=asset_type,
                related_page="",
                related_slug="",
                alt_text="",
                path=rel,
                source="assets/visuals/",
                status="complete",
            ),
        )


def validate_assets(entries: dict[str, dict]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    path_counts: dict[str, list[str]] = {}
    filename_counts: dict[str, list[str]] = {}

    for entry in entries.values():
        asset_id = entry["id"]
        path = _text(entry.get("path"))
        status = entry.get("status")
        alt_text = _text(entry.get("alt_text"))

        if path:
            path_counts.setdefault(path, []).append(asset_id)
            filename_counts.setdefault(entry.get("filename", ""), []).append(asset_id)

        if status == "missing" and path.startswith("/assets/visuals/"):
            errors.append(f"Missing file: {path} ({asset_id})")

        if status == "placeholder" and not alt_text and entry.get("type") != "icon":
            warnings.append(f"Placeholder without alt text: {asset_id}")

        if path.startswith("/assets/visuals/") and not _valid_format(path):
            errors.append(f"Wrong format: {path} ({asset_id})")

        if path.startswith("/assets/visuals/") and status == "complete":
            disk_path = _local_path(path)
            if disk_path and disk_path.suffix.lower() not in VALID_EXTENSIONS:
                errors.append(f"Wrong format on disk: {path}")

    for path, ids in path_counts.items():
        if len(ids) > 1:
            warnings.append(f"Duplicate path reference {path}: {', '.join(ids)}")

    for filename, ids in filename_counts.items():
        if filename and len(ids) > 1:
            unique_paths = {entries[i]["path"] for i in ids if entries[i].get("path")}
            if len(unique_paths) > 1:
                warnings.append(f"Duplicate filename {filename} across paths: {', '.join(ids)}")

    broken_refs = [e for e in entries.values() if e["status"] == "missing"]
    placeholders = [e for e in entries.values() if e["status"] == "placeholder"]
    complete = [e for e in entries.values() if e["status"] == "complete"]

    return {
        "errors": errors,
        "warnings": warnings,
        "broken_references": len(broken_refs),
        "placeholder_count": len(placeholders),
        "complete_count": len(complete),
    }


def build_summary(entries: dict[str, dict]) -> dict:
    total = len(entries)
    complete = sum(1 for e in entries.values() if e["status"] == "complete")
    missing = sum(1 for e in entries.values() if e["status"] == "missing")
    placeholder = sum(1 for e in entries.values() if e["status"] == "placeholder")
    pct = round((complete / total) * 100, 1) if total else 0.0
    by_type: dict[str, dict[str, int]] = {}
    for entry in entries.values():
        t = entry["type"]
        bucket = by_type.setdefault(t, {"total": 0, "complete": 0, "missing": 0, "placeholder": 0})
        bucket["total"] += 1
        bucket[entry["status"]] += 1
    return {
        "total": total,
        "complete": complete,
        "missing": missing,
        "placeholder": placeholder,
        "completion_pct": pct,
        "by_type": by_type,
    }


def write_manifest(entries: dict[str, dict], summary: dict, validation: dict) -> None:
    VISUALS_ROOT.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "validation": {
            "error_count": len(validation["errors"]),
            "warning_count": len(validation["warnings"]),
            "errors": validation["errors"],
            "warnings": validation["warnings"],
        },
        "assets": sorted(entries.values(), key=lambda x: (x["type"], x["id"])),
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(entries: dict[str, dict], summary: dict, validation: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Visual Assets Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "Manifest: [assets/visuals/manifest.json](../../assets/visuals/manifest.json)",
        "",
        "Run `py tools/validate_visual_assets.py` to refresh this report.",
        "",
        "## Summary",
        "",
        f"- Total assets required: **{summary['total']}**",
        f"- Completed: **{summary['complete']}**",
        f"- Missing: **{summary['missing']}**",
        f"- Placeholder: **{summary['placeholder']}**",
        f"- Completion: **{summary['completion_pct']}%**",
        "",
        "## By type",
        "",
        "| Type | Total | Complete | Missing | Placeholder |",
        "|------|-------|----------|---------|-------------|",
    ]
    for asset_type in sorted(summary["by_type"]):
        block = summary["by_type"][asset_type]
        lines.append(
            f"| {asset_type} | {block['total']} | {block['complete']} | {block['missing']} | {block['placeholder']} |"
        )
    lines.extend(["", "## Validation", ""])
    if validation["errors"]:
        lines.append("### Errors")
        lines.append("")
        lines.extend(f"- {err}" for err in validation["errors"])
        lines.append("")
    else:
        lines.append("- No blocking errors.")
        lines.append("")
    if validation["warnings"]:
        lines.append("### Warnings")
        lines.append("")
        lines.extend(f"- {warn}" for warn in validation["warnings"][:40])
        if len(validation["warnings"]) > 40:
            lines.append(f"- … and {len(validation['warnings']) - 40} more")
        lines.append("")

    lines.extend(["## Missing assets", ""])
    missing_items = [e for e in entries.values() if e["status"] == "missing"]
    if missing_items:
        for entry in sorted(missing_items, key=lambda x: x["id"]):
            lines.append(f"- `{entry['path']}` — {entry['type']} ({entry['related_page'] or 'unlinked'})")
    else:
        lines.append("- None")
    lines.extend(["", "## Placeholder assets", ""])
    placeholder_items = [e for e in entries.values() if e["status"] == "placeholder"]
    if placeholder_items:
        for entry in sorted(placeholder_items, key=lambda x: x["id"])[:30]:
            lines.append(f"- `{entry['id']}` — {entry['type']} ({entry['related_page'] or 'unlinked'})")
        if len(placeholder_items) > 30:
            lines.append(f"- … and {len(placeholder_items) - 30} more")
    else:
        lines.append("- None")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def generate_visual_assets() -> dict:
    ensure_production_folders()
    entries = collect_content_assets()
    collect_disk_assets(entries)
    summary = build_summary(entries)
    validation = validate_assets(entries)
    write_manifest(entries, summary, validation)
    write_report(entries, summary, validation)
    return {"summary": summary, "validation": validation}


def main() -> int:
    result = generate_visual_assets()
    summary = result["summary"]
    validation = result["validation"]

    print("Visual asset pipeline")
    print(f"  Wrote {MANIFEST_PATH}")
    print(f"  Wrote {REPORT_PATH}")
    print()
    print(f"  Total: {summary['total']}  Complete: {summary['complete']}  Missing: {summary['missing']}  Placeholder: {summary['placeholder']}  ({summary['completion_pct']}%)")
    for err in validation["errors"][:10]:
        print(f"  ERROR: {err}")
    for warn in validation["warnings"][:10]:
        print(f"  WARN: {warn}")
    return 1 if validation["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
