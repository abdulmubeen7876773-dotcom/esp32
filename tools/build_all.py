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


def run_step(name: str) -> list[str]:
    path = TOOLS / name
    if not path.exists():
        raise SystemExit(f"Missing build script: {path}")
    print(f"\n=== {name} ===")
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.stderr:
        print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n", file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

    warnings: list[str] = []
    for line in (proc.stdout + proc.stderr).splitlines():
        text = line.strip()
        if text.startswith("IndexNow: HTTP") and "HTTP 200" not in text:
            warnings.append(text)
    return warnings


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
    warnings: list[str] = []
    for step in STEPS:
        warnings.extend(run_step(step))
    duration = round(time.perf_counter() - started, 2)

    sys.path.insert(0, str(TOOLS))
    from build_report import generate_build_report

    generate_build_report(
        {
            "status": "PASS",
            "duration_seconds": duration,
            "warnings": warnings,
            "errors": [],
        }
    )
    from content_dashboard import generate_content_dashboard

    generate_content_dashboard()
    print("\nBuild complete. Deploy root HTML/JSON/JS to static hosting.")


if __name__ == "__main__":
    main()
