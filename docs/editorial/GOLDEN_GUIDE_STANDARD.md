# Golden Guide Standard

The ESP32 Engine mission guide is a **guided adventure**, not a tutorial blog post. The reference implementation is `content/guides/blink-led-esp32.yaml` (Mission 1). Every new mission must follow this standard before publication.

**Related:** [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md) · [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md) · [CONTENT_QA_CHECKLIST.md](CONTENT_QA_CHECKLIST.md) · `content/guide-template.yaml`

---

## Purpose

Missions are the core learning loop of ESP32 Engine. A guide page must take a motivated 10–16 year old from **curiosity → confidence → completion → next step** in one scroll. Reference guides (non-mission) use a subset of this standard.

---

## Render order (missions — fixed by template)

Order is defined in `tools/guide_mission.py` → `render_mission_guide()`. **Do not reorder in YAML.**

| # | Section | YAML source |
|---|---------|-------------|
| 1 | Mission card (hero) | `mission.badge`, `mission.icon`, `mission.title`, `lead`, meta |
| 2 | The Story | `mission.story` |
| 3 | Explain Like I'm 12 | `mission.eli12` |
| 4 | Safety | `mission.safety` |
| 5 | What You'll Build | `mission.what_you_build` |
| 6 | Things You'll Need | `mission.things_you_need` |
| 7 | Component Spotlight | Auto from parts with `/components/` links + `component_spotlight_lead` |
| 8 | Concept | `mission.concept` |
| 9 | Wiring Diagram | `mission.wiring` |
| 10 | Code | `mission.code` (+ output preview in sidebar) |
| 11 | Expected Output | `mission.expected_output` |
| 12 | Mini Quiz | `mission.quiz` |
| 13 | Challenge Yourself | `mission.challenge_items` or `mission.challenge` |
| 14 | Mission Complete | `mission.complete` |
| 15 | Continue Your Journey | `mission.next_missions` |

---

## Why order matters

The sequence follows **learning psychology**, not datasheet logic.

```
Hook (card + story) → Trust (safety) → Preview (build + parts)
→ Understand (concept) → Do (wiring + code) → Verify (output)
→ Reflect (quiz) → Extend (challenge) → Pride (complete) → Path (next)
```

| Position | Why it comes here |
|----------|-------------------|
| Story before ELI12 | Emotional hook before explanation — learner commits before jargon |
| Safety before wiring | Parent trust gate before hands touch wires |
| Parts before concept | Concrete objects before abstract GPIO theory |
| Concept before wiring | Mental model before breadboard — reduces wiring errors |
| Code after wiring | Hands built the circuit; code now has physical meaning |
| Output after code | Confirms success criteria before self-test |
| Quiz after output | Assessment only after learner saw what "right" looks like |
| Challenge after quiz | Extension is optional curiosity — never blocks completion |
| Complete before next | Pride moment must land before suggesting another mission |

---

## Section guide — WHY each exists

### Mission card + metadata (`title`, `headline`, `lead`, `meta_description`)

**Why:** Search landing and emotional contract. `lead` is the promise; `meta_description` is the SEO + parent skim line.

**Must:** `format: mission`, `mission_number`, `reading_time`, `proficiency_level`, kid-friendly `lead`.

---

### The Story (`mission.story`)

**Why:** Storytelling converts "homework" into "my mission." The learner is the protagonist — captain, inventor, explorer.

**Must:** 2–4 short paragraphs, present tense, adventure tone, clear stakes ("Mission Control is waiting").

**Avoid:** Textbook definitions, passive voice, specs in the story block.

---

### Explain Like I'm 12 (`mission.eli12`)

**Why:** Plain-language safety net before concept section introduces GPIO, I2C, or protocol names.

**Must:** Bullets or short lines, real-life analogy, no shame language.

---

### Safety (`mission.safety`)

**Why:** Parent trust blocker. First bullet must be **unplug USB before changing wires** for hardware missions.

**Must:** 3+ bullets — voltage limits, supervision, handling notes.

---

### What You'll Build (`mission.what_you_build`)

**Why:** Sets success picture before steps — "what will I have when I'm done?"

**Must:** Bulleted deliverables: circuit + code + proof of learning.

---

### Things You'll Need (`mission.things_you_need`)

**Why:** Scannable prep list for kids, parents, and teachers. Links to component pages build encyclopedia ↔ mission loop.

**Must:** Each item with `item`; link `/components/{slug}.html` when catalog entry exists; `note` for color/size hints.

---

### Component Spotlight (derived from parts + `component_spotlight_lead`)

**Why:** Deepens relationship with the "brain" or sensor part without leaving the mission. One tap to component guide.

**Must:** At least one component link in `things_you_need`; optional `component_spotlight_lead` copy.

---

### Concept (`mission.concept`)

