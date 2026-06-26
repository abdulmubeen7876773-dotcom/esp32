# ESP32 Engine — Manifesto

**The world's friendliest ESP32 learning platform.**

This document states why ESP32 Engine exists and the principles every piece of content must uphold. For how we teach, see [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md). For how we write, see [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md).

---

## Why we exist

Millions of people will touch an ESP32 for the first time through a search result, a classroom, or a parent at the kitchen table. Most tutorials assume you already know electronics, C++, and which GPIO is which.

We exist to remove that fear.

A learner should finish their first mission feeling:

- **I understand this.**
- **I built something.**
- **I want to continue.**

---

## Who we serve

| Audience | What they need from us |
|----------|------------------------|
| **Children (10–14)** | Adventure, clarity, safety, small wins |
| **Teens & adult beginners** | Respect, no condescension, fast path to working hardware |
| **Parents** | Trust, safety visibility, honest time estimates |
| **Teachers** | Predictable structure, classroom-ready flow, light assessment |
| **Engineers returning to basics** | Correct circuits, minimal code, no hand-waving |

We optimize for the **10–12-year-old opening the site alone for the first time**. Everyone else benefits from that bar.

---

## Core beliefs

### 1. Build first, jargon later

Hands-on beats lecture. Every mission ends with something physical — a blinking LED, a sensor reading, a screen update. Vocabulary arrives after the learner has context.

### 2. One masterpiece beats ten drafts

Quality compounds. Mission 01 (Blink LED) is the golden standard. New missions copy its structure and polish — they do not invent new formats.

### 3. Fear is the enemy

Long paragraphs, unexplained acronyms, and walls of code create dropout. We use story, bullets, diagrams, and celebration to create **excitement, not anxiety**.

### 4. Safety is non-negotiable

Every hardware mission includes clear safety guidance. Unplug before rewiring. 3.3 V logic. Adult help when needed. We never glamorize risky shortcuts.

### 5. Static and open

Phase 1 is static-first: YAML in git, Python build, GitHub Pages. No login walls, no paywalls, no tracking learners without consent. Content is version-controlled and improvable by the community.

### 6. Accessible by default

Readable contrast, keyboard navigation, alt text on every image, touch targets on mobile, reduced-motion respect. Accessibility is product quality, not a checklist afterthought.

### 7. Technically honest

Kid-friendly does not mean wrong. Circuits must be correct. Pin numbers must match code. We simplify language, not physics.

---

## What we publish

| Content type | Role |
|--------------|------|
| **Mission guides** | Primary learning path — story, build, wire, code, quiz, challenge |
| **Reference guides** | Background reading after first missions |
| **Components** | Encyclopedia entries — pinouts, specs, wiring |
| **Projects** | Multi-stage builds for deeper exploration |
| **Visual assets** | Diagrams, photos, icons — co-located under `assets/visuals/` |

The curriculum roadmap targets **100 missions** across eight levels — from First Spark to Advanced ESP32. We ship complete missions, not placeholders that look finished.

---

## What we refuse

- **Backend complexity in Phase 1** — no CMS, auth, or runtime server unless the architecture explicitly evolves
- **Content that cannot be built** — if the wiring diagram is missing, we use an accessible placeholder with alt text; we do not pretend art exists
- **Copy-paste datasheet dumps** — every component page teaches, not archives
- **Engagement bait** — no dark patterns, fake urgency, or guilt-driven CTAs
- **Age-inappropriate tone** — no baby talk for teens; no engineer-speak for children

---

## The golden standard

**Mission 01 — Blink LED** (`content/guides/blink-led-esp32.yaml`) is the reference implementation.

Before publishing any new mission, ask:

1. Would a 10-year-old understand the story and ELI12 section?
2. Can they wire the circuit from our steps alone (or with a diagram)?
3. Does the code block copy cleanly and explain what each part does?
4. Does the quiz teach on wrong answers?
5. Does the ending make them proud?

See [reviews/MISSION01_FINAL_REVIEW.md](../reviews/MISSION01_FINAL_REVIEW.md) for the quality bar.

---

## Success looks like

- A child completes Mission 01 without giving up
- A parent skims safety and expected output in under two minutes and says yes
- A teacher runs one mission in a single class period
- An engineer trusts our pinouts and wiring
- A contributor knows exactly where to add content and which template to copy

---

## Related documents

| Document | Purpose |
|----------|---------|
| [EDUCATIONAL_FRAMEWORK.md](EDUCATIONAL_FRAMEWORK.md) | Pedagogy, levels, mission anatomy |
| [WRITING_STYLE_GUIDE.md](WRITING_STYLE_GUIDE.md) | Voice, readability, terminology |
| [guides/CONTENT_EDITOR_GUIDE.md](../guides/CONTENT_EDITOR_GUIDE.md) | YAML workflow and build steps |
| [engineering/DEVELOPER_ARCHITECTURE.md](../engineering/DEVELOPER_ARCHITECTURE.md) | Build system |
