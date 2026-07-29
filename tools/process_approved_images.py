from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
# Original approved source archive: 29-July-2026 Three folders.zip
SOURCE_ROOT = ROOT / "source-assets" / "generated-images" / "2026-07-29"
PUBLIC_ROOT = ROOT / "assets" / "images"


@dataclass(frozen=True)
class SourceAsset:
    incoming: str
    source_path: Path


APPROVED_SOURCES = {
    "parents-hero": SourceAsset("08_Parents_Teachers/1.png", SOURCE_ROOT / "parents-teachers" / "parents-hero-home-learning.png"),
    "teachers-starter": SourceAsset("08_Parents_Teachers/2.png", SOURCE_ROOT / "parents-teachers" / "teachers-starter-missions.png"),
    "parents-roadmap": SourceAsset("08_Parents_Teachers/3.png", SOURCE_ROOT / "parents-teachers" / "parents-learning-roadmap.png"),
    "parents-kit": SourceAsset("08_Parents_Teachers/4.png", SOURCE_ROOT / "parents-teachers" / "parents-starter-kit.png"),
    "teachers-hero": SourceAsset("08_Parents_Teachers/5.png", SOURCE_ROOT / "parents-teachers" / "teachers-hero-classroom.png"),
    "parents-confidence": SourceAsset("08_Parents_Teachers/6.png", SOURCE_ROOT / "parents-teachers" / "parents-confidence.png"),
    "teachers-group": SourceAsset("08_Parents_Teachers/7.png", SOURCE_ROOT / "parents-teachers" / "teachers-group-activities.png"),
    "teachers-lab": SourceAsset("08_Parents_Teachers/8.png", SOURCE_ROOT / "parents-teachers" / "teachers-practical-lab.png"),
    "teachers-hub": SourceAsset("08_Parents_Teachers/9.png", SOURCE_ROOT / "parents-teachers" / "teachers-resource-hub.png"),
    "parents-beginner": SourceAsset("08_Parents_Teachers/10.png", SOURCE_ROOT / "parents-teachers" / "parents-beginner-friendly.png"),
    "og-home": SourceAsset("09_Social_OG/1.png", SOURCE_ROOT / "social-og" / "og-home-default.png"),
    "og-projects": SourceAsset("09_Social_OG/2.png", SOURCE_ROOT / "social-og" / "og-projects.png"),
    "og-guides": SourceAsset("09_Social_OG/3.png", SOURCE_ROOT / "social-og" / "og-guides.png"),
    "og-components": SourceAsset("09_Social_OG/4.png", SOURCE_ROOT / "social-og" / "og-components.png"),
    "og-parents": SourceAsset("09_Social_OG/6.png", SOURCE_ROOT / "social-og" / "og-parents.png"),
    "og-teachers": SourceAsset("09_Social_OG/7.png", SOURCE_ROOT / "social-og" / "og-teachers.png"),
    "learning-hero": SourceAsset("10_Learning_Paths/1.png", SOURCE_ROOT / "learning-paths" / "learning-hero.png"),
    "learning-iot": SourceAsset("10_Learning_Paths/2.png", SOURCE_ROOT / "learning-paths" / "learning-iot.png"),
    "learning-robotics": SourceAsset("10_Learning_Paths/3.png", SOURCE_ROOT / "learning-paths" / "learning-robotics.png"),
    "learning-builder": SourceAsset("10_Learning_Paths/4.png", SOURCE_ROOT / "learning-paths" / "learning-builder.png"),
    "learning-explorer": SourceAsset("10_Learning_Paths/5.png", SOURCE_ROOT / "learning-paths" / "learning-explorer.png"),
    "learning-classroom": SourceAsset("10_Learning_Paths/10.png", SOURCE_ROOT / "learning-paths" / "learning-classroom.png"),
}

RESPONSIVE_OUTPUTS = [
    ("parents-hero", "generated/heroes/parents-learning-together", [(640, 360), (1024, 576)], None),
    ("teachers-hero", "generated/heroes/teachers-classroom-esp32", [(640, 360), (1024, 576)], None),
    ("learning-hero", "generated/heroes/learning-paths-esp32", [(640, 360), (1024, 576)], (0.0, 0.0, 0.872, 0.879)),
    ("parents-roadmap", "generated/sections/parents-learning-roadmap", [(640, 360), (1024, 576)], None),
    ("parents-confidence", "generated/sections/parents-confidence", [(640, 360), (1024, 576)], None),
    ("teachers-group", "generated/sections/teachers-group-activities", [(640, 360), (1024, 576)], None),
    ("learning-classroom", "generated/sections/teacher-led-learning", [(640, 360), (1024, 576)], None),
    ("parents-kit", "generated/cards/parents-starter-kit", [(480, 270), (640, 360)], None),
    ("parents-beginner", "generated/cards/parents-beginner-friendly", [(480, 270), (640, 360)], None),
    ("teachers-starter", "generated/cards/teachers-starter-missions", [(480, 270), (640, 360)], None),
    ("teachers-lab", "generated/cards/teachers-practical-lab", [(480, 270), (640, 360)], None),
    ("teachers-hub", "generated/cards/teachers-resource-hub", [(480, 270), (640, 360)], None),
    ("learning-iot", "generated/cards/learning-iot-dashboard", [(480, 270), (640, 360)], None),
    ("learning-robotics", "generated/cards/learning-robotics-workspace", [(480, 270), (640, 360)], None),
    ("learning-builder", "generated/cards/learning-smart-home-builder", [(480, 270), (640, 360)], None),
    ("learning-explorer", "generated/cards/learning-sensors-explorer", [(480, 270), (640, 360)], None),
]

