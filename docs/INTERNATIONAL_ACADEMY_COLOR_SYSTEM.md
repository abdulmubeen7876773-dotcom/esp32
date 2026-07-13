# International Academy Color System

## 1. Design objective

ESP32 Engine now uses a calmer international STEM academy color system. The goal is to keep the existing site structure, routes, content, and workflows intact while moving the visual language away from a colorful maker-site style and toward a mature, trustworthy learning platform for students, parents, teachers, and makers.

## 2. Final palette

Brand tokens:

- `--color-brand-primary`: `#081D3A` for primary navy actions, hero depth, and footer identity.
- `--color-brand-primary-hover`: `#0D2A50` for navy hover and dark-mode primary buttons.
- `--color-brand-primary-soft`: `#EAF0F7` for quiet navy-tinted surfaces.
- `--color-brand-secondary`: `#1488A6` for teal interactive emphasis.
- `--color-brand-secondary-hover`: `#0F718B` for teal hover and readable labels.
- `--color-brand-secondary-soft`: `#E7F7FA` for teal-tinted badges and result boxes.
- `--color-accent-learner`: `#F59E0B` for learner highlights and featured badges.
- `--color-accent-learner-hover`: `#D98705` for amber hover states.
- `--color-accent-learner-soft`: `#FFF4D8` for soft featured states.

Semantic tokens:

- Success: `#22C55E` / `#EAF8EF`
- Info: `#2563EB` / `#EAF1FF`
- Warning: `#F59E0B` / `#FFF4D8`
- Danger: `#EF4444` / `#FDECEC`
- Advanced: `#7C3AED` / `#F1EAFE`

Neutral tokens:

- White through neutral 900: `#FFFFFF`, `#FCFDFE`, `#F8FAFC`, `#F1F5F9`, `#E2E8F0`, `#CBD5E1`, `#94A3B8`, `#64748B`, `#475569`, `#334155`, `#1E293B`, `#0F172A`

Dark tokens:

- `--color-dark-bg`: `#071426`
- `--color-dark-surface`: `#0C1D33`
- `--color-dark-surface-raised`: `#112641`
- `--color-dark-border`: `#203653`
- `--color-dark-text`: `#F8FAFC`
- `--color-dark-text-muted`: `#B6C5D8`

## 3. Light mode

Light mode maps page backgrounds to neutral 50, cards to white, muted sections to neutral 25/100, body copy to neutral 600, headings to neutral 900, borders to neutral 200/300, and primary actions to academy navy. Teal is reserved for active links, interactive emphasis, calculator outputs, selected states, and secondary buttons. Amber is reserved for learner or featured emphasis.

## 4. Dark mode

Dark mode uses deep navy-charcoal page backgrounds with raised navy card surfaces, soft blue-gray borders, off-white text, and muted blue-gray secondary text. Teal remains the main interactive accent, while dark primary buttons use approved navy fills with teal borders to preserve AA contrast with white text.

## 5. Component mappings

- Header: near-white surface in light mode, deep navy surface in dark mode, subtle borders, teal active/hover states, consistent search and theme buttons.
- Hero: restrained navy hero background, white headings, muted light body text, amber only for learner highlights.
- Cards: shared white or dark-surface cards, consistent border, radius, and shadow scale across home, project, guide, component, category, search, and tool cards.
- Buttons: navy primary, teal secondary/outline, amber only for featured learner emphasis, dark-mode primary buttons adjusted for AA contrast.
- Badges: beginner maps to success, intermediate to info, advanced to purple, featured to amber, category labels to teal.
- Forms: shared input background, border, placeholder color, and visible focus ring.
- Tables: neutral borders, soft header backgrounds, preserved horizontal scroll behavior.
- Code: dark navy code surface with high-contrast text.
- Footer: calm deep navy, white headings, muted links, teal hover treatment.
- Alerts and calculator outputs: semantic soft surfaces with readable foreground colors.
- Focus states: visible info/teal ring retained for keyboard users in both themes.

