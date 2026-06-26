import json
import re
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_components, load_guides, load_projects

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REPORTS_DIR = ROOT / "docs" / "reports"

HREF_RE = re.compile(r"""href=["']([^"'#?]+)["']""")
SRC_RE = re.compile(r"""src=["']([^"'#?]+)["']""")
YAML_PATH_RE = re.compile(r"""["'](/(?:assets|guides|components|projects|category|images)[^"']+)["']""")

HTML_SCAN_DIRS = (
    ROOT,
    ROOT / "guides",
    ROOT / "components",
    ROOT / "projects",
    ROOT / "category",
)

PLACEHOLDER_HINTS = ("placeholder", "placehold.co", "via.placeholder", "unsplash.com", "picsum.photos")


def _is_mission(guide: dict) -> bool:
    return guide.get("format") == "mission" or bool(guide.get("mission"))


def _local_file_for_url(url: str) -> Path | None:
    if not url or url.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
        return None
    path = url.split("?")[0].split("#")[0]
    if not path.startswith("/"):
        return None
    rel = path.lstrip("/")
    if not rel:
        return ROOT / "index.html"
    candidate = ROOT / rel
    if candidate.is_file():
        return candidate
    html_candidate = candidate.with_suffix(".html")
    if html_candidate.is_file():
        return html_candidate
    return candidate


def _url_exists(url: str) -> bool:
    local = _local_file_for_url(url)
    if local is None:
        return True
    return local.is_file()


def _local_asset_exists(url: str) -> bool:
    if not url or not url.startswith("/"):
        return False
    return (ROOT / url.lstrip("/")).is_file()


def _normalize_site_url(url: str) -> str:
    path = url.split("?")[0].split("#")[0]
    if not path.startswith("/"):
        return path
    if path.endswith("/") and path != "/":
        path = path[:-1]
    if path == "/":
        return path
    if "." in Path(path.lstrip("/")).name:
        return path
    return f"{path}.html"


def _iter_html_files() -> list[Path]:
    files: list[Path] = []
    for base in HTML_SCAN_DIRS:
        if not base.exists():
            continue
        if base == ROOT:
            files.extend(base.glob("*.html"))
            continue
        if base.name == "projects":
            files.extend(base.glob("*.html"))
            continue
        files.extend(base.glob("*.html"))
    return sorted(set(files))


def _collect_yaml_asset_paths() -> set[str]:
    paths: set[str] = set()
    for folder in (CONTENT / "guides", CONTENT / "components", CONTENT / "projects", CONTENT / "pages"):
        if not folder.exists():
            continue
        for yaml_path in folder.glob("*.yaml"):
            text = yaml_path.read_text(encoding="utf-8", errors="replace")
            for match in YAML_PATH_RE.finditer(text):
                paths.add(match.group(1))
    return paths


def _collect_image_urls() -> list[dict]:
    refs: list[dict] = []
    for guide in load_guides():
        slug = guide.get("slug", "?")
        mission = guide.get("mission") or {}
        for block_name in ("concept", "wiring"):
            block = mission.get(block_name) or {}
            if isinstance(block, dict) and block.get("image"):
                refs.append({"source": f"guides/{slug}.yaml", "url": str(block["image"])})
    for comp in load_components():
        slug = comp.get("slug", "?")
        if comp.get("image"):
            refs.append({"source": f"components/{slug}.yaml", "url": str(comp["image"])})
        wiring = comp.get("wiring") or {}
        if isinstance(wiring, dict) and wiring.get("image"):
            refs.append({"source": f"components/{slug}.yaml", "url": str(wiring["image"])})
    for proj in load_projects():
        slug = proj.get("slug", "?")
        project = proj.get("project") or {}
        for field in ("hero_image", "image", "wiring_image", "output_image"):
            url = project.get(field) or proj.get(field)
            if url:
                refs.append({"source": f"projects/{slug}.yaml", "url": str(url)})
    return refs


def check_broken_links() -> list[dict]:
    issues: list[dict] = []
    seen: set[str] = set()

    for html_path in _iter_html_files():
        rel = html_path.relative_to(ROOT).as_posix()
        page = f"/{rel}" if rel != "index.html" else "/"
        text = html_path.read_text(encoding="utf-8", errors="replace")
        targets: set[str] = set()
        for match in HREF_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith("/"):
                targets.add(_normalize_site_url(raw))
        for match in SRC_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith("/"):
                targets.add(_normalize_site_url(raw))
        for target in targets:
            key = f"{target}|{page}"
            if key in seen:
                continue
            seen.add(key)
            if not _url_exists(target):
                issues.append({"url": target, "source": page, "type": "html"})

    for yaml_path in sorted(_collect_yaml_asset_paths()):
        key = f"{yaml_path}|yaml"
        if key in seen:
            continue
        seen.add(key)
        if not _url_exists(yaml_path):
            issues.append({"url": yaml_path, "source": "content YAML", "type": "yaml"})
    return issues


def check_missing_assets() -> list[dict]:
    issues: list[dict] = []
    seen: set[str] = set()

    for ref in _collect_image_urls():
        url = ref["url"]
        if not url.startswith("/"):
            continue
        if url in seen:
            continue
        seen.add(url)
        if not _local_file_for_url(url) or not _url_exists(url):
            issues.append({"url": url, "source": ref["source"]})

    for yaml_path in sorted(_collect_yaml_asset_paths()):
        if not yaml_path.startswith("/assets/"):
            continue
        if yaml_path in seen:
            continue
        seen.add(yaml_path)
        if not _url_exists(yaml_path):
            issues.append({"url": yaml_path, "source": "content YAML"})
    return issues


