import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "legacy"))

from cms_loader import COMPONENTS_DIR, GUIDES_DIR, PROJECTS_DIR, load_yaml, save_yaml
from parse_archive_html import parse_archive_page
from parse_batch_php import parse_batch_file

BATCH_DIR = Path(
    r"C:/Users/HP/Documents/Codex/2026-06-24/he/work/esp32engine-theme"
)
SQL_PATH = BATCH_DIR / "esp32engine_local_20260622_2349.sql"
ARCHIVE = ROOT / "projects" / "_archive"
REPORT_PATH = ROOT / "docs" / "reports" / "LEGACY_IMPORT_SUMMARY.md"

SLUG_ALIASES = {
    "esp32-rfid-access-control": "esp32-rfid-access-control-system",
    "esp32-security-camera": "esp32-security-camera-system",
    "esp32-greenhouse-controller": "esp32-greenhouse-automation-controller",
    "esp32-lora-remote-sensor": "esp32-lora-remote-sensor-node",
}

CATEGORY_MAP = {
    "home-automation": "Home Automation",
    "iot-projects": "IoT Projects",
    "iot": "IoT Projects",
    "sensor-projects": "Sensor Projects",
    "sensor": "Sensor Projects",
    "security": "Security Projects",
    "robotics": "Robotics",
    "esp32-cam": "ESP32-CAM",
    "ai-projects": "AI Projects",
    "ai": "AI Projects",
    "environment": "Environmental",
    "environmental": "Environmental",
    "agriculture": "Agriculture",
    "healthcare": "Healthcare",
    "industrial": "Industrial Automation",
    "led-projects": "LED Projects",
    "led": "LED Projects",
    "smart-city": "Smart City",
    "energy-monitoring": "Energy Monitoring",
    "energy": "Energy Monitoring",
    "education": "Education",
}

TIER1 = [
    "esp32-iot-weather-station",
    "esp32-smart-irrigation-system",
    "esp32-motion-security-alert",
    "esp32-distance-monitoring-system",
    "esp32-home-climate-automation",
    "esp32-air-quality-monitor",
    "esp32-learning-trainer",
    "esp32-tinyml-sound-classifier",
    "esp32-machine-monitoring-node",
    "esp32-camera-capture-server",
    "esp32-smart-energy-meter",
    "esp32-pulse-oximeter-logger",
    "esp32-wifi-robot-controller",
    "esp32-rgb-led-pattern-controller",
    "esp32-smart-street-light",
]

TIER2 = [
    "esp32-smart-thermostat",
    "esp32-rfid-access-control-system",
    "esp32-soil-moisture-monitor",
    "esp32-mqtt-sensor-dashboard",
    "esp32-neopixel-music-visualizer",
    "esp32-line-following-robot",
    "esp32-smart-door-lock",
    "esp32-gps-tracker",
    "esp32-oled-weather-clock",
    "esp32-vibration-monitor",
    "esp32-cam-face-detection",
    "esp32-cam-qr-scanner",
    "esp32-gesture-recognition",
    "esp32-ecg-monitor",
    "esp32-ble-beacon",
    "esp32-fire-alarm-system",
    "esp32-smart-parking-sensor",
    "esp32-soil-ph-monitor",
    "esp32-cnc-controller",
    "esp32-smart-mailbox",
    "esp32-voice-controlled-relay",
    "esp32-ir-remote-control",
]

TIER3 = [
    "esp32-smart-power-strip",
    "esp32-water-leak-detector",
    "esp32-ac-power-monitor",
    "esp32-ai-object-detector",
    "esp32-uv-index-monitor",
    "esp32-led-matrix-display",
]

TIER4 = [
    "esp32-greenhouse-automation-controller",
    "esp32-security-camera-system",
    "esp32-robot-arm-controller",
    "esp32-lora-remote-sensor-node",
    "esp32-rfid-inventory-tracker",
    "esp32-lightning-detector",
    "esp32-digital-piano",
]

WP_GUIDES = ["debouncing-buttons-esp32", "digital-outputs-esp32"]

stats = {
    "projects_imported": 0,
    "projects_enriched": 0,
    "guides_imported": 0,
    "guides_enriched": 0,
    "components_enriched": 0,
    "skipped": [],
    "merges": [],
    "missing_assets": [],
    "needs_polish": [],
}


def canonical_slug(slug: str) -> str:
    return SLUG_ALIASES.get(slug, slug)


def map_category(raw: str) -> str:
    if not raw:
        return "TODO: category"
    key = raw.strip().lower().replace(" ", "-")
    if raw in CATEGORY_MAP.values():
        return raw
    return CATEGORY_MAP.get(key, raw.replace("-", " ").title())