## 6. Files changed

CSS:

- `style.css`

JavaScript:

- `ui.js`

Generators:

- `tools/site_layout.py`
- `tools/component_page.py`
- `tools/rebuild_projects.py`
- `tools/rebuild_parents.py`

Templates:

- No separate template files were changed.

Content:

- `content/pages/about.yaml`
- `content/pages/learning.yaml`
- `content/site.yaml`

Tests:

- `tests/ui-ux.spec.ts`

Generated HTML and reports:

- The site was rebuilt through `build.bat`, refreshing public HTML pages, category pages, guide pages, component pages, project pages, sitemap/search output, and generated report artifacts.

## 7. Validation results

- `build.bat`: PASS.
- `validate.bat`: PASS.
- `npm run test:ui`: PASS, 139/139 tests.
- `python tools/validate_badge_clarity.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` passed across 120 public pages.
- `python tools/validate_encoding_integrity.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` passed.
- `python tools/validate_publication_integrity.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` passed: 49 public projects, 1 staged project.
- `python tools/validate_html_integrity.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` passed.
- `python tools/validate_seo.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` passed: 116 pages, 111 sitemap URLs, 0 broken links, 0 broken assets, 0 warnings, 0 errors.
- `python tools/release_validation.py`: direct `python` launcher unavailable on PATH; rerun with `.venv\Scripts\python.exe` exited 0. The batch validation report remains WARN with blocker=0, warning=54, info=300.
- `git diff --check`: PASS; Git printed CRLF working-copy notices for touched text files.

## 8. Remaining visual risks

- Some long-standing quality/report warnings remain outside this color-system sprint, including component guide enhancements, guide quiz completeness, and the staged TinyML project warning.
- Generated reports still show many placeholder visual assets, but this task did not replace assets or change content publishing status.
- A few source-rendered technical SVGs retain purposeful semantic accent colors; the main shared homepage board SVG and component hero SVG were aligned to the academy palette.

## 9. Final Visual Correction Pass

Fixed source-level visual consistency issues without changing the site design, routes, branding, layout system, navigation, SEO strategy, or performance behavior.

- Dark mode: strengthened shared dark card, table, code, form, button, heading, and page-surface rules so representative public pages no longer render white cards or unreadable headings after theme switching.
- Sticky header and Explore bar: added a shared sticky height token and scroll padding/margins so headings and anchor targets are not clipped beneath the combined sticky bars.
- Encoding and headings: expanded the encoding integrity validator for visible mojibake markers and added merged-heading detection for fused labels such as `PARTSComponents Required`.
- Counts: corrected public-facing counts to show 49 public projects, 8 components, 16 missions, 18 guides/resources, 16 categories, with the staged TinyML page excluded from public project counts.
- Card density and hierarchy: tightened project/card text behavior and added subtle shared card accents while preserving the existing compact layout.
- Browser coverage: added Playwright checks for dark-mode readability, sticky anchor visibility, public count consistency, and merged section headings.

Final validation:

- `build.bat`: PASS.
- `validate.bat`: PASS.
- `npm run test:ui`: PASS, 139/139 tests.
- `.venv\Scripts\python.exe tools\validate_badge_clarity.py`: PASS across 120 public pages.
- `.venv\Scripts\python.exe tools\validate_encoding_integrity.py`: PASS.
- `.venv\Scripts\python.exe tools\validate_publication_integrity.py`: PASS, 49 public projects and 1 staged project.
- `.venv\Scripts\python.exe tools\validate_html_integrity.py`: PASS.
- `.venv\Scripts\python.exe tools\validate_seo.py`: PASS, 0 warnings, 0 errors, 0 broken links, 0 broken assets.
- `.venv\Scripts\python.exe tools\release_validation.py`: exited 0. Release report remains WARN with blocker=0, warning=54, info=300 from pre-existing quality/report items.
