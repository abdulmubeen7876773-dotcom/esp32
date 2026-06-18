import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import INDEXNOW_KEY, SITE_DOMAIN

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
KEY_FILE = ROOT / f"{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def write_key_file() -> None:
    KEY_FILE.write_text(INDEXNOW_KEY + "\n", encoding="utf-8")


def sitemap_urls(limit: int = 200) -> list[str]:
    if not SITEMAP.exists():
        return [SITE_DOMAIN + "/"]
    root = ET.parse(SITEMAP).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for loc in root.findall(".//sm:loc", ns):
        if loc.text:
            urls.append(loc.text.strip())
    if not urls:
        for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            if loc.text:
                urls.append(loc.text.strip())
    return urls[:limit]


def ping(urls: list[str]) -> bool:
    if not urls:
        print("IndexNow: no URLs to submit")
        return False
    host = SITE_DOMAIN.replace("https://", "").replace("http://", "").rstrip("/")
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_DOMAIN}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow: submitted {len(urls)} URLs (HTTP {resp.status})")
            return True
    except urllib.error.HTTPError as e:
        print(f"IndexNow: HTTP {e.code} — {e.read().decode('utf-8', errors='replace')[:200]}")
    except Exception as e:
        print(f"IndexNow: skipped — {e}")
    return False


def main():
    write_key_file()
    urls = sitemap_urls()
    ping(urls)


if __name__ == "__main__":
    main()
