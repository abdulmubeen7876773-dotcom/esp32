import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import get_content_store
from site_layout import (
    SITE_NAME,
    SITE_DOMAIN,
    breadcrumb_schema,
    footer_html,
    head_html,
    header_html,
    organization_schema,
    json_ld_script,
    static_page_shell,
    webpage_schema,
    website_schema,
    UI_JS_SRC,
)

ROOT = Path(__file__).resolve().parent.parent


def normalize_body(body: str) -> str:
    body = (body or "").strip()
    if not body:
        return ""
    if body.startswith("  "):
        return body
    return "\n".join(f"  {line}" if line.strip() else line for line in body.splitlines())


def normalize_heading_outline(body: str) -> str:
    if "<h1" not in body or "<h2" in body.split("<h1", 1)[-1].split("<h3", 1)[0]:
        return body
    return body.replace("</h1>", '</h1>\n<h2 class="visually-hidden">Page sections</h2>', 1)


def page_schema(page: dict) -> str:
    slug = page["slug"]
    title = page["title"]
    desc = page["meta_description"]
    crumbs = breadcrumb_schema([("Home", "/"), (title.split("|")[0].strip(), f"{slug}.html")])
    page_types = {
        "contact": "ContactPage",
        "about": "AboutPage",
    }
    page_type = page_types.get(slug, "WebPage")
    schema = organization_schema() + webpage_schema(title, desc, f"{slug}.html", page_type) + crumbs
    if slug == "about":
        schema += website_schema()
    if slug == "author":
        schema += json_ld_script(
            {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": "Abdul Mubeen",
                "url": f"{SITE_DOMAIN}/author.html",
                "worksFor": {"@type": "Organization", "name": "ESP32 Engine", "url": SITE_DOMAIN + "/"},
                "knowsAbout": [
                    "ESP32",
                    "Arduino",
                    "embedded systems education",
                    "electronics prototyping",
                    "STEM learning",
                ],
            }
        )
    return schema


def cms_page_html(page: dict) -> str:
    slug = page["slug"]
    return static_page_shell(
        page.get("nav", slug),
        page["title"],
        page["meta_description"],
        normalize_body(normalize_heading_outline(page.get("body_html", ""))),
        f"{slug}.html",
        page_schema(page),
    )


def not_found_page() -> str:
    schema = organization_schema() + webpage_schema(
        f"Page Not Found | {SITE_NAME}",
        "The page you requested was not found on ESP32 Engine.",
        "404.html",
        "WebPage",
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", f"Page Not Found | {SITE_NAME}", "The page you requested was not found on ESP32 Engine.", canonical_path="404.html", robots="noindex,nofollow", extra_schema=schema)}
</head>
<body>
<main>
{header_html("home")}
<section class="section-block wrap page-head static-page">
  <h1>Page not found</h1>
  <p>The page you requested does not exist or may have moved.</p>
  <p><a class="btn btn-primary" href="/">Back to Home</a> · <a class="btn btn-secondary" href="/projects.html">Browse Projects</a></p>
</section>
</main>
{footer_html()}
<script src="{UI_JS_SRC}" defer></script>
</body>
</html>"""


def main():
    pages = get_content_store().pages()
    if not pages:
        raise SystemExit("No pages found in content/pages/. Add a YAML file under content/pages/.")
    for slug, data in pages.items():
        out = ROOT / f"{slug}.html"
        out.write_text(cms_page_html(data), encoding="utf-8")
        print(f"Wrote {slug}.html")
    (ROOT / "404.html").write_text(not_found_page(), encoding="utf-8")
    print("Wrote 404.html")


if __name__ == "__main__":
    main()
