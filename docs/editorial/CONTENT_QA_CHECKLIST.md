# ESP32 Engine — Content QA Checklist

Use this before publishing any **guide**, **component page**, or **project page**.

**How to use:** Open the YAML in `content/`, run `py tools/build_all.py`, preview the generated HTML locally or after deploy, then check every item that applies. One failed **blocker** in Safety or Engineer Accuracy → **Do Not Publish**.

**Templates:** Mission guide → `content/guides/blink-led-esp32.yaml` · Component → `content/components/dht22.yaml` · Project → `content/projects/esp32-iot-weather-station.yaml`

**Related:** [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md) · [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md)

---

## Page info

| Field | Value |
|-------|-------|
| **Content type** | ☐ Guide (mission) ☐ Guide (reference) ☐ Component ☐ Project |
| **Slug / file** | `content/…` |
| **Reviewer** | |
| **Date** | |
| **Build run** | ☐ `py tools/build_all.py` passed |

---

## 1. Child readability

*Can a motivated 10–12-year-old follow this without giving up?*

- [ ] Hero lead is one or two short sentences — outcome is clear
- [ ] No paragraph longer than ~4 lines (missions: story, concept, output)
- [ ] Lists use bullets (`- ` in YAML) instead of dense prose
- [ ] Missions include **ELI12** before technical terms appear in concept/code
- [ ] Wiring steps are numbered, one action per step
- [ ] Jargon is introduced after a plain-language name (e.g. "long leg (+)" before "anode")
- [ ] Code is short enough to fit on one phone screen (scroll OK, but not a wall)
- [ ] Expected output describes what success **looks like**, not just "it works"
- [ ] Tone is encouraging — no shame, no "simply" / "obviously"
- [ ] Mission ends with **Mission Complete** pride + clear **Next Mission**

**Reference guides only:** intro story or lead explains why this matters before deep detail.

---

## 2. Parent trust

*Can a parent skim in under 2 minutes and feel OK saying yes?*

- [ ] **Parent Safe** badge is accurate for this content
- [ ] Safety section exists for any hardware mission/project (reference guides: sensible defaults)
- [ ] First safety bullet is **unplug USB before changing wires** (hardware content)
- [ ] 3.3 V / voltage limits stated where GPIO or power pins are used
- [ ] Adult supervision mentioned for USB, small parts, or soldering when relevant
- [ ] `reading_time` is honest for read + first build attempt
- [ ] No links to sign-ups, Discord, or off-site tools without context
- [ ] Parts list does not require expensive or hard-to-find items without a note

---

## 3. Teacher usability

*Can this run in one class period (~45–60 min)?*

- [ ] Section order matches the mission template (no skipped or reordered blocks)
- [ ] **Things You'll Need** is a complete, scannable parts list
- [ ] Wiring steps include a **double-check** line before power-on
- [ ] Quiz has 2–4 questions with explanations (missions)
- [ ] Wrong quiz answers teach — `wrong_feedback` + `explanation` filled in
- [ ] Challenge is optional extension, not required for core learning
- [ ] Skills checklist at end matches what the lesson actually teaches
- [ ] Prerequisite missions or components are linked or named in prose

**Projects (staged):** beginner stage is achievable alone; advanced stages labeled clearly.

---

## 4. Engineer accuracy

*Would you trust this circuit and code on real hardware?*

- [ ] Pin numbers in wiring match pin numbers in code (`#define`, `pinMode`, etc.)
- [ ] GPIO labels consistent: `GPIO 2` in prose, same pin in diagram alt text
- [ ] Resistor values, voltage levels, and polarities are correct
- [ ] Code compiles in Arduino IDE with stated board package (ESP32)
- [ ] No 5 V directly on GPIO; level-shifting noted if 5 V parts are used
- [ ] Component specs match datasheet order of magnitude (not copy-paste errors)
- [ ] `illustration_alt` matches the actual circuit described in steps
- [ ] Troubleshooting hint targets the **most common** failure, not edge cases

**Blockers:** wrong pin, missing resistor, reversed polarity, or code that cannot run → **Do Not Publish**.

---

## 5. Safety

*Non-negotiable for hardware content.*

- [ ] Safety block present (missions/projects with wiring)
- [ ] Unplug-before-rewiring rule included
- [ ] Mains voltage / wall power not implied as beginner-safe without explicit warnings
- [ ] Relay, motor, or battery content includes appropriate cautions
- [ ] No instructions that bypass fuse, insulation, or enclosure when required
- [ ] Soldering or hot tools flagged for adult supervision

**Any unchecked safety item on a hardware page → Do Not Publish until fixed.**

---

## 6. Visual learning

