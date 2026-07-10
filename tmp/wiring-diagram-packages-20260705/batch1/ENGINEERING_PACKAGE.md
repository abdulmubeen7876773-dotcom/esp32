# ESP32 Engine — Top 10 Golden Tutorials
## Wiring Diagram Engineering Package

**Prepared by:** Visual Engineering — ESP32 Engine
**Scope:** SVG wiring diagrams + engineering documentation for the Top 10 Golden Tutorials
**Verification method:** Each diagram is cross-checked against the project's own Beginner-stage wiring table and `.ino` source (Beginner stage used as the canonical/entry-level build for all 10).
**Status:** 9 of 10 verified and diagrammed. 1 of 10 blocked — see Engineering Review at the end.

---

## 1. ESP32 Soil Moisture Monitor

**File:** `esp32-soil-moisture-monitor-wiring.svg` ✅ Verified

### Engineering Notes
Capacitive soil sensor output is analog and noisy near dry/wet transition points; the design uses a single ADC1 channel (GPIO34) with software thresholding rather than hardware filtering. Three status LEDs give a coarse moisture band (dry/moderate/moist), and a buzzer provides an audible alert on critical dryness. All switching is direct-drive (no transistor stage needed) since LED and buzzer currents are within GPIO sink/source limits.

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| Sensor AOUT | GPIO34 | Input (ADC1_CH6) | Input-only pin, correct choice for analog read |
| Green LED | GPIO25 | Output | 220Ω series resistor to GND |
| Yellow LED | GPIO26 | Output | 220Ω series resistor to GND |
| Red LED | GPIO27 | Output | 220Ω series resistor to GND |
| Buzzer | GPIO32 | Output | Active buzzer, direct drive |

### Component List
- ESP32 DevKit V1 (30-pin)
- Capacitive Soil Moisture Sensor v1.2
- 3× LED (green/yellow/red) + 3× 220Ω resistor
- 1× 5V active buzzer
- Breadboard + jumper wires

### Power Requirements
- Sensor: 3.3V–5.5V (using 3.3V rail here)
- Total board current draw: <100mA (LEDs + buzzer combined)
- USB power (5V/500mA) sufficient

### Safety Notes
- GPIO34 is **input-only** — never configure as OUTPUT
- Capacitive sensor does not corrode like resistive types; safe for continuous power
- Calibrate `AIR_VALUE`/`WATER_VALUE` per individual sensor unit before deployment

---

## 2. ESP32 Air Quality Monitor

**File:** `esp32-air-quality-monitor-wiring.svg` ⚠️ Verified with 1 excluded entry

### Engineering Notes
MQ-135 gas sensor requires a burn-in/heater warm-up period (~24–48 hrs for stable baseline, several minutes for a rough reading) — this should be called out in the tutorial text but is a firmware/UX note, not a wiring issue. The relay-driven fan gives simple on/off ventilation control once a threshold is crossed. **One wiring table entry was excluded from this diagram**: the site currently lists an "Air Quality LED" wired via I2C (SDA→GPIO21, SCL→GPIO22), but an LED has no I2C interface, and the Beginner `.ino` never calls `Wire.begin()` or references GPIO21/22 at all. This is a content-generation defect, not a real component — see remaining blockers.

### GPIO Mapping (verified subset only)
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| MQ-135 AOUT | GPIO34 | Input (ADC1_CH6) | Input-only pin, correct |
| Fan Relay IN | GPIO26 | Output | Drives relay module |
| ~~Air Quality LED SDA~~ | ~~GPIO21~~ | — | **Excluded — invalid, see blockers** |
| ~~Air Quality LED SCL~~ | ~~GPIO22~~ | — | **Excluded — invalid, see blockers** |

### Component List
- ESP32 DevKit V1
- MQ-135 Gas Sensor module
- 1-channel relay module + fan/ventilation load
- Breadboard + jumper wires
- *(Pending: correct status indicator component once content is fixed)*

### Power Requirements
- MQ-135: 5V heater supply recommended (module has onboard regulator, accepts 3.3–5V logic)
- Relay module: 5V coil, switches external fan circuit (mains or 12V — isolate accordingly)

### Safety Notes
- If fan is mains-voltage, use a relay module rated for mains switching with proper isolation — do not wire mains directly near the breadboard
- MQ-135 surface gets warm during operation (normal) — mount with ventilation clearance

---

## 3. ESP32 Smart Parking Sensor

**File:** `esp32-smart-parking-sensor-wiring.svg` ✅ Verified

