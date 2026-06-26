import json
import re
import struct
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import yaml

from cms_loader import load_components, load_guides, load_pages, load_projects, load_yaml
from content_store import validate_content

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "docs" / "reports"
CONTENT = ROOT / "content"

HREF_RE = re.compile(r"""href=["']([^"'#?]+)["']""")
SRC_RE = re.compile(r"""src=["']([^"'#?]+)["']""")
YAML_PATH_RE = re.compile(r"""["'](/(?:assets|guides|components|projects|category|images)[^"']+)["']""")

SUPPORTED_IMAGE_EXT = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
PLACEHOLDER_HOSTS = ("placeholder", "placehold.co", "via.placeholder", "unsplash.com", "picsum.photos")

DIMENSION_TARGETS = {
    "components/photo": (800, 600),
    "components/pinout": (600, 400),
    "guides/wiring": (960, 540),
    "guides/concept": (720, 480),
    "guides/output": (800, 450),
    "projects/hero": (1200, 630),
    "projects/wiring": (960, 540),
    "projects/output": (800, 600),
}

DOC_FILES = (
    "docs/README.md",
    "docs/editorial/MANIFESTO.md",
    "docs/editorial/EDUCATIONAL_FRAMEWORK.md",
    "docs/editorial/WRITING_STYLE_GUIDE.md",
    "docs/editorial/CONTENT_QA_CHECKLIST.md",
    "docs/guides/CONTENT_EDITOR_GUIDE.md",
    "docs/engineering/DEVELOPER_ARCHITECTURE.md",
    "docs/reference/CONTENT_INVENTORY.md",
)

HTML_SCAN_DIRS = (
    ROOT,
    ROOT / "guides",
    ROOT / "components",
    ROOT / "projects",
    ROOT / "category",
)

LISTING_PAGES = {
    "/",
    "/index.html",
    "/guides.html",
    "/components.html",
    "/projects.html",
    "/sitemap.html",
    "/search.html",
    "/404.html",
}

ORPHAN_EXCLUDE_PREFIXES = ("/google", "/pinterest-", "/category/index")


def _load_roadmap(name: str) -> dict:
    path = CONTENT / name
    if not path.exists():
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _is_mission(guide: dict) -> bool:
    return guide.get("format") == "mission" or bool(guide.get("mission"))


def _is_reference_guide(guide: dict) -> bool:
    return not _is_mission(guide)


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
    if candidate.with_suffix(".html").is_file():
        return candidate.with_suffix(".html")
    if (candidate / "index.html").is_file():
        return candidate / "index.html"
    return candidate


def _url_exists(url: str) -> bool:
    local = _local_file_for_url(url)
    if local is None:
        return True
    return local.is_file()


def _is_placeholder_url(url: str) -> bool:
    if not url:
        return False
    lower = url.lower()
    if "placeholder" in lower:
        return True
    if any(host in lower for host in PLACEHOLDER_HOSTS):
        return True
    if lower.startswith(("http://", "https://")):
        return True
    return False


def _iter_html_files() -> list[Path]:
    files: list[Path] = []
    for base in HTML_SCAN_DIRS:
        if not base.exists():
            continue
        if base == ROOT:
            for path in base.glob("*.html"):
                files.append(path)
            continue
        if base.name == "projects":
            for path in base.glob("*.html"):
                files.append(path)
            continue
        files.extend(base.glob("*.html"))
    return sorted(set(files))


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


def _collect_html_links() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    hrefs_by_page: dict[str, set[str]] = {}
    srcs_by_page: dict[str, set[str]] = {}
    for html_path in _iter_html_files():
        rel = html_path.relative_to(ROOT).as_posix()
        page_url = f"/{rel}" if rel != "index.html" else "/"
        text = html_path.read_text(encoding="utf-8", errors="replace")
        hrefs = set()
        srcs = set()
        for match in HREF_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith("/"):
                hrefs.add(_normalize_site_url(raw))
        for match in SRC_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith("/"):
                srcs.add(_normalize_site_url(raw))
        hrefs_by_page[page_url] = hrefs
        srcs_by_page[page_url] = srcs
    return hrefs_by_page, srcs_by_page


