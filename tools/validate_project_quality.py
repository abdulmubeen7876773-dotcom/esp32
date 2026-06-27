import json
import re
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "content" / "projects"
REPORTS_DIR = ROOT / "docs" / "reports"
TEMPLATE_SLUG = "project-template"
BENCHMARK_SLUG = "esp32-iot-weather-station"

GOLDEN_REQUIRED_CHECKS = (
    ("story", "Mission Story"),
    ("eli12", "Explain Like I'm 12"),
    ("parent_safety", "Parent Safety"),
    ("what_you_build", "What You Will Build"),
    ("components", "Components List"),
    ("wiring", "Wiring"),
    ("code", "Code"),
    ("output", "Expected Output"),
    ("common_mistakes", "Common Mistakes"),
    ("troubleshooting", "Troubleshooting"),
    ("upgrade_ideas", "Upgrade Ideas"),
    ("related_guides", "Related Guides"),
    ("related_projects", "Related Projects"),
    ("project_complete", "Project Complete"),
    ("related_components", "Related Components"),
)

GOLDEN_RECOMMENDED = (
    ("project_meta", "Project Meta Badges"),
    ("hardware_sync", "Root Hardware Block"),
)

STAGED_REQUIRED_CHECKS = (
    ("title", "Title"),
    ("description", "Description"),
    ("category", "Category"),
    ("hardware", "Hardware Block"),
)


def _load_project(path: Path) -> dict:
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _text(value) -> str:
    return str(value or "").strip()


def _is_golden(project: dict) -> bool:
    return _text(project.get("format")).lower() == "golden" or bool(project.get("project"))


def _project_block(project: dict) -> dict:
    block = project.get("project") or {}
    return block if isinstance(block, dict) else {}


def _components(proj: dict) -> list:
    items = proj.get("components") or proj.get("things_you_need") or []
    return items if isinstance(items, list) else []


def _component_links(components: list) -> list[str]:
    links: list[str] = []
    for item in components:
        if isinstance(item, dict):
            link = _text(item.get("link"))
            if "/components/" in link:
                links.append(link)
    return links


def _has_wiring(proj: dict) -> bool:
    wiring = proj.get("wiring") or {}
    if not isinstance(wiring, dict):
        return False
    steps = wiring.get("steps") or []
    return isinstance(steps, list) and len(steps) >= 3


def _wiring_unplug_first(proj: dict) -> bool:
    wiring = proj.get("wiring") or {}
    if not isinstance(wiring, dict):
        return False
    steps = wiring.get("steps") or []
    if not steps:
        return False
    first = _text(steps[0] if isinstance(steps[0], str) else steps[0].get("text", "")).lower()
    return "unplug" in first


def _has_code(proj: dict) -> bool:
    code = proj.get("code") or {}
    if isinstance(code, dict) and _text(code.get("content")):
        return True
    return bool(_text(proj.get("example_code")))


def _golden_presence(project: dict) -> dict[str, bool]:
    proj = _project_block(project)
    components = _components(proj)
    complete = proj.get("complete") or {}
    skills = complete.get("skills") or [] if isinstance(complete, dict) else []
    guides = proj.get("related_guides") or []
    projects = proj.get("related_projects") or []
    hardware = project.get("hardware") or {}

    return {
        "story": len(_text(proj.get("story"))) >= 80,
        "eli12": len(_text(proj.get("eli12"))) >= 40,
        "parent_safety": len(_text(proj.get("parent_safety"))) >= 40,
        "what_you_build": len(_text(proj.get("what_you_build"))) >= 30,
        "components": len(components) >= 3,
        "wiring": _has_wiring(proj),
        "code": _has_code(proj),
        "output": len(_text(proj.get("expected_output"))) >= 40,
        "common_mistakes": isinstance(proj.get("common_mistakes"), list)
        and len(proj.get("common_mistakes") or []) >= 3,
        "troubleshooting": isinstance(proj.get("troubleshooting"), list)
        and len(proj.get("troubleshooting") or []) >= 2,
        "upgrade_ideas": isinstance(proj.get("upgrade_ideas"), list)
        and len(proj.get("upgrade_ideas") or []) >= 2,
        "related_guides": isinstance(guides, list) and len(guides) >= 2,
        "related_projects": isinstance(projects, list) and len(projects) >= 1,
        "project_complete": isinstance(complete, dict)
        and bool(_text(complete.get("summary")))
        and isinstance(skills, list)
        and len(skills) >= 2,
        "related_components": len(_component_links(components)) >= 1,
        "project_meta": all(
            _text(proj.get(k))
            for k in ("mission_title", "difficulty", "age", "estimated_time", "budget")
        ),
        "hardware_sync": isinstance(hardware, dict) and bool(hardware.get("wiring")),
    }


