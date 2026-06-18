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
RFC_DATE = format_datetime(datetime.now(timezone.utc), usegmt=True)


def feed_item(parent: dict) -> str:
    link = f"{SITE_DOMAIN}/projects/{parent['slug']}.html"
    title = esc(parent["title"])
    desc = esc(parent["description"])
    return f"""    <item>
      <title>{title}</title>
      <link>{html.escape(link)}</link>
      <guid isPermaLink="true">{html.escape(link)}</guid>
      <description>{desc}</description>
      <pubDate>{RFC_DATE}</pubDate>
      <category>{esc(parent["category"])}</category>
    </item>"""


def main():
    items = "\n".join(feed_item(p) for p in PARENTS)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(SITE_NAME)}</title>
    <link>{SITE_DOMAIN}/</link>
    <description>Latest ESP32 project tutorials with wiring guides, Arduino code, and three skill levels.</description>
    <language>en-us</language>
    <lastBuildDate>{RFC_DATE}</lastBuildDate>
{items}
  </channel>
</rss>
"""
    FEED_OUT.write_text(xml, encoding="utf-8")
    print(f"Wrote feed.xml ({len(PARENTS)} items)")


if __name__ == "__main__":
    main()