*Diagrams and assets support understanding, not decoration.*

- [ ] Every planned image has `illustration_alt` or `image_alt` in YAML
- [ ] YAML `image:` paths point to files that **exist** OR placeholder frame is intentional
- [ ] Asset paths use site-root format: `/assets/visuals/…`
- [ ] Wiring diagram spec exists in repo if art is still pending (optional but recommended)
- [ ] Component photo has alt text; CDN URLs are temporary-only with migration plan
- [ ] Icons on parts list and sections aid scanning — not random decoration
- [ ] Wire colors in steps match diagram spec when both exist

**Missions/projects:** wiring section has diagram or numbered steps clear enough to build without art.

---

## 7. Accessibility

*Works for keyboard, screen readers, and mobile.*

- [ ] Previewed on mobile width (~375px) — no horizontal overflow on prose
- [ ] Code block has **Copy** button; quiz options are large enough to tap (44px)
- [ ] Alt text describes what the learner sees — does not start with "Image of"
- [ ] Section headings follow logical order (H1 → H2, no skipped levels in template output)
- [ ] Quiz feedback uses `aria-live` (template default — verify it appears after answer)
- [ ] Color is not the only cue for quiz correct/wrong (border + background in template)
- [ ] No essential information conveyed by emoji alone (emoji is supplementary)

---

## 8. SEO basics

*Findable and honest in search results.*

- [ ] `title` follows `{Headline} | ESP32 Engine`
- [ ] `headline` is human-readable (no pipe, no keyword stuffing)
- [ ] `meta_description` is one clear sentence, ≤ ~160 characters
- [ ] `slug` is lowercase, hyphenated, matches filename
- [ ] `date_modified` updated for this publish
- [ ] `keywords` field present and relevant (not spam)
- [ ] `proficiency_level` matches actual difficulty

---

## 9. Internal linking

*Learners can move through the curriculum.*

- [ ] Component parts link to `/components/{slug}.html` where catalog entries exist
- [ ] **Next missions** (or related guides) point to valid slugs
- [ ] Links use site-root paths (`/components/…`, `/guides/…`, `/projects/…`)
- [ ] No broken links in YAML (spot-check in built HTML)
- [ ] Project links to component guides used in `hardware:` or `project:` block
- [ ] Golden project/mission cross-links match curriculum order where intentional

---

## 10. Final publish decision

**Blockers resolved?**

- [ ] `py tools/build_all.py` completes with no validation errors
- [ ] Content validation passed (inventory counts sane)
- [ ] Previewed generated HTML for this page only — not just YAML
- [ ] `date_modified` committed with content changes
- [ ] Asset files committed in same commit as YAML (if images added)

**Reviewer sign-off:**

| Criterion | Pass? |
|-----------|-------|
| Child readability (§1) | ☐ |
| Parent trust (§2) | ☐ |
| Teacher usability (§3) | ☐ |
| Engineer accuracy (§4) | ☐ |
| Safety (§5) | ☐ |
| Visual learning (§6) | ☐ |
| Accessibility (§7) | ☐ |
| SEO basics (§8) | ☐ |
| Internal linking (§9) | ☐ |

---

## Decision

Check **one** outcome:

### ☐ Publish Approved

All applicable sections pass. No safety or accuracy blockers. Ready for `main`.

**Action:** Commit YAML (+ assets), push, verify deploy.

---

### ☐ Needs Revision

Mostly ready — fixable issues only (copy length, missing alt text, one quiz explanation, pending diagram with good placeholder).

**Action:** List revisions below, fix, re-run checklist, do not publish until re-reviewed.

| Issue | Owner | Fixed? |
|-------|-------|--------|
| | | ☐ |
| | | ☐ |

---

### ☐ Do Not Publish

Safety failure, wrong circuit/code, broken build, missing required sections, or content that fails the Core (10–12) readability bar.

**Action:** Do not push to `main`. Open revision task; copy from golden template if structure is wrong.

| Blocker | |
|---------|---|
| | |

---

## Quick reference — minimum bar by type

| Type | Must have |
|------|-----------|
| **Mission guide** | Full `mission:` block, safety, wiring steps, code, quiz, complete, next_missions |
| **Reference guide** | `lead`, body content, sensible reading time |
| **Component** | Name, description, pinout/wiring alt, linkable slug |
| **Project (golden)** | `format: golden`, full `project:` block, hero/wiring/output alt text |
| **Project (staged)** | `hardware:` wiring, three stages, valid category |

**Golden benchmarks:** [reviews/MISSION01_FINAL_REVIEW.md](../reviews/MISSION01_FINAL_REVIEW.md) · `content/guides/blink-led-esp32.yaml`
