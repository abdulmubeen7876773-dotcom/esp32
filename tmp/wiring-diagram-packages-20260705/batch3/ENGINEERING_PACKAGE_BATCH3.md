# ESP32 Engine — Golden Wiring Sprint, Batch 3
## Engineering Package

**Scope:** Next 10 projects alphabetically after Batch 2 (per sitemap.xml, LED Matrix Display skipped — already completed in Batch 1).
**Status:** 10 of 10 verified and diagrammed. 0 blocked. 2 projects had one invalid wiring-table entry excluded.
**Repository status:** Untouched. Standalone assets only.

---

## Pre-Check: Systemic Bug Search (as requested)

Before diagramming, every project was checked specifically for:
1. Non-I2C components incorrectly assigned SDA/SCL GPIO21/22
2. `analogRead()` on non-ADC-capable pins

**Result:**

| Project | I2C Misuse Found? | Invalid ADC Pin Found? |
|---|---|---|
| Greenhouse Automation Controller | No — OLED I2C is legitimate | No |
| Home Climate Automation | No | No |
| IoT Weather Station | No — BME280 + OLED I2C legitimate | No |
| IR Remote Control | No | No |
| Learning Trainer Board | **Yes — "Rgb Led SDA/SCL"** | No (GPIO12 is real ADC2, see note) |
| Lightning Detector | No — OLED I2C is legitimate | No |
| Line Following Robot | No | No (GPIO34/35 both real ADC1) |
| LoRa Remote Sensor Node | No | No |
| Machine Monitoring Node | **Yes — "Alarm Led SDA/SCL"** | No (GPIO35 is real ADC1) |
| Motion Security Alert | No | No |

**This confirms the systemic template bug (non-I2C component given SDA/SCL) in 2 more projects this batch — 5th and 6th confirmed occurrences across three batches** (previously: Air Quality Monitor, Smart Street Light — Batch 1; Distance Monitoring System — Batch 2).

---

## 1. ESP32 Greenhouse Automation Controller

**File:** `esp32-greenhouse-automation-controller-wiring.svg` ✅ Verified

### Engineering Notes
DHT22 climate sensing drives a 12V exhaust fan relay on OR logic (temperature OR humidity threshold) — a sound design choice since either condition alone can justify ventilation. The OLED here is a genuinely I2C device correctly wired — this project shows the *correct* pattern that the buggy projects should have followed.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| DHT22 DATA | GPIO4 | 10kΩ pull-up |
| Fan Relay IN | GPIO26 | Active LOW |
| OLED SDA | GPIO21 | Legitimate I2C |
| OLED SCL | GPIO22 | Legitimate I2C |

### Component List
ESP32 DevKit V1 · DHT22 · 12V exhaust fan · 5V relay module · SSD1306 OLED

### Power Requirements
Fan: 12V DC/AC via relay (isolate from ESP32 supply). ESP32: USB 5V.

### Safety Notes
If driving mains-voltage fan, use a properly isolated relay module.

### Common Wiring Mistakes
Confusing OR logic for AND — the fan should activate on *either* high temp or high humidity independently.

### Troubleshooting
Fan cycles rapidly near threshold → add 2°C hysteresis (code has no hysteresis in Beginner stage by design; this is addressed in Intermediate).

---

## 2. ESP32 Home Climate Automation

**File:** `esp32-home-climate-automation-wiring.svg` ✅ Verified

### Engineering Notes
Simplest possible threshold-driven relay project — good first "real automation" build after the Golden Tutorials sensor-only projects. No I2C, no ADC ambiguity.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| DHT22 DATA | GPIO4 | 10kΩ pull-up |
| Relay IN | GPIO26 | Threshold-driven |

### Component List
ESP32 DevKit V1 · DHT22 · Relay module

### Power Requirements
Standard USB 5V; relay coil typically 5V.

### Safety Notes
Isolate any mains-voltage load switched by the relay.

### Common Wiring Mistakes
Forgetting the pull-up resistor on DHT22 DATA — causes intermittent NaN readings.

### Troubleshooting
NaN readings → verify 10kΩ pull-up present and DHT22 power matches module variant (3.3V vs 5V).

---

## 3. ESP32 IoT Weather Station

**File:** `esp32-iot-weather-station-wiring.svg` ✅ Verified

