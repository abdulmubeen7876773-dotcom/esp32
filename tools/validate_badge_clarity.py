from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

BADGE_CLASSES = {
    "premium-icon",
    "path-icon",
    "project-section-icon",
    "mission-section-icon",
    "component-section-icon",
    "project-part-icon",
    "project-component-icon",
    "project-hero-icon",
    "project-mission-icon",
    "mission-illustration-icon",
}

PROHIBITED = {
    "SAFE",
    "KIT",
    "PACE",
    "PLAN",
    "WORK",
    "TASK",
    "OUT",
    "DL",
    "MCQ",
    "RUB",
    "EXAM",
    "LAB",
    "USE",
    "TALK",
    "BOT",
    "IND",
    "EDU",
    "PRINT",
    "TEAM",
    "DEMO",
    "NOTE",
}

TECHNICAL_OK = {
    "AC",
    "ADC",
    "AI",
    "BLE",
    "CNC",
    "DC",
    "ECG",
    "ESP32",
    "FAQ",
    "GPS",
    "GPIO",
    "I2C",
    "IR",
    "LED",
    "IoT",
    "MQTT",
    "OK",
    "PIN",
    "PWM",
    "QR",
    "RFID",
    "RSSI",
    "RGB",
    "SPI",
    "UART",
    "UV",
}

VERIFICATION_PAGES = {
    "google926bc78bc682aaf9.html",
    "googlec0cbd82255f45946.html",
    "pinterest-f71bc.html",
}


def normalized_classes(raw: str | None) -> set[str]:
    return {part.strip() for part in str(raw or "").split() if part.strip()}


class BadgeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[dict] = []
        self.badges: list[dict[str, str]] = []
        self._capture: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = normalized_classes(attr.get("class"))
        node = {"tag": tag, "classes": classes, "h3": "", "text": ""}
        self.stack.append(node)
        if tag == "span" and classes & BADGE_CLASSES:
            title = ""
            for parent in reversed(self.stack[:-1]):
                if parent["tag"] == "article":
                    title = parent.get("h3", "")
                    break
            self._capture = {"classes": " ".join(sorted(classes & BADGE_CLASSES)), "title": title, "text": ""}

    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag == "span":
            self.badges.append(
                {
                    "classes": self._capture["classes"],
                    "title": re.sub(r"\s+", " ", self._capture.get("title", "")).strip(),
                    "text": re.sub(r"\s+", " ", self._capture.get("text", "")).strip(),
                }
            )
            self._capture = None
        if self.stack:
            node = self.stack.pop()
            if node["tag"] == "h3":
                for parent in reversed(self.stack):
                    if parent["tag"] == "article" and not parent.get("h3"):
                        parent["h3"] = re.sub(r"\s+", " ", node.get("text", "")).strip()
                        break
            if self.stack:
                self.stack[-1]["text"] += node.get("text", "")

    def handle_data(self, data: str) -> None:
        if self.stack:
            self.stack[-1]["text"] += data
        if self._capture is not None:
            self._capture["text"] += data


def public_pages() -> list[Path]:
    pages = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or "_archive" in rel.parts or path.name in VERIFICATION_PAGES:
            continue
        pages.append(path)
    return pages


def issue_type(text: str) -> str:
    if text in PROHIBITED:
        return "prohibited-internal-badge"
    if re.fullmatch(r"[A-Z0-9]{2,5}", text) and text not in TECHNICAL_OK and not re.fullmatch(r"\d+", text):
        return "unexplained-uppercase-badge"
    return ""


def main() -> int:
    issues: list[str] = []
    for page in public_pages():
        parser = BadgeParser()
        parser.feed(page.read_text(encoding="utf-8", errors="ignore"))
        for badge in parser.badges:
            text = badge["text"]
            kind = issue_type(text)
            if kind:
                issues.append(
                    f"{page.relative_to(ROOT)}\t{badge.get('title') or '(section)'}\t{text}\t{kind}"
                )

    if issues:
        print("Badge clarity validation failed:")
        print("page\tcard title\tvisible badge\tissue type")
        for item in issues:
            print(item)
        return 1

    print(f"Badge clarity validation passed across {len(public_pages())} public pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
