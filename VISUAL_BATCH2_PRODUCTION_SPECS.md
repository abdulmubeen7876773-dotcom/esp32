# Visual Batch 2 Production Specs

Batch 2 covers I2C, display, and environmental wiring guide assets only. This file is the generation-ready source for five standalone SVG wiring diagrams. No site references, YAML image fields, generated HTML, CSS, sitemap, SEO metadata, commits, or pushes are changed in this phase.

## Batch 2 Assets

| Asset ID | Page | Target filename |
| --- | --- | --- |
| V010 | `/guides/connect-oled-esp32.html` | `connect-oled-esp32-wiring.svg` |
| V013 | `/guides/environmental-sensors.html` | `environmental-sensors-wiring.svg` |
| V014 | `/guides/i2c-communication.html` | `i2c-communication-wiring.svg` |
| V016 | `/guides/oled-display-esp32.html` | `oled-display-esp32-wiring.svg` |
| V021 | `/guides/smart-environment-monitor-capstone.html` | `smart-environment-monitor-capstone-wiring.svg` |

## Locked Visual Style

- Premium engineering documentation matching Batch 1.
- Realistic ESP32 DevKit board and realistic breadboard where appropriate.
- Realistic SSD1306 OLED, BME280 module, potentiometer, LEDs, button, and resistors where required.
- Clean white/light neutral background.
- Circuit fills roughly 80-85% of a 16:9 canvas.
- Minimal title area.
- Readable GPIO, SDA, SCL, voltage, resistor, polarity, and common-ground labels.
- Wire colors: red = VCC / 3.3 V, black = GND, green = I2C SDA, purple = I2C SCL, yellow = analog signal, orange = digital/control, blue = secondary signal.
- No marketing panels, decorative clutter, fake dashboard, fake readings, duplicated modules, Arduino Uno D-pin naming, or swapped SDA/SCL.

---

## V010 - Connect OLED Display with ESP32

- Asset ID: `V010`
- Page title: Connect OLED Display with ESP32 | ESP32 Engine
- Page URL: `https://esp32engine.com/guides/connect-oled-esp32.html`
- Source file: `content/guides/connect-oled-esp32.yaml`
- Target filename: `connect-oled-esp32-wiring.svg`
- Target folder: `/assets/visuals/guides/wiring`
- Asset type: Wiring diagram with I2C bus labels
- Exact hardware shown: ESP32 DevKit, breadboard or direct jumper layout, one SSD1306 0.96 inch I2C OLED module with VCC/GND/SDA/SCL pins, USB cable reference.
- Exact GPIO mapping: OLED SDA -> ESP32 GPIO21; OLED SCL -> ESP32 GPIO22.
- Exact power mapping: OLED VCC -> ESP32 3.3 V; OLED GND -> ESP32 GND.
- Exact wire colors: red 3.3 V to OLED VCC; black GND to OLED GND; green GPIO21 to OLED SDA; purple GPIO22 to OLED SCL.
- Required labels: `ESP32 DevKit`, `SSD1306 I2C OLED`, `OLED VCC`, `OLED GND`, `OLED SDA`, `OLED SCL`, `GPIO21 SDA`, `GPIO22 SCL`, `3.3 V`, `GND`, `address 0x3C or 0x3D`.
- Required annotations: This is four-pin I2C OLED wiring; source uses `Wire.begin(21, 22)`; try `0x3C` first and scan/check `0x3D` if blank.
- Safety note: Use 3.3 V for this ESP32 beginner wiring even if some OLED modules tolerate 5 V.
- What must NOT appear: SPI OLED pins such as MOSI/CLK/DC/CS, 5 V power as the recommended beginner path, fake display readings, Arduino D-pin labels, swapped SDA/SCL.
- Aspect ratio: 16:9 landscape, 1600x900 SVG viewport.
- Recommended placement: Existing guide wiring section.
- Alt text: ESP32 wired to an SSD1306 I2C OLED with VCC to 3.3 V, GND to GND, SDA to GPIO21, and SCL to GPIO22.
- TechnicalVerification: YES

---

## V013 - ESP32 Environmental Sensors Tutorial