### Engineering Notes
Standard HC-SR04 ultrasonic ranging. The critical engineering detail — correctly reflected in the diagram — is the **mandatory voltage divider on ECHO**: the sensor's ECHO pin outputs 5V, but ESP32 GPIO inputs are 3.3V-tolerant only. A 10kΩ/20kΩ divider brings this down to a safe ~3.3V.

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| TRIG | GPIO5 | Output | 3.3V output is fine for TRIG |
| ECHO | GPIO18 | Input | **Via 10kΩ/20kΩ divider — 5V→3.3V** |
| Green LED (Free) | GPIO25 | Output | 220Ω resistor to GND |
| Red LED (Occupied) | GPIO26 | Output | 220Ω resistor to GND |

### Component List
- ESP32 DevKit V1
- HC-SR04 Ultrasonic Distance Sensor
- 10kΩ + 20kΩ resistors (voltage divider)
- 2× LED (green/red) + 2× 220Ω resistor

### Power Requirements
- HC-SR04: 5V (Vin pin) — does not operate reliably on 3.3V
- Total current: <60mA

### Safety Notes
- **Do not skip the voltage divider** — direct 5V ECHO into GPIO18 risks permanent pin damage over repeated exposure
- Mount sensor with a clear, unobstructed line of sight to the parking bay surface

---

## 4. ESP32 Water Leak Detector

**File:** `esp32-water-leak-detector-wiring.svg` ✅ Verified

### Engineering Notes
Resistive water sensor strip provides both an analog (graduated wetness level) and digital (simple wet/dry threshold) output, both wired here for redundancy. Direct-drive buzzer + dual LED gives an unmistakable local alarm.

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| Sensor AOUT | GPIO34 | Input (ADC1_CH6) | Input-only pin |
| Sensor DOUT | GPIO35 | Input (ADC1_CH7) | Input-only pin |
| Buzzer | GPIO25 | Output | Active buzzer |
| Red LED (Leak) | GPIO26 | Output | 220Ω resistor to GND |
| Green LED (Normal) | GPIO27 | Output | 220Ω resistor to GND |

### Component List
- ESP32 DevKit V1
- Resistive Water/Rain Sensor strip
- 1× 5V active buzzer
- 2× LED (red/green) + 2× 220Ω resistor

### Power Requirements
- Sensor: 3.3V, low current
- Total board draw: <80mA

### Safety Notes
- Resistive sensors corrode over time under continuous power — consider GPIO-switched VCC (power only during reads) for long-term deployments
- Position sensor strip at the lowest point of the monitored area for earliest leak detection

---

## 5. ESP32 Smart Street Light

**File:** `esp32-smart-street-light-wiring.svg` ⚠️ Verified with 1 excluded entry

### Engineering Notes
Simple LDR voltage-divider circuit drives an ambient-light threshold that switches a relay-controlled light circuit. **One wiring table entry was excluded**: the site lists a "Motion Sensor" wired via I2C (SDA→GPIO21, SCL→GPIO22), but this component is never wired or referenced in the Beginner `.ino` — same content-generation defect as the Air Quality Monitor. Motion-triggered dimming would be a reasonable Intermediate/Advanced-stage feature, but it isn't implemented in the code this diagram is verified against.

### GPIO Mapping (verified subset only)
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| LDR signal | GPIO33 | Input (ADC1_CH5) | Input-only pin, voltage divider |
| Street Light Relay | GPIO25 | Output | Drives relay module |
| ~~Motion Sensor SDA~~ | ~~GPIO21~~ | — | **Excluded — invalid, see blockers** |
| ~~Motion Sensor SCL~~ | ~~GPIO22~~ | — | **Excluded — invalid, see blockers** |

### Component List
- ESP32 DevKit V1
- LDR (photoresistor) + fixed resistor (voltage divider)
- 1-channel relay module + light fixture
- *(Pending: correct motion sensor component once content is fixed)*

### Power Requirements
- LDR divider: 3.3V, negligible current
- Relay: 5V coil, switches external light circuit (isolate mains wiring properly)

### Safety Notes
- If switching a mains-voltage light fixture, use a properly rated relay and enclosure — do not expose mains wiring on an open breadboard

---

## 6. ESP32 LED Matrix Display

**File:** `esp32-led-matrix-display-wiring.svg` ✅ Verified

### Engineering Notes
Standard MAX7219-driven 8×8 matrix over SPI-like 3-wire interface (DIN/CS/CLK). Module requires 5V for correct brightness/contrast, sourced from Vin rather than the 3.3V rail.

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| DIN (MOSI) | GPIO23 | Output | Data to MAX7219 |
| CS | GPIO5 | Output | Chip select |
| CLK | GPIO18 | Output | Clock |

