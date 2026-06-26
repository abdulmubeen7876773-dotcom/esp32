import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "docs" / "reports"


def count_artifacts() -> dict:
    components = len(list((ROOT / "components").glob("*.html"))) if (ROOT / "components").exists() else 0
    guides = len(list((ROOT / "guides").glob("*.html"))) if (ROOT / "guides").exists() else 0
    projects = len(list((ROOT / "projects").glob("*.html"))) if (ROOT / "projects").exists() else 0
    static_pages = len(list(ROOT.glob("*.html")))
    if (ROOT / "category").exists():
        static_pages += len(list((ROOT / "category").glob("*.html")))

    search_index = 0
    search_path = ROOT / "search-index.json"
    if search_path.exists():
        data = json.loads(search_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            search_index = len(data)
        elif isinstance(data, dict):
            search_index = len(data.get("items") or data.get("entries") or [])

    sitemap = 0
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        root = ET.parse(sitemap_path).getroot()
        sitemap = len(root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"))
        if not sitemap:
            sitemap = len(root.findall(".//loc"))

    feed = 0
    feed_path = ROOT / "feed.xml"
    if feed_path.exists():
        root = ET.parse(feed_path).getroot()
        feed = len(root.findall(".//item"))

    return {
        "guides": guides,
        "components": components,
        "projects": projects,
        "pages": static_pages,
        "search_index": search_index,
        "sitemap": sitemap,
        "feed": feed,
    }


def build_report_payload(build_meta: dict) -> dict:
    counts = count_artifacts()
    duration = build_meta.get("duration_seconds", 0)
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": build_meta.get("status", "PASS"),
        "build_time_seconds": duration,
        "build_duration_seconds": duration,
        "generated_guides": counts["guides"],
        "generated_components": counts["components"],
        "generated_projects": counts["projects"],
        "generated_pages": counts["pages"],
        "search_index": counts["search_index"],
        "sitemap": counts["sitemap"],
        "feed": counts["feed"],
        "warnings": build_meta.get("warnings") or [],
        "errors": build_meta.get("errors") or [],
    }


def write_latest_build_md(report: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Latest Build Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Build Status",
        "",
        report["status"],
        "",
        "## Generated Pages",
        "",
        f"- Guides: {report['generated_guides']}",
        f"- Components: {report['generated_components']}",
        f"- Projects: {report['generated_projects']}",
        f"- Static pages: {report['generated_pages']}",
        "",
        "## Search Index",
        "",
        str(report["search_index"]),
        "",
        "## Sitemap",
        "",
        str(report["sitemap"]),
        "",
        "## Feed",
        "",
        str(report["feed"]),
        "",
        "## Build Time",
        "",
        f"{report['build_time_seconds']}s",
        "",
        "## Build Duration",
        "",
        f"{report['build_duration_seconds']}s",
        "",
        f"## Warnings ({len(report['warnings'])})",
        "",
    ]
    if report["warnings"]:
        lines.extend(f"- {w}" for w in report["warnings"])
    else:
        lines.append("- None")
    lines.extend(["", f"## Errors ({len(report['errors'])})", ""])
    if report["errors"]:
        lines.extend(f"- {e}" for e in report["errors"])
    else:
        lines.append("- None")
    lines.append("")
    (REPORTS_DIR / "latest-build.md").write_text("\n".join(lines), encoding="utf-8")


def generate_build_report(build_meta: dict) -> dict:
    report = build_report_payload(build_meta)
    (ROOT / "build-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_latest_build_md(report)
    print("\n=== build_report.py ===")
    print("Wrote build-report.json")
    print("Wrote docs/reports/latest-build.md")
    return report
