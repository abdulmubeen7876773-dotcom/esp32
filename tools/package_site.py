"""Copy reader-facing static files into a fresh deployment directory.

Sources, historical backups, audit reports and component review inputs stay in
the repository. This does not delete or edit any source files.
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIRS = {"assets", "category", "components", "guides", "projects"}
ROOT_EXTENSIONS = {".html", ".css", ".js", ".xml", ".svg", ".jpg", ".png", ".webp"}
ROOT_FILES = {".nojekyll", "CNAME", "ads.txt", "robots.txt", "projects.json", "search-index.json"}
PROTECTED = {"component images.zip", "esp32-component-master-catalog.backup.csv",
             "esp32-component-master-catalog.csv", "esp32-component-master-catalog.md"}


def public_file(relative: Path) -> bool:
    if relative.name in PROTECTED or "_archive" in relative.parts:
        return False
    if len(relative.parts) == 1:
        return (relative.suffix in ROOT_EXTENSIONS or relative.name in ROOT_FILES
                or relative.name.startswith("esp32engineindex") and relative.suffix == ".txt")
    if relative.parts[0] == "assets":
        return relative.suffix.lower() in {".svg", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".ico", ".css", ".js", ".woff", ".woff2", ".ttf", ".mp4", ".pdf"}
    return relative.parts[0] in PUBLIC_DIRS and relative.suffix == ".html"


def package_site(output: Path) -> int:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Deployment output must be outside the repository")
    output.mkdir(parents=True, exist_ok=False)
    count = 0
    candidates = list(ROOT.iterdir())
    for directory in PUBLIC_DIRS:
        candidates.extend((ROOT / directory).rglob("*"))
    for source in sorted(set(candidates)):
        if source.is_file() and not source.is_symlink() and public_file(source.relative_to(ROOT)):
            destination = output / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(f"Packaged {package_site(args.output)} public files into {args.output}")