### Engineering Notes
BME280 provides three genuinely useful environmental readings (temp/humidity/pressure) over one I2C bus — efficient pin usage. Optional OLED correctly shares the same bus rather than being given a bogus separate interface.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| BME280 SDA | GPIO21 | I2C, addr 0x76/0x77 |
| BME280 SCL | GPIO22 | I2C |

### Component List
ESP32 DevKit V1 · BME280 · SSD1306 OLED (optional)

### Power Requirements
3.3V only for BME280 — 5V may damage some breakout variants.

### Safety Notes
None — low voltage, no external power components.

### Common Wiring Mistakes
Assuming BME280 = BMP280 (BMP280 lacks a humidity sensor and will return NaN for humidity).

### Troubleshooting
`bme.begin(0x76)` fails → retry with 0x77; address varies by board manufacturer.

---

## 4. ESP32 IR Remote Control

**File:** `esp32-ir-remote-control-wiring.svg` ✅ Verified

### Engineering Notes
Clean separation of IR receive (TSOP38238, demodulated digital pulses) and IR transmit (bare LED, needs external modulation via library) — correctly reflects how real IR remotes work at 38kHz carrier.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| TSOP38238 OUT | GPIO15 | Digital input |
| IR LED anode | GPIO4 | Via 100Ω resistor |

### Component List
ESP32 DevKit V1 · TSOP38238 IR receiver · 940nm IR LED · 100Ω resistor

### Power Requirements
3.3V for receiver; LED direct-driven at ~30mA GPIO limit (upgradeable to transistor-driven for range in Intermediate stage).

### Safety Notes
None — low voltage.

### Common Wiring Mistakes
TSOP38238 pin order varies by manufacturer — always check datasheet rather than assuming OUT/GND/VCC left-to-right.

### Troubleshooting
Protocol shows UNKNOWN → some devices use proprietary protocols; use raw pulse dump to manually decode.

---

## 5. ESP32 Learning Trainer Board

**File:** `esp32-learning-trainer-wiring.svg` ⚠️ Verified with 1 excluded entry

