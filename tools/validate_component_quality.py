import json
import re
from datetime import datetime, timezone
from pathlib import Path

from cms_loader import load_yaml

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_DIR = ROOT / "content" / "components"
REPORTS_DIR = ROOT / "docs" / "reports"
TEMPLATE_SLUG = "component-template"

FAQ_PREFIXES = {
    "glossary": re.compile(r"^glossary\s*[—\-]", re.I),
    "parent_tips": re.compile(r"^parent tips\s*[—\-]", re.I),
    "teacher_tips": re.compile(r"^teacher tips\s*[—\-]", re.I),
    "challenge": re.compile(r"^challenge yourself\s*[—\-]", re.I),
    "mini_quiz": re.compile(r"^mini quiz\s*[—\-]", re.I),
}

REQUIRED_CHECKS = (
    ("eli12", "Explain Like I'm 12"),
    ("quick_facts", "Quick Facts"),
    ("pinout", "Pinout"),
    ("troubleshooting", "Troubleshooting"),
    ("faqs", "FAQ"),
    ("glossary", "Glossary"),
    ("parent_tips", "Parent Tips"),
    ("teacher_tips", "Teacher Tips"),
    ("challenge", "Challenge"),
    ("related_guides", "Related Guides"),
    ("related_projects", "Related Projects"),
    ("code", "Code"),
    ("output", "Output"),
)

GOLDEN_OPTIONAL = (
    ("wiring", "Wiring"),
    ("common_mistakes", "Common Mistakes"),
    ("specs", "Technical Specifications"),
    ("datasheet", "Datasheet"),
    ("mini_quiz", "Mini Quiz"),
)


def _load_component(path: Path) -> dict:
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _text(value) -> str:
    return str(value or "").strip()


def _faq_band_counts(faqs: list) -> dict[str, int]:
    counts = {key: 0 for key in FAQ_PREFIXES}
    for item in faqs:
        if not isinstance(item, dict):
            continue
        question = _text(item.get("question"))
        for key, pattern in FAQ_PREFIXES.items():
            if pattern.search(question):
                counts[key] += 1
    return counts


def _has_pinout(comp: dict) -> bool:
    pinout = comp.get("pinout") or []
    pins = comp.get("pins") or []
    if pinout and isinstance(pinout, list):
        return len(pinout) >= 1
    return bool(pins)


def _has_code(comp: dict) -> bool:
    code = comp.get("code") or {}
    if isinstance(code, dict) and _text(code.get("content")):
        return True
    return bool(_text(comp.get("example_code")))


def _has_wiring(comp: dict) -> bool:
    wiring = comp.get("wiring") or {}
    if not isinstance(wiring, dict):
        return False
    return bool(wiring.get("steps") or _text(wiring.get("summary")))


def _section_presence(comp: dict) -> dict[str, bool]:
    faqs = comp.get("faqs") or []
    bands = _faq_band_counts(faqs if isinstance(faqs, list) else [])
    quick_facts = comp.get("quick_facts") or []

    return {
        "eli12": bool(_text(comp.get("eli12"))),
        "quick_facts": isinstance(quick_facts, list) and len(quick_facts) >= 4,
        "pinout": _has_pinout(comp),
        "troubleshooting": isinstance(comp.get("troubleshooting"), list) and len(comp.get("troubleshooting") or []) >= 2,
        "faqs": isinstance(faqs, list) and len(faqs) >= 4,
        "glossary": bands["glossary"] >= 2,
        "parent_tips": bands["parent_tips"] >= 2,
        "teacher_tips": bands["teacher_tips"] >= 2,
        "challenge": bands["challenge"] >= 2,
        "mini_quiz": bands["mini_quiz"] >= 2,
        "related_guides": isinstance(comp.get("related_guides"), list) and len(comp.get("related_guides") or []) >= 2,
        "related_projects": isinstance(comp.get("related_projects"), list) and len(comp.get("related_projects") or []) >= 1,
        "code": _has_code(comp),
        "output": bool(_text(comp.get("output"))),
        "wiring": _has_wiring(comp),
        "common_mistakes": isinstance(comp.get("common_mistakes"), list) and len(comp.get("common_mistakes") or []) >= 3,
        "specs": isinstance(comp.get("specs"), list) and len(comp.get("specs") or []) >= 5,
        "datasheet": bool(_text(comp.get("datasheet_url"))),
    }


def _missing_sections(presence: dict[str, bool]) -> list[str]:
    missing: list[str] = []
    for key, label in REQUIRED_CHECKS:
        if not presence.get(key, False):
            missing.append(label)
    for key, label in GOLDEN_OPTIONAL:
        if not presence.get(key, False):
            missing.append(f"{label} (recommended)")
    return missing