def _discovered_urls() -> set[str]:
    urls = set(LISTING_PAGES)
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        try:
            root = ET.parse(sitemap_path).getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [el.text.strip() for el in root.findall(".//sm:loc", ns) if el.text]
            if not locs:
                locs = [el.text.strip() for el in root.findall(".//loc") if el.text]
            for loc in locs:
                path = loc.replace("https://esp32engine.com", "").replace("http://esp32engine.com", "")
                urls.add(_normalize_site_url(path))
        except ET.ParseError:
            pass
    search_path = ROOT / "search-index.json"
    if search_path.exists():
        try:
            data = json.loads(search_path.read_text(encoding="utf-8"))
            items = data if isinstance(data, list) else data.get("items") or data.get("entries") or []
            for item in items:
                if isinstance(item, dict) and item.get("url"):
                    urls.add(_normalize_site_url(str(item["url"])))
        except (json.JSONDecodeError, OSError):
            pass
    return urls


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


def check_links() -> dict:
    hrefs_by_page, srcs_by_page = _collect_html_links()
    broken_internal: list[str] = []
    missing_pages: list[str] = []
    missing_assets: list[str] = []
    broken_images: list[str] = []
    duplicate_urls: list[str] = []
    unused_pages: list[str] = []

    all_targets: dict[str, list[str]] = {}
    for page, hrefs in hrefs_by_page.items():
        for href in hrefs:
            all_targets.setdefault(href, []).append(page)
    for page, srcs in srcs_by_page.items():
        for src in srcs:
            all_targets.setdefault(src, []).append(page)

    for target, sources in sorted(all_targets.items()):
        if not _url_exists(target):
            entry = f"{target} (from {', '.join(sorted(set(sources))[:3])})"
            if any(target.startswith(p) for p in ("/assets/", "/images/")):
                missing_assets.append(entry)
                if target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                    broken_images.append(entry)
            else:
                broken_internal.append(entry)
                missing_pages.append(entry)

    for yaml_path in sorted(_collect_yaml_asset_paths()):
        if not _url_exists(yaml_path):
            entry = f"{yaml_path} (YAML reference)"
            if yaml_path.startswith("/assets/"):
                missing_assets.append(entry)
            else:
                broken_internal.append(entry)

    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        try:
            root = ET.parse(sitemap_path).getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [el.text.strip() for el in root.findall(".//sm:loc", ns) if el.text]
            if not locs:
                locs = [el.text.strip() for el in root.findall(".//loc") if el.text]
            normalized = [_normalize_site_url(u.replace("https://esp32engine.com", "").replace("http://esp32engine.com", "")) for u in locs]
            seen: dict[str, int] = {}
            for loc in normalized:
                seen[loc] = seen.get(loc, 0) + 1
            duplicate_urls = [f"{loc} ({count}× in sitemap)" for loc, count in sorted(seen.items()) if count > 1]
        except ET.ParseError:
            pass

    all_linked = set()
    for hrefs in hrefs_by_page.values():
        all_linked.update(hrefs)
    for srcs in srcs_by_page.values():
        all_linked.update(srcs)
    all_linked.update(_discovered_urls())

    for html_path in _iter_html_files():
        rel = html_path.relative_to(ROOT).as_posix()
        page_url = f"/{rel}" if rel != "index.html" else "/"
        norm = _normalize_site_url(page_url)
        if norm in LISTING_PAGES or page_url in LISTING_PAGES:
            continue
        if any(norm.startswith(prefix) for prefix in ORPHAN_EXCLUDE_PREFIXES):
            continue
        if norm not in all_linked and page_url not in all_linked:
            unused_pages.append(page_url)

    return {
        "broken_internal_links": broken_internal,
        "missing_pages": missing_pages,
        "missing_assets": missing_assets,
        "broken_image_paths": broken_images,
        "duplicate_urls": duplicate_urls,
        "unused_pages": unused_pages,
        "summary": {
            "broken_internal_links": len(broken_internal),
            "missing_pages": len(missing_pages),
            "missing_assets": len(missing_assets),
            "broken_image_paths": len(broken_images),
            "duplicate_urls": len(duplicate_urls),
            "unused_pages": len(unused_pages),
        },
    }


