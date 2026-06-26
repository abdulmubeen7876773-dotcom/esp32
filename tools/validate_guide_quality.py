import json
import re
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_yaml

ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = ROOT / "content" / "guides"
REPORTS_DIR = ROOT / "docs" / "reports"
TEMPLATE_SLUG = "guide-template"
BENCHMARK_SLUG = "blink-led-esp32"

MISSION_REQUIRED_CHECKS = (
    ("mission_story", "Mission Story"),
    ("eli12", "Explain Like I'm 12"),
    ("things_you_need", "Things You'll Need"),
    ("safety", "Safety"),
    ("concept", "Concept"),
    ("wiring", "Wiring"),
    ("code", "Code"),
    ("output", "Output"),
    ("quiz", "Quiz"),
    ("challenge", "Challenge"),
    ("mission_complete", "Mission Complete"),
    ("next_mission", "Next Mission"),
    ("related_components", "Related Components"),
    ("learning_outcomes", "Learning Outcomes"),
)

MISSION_RECOMMENDED = (
    ("related_projects", "Related Projects"),
    ("what_you_build", "What You'll Build"),
    ("component_spotlight", "Component Spotlight"),
)

REFERENCE_REQUIRED_CHECKS = (
    ("intro_story", "Intro Story"),
    ("intro_eli12", "Explain Like I'm 12"),
    ("intro_safety", "Safety"),
    ("body", "Body Content"),
    ("meta_description", "Meta Description"),
    ("related_guides", "Related Guides"),
)


def _load_guide(path: Path) -> dict:
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _text(value) -> str:
    return str(value or "").strip()


def _is_mission(guide: dict) -> bool:
    return _text(guide.get("format")).lower() == "mission" or bool(guide.get("mission"))


def _safety_items(mission: dict) -> list:
    safety = mission.get("safety") or []
    if not isinstance(safety, list):
        return []
    items: list[str] = []
    for entry in safety:
        if isinstance(entry, dict):
            items.append(_text(entry.get("text")))
        else:
            items.append(_text(entry))
    return [i for i in items if i]


def _things_you_need(mission: dict) -> list:
    items = mission.get("things_you_need") or []
    return items if isinstance(items, list) else []


def _component_links(things: list) -> list[str]:
    links: list[str] = []
    for item in things:
        if not isinstance(item, dict):
            continue
        link = _text(item.get("link"))
        if "/components/" in link:
            links.append(link)
    return links


def _quiz_items(mission: dict) -> list:
    quiz = mission.get("quiz") or []
    return quiz if isinstance(quiz, list) else []


def _quiz_quality(quiz: list) -> dict:
    complete = 0
    for q in quiz:
        if not isinstance(q, dict):
            continue
        opts = q.get("options") or []
        if (
            _text(q.get("question"))
            and isinstance(opts, list)
            and len(opts) >= 3
            and q.get("correct") is not None
            and _text(q.get("explanation"))
            and _text(q.get("correct_feedback"))
            and _text(q.get("wrong_feedback"))
        ):
            complete += 1
    return {"count": len(quiz), "complete": complete}


def _has_challenge(mission: dict) -> bool:
    items = mission.get("challenge_items") or []
    if isinstance(items, list) and len(items) >= 2:
        return True
    return len(_text(mission.get("challenge"))) >= 40


def _has_code(mission: dict) -> bool:
    code = mission.get("code") or {}
    if isinstance(code, dict) and _text(code.get("content")):
        return True
    return False


def _has_wiring(mission: dict) -> bool:
    wiring = mission.get("wiring") or {}
    if not isinstance(wiring, dict):
        return False
    steps = wiring.get("steps") or []
    return isinstance(steps, list) and len(steps) >= 3


def _wiring_unplug_first(mission: dict) -> bool:
    wiring = mission.get("wiring") or {}
    if not isinstance(wiring, dict):
        return False
    steps = wiring.get("steps") or []
    if not steps:
        return False
    first = _text(steps[0] if isinstance(steps[0], str) else steps[0].get("text", "")).lower()
    return "unplug" in first


