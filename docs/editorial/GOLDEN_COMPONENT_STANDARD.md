# Golden Component Standard

The ESP32 Engine component page is a **learning experience**, not a datasheet. The reference implementation is `content/components/dht22.yaml`. Every new or updated component must follow this standard before publication.

**Related:** [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md) · [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md) · [CONTENT_QA_CHECKLIST.md](CONTENT_QA_CHECKLIST.md) · `content/component-template.yaml`

---

## Purpose

Component pages sit between **missions** (hands-on build) and **projects** (capstone builds). A learner lands here to answer:

- What is this part?
- Why would I use it?
- How do I wire it safely?
- What should I expect when it works?

Parents and teachers skim for trust. Engineers skim for pins, voltage, and protocol. The golden standard serves all four audiences in one scroll without feeling like four different documents.

---

## Render order (fixed by template)

The build renders sections in this order. **Do not reorder in YAML** — order is defined in `tools/component_page.py`.

| # | Rendered section | Primary YAML fields |
|---|------------------|---------------------|
| 1 | Hero | `name`, `summary`, `category`, `difficulty`, `icon`, `image` |
| 2 | Explain Like I'm 12 | `eli12` |
| 3 | Quick Facts | `quick_facts` |
| 4 | Technical Specifications | `specs`, `library` |
| 5 | Pinout | `pinout` (preferred) or `pins` |
| 6 | Wiring | `wiring` |
| 7 | Code Example | `code` (preferred) or `example_code` |
| 8 | Expected Output | `output` |
| 9 | Common Mistakes | `common_mistakes` |
| 10 | Troubleshooting | `troubleshooting` |
| 11 | Related Guides | `related_guides` |
| 12 | Related Projects | `related_projects` |
| 13 | FAQ | `faqs` |
| 14 | Downloads | `datasheet_url`, `datasheet_note` |

Extended content (glossary, parent tips, teacher tips, challenge, mini quiz) lives **inside `faqs`** using labeled question prefixes until dedicated template fields exist.

---

## Educational flow

```
Trust (Hero) → Curiosity (ELI12) → Scan (Quick Facts) → Understand (Specs)
→ Connect (Pinout + Wiring) → Do (Code + Output) → Avoid pain (Mistakes + Troubleshooting)
→ Continue learning (Related) → Answer search questions (FAQ) → Go deeper (Datasheet)
```

**Learning psychology**

1. **Hero + ELI12** — Reduce fear before jargon. The learner must feel capable before seeing pin names.
2. **Quick Facts** — Reward skimmers with wins; build confidence with scannable tiles.
3. **Specs** — Satisfy "how does it work?" with layered depth: what → how → inside → voltage → protocol → compare → uses → safety.
4. **Pinout + Wiring** — Transfer from understanding to action. One GPIO in code must match one wire on the breadboard.
5. **Code + Output** — Close the loop: "I ran it and I know success looks like this."
6. **Mistakes + Troubleshooting** — Normalize failure. NaN, blank screens, and loose wires are expected, not shameful.
7. **Related + FAQ** — Branch to missions, projects, and search-intent questions without leaving the ecosystem.

---

## Section guide — WHY each exists

### 1. Hero (`summary`, `name`, `image`)

**Why:** First impression for search, parents, and kids. Answers "Am I in the right place?" in one sentence.

**Must:** Outcome-oriented summary (what it does for *your* project), category badge, difficulty, product photo or icon fallback.

**Avoid:** Datasheet tone, part numbers without context, specs in the hero.

---

### 2. Explain Like I'm 12 (`eli12`)

**Why:** Bridges curiosity to competence. A 12-year-old should understand the *job* of the part before pin labels.

**Must:** Real-life analogy, short paragraphs (max ~4 lines each), one "what would you ask next?" hook, no shame language.

**Avoid:** GPIO jargon before plain words, passive voice, walls of text.

---

### 3. Quick Facts (`quick_facts`)

**Why:** Dual-audience scan card — kids see "3 wires"; teachers see accuracy and logic level.

**Must:** At least 4 labeled facts (measures, pins, best for, speed/voltage, first mission link when applicable).

**Avoid:** Duplicating entire specs list; unlabeled bullet dumps.

---

### 4. Technical Specifications (`specs`, `library`)

**Why:** One section carries multiple teaching layers without separate template blocks. Labels in each bullet act as micro-headings.

**Recommended labeled bullets (from DHT22 golden pattern):**

| Label | Why it exists |
|-------|----------------|
| What it does | Plain answer to "What is this?" for SEO and beginners |
| How it works | Conceptual model before protocol details |
| Inside, simply | Internal working without chip-level datasheet dump |
| Voltage | Safety and ESP32 compatibility — parent/engineer blocker |
| Communication | Protocol choice (I2C, SPI, one-wire, digital) — engineer clarity |
| Range / accuracy | Honest expectations — no invented numbers |
| Sampling / speed | Prevents code bugs (e.g. DHT read too fast) |
| Comparison | DHT22 vs DHT11 style — helps purchase decisions |
| Real-world uses | Motivation — "where will I see this?" |
| Interesting facts | Delight and memory hooks for kids |
| Safety notes | Parent trust — low voltage, unplug rule, supervision |