def _has_troubleshooting(guide: dict, mission: dict) -> bool:
    if guide.get("troubleshooting") or mission.get("troubleshooting"):
        return True
    expected = str(mission.get("expected_output") or guide.get("expected_output") or "")
    body = str(guide.get("body") or "")
    combined = (expected + body).lower()
    return "troubleshoot" in combined or "if nothing" in combined or "if you see" in combined


def _has_component_spotlight(guide: dict, mission: dict) -> bool:
    if mission.get("component_spotlight_lead") or guide.get("component_spotlight_lead"):
        return True
    for item in mission.get("things_you_need") or []:
        if isinstance(item, dict) and str(item.get("link", "")).startswith("/components/"):
            return True
    return False


def _has_related_guides(guide: dict, mission: dict) -> bool:
    if guide.get("related_guides"):
        return True
    if mission.get("next_missions"):
        return True
    return False


def content_validation_warnings() -> list[dict]:
    warnings: list[dict] = []
    for guide in load_guides():
        slug = guide.get("slug", "?")
        mission = guide.get("mission") or {}
        if not _is_mission(guide):
            continue
        checks = [
            ("no_quiz", bool(mission.get("quiz") or guide.get("quiz"))),
            ("no_challenge", bool(mission.get("challenge_items") or mission.get("challenge") or guide.get("challenge"))),
            ("no_wiring", bool(mission.get("wiring") and (mission.get("wiring") or {}).get("steps"))),
            ("no_output", bool(mission.get("expected_output") or guide.get("expected_output"))),
            ("no_troubleshooting", _has_troubleshooting(guide, mission)),
            ("no_related_guides", _has_related_guides(guide, mission)),
            ("no_related_projects", bool(guide.get("related_projects"))),
            ("no_component_spotlight", _has_component_spotlight(guide, mission)),
        ]
        for code, ok in checks:
            if not ok:
                warnings.append({"type": code, "source": f"guides/{slug}.yaml", "slug": slug})
    return warnings


def _read_raster_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    if data[:2] == b"\xff\xd8":
        idx = 2
        while idx < len(data) - 8:
            if data[idx] != 0xFF:
                idx += 1
                continue
            marker = data[idx + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[idx + 5 : idx + 9])
                return w, h
            length = struct.unpack(">H", data[idx + 2 : idx + 4])[0]
            idx += 2 + length
    return None


def _dimension_target_for_path(path: str) -> tuple[int, int] | None:
    lower = path.lower()
    for key, dims in DIMENSION_TARGETS.items():
        if key.replace("/", "/visuals/") in lower or key in lower:
            return dims
    if "/wiring/" in lower:
        return DIMENSION_TARGETS["guides/wiring"]
    if "/concept/" in lower:
        return DIMENSION_TARGETS["guides/concept"]
    if "/photo/" in lower:
        return DIMENSION_TARGETS["components/photo"]
    if "/pinout/" in lower:
        return DIMENSION_TARGETS["components/pinout"]
    return None


