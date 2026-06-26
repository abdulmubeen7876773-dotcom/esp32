import json
import socket
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB_PAGES_HINTS = ("185.199.", "185.199")
LEGACY_AWS_STAGING_IP = "16.192.62.20"
STAGING_HOST = "stg.esp32engine.com"
PRODUCTION_HOST = "esp32engine.com"
STAGING_MARKER_OLD = "Premium ESP32"
STAGING_MARKER_NEW = "Build Amazing Things with ESP32"
GITHUB_IO_CNAME = "abdulmubeen7876773-dotcom.github.io"


def _resolve_ipv4(host: str) -> list[str]:
    try:
        return sorted({item[4][0] for item in socket.getaddrinfo(host, None, socket.AF_INET)})
    except socket.gaierror:
        return []


def _fetch_title(host: str) -> str:
    url = f"https://{host}/"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            html = response.read(80000).decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return ""
    for line in html.splitlines():
        lower = line.lower()
        if "<title" in lower:
            start = line.lower().find("<title")
            end = line.lower().find("</title>")
            if end > start:
                return line[start:end].split(">", 1)[-1].strip()
    return ""


def check_staging_dns() -> dict:
    staging_ips = _resolve_ipv4(STAGING_HOST)
    production_ips = _resolve_ipv4(PRODUCTION_HOST)
    staging_title = _fetch_title(STAGING_HOST)
    production_title = _fetch_title(PRODUCTION_HOST)

    staging_on_github_pages = any(ip.startswith(GITHUB_PAGES_HINTS) for ip in staging_ips)
    staging_on_legacy_aws = LEGACY_AWS_STAGING_IP in staging_ips
    staging_serves_old = STAGING_MARKER_OLD in staging_title
    staging_serves_new = STAGING_MARKER_NEW in staging_title

    warnings: list[str] = []
    errors: list[str] = []

    if staging_on_legacy_aws:
        errors.append(
            f"{STAGING_HOST} resolves to legacy AWS host {LEGACY_AWS_STAGING_IP} — not GitHub Pages."
        )
    if not staging_on_github_pages:
        warnings.append(
            f"{STAGING_HOST} does not resolve to GitHub Pages ({', '.join(staging_ips) or 'no A record'})."
        )
    if staging_serves_old:
        errors.append(f"{STAGING_HOST} is still serving the pre-mission static snapshot.")
    if production_title and STAGING_MARKER_NEW not in production_title:
        warnings.append(f"{PRODUCTION_HOST} title does not match the current mission-based build.")

    return {
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "staging_host": STAGING_HOST,
        "production_host": PRODUCTION_HOST,
        "staging_ips": staging_ips,
        "production_ips": production_ips,
        "recommended_staging_cname": GITHUB_IO_CNAME,
        "staging_on_github_pages": staging_on_github_pages,
        "staging_on_legacy_aws": staging_on_legacy_aws,
        "staging_title": staging_title,
        "production_title": production_title,
        "staging_serves_old_build": staging_serves_old,
        "staging_serves_new_build": staging_serves_new,
        "warnings": warnings,
        "errors": errors,
    }


def main() -> int:
    result = check_staging_dns()
    print(json.dumps(result, indent=2))
    for warning in result["warnings"]:
        print(f"::warning::{warning}")
    for error in result["errors"]:
        print(f"::error::{error}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