def _warnings(comp: dict, presence: dict[str, bool]) -> list[str]:
    warnings: list[str] = []
    for key, label in REQUIRED_CHECKS:
        if not presence.get(key, False):
            warnings.append(f"Missing {label}")
    wiring = comp.get("wiring") or {}
    if isinstance(wiring, dict) and wiring and not _text(wiring.get("illustration_alt")):
        warnings.append("Wiring section missing illustration_alt (accessibility)")
    if _text(comp.get("image", "")).startswith("http"):
        warnings.append("Image uses external CDN URL — migrate to /assets/visuals/ when ready")
    if presence.get("pinout") and not comp.get("pinout") and comp.get("pins"):
        warnings.append("Using legacy pins list — upgrade to structured pinout rows")
    if _has_code(comp) and not comp.get("code") and comp.get("example_code"):
        warnings.append("Using legacy example_code — upgrade to code block with filename")
    return warnings


def _score_child(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    eli12 = _text(comp.get("eli12"))
    if len(eli12) >= 200:
        score += 25
    elif eli12:
        score += 12
    if presence["quick_facts"]:
        score += 20
    if presence["output"] and len(_text(comp.get("output"))) >= 80:
        score += 15
    elif presence["output"]:
        score += 8
    if presence["challenge"]:
        score += 15
    if presence["mini_quiz"]:
        score += 10
    if presence["common_mistakes"]:
        score += 10
    if len(_text(comp.get("summary"))) >= 80:
        score += 5
    return min(100, score)


def _score_parent(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    if presence["parent_tips"]:
        score += 30
    if presence["troubleshooting"]:
        score += 25
    specs_text = " ".join(str(s) for s in (comp.get("specs") or [])).lower()
    mistakes = " ".join(
        _text(i.get("text") if isinstance(i, dict) else i) for i in (comp.get("common_mistakes") or [])
    ).lower()
    if "safety" in specs_text or "unplug" in specs_text or "safety" in mistakes or "unplug" in mistakes:
        score += 20
    if presence["datasheet"]:
        score += 15
    if presence["related_guides"]:
        score += 10
    return min(100, score)


def _score_teacher(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    if presence["teacher_tips"]:
        score += 30
    guides = comp.get("related_guides") or []
    if isinstance(guides, list) and len(guides) >= 2:
        score += 20
    if presence["related_projects"]:
        score += 15
    if presence["datasheet"]:
        score += 15
    if presence["quick_facts"]:
        score += 10
    if presence["specs"]:
        score += 10
    return min(100, score)


def _score_engineering(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    if presence["pinout"]:
        score += 20
    if presence["code"]:
        score += 20
    if presence["wiring"]:
        score += 15
    troubleshooting = comp.get("troubleshooting") or []
    if isinstance(troubleshooting, list) and len(troubleshooting) >= 3:
        score += 20
    elif presence["troubleshooting"]:
        score += 10
    specs_text = " ".join(str(s) for s in (comp.get("specs") or [])).lower()
    if "voltage" in specs_text or "3.3" in specs_text:
        score += 10
    if "communication" in specs_text or "i2c" in specs_text or "protocol" in specs_text or "digital" in specs_text:
        score += 5
    if _text(comp.get("library")):
        score += 10
    return min(100, score)


def _score_seo(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    faqs = comp.get("faqs") or []
    if isinstance(faqs, list):
        if len(faqs) >= 10:
            score += 25
        elif len(faqs) >= 4:
            score += 15
        seo_hits = 0
        for item in faqs:
            if not isinstance(item, dict):
                continue
            q = _text(item.get("question")).lower()
            if any(k in q for k in ("what is", "how do", "how to", "connect", "vs ", "compare", "accurate", "work")):
                seo_hits += 1
        score += min(25, seo_hits * 5)
    summary = _text(comp.get("summary")).lower()
    if summary and len(summary) >= 60:
        score += 15
    guides = comp.get("related_guides") or []
    projects = comp.get("related_projects") or []
    described = 0
    for item in list(guides) + list(projects):
        if isinstance(item, dict) and _text(item.get("description")):
            described += 1
    score += min(20, described * 5)
    specs = comp.get("specs") or []
    specs_joined = " ".join(str(s).lower() for s in specs)
    if "real-world" in specs_joined or "uses" in specs_joined or "comparison" in specs_joined or " vs " in specs_joined:
        score += 15
    return min(100, score)


def _score_accessibility(comp: dict, presence: dict[str, bool]) -> int:
    score = 0
    wiring = comp.get("wiring") or {}
    if isinstance(wiring, dict) and _text(wiring.get("illustration_alt")):
        score += 25
    if _text(comp.get("image")):
        score += 20
    if len(_text(comp.get("eli12"))) >= 120:
        score += 20
    if presence["output"] and len(_text(comp.get("output"))) >= 60:
        score += 20
    if presence["glossary"]:
        score += 15
    return min(100, score)


def analyze_component(comp: dict) -> dict:
    presence = _section_presence(comp)
    scores = {
        "child_experience": _score_child(comp, presence),
        "parent_experience": _score_parent(comp, presence),
        "teacher_experience": _score_teacher(comp, presence),
        "engineering": _score_engineering(comp, presence),
        "seo": _score_seo(comp, presence),
        "accessibility": _score_accessibility(comp, presence),
    }
    scores["overall"] = round(sum(scores.values()) / len(scores))
    missing = _missing_sections(presence)
    warnings = _warnings(comp, presence)
    priority = "LOW"
    if scores["overall"] < 50 or not presence["eli12"] or not presence["code"]:
        priority = "HIGH"
    elif scores["overall"] < 75:
        priority = "MEDIUM"
    recommendations = _recommendations(comp, presence, scores)
    return {
        "slug": comp.get("slug", path_stem(comp)),
        "name": comp.get("name", comp.get("slug", "?")),
        "scores": scores,
        "missing_sections": missing,
        "warnings": warnings,
        "priority": priority,
        "recommendations": recommendations,
        "presence": presence,
    }


def path_stem(comp: dict) -> str:
    return _text(comp.get("slug")) or "?"


def _recommendations(comp: dict, presence: dict[str, bool], scores: dict) -> list[str]:
    recs: list[str] = []
    if not presence["eli12"]:
        recs.append("Add multi-paragraph eli12 with analogy and a curiosity hook.")
    if not presence["quick_facts"]:
        recs.append("Add at least 4 quick_facts tiles (Measures, Pins, Best for, Voltage or speed).")
    if not presence["pinout"]:
        recs.append("Replace flat pins list with structured pinout rows (pin, role, connects, note).")
    if not presence["glossary"]:
        recs.append('Add 2+ FAQ entries prefixed "Glossary —".')
    if not presence["parent_tips"]:
        recs.append('Add 2+ FAQ entries prefixed "Parent tips —" (safety, parts, time).')
    if not presence["teacher_tips"]:
        recs.append('Add 2+ FAQ entries prefixed "Teacher tips —" (period fit, objectives, assessment).')
    if not presence["challenge"]:
        recs.append('Add 2+ FAQ entries prefixed "Challenge yourself —".')
    if not presence["troubleshooting"]:
        recs.append("Add at least 2 problem/fix troubleshooting pairs.")
    if not presence["related_guides"]:
        recs.append("Link to 2+ related guides with descriptions.")
    if not presence["related_projects"]:
        recs.append("Link to at least 1 related project with description.")
    if not presence["wiring"]:
        recs.append("Add wiring block with illustration_alt, summary, and numbered steps.")
    if not presence["common_mistakes"]:
        recs.append("Add 3+ common_mistakes entries.")
    if scores["seo"] < 60:
        recs.append("Expand FAQs with natural SEO questions (What is…? How to connect…?).")
    if _text(comp.get("image", "")).startswith("http"):
        recs.append("Plan migration to local /assets/visuals/components/photos/ image.")
    if not recs:
        recs.append("Minor polish only — align with DHT22 depth where applicable.")
    return recs[:8]


def analyze_all_components() -> list[dict]:
    results: list[dict] = []
    for path in sorted(COMPONENTS_DIR.glob("*.yaml")):
        if path.stem == TEMPLATE_SLUG:
            continue
        comp = _load_component(path)
        if not comp:
            continue
        comp.setdefault("slug", path.stem)
        results.append(analyze_component(comp))
    return results


def write_report(results: list[dict]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    benchmark = next((r for r in results if r["slug"] == "dht22"), None)

    lines = [
        "# Component Quality Report",
        "",
        f"Generated: {generated}",
        "",
        "Benchmark: **DHT22** is the golden standard (`content/components/dht22.yaml`).",
        "",
        "Standard: [GOLDEN_COMPONENT_STANDARD.md](../editorial/GOLDEN_COMPONENT_STANDARD.md)",
        "",
        "Run `py tools/validate_component_quality.py` to refresh this report.",
        "",
    ]

    if benchmark:
        bs = benchmark["scores"]
        lines.extend(
            [
                "## Golden Benchmark (DHT22)",
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
            "| Component | Overall | Priority | Missing required |",
            "|-----------|---------|----------|------------------|",
        ]
    )
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        required_missing = sum(
            1 for key, label in REQUIRED_CHECKS if label in r["missing_sections"]
        )
        lines.append(
            f"| {r['name']} | {r['scores']['overall']}/100 | {r['priority']} | {required_missing} |"
        )
    lines.append("")

    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        s = r["scores"]
        lines.extend(
            [
                f"## {r['name']} (`{r['slug']}`)",
                "",
                f"**Overall score:** {s['overall']}/100 · **Priority:** {r['priority']}",
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

    report_path = REPORTS_DIR / "component-quality-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = ROOT / "component-quality-report.json"
    payload = {
        "generated_at": generated,
        "benchmark_slug": "dht22",
        "components": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    results = analyze_all_components()
    write_report(results)

    print("Component quality report")
    print(f"  Wrote {REPORTS_DIR / 'component-quality-report.md'}")
    print(f"  Wrote {ROOT / 'component-quality-report.json'}")
    print()
    for r in sorted(results, key=lambda x: x["scores"]["overall"]):
        missing_req = [label for key, label in REQUIRED_CHECKS if label in r["missing_sections"]]
        print(
            f"  {r['slug']}: {r['scores']['overall']}/100 ({r['priority']})"
            + (f" — missing: {', '.join(missing_req)}" if missing_req else "")
        )
        for w in r["warnings"]:
            print(f"    WARN: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
