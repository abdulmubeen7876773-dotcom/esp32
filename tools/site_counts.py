from functools import lru_cache

from content_store import get_content_store
from project_icons import slug_cat
from project_text import is_golden_project


def _project_difficulty(project: dict) -> str:
    project_block = project.get("project") or {}
    return str(project_block.get("difficulty") or project.get("difficulty") or "").lower()


def _has_text(project: dict, keys: list[str]) -> bool:
    project_block = project.get("project") or {}
    return any(str(project_block.get(key) or project.get(key) or "").strip() for key in keys)


@lru_cache(maxsize=1)
def site_counts() -> dict[str, int]:
    store = get_content_store()
    projects = store.projects()
    golden = [project for project in projects if is_golden_project(project)]
    guides = store.guides()
    categories = {slug_cat(project.get("category", "")) for project in projects if project.get("category")}
    return {
        "total_projects": len(projects),
        "golden_projects": len(golden),
        "staged_projects": len(projects) - len(golden),
        "guides": len(guides),
        "missions": sum(1 for guide in guides if guide.get("kind") == "mission" or guide.get("mission")),
        "components": len(store.components()),
        "categories": len(categories),
        "beginner_projects": sum(1 for project in golden if "beginner" in _project_difficulty(project)),
        "classroom_ready_projects": sum(
            1 for project in golden if _has_text(project, ["classroom_use", "learning_outcomes"])
        ),
        "parent_guided_projects": sum(
            1 for project in golden if _has_text(project, ["adult_supervision", "parent_prompt", "recommended_age"])
        ),
    }


def count_value(name: str) -> int:
    return site_counts()[name]


def render_count_tokens(text: str) -> str:
    out = str(text or "")
    for key, value in site_counts().items():
        out = out.replace("{{" + key + "}}", str(value))
    return out