### Component List
- ESP32 DevKit V1
- MAX7219 8×8 LED Matrix module (single unit)

### Power Requirements
- Matrix: 5V (Vin) — 3.3V under-powers the display
- Current scales with lit-pixel count; worst case (all LEDs lit) ~200–300mA per module

### Safety Notes
- When chaining multiple matrix modules, CS and CLK are shared; only DOUT→DIN daisy-chains between modules
- No GPIO34 usage in this project — a previously-flagged stray safety-note reference has been removed (see files-changed report)

---

## 7. ESP32 MQTT Sensor Dashboard

**File:** `esp32-mqtt-sensor-dashboard-wiring.svg` ✅ Verified

### Engineering Notes
Pure sensor-to-cloud pipeline — DHT22 reads locally, ESP32 publishes over Wi-Fi/MQTT to a broker (Node-RED/dashboard on the receiving end). No physical output exists on this beginner build; all "dashboard" behavior happens off-device.

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| DHT22 DATA | GPIO4 | Input/Output (single-wire) | Requires 10kΩ pull-up to 3.3V |

### Component List
- ESP32 DevKit V1
- DHT22 Temperature/Humidity sensor
- 1× 10kΩ resistor (pull-up)

### Power Requirements
- DHT22: 3.3V, low current (<2.5mA)
- Wi-Fi radio active transmission draws up to ~240mA in bursts — ensure USB supply can handle transients

### Safety Notes
- No GPIO26/GPIO34 usage in this project — previously-flagged stray safety-note references have been removed (see files-changed report)
- Do not omit the pull-up resistor; DHT22 single-wire protocol is unreliable without it

---

## 8. ESP32 BLE Beacon

**File:** `esp32-ble-beacon-wiring.svg` ✅ Verified — no external wiring by design

### Engineering Notes
Pure software/radio project. The ESP32's onboard BLE 4.2 radio broadcasts an iBeacon-format advertising packet; no GPIO wiring exists or is needed for the Beginner stage. This is correctly reflected as "no external wiring" in both the site's own wiring table and the `.ino` source.

### GPIO Mapping
*(None — no external hardware connections)*

### Component List
- ESP32 DevKit V1 only

### Power Requirements
- USB power (5V/500mA); BLE advertising draws modest, intermittent current (<50mA average)

### Safety Notes
- None applicable — no external circuit

---

## 9. ESP32-CAM QR Code Scanner

**File:** `esp32-cam-qr-scanner-wiring.svg` ✅ Verified — exact match to standard AI-Thinker pinout

### Engineering Notes
This is the reference-quality diagram in the set: every pin was cross-checked against the Beginner `.ino` and matches the industry-standard AI-Thinker ESP32-CAM pin map exactly. The onboard OV2640 ribbon is factory-soldered — no manual camera wiring is needed. The only "wiring" a builder performs is the FTDI programmer connection for flashing, including the well-known **IO0→GND upload-mode jumper** (must be removed post-flash for normal boot).

### GPIO Mapping
| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| PWDN | GPIO32 | Output | Power-down control |
| RESET | -1 (n/c) | — | Not connected on AI-Thinker |
| XCLK | GPIO0 | Output | Camera clock — shared with boot-strap pin |
| SIOD (SDA) | GPIO26 | I/O | Camera I2C config bus |
| SIOC (SCL) | GPIO27 | Output | Camera I2C config bus |
| VSYNC | GPIO25 | Input | Frame sync |
| HREF | GPIO23 | Input | Line sync |
| PCLK | GPIO22 | Input | Pixel clock |
| Y9–Y2 (8-bit data) | GPIO35,34,39,36,21,19,18,5 | Input | Parallel pixel data bus |
| U0R / U0T | GPIO3 / GPIO1 | I/O | FTDI programming UART |
| IO0 | GPIO0 | Output (temp) | Upload-mode jumper to GND, remove after flashing |

### Component List
- ESP32-CAM (AI-Thinker) board with onboard OV2640
- FTDI USB-to-serial programmer (3.3V logic)
- Jumper wires (programming only)

### Power Requirements
- 5V via FTDI or dedicated supply — **the onboard regulator is under-specced for Wi-Fi transmit bursts on some clone boards**; use a supply capable of ≥500mA, or add a 1000µF capacitor across 5V/GND if brownouts occur during capture+Wi-Fi
- Do not power the camera from a microcontroller's 3.3V regulator (e.g., an Uno's onboard reg) — insufficient current

