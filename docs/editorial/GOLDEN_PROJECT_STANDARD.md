# Golden Project Standard

The ESP32 Engine build project is a **capstone adventure** — longer than a mission, still kid-first. The reference implementation is `content/projects/esp32-iot-weather-station.yaml` (ESP32 Mini Weather Station). Every new golden project must follow this standard before publication.

**Related:** [GOLDEN_GUIDE_STANDARD.md](GOLDEN_GUIDE_STANDARD.md) · [GOLDEN_COMPONENT_STANDARD.md](GOLDEN_COMPONENT_STANDARD.md) · `content/project-template.yaml`

---

## Purpose

Missions teach one skill in 10–15 minutes. **Projects** combine skills into a real build a learner can finish in one sitting (45–60 min) and show off. A golden project page must take a motivated 10–16 year old from **curiosity → build → debug → pride → next build** in one scroll.

Staged projects (YAML without a `project:` block) are placeholders — not golden. They score separately in the quality report.

---

## Render order (golden — fixed by template)

Order is defined in `tools/project_page.py` → `render_project_body()`. **Do not reorder in YAML.**

| # | Section | YAML source |
|---|---------|-------------|
| 1 | Hero + meta badges | Root `title`, `description`, `category`; `project.icon`, `difficulty`, `age`, `estimated_time`, `budget` |
| 2 | Project Mission card | `project.mission_title`, `project.icon` |
| 3 | The Story | `project.story` |
| 4 | Explain Like I'm 12 | `project.eli12` |
| 5 | For Parents & Teachers | `project.parent_safety` |
| 6 | Learning Support (optional) | `recommended_age`, `adult_supervision`, `skills_practiced`, `learning_outcomes`, `classroom_use`, `parent_prompt`, `mini_experiments`, `screen_free_activity`, `next_challenge` |
| 7 | What You Will Build | `project.what_you_build` |
| 8 | Components List | `project.components` |
| 9 | Related Components | Auto from parts with `/components/` links |
| 10 | Wiring | `project.wiring` |
| 11 | Code | `project.code` |
| 12 | Expected Output | `project.expected_output` |
| 13 | Troubleshooting | `project.troubleshooting` |
| 14 | Common Mistakes | `project.common_mistakes` |
| 15 | Upgrade Ideas | `project.upgrade_ideas` |
| 16 | Related Guides | `project.related_guides` |
| 17 | Related Projects | `project.related_projects` |
| 18 | Project Complete | `project.complete` |

---

## Why order matters

Projects are longer builds. Order follows **trust → prep → do → verify → recover → grow → connect → celebrate**.

```
Hook (hero + story) → Plain language (ELI12) → Parent trust (safety)
→ Preview (build + parts) → Wire → Code → Verify (output)
→ Recover (troubleshooting + mistakes) → Grow (upgrades)
→ Connect (guides + projects) → Pride (complete)
```

| Position | Why it comes here |
|----------|-------------------|
| Story before ELI12 | Emotional commitment before explanation |
| Parent safety before parts | Parent skim gate before shopping list |
| Parts before wiring | Concrete objects before GPIO steps |
| Wiring before code | Circuit exists before `#define` has meaning |
| Output after code | Success criteria before debugging |
| Troubleshooting before mistakes | Fix paths before prevention tips |
| Upgrades after mistakes | Curiosity path for finishers who succeeded |
| Related guides before related projects | Reinforce skills before suggesting harder builds |
| Complete last | Pride moment must not be buried under links |

---

## Section guide — WHY each exists

### Root metadata (`format`, `title`, `description`, `category`)

**Why:** Search landing, project library cards, and parent time budgeting.

**Must:** `format: golden`, kid-friendly `description`, valid `category`, `slug` matching filename.

---

### Project mission card (`project.mission_title`, `project.icon`)

**Why:** Same emotional contract as mission badges — this is a **build**, not a blog article.

**Must:** Active title ("Build Your Mini Weather Station"), emoji icon.

---

### Meta badges (`project.difficulty`, `age`, `estimated_time`, `budget`)

**Why:** Parents and teachers filter by time, cost, and level before starting.

**Must:** Honest `estimated_time` (45–60 min typical), `age` hint, `budget` range.

---

### The Story (`project.story`)

**Why:** Projects take longer than missions — story sustains motivation through wiring and debugging.

**Must:** 2–4 short paragraphs, present tense, real-world connection ("classroom weather stations").

---

### Explain Like I'm 12 (`project.eli12`)

**Why:** Plain-language safety net before wiring steps reference GPIO and libraries.

**Must:** Short paragraphs or bullets, analogy, no shame language.

---

### For Parents & Teachers (`project.parent_safety`)