def wiring_to_hardware(wiring: list[dict]) -> dict:
    sensor_pin = "TODO: sensor_pin"
    output_pin = "TODO: output_pin"
    sensor_name = "TODO: sensor"
    output_name = "TODO: output"
    hw_wiring = []
    for row in wiring:
        comp = row.get("component", "")
        pin = row.get("pin", "")
        hw_wiring.append({"component": comp, "pin": pin})
        low = comp.lower()
        if "gnd" in low or pin.upper() == "GND":
            continue
        if "vcc" in low or "vin" in low or "3.3" in pin or "5v" in pin.lower():
            continue
        if "sda" in low or "scl" in low or "i2c" in low:
            continue
        if "gpio" in pin.lower() and sensor_pin.startswith("TODO"):
            if any(k in low for k in ("sensor", "dht", "mq", "pir", "hc-sr", "mic", "gps", "temp", "humid", "soil", "ph", "uv", "vibrat", "leak", "smoke", "gas", "pressure", "pulse", "ecg", "gesture", "rfid", "reed", "ldr", "light", "sound", "inmp", "max301", "mpu", "ad823", "as3935", "guva")):
                sensor_pin = pin
                sensor_name = comp
            elif output_pin.startswith("TODO"):
                output_pin = pin
                output_name = comp
        elif "gpio" in pin.lower() and output_pin.startswith("TODO"):
            output_pin = pin
            output_name = comp
    return {
        "sensor_pin": sensor_pin,
        "output_pin": output_pin,
        "sensor_name": sensor_name,
        "output_name": output_name,
        "wiring": hw_wiring,
    }


def level_to_build(level: str, data: dict) -> dict:
    wiring_rows = []
    for row in data.get("wiring") or []:
        wiring_rows.append((row["component"], row["pin"], row.get("note") or ""))
    trouble = []
    for row in data.get("troubleshooting") or []:
        if isinstance(row, dict):
            trouble.append((row.get("problem", ""), row.get("fix") or row.get("solution", "")))
    return {
        "level": level,
        "overview_html": data.get("overview_html") or "",
        "components": data.get("components") or [],
        "wiring": wiring_rows,
        "how": data.get("how") or [],
        "apps": data.get("apps") or [],
        "troubleshooting": trouble,
        "upgrades": data.get("upgrades") or [],
        "code": data.get("code") or "",
        "code_filename": data.get("code_filename") or "",
    }


def load_batch_index() -> dict[str, dict]:
    index: dict[str, dict] = {}
    if not BATCH_DIR.exists():
        stats["skipped"].append(f"Batch directory missing: {BATCH_DIR}")
        return index
    for path in sorted(BATCH_DIR.glob("projects-data-batch*.php")):
        for proj in parse_batch_file(path):
            slug = canonical_slug(proj["slug"])
            if slug in index:
                stats["merges"].append(
                    f"{slug}: kept batch from {path.name}, dropped duplicate slug {proj['slug']}"
                )
            else:
                index[slug] = proj
    return index


def find_archive_html(source_base: str) -> Path | None:
    if ARCHIVE.exists():
        matches = sorted(ARCHIVE.glob(f"{source_base}-project-*.html"))
        if matches:
            return matches[0]
    matches = sorted((ROOT / "projects").glob(f"{source_base}-project-*.html"))
    return matches[0] if matches else None


