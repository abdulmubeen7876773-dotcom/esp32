import re


SITE_SUFFIX = " | ESP32 Engine"
PROJECT_HREF_RE = re.compile(r"(?:^|/)projects/([^/#?]+)\.html$")


def is_golden_project(project: dict) -> bool:
    return project.get("format") == "golden" or bool(project.get("project"))


def public_projects(projects: list[dict]) -> list[dict]:
    return [project for project in projects if is_golden_project(project)]


def primary_difficulty(project: dict) -> str:
    project_block = project.get("project") or {}
    value = str(project_block.get("difficulty") or project.get("difficulty") or "").strip()
    if value.lower() in {"beginner", "intermediate", "advanced"}:
        return value.title()
    return "Beginner"


def project_title(project: dict) -> str:
    return str(project.get("title") or project.get("slug") or "").strip()


def project_meta_description(project: dict) -> str:
    """Authoritative long project description.

    Golden projects use meta_description as the source of truth. The fallback keeps
    staged legacy pages buildable while Phase A validation targets Golden pages.
    """
    return str(project.get("meta_description") or project.get("description") or "").strip()


def card_description(project: dict, limit: int = 118) -> str:
    """Deterministically shorten the authoritative description for cards."""
    desc = project_meta_description(project)
    if len(desc) <= limit:
        return desc
    boundary = max(desc.rfind(". ", 0, limit + 1), desc.rfind("? ", 0, limit + 1), desc.rfind("! ", 0, limit + 1))
    if boundary >= 60:
        return desc[: boundary + 1].strip()
    return desc[: max(0, limit - 1)].rstrip(" ,;:-") + "…"


def html_page_title(project: dict) -> str:
    return f"{project_title(project)}{SITE_SUFFIX}"


def breadcrumb_label(project: dict, limit: int = 80) -> str:
    title = project_title(project)
    if len(title) <= limit:
        return title
    return title[: limit - 1].rstrip(" ,;:-") + "…"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def project_slug_from_href(href: str) -> str:
    href = str(href or "").split("#", 1)[0].split("?", 1)[0].strip()
    match = PROJECT_HREF_RE.search(href)
    if match:
        return match.group(1)
    if href and "/" not in href and href.endswith(".html"):
        return href[:-5]
    return ""