- Asset ID: `V013`
- Page title: ESP32 Environmental Sensors Tutorial | ESP32 Engine
- Page URL: `https://esp32engine.com/guides/environmental-sensors.html`
- Source file: `content/guides/environmental-sensors.yaml`
- Target filename: `environmental-sensors-wiring.svg`
- Target folder: `/assets/visuals/guides/wiring`
- Asset type: Shared I2C wiring diagram
- Exact hardware shown: ESP32 DevKit V1, breadboard, BME280 environmental sensor module, SSD1306 OLED display, jumper wires.
- Exact GPIO mapping: BME280 SDA and OLED SDA share ESP32 GPIO21; BME280 SCL and OLED SCL share ESP32 GPIO22.
- Exact power mapping: BME280 VIN/VCC and OLED VCC share ESP32 3.3 V; BME280 GND and OLED GND share ESP32 GND.
- Exact wire colors: red shared 3.3 V bus; black shared GND bus; green shared SDA bus from GPIO21 to both devices; purple shared SCL bus from GPIO22 to both devices.
- Required labels: `GPIO21 SDA shared`, `GPIO22 SCL shared`, `BME280 VIN/VCC`, `BME280 GND`, `BME280 SDA`, `BME280 SCL`, `OLED VCC`, `OLED GND`, `OLED SDA`, `OLED SCL`, `3.3 V`, `GND`, `BME280 0x76/0x77`, `OLED 0x3C`.
- Required annotations: BME280 and OLED share the same I2C bus; source code uses `I2C_SDA = 21`, `I2C_SCL = 22`, OLED address `0x3C`, and BME280 address test `0x76` then `0x77`.
- Safety note: Use 3.3 V for both modules and common GND; do not swap SDA/SCL.
- What must NOT appear: Separate fake I2C buses, DHT22 instead of BME280, 5 V as the recommended beginner power, invented addresses beyond those documented, fake environmental readings.
- Aspect ratio: 16:9 landscape, 1600x900 SVG viewport.
- Recommended placement: Existing guide wiring section.
- Alt text: ESP32 shared I2C wiring with BME280 and SSD1306 OLED both connected to GPIO21 SDA, GPIO22 SCL, 3.3 V, and GND.
- TechnicalVerification: YES

---

## V014 - ESP32 I2C Communication Tutorial

- Asset ID: `V014`
- Page title: ESP32 I2C Communication Tutorial | ESP32 Engine
- Page URL: `https://esp32engine.com/guides/i2c-communication.html`
- Source file: `content/guides/i2c-communication.yaml`
- Target filename: `i2c-communication-wiring.svg`
- Target folder: `/assets/visuals/guides/wiring`
- Asset type: Shared I2C bus wiring diagram
- Exact hardware shown: ESP32 DevKit, breadboard, SSD1306 OLED display, BME280 sensor module, USB/Serial Monitor reference.
- Exact GPIO mapping: OLED SDA and BME280 SDA share ESP32 GPIO21; OLED SCL and BME280 SCL share ESP32 GPIO22.
- Exact power mapping: OLED VCC and BME280 VIN/VCC -> ESP32 3.3 V; OLED GND and BME280 GND -> ESP32 GND.
- Exact wire colors: red shared 3.3 V; black common GND; green shared SDA from GPIO21; purple shared SCL from GPIO22.
- Required labels: `ESP32 controller`, `GPIO21 SDA`, `GPIO22 SCL`, `OLED 0x3C/0x3D`, `BME280 0x76/0x77`, `shared I2C bus`, `3.3 V`, `GND`, `I2C scanner`.
- Required annotations: Two devices share SDA/SCL because they have different addresses; source scanner uses `Wire.begin(I2C_SDA, I2C_SCL)` with `I2C_SDA = 21`, `I2C_SCL = 22`.
- Safety note: Do not connect GPIO21 or GPIO22 to 5 V logic; keep wiring short and common ground shared.
- What must NOT appear: Separate private SDA/SCL lines per device, swapped SDA/SCL, invented address values, Arduino D-pin labels, fake bus analyzer display.
- Aspect ratio: 16:9 landscape, 1600x900 SVG viewport.
- Recommended placement: Existing guide wiring section.
- Alt text: ESP32 I2C bus wiring showing GPIO21 SDA and GPIO22 SCL shared by an SSD1306 OLED and BME280 sensor.
- TechnicalVerification: YES

---

## V016 - ESP32 OLED Display Tutorial

