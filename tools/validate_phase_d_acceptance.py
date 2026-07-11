from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

PLACEHOLDER_RE = re.compile(
    r"\b(coming soon|resource coming soon|lesson plans coming soon|worksheets coming soon|"
    r"classroom packs coming soon|download available soon)\b",
    re.I,
)

FUTURE_PROMISE_RE = re.compile(
    r"\b(will be grouped here|as the resource library grows|available soon)\b",
    re.I,
)

VERIFICATION_PAGES = {
    "google926bc78bc682aaf9.html",
    "googlec0cbd82255f45946.html",
    "pinterest-f71bc.html",
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = dict(attrs)
        href = values.get("href")
        if href:
            self.hrefs.append(href)


def route_exists(href: str) -> bool:
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:")):
        return True
    if href == "/":
        return (ROOT / "index.html").exists()
    if href.startswith("/"):
        path = ROOT / href.lstrip("/")
    else:
        path = ROOT / href
    if path.is_dir():
        path = path / "index.html"
    return path.exists()


def public_html_pages() -> list[Path]:
    pages = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or "_archive" in rel.parts or path.name in VERIFICATION_PAGES:
            continue
        pages.append(path)
    return pages


def main() -> int:
    errors: list[str] = []

    teachers = ROOT / "teachers.html"
    if not teachers.exists():
        errors.append("teachers.html is missing; rebuild static pages.")
    else:
        html = teachers.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_RE.search(html):
            errors.append("teachers.html contains visible Coming Soon placeholder wording.")
        if FUTURE_PROMISE_RE.search(html):
            errors.append("teachers.html contains future-resource promise wording instead of usable resources.")
        parser = LinkParser()
        parser.feed(html)
        for href in parser.hrefs:
            if not route_exists(href):
                errors.append(f"teachers.html CTA/link target missing: {href}")

    for path in public_html_pages():
        html = path.read_text(encoding="utf-8", errors="ignore")
        h1_count = len(re.findall(r"<h1\b", html, re.I))
        if h1_count != 1:
            errors.append(f"{path.relative_to(ROOT)} has {h1_count} H1 elements")

    if errors:
        print("Phase D acceptance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Phase D acceptance validation passed: teachers CTAs, placeholders, and H1s checked across {len(public_html_pages())} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
