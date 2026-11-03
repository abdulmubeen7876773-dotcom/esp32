"""Copy reader-facing static files into a fresh deployment directory.

Sources, historical backups, audit reports and component review inputs stay in
the repository. This does not delete or edit any source files.
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIRS = {"assets", "category", "components", "guides", "projects"}
ROOT_EXTENSIONS = {".html", ".css", ".js", ".xml", ".svg", ".jpg", ".png", ".webp"}
ROOT_FILES = {".nojekyll", "CNAME", "ads.txt", "robots.txt", "projects.json", "search-index.json"}
PROTECTED = {"component images.zip", "esp32-component-master-catalog.backup.csv",
             "esp32-component-master-catalog.csv", "esp32-component-master-catalog.md"}


def public_file(relative: Path) -> bool:
    if relative.name in PROTECTED or "_archive" in relative.parts:
        return False
    if len(relative.parts) == 1:
        return (relative.suffix in ROOT_EXTENSIONS or relative.name in ROOT_FILES
                or relative.name.startswith("esp32engineindex") and relative.suffix == ".txt")
    if relative.parts[:4] == ("assets", "downloads", "guides", "blink-led") and relative.name == "blink_led.ino":
        return True
    if relative.as_posix() in {
        'assets/downloads/guides/timing-review-20261104/dht11_reviewed_6s.ino',
        'assets/downloads/projects/review-fixes-20261103/iot-weather-station.ino',
        'assets/downloads/projects/review-fixes-20261103/line-following-robot.ino',
        'assets/downloads/guides/contributor-media-20261101/button_control_led_code.ino',
        'assets/downloads/guides/contributor-media-20261101/dht11_original_2s.ino',
        'assets/downloads/guides/contributor-media-20261101/floating_gpio27_original.ino',
        'assets/downloads/guides/contributor-media-20261101/floating_gpio27_original.zip',
        'assets/downloads/guides/contributor-media-20261101/oled_hello_maker.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio27-debounce.ino',
        'assets/downloads/guides/contributor-media-20261102/multiple-buttons.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio27-external-pulldown.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio27-internal-pullup.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio34-potentiometer.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio34-ldr-threshold-800.ino',
        'assets/downloads/guides/contributor-media-20261102/gpio18-pwm-led-fade.ino',
        'assets/downloads/guides/contributor-media-20261103/gpio34-oled-values.ino',
        'assets/downloads/guides/contributor-media-20261103/bme280-i2c-readings.ino',
    }:
        return True
    if relative.parts[0] == "assets":
        return relative.suffix.lower() in {".svg", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".ico", ".css", ".js", ".woff", ".woff2", ".ttf", ".mp4", ".pdf"}
    return relative.parts[0] in PUBLIC_DIRS and relative.suffix == ".html"


def package_site(output: Path) -> int:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Deployment output must be outside the repository")
    output.mkdir(parents=True, exist_ok=False)
    count = 0
    candidates = list(ROOT.iterdir())
    for directory in PUBLIC_DIRS:
        candidates.extend((ROOT / directory).rglob("*"))
    for source in sorted(set(candidates)):
        if source.is_file() and not source.is_symlink() and public_file(source.relative_to(ROOT)):
            destination = output / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(f"Packaged {package_site(args.output)} public files into {args.output}")