**Why:** Projects use USB power, breadboards, and sometimes Wi-Fi — parents need a trust block.

**Must:** 3.3 V / no mains, unplug before rewiring, adult supervision note.

---

### What You Will Build (`project.what_you_build`)

**Why:** Sets the finish-line picture — circuit + code + observable outcome.

**Must:** Describe circuit, program behavior, and what success looks like.

---

### Components List (`project.components`)

**Why:** Scannable BOM for kids, parents, and teachers. Links to component pages close the encyclopedia loop.

**Must:** Each item with `item`, `note`; link `/components/{slug}.html` when catalog entry exists; `icon` optional.

---

### Related Components (derived from linked parts)

**Why:** One tap to deep-dive on the sensor or board without leaving the project.

**Must:** At least one component link in `project.components`.

---

### Wiring (`project.wiring`)

**Why:** #1 failure point. Numbered steps + summary + accessibility alt text.

**Must:** Unplug-first step, `illustration_alt`, `summary`, GPIO labels match code.

---

### Code (`project.code`)

**Why:** Copy-paste runnable proof. Filename helps Arduino IDE users.

**Must:** `filename`, `content`; pin constants match wiring.

---

### Expected Output (`project.expected_output`)

**Why:** Learner knows success before opening troubleshooting.

**Must:** Sample Serial/display output, interaction hint ("breathe on the sensor"), gentle failure hint.

---

### Troubleshooting (`project.troubleshooting`)

**Why:** Projects run longer — learners will hit problems. Problem/fix pairs reduce abandon rate.

**Must:** 2+ entries with `problem` and `fix`; most common symptom first.

---

### Common Mistakes (`project.common_mistakes`)

**Why:** Prevention beats recovery — teach what peers got wrong before they repeat it.

**Must:** 3+ entries with `text`; include timing, GPIO mismatch, USB cable type.

---

### Upgrade Ideas (`project.upgrade_ideas`)

**Why:** Projects without extension feel like dead ends. Upgrades keep advanced kids engaged without raising floor difficulty.

**Must:** 2+ ideas spanning display, logging, Wi-Fi, or automation — mark Advanced when needed.

---

### Related Guides (`project.related_guides`)

**Why:** Bridge back to missions that teach prerequisite skills.

**Must:** 2+ entries with `title`, `href`, `description`.

---

### Related Projects (`project.related_projects`)

**Why:** Show the learning path forward — capstone to capstone.

**Must:** 1+ entries with `title`, `href`, `description`.

---

### Project Complete (`project.complete`)

**Why:** Pride ritual + teacher assessment via skills list.

**Must:** `summary` (emotional + technical), `skills` (2+ concrete outcomes).

---

### Root `hardware` block (legacy compatibility)

**Why:** Staged project rebuild pipeline and search index still read root `hardware` for pin metadata.

**Must for golden:** Keep `hardware` in sync with `project.wiring` and code pin constants.

---

## Staged projects (non-golden)

Projects without `format: golden` and without a `project:` block are **staged placeholders**. They appear in the project library but fail golden section checks until upgraded. Do not publish staged pages as finished learning content.

---

## Project pacing

| Element | Target |
|---------|--------|
| Estimated time | Honest 45–60 min for beginner golden projects |
| Story | 60–120 seconds read |
| Wiring steps | 5–7 steps, one action each |
| Code | Runnable in one paste; libraries named in wiring or guides |
| Troubleshooting | 3+ problem/fix pairs |
| Common mistakes | 3–5 entries |
| Upgrade ideas | 3–4 ideas |
| Related guides | 2+ |
| Skills | 3 concrete outcomes |

---

## SEO structure

- `title` — outcome-focused, human readable
- `description` — what you build, sensor/output hint, age-friendly
- `category` — valid library category
- Related guides and projects carry semantic internal links with descriptions

---

## Quality validation

```
py tools/validate_project_quality.py
```

Outputs `docs/reports/project-quality-report.md`. **Golden target:** ESP32 Mini Weather Station = 100/100 benchmark.

---

## Authoring workflow

1. Copy `content/project-template.yaml` → `content/projects/your-project-slug.yaml`
2. Fill all `project:` blocks; sync `hardware` pins with wiring and code
3. Run `py tools/build_all.py` — preview `/projects/your-project-slug.html`
4. Run `py tools/validate_project_quality.py`
5. Compare score against weather station benchmark before publish

---

## Sign-off

| Role | Question |
|------|----------|
| Child | Did the story make me want to finish the build? Can I recover when something breaks? |
| Parent | Do I know time, cost, and safety before we start? |
| Teacher | Can I assess with the skills list in one class period? |
| Engineer | Do pins in hardware, wiring, and code agree? |

If any answer is no — revise YAML before publish.
