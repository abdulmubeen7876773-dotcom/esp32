# Blink LED Wiring Diagram — Production Spec

**Target file:** `blink-led-wiring-esp32.svg`  
**Deploy path:** `/assets/visuals/guides/wiring/blink-led-wiring-esp32.svg`  
**Content slug:** `blink-led-esp32`  
**Mission:** Mission 1 — Blink an LED with ESP32

This document is the handoff brief for the illustrator. Do not ship raster exports until SVG is approved.

---

## Layout

| Zone | Content |
|------|---------|
| **Left (~40%)** | ESP32 DevKit board, USB port facing down or toward viewer, pin labels visible on the inner edge |
| **Right (~55%)** | Half-size breadboard in top view, centered vertically |
| **Gap (~5%)** | Clear space between board and breadboard for jumper wires |

Reading order: left → right, signal path top → bottom on the breadboard.

---

## Circuit (exact connections)

```
GPIO 2 ──(yellow wire)──► 220Ω resistor ──► LED long leg (+) ──► LED short leg (−) ──(black wire)──► GND
```

| Connection | Detail |
|------------|--------|
| Signal | **GPIO 2** on ESP32 → one leg of **220Ω resistor** (yellow jumper) |
| Resistor → LED | Other resistor leg → same breadboard row as **LED long leg (+)** |
| Return | **LED short leg (−)** row → **GND** on ESP32 (black jumper) |
| Power | **3.3 V not used** — do not draw VCC, 3V3, or power rails on this diagram |

Only two wires leave the ESP32: one from **GPIO 2**, one to **GND**.

---

## Wire colors

| Wire | Color | Hex (suggested) |
|------|-------|-----------------|
| GPIO signal (GPIO 2 → resistor) | Yellow | `#E6B800` |
| Ground (LED cathode → GND) | Black | `#1A1A1A` |

Use solid strokes, 3–4 px at 960 px canvas width. Rounded line caps.

---

## Required labels (beginner-friendly)

Every label uses sentence case, 14–18 px equivalent at 960 px width, high contrast on background.

| Element | Label text |
|---------|------------|
| ESP32 pin | `GPIO 2` |
| Resistor | `220Ω resistor` |
| LED anode | `LED long leg (+)` |
| LED cathode | `LED short leg (−)` |
| ESP32 pin | `GND` |

Optional callouts (small, secondary): `ESP32 DevKit`, `Breadboard` — only if they do not crowd primary labels.

Do not use jargon-only labels (`D2`, `cathode`, `anode`) without the friendly text above.

---

## Component drawing rules

### ESP32 DevKit

- Simplified flat rectangle with rounded corners
- Show a row of pin headers; highlight **GPIO 2** and **GND** with small filled dots or accent rings
- No brand logo; generic DevKit silhouette

### Breadboard

- Standard dual-rail top view; center trench visible
- LED straddling the trench (long leg on one side, short leg on the other)
- Resistor bent in a U or zigzag between GPIO row and LED anode row

### LED

- Flat vector LED icon (circle or dome + two legs)
- **Long leg (+)** visibly longer than **short leg (−)**
- Subtle glow tint on the dome optional; keep flat style

### Resistor

- Zigzag or IEC rectangle symbol with color bands optional (red-red-brown = 220Ω)
- Label `220Ω resistor` adjacent, not overlapping the symbol

---

## Visual style

| Property | Value |
|----------|-------|
| Style | Clean flat vector — no photos, no 3D, no gradients except soft LED tint |
| Background | White `#FFFFFF` or soft gray `#F5F5F7` |
| Stroke | `#333333` or `#1D1D1F` for outlines; 1.5–2 px |
| Accent | Site blue `#0071E3` for GPIO 2 highlight only (optional) |
| Shadows | None or single 2% drop shadow on board/breadboard only |
| Typography | Sans-serif (Inter, system-ui, or Arial in SVG `<text>`) |
| Label contrast | WCAG AA minimum on background |

---

## Canvas & export

| Property | Value |
|----------|-------|
| Format | SVG 1.1 |
| Artboard | **960 × 540 px** (16:9) |
| ViewBox | `0 0 960 540` |
| Safe margin | 32 px on all sides |
| Mobile | Must remain legible when scaled to **320 px** wide; labels never below 11 px rendered size |
| Retina | Vector — no @2x export required |

Optimize SVG: no embedded raster, minimal `<defs>`, readable layer/group names (`esp32`, `breadboard`, `led`, `resistor`, `wire-signal`, `wire-gnd`, `labels`).

---

## Alt text (for YAML `illustration_alt`)

Use verbatim in `content/guides/blink-led-esp32.yaml`:

```
Breadboard wiring diagram — ESP32 GPIO 2 through a 220 ohm resistor to the LED long leg, LED short leg to GND
```

---

## YAML reference (after file exists)

```yaml
wiring:
  illustration_alt: Breadboard wiring diagram — ESP32 GPIO 2 through a 220 ohm resistor to the LED long leg, LED short leg to GND
  image: /assets/visuals/guides/wiring/blink-led-wiring-esp32.svg
```

Until `blink-led-wiring-esp32.svg` is committed, the site shows the gray placeholder frame with the alt text above.

---

## Checklist before merge

- [ ] ESP32 on left, breadboard on right
- [ ] GPIO 2 → 220Ω → LED (+) → LED (−) → GND only
- [ ] No 3.3 V / VCC wire
- [ ] Yellow signal wire, black GND wire
- [ ] All five required labels present and readable at 320 px width
- [ ] 960 × 540 SVG, flat vector, light background
- [ ] Alt text matches YAML
- [ ] File named `blink-led-wiring-esp32.svg` in this folder
