import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET

from cms_loader import load_projects
from project_text import is_golden_project

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://esp32engine.com"
PUBLIC_EXCLUDES = {
    ".git",
    ".venv",
    "tmp",
    "docs",
    "tools",
    "assets",
    "content",
    "admin",
    "node_modules",
    "playwright-report",
    "test-results",
    "__pycache__",
}

KNOWN_AFFECTED_URLS = [
    "https://esp32engine.com/category/education.html",
    "https://esp32engine.com/category/environmental.html",
    "https://esp32engine.com/category/esp32-cam.html",
    "https://esp32engine.com/category/healthcare.html",
    "https://esp32engine.com/category/home-automation.html",
    "https://esp32engine.com/category/led-projects.html",
    "https://esp32engine.com/category/robotics.html",
    "https://esp32engine.com/category/security-projects.html",
    "https://esp32engine.com/category/sensor-projects.html",
    "https://esp32engine.com/category/smart-city.html",
    "https://esp32engine.com/disclaimer.html",
    "https://esp32engine.com/guides.html",
    "https://esp32engine.com/guides/what-is-esp32.html",
    "https://esp32engine.com/terms.html",
    "https://esp32engine.com/projects/esp32-air-quality-monitor.html",
    "https://esp32engine.com/projects/esp32-camera-capture-server.html",
    "https://esp32engine.com/projects/esp32-learning-trainer.html",
    "https://esp32engine.com/projects/esp32-machine-monitoring-node.html",
    "https://esp32engine.com/projects/esp32-rfid-inventory-tracker.html",
    "https://esp32engine.com/projects/esp32-smart-energy-meter.html",
    "https://esp32engine.com/projects/esp32-smart-irrigation-system.html",
    "https://esp32engine.com/projects/esp32-smart-street-light.html",
    "https://esp32engine.com/projects/esp32-soil-moisture-monitor.html",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.title = ""
        self.meta_description = ""
        self.robots = ""
        self.canonicals = []
        self.og_urls = []
        self.h1 = []
        self.h1_count = 0
        self.ids = set()
        self.jsonld = []
        self.breadcrumb = False
        self.structured_data = False
        self._tag_stack = []
        self._capture_title = False
        self._capture_h1 = False
        self._capture_jsonld = False
        self._jsonld_buf = []
        self.visible_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self._tag_stack.append(tag)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "title":
            self._capture_title = True
        if tag == "h1":
            self._capture_h1 = True
            self.h1_count += 1
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            prop = (attrs.get("property") or "").lower()
            if name == "description":
                self.meta_description = attrs.get("content", "")
            if name == "robots":
                self.robots = attrs.get("content", "")
            if prop == "og:url":
                self.og_urls.append(attrs.get("content", ""))
        if tag == "link" and (attrs.get("rel") or "").lower() == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs)
        if tag == "nav" and "breadcrumb" in (attrs.get("class") or ""):
            self.breadcrumb = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._capture_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._capture_title = False
        if tag == "h1":
            self._capture_h1 = False
        if tag == "script" and self._capture_jsonld:
            raw = "".join(self._jsonld_buf).strip()
            if raw:
                self.jsonld.append(raw)
                self.structured_data = True
            self._capture_jsonld = False
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._capture_title:
            self.title += data
        if self._capture_h1:
            self.h1.append(data.strip())
        if self._capture_jsonld:
            self._jsonld_buf.append(data)
        if self._tag_stack and self._tag_stack[-1] not in {"script", "style", "noscript"}:
            text = data.strip()
            if text:
                self.visible_text.append(text)


def public_html_pages():
    pages = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if "_archive" in rel.parts or any(part in PUBLIC_EXCLUDES for part in rel.parts):
            continue
        pages.append(rel.as_posix())
    return sorted(pages)


def route_to_page(path: str) -> str:
    path = unquote(path.split("#", 1)[0].split("?", 1)[0]).strip()
    if not path or path == "/":
        return "index.html"
    parsed = urlparse(path)
    if parsed.scheme:
        if parsed.netloc != "esp32engine.com":
            return ""
        path = parsed.path
    path = path.lstrip("/")
    if not path:
        return "index.html"
    if path.endswith("/"):
        return path + "index.html"
    if path.endswith("/index.html"):
        return path
    if not Path(path).suffix:
        return path + "/index.html"
    return os.path.normpath(path).replace("\\", "/")


def page_to_canonical(page: str, parser: PageParser) -> str:
    if parser.canonicals:
        return parser.canonicals[0]
    if page == "index.html":
        return DOMAIN + "/"
    return DOMAIN + "/" + page.replace("index.html", "")


