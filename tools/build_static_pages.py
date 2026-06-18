import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cms_loader import load_pages
from site_layout import (
    SITE_NAME,
    footer_html,
    head_html,
    header_html,
    organization_schema,
    static_page_shell,
    website_schema,
)

ROOT = Path(__file__).resolve().parent.parent


def normalize_body(body: str) -> str:
    body = (body or "").strip()
    if not body:
        return ""
    if body.startswith("  "):
        return body
    return "\n".join(f"  {line}" if line.strip() else line for line in body.splitlines())


def page_schema(slug: str) -> str:
    if slug == "about":
        return organization_schema() + website_schema()
    return organization_schema()


def cms_page_html(page: dict) -> str:
    slug = page["slug"]
    return static_page_shell(
        page.get("nav", "about"),
        page["title"],
        page["meta_description"],
        normalize_body(page.get("body_html", "")),
        f"{slug}.html",
        page_schema(slug),
    )


def not_found_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", f"Page Not Found | {SITE_NAME}", "The page you requested was not found on ESP32 Engine.", canonical_path="404.html")}
</head>
<body>
<main>
{header_html("home")}
<section class="section-block wrap page-head static-page">
  <h1>Page not found</h1>
  <p>The page you requested does not exist or may have moved.</p>
  <p><a class="btn btn-primary" href="index.html">Back to Home</a> · <a class="btn btn-secondary" href="projects.html">Browse Projects</a></p>
</section>
</main>
{footer_html()}
<script src="ui.js" defer></script>
</body>
</html>"""


def main():
    pages = load_pages()
    if not pages:
        raise SystemExit("No CMS pages found in content/pages/. Run tools/migrate_to_cms.py first.")
    for slug, data in pages.items():
        out = ROOT / f"{slug}.html"
        out.write_text(cms_page_html(data), encoding="utf-8")
        print(f"Wrote {slug}.html")
    (ROOT / "404.html").write_text(not_found_page(), encoding="utf-8")
    print("Wrote 404.html")


if __name__ == "__main__":
    main()