def enrich_tier1(existing: dict) -> dict:
    slug = existing["slug"]
    if existing.get("format") == "golden":
        existing.setdefault("quality_status", "golden")
        existing.setdefault("status", "complete")
        stats["projects_enriched"] += 1
        stats["needs_polish"].append(f"{slug} (golden — no legacy overlay)")
        return existing

    source_base = existing.get("source_base", "")
    archive = find_archive_html(source_base) if source_base else None
    if not archive:
        stats["missing_assets"].append(f"{slug}: no archive HTML for source_base={source_base}")
        existing["quality_status"] = "legacy_import"
        existing["status"] = "needs_polish"
        existing.setdefault("import_tier", 1)
        if not existing.get("meta_description"):
            existing["meta_description"] = "TODO: meta_description"
        stats["projects_enriched"] += 1
        stats["needs_polish"].append(slug)
        return existing

    parsed = parse_archive_page(archive)
    levels = existing.get("levels") or {}
    beginner = level_to_build(
        "beginner",
        {
            "overview_html": parsed.get("overview_html") or f"<p>{parsed.get('lead', '')}</p>",
            "components": parsed.get("components") or [],
            "wiring": parsed.get("wiring") or [],
            "code": parsed.get("code") or "",
            "how": [],
            "apps": parsed.get("apps") or [],
            "troubleshooting": [],
            "upgrades": parsed.get("upgrades") or [],
        },
    )
    if beginner["code"]:
        levels["beginner"] = beginner
    for lv in ("intermediate", "advanced"):
        if lv not in levels:
            levels[lv] = {"overview_html": f"<p>TODO: import {lv} content from batch or WordPress</p>", "code": ""}

    if parsed.get("wiring"):
        hw = wiring_to_hardware(parsed["wiring"])
        existing["hardware"] = {**existing.get("hardware", {}), **hw}
    elif existing.get("hardware", {}).get("wiring"):
        levels["beginner"]["wiring"] = [
            (r.get("component", ""), r.get("pin", ""), "")
            for r in existing["hardware"]["wiring"]
            if isinstance(r, dict)
        ]

    if parsed.get("meta_description"):
        existing["meta_description"] = parsed["meta_description"]
    if parsed.get("meta_title"):
        existing["meta_title"] = parsed["meta_title"]
    if parsed.get("category") and parsed["category"] not in ("ESP32", ""):
        existing["category"] = map_category(parsed["category"])

    existing["levels"] = levels
    existing["quality_status"] = "legacy_import"
    existing["status"] = "needs_polish"
    existing["import_tier"] = 1
    existing["import_source"] = archive.name
    stats["projects_enriched"] += 1
    stats["needs_polish"].append(slug)
    return existing


def project_from_batch(batch: dict, tier: int) -> dict:
    slug = canonical_slug(batch["slug"])
    wiring = batch["levels"].get("beginner", {}).get("wiring") or []
    hw = wiring_to_hardware(wiring)
    levels = {}
    for lv, data in batch.get("levels", {}).items():
        levels[lv] = level_to_build(lv, data)

    sensor = hw.get("sensor_name", "TODO: sensor")
    output = hw.get("output_name", "TODO: output")
    return {
        "slug": slug,
        "title": batch.get("title") or slug,
        "category": map_category(batch.get("category", "")),
        "description": batch.get("lead") or batch.get("meta_description") or "TODO: description",
        "meta_description": batch.get("meta_description") or "TODO: meta_description",
        "source_base": f"{slug}-legacy-import",
        "sensor": sensor,
        "output": output,
        "featured": False,
        "date_published": "2026-06-14",
        "date_modified": str(date.today()),
        "quality_status": "legacy_import",
        "status": "needs_polish",
        "import_tier": tier,
        "import_source": "batch-php",
        "hardware": hw,
        "levels": levels,
        "related_slugs": batch.get("related") or [],
    }


def extract_wp_posts(sql_text: str) -> dict[str, dict]:
    posts: dict[str, dict] = {}
    if not sql_text:
        return posts
    for slug in WP_GUIDES:
        idx = sql_text.find(f"'{slug}'")
        if idx == -1:
            stats["skipped"].append(f"Guide {slug} not found in SQL dump")
            continue
        window = sql_text[max(0, idx - 2000) : idx + 120000]
        title_m = re.search(r",'" + re.escape(slug) + r"',[^,]*,[^,]*,'((?:\\'|[^'])*)'", window)
        content_m = re.search(r"'post_content','((?:\\'|[^'])*)'", window)
        if not content_m:
            content_m = re.search(r"post_content','((?:\\'|[^'])*)'", window)
        if content_m:
            body = content_m.group(1).replace("\\'", "'").replace("\\r\\n", "\n").replace("\\n", "\n")
            title = title_m.group(1).replace("\\'", "'") if title_m else slug.replace("-", " ").title()
            posts[slug] = {"post_name": slug, "title": title, "body_html": body}
        else:
            stats["skipped"].append(f"Guide {slug}: post_content not extracted from SQL window")
    return posts


def import_wp_guides(posts: dict[str, dict]) -> None:
    for slug in WP_GUIDES:
        post = posts.get(slug)
        path = GUIDES_DIR / f"{slug}.yaml"
        if path.exists():
            stats["guides_enriched"] += 1
            continue
        if not post or not post.get("body_html"):
            stats["skipped"].append(f"Guide {slug}: no SQL body extracted")
            continue
        guide = {
            "slug": slug,
            "title": f"{post.get('title', slug)} | ESP32 Engine",
            "headline": post.get("title", slug),
            "meta_description": "TODO: meta_description from WordPress excerpt",
            "sort_order": 10,
            "quality_status": "legacy_import",
            "status": "needs_polish",
            "import_source": "wordpress-sql",
            "body_html": post["body_html"],
        }
        save_yaml(path, guide)
        stats["guides_imported"] += 1
        stats["needs_polish"].append(f"guide:{slug}")


