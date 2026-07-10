from collections import defaultdict
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store
from project_icons import slug_cat
from project_text import is_golden_project

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_GUIDE_TYPES = {"mission", "quick_build", "reference", "classroom_lesson", "troubleshooting"}
SEO_FAQ_RE = re.compile(r"\bwhy\s+(might|would|does)\s+google\b|\bbest\s+esp32\s+project\b", re.I)
PROHIBITED_CLAIM_RE = re.compile(
    r"\b(medical[ -]?grade|clinically|diagnos(?:e|is|tic)|guaranteed|crime prevention|"
    r"tested in classrooms|proven in schools|meets .*curriculum|meets .*standard|"
    r"industrial[ -]?grade|weather warning system)\b",
    re.I,
)
TESTIMONIAL_RE = re.compile(r"\b(testimonial|what parents say|what teachers say|quote from|says:)\b", re.I)


def normalize_question(question: str) -> str:
    value = re.sub(r"[^a-z0-9 ]+", "", str(question or "").lower())
    return re.sub(r"\s+", " ", value).strip()


def json_ld_objects(text: str) -> list[dict]:
    objects = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S | re.I):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            objects.append(value)
    return objects


def main() -> int:
    store = get_content_store()
    errors: list[str] = []

    track_orders: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for guide in store.guides():
        slug = guide.get("slug", "")
        guide_type = guide.get("guide_type") or ("mission" if guide.get("mission") else "reference")
        if guide_type not in ALLOWED_GUIDE_TYPES:
            errors.append(f"{slug}: unknown guide_type {guide_type}")
            continue
        if guide_type == "mission":
            if not guide.get("track_order"):
                errors.append(f"{slug}: mission missing track_order")
            else:
                track = guide.get("track", "core")
                track_orders[track].append((int(guide["track_order"]), slug))
        elif guide.get("track_order"):
            errors.append(f"{slug}: non-mission has track_order")
    for track, items in track_orders.items():
        seen: dict[int, str] = {}
        for order, slug in items:
            if order in seen:
                errors.append(f"track {track}: duplicate track_order {order} on {seen[order]} and {slug}")
            seen[order] = slug

    for guide in store.guides():
        path = ROOT / "guides" / f"{guide['slug']}.html"
        if not path.exists():
            errors.append(f"guide URL missing: guides/{guide['slug']}.html")
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        guide_type = guide.get("guide_type") or ("mission" if guide.get("mission") else "reference")
        if guide_type == "mission":
            expected = f"Mission {int(guide['track_order']):02d}"
            if expected not in html:
                errors.append(f"{guide['slug']}: generated mission label missing {expected}")

    for category_slug in sorted({slug_cat(p.get("category", "")) for p in store.projects() if p.get("category")}):
        path = ROOT / "category" / f"{category_slug}.html"
        if not path.exists():
            errors.append(f"category URL missing: category/{category_slug}.html")
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        for marker in ["site-header", "top-nav", "site-footer", "breadcrumb", "project-card-item", "canonical"]:
            if marker not in html:
                errors.append(f"category/{category_slug}.html missing shared shell marker {marker}")

    question_map: dict[str, list[str]] = defaultdict(list)
    for project in store.projects():
        if not is_golden_project(project):
            continue
        project_block = project.get("project") or {}
        for item in project_block.get("faqs", []) or []:
            if not isinstance(item, dict):
                continue
            question = item.get("question", "")
            if SEO_FAQ_RE.search(question):
                errors.append(f"{project['slug']}: prohibited SEO FAQ {question}")
            normalized = normalize_question(question)
            if normalized:
                question_map[normalized].append(project["slug"])
        page = ROOT / "projects" / f"{project['slug']}.html"
        if page.exists():
            html = page.read_text(encoding="utf-8", errors="ignore")
            visible_faq = 'id="faq"' in html or 'id="faqs"' in html or "project-faq" in html
            schema_faq = any(obj.get("@type") == "FAQPage" for obj in json_ld_objects(html))
            if schema_faq and not visible_faq:
                errors.append(f"{project['slug']}: FAQ schema emitted without visible FAQ section")
    for question, slugs in question_map.items():
        if len(set(slugs)) > 3:
            errors.append(f"generic FAQ repeated on {len(set(slugs))} projects: {question}")

    content_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in list((ROOT / "content").rglob("*.yaml")) + list((ROOT / "content").rglob("*.md"))
    )
    for line in content_text.splitlines():
        if PROHIBITED_CLAIM_RE.search(line):
            lowered = line.lower()
            if any(token in lowered for token in ["not ", "no.", "no ", "must not", "avoid", "educational estimate", "using the project for diagnosis", "claiming guaranteed", "for diagnosis, treatment"]):
                continue
            errors.append(f"prohibited unsupported-claim pattern remains in content: {line.strip()[:140]}")
            break
    testimonial_hits = [
        str(path.relative_to(ROOT))
        for path in list((ROOT / "content").rglob("*.yaml")) + list((ROOT / "content").rglob("*.md"))
        if TESTIMONIAL_RE.search(path.read_text(encoding="utf-8", errors="ignore"))
    ]
    if testimonial_hits:
        errors.append("testimonial-style source text remains: " + ", ".join(testimonial_hits[:8]))

    if errors:
        print("Phase C cleanup validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Phase C cleanup validation passed: {sum(len(v) for v in track_orders.values())} missions, "
        f"{len(store.guides())} guide URLs, category shared shell, FAQ/schema, claims, testimonials."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
