import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_components, load_guides, load_projects, load_yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REPORTS_DIR = ROOT / "docs" / "reports"

HREF_RE = re.compile(r"""href=["']([^"'#?]+)["']""")
SRC_RE = re.compile(r"""src=["']([^"'#?]+)["']""")

HTML_SCAN_DIRS = (
    ROOT,
    ROOT / "guides",
    ROOT / "components",
    ROOT / "projects",
    ROOT / "category",
)

PLACEHOLDER_HINTS = ("placeholder", "placehold.co", "via.placeholder", "unsplash.com", "picsum.photos")

REQUIRED_BUILD_OUTPUT = (
    "index.html",
    "guides.html",
    "components.html",
    "projects.html",
    "search-index.json",
    "sitemap.xml",
    "feed.xml",
    "projects.json",
    "project-icons.js",
)

Severity = str


def _finding(severity: Severity, category: str, message: str, **fields) -> dict:
    item = {"severity": severity, "category": category, "message": message}
    item.update(fields)
    return item


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


def _local_visual_photo(url: str) -> bool:
    return url.startswith("/assets/visuals/") and _local_asset_exists(url)


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


def _is_asset_url(url: str) -> bool:
    return url.startswith(("/assets/", "/images/"))


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


def _load_roadmap(name: str) -> dict:
    path = CONTENT / name
    if not path.exists():
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _published_slugs(folder: str) -> set[str]:
    path = CONTENT / folder
    if not path.exists():
        return set()
    return {p.stem for p in path.glob("*.yaml")}


def check_broken_links() -> list[dict]:
    findings: list[dict] = []
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
            if _is_asset_url(target):
                continue
            key = f"{target}|{page}"
            if key in seen:
                continue
            seen.add(key)
            if not _url_exists(target):
                findings.append(
                    _finding(
                        "BLOCKER",
                        "broken_links",
                        f"Broken link {target} on {page}",
                        url=target,
                        source=page,
                    )
                )
    return findings


def check_missing_pages() -> list[dict]:
    findings: list[dict] = []
    for guide in load_guides():
        slug = guide.get("slug", "?")
        html_path = ROOT / "guides" / f"{slug}.html"
        if not html_path.is_file():
            findings.append(
                _finding(
                    "BLOCKER",
                    "missing_pages",
                    f"Guide YAML has no built HTML page: guides/{slug}.html",
                    slug=slug,
                    source=f"content/guides/{slug}.yaml",
                    expected=str(html_path.relative_to(ROOT)),
                )
            )
    for comp in load_components():
        slug = comp.get("slug", "?")
        html_path = ROOT / "components" / f"{slug}.html"
        if not html_path.is_file():
            findings.append(
                _finding(
                    "BLOCKER",
                    "missing_pages",
                    f"Component YAML has no built HTML page: components/{slug}.html",
                    slug=slug,
                    source=f"content/components/{slug}.yaml",
                    expected=str(html_path.relative_to(ROOT)),
                )
            )
    for proj in load_projects():
        slug = proj.get("slug", "?")
        html_path = ROOT / "projects" / f"{slug}.html"
        if not html_path.is_file():
            findings.append(
                _finding(
                    "BLOCKER",
                    "missing_pages",
                    f"Project YAML has no built HTML page: projects/{slug}.html",
                    slug=slug,
                    source=f"content/projects/{slug}.yaml",
                    expected=str(html_path.relative_to(ROOT)),
                )
            )
    return findings


def check_missing_build_output() -> list[dict]:
    findings: list[dict] = []
    for rel in REQUIRED_BUILD_OUTPUT:
        path = ROOT / rel
        if not path.is_file():
            findings.append(
                _finding(
                    "BLOCKER",
                    "missing_build_output",
                    f"Required build artifact missing: {rel}",
                    path=rel,
                )
            )
    return findings


def check_build_failures(build_meta: dict) -> list[dict]:
    findings: list[dict] = []
    status = str(build_meta.get("status", "PASS")).upper()
    if status == "FAIL":
        findings.append(
            _finding(
                "BLOCKER",
                "build_failures",
                "Build did not complete successfully",
                status=status,
            )
        )
    for error in build_meta.get("errors") or []:
        findings.append(
            _finding(
                "BLOCKER",
                "build_failures",
                str(error),
                detail=str(error),
            )
        )
    return findings