def _mission_presence(guide: dict) -> dict[str, bool]:
    mission = guide.get("mission") or {}
    if not isinstance(mission, dict):
        mission = {}
    things = _things_you_need(mission)
    quiz = _quiz_items(mission)
    quiz_q = _quiz_quality(quiz)
    complete = mission.get("complete") or {}
    skills = complete.get("skills") or [] if isinstance(complete, dict) else []
    next_missions = mission.get("next_missions") or []
    concept = mission.get("concept") or {}

    return {
        "mission_story": len(_text(mission.get("story"))) >= 80,
        "eli12": len(_text(mission.get("eli12"))) >= 40,
        "things_you_need": len(things) >= 3,
        "safety": len(_safety_items(mission)) >= 2,
        "concept": isinstance(concept, dict) and bool(_text(concept.get("body"))),
        "wiring": _has_wiring(mission),
        "code": _has_code(mission),
        "output": len(_text(mission.get("expected_output"))) >= 40,
        "quiz": quiz_q["count"] >= 2 and quiz_q["complete"] >= 2,
        "challenge": _has_challenge(mission),
        "mission_complete": isinstance(complete, dict)
        and bool(_text(complete.get("summary")))
        and bool(_text(complete.get("subtitle"))),
        "next_mission": isinstance(next_missions, list) and len(next_missions) >= 1,
        "related_components": len(_component_links(things)) >= 1
        or bool(_text(mission.get("component_spotlight_lead"))),
        "related_projects": isinstance(guide.get("related_projects"), list)
        and len(guide.get("related_projects") or []) >= 1,
        "learning_outcomes": isinstance(skills, list) and len(skills) >= 2,
        "what_you_build": len(_text(mission.get("what_you_build"))) >= 30,
        "component_spotlight": bool(_text(mission.get("component_spotlight_lead")))
        and len(_component_links(things)) >= 1,
    }


def _reference_presence(guide: dict) -> dict[str, bool]:
    intro = guide.get("intro") or {}
    if not isinstance(intro, dict):
        intro = {}
    body = _text(guide.get("body_html") or guide.get("body"))
    related = guide.get("related_guides") or []
    return {
        "intro_story": len(_text(intro.get("story"))) >= 60,
        "intro_eli12": len(_text(intro.get("eli12"))) >= 40,
        "intro_safety": len(_safety_items(intro)) >= 2,
        "body": len(body) >= 500,
        "meta_description": len(_text(guide.get("meta_description"))) >= 60,
        "related_guides": isinstance(related, list) and len(related) >= 2,
    }


def _missing_sections(presence: dict[str, bool], mission: bool) -> list[str]:
    missing: list[str] = []
    checks = MISSION_REQUIRED_CHECKS if mission else REFERENCE_REQUIRED_CHECKS
    for key, label in checks:
        if not presence.get(key, False):
            missing.append(label)
    if mission:
        for key, label in MISSION_RECOMMENDED:
            if not presence.get(key, False):
                missing.append(f"{label} (recommended)")
    return missing


def _warnings(guide: dict, presence: dict[str, bool], mission: bool) -> list[str]:
    warnings: list[str] = []
    checks = MISSION_REQUIRED_CHECKS if mission else REFERENCE_REQUIRED_CHECKS
    for key, label in checks:
        if not presence.get(key, False):
            warnings.append(f"Missing {label}")

    if mission:
        m = guide.get("mission") or {}
        quiz = _quiz_items(m)
        qq = _quiz_quality(quiz)
        if qq["count"] >= 2 and qq["complete"] < qq["count"]:
            warnings.append(
                f"Quiz has {qq['count']} questions but only {qq['complete']} with full feedback fields"
            )
        concept = m.get("concept") or {}
        if isinstance(concept, dict) and concept and not _text(concept.get("illustration_alt")):
            warnings.append("Concept section missing illustration_alt (accessibility)")
        wiring = m.get("wiring") or {}
        if isinstance(wiring, dict) and wiring and not _text(wiring.get("illustration_alt")):
            warnings.append("Wiring section missing illustration_alt (accessibility)")
        if _has_wiring(m) and not _wiring_unplug_first(m):
            warnings.append("Wiring first step should mention unplugging USB")
        if not presence.get("related_projects"):
            warnings.append("Missing Related Projects (recommended from Mission 2+)")
        complete = m.get("complete") or {}
        if isinstance(complete, dict) and _text(complete.get("summary")) and not _text(complete.get("subtitle")):
            warnings.append("Mission complete missing emotional subtitle")
    else:
        if not (guide.get("faqs") or []):
            warnings.append("Reference guide has no FAQs (recommended for SEO)")
    return warnings


