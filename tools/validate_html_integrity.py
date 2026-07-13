from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "_archive", "playwright-report", "test-results"}
HEADING_RE = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.I | re.S)
ID_RE = re.compile(r"\sid=[\"']([^\"']+)[\"']", re.I)
EMPTY_LINK_RE = re.compile(r"<a\b(?=[^>]*href=)[^>]*>\s*</a>", re.I | re.S)
EMPTY_BUTTON_RE = re.compile(r"<button\b(?![^>]*aria-label=)[^>]*>\s*</button>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", html)).strip()


def html_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*.html")
        if not any(part in SKIP_PARTS for part in path.parts)
    ]


def main() -> int:
    errors: list[str] = []
    for path in html_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if path.name.startswith(("google", "pinterest")):
            continue
        ids = ID_RE.findall(text)
        duplicates = sorted({id_ for id_ in ids if ids.count(id_) > 1})
        for id_ in duplicates:
            errors.append(f"{rel}: duplicate id {id_!r}")
        if EMPTY_LINK_RE.search(text):
            errors.append(f"{rel}: empty link with href")
        if EMPTY_BUTTON_RE.search(text):
            errors.append(f"{rel}: empty button")
        if '<link rel="canonical"' not in text and rel.name != "404.html":
            errors.append(f"{rel}: missing canonical link")
        h1_count = len(re.findall(r"<h1\b", text, re.I))
        if rel.name != "404.html" and h1_count != 1:
            errors.append(f"{rel}: expected exactly one H1, found {h1_count}")
        for _, heading_html in HEADING_RE.findall(text):
            words = re.findall(r"[A-Za-z]+", strip_tags(heading_html).lower())
            for left, right in zip(words, words[1:]):
                if left == right and len(left) > 2 and left not in {"review", "display"}:
                    errors.append(f"{rel}: repeated heading word {left!r}")
                    break
    if errors:
        print("HTML integrity validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("HTML integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