def _collect_image_refs() -> list[dict]:
    refs: list[dict] = []
    for guide in load_guides():
        slug = guide.get("slug", "?")
        mission = guide.get("mission") or {}
        concept = mission.get("concept") or {}
        wiring = mission.get("wiring") or {}
        for label, block in (("concept", concept), ("wiring", wiring)):
            if not isinstance(block, dict):
                continue
            refs.append(
                {
                    "source": f"guides/{slug}.yaml",
                    "field": f"mission.{label}",
                    "url": block.get("image", ""),
                    "alt": block.get("illustration_alt") or block.get("alt") or "",
                }
            )
    for comp in load_components():
        slug = comp.get("slug", "?")
        refs.append(
            {
                "source": f"components/{slug}.yaml",
                "field": "image",
                "url": comp.get("image", ""),
                "alt": comp.get("image_alt") or "",
            }
        )
        wiring = comp.get("wiring") or {}
        if isinstance(wiring, dict):
            refs.append(
                {
                    "source": f"components/{slug}.yaml",
                    "field": "wiring.image",
                    "url": wiring.get("image", ""),
                    "alt": wiring.get("illustration_alt") or wiring.get("alt") or "",
                }
            )
    for proj in load_projects():
        slug = proj.get("slug", "?")
        project = proj.get("project") or {}
        for field in ("hero_image", "image", "wiring_image", "output_image"):
            url = str(project.get(field) or proj.get(field) or "").strip()
            alt = str(project.get(f"{field}_alt") or proj.get("image_alt") or "").strip()
            if not url and not alt:
                continue
            refs.append(
                {
                    "source": f"projects/{slug}.yaml",
                    "field": field,
                    "url": url,
                    "alt": alt,
                }
            )
    return refs


def image_validation_warnings() -> list[dict]:
    warnings: list[dict] = []
    for ref in _collect_image_refs():
        url = str(ref.get("url") or "").strip()
        alt = str(ref.get("alt") or "").strip()
        source = ref["source"]
        field = ref["field"]
        if not url:
            if alt:
                warnings.append({"type": "missing_image_for_alt", "source": source, "field": field})
            continue
        if not alt:
            warnings.append({"type": "missing_alt_text", "source": source, "field": field, "url": url})
        if _is_placeholder_url(url):
            warnings.append({"type": "placeholder_image", "source": source, "field": field, "url": url})
        local = _local_file_for_url(url)
        if local and local.is_file():
            ext = local.suffix.lower()
            if ext not in SUPPORTED_IMAGE_EXT:
                warnings.append({"type": "unsupported_format", "source": source, "field": field, "url": url})
            elif ext in {".png", ".jpg", ".jpeg"}:
                dims = _read_raster_dimensions(local)
                target = _dimension_target_for_path(url)
                if dims and target:
                    tw, th = target
                    w, h = dims
                    tolerance = 0.15
                    if abs(w - tw) / tw > tolerance or abs(h - th) / th > tolerance:
                        warnings.append(
                            {
                                "type": "wrong_dimensions",
                                "source": source,
                                "field": field,
                                "url": url,
                                "actual": f"{w}x{h}",
                                "expected": f"{tw}x{th}",
                            }
                        )
        elif url.startswith("/"):
            warnings.append({"type": "missing_image_file", "source": source, "field": field, "url": url})
    return warnings


def build_content_dashboard() -> dict:
    guide_roadmap = _load_roadmap("guide-roadmap.yaml")
    component_roadmap = _load_roadmap("component-roadmap.yaml")
    guides = load_guides()
    components = load_components()
    projects = load_projects()

    mission_count = sum(1 for g in guides if _is_mission(g))
    reference_count = sum(1 for g in guides if _is_reference_guide(g))

    missing_illustrations: list[str] = []
    missing_wiring: list[str] = []
    missing_photos: list[str] = []
    missing_pinouts: list[str] = []

    for guide in guides:
        slug = guide.get("slug", "?")
        if not _is_mission(guide):
            continue
        mission = guide.get("mission") or {}
        concept = mission.get("concept") or {}
        wiring = mission.get("wiring") or {}
        concept_img = concept.get("image", "") if isinstance(concept, dict) else ""
        wiring_img = wiring.get("image", "") if isinstance(wiring, dict) else ""
        if concept.get("illustration_alt") and not (concept_img and _url_exists(concept_img)):
            missing_illustrations.append(f"guides/{slug}: concept illustration")
        if wiring.get("steps") and not (wiring_img and _url_exists(wiring_img)):
            missing_wiring.append(f"guides/{slug}: wiring diagram")

    for comp in components:
        slug = comp.get("slug", "?")
        image = str(comp.get("image") or "")
        if not image or _is_placeholder_url(image):
            missing_photos.append(f"components/{slug}: photo")
        if not comp.get("pinout"):
            missing_pinouts.append(f"components/{slug}: pinout")

    components_planned = component_roadmap.get("target_total", len(components))
    components_completed = len(components)
    guides_planned = guide_roadmap.get("target_total", len(guides))
    guides_completed = guide_roadmap.get("complete_count", mission_count + reference_count)
    projects_completed = len(projects)
    projects_planned = projects_completed

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "components": {"completed": components_completed, "planned": components_planned},
        "guides": {"completed": guides_completed, "planned": guides_planned},
        "projects": {"completed": projects_completed, "planned": projects_planned},
        "mission_count": mission_count,
        "reference_guides": reference_count,
        "illustrations": {
            "missing": len(missing_illustrations),
            "items": missing_illustrations,
        },
        "missing_wiring_diagrams": missing_wiring,
        "missing_photos": missing_photos,
        "missing_pinouts": missing_pinouts,
        "content_files": {
            "guides_yaml": len(guides),
            "components_yaml": len(components),
            "projects_yaml": len(projects),
        },
    }