### Safety Notes
- GPIO0 low at boot = flashing mode; GPIO0 floating/high at boot = normal run mode — this is the #1 support issue for ESP32-CAM builders
- Never connect both FTDI 5V and an external 5V supply simultaneously (back-powering risk)

---

## 🔴 10. ESP32 Camera Capture Server — Engineering Review (No Diagram Produced)

**File:** *(none — blocked)*

### Why This Project Is Technically Incorrect

The current site content treats "Camera Capture Server" as a generic analog-sensor project:

- Wiring table: `Camera Module signal → GPIO4 (analog input)`, `MicroSD Card → GPIO2 (digital control)`
- Beginner code: a single `analogRead(GPIO4)` compared against a threshold — no camera driver, no image buffer, no SD card write, no HTTP server

This does not describe a camera in any electrical sense. A camera module (OV2640, as used across the ESP32-CAM family) requires a parallel data interface, not a single ADC pin:

| Real Requirement | Current (Incorrect) Content |
|---|---|
| ~14 dedicated GPIOs (XCLK, PCLK, VSYNC, HREF, 8× data lines, SIOD, SIOC, PWDN) | 1 GPIO (GPIO4), treated as analog sensor |
| `esp_camera.h` driver + frame buffer management | No camera library referenced anywhere |
| 4-bit SDMMC or SPI interface for microSD | GPIO2 treated as a simple digital output |
| On AI-Thinker boards, **GPIO4 is the onboard flash LED** and **GPIO2 is an SDMMC data line** | Both reassigned to unrelated generic sensor roles |

### What Hardware Should Actually Be Used
- **ESP32-CAM (AI-Thinker)** board — same hardware family already correctly documented in the QR Code Scanner project (#9 above)
- Optional: FTDI programmer for flashing (camera boards have no onboard USB)
- Optional: microSD card if local storage is desired (uses the board's built-in SDMMC pins, not general GPIO)

### What Wiring Should Actually Exist
Identical camera pin map to the QR Code Scanner (#9): PWDN=32, XCLK=0, SIOD=26, SIOC=27, VSYNC=25, HREF=23, PCLK=22, Y9–Y2 on GPIO35/34/39/36/21/19/18/5, plus the FTDI programming connections and IO0→GND upload jumper.

### What Code Architecture Is Expected
A real "Camera Capture Server" should:
1. Initialize the camera via `esp_camera_init()` with the AI-Thinker pin config struct
2. Connect to Wi-Fi
3. Run a lightweight HTTP server (e.g., `WebServer` or the official `CameraWebServer` example pattern) that serves either:
   - A single JPEG snapshot per request at an endpoint like `/capture`, or
   - An MJPEG stream at `/stream`
4. Optionally write captured frames to microSD via the board's SDMMC interface (not a general-purpose GPIO)

### Recommendation
Rewrite this project from scratch using the pin map and board already verified in project #9. Do not attempt to patch the existing wiring table — the underlying concept (camera-as-analog-sensor) is fundamentally incompatible with real camera hardware, so a partial fix would still misrepresent how a camera module works to learners.

---

## Summary Table — Integration Readiness

| # | Project | Diagram | Safe to Integrate? |
|---|---|---|---|
| 1 | Soil Moisture Monitor | ✅ | Yes |
| 2 | Air Quality Monitor | ⚠️ | Yes, with the excluded I2C LED entry noted as a known content gap |
| 3 | Smart Parking Sensor | ✅ | Yes |
| 4 | Water Leak Detector | ✅ | Yes |
| 5 | Smart Street Light | ⚠️ | Yes, with the excluded I2C motion sensor entry noted as a known content gap |
| 6 | LED Matrix Display | ✅ | Yes |
| 7 | MQTT Sensor Dashboard | ✅ | Yes |
| 8 | BLE Beacon | ✅ | Yes (no wiring by design) |
| 9 | ESP32-CAM QR Code Scanner | ✅ | Yes — reference-quality |
| 10 | Camera Capture Server | 🔴 | **No — requires full content rewrite first** |

**Remaining blockers before full integration:**
1. Air Quality Monitor and Smart Street Light source YAML still contain the invalid I2C entries — diagrams are safe to integrate now, but the *text/wiring table* on those pages will still show the bad entries until the content itself is edited.
2. Camera Capture Server needs a complete content rewrite (wiring table + code) before any diagram can be produced.
3. LED Matrix Display and MQTT Sensor Dashboard safety-note text (GPIO34 / GPIO26 references) still needs removal at the content level — the diagrams themselves never included these errors.