def _staged_presence(project: dict) -> dict[str, bool]:
    hardware = project.get("hardware") or {}
    return {
        "title": bool(_text(project.get("title"))),
        "description": len(_text(project.get("description"))) >= 30,
        "category": bool(_text(project.get("category"))),
        "hardware": isinstance(hardware, dict) and bool(hardware.get("wiring")),
    }


def _missing_sections(presence: dict[str, bool], golden: bool) -> list[str]:
    missing: list[str] = []
    checks = GOLDEN_REQUIRED_CHECKS if golden else STAGED_REQUIRED_CHECKS
    for key, label in checks:
        if not presence.get(key, False):
            missing.append(label)
    if golden:
        for key, label in GOLDEN_RECOMMENDED:
            if not presence.get(key, False):
                missing.append(f"{label} (recommended)")
    return missing


def _warnings(project: dict, presence: dict[str, bool], golden: bool) -> list[str]:
    warnings: list[str] = []
    checks = GOLDEN_REQUIRED_CHECKS if golden else STAGED_REQUIRED_CHECKS
    for key, label in checks:
        if not presence.get(key, False):
            warnings.append(f"Missing {label}")

    if golden:
        proj = _project_block(project)
        wiring = proj.get("wiring") or {}
        if isinstance(wiring, dict) and wiring and not _text(wiring.get("illustration_alt")):
            warnings.append("Wiring section missing illustration_alt (accessibility)")
        if _has_wiring(proj) and not _wiring_unplug_first(proj):
            warnings.append("Wiring first step should mention unplugging USB")
        safety = _text(proj.get("parent_safety")).lower()
        if proj.get("parent_safety") and "unplug" not in safety:
            warnings.append("Parent safety should mention unplugging before rewiring")
        guides = proj.get("related_guides") or []
        for item in guides if isinstance(guides, list) else []:
            if isinstance(item, dict) and not _text(item.get("description")):
                warnings.append("Related guide entry missing description")
                break
    else:
        warnings.append("Staged placeholder — upgrade to format: golden with full project block")
    return warnings


