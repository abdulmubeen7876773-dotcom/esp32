from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "images" / "heroes" / "home-hero.webp"
OUT = ROOT / "assets" / "images" / "heroes"

SIZES = (640, 1024)


def save_variants() -> None:
    img = Image.open(SRC).convert("RGB")
    for w in SIZES:
        h = round(img.height * (w / img.width))
        resized = img.resize((w, h), Image.Resampling.LANCZOS)
        webp_path = OUT / f"home-hero-{w}.webp"
        avif_path = OUT / f"home-hero-{w}.avif"
        resized.save(webp_path, "WEBP", quality=82, method=6)
        resized.save(avif_path, "AVIF", quality=50)
        print(f"{webp_path.name}: {webp_path.stat().st_size // 1024}KB")
        print(f"{avif_path.name}: {avif_path.stat().st_size // 1024}KB")


if __name__ == "__main__":
    save_variants()