def resolve_link(href: str, source: str) -> str:
    href = href.strip()
    if not href or href.startswith("#"):
        return ""
    parsed = urlparse(href)
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return ""
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc not in {"esp32engine.com", "www.esp32engine.com"}:
            return ""
        return route_to_page(parsed.path)
    if href.startswith("/"):
        return route_to_page(href)
    base = Path(source).parent
    return route_to_page((base / href).as_posix())


def sitemap_urls():
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in tree.findall(".//sm:loc", ns) if el.text]


def project_slug_for_page(page: str) -> str:
    if page.startswith("projects/") and page.endswith(".html"):
        return Path(page).stem
    return ""


def source_for_page(page: str) -> str:
    if page == "index.html":
        return "content/home.yaml"
    if page.startswith("guides/"):
        return f"content/guides/{Path(page).stem}.yaml"
    if page.startswith("components/"):
        return f"content/components/{Path(page).stem}.yaml"
    if page.startswith("projects/"):
        return f"content/projects/{Path(page).stem}.yaml"
    if page.startswith("category/"):
        return "content/categories.yaml"
    return f"content/pages/{Path(page).stem}.yaml"


def is_important(page: str) -> bool:
    return (
        page == "index.html"
        or page in {"projects.html", "guides.html", "components.html", "learning.html", "category/index.html"}
        or page.startswith(("projects/", "guides/", "components/", "category/"))
    )