**Library line:** Tells beginners exactly what to install in Arduino IDE.

---

### 5. Pinout (`pinout`)

**Why:** Wiring errors are the #1 support issue. Structured rows beat prose.

**Must:** Each row — pin name, role, connects to ESP32, note (polarity, pull-up, color hint).

**Prefer** `pinout` over legacy `pins` list — richer for accessibility and teaching.

---

### 6. Wiring (`wiring`)

**Why:** Turns pinout into action. Matches mission template psychology (numbered steps, double-check).

**Must:** `illustration_alt` (describes circuit for screen readers), summary paragraph, numbered steps, unplug-first step, double-check before power-on.

**Asset path:** `/assets/visuals/components/...` when diagram exists; placeholder OK until art lands.

---

### 7. Code Example (`code`)

**Why:** Proof the part works on ESP32 with copy-paste friendly sample.

**Must:** `filename`, `content`, error handling where realistic (e.g. NaN check), pin constants matching wiring section.

**Prefer** `code:` block over legacy `example_code`.

---

### 8. Expected Output (`output`)

**Why:** Success criteria for child and teacher assessment. "It works" is not enough — describe Serial Monitor lines, screen text, or LED behavior.

**Must:** Sample output text, what changes when you interact (breathe on sensor, wave hand), calm guidance if output is wrong.

---

### 9. Common Mistakes (`common_mistakes`)

**Why:** Prevention beats troubleshooting. Short amber callouts for the top 4–7 real-world errors.

**Must:** Wrong GPIO, wrong voltage, timing issues, loose wires — specific to this part.

---

### 10. Troubleshooting (`troubleshooting`)

**Why:** Recovery path when prevention failed. Problem/fix pairs mirror classroom help desk.

**Must:** At least 3 pairs; lead with most common symptom (NaN, blank, stuck zero); fixes are actionable ordered steps.

---

### 11. Related Guides (`related_guides`)

**Why:** Component ↔ mission loop. Learner goes from encyclopedia entry to hands-on mission.

**Must:** At least 2 links with `title`, `href`, `description`; include prerequisite mission when applicable.

---

### 12. Related Projects (`related_projects`)

**Why:** Shows capstone destination — "why am I learning this part?"

**Must:** At least 1 project card with description; prefer projects that actually use the component.

---

### 13. FAQ (`faqs`)

**Why:** SEO, glossary, parent/teacher layers, and micro-assessment without changing the HTML template.

**Strategy — four FAQ bands (use question prefixes):**

| Prefix | Audience | Minimum | Why |
|--------|----------|---------|-----|
| *(none)* | SEO / all | 4+ | Natural questions: What is…? How to connect…? How accurate…? |
| `Glossary —` | Child / all | 2+ | Define RH, GPIO, NaN, Serial Monitor without a separate page |
| `Mini quiz —` | Child | 2+ | Confidence check; answer teaches |
| `Challenge yourself —` | Child | 2+ | Optional extension; curiosity not requirement |
| `Parent tips —` | Parent | 2+ | Safety, parts list, time estimate, supervision |
| `Teacher tips —` | Teacher | 2+ | Period fit, objectives, low-stress assessment |

**SEO:** Write questions people search — "How do I connect X to ESP32?" — without keyword stuffing.

---

### 14. Downloads (`datasheet_url`)

**Why:** Teacher and advanced builder escape hatch. Keeps hero kid-friendly while honoring engineering depth.

**Must:** Valid PDF link when available; `datasheet_note` explains who it's for.

---

## Readability rules

- Second person ("you"), present tense, active voice
- 8–16 word sentences in ELI12 and wiring steps
- Bullets over paragraphs for lists of 3+
- Introduce "pin" before "GPIO pin"
- Never "simply" / "just" / "obviously"
- Do not invent specs — use datasheet values or leave TODO for editorial review

---

## Quality validation

Run before publishing:

```
py tools/validate_component_quality.py
```

Outputs `docs/reports/component-quality-report.md` with scores and missing sections.

**Golden target:** DHT22 score is the benchmark (~90+ overall). New components should reach 75+ before publish; 90+ for flagship parts.

---

## Authoring workflow

1. Copy `content/component-template.yaml` → `content/components/your-part.yaml`
2. Fill every section; delete placeholder comments as you go
3. Run `py tools/build_all.py` and preview `/components/your-part.html`
4. Run `py tools/validate_component_quality.py`
5. Complete [CONTENT_QA_CHECKLIST.md](CONTENT_QA_CHECKLIST.md) component rows
6. Add component to `content/component-roadmap.yaml` when ready

---

## Sign-off

| Role | Question |
|------|----------|
| Child | Can I wire this with a parent and feel proud when Serial Monitor changes? |
| Parent | Is USB-only safety clear? Do I know what to buy and how long it takes? |
| Teacher | Can I run this in one period with checklist assessment? |
| Engineer | Do pins, voltage, and code agree? Is troubleshooting honest? |

If any answer is no — revise YAML before publish.