def check_duplicate_urls() -> list[dict]:
    findings: list[dict] = []
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        return findings
    try:
        root = ET.parse(sitemap_path).getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [el.text.strip() for el in root.findall(".//sm:loc", ns) if el.text]
        if not locs:
            locs = [el.text.strip() for el in root.findall(".//loc") if el.text]
        seen: dict[str, int] = {}
        for loc in locs:
            seen[loc] = seen.get(loc, 0) + 1
        for loc, count in sorted(seen.items()):
            if count > 1:
                findings.append(
                    _finding(
                        "BLOCKER",
                        "duplicate_urls",
                        f"Duplicate sitemap URL ({count}×): {loc}",
                        url=loc,
                        count=count,
                    )
                )
    except ET.ParseError:
        findings.append(
            _finding(
                "BLOCKER",
                "duplicate_urls",
                "Could not parse sitemap.xml to check duplicate URLs",
                path="sitemap.xml",
            )
        )
    return findings


def check_placeholder_images() -> list[dict]:
    findings: list[dict] = []
    seen: set[str] = set()

    for comp in load_components():
        slug = comp.get("slug", "?")
        source = f"components/{slug}.yaml"
        url = str(comp.get("image") or "")
        if not url:
            continue
        key = f"{source}|{url}"
        if key in seen:
            continue
        seen.add(key)
        lower = url.lower()
        reason = ""
        if lower.startswith(("http://", "https://")):
            reason = "external CDN URL"
        elif any(hint in lower for hint in PLACEHOLDER_HINTS):
            reason = "placeholder path"
        if reason:
            findings.append(
                _finding(
                    "WARNING",
                    "placeholder_images",
                    f"{source}: {reason}",
                    url=url,
                    source=source,
                    reason=reason,
                )
            )
    return findings


def check_missing_wiring_diagrams() -> list[dict]:
    findings: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        source = f"guides/{slug}.yaml"
        mission = guide.get("mission") or {}
        wiring = mission.get("wiring") or {}
        if not isinstance(wiring, dict) or not wiring.get("steps"):
            findings.append(
                _finding(
                    "WARNING",
                    "missing_wiring_diagrams",
                    f"{source}: no wiring steps",
                    slug=slug,
                    source=source,
                )
            )
            continue
        image = str(wiring.get("image") or "")
        if not _local_asset_exists(image):
            findings.append(
                _finding(
                    "WARNING",
                    "missing_wiring_diagrams",
                    f"{source}: missing wiring diagram file",
                    slug=slug,
                    source=source,
                    url=image or None,
                )
            )

    for comp in load_components():
        slug = comp.get("slug", "?")
        source = f"components/{slug}.yaml"
        wiring = comp.get("wiring") or {}
        if not isinstance(wiring, dict) or not (wiring.get("steps") or wiring.get("summary")):
            continue
        image = str(wiring.get("image") or "")
        if not _local_asset_exists(image):
            findings.append(
                _finding(
                    "WARNING",
                    "missing_wiring_diagrams",
                    f"{source}: missing wiring diagram file",
                    slug=slug,
                    source=source,
                    url=image or None,
                )
            )
    return findings


def check_missing_illustrations() -> list[dict]:
    findings: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        source = f"guides/{slug}.yaml"
        mission = guide.get("mission") or {}
        concept = mission.get("concept") or {}
        if not isinstance(concept, dict):
            continue
        if not (concept.get("illustration_alt") or concept.get("image")):
            continue
        image = str(concept.get("image") or "")
        if not _local_asset_exists(image):
            findings.append(
                _finding(
                    "WARNING",
                    "missing_illustrations",
                    f"{source}: missing concept illustration",
                    slug=slug,
                    source=source,
                    url=image or None,
                )
            )
    return findings


def check_missing_photos() -> list[dict]:
    findings: list[dict] = []
    for comp in load_components():
        slug = comp.get("slug", "?")
        source = f"components/{slug}.yaml"
        image = str(comp.get("image") or "")
        if _local_visual_photo(image):
            continue
        findings.append(
            _finding(
                "WARNING",
                "missing_photos",
                f"{source}: no local component photo in /assets/visuals/",
                slug=slug,
                source=source,
                url=image or None,
            )
        )
    return findings


