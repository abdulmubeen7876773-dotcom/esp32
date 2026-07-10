# ESP32 Engine — Golden Wiring Sprint, Batch 2
## Engineering Package

**Scope:** Projects 11–20 (first 10 remaining after Batch 1's curated 10, taken in the site's own alphabetical project order).
**Status:** 9 of 10 verified and diagrammed. 1 of 10 blocked — Engineering Review below.
**Repository status:** Untouched, as instructed. Standalone assets only.

---

## 1. ESP32 AC Power Monitor

**File:** `esp32-ac-power-monitor-wiring.svg` ✅ Verified

### Engineering Notes
Non-invasive current sensing via SCT-013 clamp — the live wire is never opened or touched directly, making this one of the safer mains-adjacent beginner projects. The critical engineering element is AC coupling: the CT outputs a symmetric AC voltage that must be biased to sit within the ESP32 ADC's 0–3.3V unipolar range.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| SCT-013 output (via cap + divider) | GPIO34 | ADC1_CH6, input-only — correct |

### Component List
ESP32 DevKit V1 · SCT-013-030 CT clamp · 2× 10kΩ resistor · 10µF electrolytic capacitor · 3.5mm jack socket

### Power Requirements
ESP32: USB 5V. CT clamp is self-powered by the magnetic field — no external supply needed.

### Safety Notes
Never open a CT secondary while the primary (live wire) is energized — always clamp/unclamp with the circuit de-energized if possible, or ensure the CT burden resistor circuit stays intact.

### Common Wiring Mistakes
Connecting AOUT directly to GPIO34 without the AC-coupling cap + divider — this clips the signal against 0V and produces only the positive half-cycle.

### Troubleshooting
If Serial shows a constant near-2048 reading with no variation, verify the divider midpoint voltage with a multimeter (should read ~1.65V at idle).

---

## 2. ESP32 AI Object Detector

**File:** `esp32-ai-object-detector-wiring.svg` ✅ Verified

### Engineering Notes
Colour-blob detection on raw RGB565 pixels — a genuine, if simple, computer-vision technique requiring no ML model. Pin map is byte-for-byte identical to the verified AI-Thinker standard from Batch 1's CAM QR Scanner.

### GPIO Mapping
Standard AI-Thinker camera pins (PWDN=32, XCLK=0, SIOD=26, SIOC=27, VSYNC=25, HREF=23, PCLK=22, Y9–Y2=35,34,39,36,21,19,18,5) + Red LED on **GPIO33 (onboard, no wiring needed)**.

