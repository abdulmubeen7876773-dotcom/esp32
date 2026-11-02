"""Responsive copies for existing homepage and guide-list artwork."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


def responsive_attributes(src, sizes):
    widths = (480, 768, 1024, 1280)
    path = Path(src)
    variants = []
    for width in widths:
        variant = str(path.with_name(path.stem + "-" + str(width) + path.suffix)).replace("\\", "/")
        if (ROOT / variant.lstrip("/")).is_file():
            variants.append(f"{variant} {width}w")
    if not variants:
        return ""
    # Keep the original as the largest candidate only for known source dimensions.
    original_width = 1672 if path.name == "esp32-workbench.webp" else (1024 if path.name == "guides-hero.webp" else 1408)
    variants.append(f"{src} {original_width}w")
    return f' srcset="{", ".join(variants)}" sizes="{sizes}"'


HOME_HERO_SIZES = "(max-width: 760px) calc(100vw - 36px), (max-width: 1100px) 50vw, 640px"