def check_coming_soon_content() -> list[dict]:
    findings: list[dict] = []
    guide_roadmap = _load_roadmap("guide-roadmap.yaml")
    component_roadmap = _load_roadmap("component-roadmap.yaml")
    published_guides = _published_slugs("guides")
    published_components = _published_slugs("components")

    for item in guide_roadmap.get("missions") or []:
        if str(item.get("status", "")).lower() != "coming soon":
            continue
        slug = item.get("slug", "?")
        findings.append(
            _finding(
                "INFO",
                "coming_soon_content",
                f"Guide mission coming soon: {item.get('title', slug)}",
                slug=slug,
                roadmap="guide-roadmap.yaml",
                status="Coming Soon",
                published=slug in published_guides,
            )
        )

    for item in component_roadmap.get("components") or []:
        if str(item.get("status", "")).lower() != "coming soon":
            continue
        slug = item.get("slug", "?")
        findings.append(
            _finding(
                "INFO",
                "coming_soon_content",
                f"Component coming soon: {item.get('name', slug)}",
                slug=slug,
                roadmap="component-roadmap.yaml",
                status="Coming Soon",
                published=slug in published_components,
            )
        )
    return findings


def check_planned_assets() -> list[dict]:
    findings: list[dict] = []
    for guide in load_guides():
        if not _is_mission(guide):
            continue
        slug = guide.get("slug", "?")
        source = f"guides/{slug}.yaml"
        mission = guide.get("mission") or {}
        wiring = mission.get("wiring") or {}
        if not isinstance(wiring, dict):
            continue
        image = str(wiring.get("image") or "")
        if image.startswith("/assets/visuals/") and not _local_asset_exists(image):
            findings.append(
                _finding(
                    "INFO",
                    "planned_assets",
                    f"{source}: planned wiring asset not yet published",
                    slug=slug,
                    source=source,
                    url=image,
                )
            )
        concept = mission.get("concept") or {}
        if isinstance(concept, dict):
            image = str(concept.get("image") or "")
            if image.startswith("/assets/visuals/") and not _local_asset_exists(image):
                findings.append(
                    _finding(
                        "INFO",
                        "planned_assets",
                        f"{source}: planned concept asset not yet published",
                        slug=slug,
                        source=source,
                        url=image,
                    )
                )
    return findings


def check_incomplete_roadmap_items() -> list[dict]:
    findings: list[dict] = []
    guide_roadmap = _load_roadmap("guide-roadmap.yaml")
    component_roadmap = _load_roadmap("component-roadmap.yaml")

    if guide_roadmap:
        complete = int(guide_roadmap.get("complete_count") or 0)
        planned = int(guide_roadmap.get("target_total") or 0)
        remaining = max(0, planned - complete)
        findings.append(
            _finding(
                "INFO",
                "incomplete_roadmap_items",
                f"Guides roadmap: {complete}/{planned} complete ({remaining} remaining)",
                roadmap="guide-roadmap.yaml",
                complete=complete,
                planned=planned,
                remaining=remaining,
            )
        )

    if component_roadmap:
        complete = int(component_roadmap.get("complete_count") or 0)
        planned = int(component_roadmap.get("target_total") or 0)
        remaining = max(0, planned - complete)
        findings.append(
            _finding(
                "INFO",
                "incomplete_roadmap_items",
                f"Components roadmap: {complete}/{planned} complete ({remaining} remaining)",
                roadmap="component-roadmap.yaml",
                complete=complete,
                planned=planned,
                remaining=remaining,
            )
        )

    projects_complete = len(load_projects())
    findings.append(
        _finding(
            "INFO",
            "incomplete_roadmap_items",
            f"Projects portfolio: {projects_complete} golden projects published",
            complete=projects_complete,
            planned=projects_complete,
            remaining=0,
        )
    )
    return findings


def _count_by_severity(findings: list[dict]) -> dict:
    counts = {"BLOCKER": 0, "WARNING": 0, "INFO": 0}
    for item in findings:
        counts[item["severity"]] = counts.get(item["severity"], 0) + 1
    return counts


def _count_by_category(findings: list[dict]) -> dict:
    categories: dict[str, dict[str, int]] = {}
    for item in findings:
        cat = item["category"]
        sev = item["severity"]
        if cat not in categories:
            categories[cat] = {"BLOCKER": 0, "WARNING": 0, "INFO": 0, "total": 0}
        categories[cat][sev] = categories[cat].get(sev, 0) + 1
        categories[cat]["total"] += 1
    return categories


def _release_status(severity_counts: dict) -> str:
    if severity_counts.get("BLOCKER", 0) > 0:
        return "BLOCKED"
    if severity_counts.get("WARNING", 0) > 0:
        return "WARN"
    return "PASS"


