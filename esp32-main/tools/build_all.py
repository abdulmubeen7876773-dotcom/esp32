import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

STEPS = [
    "migrate_to_cms.py",
    "rebuild_parents.py",
    "build_static_pages.py",
    "build_guides.py",
    "rebuild_index.py",
]


def run_step(name: str) -> None:
    path = TOOLS / name
    if not path.exists():
        raise SystemExit(f"Missing build script: {path}")
    print(f"\n=== {name} ===")
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main():
    content = ROOT / "content" / "site.yaml"
    if not content.exists():
        run_step("migrate_to_cms.py")
    else:
        print("CMS content found, skipping migration")
    for step in STEPS[1:]:
        run_step(step)
    print("\nBuild complete.")


if __name__ == "__main__":
    main()