def main():
    errors = []
    warnings = []
    pages = public_html_pages()
    page_set = set(pages)
    parsed = {}
    inbound = defaultdict(set)
    outbound_counts = Counter()
    broken_links = []
    broken_assets = []

    for page in pages:
        parser = PageParser()
        parser.feed((ROOT / page).read_text(encoding="utf-8", errors="ignore"))
        parsed[page] = parser
        for href in parser.links:
            target = resolve_link(href, page)
            if not target:
                continue
            outbound_counts[page] += 1
            if target in page_set:
                inbound[target].add(page)
            elif target.endswith(".html"):
                broken_links.append((page, href, target))
        for img in parser.images:
            src = img.get("src", "")
            if not src or urlparse(src).scheme:
                continue
            asset = resolve_link(src, page) if src.endswith(".html") else src.lstrip("/")
            if asset and not (ROOT / asset).exists():
                broken_assets.append((page, src))

    titles = Counter(p.title.strip() for p in parsed.values() if p.title.strip())
    descriptions = Counter(p.meta_description.strip() for p in parsed.values() if p.meta_description.strip())
    canonicals = Counter(page_to_canonical(page, p) for page, p in parsed.items())
    sm_urls = sitemap_urls()
    sm_set = set(sm_urls)
    projects = load_projects()
    public_project_slugs = {p["slug"] for p in projects if is_golden_project(p)}
    non_public_project_slugs = {p["slug"] for p in projects if not is_golden_project(p)}

    if len(sm_urls) != len(sm_set):
        errors.append("sitemap contains duplicate URLs")
    for url in sm_urls:
        parsed_url = urlparse(url)
        if parsed_url.scheme != "https" or parsed_url.netloc != "esp32engine.com":
            errors.append(f"sitemap contains non-HTTPS or non-production URL: {url}")
        if parsed_url.query:
            errors.append(f"sitemap contains query-string URL: {url}")
        if parsed_url.path == "/search.html":
            errors.append("sitemap includes search.html")
        if parsed_url.path == "/404.html":
            errors.append("sitemap includes 404.html")
        if parsed_url.path == "/category/index.html":
            errors.append("sitemap includes /category/index.html instead of /category/")
        if any(token in parsed_url.path.lower() for token in ("google", "pinterest", "verification")):
            errors.append(f"sitemap includes verification file: {url}")
        if any(part in parsed_url.path.strip("/").split("/") for part in ("docs", "tools", "test-results", "playwright-report")):
            errors.append(f"sitemap includes non-public report or tool artifact: {url}")
        slug = project_slug_for_page(route_to_page(url))
        if slug in non_public_project_slugs:
            errors.append(f"sitemap includes non-public project: {url}")
        elif slug and slug not in public_project_slugs:
            errors.append(f"sitemap includes unknown project: {url}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8", errors="ignore")
    if f"Sitemap: {DOMAIN}/sitemap.xml" not in robots:
        errors.append("robots.txt does not reference the production sitemap")
    if re.search(r"Disallow:\s*/(guides|category|components)(?:/|\s|$)", robots) or re.search(r"Disallow:\s*/projects(?:\s|$)", robots):
        errors.append("robots.txt blocks important public sections")

    for page, parser in parsed.items():
        important = is_important(page)
        canonical = page_to_canonical(page, parser)
        if important and len(parser.canonicals) != 1:
            errors.append(f"{page}: expected exactly one canonical")
        if important and canonical not in sm_set:
            errors.append(f"{page}: important page missing from sitemap ({canonical})")
        if canonical.startswith("http://") or "www.esp32engine.com" in canonical or "localhost" in canonical:
            errors.append(f"{page}: invalid canonical host or scheme")
        if canonical != DOMAIN + "/" and route_to_page(canonical) != page:
            errors.append(f"{page}: canonical does not resolve to this output file")
        if parser.og_urls and parser.og_urls[0] != canonical:
            errors.append(f"{page}: og:url does not match canonical")
        if important and parser.robots and any(token in parser.robots.lower() for token in ("noindex", "none", "nofollow")):
            errors.append(f"{page}: important page has non-indexable robots meta")
        if important and page != "index.html" and not inbound[page]:
            errors.append(f"{page}: important page has no incoming HTML links")
        if important and not parser.title.strip():
            errors.append(f"{page}: missing title")
        if important and not parser.meta_description.strip():
            errors.append(f"{page}: missing meta description")
        if important and parser.h1_count != 1:
            warnings.append(f"{page}: expected one H1")
        if important and len(" ".join(parser.visible_text).split()) < 120:
            warnings.append(f"{page}: low visible word count")
        if important and page != "index.html" and not parser.breadcrumb:
            warnings.append(f"{page}: missing visible breadcrumb")
        if important and not parser.structured_data:
            warnings.append(f"{page}: missing structured data")
        for raw in parser.jsonld:
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{page}: invalid JSON-LD ({exc})")

    for url in sm_urls:
        page = route_to_page(url)
        if page not in page_set:
            errors.append(f"sitemap URL has no output file: {url}")
            continue
        sitemap_parser = parsed[page]
        canonical = page_to_canonical(page, sitemap_parser)
        if canonical != url:
            errors.append(f"sitemap URL is not self-canonical: {url} (canonical: {canonical})")
        robots_meta = sitemap_parser.robots.lower()
        if any(token in robots_meta for token in ("noindex", "none", "nofollow")):
            errors.append(f"sitemap includes noindex page: {url}")

    for url in KNOWN_AFFECTED_URLS:
        page = route_to_page(url)
        if page not in page_set:
            errors.append(f"affected URL missing output file: {url}")
            continue
        parser = parsed[page]
        canonical = page_to_canonical(page, parser)
        if canonical not in sm_set:
            errors.append(f"affected URL not in sitemap: {url}")
        if "noindex" in parser.robots.lower():
            errors.append(f"affected URL noindex: {url}")
        if page != "index.html" and not inbound[page]:
            errors.append(f"affected URL has no inbound links: {url}")

    if broken_links:
        for page, href, target in broken_links[:50]:
            errors.append(f"{page}: broken internal link {href} -> {target}")
    if broken_assets:
        for page, src in broken_assets[:50]:
            errors.append(f"{page}: broken image asset {src}")

    duplicate_titles = [title for title, count in titles.items() if count > 1 and title]
    duplicate_desc = [desc for desc, count in descriptions.items() if count > 1 and desc]
    duplicate_canonicals = [url for url, count in canonicals.items() if count > 1 and url]
    if duplicate_canonicals:
        errors.append(f"duplicate canonical URLs: {len(duplicate_canonicals)}")
    if duplicate_titles:
        warnings.append(f"duplicate titles: {len(duplicate_titles)}")
    if duplicate_desc:
        warnings.append(f"duplicate meta descriptions: {len(duplicate_desc)}")

    important_orphans = sorted(page for page in pages if is_important(page) and page != "index.html" and not inbound[page])
    sitemap_only = sorted(
        page for page in pages if is_important(page) and page_to_canonical(page, parsed[page]) in sm_set and not inbound[page]
    )

    print("SEO validation")
    print(f"  pages: {len(pages)}")
    print(f"  sitemap URLs: {len(sm_urls)}")
    print(f"  broken links: {len(broken_links)}")
    print(f"  broken assets: {len(broken_assets)}")
    print(f"  important orphans: {len(important_orphans)}")
    print(f"  sitemap-only important pages: {len(sitemap_only)}")
    print(f"  warnings: {len(warnings)}")
    print(f"  errors: {len(errors)}")
    for item in warnings[:25]:
        print(f"  WARN: {item}")
    for item in errors[:80]:
        print(f"  ERROR: {item}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