def _score_mission_child(guide: dict, presence: dict[str, bool]) -> int:
    mission = guide.get("mission") or {}
    score = 0
    if len(_text(mission.get("story"))) >= 100:
        score += 20
    elif presence["mission_story"]:
        score += 10
    if len(_text(mission.get("eli12"))) >= 80:
        score += 20
    elif presence["eli12"]:
        score += 10
    qq = _quiz_quality(_quiz_items(mission))
    if qq["complete"] >= 3:
        score += 25
    elif qq["complete"] >= 2:
        score += 18
    items = mission.get("challenge_items") or []
    if isinstance(items, list) and len(items) >= 3:
        score += 15
    elif presence["challenge"]:
        score += 8
    complete = mission.get("complete") or {}
    if isinstance(complete, dict) and _text(complete.get("subtitle")) and len(_text(complete.get("summary"))) >= 80:
        score += 20
    elif presence["mission_complete"]:
        score += 10
    if len(_text(mission.get("expected_output"))) >= 80:
        score += 20
    elif presence["output"]:
        score += 10
    return min(100, score)


def _score_mission_parent(guide: dict, presence: dict[str, bool]) -> int:
    mission = guide.get("mission") or {}
    score = 0
    safety = _safety_items(mission)
    if len(safety) >= 3 and any("unplug" in s.lower() for s in safety):
        score += 30
    elif presence["safety"]:
        score += 15
    meta = _text(guide.get("meta_description"))
    if len(meta) >= 100:
        score += 25
    elif len(meta) >= 60:
        score += 15
    if _text(guide.get("reading_time")):
        score += 15
    things = _things_you_need(mission)
    with_notes = sum(1 for t in things if isinstance(t, dict) and (_text(t.get("note")) or _text(t.get("link"))))
    if len(things) >= 4 and with_notes >= 3:
        score += 30
    elif presence["things_you_need"]:
        score += 15
    return min(100, score)


def _score_mission_teacher(guide: dict, presence: dict[str, bool]) -> int:
    mission = guide.get("mission") or {}
    score = 0
    qq = _quiz_quality(_quiz_items(mission))
    if qq["complete"] >= 3:
        score += 25
    elif qq["complete"] >= 2:
        score += 15
    complete = mission.get("complete") or {}
    skills = complete.get("skills") or [] if isinstance(complete, dict) else []
    if isinstance(skills, list) and len(skills) >= 3:
        score += 25
    elif presence["learning_outcomes"]:
        score += 15
    if isinstance(complete, dict) and len(_text(complete.get("summary"))) >= 100:
        score += 20
    elif presence["mission_complete"]:
        score += 10
    things = _things_you_need(mission)
    if len(_component_links(things)) >= 1:
        score += 15
    next_m = mission.get("next_missions") or []
    if isinstance(next_m, list) and len(next_m) >= 2:
        score += 15
    elif presence["next_mission"]:
        score += 8
    return min(100, score)


def _score_mission_engineering(guide: dict, presence: dict[str, bool]) -> int:
    mission = guide.get("mission") or {}
    score = 0
    wiring = mission.get("wiring") or {}
    steps = wiring.get("steps") or [] if isinstance(wiring, dict) else []
    if isinstance(steps, list) and len(steps) >= 6:
        score += 25
    elif presence["wiring"]:
        score += 12
    if _has_code(mission):
        code = mission.get("code") or {}
        if isinstance(code, dict) and _text(code.get("notes")):
            score += 25
        else:
            score += 18
    concept = mission.get("concept") or {}
    if isinstance(concept, dict) and len(_text(concept.get("body"))) >= 80:
        score += 20
    elif presence["concept"]:
        score += 10
    out = _text(mission.get("expected_output")).lower()
    if "if nothing" in out or "if the" in out or "check" in out:
        score += 15
    elif presence["output"]:
        score += 8
    if _wiring_unplug_first(mission):
        score += 15
    return min(100, score)


