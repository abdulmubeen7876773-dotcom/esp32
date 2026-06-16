import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import (
    CONTACT_ISSUES_URL,
    GITHUB_URL,
    ORG_NAME,
    SITE_DOMAIN,
    SITE_NAME,
    footer_html,
    head_html,
    header_html,
    json_ld_script,
    organization_schema,
    static_page_shell,
    website_schema,
)

ROOT = Path(__file__).resolve().parent.parent


def about_page() -> str:
    body = f"""  <h1>About {SITE_NAME}</h1>
  <p>{SITE_NAME} is a free educational resource for students, hobbyists, and engineers who want practical ESP32 tutorials in one place. We publish wiring guides, Arduino sketches, parts lists, and step-by-step build instructions for IoT, automation, robotics, and embedded systems.</p>
  <h2>Editorial standards</h2>
  <ul>
    <li>Every tutorial includes a parts list, wiring table, working code, and demonstration steps.</li>
    <li>Projects are organized by category and difficulty so you can start at the right skill level.</li>
    <li>We focus on reproducible builds you can test on a breadboard before adding Wi-Fi or cloud features.</li>
    <li>Corrections and improvements are tracked openly on <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub</a>.</li>
  </ul>
  <h2>Who maintains this site</h2>
  <p>{SITE_NAME} is maintained by embedded systems enthusiasts who document real ESP32 builds for learning and prototyping. We review tutorials for wiring clarity, code structure, and safety notes before publishing.</p>
  <h2>Contact &amp; feedback</h2>
  <p>Report errors, suggest topics, or ask questions on our <a href="contact.html">Contact</a> page or via <a href="{CONTACT_ISSUES_URL}" target="_blank" rel="noopener">GitHub Issues</a>.</p>"""
    schema = organization_schema() + website_schema()
    return static_page_shell(
        "about",
        f"About Us | {SITE_NAME}",
        f"Learn about {SITE_NAME} — editorial standards, mission, and our 15 parent ESP32 project guides with three skill levels.",
        body,
        "about.html",
        schema,
    )


def contact_page() -> str:
    body = f"""  <h1>Contact</h1>
  <p>We welcome questions, feedback, and tutorial suggestions. For the fastest response, include the project page URL and a short description of your issue.</p>
  <p><strong>GitHub Issues:</strong> <a href="{CONTACT_ISSUES_URL}" target="_blank" rel="noopener">{CONTACT_ISSUES_URL.replace('https://', '')}</a></p>
  <p><strong>Repository:</strong> <a href="{GITHUB_URL}" target="_blank" rel="noopener">{GITHUB_URL.replace('https://', '')}</a></p>
  <p>We aim to respond within a few business days.</p>"""
    return static_page_shell(
        "contact",
        f"Contact | {SITE_NAME}",
        f"Contact {SITE_NAME} for questions, feedback, or collaboration about our ESP32 tutorials.",
        body,
        "contact.html",
        organization_schema(),
    )


def privacy_page() -> str:
    body = f"""  <h1>Privacy Policy</h1>
  <p>Last updated: June 2026</p>
  <p>{SITE_NAME} ({SITE_DOMAIN}) is an educational website. We do not require account registration and we do not sell personal information.</p>
  <h2>Information we collect</h2>
  <ul>
    <li><strong>Hosting logs:</strong> Our hosting provider may record standard server logs such as browser type, pages viewed, referring URL, and approximate region for security and performance.</li>
    <li><strong>Analytics:</strong> If enabled, Google Analytics (GA4) collects anonymized usage data such as pages visited, session duration, and device type to help us improve content.</li>
    <li><strong>Advertising:</strong> If Google AdSense or similar ad services are enabled, they may use cookies or similar technologies to serve and measure ads. See Google's policies for details.</li>
    <li><strong>Contact messages:</strong> If you contact us via GitHub Issues, GitHub processes that information under its own privacy policy.</li>
  </ul>
  <h2>Cookies &amp; similar technologies</h2>
  <p>We may use essential cookies to remember your cookie consent choice. Analytics and advertising partners may set additional cookies when you accept optional cookies in our banner.</p>
  <p>You can control cookies through your browser settings. Rejecting optional cookies limits analytics and personalized advertising but does not block access to tutorials.</p>
  <h2>Third-party services</h2>
  <ul>
    <li>Google Analytics — <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a></li>
    <li>Google AdSense (if enabled) — <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">How Google uses data in advertising</a></li>
    <li>GitHub — <a href="https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement" target="_blank" rel="noopener">GitHub Privacy Statement</a></li>
  </ul>
  <h2>Your choices</h2>
  <ul>
    <li>Opt out of Google personalized ads: <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a></li>
    <li>Industry opt-out (US): <a href="https://optout.networkadvertising.org/" target="_blank" rel="noopener">NAI Opt-Out</a></li>
    <li>Clear site data: remove cookies for {SITE_DOMAIN.replace('https://', '')} in your browser</li>
  </ul>
  <h2>Children's privacy</h2>
  <p>This site is intended for general audiences interested in electronics education. We do not knowingly collect personal information from children under 13.</p>
  <h2>Changes</h2>
  <p>We may update this policy when we add analytics, advertising, or new features. The "Last updated" date will change accordingly.</p>
  <p>Questions? Visit our <a href="contact.html">Contact</a> page.</p>"""
    return static_page_shell(
        "about",
        f"Privacy Policy | {SITE_NAME}",
        f"Privacy Policy for {SITE_NAME} — cookies, analytics, advertising, and how we handle visitor data.",
        body,
        "privacy.html",
    )


def disclaimer_page() -> str:
    body = f"""  <h1>Disclaimer</h1>
  <p>All tutorials on {SITE_NAME} are provided for educational and informational purposes only.</p>
  <p>Electronics projects involve risk. Always verify wiring, use appropriate power supplies, and follow safety guidelines when working with mains voltage, motors, pumps, relays, or high-current loads. Never leave experimental circuits unattended.</p>
  <p><strong>Healthcare projects:</strong> Tutorials in the Healthcare category are not medical advice and must not be used for diagnosis, treatment, or patient monitoring without proper validation and regulatory compliance.</p>
  <p>Code samples are starting points. You are responsible for testing and adapting firmware for your exact hardware, environment, and use case.</p>
  <p>We make reasonable efforts to keep content accurate, but we do not guarantee completeness or fitness for any particular purpose. Use the information at your own risk.</p>"""
    return static_page_shell(
        "about",
        f"Disclaimer | {SITE_NAME}",
        f"Disclaimer for {SITE_NAME} tutorials — educational use, safety, healthcare, and liability information.",
        body,
        "disclaimer.html",
    )


def not_found_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html("", f"Page Not Found | {SITE_NAME}", "The page you requested was not found on ESP32 Project Library.", canonical_path="404.html")}
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
    pages = {
        "about.html": about_page(),
        "contact.html": contact_page(),
        "privacy.html": privacy_page(),
        "disclaimer.html": disclaimer_page(),
        "404.html": not_found_page(),
    }
    for name, html in pages.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print(f"Wrote {name}")


if __name__ == "__main__":
    main()