OG_OUTPUTS = [
    ("og-home", "og/esp32-engine-home.webp", "ESP32 Engine", "Learn ESP32 by building real projects."),
    ("og-projects", "og/esp32-project-library.webp", "ESP32 Project Library", "Hands-on builds, wiring tables, and Arduino code."),
    ("og-guides", "og/esp32-learning-guides.webp", "ESP32 Learning Guides", "Step-by-step missions for beginners and classrooms."),
    ("og-components", "og/esp32-component-encyclopedia.webp", "Component Encyclopedia", "Parts explained simply for ESP32 builders."),
    ("og-parents", "og/esp32-for-parents.webp", "For Parents", "Safe, guided electronics learning at home."),
    ("og-teachers", "og/esp32-for-teachers.webp", "For Teachers", "Classroom-ready ESP32 missions and projects."),
]


def copy_sources(staging: Path) -> None:
    for asset in APPROVED_SOURCES.values():
        src = staging / asset.incoming
        if not src.exists():
            raise SystemExit(f"Missing approved source image: {src}")
        asset.source_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, asset.source_path)


def cover_crop(image: Image.Image, width: int, height: int, crop: tuple[float, float, float, float] | None = None) -> Image.Image:
    image = image.convert("RGB")
    if crop:
        left = round(image.width * crop[0])
        top = round(image.height * crop[1])
        right = round(image.width * crop[2])
        bottom = round(image.height * crop[3])
        image = image.crop((left, top, right, bottom))
    source_ratio = image.width / image.height
    target_ratio = width / height
    if source_ratio > target_ratio:
        crop_width = round(image.height * target_ratio)
        left = (image.width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, image.height))
    elif source_ratio < target_ratio:
        crop_height = round(image.width / target_ratio)
        top = (image.height - crop_height) // 2
        image = image.crop((0, top, image.width, top + crop_height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def typeface(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            line = candidate
            continue
        if line:
            lines.append(line)
        line = word
    if line:
        lines.append(line)
    return lines


def create_og(source: Image.Image, title: str, subtitle: str) -> Image.Image:
    base = cover_crop(source, 1200, 630).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 0, 1200, 630), fill=(5, 18, 36, 74))
    draw.rounded_rectangle((72, 72, 760, 558), radius=28, fill=(8, 29, 58, 222), outline=(255, 255, 255, 46), width=2)
    draw.text((116, 116), "ESP32 Engine", font=typeface(34, True), fill=(125, 211, 252))
    title_font = typeface(68, True)
    y = 190
    for line in wrap_text(draw, title, title_font, 560)[:3]:
        draw.text((116, y), line, font=title_font, fill=(255, 255, 255))
        y += 76
    subtitle_font = typeface(31)
    y += 16
    for line in wrap_text(draw, subtitle, subtitle_font, 580)[:2]:
        draw.text((116, y), line, font=subtitle_font, fill=(213, 226, 242))
        y += 42
    draw.rounded_rectangle((116, 486, 344, 526), radius=20, fill=(20, 136, 166, 232))
    draw.text((142, 494), "Learn | Build | Explore", font=typeface(20, True), fill=(255, 255, 255))
    return Image.alpha_composite(base, overlay).convert("RGB")


def save_webp(image: Image.Image, output: Path, quality: int = 82) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "WEBP", quality=quality, method=6)


def process_assets() -> None:
    missing = [str(asset.source_path) for asset in APPROVED_SOURCES.values() if not asset.source_path.exists()]
    if missing:
        raise SystemExit("Missing source assets:\n" + "\n".join(missing))
    for key, rel_base, sizes, crop in RESPONSIVE_OUTPUTS:
        source = Image.open(APPROVED_SOURCES[key].source_path)
        for width, height in sizes:
            out = PUBLIC_ROOT / f"{rel_base}-{width}.webp"
            save_webp(cover_crop(source, width, height, crop), out)
    for key, rel_path, title, subtitle in OG_OUTPUTS:
        source = Image.open(APPROVED_SOURCES[key].source_path)
        save_webp(create_og(source, title, subtitle), PUBLIC_ROOT / rel_path, quality=86)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging", type=Path, help="Folder containing the approved 08/09/10 source image folders.")
    args = parser.parse_args()
    if args.staging:
        copy_sources(args.staging)
    process_assets()


if __name__ == "__main__":
    main()