def _score_mission_seo(guide: dict, presence: dict[str, bool]) -> int:
    score = 0
    if len(_text(guide.get("meta_description"))) >= 80:
        score += 20
    if "| ESP32 Engine" in _text(guide.get("title")):
        score += 15
    keywords = guide.get("keywords") or ""
    kw_count = len([k for k in re.split(r",\s*", _text(keywords)) if k])
    if kw_count >= 3:
        score += 15
    if _text(guide.get("headline")):
        score += 15
    if len(_text(guide.get("lead"))) >= 60:
        score += 20
    if guide.get("mission_number"):
        score += 15
    return min(100, score)


def _score_mission_accessibility(guide: dict, presence: dict[str, bool]) -> int:
    mission = guide.get("mission") or {}
    score = 0
    concept = mission.get("concept") or {}
    wiring = mission.get("wiring") or {}
    if isinstance(concept, dict) and len(_text(concept.get("illustration_alt"))) >= 40:
        score += 25
    elif isinstance(concept, dict) and _text(concept.get("illustration_alt")):
        score += 15
    if isinstance(wiring, dict) and len(_text(wiring.get("illustration_alt"))) >= 40:
        score += 25
    elif isinstance(wiring, dict) and _text(wiring.get("illustration_alt")):
        score += 15
    if len(_text(mission.get("eli12"))) >= 60:
        score += 25
    if len(_text(mission.get("expected_output"))) >= 60:
        score += 25
    return min(100, score)


def _score_reference_child(guide: dict, presence: dict[str, bool]) -> int:
    intro = guide.get("intro") or {}
    score = 0
    if len(_text(intro.get("story") if isinstance(intro, dict) else "")) >= 100:
        score += 35
    elif presence.get("intro_story"):
        score += 18
    if len(_text(intro.get("eli12") if isinstance(intro, dict) else "")) >= 80:
        score += 35
    elif presence.get("intro_eli12"):
        score += 18
    faqs = guide.get("faqs") or []
    if isinstance(faqs, list) and len(faqs) >= 5:
        score += 30
    elif isinstance(faqs, list) and len(faqs) >= 2:
        score += 15
    return min(100, score)


def _score_reference_parent(guide: dict, presence: dict[str, bool]) -> int:
    intro = guide.get("intro") or {}
    score = 0
    safety = _safety_items(intro if isinstance(intro, dict) else {})
    if len(safety) >= 3:
        score += 35
    elif presence.get("intro_safety"):
        score += 18
    if len(_text(guide.get("meta_description"))) >= 80:
        score += 30
    if _text(guide.get("reading_time")):
        score += 20
    if _text(guide.get("conclusion")):
        score += 15
    return min(100, score)


def _score_reference_teacher(guide: dict, presence: dict[str, bool]) -> int:
    score = 0
    related = guide.get("related_guides") or []
    if isinstance(related, list) and len(related) >= 4:
        score += 35
    elif presence.get("related_guides"):
        score += 20
    faqs = guide.get("faqs") or []
    if isinstance(faqs, list) and len(faqs) >= 8:
        score += 35
    elif isinstance(faqs, list) and len(faqs) >= 3:
        score += 20
    if len(_text(guide.get("conclusion"))) >= 80:
        score += 30
    return min(100, score)


def _score_reference_engineering(guide: dict, presence: dict[str, bool]) -> int:
    score = 0
    body = _text(guide.get("body_html") or guide.get("body"))
    if len(body) >= 3000:
        score += 40
    elif presence.get("body"):
        score += 25
    faqs = guide.get("faqs") or []
    tech_hits = 0
    if isinstance(faqs, list):
        for item in faqs:
            if not isinstance(item, dict):
                continue
            q = _text(item.get("question")).lower()
            if any(k in q for k in ("voltage", "gpio", "wifi", "arduino", "power", "pin")):
                tech_hits += 1
    score += min(30, tech_hits * 6)
    if _text(guide.get("proficiency_level")):
        score += 15
    if presence.get("intro_safety"):
        score += 15
    return min(100, score)