def count_build_artifacts() -> dict:
    components_html = len(list((ROOT / "components").glob("*.html"))) if (ROOT / "components").exists() else 0
    guides_html = len(list((ROOT / "guides").glob("*.html"))) if (ROOT / "guides").exists() else 0
    projects_html = len(list((ROOT / "projects").glob("*.html"))) if (ROOT / "projects").exists() else 0
    static_html = len(list(ROOT.glob("*.html")))
    category_html = len(list((ROOT / "category").glob("*.html"))) if (ROOT / "category").exists() else 0

    search_count = 0
    search_path = ROOT / "search-index.json"
    if search_path.exists():
        data = json.loads(search_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            search_count = len(data)
        elif isinstance(data, dict):
            search_count = len(data.get("items") or data.get("entries") or [])

    sitemap_count = 0
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        root = ET.parse(sitemap_path).getroot()
        sitemap_count = len(root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"))
        if not sitemap_count:
            sitemap_count = len(root.findall(".//loc"))

    feed_count = 0
    feed_path = ROOT / "feed.xml"
    if feed_path.exists():
        root = ET.parse(feed_path).getroot()
        feed_count = len(root.findall(".//item"))

    return {
        "components": components_html,
        "guides": guides_html,
        "projects": projects_html,
        "static_pages": static_html + category_html,
        "search_index_entries": search_count,
        "sitemap_urls": sitemap_count,
        "feed_items": feed_count,
    }


def compute_quality_scores(
    build_status: str,
    link_report: dict,
    content_warnings: list,
    image_warnings: list,
    dashboard: dict,
    build_errors: list,
) -> dict:
    link_issues = sum(link_report["summary"].values())
    content_warn_count = len(content_warnings)
    image_warn_count = len(image_warnings)

    guides = load_guides()
    components = load_components()
    pages = load_pages()
    mission_total = max(1, sum(1 for g in guides if _is_mission(g)))

    build_score = 100 if build_status == "PASS" else 0
    build_score = max(0, build_score - len(build_errors) * 10)

    content_deductions = content_warn_count * 4
    content_score = max(0, 100 - int(content_deductions * 100 / (mission_total * 8)))

    asset_gaps = (
        len(dashboard.get("missing_wiring_diagrams") or [])
        + len(dashboard.get("missing_photos") or [])
        + len(dashboard.get("missing_pinouts") or [])
        + dashboard.get("illustrations", {}).get("missing", 0)
    )
    asset_total = max(1, len(guides) + len(components))
    asset_score = max(0, 100 - int(asset_gaps * 100 / asset_total))

    docs_present = sum(1 for rel in DOC_FILES if (ROOT / rel).is_file())
    documentation_score = int(docs_present * 100 / len(DOC_FILES))

    seo_total = len(guides) + len(components) + len(load_projects()) + len(pages)
    seo_ok = sum(1 for g in guides if g.get("meta_description"))
    seo_ok += sum(1 for c in components if c.get("summary"))
    seo_ok += sum(1 for p in load_projects() if p.get("description"))
    seo_ok += sum(1 for p in pages.values() if p.get("meta_description"))
    seo_score = int(seo_ok * 100 / max(1, seo_total))

    image_refs = _collect_image_refs()
    refs_with_url = [r for r in image_refs if r.get("url")]
    alt_ok = sum(1 for r in refs_with_url if str(r.get("alt") or "").strip())
    accessibility_score = int(alt_ok * 100 / max(1, len(refs_with_url)))

    readiness_parts = [build_score, content_score, asset_score, documentation_score, seo_score, accessibility_score]
    readiness_penalty = min(30, link_issues * 2 + image_warn_count)
    overall_readiness = max(0, int(sum(readiness_parts) / len(readiness_parts)) - readiness_penalty)

    return {
        "overall_build": build_score,
        "overall_content": content_score,
        "overall_assets": asset_score,
        "overall_documentation": documentation_score,
        "overall_seo": seo_score,
        "overall_accessibility": accessibility_score,
        "overall_readiness": overall_readiness,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_latest_build_md(build_report: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    counts = build_report["generated_pages"]
    lines = [
        "# Latest Build Report",
        "",
        f"Generated: {build_report['generated_at']}",
        "",
        "## Build Status",
        "",
        build_report["status"],
        "",
        "## Generated Pages",
        "",
        f"- Components: {counts['components']}",
        f"- Guides: {counts['guides']}",
        f"- Projects: {counts['projects']}",
        f"- Static pages: {counts['static_pages']}",
        f"- Search index entries: {counts['search_index_entries']}",
        f"- Sitemap URLs: {counts['sitemap_urls']}",
        f"- Feed items: {counts['feed_items']}",
        "",
        f"## Build Time",
        "",
        f"{build_report['build_time_seconds']}s",
        "",
        f"## Warnings ({len(build_report['warnings'])})",
        "",
    ]
    if build_report["warnings"]:
        lines.extend(f"- {w}" for w in build_report["warnings"][:50])
        if len(build_report["warnings"]) > 50:
            lines.append(f"- … and {len(build_report['warnings']) - 50} more")
    else:
        lines.append("- None")
    lines.extend(["", f"## Errors ({len(build_report['errors'])})", ""])
    if build_report["errors"]:
        lines.extend(f"- {e}" for e in build_report["errors"])
    else:
        lines.append("- None")
    lines.extend(["", "## Quality Scores", ""])
    for key, value in build_report["quality"].items():
        label = key.replace("_", " ").title()
        lines.append(f"- {label}: {value}/100")
    (REPORTS_DIR / "latest-build.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_release_checklist(
    build_report: dict,
    link_report: dict,
    dashboard: dict,
    quality: dict,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    link_ok = sum(link_report["summary"].values()) == 0
    content_ok = len(build_report.get("content_validation_warnings") or []) == 0
    image_ok = len(build_report.get("image_validation_warnings") or []) == 0
    build_ok = build_report["status"] == "PASS"
    readiness_ok = quality.get("overall_readiness", 0) >= 80

    def box(ok: bool) -> str:
        return "[x]" if ok else "[ ]"

    lines = [
        "# Release Checklist",
        "",
        f"Generated: {build_report['generated_at']}",
        "",
        "Complete these checks before production deployment.",
        "",
        "## Build",
        "",
        f"- {box(build_ok)} Static build passes (`py tools/build_all.py`)",
        f"- {box(build_ok)} No build errors",
        f"- {box(len(build_report['warnings']) == 0)} Zero build warnings",
        "",
        "## Content",
        "",
        f"- {box(content_ok)} Mission guides pass content validation",
        f"- {box(dashboard['mission_count'] >= 1)} At least one published mission",
        f"- {box(dashboard['reference_guides'] >= 1)} Reference guides available",
        f"- {box(dashboard['projects']['completed'] >= 1)} Golden projects built",
        "",
        "## Assets",
        "",
        f"- {box(len(dashboard['missing_wiring_diagrams']) == 0)} Wiring diagrams present for missions",
        f"- {box(len(dashboard['missing_photos']) == 0)} Component photos present",
        f"- {box(len(dashboard['missing_pinouts']) == 0)} Component pinouts documented",
        f"- {box(image_ok)} Image validation warnings resolved",
        "",
        "## Links & SEO",
        "",
        f"- {box(link_ok)} No broken internal links",
        f"- {box(link_report['summary']['duplicate_urls'] == 0)} No duplicate sitemap URLs",
        f"- {box(link_report['summary']['unused_pages'] == 0)} No orphan HTML pages",
        f"- {box(quality.get('overall_seo', 0) >= 90)} SEO score ≥ 90",
        "",
        "## Documentation",
        "",
        f"- {box(quality.get('overall_documentation', 0) >= 90)} Editorial and engineering docs present",
        "",
        "## Accessibility",
        "",
        f"- {box(quality.get('overall_accessibility', 0) >= 80)} Alt text coverage ≥ 80%",
        "",
        "## Overall Readiness",
        "",
        f"- {box(readiness_ok)} Overall readiness score ≥ 80 ({quality.get('overall_readiness', 0)}/100)",
        "",
        "## Manual verification (human)",
        "",
        "- [ ] Spot-check Mission 01 on mobile (375px width)",
        "- [ ] Verify analytics ID in `content/site.yaml`",
        "- [ ] Confirm DNS points to current static host",
        "- [ ] Review staging vs production content parity",
        "",
    ]
    (REPORTS_DIR / "RELEASE_CHECKLIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_release_readiness(build_meta: dict) -> dict:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    content_errors = validate_content()
    link_report = check_links()
    content_warnings = content_validation_warnings()
    image_warnings = image_validation_warnings()
    dashboard = build_content_dashboard()
    page_counts = count_build_artifacts()

    flat_warnings: list[str] = []
    for w in content_warnings:
        flat_warnings.append(f"{w['type']}: {w['source']}")
    for w in image_warnings:
        flat_warnings.append(f"{w['type']}: {w['source']} ({w.get('url', w.get('field', ''))})")
    for category, items in link_report.items():
        if category == "summary" or not isinstance(items, list):
            continue
        for item in items[:20]:
            flat_warnings.append(f"link:{category}: {item}")

    status = build_meta.get("status", "PASS")
    if content_errors:
        status = "FAIL"

    quality = compute_quality_scores(
        status,
        link_report,
        content_warnings,
        image_warnings,
        dashboard,
        content_errors,
    )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    build_report = {
        "generated_at": generated_at,
        "status": status,
        "build_time_seconds": build_meta.get("duration_seconds", 0),
        "steps": build_meta.get("steps", []),
        "generated_pages": page_counts,
        "errors": content_errors,
        "warnings": flat_warnings,
        "content_validation_warnings": content_warnings,
        "image_validation_warnings": image_warnings,
        "link_check": link_report,
        "quality": quality,
    }

    _write_json(ROOT / "build-report.json", build_report)
    _write_json(ROOT / "content-dashboard.json", dashboard)
    write_latest_build_md(build_report)
    write_release_checklist(build_report, link_report, dashboard, quality)

    print("\n=== release_readiness.py ===")
    print(f"Build report: build-report.json, docs/reports/latest-build.md")
    print(f"Content dashboard: content-dashboard.json")
    print(f"Release checklist: docs/reports/RELEASE_CHECKLIST.md")
    print(f"Overall readiness: {quality['overall_readiness']}/100")
    print(f"Warnings: {len(flat_warnings)} | Errors: {len(content_errors)}")

    return build_report


if __name__ == "__main__":
    run_release_readiness({"status": "PASS", "duration_seconds": 0, "steps": []})