**Why:** "How does it work?" answered simply before code references `pinMode` or libraries.

**Must:** `title`, `body` bullets, `illustration_alt` for accessibility.

---

### Wiring (`mission.wiring`)

**Why:** #1 failure point for beginners. Numbered steps + double-check line match engineering reality.

**Must:** Unplug-first step, one action per step, GPIO labels match code, `illustration_alt`, optional `image` path.

---

### Code (`mission.code`)

**Why:** Copy-paste runnable proof. Notes explain setup vs loop without requiring comment literacy in source.

**Must:** `filename`, `content`, `notes`; pin constants match wiring; short enough for one phone screen scroll.

---

### Expected Output (`mission.expected_output`)

**Why:** Learner knows success looks like before quiz. Includes gentle troubleshooting hint ("If nothing happens…").

**Must:** Describe visible/Serial behavior; mention normal edge cases (onboard LED, etc.).

---

### Mini Quiz (`mission.quiz`)

**Why quizzes exist:** Confidence checks, not exams. Wrong answers teach via `wrong_feedback` + `explanation`. Immediate feedback builds growth mindset.

**Must:** 2–4 questions; 3 options each; `correct` index; `correct_feedback`, `wrong_feedback`, `explanation` on every question.

**Why not skip:** Missions without quiz leave no reflection moment before challenge.

---

### Challenge (`mission.challenge_items` or `mission.challenge`)

**Why challenge exists:** Optional curiosity path for fast finishers. No grades, no blocking. Keeps advanced kids engaged without raising floor difficulty.

**Must:** 2+ `challenge_items` with icon + text, or prose `challenge` with multiple ideas.

**Prefer:** Icon cards (`⚡` speed, `🎨` creative, `🆘` pattern) over single vague paragraph.

---

### Mission Complete (`mission.complete`)

**Why completion exists:** Pride ritual. Learner must feel "I am a maker now" — not just "I finished reading."

**Must:** `subtitle` (emotional), `summary` (what they achieved), `skills` list (learning outcomes for teachers).

---

### Next Mission (`mission.next_missions`)

**Why next mission exists:** Prevents dead-end. Learning path continues with 1–2 clear cards — not a wall of links.

**Must:** 1–2 entries with `slug`, `title`, `description`; forward in difficulty or complementary skill.

---

### Related Projects (`related_projects` — optional root field)

**Why:** Shows capstone destination beyond the next mission. Not required in Mission 1 (Blink LED) but recommended from Mission 2 onward when a golden project uses the same parts.

**Format:** Same as component `related_projects` — `title`, `href`, `description`.

---

### Learning Outcomes (`mission.complete.skills`)

**Why:** Teacher assessment without a test. Skills must match what the mission actually teaches.

**Must:** 2+ concrete skills ("Used GPIO 2 as digital output"), not vague ("Learned ESP32").

---

## Reference guides (non-mission)

Guides without `format: mission` use `intro.story`, `intro.eli12`, `intro.safety`, and HTML `body` content. They are scored separately in the quality report. Mission-specific sections (quiz, wiring, challenge) are not required.

---

## Mission pacing

| Element | Target |
|---------|--------|
| Reading time | Honest 10–20 min for first-build missions |
| Story | 60–120 seconds read |
| Wiring steps | 5–9 steps, one action each |
| Code | ≤ 25 lines for beginner missions |
| Quiz | 2–4 questions |
| Challenge | 2–4 cards |
| Next missions | 1–2 cards |

**Difficulty progression:** Mission N may assume skills from missions 1…N−1. Link prerequisites in `next_missions` chain and component pages.

---

## SEO structure

- `title` — primary keyword + brand suffix
- `meta_description` — mission number, outcome, quiz/challenge mention, age hint
- `keywords` — 3–6 natural phrases
- `headline` — human H1 without SEO stuffing
- Story and ELI12 carry semantic keywords naturally

---

## Quality validation

```
py tools/validate_guide_quality.py
```

Outputs `docs/reports/guide-quality-report.md`. **Golden target:** Blink LED = 100/100 benchmark.

---

## Authoring workflow

1. Copy `content/guide-template.yaml` → `content/guides/your-mission.yaml`
2. Fill all mission blocks; match GPIO in wiring, code, and quiz
3. Run `py tools/build_all.py` — preview `/guides/your-mission.html`
4. Run `py tools/validate_guide_quality.py`
5. Complete [CONTENT_QA_CHECKLIST.md](CONTENT_QA_CHECKLIST.md)

---

## Sign-off

| Role | Question |
|------|----------|
| Child | Did the story make me want to build? Can I pass the quiz without shame? |
| Parent | Is safety clear? Do I know time and parts needed? |
| Teacher | Can I assess with skills checklist in one period? |
| Engineer | Do pins in wiring, code, and quiz agree? |

If any answer is no — revise YAML before publish.