### Engineering Notes
This is a generic auto-generated "sensor + threshold + output" template project (push button → status LED/OLED). **One wiring table entry excluded**: "Rgb Led → SDA GPIO21 / SCL GPIO22" — an RGB LED has no I2C interface (it's driven by 3 PWM/digital channels), and the Beginner code never references Wire.h or GPIO21/22 at all.

**Additional finding beyond the I2C bug:** GPIO12 (used for the push button/sensor input) is a boot-strapping pin (MTDI) — safe in Beginner stage (no Wi-Fi), but the Advanced stage adds Wi-Fi while still calling `analogRead(12)`. GPIO12 is ADC2, and **ADC2 is unusable whenever Wi-Fi is active** — this will produce unreliable readings in the Advanced stage specifically, though it does not block the Beginner diagram.

### GPIO Mapping (verified subset)
| Signal | GPIO | Notes |
|---|---|---|
| Push Button Module | GPIO12 | ADC2_CH5 — fine for Beginner (no Wi-Fi) |
| Output/LED | GPIO14 | Digital output |
| ~~RGB LED SDA~~ | ~~GPIO21~~ | **Excluded — invalid, see above** |
| ~~RGB LED SCL~~ | ~~GPIO22~~ | **Excluded — invalid, see above** |

### Component List
ESP32 DevKit V1 · Push button module · Status LED/output · *(RGB LED component removed pending content fix)*

### Power Requirements
Standard USB 5V, negligible current.

### Safety Notes
None applicable at Beginner stage.

### Common Wiring Mistakes
Using GPIO12 for analog sensing in a Wi-Fi-enabled build — this is a real functional risk in the Advanced stage of this specific project.

### Troubleshooting
Output never turns on → recalibrate THRESHOLD from logged Serial readings (site's own guidance, verified sound).

---

## 6. ESP32 Lightning Detector

**File:** `esp32-lightning-detector-wiring.svg` ✅ Verified

### Engineering Notes
AS3935 Franklin lightning IC over SPI + interrupt-driven detection is a sophisticated but correctly documented design. OLED sharing the I2C bus is legitimate (unlike the buggy projects' bogus I2C entries).

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| CS | GPIO5 | SPI |
| SCK | GPIO18 | SPI |
| MOSI | GPIO23 | SPI |
| MISO | GPIO19 | SPI |
| IRQ | GPIO4 | Interrupt, RISING edge |
| OLED SDA/SCL | GPIO21/22 | Legitimate I2C |
| Red LED | GPIO26 | Via 220Ω |

### Component List
ESP32 DevKit V1 · AS3935 module (SPI variant) · SSD1306 OLED · Red LED + 220Ω resistor

### Power Requirements
AS3935: 3.3V only, not 5V tolerant.

### Safety Notes
None — indoor low-voltage electronics.

### Common Wiring Mistakes
Operating without an antenna connected can damage the RF front-end — always attach before powering.

### Troubleshooting
Frequent DISTURBER_INT with no storms → move away from switching power supplies and fluorescent lights; increase spikeRejection().

---

## 7. ESP32 Line Following Robot

**File:** `esp32-line-following-robot-wiring.svg` ✅ Verified

### Engineering Notes
Both line-sensor pins (GPIO34, GPIO35) are genuine ADC1-capable input-only pins — correct choice since ADC1 remains usable even with Wi-Fi active (relevant for future upgrades). Motor driver uses 4 independent digital pins for full H-bridge control of both motors.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| Left IR sensor | GPIO34 | ADC1_CH6, input-only |
| Right IR sensor | GPIO35 | ADC1_CH7, input-only |
| L_IN1 / L_IN2 | GPIO16 / GPIO17 | Left motor direction pair |
| R_IN1 / R_IN2 | GPIO18 / GPIO19 | Right motor direction pair |

### Component List
ESP32 DevKit V1 · 2× IR line sensor · Dual motor driver (e.g. L298N/TB6612) · 2× DC motor + wheels · Separate motor power supply

### Power Requirements
**Motors need a separate supply from ESP32** — sharing 3.3V/5V risks brownout resets from motor surge current.

### Safety Notes
Motors and servos can reset the ESP32 via voltage sag — always use a dedicated motor supply with shared ground only.

### Common Wiring Mistakes
Powering motors from the ESP32 3.3V pin directly — explicitly called out as a common mistake in the site's own content.

### Troubleshooting
Robot behavior reversed → motor driver may be active-LOW; invert logic after confirming with Serial Monitor.

---

## 8. ESP32 LoRa Remote Sensor Node

**File:** `esp32-lora-remote-sensor-node-wiring.svg` ✅ Verified

### Engineering Notes
Correctly uses board-specific Heltec WiFi LoRa 32 V2 pin mapping rather than generic ESP32 pins — appropriate since the SX1276 radio is onboard and pre-wired on this specific board family, not a separate breakout requiring manual SPI wiring.

### GPIO Mapping (Heltec LoRa32 V2 specific)
| Signal | GPIO | Notes |
|---|---|---|
| SCK | GPIO5 | SPI |
| MISO | GPIO19 | SPI |
| MOSI | GPIO27 | SPI |
| NSS/SS | GPIO18 | SPI |
| RST | GPIO14 | Radio reset |
| DIO0 | GPIO26 | RX-done interrupt |
| DHT22 DATA | GPIO4 | Transmitter node only |

### Component List
2× Heltec WiFi LoRa 32 V2 (or TTGO LoRa32) · DHT22 (transmitter) · SSD1306 OLED (receiver, often onboard) · 868/915MHz antenna ×2

### Power Requirements
USB 5V per node; battery-powered field deployment uses deep sleep (Intermediate stage).

### Safety Notes
Never operate the SX1276 without an antenna connected — can damage the RF front-end.

### Common Wiring Mistakes
Mismatched frequency/spreading-factor/bandwidth between TX and RX nodes — all four `LoRa.set...()` calls must match exactly.

### Troubleshooting
`LoRa.begin()` returns false → verify pin assignments match your specific board variant; Heltec and TTGO differ from generic Ra-02 breakout wiring.

---

## 9. ESP32 Machine Monitoring Node

**File:** `esp32-machine-monitoring-node-wiring.svg` ⚠️ Verified with 1 excluded entry

### Engineering Notes
Same generic auto-generated template family as Learning Trainer Board. Core current-sensor-to-relay logic is sound and uses a real ADC1 pin. **One wiring table entry excluded**: "Alarm Led → SDA GPIO21 / SCL GPIO22" — same invalid-I2C-on-LED defect, 6th confirmed occurrence of this systemic bug across three batches.

### GPIO Mapping (verified subset)
| Signal | GPIO | Notes |
|---|---|---|
| Current Sensor | GPIO35 | ADC1_CH7, input-only, correct |
| Relay Output | GPIO19 | Digital output |
| ~~Alarm LED SDA~~ | ~~GPIO21~~ | **Excluded — invalid** |
| ~~Alarm LED SCL~~ | ~~GPIO22~~ | **Excluded — invalid** |

### Component List
ESP32 DevKit V1 · Current sensor (e.g. ACS712/SCT-013 style) · Relay module · *(Alarm LED component removed pending content fix)*

### Power Requirements
Standard USB 5V for ESP32; relay coil typically 5V.

### Safety Notes
If monitoring/switching industrial equipment, ensure proper electrical isolation between the sensing circuit and machine power.

### Common Wiring Mistakes
Same invalid I2C entry as flagged above — needs content-level fix, not a wiring mistake a builder can resolve.

### Troubleshooting
Sensor stuck at 0 or 4095 → verify GPIO35 wiring and that sensor VCC/GND tie correctly to ESP32 rails.

---

## 10. ESP32 Motion Security Alert

**File:** `esp32-motion-security-alert-wiring.svg` ✅ Verified

### Engineering Notes
Simple, clean PIR-to-buzzer/LED design with a sensible 30-second sensor warm-up delay matching real PIR module behavior (PIR sensors need time to stabilize their pyroelectric baseline after power-on). No I2C or ADC ambiguity — this project uses the "story" template family (like Line Following Robot, IoT Weather Station) rather than the buggy generic template.

### GPIO Mapping
| Signal | GPIO | Notes |
|---|---|---|
| PIR sensor OUT | GPIO27 | Digital HIGH/LOW |
| Buzzer/Alert LED | GPIO25 | Digital output |
| Status LED | GPIO2 | Onboard, optional |

### Component List
ESP32 DevKit V1 · PIR motion sensor · Buzzer or LED

### Power Requirements
Standard USB 5V; PIR module per its own voltage label (commonly 5V-tolerant with 3.3V logic output).

### Safety Notes
None — low voltage.

### Common Wiring Mistakes
Testing immediately after power-on before the 30-second PIR warm-up completes — will show false triggers.

### Troubleshooting
PIR output never changes → verify power/ground and whether the specific PIR module output is analog or digital (some cheap clones differ).

---

## Summary Table — Integration Readiness

| # | Project | Diagram | Safe to Integrate? |
|---|---|---|---|
| 1 | Greenhouse Automation Controller | ✅ | Yes |
| 2 | Home Climate Automation | ✅ | Yes |
| 3 | IoT Weather Station | ✅ | Yes |
| 4 | IR Remote Control | ✅ | Yes |
| 5 | Learning Trainer Board | ⚠️ | Yes, with excluded RGB LED entry noted as content gap; Advanced-stage GPIO12/Wi-Fi conflict also flagged |
| 6 | Lightning Detector | ✅ | Yes |
| 7 | Line Following Robot | ✅ | Yes |
| 8 | LoRa Remote Sensor Node | ✅ | Yes |
| 9 | Machine Monitoring Node | ⚠️ | Yes, with excluded Alarm LED entry noted as content gap |
| 10 | Motion Security Alert | ✅ | Yes |

**No project required an Engineering Review block in this batch** — unlike Batch 2's Distance Monitoring System, none of this batch's issues broke core functionality; all were either legitimate (OLED I2C) or isolated to one excludable component entry.

## Remaining Blockers (content-level, cumulative across all 3 batches)

1. **Systemic template bug — now 6 confirmed occurrences**: Air Quality Monitor, Smart Street Light (Batch 1); Distance Monitoring System (Batch 2); Learning Trainer Board, Machine Monitoring Node (Batch 3), plus the pattern likely recurs in any remaining project using the same generic "sensor + threshold + output" auto-generated template. **Recommend a targeted find-and-fix pass across the remaining ~20 unaudited projects for any wiring table row containing both a non-I2C component name and "SDA"/"SCL" fields.**
2. Learning Trainer Board's Advanced stage reuses an ADC2 pin (GPIO12) while Wi-Fi is active — recommend moving to an ADC1 pin (e.g. GPIO34) for the Advanced-stage sensor input specifically.
3. Camera Capture Server (Batch 1) and Distance Monitoring System (Batch 2) still need full content rewrites before diagrams can be produced.
