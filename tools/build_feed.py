import html
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parent_registry import PARENTS
from site_layout import SITE_DOMAIN, SITE_NAME, esc

ROOT = Path(__file__).resolve().parent.parent
FEED_OUT = ROOT / "feed.xml"
FALLBACK_DATE = datetime(2026, 6, 14, 12, 0, 0, tzinfo=timezone.utc)


def project_pub_date(parent: dict) -> datetime:
    raw = (parent.get("date_modified") or parent.get("date_published") or "").strip()
    if not raw:
        return FALLBACK_DATE
    try:
        if "T" in raw:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        else:
            dt = datetime.strptime(raw[:10], "%Y-%m-%d").replace(
                hour=12, minute=0, second=0, tzinfo=timezone.utc
            )
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return FALLBACK_DATE


def rfc_date(dt: datetime) -> str:
    return format_datetime(dt, usegmt=True)


def feed_item(parent: dict) -> str:
    link = f"{SITE_DOMAIN}/projects/{parent['slug']}.html"
    title = esc(parent["title"])
    desc = esc(parent["description"])
    pub = rfc_date(project_pub_date(parent))
    return f"""    <item>
      <title>{title}</title>
      <link>{html.escape(link)}</link>
      <guid isPermaLink="true">{html.escape(link)}</guid>
      <description>{desc}</description>
      <pubDate>{pub}</pubDate>
      <category>{esc(parent["category"])}</category>
    </item>"""


def main():
    ordered = sorted(PARENTS, key=lambda p: p.get("slug", ""))
    last_build = max((project_pub_date(p) for p in ordered), default=FALLBACK_DATE)
    items = "\n".join(feed_item(p) for p in ordered)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(SITE_NAME)}</title>
    <link>{SITE_DOMAIN}/</link>
    <description>Latest ESP32 project tutorials with wiring guides, Arduino code, and three skill levels.</description>
    <language>en-us</language>
    <lastBuildDate>{rfc_date(last_build)}</lastBuildDate>
{items}
  </channel>
</rss>
"""
    FEED_OUT.write_text(xml, encoding="utf-8")
    print(f"Wrote feed.xml ({len(ordered)} items)")


if __name__ == "__main__":
    main()