def build_release_report(build_meta: dict | None = None) -> dict:
    build_meta = build_meta or {"status": "PASS", "errors": []}
    all_findings = [
        *check_build_failures(build_meta),
        *check_broken_links(),
        *check_missing_pages(),
        *check_missing_build_output(),
        *check_duplicate_urls(),
        *check_placeholder_images(),
        *check_missing_wiring_diagrams(),
        *check_missing_illustrations(),
        *check_missing_photos(),
        *check_coming_soon_content(),
        *check_planned_assets(),
        *check_incomplete_roadmap_items(),
    ]

    severity_counts = _count_by_severity(all_findings)
    grouped = {
        "blocker": [f for f in all_findings if f["severity"] == "BLOCKER"],
        "warning": [f for f in all_findings if f["severity"] == "WARNING"],
        "info": [f for f in all_findings if f["severity"] == "INFO"],
    }

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": _release_status(severity_counts),
        "build_status": str(build_meta.get("status", "PASS")).upper(),
        "summary": {
            "blocker": severity_counts.get("BLOCKER", 0),
            "warning": severity_counts.get("WARNING", 0),
            "info": severity_counts.get("INFO", 0),
            "total": len(all_findings),
        },
        "severity_rules": {
            "BLOCKER": [
                "broken_links",
                "missing_pages",
                "missing_build_output",
                "build_failures",
                "duplicate_urls",
            ],
            "WARNING": [
                "placeholder_images",
                "missing_wiring_diagrams",
                "missing_illustrations",
                "missing_photos",
            ],
            "INFO": [
                "coming_soon_content",
                "planned_assets",
                "incomplete_roadmap_items",
            ],
        },
        "categories": _count_by_category(all_findings),
        "findings": grouped,
    }


def _format_finding(item: dict) -> str:
    parts = [item["message"]]
    if item.get("url"):
        parts.append(f"({item['url']})")
    elif item.get("source") and item["category"] not in ("coming_soon_content", "incomplete_roadmap_items"):
        parts.append(f"({item['source']})")
    return " ".join(parts)


def write_release_report_md(report: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary = report["summary"]
    lines = [
        "# Release Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Release Status",
        "",
        report["status"],
        "",
        f"Build status: {report['build_status']}",
        "",
        "## Severity Summary",
        "",
        f"- BLOCKER: {summary['blocker']}",
        f"- WARNING: {summary['warning']}",
        f"- INFO: {summary['info']}",
        f"- Total findings: {summary['total']}",
        "",
        "## Severity Rules",
        "",
        "### BLOCKER",
        "",
        "- Broken links",
        "- Missing pages",
        "- Missing build output",
        "- Build failures",
        "- Duplicate URLs",
        "",
        "### WARNING",
        "",
        "- Placeholder images",
        "- Missing wiring diagrams",
        "- Missing illustrations",
        "- Missing photos",
        "",
        "### INFO",
        "",
        "- Coming soon content",
        "- Planned assets",
        "- Incomplete roadmap items",
        "",
    ]

    for severity_key, title in (("blocker", "BLOCKER"), ("warning", "WARNING"), ("info", "INFO")):
        items = report["findings"][severity_key]
        lines.extend([f"## {title}", "", f"Count: {len(items)}", ""])
        if not items:
            lines.append("- None")
            lines.append("")
            continue
        by_category: dict[str, list[dict]] = {}
        for item in items:
            by_category.setdefault(item["category"], []).append(item)
        for category in sorted(by_category):
            cat_items = by_category[category]
            lines.append(f"### {category} ({len(cat_items)})")
            lines.append("")
            display_items = cat_items if severity_key != "info" else cat_items[:25]
            for item in display_items:
                lines.append(f"- {_format_finding(item)}")
            if severity_key == "info" and len(cat_items) > 25:
                lines.append(f"- … and {len(cat_items) - 25} more")
            lines.append("")

    (REPORTS_DIR / "release-report.md").write_text("\n".join(lines), encoding="utf-8")


def generate_release_report(build_meta: dict | None = None) -> dict:
    report = build_release_report(build_meta)
    (ROOT / "release-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_release_report_md(report)
    print("\n=== release_validation.py ===")
    print("Wrote release-report.json")
    print("Wrote docs/reports/release-report.md")
    print(
        f"Release status: {report['status']} "
        f"(blocker={report['summary']['blocker']}, "
        f"warning={report['summary']['warning']}, "
        f"info={report['summary']['info']})"
    )
    return report
