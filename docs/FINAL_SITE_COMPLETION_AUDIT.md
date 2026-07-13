# Final Site Completion Audit

Generated: 2026-07-13

## 1. Executive summary

Fixed the confirmed learner-facing integrity issues at source/generator level: mojibake prevention, staged TinyML exclusion, public-only counts, category generation, project difficulty labels, duplicated headings, misleading project claims, search/listing behavior, component taxonomy, sitemap filtering, and validation guardrails.

Intentionally not changed: website design, branding, colors, fonts, navigation model, SEO strategy, analytics strategy, paid dependencies, or non-sprint asset-quality backlog.

Final release state: build and validation pass. Release validation reports WARN with 0 blockers, 54 warnings, and 300 info items for existing asset/roadmap quality backlog outside this sprint.

## 2. Files changed

### Source content

- content/components/relay-module.yaml
- content/guides/blink-led-esp32.yaml
- content/guides/connect-oled-esp32.yaml
- content/guides/installing-arduino-ide-esp32.yaml
- content/guides/read-temperature-dht22.yaml
- content/guides/what-is-esp32.yaml
- content/learning-paths.yaml
- content/pages/about.yaml
- content/pages/downloads.yaml
- content/pages/learning.yaml
- content/pages/news.yaml
- content/pages/parents.yaml
- content/pages/teachers.yaml
- content/projects/esp32-fire-alarm-system.yaml
- content/projects/esp32-smart-energy-meter.yaml
- content/projects/esp32-voice-controlled-relay.yaml

### Generators and shared templates

- tools/build_categories.py
- tools/build_search_index.py
- tools/build_sitemap.py
- tools/component_page.py
- tools/guide_mission.py
- tools/project_page.py
- tools/project_text.py
- tools/rebuild_index.py
- tools/rebuild_parents.py
- tools/release_validation.py
- tools/site_counts.py
- tools/site_layout.py

### JavaScript and CSS

- projects.js
- search.js
- style.css
- ui.js

### Validators and build scripts

- validate.bat
- tools/validate_encoding_integrity.py
- tools/validate_publication_integrity.py
- tools/validate_html_integrity.py
- tools/validate_phase_d_acceptance.py

### Browser verification

- package.json
- package-lock.json
- playwright.config.ts
- tests/ui-ux.spec.ts

### Generated output and reports

