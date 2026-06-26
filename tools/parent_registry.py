import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store

ROOT = Path(__file__).resolve().parent.parent


def legacy_from_git() -> list[dict]:
    try:
        raw = subprocess.check_output(
            ["git", "show", "HEAD:tools/parent_registry.py"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    ns: dict = {}
    exec(raw, ns)
    return ns.get("PARENTS", [])


PARENTS = get_content_store().projects() or legacy_from_git()
PARENT_BY_SLUG = {p["slug"]: p for p in PARENTS}