def _score_reference_seo(guide: dict, presence: dict[str, bool]) -> int:
    score = 0
    if len(_text(guide.get("meta_description"))) >= 100:
        score += 25
    faqs = guide.get("faqs") or []
    if isinstance(faqs, list) and len(faqs) >= 8:
        score += 30
    elif isinstance(faqs, list) and len(faqs) >= 3:
        score += 15
    if _text(guide.get("title")) and _text(guide.get("headline")):
        score += 20
    keywords = guide.get("keywords") or ""
    if len([k for k in re.split(r",\s*", _text(keywords)) if k]) >= 4:
        score += 15
    related = guide.get("related_guides") or []
    described = sum(
        1 for item in (related if isinstance(related, list) else [])
        if isinstance(item, dict) and _text(item.get("description"))
    )
    score += min(10, described * 3)
    return min(100, score)


def _score_reference_accessibility(guide: dict, presence: dict[str, bool]) -> int:
    score = 0
    body = _text(guide.get("body_html") or guide.get("body")).lower()
    if "<h2" in body or "<h3" in body:
        score += 30
    intro = guide.get("intro") or {}
    if isinstance(intro, dict) and len(_text(intro.get("eli12"))) >= 60:
        score += 25
    faqs = guide.get("faqs") or []
    if isinstance(faqs, list) and len(faqs) >= 5:
        score += 25
    if _text(guide.get("lead")):
        score += 20
    return min(100, score)


def _recommendations(guide: dict, presence: dict[str, bool], scores: dict, mission: bool) -> list[str]:
    recs: list[str] = []
    if mission:
        m = guide.get("mission") or {}
        if not presence.get("mission_story"):
            recs.append("Add 2–4 paragraph mission story with emotional hook and present tense.")
        if not presence.get("eli12"):
            recs.append("Add eli12 bullets with analogy before concept jargon.")
        if not presence.get("quiz"):
            recs.append("Add 2+ quiz questions with correct_feedback, wrong_feedback, and explanation.")
        qq = _quiz_quality(_quiz_items(m))
        if qq["count"] >= 2 and qq["complete"] < qq["count"]:
            recs.append("Complete quiz feedback fields on every question (golden standard).")
        if not presence.get("challenge"):
            recs.append("Add 2+ challenge_items with icons or a multi-idea challenge block.")
        if not presence.get("learning_outcomes"):
            recs.append("Add 2+ concrete skills in mission.complete.skills.")
        if not presence.get("related_components"):
            recs.append("Link at least one part in things_you_need to /components/ and add component_spotlight_lead.")
        if not presence.get("related_projects"):
            recs.append("Add related_projects at guide root when a capstone uses these skills.")
        concept = m.get("concept") or {}
        if isinstance(concept, dict) and not _text(concept.get("illustration_alt")):
            recs.append("Add illustration_alt to concept block.")
        wiring = m.get("wiring") or {}
        if isinstance(wiring, dict) and not _text(wiring.get("illustration_alt")):
            recs.append("Add illustration_alt to wiring block.")
        complete = m.get("complete") or {}
        if isinstance(complete, dict) and not _text(complete.get("subtitle")):
            recs.append("Add emotional subtitle to mission.complete.")
    else:
        if not presence.get("intro_story"):
            recs.append("Add intro.story emotional hook.")
        if not presence.get("body"):
            recs.append("Expand body_html reference content.")
        if not (guide.get("faqs") or []):
            recs.append("Add FAQ entries for SEO and teacher assessment.")
    if scores["seo"] < 70:
        recs.append("Strengthen meta_description, keywords, and descriptive cross-links.")
    if not recs:
        recs.append("Minor polish only — align with Blink LED golden standard where applicable.")
    return recs[:8]


