import html
import re
from pathlib import Path

LEVEL_KEYS = ("beginner", "intermediate", "advanced")


def _extract_php_string(text: str, pos: int) -> tuple[str, int]:
    if pos >= len(text) or text[pos] not in ("'", '"'):
        return "", pos
    quote = text[pos]
    pos += 1
    out: list[str] = []
    while pos < len(text):
        ch = text[pos]
        if ch == "\\" and pos + 1 < len(text):
            out.append(text[pos + 1])
            pos += 2
            continue
        if ch == quote:
            return "".join(out), pos + 1
        out.append(ch)
        pos += 1
    return "".join(out), pos


def _find_key_string(block: str, key: str) -> str:
    m = re.search(rf"'{re.escape(key)}'\s*=>\s*", block)
    if not m:
        return ""
    return _extract_php_string(block, m.end())[0]


def _find_level_block(project_block: str, level: str) -> str:
    m = re.search(rf"'{level}'\s*=>\s*\[", project_block)
    if not m:
        return ""
    start = m.end() - 1
    depth = 0
    for i in range(start, len(project_block)):
        ch = project_block[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return project_block[start : i + 1]
    return ""


def _parse_string_list(block: str, key: str) -> list[str]:
    m = re.search(rf"'{re.escape(key)}'\s*=>\s*\[", block)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    for i in range(start, len(block)):
        ch = block[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                inner = block[start + 1 : i]
                items = []
                for sm in re.finditer(r"'((?:\\'|[^'])*)'", inner):
                    items.append(sm.group(1).replace("\\'", "'"))
                return items
    return []


def _parse_components(block: str) -> list[str]:
    m = re.search(r"'components'\s*=>\s*\[", block)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    for i in range(start, len(block)):
        ch = block[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                inner = block[start + 1 : i]
                items = []
                for row in re.finditer(
                    r"\[\s*'qty'\s*=>\s*'([^']*)'\s*,\s*'name'\s*=>\s*'((?:\\'|[^'])*)'"
                    r"(?:\s*,\s*'notes'\s*=>\s*'((?:\\'|[^'])*)')?\s*\]",
                    inner,
                    re.S,
                ):
                    qty, name, notes = row.group(1), row.group(2).replace("\\'", "'"), row.group(3) or ""
                    label = f"{qty}× {name}".strip()
                    if notes:
                        label = f"{label} — {notes.replace(chr(39), chr(39))}"
                    items.append(label)
                return items
    return []


def _parse_wiring(block: str) -> list[dict]:
    m = re.search(r"'wiring'\s*=>\s*\[", block)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    for i in range(start, len(block)):
        ch = block[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                inner = block[start + 1 : i]
                rows = []
                for row in re.finditer(
                    r"\[\s*'component'\s*=>\s*'((?:\\'|[^'])*)'\s*,\s*'esp32_pin'\s*=>\s*'((?:\\'|[^'])*)'"
                    r"(?:\s*,\s*'notes'\s*=>\s*'((?:\\'|[^'])*)')?\s*\]",
                    inner,
                    re.S,
                ):
                    rows.append(
                        {
                            "component": row.group(1).replace("\\'", "'"),
                            "pin": row.group(2).replace("\\'", "'"),
                            "note": (row.group(3) or "").replace("\\'", "'"),
                        }
                    )
                return rows
    return []


def _parse_pairs(block: str, key: str, a: str, b: str) -> list[dict]:
    m = re.search(rf"'{re.escape(key)}'\s*=>\s*\[", block)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    for i in range(start, len(block)):
        ch = block[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                inner = block[start + 1 : i]
                rows = []
                for row in re.finditer(
                    rf"\[\s*'{a}'\s*=>\s*'((?:\\'|[^'])*)'\s*,\s*'{b}'\s*=>\s*'((?:\\'|[^'])*)'\s*\]",
                    inner,
                    re.S,
                ):
                    rows.append(
                        {
                            a: row.group(1).replace("\\'", "'"),
                            b: row.group(2).replace("\\'", "'"),
                        }
                    )
                return rows
    return []


def _parse_level(level_block: str) -> dict:
    overview = _find_key_string(level_block, "overview")
    code = _find_key_string(level_block, "code")
    code_filename = _find_key_string(level_block, "code_filename")
    how_rows = _parse_pairs(level_block, "how_it_works", "step", "detail")
    trouble_rows = _parse_pairs(level_block, "troubleshooting", "problem", "solution")
    return {
        "overview_html": overview,
        "components": _parse_components(level_block),
        "wiring": _parse_wiring(level_block),
        "code": code,
        "code_filename": code_filename,
        "how": [f"{r['step']}: {r['detail']}" for r in how_rows] if how_rows else [],
        "apps": _parse_string_list(level_block, "applications"),
        "troubleshooting": [
            {"problem": r["problem"], "fix": r["solution"]} for r in trouble_rows
        ],
        "upgrades": _parse_string_list(level_block, "upgrades"),
    }


def split_projects(text: str) -> list[str]:
    text = re.sub(r"<\?php[\s\S]*?return\s*\[", "", text, count=1)
    text = text.rsplit("];", 1)[0]
    chunks: list[str] = []
    for m in re.finditer(r"'slug'\s*=>\s*'esp32-[^']+'", text):
        chunks.append((m.start(), m.group(0)))
    blocks = []
    for i, (pos, _) in enumerate(chunks):
        end = chunks[i + 1][0] if i + 1 < len(chunks) else len(text)
        start = text.rfind("[", 0, pos)
        if start == -1:
            start = max(0, pos - 200)
        blocks.append(text[start:end].strip().rstrip(","))
    return blocks


def parse_batch_file(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    projects = []
    for block in split_projects(raw):
        slug = _find_key_string(block, "slug")
        if not slug:
            continue
        levels = {}
        for lv in LEVEL_KEYS:
            lb = _find_level_block(block, lv)
            if lb:
                parsed = _parse_level(lb)
                if parsed.get("code"):
                    levels[lv] = parsed
        projects.append(
            {
                "slug": slug,
                "title": _find_key_string(block, "title"),
                "meta_description": _find_key_string(block, "meta_desc"),
                "category": _find_key_string(block, "category"),
                "lead": _find_key_string(block, "lead"),
                "read_time": _find_key_string(block, "read_time"),
                "related": _parse_string_list(block, "related"),
                "levels": levels,
            }
        )
    return projects


def strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()