def check_placeholders() -> list[dict]:
    issues: list[dict] = []
    seen: set[str] = set()

    for ref in _collect_image_urls():
        url = ref["url"]
        key = f"{url}|{ref['source']}"
        if key in seen:
            continue
        seen.add(key)
        lower = url.lower()
        reason = ""
        if lower.startswith(("http://", "https://")):
            reason = "external CDN URL"
        elif any(hint in lower for hint in PLACEHOLDER_HINTS):
            reason = "placeholder path"
        elif url.startswith("/") and not _url_exists(url):
            reason = "missing local file"
        if reason:
            issues.append({"url": url, "source": ref["source"], "reason": reason})
    return issues


def _has_troubleshooting(guide: dict, mission: dict) -> bool:
    if guide.get("troubleshooting") or mission.get("troubleshooting"):
        return True
    expected = str(mission.get("expected_output") or guide.get("expected_output") or "")
    body = str(guide.get("body") or "")
    combined = (expected + body).lower()
    return any(
        phrase in combined
        for phrase in ("troubleshoot", "if nothing", "if the screen", "if you see", "if upload")
    )


def check_missing_quiz() -> list[dict]:
    issues: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        mission = guide.get("mission") or {}
        if mission.get("quiz") or guide.get("quiz"):
            continue
        issues.append({"slug": guide.get("slug", "?"), "source": f"guides/{guide.get('slug', '?')}.yaml"})
    return issues


def check_missing_wiring() -> list[dict]:
    issues: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        mission = guide.get("mission") or {}
        wiring = mission.get("wiring") or {}
        if not isinstance(wiring, dict) or not wiring.get("steps"):
            issues.append({"slug": slug, "source": f"guides/{slug}.yaml", "detail": "no wiring steps"})
            continue
        image = str(wiring.get("image") or "")
        if not _local_asset_exists(image):
            issues.append({"slug": slug, "source": f"guides/{slug}.yaml", "detail": "missing wiring diagram file"})
    return issues


def check_missing_challenge() -> list[dict]:
    issues: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        mission = guide.get("mission") or {}
        if mission.get("challenge_items") or mission.get("challenge") or guide.get("challenge"):
            continue
        issues.append({"slug": guide.get("slug", "?"), "source": f"guides/{guide.get('slug', '?')}.yaml"})
    return issues


def check_missing_troubleshooting() -> list[dict]:
    issues: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        mission = guide.get("mission") or {}
        if _has_troubleshooting(guide, mission):
            continue
        issues.append({"slug": guide.get("slug", "?"), "source": f"guides/{guide.get('slug', '?')}.yaml"})
    return issues


def build_release_report() -> dict:
    broken_links = check_broken_links()
    missing_assets = check_missing_assets()
    placeholders = check_placeholders()
    missing_quiz = check_missing_quiz()
    missing_wiring = check_missing_wiring()
    missing_challenge = check_missing_challenge()
    missing_troubleshooting = check_missing_troubleshooting()

    summary = {
        "broken_links": len(broken_links),
        "missing_assets": len(missing_assets),
        "placeholders": len(placeholders),
        "missing_quiz": len(missing_quiz),
        "missing_wiring": len(missing_wiring),
        "missing_challenge": len(missing_challenge),
        "missing_troubleshooting": len(missing_troubleshooting),
    }
    summary["total_issues"] = sum(summary.values())

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "PASS" if summary["total_issues"] == 0 else "WARN",
        "summary": summary,
        "broken_links": broken_links,
        "missing_assets": missing_assets,
        "placeholders": placeholders,
        "missing_quiz": missing_quiz,
        "missing_wiring": missing_wiring,
        "missing_challenge": missing_challenge,
        "missing_troubleshooting": missing_troubleshooting,
    }


def write_release_report_md(report: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary = report["summary"]
    lines = [
        "# Release Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Status",
        "",
        report["status"],
        "",
        "## Summary",
        "",
        f"- Broken links: {summary['broken_links']}",
        f"- Missing assets: {summary['missing_assets']}",
        f"- Placeholders: {summary['placeholders']}",
        f"- Missing quiz: {summary['missing_quiz']}",
        f"- Missing wiring: {summary['missing_wiring']}",
        f"- Missing challenge: {summary['missing_challenge']}",
        f"- Missing troubleshooting: {summary['missing_troubleshooting']}",
        f"- Total issues: {summary['total_issues']}",
        "",
    ]

    sections = [
        ("Broken Links", "broken_links", lambda item: f"{item['url']} (from {item['source']})"),
        ("Missing Assets", "missing_assets", lambda item: f"{item['url']} (from {item['source']})"),
        (
            "Placeholders",
            "placeholders",
            lambda item: f"{item['url']} — {item['reason']} (from {item['source']})",
        ),
        ("Missing Quiz", "missing_quiz", lambda item: item["source"]),
        (
            "Missing Wiring",
            "missing_wiring",
            lambda item: f"{item['source']} — {item.get('detail', 'missing wiring')}",
        ),
        ("Missing Challenge", "missing_challenge", lambda item: item["source"]),
        ("Missing Troubleshooting", "missing_troubleshooting", lambda item: item["source"]),
    ]

    for title, key, fmt in sections:
        items = report[key]
        lines.extend([f"## {title}", "", f"Count: {len(items)}", ""])
        if items:
            lines.extend(f"- {fmt(item)}" for item in items)
        else:
            lines.append("- None")
        lines.append("")

    (REPORTS_DIR / "release-report.md").write_text("\n".join(lines), encoding="utf-8")


def generate_release_report() -> dict:
    report = build_release_report()
    (ROOT / "release-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_release_report_md(report)
    print("\n=== release_validation.py ===")
    print("Wrote release-report.json")
    print("Wrote docs/reports/release-report.md")
    print(f"Release status: {report['status']} ({report['summary']['total_issues']} issues)")
    return report