def analyze_guide(guide: dict) -> dict:
    mission = _is_mission(guide)
    presence = _mission_presence(guide) if mission else _reference_presence(guide)

    if mission:
        scores = {
            "child_experience": _score_mission_child(guide, presence),
            "parent_experience": _score_mission_parent(guide, presence),
            "teacher_experience": _score_mission_teacher(guide, presence),
            "engineering": _score_mission_engineering(guide, presence),
            "seo": _score_mission_seo(guide, presence),
            "accessibility": _score_mission_accessibility(guide, presence),
        }
    else:
        scores = {
            "child_experience": _score_reference_child(guide, presence),
            "parent_experience": _score_reference_parent(guide, presence),
            "teacher_experience": _score_reference_teacher(guide, presence),
            "engineering": _score_reference_engineering(guide, presence),
            "seo": _score_reference_seo(guide, presence),
            "accessibility": _score_reference_accessibility(guide, presence),
        }

    scores["overall"] = round(sum(scores.values()) / len(scores))
    missing = _missing_sections(presence, mission)
    warnings = _warnings(guide, presence, mission)
    recommendations = _recommendations(guide, presence, scores, mission)

    priority = "LOW"
    if scores["overall"] < 50:
        priority = "HIGH"
    elif scores["overall"] < 75:
        priority = "MEDIUM"

    title = guide.get("headline") or guide.get("title") or guide.get("slug", "?")
    if mission:
        m = guide.get("mission") or {}
        title = m.get("title") or title

    return {
        "slug": guide.get("slug", "?"),
        "title": title,
        "guide_type": "mission" if mission else "reference",
        "scores": scores,
        "missing_sections": missing,
        "warnings": warnings,
        "priority": priority,
        "recommendations": recommendations,
        "presence": presence,
    }


def analyze_all_guides() -> list[dict]:
    results: list[dict] = []
    for path in sorted(GUIDES_DIR.glob("*.yaml")):
        if path.stem == TEMPLATE_SLUG:
            continue
        guide = _load_guide(path)
        if not guide:
            continue
        guide.setdefault("slug", path.stem)
        results.append(analyze_guide(guide))
    return results


def write_report(results: list[dict]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    benchmark = next((r for r in results if r["slug"] == BENCHMARK_SLUG), None)

    lines = [
        "# Guide Quality Report",
        "",
        f"Generated: {generated}",
        "",
        f"Benchmark: **Blink LED** is the golden standard (`content/guides/{BENCHMARK_SLUG}.yaml`).",
        "",
        "Standard: [GOLDEN_GUIDE_STANDARD.md](../editorial/GOLDEN_GUIDE_STANDARD.md)",
        "",
        "Run `py tools/validate_guide_quality.py` to refresh this report.",
        "",
    ]

    if benchmark:
        bs = benchmark["scores"]
        lines.extend(
            [
                "## Golden Benchmark (Blink LED)",
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
            "| Guide | Type | Overall | Priority | Missing required |",
            "|-------|------|---------|----------|------------------|",
        ]
    )
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        required_missing = sum(
            1
            for key, label in (MISSION_REQUIRED_CHECKS if r["guide_type"] == "mission" else REFERENCE_REQUIRED_CHECKS)
            if label in r["missing_sections"]
        )
        lines.append(
            f"| {r['title']} | {r['guide_type']} | {r['scores']['overall']}/100 | {r['priority']} | {required_missing} |"
        )
    lines.append("")

    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        s = r["scores"]
        lines.extend(
            [
                f"## {r['title']} (`{r['slug']}`)",
                "",
                f"**Type:** {r['guide_type']} · **Overall score:** {s['overall']}/100 · **Priority:** {r['priority']}",
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

    report_path = REPORTS_DIR / "guide-quality-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = ROOT / "guide-quality-report.json"
    payload = {
        "generated_at": generated,
        "benchmark_slug": BENCHMARK_SLUG,
        "guides": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    results = analyze_all_guides()
    write_report(results)

    print("Guide quality report")
    print(f"  Wrote {REPORTS_DIR / 'guide-quality-report.md'}")
    print(f"  Wrote {ROOT / 'guide-quality-report.json'}")
    print()
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        checks = MISSION_REQUIRED_CHECKS if r["guide_type"] == "mission" else REFERENCE_REQUIRED_CHECKS
        missing_req = [label for key, label in checks if label in r["missing_sections"]]
        print(
            f"  {r['slug']}: {r['scores']['overall']}/100 ({r['priority']}) [{r['guide_type']}]"
            + (f" — missing: {', '.join(missing_req)}" if missing_req else "")
        )
        for w in r["warnings"]:
            print(f"    WARN: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