def enrich_components() -> None:
    for path in sorted(COMPONENTS_DIR.glob("*.yaml")):
        data = load_yaml(path) or {}
        slug = data.get("slug", path.stem)
        if slug == "dht22":
            data.setdefault("quality_status", "golden")
            data.setdefault("status", "complete")
        else:
            data.setdefault("quality_status", "legacy_import")
            data.setdefault("status", "needs_polish")
            stats["needs_polish"].append(f"component:{slug}")
        if not data.get("image") or str(data.get("image", "")).startswith("TODO"):
            stats["missing_assets"].append(f"component:{slug}: featured image")
        save_yaml(path, data)
        stats["components_enriched"] += 1


def enrich_guides() -> None:
    for path in sorted(GUIDES_DIR.glob("*.yaml")):
        data = load_yaml(path) or {}
        slug = data.get("slug", path.stem)
        if data.get("format") == "mission" or data.get("mission"):
            data.setdefault("quality_status", "golden")
            data.setdefault("status", "complete")
        else:
            data.setdefault("quality_status", "legacy_import")
            data.setdefault("status", "needs_polish")
            stats["needs_polish"].append(f"guide:{slug}")
        save_yaml(path, data)
        stats["guides_enriched"] += 1


def write_report() -> None:
    lines = [
        "# Legacy Import Summary",
        "",
        f"**Date:** {date.today()}",
        f"**Source plan:** `D:/jsnjd/docs/reports/CONTENT_MIGRATION_PLAN.md`",
        "",
        "## Counts",
        "",
        f"| Metric | Count |",
        f"|--------|------:|",
        f"| Projects imported (new YAML) | {stats['projects_imported']} |",
        f"| Projects enriched (existing) | {stats['projects_enriched']} |",
        f"| Guides imported (new YAML) | {stats['guides_imported']} |",
        f"| Guides enriched (metadata) | {stats['guides_enriched']} |",
        f"| Components enriched (metadata) | {stats['components_enriched']} |",
        "",
        "## Skipped items",
        "",
    ]
    if stats["skipped"]:
        for item in stats["skipped"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.extend(["", "## Duplicate merges", ""])
    if stats["merges"]:
        for item in stats["merges"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.extend(["", "## Missing assets", ""])
    for item in stats["missing_assets"][:50]:
        lines.append(f"- {item}")
    if len(stats["missing_assets"]) > 50:
        lines.append(f"- … and {len(stats['missing_assets']) - 50} more")
    lines.extend(["", "## Items needing polish", ""])
    for item in stats["needs_polish"][:80]:
        lines.append(f"- {item}")
    if len(stats["needs_polish"]) > 80:
        lines.append(f"- … and {len(stats['needs_polish']) - 80} more")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    batch_index = load_batch_index()
    sql_text = SQL_PATH.read_text(encoding="utf-8", errors="replace") if SQL_PATH.exists() else ""
    if not SQL_PATH.exists():
        stats["skipped"].append(f"SQL dump missing: {SQL_PATH}")

    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        data = load_yaml(path) or {}
        slug = data.get("slug", path.stem)
        if slug in TIER1:
            save_yaml(path, enrich_tier1(data))

    existing_slugs = {p.stem for p in PROJECTS_DIR.glob("*.yaml")}

    def import_tier(slugs: list[str], tier: int) -> None:
        nonlocal existing_slugs
        for slug in slugs:
            if slug in existing_slugs:
                continue
            batch = batch_index.get(slug)
            if batch:
                out = project_from_batch(batch, tier)
                save_yaml(PROJECTS_DIR / f"{slug}.yaml", out)
                existing_slugs.add(slug)
                stats["needs_polish"].append(slug)
            elif tier >= 4 and sql_text:
                stats["skipped"].append(f"{slug}: Tier {tier} — no batch data, SQL body not extracted yet")
            else:
                stats["skipped"].append(f"{slug}: no batch data found")

    import_tier(TIER2, 2)
    import_tier(TIER3, 3)
    import_tier(TIER4, 4)

    wp_posts = extract_wp_posts(sql_text)
    import_wp_guides(wp_posts)
    enrich_guides()
    enrich_components()
    stats["projects_imported"] = len(
        [s for s in {p.stem for p in PROJECTS_DIR.glob("*.yaml")} if s not in set(TIER1)]
    )
    write_report()

    print(f"Projects imported: {stats['projects_imported']}")
    print(f"Projects enriched: {stats['projects_enriched']}")
    print(f"Guides imported: {stats['guides_imported']}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
