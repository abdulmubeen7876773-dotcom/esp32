import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

STEPS = [
    "validate_content.py",
    "rebuild_parents.py",
    "build_static_pages.py",
    "build_guides.py",
    "build_components.py",
    "build_search_index.py",
    "rebuild_index.py",
]


def run_step(name: str) -> None:
    path = TOOLS / name
    if not path.exists():
        raise SystemExit(f"Missing build script: {path}")
    print(f"\n=== {name} ===")
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main():
    cfg = ROOT / "static.config.yaml"
    if not cfg.exists():
        raise SystemExit("Missing static.config.yaml — static-first config required.")
    content = ROOT / "content" / "site.yaml"
    if not content.exists():
        raise SystemExit(
            "Missing content/site.yaml. Add site settings under content/ before building."
        )
    print("Static-first build (Phase 1) — files only, no runtime server.")
    started = time.perf_counter()
    steps_run = []
    for step in STEPS:
        run_step(step)
        steps_run.append({"name": step, "status": "PASS"})
    duration = round(time.perf_counter() - started, 2)

    sys.path.insert(0, str(TOOLS))
    from release_readiness import run_release_readiness

    run_release_readiness(
        {
            "status": "PASS",
            "duration_seconds": duration,
            "steps": steps_run,
        }
    )
    print("\nBuild complete. Deploy root HTML/JSON/JS to static hosting.")


if __name__ == "__main__":
    main()
