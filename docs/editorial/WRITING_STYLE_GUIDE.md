# ESP32 Engine — Writing Style Guide

How we write every headline, story, step, and quiz on ESP32 Engine. For principles, see [MANIFESTO.md](MANIFESTO.md). For structure and pedagogy, see [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md).

---

## Voice

ESP32 Engine sounds like a **patient expert friend** — not a textbook, not a hype marketer, not a chatbot.

| We are | We are not |
|--------|------------|
| Warm, direct, confident | Cold, corporate, vague |
| Short and clear | Wordy or academic |
| Encouraging | Condescending or overly cute |
| Technically accurate | Dumbed-down or wrong |
| Adventure-oriented (missions) | Exam-oriented or punitive |

**Inspiration (tone only — do not copy UI):** Apple clarity, Duolingo encouragement, LEGO Education hands-on framing, Khan Academy patience.

---

## Point of view and tense

- Use **second person** ("you") — the learner is the protagonist
- Use **present tense** for instructions: "Connect GPIO 2" not "You will connect"
- Use **active voice**: "The ESP32 sends power" not "Power is sent by the ESP32"
- Missions may use **story present** in the opening: "You're the captain…"

---

## Readability rules

These apply to all mission YAML prose fields.

### Length

- **Maximum ~4 lines per paragraph** — then break or use bullets
- **Prefer bullets** for lists of 3+ items (prefix YAML lines with `- `)
- **One idea per wiring step** — split combined actions

### Sentence length

- Target **8–16 words** per sentence in ELI12 and wiring steps
- Concept section may reach **20 words** if needed for accuracy
- Never stack three commas in one sentence

### Words to avoid (or delay)

| Avoid early | Use instead (first mention) |
|-------------|----------------------------|
| GPIO alone | "pin" then "GPIO pin" in concept |
| Cathode / anode alone | "long leg (+)" / "short leg (−)" then name in concept |
| Pull-up, floating, sink/source | Reference guide or later missions |
| "Simply" / "just" / "obviously" | Delete — if it were obvious, we would not say it |
| "Image of…" in alt text | Describe what the learner sees |

### Words we use consistently

| Term | Rule |
|------|------|
| ESP32 DevKit | Generic board name — no brand lock-in |
| GPIO 2 | Space before number: `GPIO 2`, not `GPIO2` in prose |
| GND | OK after first "ground" in wiring; match diagram labels |
| Arduino IDE | Capitalize; link to install guide when first upload is required |
| Mission | Capitalize when meaning a guide unit: "Mission 1" |
| breadboard | Lowercase unless start of sentence |

---

## Section-by-section style

### Hero (`lead`)

- One or two sentences
- State the outcome emotionally: *"Let's make it blink!"*
- No technical specs in the lead

**Good:** *Your first real ESP32 project — one LED, a few wires, and code you write yourself. Let's make it blink!*

**Bad:** *This tutorial covers digital output configuration on ESP32 GPIO pins using the Arduino core.*

### Story

- 2–4 short paragraphs OR 3 tight paragraphs max
- Metaphor allowed (spaceship, robot, lighthouse) — one metaphor per mission, sustained
- End with the stakes: what success proves

### ELI12 (`eli12`)

- **Bullet list only** (4–6 bullets)
- No code, no pin numbers unless unavoidable
- Analogies welcome: "speed bump" for resistor, "brain" for ESP32

### What You'll Build

- Bullet list of **outcomes**, not steps
- Include confidence line: "Proof that you can…"

### Things You'll Need

- `item`: short name
- `note`: one line — color, size, or "any color is fine"
- Link to component page when catalog entry exists

### Safety

- Bullet list, **3 items max** for simple missions
- First bullet: unplug USB
- Plain language — no ALL CAPS warnings

### Concept

- Title as question: *How Does Blinking Work?*
- Body as bullets after ELI12 introduced the idea
- Name functions here (`pinMode`, `digitalWrite`, `delay`) with one-line roles

### Wiring steps

- Numbered strings in YAML `steps:` array
- Start with physical setup, end with upload
- Include a **double-check** step before power-on
- Wire colors when spec defines them (yellow signal, black GND)
- Use `(+)` and `(−)` on first LED mention in steps

### Code notes (`code.notes`)

- Bullets explaining `setup()`, `loop()`, and one experiment hint
- Do not restate every line — explain the **pattern**

### Expected output

- First block: bullet list of what success looks like
- Second block (paragraph): one troubleshooting path — most common failure only

### Quiz

- Question: one sentence, no trick wording
- Options: parallel grammar, similar length
- `correct_feedback`: celebrate + reinforce
- `wrong_feedback`: gentle + redirect
- `explanation`: teach the concept in one sentence

### Challenge items

- Start with verb: "Blink faster", "Try delay(1000)"
- Icon + one line each
- Last item invites creativity

### Mission complete

- `subtitle`: one proud line (*You just became an ESP32 maker.*)
- `summary`: 1–2 sentences — past tense achievement
- `skills`: 3 bullet skills — verb-first ("Connected…", "Used…", "Uploaded…")

---

## YAML formatting conventions

```yaml
mission:
  story: |
    Paragraph one.

    Paragraph two.
  eli12: |
    - Bullet one.
    - Bullet two.
```

- Use `|` block scalars for multi-line fields
- Blank line between paragraphs in story
- Bullets: each line starts with `- ` inside the block
- Quotes in YAML: single quotes for dates `'2026-06-27'`
- Emoji in `icon` fields only — not in body prose unless mission card icon

---

## Headlines and SEO

| Field | Rule |
|-------|------|
| `title` | `{Headline} \| ESP32 Engine` |
| `headline` | Human-facing H1 — no pipe, no brand suffix |
| `meta_description` | One sentence, ≤ 160 chars, includes "Mission N" for missions |
| `slug` | lowercase, hyphens, matches filename |

**Good meta_description:** *Mission 1 — blink your first LED with ESP32. Kid-friendly steps, wiring, code, and quiz.*

---

## Alt text

- Describe the **circuit or result**, not the file format
- Include pin names for wiring diagrams
- Do not start with "Image of" or "Diagram of"

**Good:** *Breadboard wiring — ESP32 GPIO 2 through a 220 ohm resistor to the LED long leg, LED short leg to GND*

---

## Inclusive language

- "Ask an adult" not "ask your mom and dad"
- "Learner" in docs; "you" on site
- Avoid culture-specific sports metaphors
- Avoid gendered roles in stories (captain, maker, inventor — all neutral)

---

## Editing checklist

Before submitting mission YAML:

- [ ] Every paragraph ≤ 4 lines
- [ ] ELI12, build, concept use bullets where possible
- [ ] Wiring steps numbered and testable
- [ ] Safety includes unplug-first
- [ ] Quiz wrong answers teach
- [ ] Complete section celebrates success
- [ ] `date_modified` updated
- [ ] Read aloud once — would a 10-year-old stay engaged?

---

## Related documents

| Document | Purpose |
|----------|---------|
| [MANIFESTO.md](MANIFESTO.md) | Why we write this way |
| [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md) | Section order and assessment |
| [guides/CONTENT_EDITOR_GUIDE.md](../guides/CONTENT_EDITOR_GUIDE.md) | Build workflow |
| [assets/visuals/README.md](../../assets/visuals/README.md) | Image and alt text rules |

**Golden example:** `content/guides/blink-led-esp32.yaml`
