# ESP32 Engine Top 5 SEO Changelog

## guides/pull-up-vs-pull-down-resistors.html

- Source file modified: content/guides/pull-up-vs-pull-down-resistors.yaml
- Title before: ESP32 Pull-up vs Pull-down Resistors Explained | ESP32 Engine
- Title after: ESP32 Pull-up vs Pull-down Resistors: Button Wiring | ESP32 Engine
- Meta before: ESP32 pull-up vs pull-down resistors explained with button wiring, INPUT_PULLUP logic, floating GPIO fixes, and when to use each circuit.
- Meta after: Choose ESP32 pull-up or pull-down button wiring with INPUT_PULLUP logic, 10 kOhm resistor examples, floating GPIO fixes, and pressed HIGH/LOW behavior.
- Intro changes: Lead now immediately states when an ESP32 input should rest HIGH or LOW, calls out INPUT_PULLUP pressed-LOW logic, and keeps the floating GPIO fix visible.
- Internal links added: No new broad links; existing mission links to floating pins, debouncing, and button paths were preserved.
- Other content changes: None beyond title/meta/lead tuning.
- Reason: Improve CTR for page-1 pull-up/pull-down and button wiring queries while preserving the successful page structure.
- Risk level: LOW

## guides/digital-inputs-floating-pins.html

- Source file modified: content/guides/digital-inputs-floating-pins.yaml
- Title before: ESP32 Digital Inputs and Floating Pins Explained | ESP32 Engine
- Title after: ESP32 Floating Pins and Digital Inputs Explained | ESP32 Engine
- Meta before: Learn why an ESP32 GPIO can return random HIGH and LOW readings when left floating, how digital inputs work, and how pull-up or pull-down resistors stabilize the input.
- Meta after: Fix random ESP32 digital input readings by understanding floating GPIO pins, HIGH/LOW logic, INPUT mode, and when pull-up or pull-down resistors are needed.
- Intro changes: Existing lead already answered the floating-pin issue directly, so it was preserved.
- Internal links added: Existing path to the pull-up/pull-down mission remains the primary contextual next step.
- Other content changes: None beyond title/meta tuning.
- Reason: Put the highest-intent "floating pins" language first for random HIGH/LOW queries.
- Risk level: LOW

## components/bme280.html

- Source file modified: content/components/bme280.yaml
- Title before: BME280 Sensor with ESP32
- Title after: BME280 ESP32 Sensor Wiring and Code
- Meta before: BME280 ESP32 wiring guide for I2C weather projects, with GPIO21/GPIO22 pinout, 3.3 V power, Arduino code, 0x76/0x77 address handling, and temperature, humidity, pressure, and altitude-estimate guidance.
- Meta after: Wire a BME280 sensor to ESP32 over I2C with GPIO21/GPIO22, 3.3 V power, Arduino code, 0x76/0x77 address handling, and temperature, humidity, pressure, and altitude-estimate guidance.
- Intro changes: Existing opening copy already explains BME280 measurements, ESP32 I2C, GPIO21/GPIO22, 0x76/0x77, and BMP280 difference, so it was preserved.
- Internal links added: Existing related links to IoT Weather Station, OLED Weather Clock, MQTT Sensor Dashboard, I2C, OLED, DHT22, SSD1306 OLED, and ESP32 DevKit were preserved.
- Other content changes: None beyond name/summary tuning.
- Reason: Make the page more clearly ESP32-specific and more action-oriented without targeting only the broad "BME280" query.
- Risk level: LOW

## projects/esp32-led-matrix-display.html

- Source file modified: content/projects/esp32-led-matrix-display.yaml
- Title before: ESP32 LED Matrix Display
- Title after: ESP32 LED Matrix Display: MAX7219 Scrolling Text
- Meta before: Build an ESP32 MAX7219 LED matrix display with SPI wiring on GPIO23, GPIO5, GPIO18, 5 V matrix power, MD_Parola scrolling text code, brightness control, and troubleshooting.
- Meta after: Build an ESP32 MAX7219 LED matrix display with SPI wiring, 5 V matrix power, MD_Parola scrolling text code, brightness control, and troubleshooting.
- Intro changes: Description and story now foreground MAX7219, scrolling text, brightness control, safe 5 V matrix power, and non-blocking display behavior.
- Internal links added: Existing related links to OLED display and OLED Weather Clock were preserved.
- Other content changes: Meta title changed to "ESP32 LED Matrix Display MAX7219 Tutorial"; broad real-time ticker wording was reduced in the main description.
- Reason: Improve query match for ESP32 LED matrix, MAX7219 ESP32, and scrolling text searches.
- Risk level: LOW

## projects/esp32-ir-remote-control.html

- Source file modified: content/projects/esp32-ir-remote-control.yaml
- Title before: ESP32 IR Remote Control with IRremote Library
- Title after: ESP32 IR Remote Control: IRremote Receive and Send
- Meta before: Build an ESP32 IR remote control with TSOP38238 receiver wiring, IRremote library code, NEC send/receive behavior, and safe compatibility limits.
- Meta after: Build an ESP32 IR remote with TSOP38238 receiver wiring, transistor IR LED driver, IRremote NEC receive/send code, line-of-sight testing, and safety limits.
- Intro changes: Description now clarifies that the project learns and replays owned NEC commands; existing story and engineering explanation preserve receive/send limits.
- Internal links added: Related guide links to Digital Inputs and Floating Pins and ESP32 Pull-up vs Pull-down Resistors support receiver-input troubleshooting; related safety/control links were preserved.
- Other content changes: FAQ answers were made more specific about NEC-only replay, allowed devices, transistor driver purpose, and transmit troubleshooting.
- Reason: Improve match for IRremote, receive IR codes, send IR codes, and NEC remote intent without overclaiming universal compatibility.
- Risk level: LOW
