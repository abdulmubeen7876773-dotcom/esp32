# ESP32 Engine — Educational Framework

How we teach ESP32 — structure, progression, assessment, and audience scaffolding. For why we teach this way, see [MANIFESTO.md](MANIFESTO.md). For voice and sentence-level rules, see [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md).

---

## Learning philosophy

ESP32 Engine uses **guided discovery**:

1. **Hook** — story or question that creates stakes
2. **Scaffold** — ELI12 explanation before technical terms
3. **Build** — physical circuit or tangible output
4. **Name** — introduce vocabulary after experience
5. **Check** — quiz reinforces, never punishes
6. **Extend** — optional challenge for curiosity
7. **Celebrate** — mission complete + clear next step

We do not teach theory chapters before the learner touches hardware. Reference guides exist for depth after missions.

---

## Primary audience bands

| Band | Age | Reading level | Supervision |
|------|-----|---------------|-------------|
| **Core** | 10–12 | Short sentences, bullets, metaphors | Adult nearby for USB and first wiring |
| **Supported** | 13–15 | Same structure, slightly denser concept | Optional adult for power tools / soldering |
| **Independent** | 16+ and adult beginners | Missions + reference guides | Self-directed |

All mission content is written to the **Core** band. Older learners get clarity without insult; younger learners get structure without drowning.

---

## Content types and when to use them

### Mission guides (`format: mission`)

**Use for:** Every hands-on learning unit in the curriculum.

**Template:** `content/guides/blink-led-esp32.yaml`

**Fixed section order:**

```
Mission Hero (page head)
  ↓
Mission Story
  ↓
Explain Like I'm 12
  ↓
What You'll Build
  ↓
Things You'll Need
  ↓
Safety First
  ↓
Component Spotlight
  ↓
Concept
  ↓
Wiring
  ↓
Code
  ↓
Expected Output
  ↓
Mini Quiz
  ↓
Challenge Yourself
  ↓
Mission Complete
  ↓
Next Mission
```

Do not reorder sections without updating the shared template in `tools/guide_mission.py`.

### Reference guides (legacy format)

**Use for:** Background articles — IDE install, "what is ESP32," deep dives.

**When:** After Mission 1–3, or when content is conceptual rather than hands-on.

**Template:** `content/guides/what-is-esp32.yaml`

### Component pages

**Use for:** Reusable parts catalog — DHT22, DevKit, OLED, etc.

**Golden template:** `content/components/dht22.yaml`

Components are linked from missions and projects. A child should understand the **note** line under each part name.

### Projects

**Use for:** Multi-step builds with beginner / intermediate / advanced stages, or golden single-scroll projects.

**Golden template:** `content/projects/esp32-iot-weather-station.yaml`

Projects are destinations after missions teach prerequisite skills.

---

## Curriculum progression

The master roadmap lives in `content/guide-roadmap.yaml` — **100 missions** across eight levels:

| Level | Focus | Example topics |
|-------|-------|----------------|
| First Spark | GPIO, LEDs, basics | Blink, button, PWM |
| Sensors | Reading the world | DHT22, ultrasonic, PIR |
| Displays | Output beyond Serial | OLED, LCD |
| Motors | Motion and control | Servo, DC motor, relay |
| Communication | WiFi, BLE, serial | Web server, MQTT intro |
| IoT Projects | Connected systems | Weather, automation |
| AI Projects | On-device intelligence | Sound classifiers, simple ML |
| Advanced ESP32 | Power, sleep, RTOS intro | Deep dives |

**Rule:** A mission may assume skills from earlier missions in the same or prior level. Link to prerequisite missions or components explicitly.

Component roadmap: `content/component-roadmap.yaml` (210 components planned).

---

## Mission anatomy (pedagogical purpose)

| Section | Pedagogical job |
|---------|-----------------|
| **Story** | Emotional hook; learner is the hero, not the student |
| **ELI12** | Zero-jargon mental model before GPIO, `digitalWrite`, etc. |
| **What You'll Build** | Outcome preview — reduces uncertainty |
| **Things You'll Need** | Scannable prep; links to component pages |
| **Safety First** | Unplug-first; voltage limits; adult help |
| **Component Spotlight** | Deep link to one key part (usually the board) |
| **Concept** | Name the ideas — after ELI12, before wiring |
| **Wiring** | Numbered steps; diagram when available |
| **Code** | Minimal working sketch + notes explaining setup/loop |
| **Expected Output** | Success criteria + one troubleshooting hint |
| **Mini Quiz** | 2–4 questions; wrong answers teach |
| **Challenge Yourself** | Optional creativity — speed, patterns, extensions |
| **Mission Complete** | Pride + skills checklist |
| **Next Mission** | One primary "Up Next" + optional alternate |

---

## Assessment design

### Mini quiz rules

- **2–4 questions** per mission
- Questions test **understanding**, not memorization of trivia
- Every question has an **explanation** field
- Use `correct_feedback` and `wrong_feedback` for encouraging tone
- Wrong answers reveal the correct option and explain why — never shame

Good question: *Why do we use a resistor with the LED?*

Bad question: *What year was the ESP32 released?*

### Challenge design

Challenges are **optional extensions**, not graded homework.

Good challenges:

- Change a number (`delay(200)`) and observe
- Blink SOS or invent a pattern
- Combine with a prior mission skill

Bad challenges:

- Require parts not listed in the mission
- Require cloud accounts or paid services without warning

Use `challenge_items` with icons for scannable cards.

---

## Safety and supervision

Every hardware mission includes a **Safety First** block.

Minimum coverage:

1. Unplug USB before changing wires
2. Voltage limits (3.3 V GPIO on ESP32)
3. Adult help for USB, sharp parts, or soldering when applicable

Order matters: **unplug first** — it is the habit we want to build.

Badge labels in the hero:

- **Parent Safe** — no dangerous procedures without warnings
- **Teacher Friendly** — classroom-appropriate structure and time box

---

## Visual and multimodal learning

Learners understand faster with:

- Wiring diagrams (SVG preferred)
- Concept illustrations
- Expected output photos or Serial Monitor descriptions
- Icons on section headers and part lists

Alt text is mandatory in YAML — see [assets/visuals/README.md](../../assets/visuals/README.md).

Placeholder frames are acceptable until art ships. Never point YAML at a missing image file.

---

## Inclusivity and access

- Write for global English — avoid idioms that do not translate
- Use metric and common imperial where helpful (mm and inches for parts)
- Do not assume expensive kits; note substitutes where possible
- Gender-neutral "you" — avoid defaulting to "he" for engineers
- Screen reader users get the same story from alt text and section headings

---

## Quality gate before publish

Run the five-perspective check (from Mission 01 review):

1. **Child** — Can I follow this alone?
2. **Parent** — Is it safe and trustworthy?
3. **Teacher** — Does it fit one class period?
4. **Engineer** — Is the circuit and code correct?
5. **UX designer** — Is it scannable on a phone?

Target score: **90+** on internal review before calling a mission golden.

---

## Related documents

| Document | Purpose |
|----------|---------|
| [MANIFESTO.md](MANIFESTO.md) | Mission and principles |
| [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md) | Sentence-level rules |
| [guides/CONTENT_EDITOR_GUIDE.md](../guides/CONTENT_EDITOR_GUIDE.md) | Adding YAML content |
| [reviews/MISSION01_FINAL_REVIEW.md](../reviews/MISSION01_FINAL_REVIEW.md) | Golden mission benchmark |
| [reference/CONTENT_INVENTORY.md](../reference/CONTENT_INVENTORY.md) | File inventory |