### Component List
ESP32-CAM (AI-Thinker) · FTDI USB-serial adapter · (Red LED is onboard — no external LED/resistor needed despite the site's component list suggesting one)

### Power Requirements
5V/500mA minimum — insufficient FTDI 3.3V power is the #1 cause of camera crashes.

### Safety Notes
IO0→GND only during flashing; remove before normal operation.

### Common Wiring Mistakes
Site's component list lists "1× Red LED and 220 ohm resistor" as if external — GPIO33 is the AI-Thinker board's onboard LED, so no external LED is actually needed for this specific pin. Not wrong, just redundant hardware if followed literally.

### Troubleshooting
If detection ratio is always 0.000, confirm `PIXFORMAT_RGB565` is set — JPEG format will not work with pixel-threshold logic.

---

## 3. ESP32-CAM Face Detection

**File:** `esp32-cam-face-detection-wiring.svg` ✅ Verified

### Engineering Notes
Uses Espressif's built-in MTMN face detector — a genuine on-device neural network requiring no external ML framework integration, unlike the AI Object Detector's TFLite path. SVGA (800×600) is a heavier frame size, so a stable 5V/2A supply matters more here than in lighter QVGA projects.

### GPIO Mapping
Standard AI-Thinker camera pins (identical to project #2 and QR Scanner) + FTDI programming pins.

### Component List
ESP32-CAM (AI-Thinker) · FTDI USB-serial adapter · Dedicated 5V/2A power supply

### Power Requirements
310mA peak during streaming — FTDI's 3.3V/500mA is not sufficient; dedicated 5V supply required.

### Safety Notes
Same IO0/GND upload-mode caution as all AI-Thinker builds.

### Common Wiring Mistakes
Powering from FTDI 3.3V pin instead of 5V — causes repeated reboots under streaming load.

### Troubleshooting
Camera init error 0x105 (ESP_ERR_NOT_FOUND) → reseat the OV2640 ribbon cable; it is fragile and easily loosened.

---

## 4. ESP32 CNC Controller

**File:** `esp32-cnc-controller-wiring.svg` ✅ Verified

### Engineering Notes
Single-axis stepper fundamentals: STEP/DIR/EN control of an A4988 driver. The most safety-relevant engineering detail is the mandatory 100µF decoupling capacitor across VMOT — without it, back-EMF from the stepper coil can spike the motor supply and crash the ESP32.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| STEP | GPIO14 | Pulse output |
| DIR | GPIO27 | Direction |
| EN | GPIO26 | LOW = enabled |

### Component List
ESP32 DevKit V1 · A4988 driver · NEMA 17 stepper · 12V/2A supply (separate from ESP32) · 100µF capacitor

### Power Requirements
**Two separate supplies**: ESP32 via USB 5V; motor via dedicated 12V/2A. Never share these rails.

### Safety Notes
Set A4988 current limit (Vref = Imax × 8 × Rs) via trim pot **before** connecting the motor — an unset or too-high limit will overheat the driver within seconds.

### Common Wiring Mistakes
Omitting the VMOT decoupling capacitor — this is explicitly called out in the project's own troubleshooting section as a cause of ESP32 resets.

### Troubleshooting
Motor vibrates without rotating → coil pairs mis-wired; verify continuity pairs with a multimeter before assuming a firmware issue.

---

## 5. ESP32 Digital Piano

**File:** `esp32-digital-piano-wiring.svg` ✅ Verified

### Engineering Notes
Capacitive touch sensing repurposes the ESP32's built-in touch peripheral (normally used for wake-on-touch) as musical keys. Touch-pin-to-GPIO mapping (T0=4, T3=15, T4=13, T5=12, T6=14, T7=27, T8=33, T9=32) was cross-checked against the real ESP32 touch peripheral table and matches exactly.

### GPIO Mapping
8 touch pads on GPIO 4,15,13,12,14,27,33,32 (T0,T3,T4,T5,T6,T7,T8,T9) + Buzzer on GPIO25.

### Component List
ESP32 DevKit V1 · Passive piezo buzzer · 8× copper foil tape pads · jumper wires

### Power Requirements
Negligible — touch sensing and PWM buzzer draw minimal current, USB power is ample.

### Safety Notes
None applicable — low-voltage, no external power components.

### Common Wiring Mistakes
Using an **active** buzzer instead of passive — an active buzzer has its own oscillator and will not respond to the LEDC PWM frequency changes needed to produce different musical notes.

### Troubleshooting
If touch is detected inconsistently, keep touch-pad wire runs under 10cm — longer wires add stray capacitance that masks the touch signal.

---

## 6. ESP32 ECG Monitor

**File:** `esp32-ecg-monitor-wiring.svg` ✅ Verified

### Engineering Notes
Genuine biopotential signal acquisition via the AD8232 instrumentation amplifier, which handles the two-pole high-pass and low-pass filtering in hardware. Leads-off detection (LO+/LO-) is a real safety/data-quality feature, correctly wired and used in the code.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| OUTPUT | GPIO34 | ADC1_CH6 — correct ADC-capable pin |
| LO+ | GPIO32 | Digital input |
| LO- | GPIO33 | Digital input |

### Component List
ESP32 DevKit V1 · AD8232 module · 3× disposable Ag-AgCl electrode pads · snap lead cable

### Power Requirements
3.3V only — do not use 5V with this module.

### Safety Notes
**This is an educational project, not a medical device.** Should not be used for diagnosis, health monitoring, or any decision affecting real cardiac care.

### Common Wiring Mistakes
RL electrode placed on the arm instead of the lower left rib — this electrode is a reference/driven-ground point, not a signal electrode, and mis-placement increases noise.

### Troubleshooting
Erratic spikes synced to mains frequency → run from battery-powered laptop, away from mains appliances, during recording.

---

## 7. ESP32 Fire Alarm System

**File:** `esp32-fire-alarm-system-wiring.svg` ✅ Verified (1 documentation gap noted)

### Engineering Notes
Dual-output MQ-2 sensing (analog + digital) provides redundant detection — a genuinely good practice. The 30-second preheat delay in the code correctly matches the MQ-2's real physical warm-up requirement.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| AOUT | GPIO34 | ADC1_CH6, via voltage divider (see note) |
| DOUT | GPIO35 | ADC1_CH7, digital threshold |
| Red LED | GPIO25 | Alarm indicator |
| Green LED | GPIO26 | Normal status |
| Buzzer | GPIO27 | Active buzzer |

### Component List
ESP32 DevKit V1 · MQ-2 smoke/gas sensor · active buzzer · red + green LED · 2× 220Ω resistor · **10kΩ + 20kΩ resistors (divider — see gap below)**

### Power Requirements
MQ-2 heater: 5V at 150mA — must use Vin, not 3.3V.

### Safety Notes
If used to control a mains-voltage fan or alarm siren via relay, ensure proper isolation — this is called out in the site's own upgrade path.

### Common Wiring Mistakes / Documentation Gap
🟡 The wiring table's own notes column says "use voltage divider from 5V output" for MQ-2 AOUT, but the **components list omits the 10kΩ/20kΩ resistors** needed to build that divider. The diagram includes them for a complete, safe build — but the source content should be corrected to list these resistors explicitly.

### Troubleshooting
Alarm triggers immediately after power-on → this is the expected cold-sensor transient; the 30-second preheat in the code should suppress it. Do not test during warmup.

---

## 8. ESP32 Gesture Recognition

**File:** `esp32-gesture-recognition-wiring.svg` ✅ Verified

### Engineering Notes
APDS-9960 handles the directional swipe decoding entirely in its own photodiode array and onboard processing — the ESP32's job is simply I2C communication and interrupt handling, a good example of offloading signal processing to purpose-built hardware.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| SDA | GPIO21 | I2C data |
| SCL | GPIO22 | I2C clock |
| INT | GPIO4 | Active LOW interrupt |
| 4× LED | GPIO25,26,27,14 | One per direction |

### Component List
ESP32 DevKit V1 · APDS-9960 breakout · 4× LED (R/G/B/Y) · 4× 220Ω resistor

### Power Requirements
**3.3V only** — the APDS-9960 will be damaged by 5V.

### Safety Notes
Double-check module voltage rating before connecting; some breakout variants differ.

### Common Wiring Mistakes
Running both gesture and proximity sensing modes simultaneously without properly sequencing `enableProximitySensor()` calls — noted as a library limitation in the project's own troubleshooting section.

### Troubleshooting
APDS-9960 init fails → confirm I2C address 0x39 with a scanner sketch before assuming a wiring fault.

---

## 9. ESP32 GPS Tracker

**File:** `esp32-gps-tracker-wiring.svg` ✅ Verified

### Engineering Notes
Standard UART2 NMEA parsing via TinyGPS++ — a clean, minimal example of hardware serial communication distinct from the USB-Serial (UART0) used for debugging.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| RX2 (← GPS TX) | GPIO16 | UART2 |
| TX2 (→ GPS RX) | GPIO17 | Optional, UART2 |

### Component List
ESP32 DevKit V1 · NEO-6M GPS module with antenna

### Power Requirements
Module has onboard regulator — accepts 3.3V or 5V input directly.

### Safety Notes
None applicable — low-voltage, no external power components.

### Common Wiring Mistakes
Swapping TX/RX — the project's own troubleshooting explicitly flags GPIO16 vs GPIO17 confusion as the top no-data issue.

### Troubleshooting
No data after 10 seconds → verify NEO-6M TX is on GPIO16 (not 17); the module transmits NMEA sentences even without a satellite fix, so silence indicates a wiring fault, not a fix problem.

---

## 🔴 10. ESP32 Distance Monitoring System — Engineering Review (No Diagram Produced)

**File:** *(none — blocked)*

### Why This Project Is Technically Incorrect

Two separate defects, one of which is a genuine functional failure rather than a documentation quirk:

**Defect 1 — Invalid ADC pin (critical, breaks functionality)**

The code calls `analogRead(SENSOR_PIN)` where `SENSOR_PIN = 5` (GPIO5). **GPIO5 has no ADC unit attached on the ESP32.** The only ADC-capable pins are GPIO32–39 (ADC1) and GPIO0,2,4,12–15,25–27 (ADC2, unusable alongside active Wi-Fi). `analogRead()` on GPIO5 does not throw an error — it silently returns an undefined/meaningless value, which is worse than a hard failure because a learner following this tutorial will see *numbers* on the Serial Monitor and reasonably assume the sensor is working.

**Defect 2 — Invalid I2C entry (same template bug pattern as Batch 1)**

The wiring table lists `Buzzer SDA → GPIO21`, `SCL → GPIO22` — a buzzer has no I2C interface, and this exact pattern (a non-I2C component given SDA/SCL fields) was already identified in Batch 1 for the Air Quality Monitor and Smart Street Light. This confirms the earlier hypothesis of a **systemic content-generation defect** affecting a shared template, now observed in a third project.

### What Hardware Should Actually Be Used

For a genuine "Ultrasonic Sensor" distance-monitoring project, the correct component is an **HC-SR04** (already correctly documented in Batch 1's Smart Parking Sensor) or a **VL53L0X Time-of-Flight sensor** (true I2C device, which would legitimately use SDA/SCL pins).

### What Wiring Should Actually Exist

**If HC-SR04 (digital trigger/echo):**
- TRIG → any digital GPIO (e.g. GPIO5, output)
- ECHO → digital input **via 10kΩ/20kΩ divider** (5V signal → 3.3V safe), e.g. GPIO18

**If VL53L0X (I2C ToF):**
- SDA → GPIO21, SCL → GPIO22 (this would make the I2C entry legitimate)
- No analog pin needed at all

### What Code Architecture Is Expected

The current code's `analogRead()` + threshold pattern is fundamentally the wrong approach for either real ultrasonic option:
- HC-SR04 requires a **pulse-timing** measurement (`pulseIn()` on ECHO after a TRIG pulse), not `analogRead()`
- VL53L0X requires the **manufacturer's I2C driver library** (e.g. Adafruit_VL53L0X), which returns a distance-in-mm value directly — no threshold tuning against raw ADC counts needed

### Recommendation

This project's beginner content appears to have been generated from the same generic "analog sensor + threshold + digital output" template used for genuinely analog projects (soil moisture, gas sensors), but incorrectly applied to an ultrasonic/ToF sensor family that is inherently digital-timing or I2C-based. Recommend rewriting from the HC-SR04 pattern already verified correct in the Smart Parking Sensor project (Batch 1), which is the more beginner-appropriate and lower-cost option.

---

## Summary Table — Integration Readiness

| # | Project | Diagram | Safe to Integrate? |
|---|---|---|---|
| 1 | AC Power Monitor | ✅ | Yes |
| 2 | AI Object Detector | ✅ | Yes |
| 3 | CAM Face Detection | ✅ | Yes |
| 4 | CNC Controller | ✅ | Yes |
| 5 | Digital Piano | ✅ | Yes |
| 6 | ECG Monitor | ✅ | Yes (with "educational only" disclaimer recommended) |
| 7 | Fire Alarm System | ✅ | Yes, with divider-resistor documentation gap noted |
| 8 | Gesture Recognition | ✅ | Yes |
| 9 | GPS Tracker | ✅ | Yes |
| 10 | Distance Monitoring System | 🔴 | **No — requires full rewrite (wrong ADC pin + wrong sensor architecture)** |

**Remaining blockers before full integration:**
1. Distance Monitoring System needs complete rewrite — recommend basing it on the already-verified HC-SR04 pattern from Batch 1's Smart Parking Sensor.
2. Fire Alarm System's components list should be updated to explicitly include the 10kΩ/20kΩ divider resistors already implied by its own wiring notes.
3. The systemic "non-I2C component given SDA/SCL fields" template bug has now been confirmed in **three** projects across two batches (Air Quality Monitor, Smart Street Light, Distance Monitoring System) — recommend an audit of the remaining 40 projects for the same pattern before further diagram production.
