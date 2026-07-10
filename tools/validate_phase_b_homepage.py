import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_home_recommendations
from content_store import get_content_store
from project_text import is_golden_project
from site_counts import site_counts

ROOT = Path(__file__).resolve().parent.parent
AUDIENCE_KEYS = {"student", "parent", "teacher", "maker"}
GOAL_KEYS = {
    "first-esp32-project",
    "sensors-and-data",
    "smart-home-and-iot",
    "robotics-and-motion",
    "cameras-and-computer-vision",
    "ai-and-advanced-builds",
}


def public_file_for_href(href: str) -> Path:
    href = href.split("#", 1)[0].split("?", 1)[0]
    if href.startswith("/"):
        href = href[1:]
    if not href:
        href = "index.html"
    if href.endswith("/"):
        href += "index.html"
    return ROOT / href


def main() -> int:
    config = load_home_recommendations()
    store = get_content_store()
    projects = {project["slug"]: project for project in store.projects()}
    golden = {slug for slug, project in projects.items() if is_golden_project(project)}
    errors: list[str] = []

    audiences = config.get("audiences", {})
    goals = config.get("goals", {})
    matrix = config.get("recommendations", {})
    if set(audiences) != AUDIENCE_KEYS:
        errors.append(f"audiences expected {sorted(AUDIENCE_KEYS)} actual {sorted(audiences)}")
    if set(goals) != GOAL_KEYS:
        errors.append(f"goals expected {sorted(GOAL_KEYS)} actual {sorted(goals)}")

    combo_count = 0
    used_slugs: set[str] = set()
    for audience in AUDIENCE_KEYS:
        for goal in GOAL_KEYS:
            combo_count += 1
            slugs = ((matrix.get(audience) or {}).get(goal) or [])
            if not 1 <= len(slugs) <= 3:
                errors.append(f"{audience}/{goal}: expected 1-3 slugs actual {len(slugs)}")
            if len(slugs) != len(set(slugs)):
                errors.append(f"{audience}/{goal}: duplicate slug in combination")
            for slug in slugs:
                used_slugs.add(slug)
                if slug not in projects:
                    errors.append(f"{audience}/{goal}: missing project slug {slug}")
                elif slug not in golden:
                    errors.append(f"{audience}/{goal}: non-Golden project slug {slug}")
    if combo_count != 24:
        errors.append(f"combination count expected 24 actual {combo_count}")
    if "esp32-tinyml-sound-classifier" in used_slugs:
        errors.append("staged TinyML project appears in recommendations")

    counts = site_counts()
    if counts["total_projects"] != 50 or counts["golden_projects"] != 49 or counts["staged_projects"] != 1:
        errors.append(f"portfolio counts unexpected: {counts}")

    home_path = ROOT / "index.html"
    if home_path.exists():
        home = home_path.read_text(encoding="utf-8")
        if "<noscript>" not in home or "home-noscript-heading" not in home:
            errors.append("homepage no-JS fallback section missing")
        for slug in used_slugs:
            href = f"/projects/{slug}.html"
            if href not in home:
                errors.append(f"homepage raw HTML missing recommendation link {href}")
        if len(re.findall(r"<button[^>]+data-audience=", home)) != 4:
            errors.append("homepage does not render 4 audience buttons")
        if len(re.findall(r"<button[^>]+data-goal=", home)) != 6:
            errors.append("homepage does not render 6 goal buttons")
        if 'aria-pressed="true"' not in home:
            errors.append("homepage selected state aria-pressed missing")
        data_match = re.search(r'<script type="application/json" id="home-recommendation-data">(.*?)</script>', home, re.S)
        if not data_match:
            errors.append("homepage recommendation JSON missing")
        else:
            data = json.loads(data_match.group(1))
            if set(data) != AUDIENCE_KEYS:
                errors.append("homepage recommendation JSON audience keys mismatch")
    else:
        errors.append("generated homepage missing")

    hrefs = set(re.findall(r'href="([^"#?:]+(?:\.html|/))"', home_path.read_text(encoding="utf-8") if home_path.exists() else ""))
    for href in hrefs:
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        if not public_file_for_href(href).exists():
            errors.append(f"homepage link does not resolve: {href}")

    generated_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in [ROOT / "index.html", ROOT / "learning.html", ROOT / "downloads.html", ROOT / "projects.html"]
        if path.exists()
    )
    stale_patterns = [
        r"\b15 parent projects\b",
        r"\b15 projects\b",
        r"\b12 missions planned\b",
    ]
    for pattern in stale_patterns:
        if re.search(pattern, generated_text, re.I):
            errors.append(f"stale hardcoded count pattern remains: {pattern}")

    if errors:
        print("Phase B homepage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Phase B homepage validation passed: "
        f"24 combinations, {len(used_slugs)} unique Golden projects, counts {counts}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
