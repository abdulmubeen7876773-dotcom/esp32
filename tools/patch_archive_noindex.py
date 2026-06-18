import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "projects" / "_archive"


def patch_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if "noindex" in raw.lower():
        return False
    if re.search(r'<meta name="robots" content="[^"]*">', raw):
        updated = re.sub(
            r'<meta name="robots" content="[^"]*">',
            '<meta name="robots" content="noindex,nofollow">',
            raw,
            count=1,
        )
    else:
        updated = raw.replace(
            "<head>",
            '<head>\n<meta name="robots" content="noindex,nofollow">',
            1,
        )
    path.write_text(updated, encoding="utf-8")
    return True


def main():
    if not ARCHIVE.exists():
        print("No archive folder found.")
        return
    changed = 0
    for path in ARCHIVE.glob("*.html"):
        if patch_file(path):
            changed += 1
    print(f"Patched {changed} archive pages with noindex,nofollow")


if __name__ == "__main__":
    main()
