from __future__ import annotations

import argparse
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
# Original approved source archive: 18-july-2026 two folders (2).zip
SOURCE_ROOT = ROOT / "source-assets" / "generated-guide-images" / "2026-07-18"
PUBLIC_ROOT = ROOT / "assets" / "images" / "guides" / "generated"


@dataclass(frozen=True)
class GuideImage:
    incoming: str
    source_name: str
    public_base: str
    crop: tuple[float, float, float, float]


APPROVED_GUIDE_IMAGES = {
    "what-is-esp32": GuideImage(
        "06_Guides_A/1.png",
        "what-is-esp32-overview.png",
        "what-is-esp32-overview",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "blink-led-esp32": GuideImage(
        "06_Guides_A/3.png",
        "blink-led-breadboard.png",
        "blink-led-breadboard",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "environmental-sensors": GuideImage(
        "07-Guides-B/1.png",
        "environmental-sensor-modules.png",
        "environmental-sensor-modules",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "analog-inputs-reading-real-world": GuideImage(
        "07-Guides-B/3.png",
        "analog-input-serial-monitor.png",
        "analog-input-serial-monitor",
        (0.08, 0.0, 0.90, 0.90),
    ),
    "read-temperature-dht22": GuideImage(
        "07-Guides-B/6.png",
        "temperature-sensor-serial-output.png",
        "temperature-sensor-serial-output",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "smart-environment-monitor-capstone": GuideImage(
        "07-Guides-B/7.png",
        "smart-environment-dashboard.png",
        "smart-environment-dashboard",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "installing-arduino-ide-esp32": GuideImage(
        "07-Guides-B/8.png",
        "arduino-ide-esp32-setup.png",
        "arduino-ide-esp32-setup",
        (0.0, 0.0, 0.90, 0.90),
    ),
    "reading-analog-sensors": GuideImage(
        "07-Guides-B/10.png",
        "analog-sensor-bench.png",
        "analog-sensor-bench",
        (0.0, 0.0, 0.82, 0.90),
    ),
}

SIZES = [(1024, 576), (640, 360), (480, 270)]


def find_zip_member(zf: zipfile.ZipFile, name: str) -> str:
    wanted = name.replace("\\", "/").lower()
    matches = [info.filename for info in zf.infolist() if info.filename.replace("\\", "/").lower().endswith(wanted)]
    if not matches:
        raise SystemExit(f"Missing approved guide source image in archive: {name}")
    return matches[0]


def copy_sources_from_archive(archive: Path) -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        for image in APPROVED_GUIDE_IMAGES.values():
            member = find_zip_member(zf, image.incoming)
            target = SOURCE_ROOT / image.source_name
            with zf.open(member) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)


def cover_crop(source: Image.Image, width: int, height: int, crop: tuple[float, float, float, float]) -> Image.Image:
    image = source.convert("RGB")
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


def process_assets() -> None:
    missing = []
    for image in APPROVED_GUIDE_IMAGES.values():
        source = SOURCE_ROOT / image.source_name
        if not source.exists():
            missing.append(str(source))
    if missing:
        raise SystemExit("Missing approved guide source assets:\n" + "\n".join(missing))

    for image in APPROVED_GUIDE_IMAGES.values():
        source = Image.open(SOURCE_ROOT / image.source_name)
        for width, height in SIZES:
            output = PUBLIC_ROOT / f"{image.public_base}-{width}.webp"
            output.parent.mkdir(parents=True, exist_ok=True)
            cover_crop(source, width, height, image.crop).save(output, "WEBP", quality=84, method=6)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, help="Path to the approved guide image zip archive.")
    args = parser.parse_args()
    if args.archive:
        copy_sources_from_archive(args.archive)
    process_assets()


if __name__ == "__main__":
    main()
