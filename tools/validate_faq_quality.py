from __future__ import annotations

from collections import defaultdict
from html import unescape
from pathlib import Path
import json
import re
import sys

from cms_loader import load_projects
from project_text import is_golden_project


ROOT = Path(__file__).resolve().parent.parent

SEO_DIRECTED_RE = re.compile(
    r"\bwhy\s+(might|would|does)\s+google\b|\bbest\s+esp32\s+project\b|\bchoose this tutorial\b",
    re.I,
)

REMOVED_GENERIC_RE = re.compile(
    r"^(which esp32 board should i use|can i change the gpio pins|can i power .+ from a phone charger|"
    r"can i add wi-?fi|what should i test first|what should i test before installing it permanently|"
    r"why is this the best project|why might google choose this tutorial|should i solder the circuit)\??$",
    re.I,
)

UNSUPPORTED_CLAIM_RE = re.compile(
    r"\b(medical[ -]?grade|clinically|diagnos(?:e|is|tic)|guaranteed|crime prevention|"
    r"tested in classrooms|proven in schools|meets .*curriculum|meets .*standard|"
    r"industrial[ -]?grade|weather warning system)\b",
    re.I,
)

NEGATION_RE = re.compile(
    r"\b(not|no|never|must not|do not|avoid|educational|prototype|estimate|without)\b",
    re.I,
)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", str(value or "")))).strip()


def normalize_question(value: str) -> str:
    value = re.sub(r"[^a-z0-9 ]+", "", str(value or "").lower())
    return re.sub(r"\s+", " ", value).strip()


def json_ld_objects(html: str) -> list[dict]:
    objects: list[dict] = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S | re.I):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            objects.append(value)
    return objects


def visible_faqs(html: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for raw in re.findall(
        r'<details class="accordion-item project-faq-item">(.*?)</details>',
        html,
        re.S | re.I,
    ):
        summary = re.search(r"<summary[^>]*>(.*?)</summary>", raw, re.S | re.I)
        body = re.search(r'<div class="accordion-content">(.*?)</div>', raw, re.S | re.I)
        if summary and body:
            items.append((normalize(summary.group(1)), normalize(body.group(1))))
    return items


def faq_schema(html: str) -> list[tuple[str, str]]:
    for obj in json_ld_objects(html):
        if obj.get("@type") != "FAQPage":
            continue
        rows: list[tuple[str, str]] = []
        for item in obj.get("mainEntity", []) or []:
            if not isinstance(item, dict):
                continue
            answer = item.get("acceptedAnswer") or {}
            rows.append((normalize(item.get("name", "")), normalize(answer.get("text", ""))))
        return rows
    return []


def source_faqs(project: dict) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for item in ((project.get("project") or {}).get("faqs") or []):
        if isinstance(item, dict) and item.get("question") and item.get("answer"):
            rows.append((normalize(item.get("question", "")), normalize(item.get("answer", ""))))
    return rows


def issue(slug: str, question: str, issue_type: str, action: str) -> str:
    q = question or "(page)"
    return f"{slug}\t{q}\t{issue_type}\t{action}"


def main() -> int:
    issues: list[str] = []
    question_map: dict[str, list[tuple[str, str]]] = defaultdict(list)

    golden_projects = [project for project in load_projects() if is_golden_project(project)]
    for project in golden_projects:
        slug = project.get("slug", "")
        source = source_faqs(project)
        if not source:
            issues.append(issue(slug, "", "missing-faq", "Add a FAQ only if the project has a real learner concern."))
            continue

        if len(source) > 5:
            unique_words = {normalize_question(q) for q, _ in source}
            if len(unique_words) < len(source):
                issues.append(issue(slug, "", "large-repetitive-faq", "Reduce overlapping FAQ items."))
            else:
                issues.append(issue(slug, "", "large-faq-review", "Confirm every FAQ is project-specific and non-filler."))

        for question, answer in source:
            normalized = normalize_question(question)
            question_map[normalized].append((slug, question))
            if SEO_DIRECTED_RE.search(question):
                issues.append(issue(slug, question, "seo-directed-question", "Remove SEO-directed wording."))
            if REMOVED_GENERIC_RE.search(question.strip().rstrip("?")):
                issues.append(issue(slug, question, "removed-generic-template", "Replace with a project-specific concern."))
            if UNSUPPORTED_CLAIM_RE.search(question + " " + answer) and not NEGATION_RE.search(question + " " + answer):
                issues.append(issue(slug, question, "unsupported-claim", "Qualify or remove the unsupported claim."))

        page = ROOT / "projects" / f"{slug}.html"
        if not page.exists():
            issues.append(issue(slug, "", "missing-generated-page", "Rebuild the project page."))
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        visible = visible_faqs(html)
        schema = faq_schema(html)
        if source != visible:
            issues.append(issue(slug, "", "visible-faq-mismatch", "Rebuild or align visible FAQ content with source."))
        if source != schema:
            issues.append(issue(slug, "", "schema-faq-mismatch", "Rebuild or align FAQ structured data with source."))

    for normalized, rows in question_map.items():
        slugs = sorted({slug for slug, _ in rows})
        if normalized and len(slugs) > 3:
            sample = rows[0][1]
            issues.append(
                issue(
                    ", ".join(slugs[:5]) + ("..." if len(slugs) > 5 else ""),
                    sample,
                    "duplicate-question",
                    "Keep exact FAQ wording to 3 or fewer unrelated projects.",
                )
            )

    if issues:
        print("FAQ quality validation failed:")
        print("project slug\tFAQ question\tissue type\trecommended action")
        for item in issues:
            print(item)
        return 1

    print(f"FAQ quality validation passed for {len(golden_projects)} Golden projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