- Asset ID: `V016`
- Page title: ESP32 OLED Display Tutorial: SSD1306 Wiring and Arduino Code | ESP32 Engine
- Page URL: `https://esp32engine.com/guides/oled-display-esp32.html`
- Source file: `content/guides/oled-display-esp32.yaml`
- Target filename: `oled-display-esp32-wiring.svg`
- Target folder: `/assets/visuals/guides/wiring`
- Asset type: OLED plus analog-input wiring diagram
- Exact hardware shown: ESP32 DevKit, breadboard, SSD1306 I2C OLED, 10 kOhm potentiometer, jumper wires.
- Exact GPIO mapping: OLED SDA -> ESP32 GPIO21; OLED SCL -> ESP32 GPIO22; potentiometer middle wiper -> ESP32 GPIO34.
- Exact power mapping: OLED VCC -> ESP32 3.3 V; OLED GND -> ESP32 GND; potentiometer outside legs -> ESP32 3.3 V and GND.
- Exact wire colors: red 3.3 V to OLED and potentiometer high side; black GND to OLED and potentiometer low side; green GPIO21 to OLED SDA; purple GPIO22 to OLED SCL; yellow GPIO34 to potentiometer middle wiper.
- Required labels: `GPIO21 SDA`, `GPIO22 SCL`, `GPIO34 ADC`, `SSD1306 OLED`, `10 kOhm potentiometer`, `middle wiper`, `3.3 V`, `GND`, `0-3.3 V analog only`, `OLED address 0x3C`.
- Required annotations: OLED uses I2C while GPIO34 reads the live analog value shown on screen; source code uses `POT_PIN = 34`, `I2C_SDA = 21`, `I2C_SCL = 22`, and `OLED_ADDRESS = 0x3C`.
- Safety note: Keep GPIO34 voltage within 0-3.3 V and power the OLED from 3.3 V for beginner wiring.
- What must NOT appear: fake separate PWM/display module, GPIO8, 5 V analog input, SPI OLED pins, fake sensor data, Arduino D-pin labels.
- Aspect ratio: 16:9 landscape, 1600x900 SVG viewport.
- Recommended placement: Existing guide wiring section.
- Alt text: ESP32 OLED and potentiometer wiring with OLED SDA on GPIO21, SCL on GPIO22, and potentiometer wiper on GPIO34.
- TechnicalVerification: YES

---

## V021 - ESP32 Smart Environment Monitor Capstone

- Asset ID: `V021`
- Page title: ESP32 Smart Environment Monitor Capstone | ESP32 Engine
- Page URL: `https://esp32engine.com/guides/smart-environment-monitor-capstone.html`
- Source file: `content/guides/smart-environment-monitor-capstone.yaml`
- Target filename: `smart-environment-monitor-capstone-wiring.svg`
- Target folder: `/assets/visuals/guides/wiring`
- Asset type: Complete capstone wiring diagram
- Exact hardware shown: ESP32 DevKit V1, breadboard, BME280 module, SSD1306 OLED, green LED, red LED, one push button, two 220 ohm or 330 ohm resistors, jumper wires.
- Exact GPIO mapping: BME280 SDA and OLED SDA share GPIO21; BME280 SCL and OLED SCL share GPIO22; green LED output -> GPIO18 through resistor; red LED output -> GPIO19 through resistor; page button -> GPIO23 using `INPUT_PULLUP`.
- Exact power mapping: BME280 VCC and OLED VCC -> ESP32 3.3 V; BME280 GND, OLED GND, LED cathodes, and button ground -> ESP32 GND.
- Exact wire colors: red shared 3.3 V; black common GND; green shared SDA; purple shared SCL; blue GPIO18 to green LED resistor; orange GPIO19 to red LED resistor; orange GPIO23 to button input.
- Required labels: `GPIO21 SDA shared`, `GPIO22 SCL shared`, `GPIO18 green LED`, `GPIO19 red LED`, `GPIO23 button INPUT_PULLUP`, `220 or 330 ohm resistor`, `LED anode long leg`, `LED cathode short leg`, `BME280`, `SSD1306 OLED`, `3.3 V`, `GND`, `BME280 0x76/0x77`, `OLED 0x3C`.
- Required annotations: Button pressed reads LOW because it connects GPIO23 to GND; green LED means normal, red LED means warning; source uses only green and red LEDs, not a yellow LED.
- Safety note: Use current-limiting resistors with both LEDs; use 3.3 V for BME280/OLED; common ground is required.
- What must NOT appear: yellow LED hardware, missing LED resistors, button tied to 3.3 V, 5 V I2C pull-ups, fake readings, duplicate OLED/BME280 modules, Arduino D-pin labels.
- Aspect ratio: 16:9 landscape, 1600x900 SVG viewport.
- Recommended placement: Existing guide wiring section.
- Alt text: ESP32 smart environment monitor wiring with BME280 and OLED on shared I2C, green LED on GPIO18, red LED on GPIO19, and page button on GPIO23.
- TechnicalVerification: YES

---

## Batch Summary

- Number of Batch 2 assets: 5.
- Number technically verified: 5.
- Number blocked: 0.
- Every spec is ready for image generation: YES.

BATCH 2 SPECS READY