def _score_golden_child(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    if len(_text(proj.get("story"))) >= 100:
        score += 25
    elif presence["story"]:
        score += 12
    if len(_text(proj.get("eli12"))) >= 80:
        score += 20
    elif presence["eli12"]:
        score += 10
    if len(_text(proj.get("expected_output"))) >= 80:
        score += 20
    elif presence["output"]:
        score += 10
    upgrades = proj.get("upgrade_ideas") or []
    if isinstance(upgrades, list) and len(upgrades) >= 3:
        score += 15
    elif presence["upgrade_ideas"]:
        score += 8
    complete = proj.get("complete") or {}
    if isinstance(complete, dict) and len(_text(complete.get("summary"))) >= 80:
        score += 20
    elif presence["project_complete"]:
        score += 10
    return min(100, score)


def _score_golden_parent(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    safety = _text(proj.get("parent_safety")).lower()
    if presence["parent_safety"] and "unplug" in safety and ("3.3" in safety or "usb" in safety):
        score += 35
    elif presence["parent_safety"]:
        score += 18
    if _text(proj.get("age")):
        score += 15
    if _text(proj.get("estimated_time")):
        score += 15
    if _text(proj.get("budget")):
        score += 15
    components = _components(proj)
    with_notes = sum(1 for c in components if isinstance(c, dict) and _text(c.get("note")))
    if len(components) >= 4 and with_notes >= 3:
        score += 20
    elif presence["components"]:
        score += 10
    return min(100, score)


def _score_golden_teacher(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    complete = proj.get("complete") or {}
    skills = complete.get("skills") or [] if isinstance(complete, dict) else []
    if isinstance(skills, list) and len(skills) >= 3:
        score += 25
    elif presence["project_complete"]:
        score += 12
    troubleshooting = proj.get("troubleshooting") or []
    if isinstance(troubleshooting, list) and len(troubleshooting) >= 3:
        score += 25
    elif presence["troubleshooting"]:
        score += 12
    guides = proj.get("related_guides") or []
    described = sum(
        1 for g in (guides if isinstance(guides, list) else [])
        if isinstance(g, dict) and _text(g.get("description"))
    )
    if described >= 2:
        score += 25
    elif presence["related_guides"]:
        score += 12
    mistakes = proj.get("common_mistakes") or []
    if isinstance(mistakes, list) and len(mistakes) >= 3:
        score += 25
    elif presence["common_mistakes"]:
        score += 12
    return min(100, score)


def _score_golden_engineering(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    wiring = proj.get("wiring") or {}
    steps = wiring.get("steps") or [] if isinstance(wiring, dict) else []
    if isinstance(steps, list) and len(steps) >= 5:
        score += 25
    elif presence["wiring"]:
        score += 12
    if _wiring_unplug_first(proj):
        score += 15
    if _has_code(proj):
        score += 25
    troubleshooting = proj.get("troubleshooting") or []
    if isinstance(troubleshooting, list) and len(troubleshooting) >= 3:
        score += 20
    elif presence["troubleshooting"]:
        score += 10
    hardware = project.get("hardware") or {}
    if isinstance(hardware, dict) and hardware.get("sensor_pin"):
        score += 15
    return min(100, score)


def _score_golden_seo(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    if len(_text(project.get("description"))) >= 60:
        score += 25
    if _text(project.get("title")):
        score += 15
    if _text(project.get("category")):
        score += 15
    guides = proj.get("related_guides") or []
    projects = proj.get("related_projects") or []
    described = 0
    for item in list(guides if isinstance(guides, list) else []) + list(
        projects if isinstance(projects, list) else []
    ):
        if isinstance(item, dict) and _text(item.get("description")):
            described += 1
    score += min(30, described * 10)
    if presence["related_projects"]:
        score += 15
    return min(100, score)


def _score_golden_accessibility(project: dict, presence: dict[str, bool]) -> int:
    proj = _project_block(project)
    score = 0
    wiring = proj.get("wiring") or {}
    if isinstance(wiring, dict) and len(_text(wiring.get("illustration_alt"))) >= 40:
        score += 30
    elif isinstance(wiring, dict) and _text(wiring.get("illustration_alt")):
        score += 18
    if len(_text(proj.get("eli12"))) >= 60:
        score += 25
    if len(_text(proj.get("expected_output"))) >= 60:
        score += 25
    if len(_text(proj.get("what_you_build"))) >= 40:
        score += 20
    return min(100, score)


def _score_staged_child(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    if len(_text(project.get("description"))) >= 60:
        score += 40
    elif presence["description"]:
        score += 20
    if _text(project.get("title")):
        score += 30
    if presence["hardware"]:
        score += 20
    return min(100, score)


def _score_staged_parent(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    if _text(project.get("category")):
        score += 30
    if len(_text(project.get("description"))) >= 40:
        score += 30
    if presence["hardware"]:
        score += 25
    return min(100, score)


def _score_staged_teacher(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    if presence["title"] and presence["description"] and presence["category"]:
        score += 35
    if presence["hardware"]:
        score += 35
    return min(100, score)


def _score_staged_engineering(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    hardware = project.get("hardware") or {}
    wiring = hardware.get("wiring") if isinstance(hardware, dict) else []
    if isinstance(wiring, list) and len(wiring) >= 3:
        score += 50
    elif presence["hardware"]:
        score += 25
    if isinstance(hardware, dict) and hardware.get("sensor_pin"):
        score += 30
    return min(100, score)


def _score_staged_seo(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    if len(_text(project.get("description"))) >= 50:
        score += 40
    if _text(project.get("title")):
        score += 30
    if _text(project.get("category")):
        score += 30
    return min(100, score)


def _score_staged_accessibility(project: dict, presence: dict[str, bool]) -> int:
    score = 0
    if len(_text(project.get("description"))) >= 40:
        score += 50
    if _text(project.get("title")):
        score += 30
    return min(100, score)


def _recommendations(project: dict, presence: dict[str, bool], scores: dict, golden: bool) -> list[str]:
    recs: list[str] = []
    if golden:
        proj = _project_block(project)
        if not presence.get("story"):
            recs.append("Add 2–4 paragraph project.story with emotional hook and real-world connection.")
        if not presence.get("parent_safety"):
            recs.append("Add project.parent_safety with 3.3 V, unplug, and supervision notes.")
        if not presence.get("troubleshooting"):
            recs.append("Add 2+ troubleshooting problem/fix pairs.")
        if not presence.get("common_mistakes"):
            recs.append("Add 3+ common_mistakes entries.")
        if not presence.get("upgrade_ideas"):
            recs.append("Add 2+ upgrade_ideas for advanced learners.")
        if not presence.get("related_guides"):
            recs.append("Link to 2+ related guides with descriptions.")
        if not presence.get("related_projects"):
            recs.append("Link to at least 1 related project with description.")
        if not presence.get("related_components"):
            recs.append("Link components in project.components to /components/ pages.")
        wiring = proj.get("wiring") or {}
        if isinstance(wiring, dict) and not _text(wiring.get("illustration_alt")):
            recs.append("Add illustration_alt to project.wiring.")
    else:
        recs.append("Upgrade to format: golden — copy content/project-template.yaml and fill all project sections.")
        recs.append(f"Use {BENCHMARK_SLUG}.yaml as the reference benchmark.")
    if scores["seo"] < 70:
        recs.append("Strengthen description and related link descriptions for SEO.")
    if not recs:
        recs.append("Minor polish only — align with Mini Weather Station depth where applicable.")
    return recs[:8]


def analyze_project(project: dict) -> dict:
    golden = _is_golden(project)
    presence = _golden_presence(project) if golden else _staged_presence(project)

    if golden:
        scores = {
            "child_experience": _score_golden_child(project, presence),
            "parent_experience": _score_golden_parent(project, presence),
            "teacher_experience": _score_golden_teacher(project, presence),
            "engineering": _score_golden_engineering(project, presence),
            "seo": _score_golden_seo(project, presence),
            "accessibility": _score_golden_accessibility(project, presence),
        }
    else:
        scores = {
            "child_experience": _score_staged_child(project, presence),
            "parent_experience": _score_staged_parent(project, presence),
            "teacher_experience": _score_staged_teacher(project, presence),
            "engineering": _score_staged_engineering(project, presence),
            "seo": _score_staged_seo(project, presence),
            "accessibility": _score_staged_accessibility(project, presence),
        }

    scores["overall"] = round(sum(scores.values()) / len(scores))
    missing = _missing_sections(presence, golden)
    warnings = _warnings(project, presence, golden)
    recommendations = _recommendations(project, presence, scores, golden)

    priority = "LOW"
    if golden:
        if scores["overall"] < 50 or not presence.get("code") or not presence.get("wiring"):
            priority = "HIGH"
        elif scores["overall"] < 75:
            priority = "MEDIUM"
    else:
        priority = "HIGH"

    title = project.get("title") or project.get("slug", "?")
    proj = _project_block(project)
    if golden and proj.get("mission_title"):
        title = proj["mission_title"]

    return {
        "slug": project.get("slug", "?"),
        "title": title,
        "project_type": "golden" if golden else "staged",
        "scores": scores,
        "missing_sections": missing,
        "warnings": warnings,
        "priority": priority,
        "recommendations": recommendations,
        "presence": presence,
    }


def analyze_all_projects() -> list[dict]:
    results: list[dict] = []
    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        if path.stem == TEMPLATE_SLUG:
            continue
        project = _load_project(path)
        if not project:
            continue
        project.setdefault("slug", path.stem)
        results.append(analyze_project(project))
    return results


def write_report(results: list[dict]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    benchmark = next((r for r in results if r["slug"] == BENCHMARK_SLUG), None)
    golden_count = sum(1 for r in results if r["project_type"] == "golden")
    staged_count = sum(1 for r in results if r["project_type"] == "staged")

    lines = [
        "# Project Quality Report",
        "",
        f"Generated: {generated}",
        "",
        "Benchmark: **ESP32 Mini Weather Station** is the golden standard (`content/projects/esp32-iot-weather-station.yaml`).",
        "",
        f"Portfolio: {golden_count} golden · {staged_count} staged placeholder(s)",
        "",
        "Standard: [GOLDEN_PROJECT_STANDARD.md](../editorial/GOLDEN_PROJECT_STANDARD.md)",
        "",
        "Run `py tools/validate_project_quality.py` to refresh this report.",
        "",
    ]

    if benchmark:
        bs = benchmark["scores"]
        lines.extend(
            [
                "## Golden Benchmark (ESP32 Mini Weather Station)",
                "",
                f"- Overall: {bs['overall']}/100",
                f"- Child: {bs['child_experience']} · Parent: {bs['parent_experience']} · Teacher: {bs['teacher_experience']}",
                f"- Engineering: {bs['engineering']} · SEO: {bs['seo']} · Accessibility: {bs['accessibility']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Summary",
            "",
            "| Project | Type | Overall | Priority | Missing required |",
            "|---------|------|---------|----------|------------------|",
        ]
    )
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        checks = GOLDEN_REQUIRED_CHECKS if r["project_type"] == "golden" else STAGED_REQUIRED_CHECKS
        required_missing = sum(1 for key, label in checks if label in r["missing_sections"])
        display_title = r["title"]
        if len(display_title) > 40:
            display_title = r["slug"]
        lines.append(
            f"| {display_title} | {r['project_type']} | {r['scores']['overall']}/100 | {r['priority']} | {required_missing} |"
        )
    lines.append("")

    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        s = r["scores"]
        lines.extend(
            [
                f"## {r['title']} (`{r['slug']}`)",
                "",
                f"**Type:** {r['project_type']} · **Overall score:** {s['overall']}/100 · **Priority:** {r['priority']}",
                "",
                "### Scores",
                "",
                f"- Child Experience: {s['child_experience']}/100",
                f"- Parent Experience: {s['parent_experience']}/100",
                f"- Teacher Experience: {s['teacher_experience']}/100",
                f"- Engineering: {s['engineering']}/100",
                f"- SEO: {s['seo']}/100",
                f"- Accessibility: {s['accessibility']}/100",
                "",
                "### Missing sections",
                "",
            ]
        )
        if r["missing_sections"]:
            lines.extend(f"- {m}" for m in r["missing_sections"])
        else:
            lines.append("- None")
        lines.extend(["", "### Recommendations", ""])
        lines.extend(f"- {rec}" for rec in r["recommendations"])
        if r["warnings"]:
            lines.extend(["", "### Warnings", ""])
            lines.extend(f"- {w}" for w in r["warnings"][:12])
        lines.append("")

    report_path = REPORTS_DIR / "project-quality-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = ROOT / "project-quality-report.json"
    payload = {
        "generated_at": generated,
        "benchmark_slug": BENCHMARK_SLUG,
        "golden_count": golden_count,
        "staged_count": staged_count,
        "projects": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    results = analyze_all_projects()
    write_report(results)

    print("Project quality report")
    print(f"  Wrote {REPORTS_DIR / 'project-quality-report.md'}")
    print(f"  Wrote {ROOT / 'project-quality-report.json'}")
    print()
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        checks = GOLDEN_REQUIRED_CHECKS if r["project_type"] == "golden" else STAGED_REQUIRED_CHECKS
        missing_req = [label for key, label in checks if label in r["missing_sections"]]
        print(
            f"  {r['slug']}: {r['scores']['overall']}/100 ({r['priority']}) [{r['project_type']}]"
            + (f" — missing: {', '.join(missing_req)}" if missing_req else "")
        )
        for w in r["warnings"]:
            print(f"    WARN: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
