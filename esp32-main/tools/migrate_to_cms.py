import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_categories import CATEGORY_INTROS
from cms_loader import CONTENT, PAGES_DIR, PROJECTS_DIR, save_yaml
from site_layout import (
    CSS_VERSION,
    GA4_MEASUREMENT_ID,
    GITHUB_URL,
    CONTACT_ISSUES_URL,
    GSC_VERIFICATION,
    INDEXNOW_KEY,
    ORG_NAME,
    PINTEREST_VERIFICATION,
    PROJECTS_PAGE_SIZE,
    SITE_DOMAIN,
    SITE_NAME,
)

ROOT = Path(__file__).resolve().parent.parent


def load_legacy_parents() -> list[dict]:
    try:
        raw = subprocess.check_output(
            ["git", "show", "HEAD:tools/parent_registry.py"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    ns: dict = {}
    exec(raw, ns)
    return ns.get("PARENTS", [])

SITE_YAML = {
    "site_name": SITE_NAME,
    "org_name": ORG_NAME,
    "site_domain": SITE_DOMAIN,
    "github_url": GITHUB_URL,
    "contact_issues_url": CONTACT_ISSUES_URL,
    "ga4_measurement_id": GA4_MEASUREMENT_ID,
    "gsc_verification": GSC_VERIFICATION,
    "pinterest_verification": PINTEREST_VERIFICATION,
    "indexnow_key": INDEXNOW_KEY,
    "css_version": CSS_VERSION.replace("seo2", "cms1") if "seo" in CSS_VERSION else "20260618-cms1",
    "projects_page_size": PROJECTS_PAGE_SIZE,
}

HOME_YAML = {
    "hero_eyebrow": "ESP32 & IoT Technology Portal",
    "hero_title": "One ESP32. Unlimited Possibilities.",
    "hero_sub": "Build IoT systems, smart automation, robotics, wireless devices, monitoring solutions, and real-world embedded projects.",
    "meta_title": "ESP32 Engine — Build, Connect & Automate with ESP32",
    "meta_description": "Build, connect, and automate with ESP32. 15 parent projects with Beginner, Intermediate, and Advanced stages for makers, students, and engineers.",
}

ABOUT_BODY = """<h1>About ESP32 Engine</h1>
<p>ESP32 Engine is a free educational resource for students, hobbyists, and engineers who want practical ESP32 tutorials in one place. We publish wiring guides, Arduino sketches, parts lists, and step-by-step build instructions for IoT, automation, robotics, and embedded systems.</p>
<h2>Editorial standards</h2>
<ul>
<li>Every tutorial includes a parts list, wiring table, working code, and demonstration steps.</li>
<li>Projects are organized by category and difficulty so you can start at the right skill level.</li>
<li>We focus on reproducible builds you can test on a breadboard before adding Wi-Fi or cloud features.</li>
<li>Corrections and improvements are tracked openly on <a href="https://github.com/abdulmubeen7876773-dotcom/esp32" target="_blank" rel="noopener">GitHub</a>.</li>
</ul>
<h2>Who maintains this site</h2>
<p>ESP32 Engine is maintained by embedded systems enthusiasts who document real ESP32 builds for learning and prototyping. We review tutorials for wiring clarity, code structure, and safety notes before publishing.</p>
<h2>Contact &amp; feedback</h2>
<p>Report errors, suggest topics, or ask questions on our <a href="contact.html">Contact</a> page or via <a href="https://github.com/abdulmubeen7876773-dotcom/esp32/issues" target="_blank" rel="noopener">GitHub Issues</a>.</p>"""

CONTACT_BODY = """<h1>Contact</h1>
<p>We welcome questions, feedback, and tutorial suggestions. For the fastest response, include the project page URL and a short description of your issue.</p>
<p><strong>GitHub Issues:</strong> <a href="https://github.com/abdulmubeen7876773-dotcom/esp32/issues" target="_blank" rel="noopener">github.com/abdulmubeen7876773-dotcom/esp32/issues</a></p>
<p><strong>Repository:</strong> <a href="https://github.com/abdulmubeen7876773-dotcom/esp32" target="_blank" rel="noopener">github.com/abdulmubeen7876773-dotcom/esp32</a></p>
<p>We aim to respond within a few business days.</p>"""

PRIVACY_BODY = """<h1>Privacy Policy</h1>
<p>Last updated: June 2026</p>
<p>ESP32 Engine (https://esp32engine.com) is an educational website. We do not require account registration and we do not sell personal information.</p>
<h2>Information we collect</h2>
<ul>
<li><strong>Hosting logs:</strong> Our hosting provider may record standard server logs such as browser type, pages viewed, referring URL, and approximate region for security and performance.</li>
<li><strong>Analytics:</strong> If enabled, Google Analytics (GA4) collects anonymized usage data such as pages visited, session duration, and device type to help us improve content.</li>
<li><strong>Contact messages:</strong> If you contact us via GitHub Issues, GitHub processes that information under its own privacy policy.</li>
</ul>
<h2>Cookies</h2>
<p>We may use essential cookies to remember your cookie consent choice. Analytics partners may set additional cookies when you accept optional cookies in our banner.</p>
<p>Questions? Visit our <a href="contact.html">Contact</a> page.</p>"""

DISCLAIMER_BODY = """<h1>Disclaimer</h1>
<p>All tutorials on ESP32 Engine are provided for educational and informational purposes only.</p>
<p>Electronics projects involve risk. Always verify wiring, use appropriate power supplies, and follow safety guidelines when working with mains voltage, motors, pumps, relays, or high-current loads.</p>
<p><strong>Healthcare projects:</strong> Tutorials in the Healthcare category are not medical advice and must not be used for diagnosis, treatment, or patient monitoring.</p>
<p>Code samples are starting points. You are responsible for testing and adapting firmware for your exact hardware and use case.</p>"""


def main():
    CONTENT.mkdir(exist_ok=True)
    PROJECTS_DIR.mkdir(exist_ok=True)
    PAGES_DIR.mkdir(exist_ok=True)

    save_yaml(CONTENT / "site.yaml", SITE_YAML)
    save_yaml(CONTENT / "home.yaml", HOME_YAML)
    save_yaml(
        CONTENT / "categories.yaml",
        {
            "categories": [
                {"name": name, "intro": intro} for name, intro in sorted(CATEGORY_INTROS.items())
            ]
        },
    )

    for p in load_legacy_parents():
        slug = p["slug"]
        data = {
            "slug": slug,
            "title": p["title"],
            "category": p["category"],
            "description": p["description"],
            "source_base": p["source_base"],
            "sensor": p["sensor"],
            "output": p["output"],
            "featured": False,
            "date_published": "2026-06-14",
            "date_modified": "2026-06-18",
            "levels": {},
        }
        save_yaml(PROJECTS_DIR / f"{slug}.yaml", data)

    pages = {
        "about": {
            "slug": "about",
            "nav": "about",
            "title": "About Us | ESP32 Engine",
            "meta_description": "Learn about ESP32 Engine — editorial standards, mission, and ESP32 project guides with three skill levels.",
            "body_html": ABOUT_BODY,
        },
        "contact": {
            "slug": "contact",
            "nav": "contact",
            "title": "Contact | ESP32 Engine",
            "meta_description": "Contact ESP32 Engine for questions, feedback, or collaboration about our ESP32 tutorials.",
            "body_html": CONTACT_BODY,
        },
        "privacy": {
            "slug": "privacy",
            "nav": "about",
            "title": "Privacy Policy | ESP32 Engine",
            "meta_description": "Privacy Policy for ESP32 Engine — cookies, analytics, and how we handle visitor data.",
            "body_html": PRIVACY_BODY,
        },
        "disclaimer": {
            "slug": "disclaimer",
            "nav": "about",
            "title": "Disclaimer | ESP32 Engine",
            "meta_description": "Disclaimer for ESP32 Engine tutorials — educational use, safety, and liability information.",
            "body_html": DISCLAIMER_BODY,
        },
    }
    for slug, data in pages.items():
        save_yaml(PAGES_DIR / f"{slug}.yaml", data)

    print(f"Migrated CMS content to {CONTENT}/")
    print(f"  site.yaml, home.yaml, categories.yaml")
    print(f"  {len(load_legacy_parents())} project YAML files")
    print(f"  {len(pages)} static page YAML files")


if __name__ == "__main__":
    main()
