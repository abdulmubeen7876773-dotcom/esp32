from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_EXTS = {".html", ".xml", ".json", ".js", ".css", ".py", ".yaml", ".yml", ".md", ".bat"}
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "playwright-report", "test-results"}
MOJIBAKE = [
    "\u00c2",
    "\u00c3",
    "\u00e2\u20ac",
    "\u00e2\u20ac\u2122",
    "\u00e2\u20ac\u0153",
    "\u00e2\u20ac\u009d",
    "\u00e2\u20ac\u201c",
    "\u00e2\u20ac\u201d",
    "\u00e2\u20ac\u00a6",
    "\u00e2\u2020",
    "\u00f0\u0178",
]


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS or part == "_archive" for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTS:
            files.append(path)
    return files


def main() -> int:
    errors: list[str] = []
    for path in iter_text_files():
        raw = path.read_bytes()
        rel = path.relative_to(ROOT)
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel}: UTF-8 BOM found")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not valid UTF-8 ({exc})")
            continue
        for pattern in MOJIBAKE:
            if pattern in text:
                errors.append(f"{rel}: suspicious mojibake sequence {pattern!r}")
        if path.suffix.lower() == ".html":
            if path.name.startswith(("google", "pinterest")):
                continue
            head_start = text.lower().find("<head")
            charset_pos = text.lower().find('<meta charset="utf-8"')
            if charset_pos == -1:
                errors.append(f"{rel}: missing <meta charset=\"utf-8\">")
            elif head_start != -1 and charset_pos - head_start > 120:
                errors.append(f"{rel}: charset declaration is too deep in <head>")
        if path.suffix.lower() == ".xml":
            first_line = text.splitlines()[0] if text.splitlines() else ""
            if "encoding=\"UTF-8\"" not in first_line and "encoding='UTF-8'" not in first_line:
                errors.append(f"{rel}: XML declaration must specify UTF-8")
    if errors:
        print("Encoding integrity validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Encoding integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