- Root pages rebuilt: index, projects, guides, components, learning, parents, teachers, downloads, news, search, sitemap, about, contact, tools, policy pages, 404.
- Project pages rebuilt: 49 public project pages.
- Staged output removed: projects/esp32-tinyml-sound-classifier.html.
- Category pages rebuilt: 16 category pages plus category/index.html.
- Component and guide pages rebuilt.
- search-index.json, projects.json, sitemap.xml, sitemap.html, feed.xml rebuilt.
- docs/reports/*.md and JSON build/report artifacts regenerated.

## 3. Issue-by-issue results

### Character encoding and mojibake

Previous problem: corrupted UTF-8 sequences appeared in source/generated content and could reappear after builds.
Root cause: source and generated files contained double-decoded text; shared head emitted scripts before charset.
Fix applied: repaired confirmed mojibake, removed BOMs, moved `<meta charset="utf-8">` to the top of generated heads, and added encoding validation.
Source files changed: tools/site_layout.py, tools/validate_encoding_integrity.py, affected YAML/Python/CSS/JS source files.
Generated pages affected: all public HTML.
Validation evidence: validate_encoding_integrity.py passed; validate.bat passed.
Final status: Fixed.

### TinyML project integrity

Previous problem: staged TinyML content was reachable through generated output and internal links.
Root cause: listings, search, sitemap, categories, counts, and release validation used all project YAML records.
Fix applied: added shared public project filtering; excluded staged TinyML from generated HTML, search index, sitemap, category pages, project listing, related discovery, and counts. Replaced learning path link with public AI object detector project.
Source files changed: tools/project_text.py, tools/rebuild_parents.py, tools/rebuild_index.py, tools/build_search_index.py, tools/build_sitemap.py, tools/build_categories.py, tools/release_validation.py, content/pages/learning.yaml, content/learning-paths.yaml.
Generated pages affected: projects.html, search-index.json, sitemap.xml, sitemap.html, category pages, learning.html.
Validation evidence: Publication integrity validation passed: 49 public projects, 1 staged project. SEO validation broken links: 0.
Final status: Fixed.

### Smart energy meter claims

Previous problem: public copy implied production-ready or deployable energy metering.
Root cause: legacy metadata used overbroad generated wording.
Fix applied: renamed visible project title to ESP32 Low-Voltage Energy Meter Demo and clarified low-voltage, educational, not billing grade, not direct mains.
Source files changed: content/projects/esp32-smart-energy-meter.yaml.
Generated pages affected: project page, project cards, search index, structured data.
Validation evidence: publication validator checks for misleading energy-meter terms and passed.
Final status: Fixed.

### Voice relay claims

Previous problem: visible metadata claimed voice/wake-word/Google Assistant behavior while the Golden implementation is threshold-based sound triggering.
Root cause: old top-level metadata remained from legacy imported levels.
Fix applied: renamed visible project title to ESP32 Sound-Triggered Relay Demo and corrected meta/search/card copy to sound-triggered relay language.
Source files changed: content/projects/esp32-voice-controlled-relay.yaml.
Generated pages affected: project page, project cards, search index, structured data.
Validation evidence: search index contains ESP32 Sound-Triggered Relay Demo; publication validator passed.
Final status: Fixed.

### Dynamic counts and public totals

Previous problem: visible counts and category totals mixed all records with public records and included staged content.
Root cause: counts were not consistently sourced from one shared public-count helper.
Fix applied: central public counts now flow through site_counts/project_text helpers and page count tokens.
Source files changed: tools/site_counts.py, tools/project_text.py, tools/site_layout.py, tools/rebuild_index.py, tools/build_categories.py, content/pages/about.yaml, content/pages/news.yaml.
Generated pages affected: homepage, about, news, projects, categories, sitemap, footer/stat sections.
Validation evidence: Phase B homepage validation reported total_projects 50, golden_projects 49, staged_projects 1, guides 18, missions 16, components 8, categories 16.
Final status: Fixed.

### Category directory

Previous problem: category directory used stale counts/template behavior and could include staged content.
Root cause: category generation used all project records and did not regenerate category/index.html with current shared shell.
Fix applied: category pages now use public projects only; category/index.html is regenerated with current header/footer and dynamic counts.
Source files changed: tools/build_categories.py.
Generated pages affected: category/*.html and category/index.html.
Validation evidence: validate_phase_c_cleanup.py and publication integrity validation passed.
Final status: Fixed.

### Project library breadcrumb, levels, and filters

Previous problem: project library breadcrumb showed an extra category; cards implied unsupported multi-level implementations.
Root cause: shared category hero and listing defaults treated all projects as multi-level.
Fix applied: project library breadcrumb is Home > Projects; cards use primary difficulty; filters use single supported difficulty; no-results state and hidden-card focus handling added.
Source files changed: tools/site_layout.py, tools/rebuild_index.py, projects.js.
Generated pages affected: projects.html, homepage latest/tutorial sections, projects.json.
Validation evidence: publication validator and HTML integrity validator passed.
Final status: Fixed.

### Duplicated generated headings

Previous problem: section labels could duplicate heading text for screen readers.
Root cause: section helpers rendered decorative label text into heading accessible names.
Fix applied: project, guide, and component section helpers suppress duplicate decorative labels.
Source files changed: tools/project_page.py, tools/guide_mission.py, tools/component_page.py.
Generated pages affected: project, guide, and component detail pages.
Validation evidence: validate_html_integrity.py duplicate heading check passed.
Final status: Fixed.

### Components

Previous problem: relay module was classified as Motors; component listing SVG art had duplicate IDs.
Root cause: source taxonomy and shared SVG IDs were too generic.
Fix applied: relay category changed to Power and Switching; component art SVG IDs now include a unique render suffix.
Source files changed: content/components/relay-module.yaml, tools/component_page.py.
Generated pages affected: components.html and components/relay-module.html.
Validation evidence: validate_html_integrity.py passed.
Final status: Fixed.

### Downloads/resources

Previous problem: downloads page wording implied downloads where the page mostly provides learning resources.
Root cause: static page content used old page label.
Fix applied: learner-facing wording changed to Learning Resources without creating fake downloadable files.
Source files changed: content/pages/downloads.yaml, shared footer wording in tools/site_layout.py.
Generated pages affected: downloads.html and footer links.
Validation evidence: validate_seo.py broken links: 0.
Final status: Fixed.

### Parents, teachers, news, and trust wording

Previous problem: testimonial-like parent quotes and internal "Golden" terminology were visible; news had stale counts/level language.
Root cause: static page content retained old editorial copy.
Fix applied: converted testimonial-style copy into informational statements, replaced internal terminology, and moved counts to dynamic tokens.
Source files changed: content/pages/parents.yaml, content/pages/teachers.yaml, content/pages/news.yaml.
Generated pages affected: parents.html, teachers.html, news.html.
Validation evidence: validate_phase_c_cleanup.py passed.
Final status: Fixed.

### Human sitemap and XML sitemap

Previous problem: human sitemap could expose verification file routes; XML sitemap could include non-public routes if generators used file presence.
Root cause: sitemap generator scanned generated files and old support links.
Fix applied: sitemap generation now uses public project collections and learner-facing support links only.
Source files changed: tools/build_sitemap.py.
Generated pages affected: sitemap.xml and sitemap.html.
Validation evidence: publication validator passed; SEO validation sitemap URLs 111, errors 0.
Final status: Fixed.

### Search behavior

Previous problem: search could leak staged content and rendered result fields without escaping.
Root cause: search index used all projects; frontend output inserted index fields directly.
Fix applied: search index uses public projects only; result rendering escapes title/type/category/description/href; page results use aria-live.
Source files changed: tools/build_search_index.py, search.js.
Generated pages affected: search-index.json and search.html.
Validation evidence: publication validator passed; SEO broken links 0.
Final status: Fixed.

### Accessibility and HTML integrity

Previous problem: duplicate IDs, empty-icon buttons, heading duplication, and staged-link leakage were not guarded.
Root cause: validators did not cover these regressions.
Fix applied: added validate_html_integrity.py and improved project/search/listing behavior.
Source files changed: projects.js, search.js, tools/validate_html_integrity.py.
Generated pages affected: components.html, projects.html, search.html.
Validation evidence: validate_html_integrity.py passed.
Final status: Fixed.

### SEO/indexing technical integrity

Previous problem: stale staged link caused a broken link after TinyML was hidden.
Root cause: learning page and path data pointed at the staged TinyML project.
Fix applied: advanced/AI learning links now target the public ESP32 AI object detector page.
Source files changed: content/pages/learning.yaml, content/learning-paths.yaml.
Generated pages affected: learning.html.
Validation evidence: validate_seo.py errors 0, warnings 0, broken links 0, broken assets 0.
Final status: Fixed.

## 4. Content integrity

- Total project records: 50.
- Public projects: 49, calculated by `project_text.is_golden_project()` / `public_projects()`.
- Staged projects: 1, `esp32-tinyml-sound-classifier`.
- Guides/resources: 18.
- Missions: 16.
- Components: 8.
- Active categories: 16.

Counts are calculated from source collections via shared helpers, not hard-coded into public pages.

## 5. TinyML status

TinyML status: staged and hidden.

Reason: the repository does not contain the full evidence required for a real TinyML project: dataset, training process, trained/exported model, feature extraction, on-device inference evidence, class labels, reproducible build, and evaluation.

Excluded from: generated project pages, projects listing, projects.json, search-index.json, sitemap.xml, sitemap.html, category pages, learning path links, and public counts.

Protected by: tools/validate_publication_integrity.py and release_validation.py public-project filtering.

## 6. Browser results

Playwright browser verification completed with Playwright 1.61.1 and Chromium 149.0.7827.55.

Result: PASS. The full browser suite ran 135 tests with 135 passed and 0 failed.

Executed viewport/page matrix:

- Viewports: 320x568, 375x667, 390x844, 768x1024, 1024x768, 1366x768, 1440x900.
- Pages: homepage, projects, display category, beginner project, safety-sensitive project, guides, guide detail, components, ESP32-CAM, HC-SR04, parents, teachers, tools, resources, contact, about, search, human sitemap.

Interaction checks executed:

- Mobile navigation click and keyboard activation.
- Homepage recommendation controls.
- Project listing filters and load-more behavior.
- Search page and global search overlay.
- Tools calculators.
- Theme toggle.
- Reduced-motion constrained viewport check.

Browser bugs found and fixed:

- Hidden search overlay controls could receive focus before the overlay opened; fixed with `inert` handling in the shared layout/script.
- Detail-page tables and inline code could overflow narrow screens; fixed with shared table/code overflow rules.
- Homepage/top-picks/roadmap decorative elements could be reported outside narrow or clipped viewports; fixed responsive bounds and browser assertions for intentional scroll/clipping.
- Search could break on array-valued index fields; fixed `search.js` normalization.
- Tools calculators could emit `NaN` or `Infinity` for blank/invalid inputs; fixed calculator guards in `content/pages/tools.yaml`.
- Existing validators scanned Playwright report/dependency HTML as public pages; fixed validator skip lists.

Artifacts:

- Playwright report: `playwright-report/index.html`.
- Test artifacts: `test-results/` is ignored and only contains failure artifacts from pre-fix runs when present.

## 7. Validation results

- build.bat: PASS.
- validate.bat: PASS.
- npm run test:ui: PASS, 135 passed.
- validate_badge_clarity.py: PASS across 120 public pages.
- validate_encoding_integrity.py: PASS.
- validate_publication_integrity.py: PASS, 49 public projects and 1 staged project.
- validate_html_integrity.py: PASS.
- validate_seo.py: PASS, 116 public pages, 111 sitemap URLs, 0 duplicate-title warnings, 0 warnings, 0 errors, 0 broken links, 0 broken assets.
- release_validation.py: WARN, 0 blockers, 54 warnings, 300 info items.
- git diff --check: PASS. Only CRLF conversion warnings were printed.
- Browser viewport suite: PASS.

## 8. Remaining risks

- Release validation still reports non-blocking warnings for existing visual asset backlog: external component photos, missing local wiring diagrams, missing concept illustrations, and placeholder visuals.
- TinyML remains staged until real model/training/evaluation evidence exists.

## 9. Final scope confirmation

- No redesign.
- No branding change.
- No unjustified color/font/layout change.
- No paid dependency.
- No staged TinyML publication.
- No manual generated-file-only fixes.
- Fixes are source/generator/validator driven and rebuild-safe.
