# ESP32 Engine Top 5 SEO Micro Audit

Scope: guides/pull-up-vs-pull-down-resistors.html, guides/digital-inputs-floating-pins.html, components/bme280.html, projects/esp32-led-matrix-display.html, projects/esp32-ir-remote-control.html.

## 1. ESP32 Pull-up vs Pull-down Resistors

- Current title: ESP32 Pull-up vs Pull-down Resistors: Button Wiring | ESP32 Engine
- Current meta: Choose ESP32 pull-up or pull-down button wiring with INPUT_PULLUP logic, 10 kOhm resistor examples, floating GPIO fixes, and pressed HIGH/LOW behavior.
- Current H1: Pull-up vs Pull-down Resistors
- Ranking opportunity: Already near page 1 for ESP32 pull-up and pull-down resistor queries; CTR can improve by making button wiring and INPUT_PULLUP intent clearer.
- Search intent: Beginner wants to choose pull-up vs pull-down wiring, understand internal ESP32 pull modes, and stop floating button input behavior.
- CTR issue: The previous wording was accurate but more generic; adding button wiring and pressed HIGH/LOW behavior makes the result more specific.
- Content gap: Query intent expects immediate comparison of default state, pressed state, INPUT_PULLUP, INPUT_PULLDOWN, and external resistor context.
- Internal linking gap: The page already fits the mission path from floating pins to debouncing; no broad link expansion needed.
- Snippet opportunity: The lead now answers when to use pull-up vs pull-down immediately.
- Recommended change: Keep the concise title/meta and direct lead. Avoid adding more FAQ or long explanatory blocks because the page is already ranking.
- Risk level: LOW

## 2. ESP32 Digital Inputs and Floating Pins

- Current title: ESP32 Floating Pins and Digital Inputs Explained | ESP32 Engine
- Current meta: Fix random ESP32 digital input readings by understanding floating GPIO pins, HIGH/LOW logic, INPUT mode, and when pull-up or pull-down resistors are needed.
- Current H1: Understanding Digital Inputs and Floating Pins
- Ranking opportunity: Current impressions indicate the page can move toward page 1 for random HIGH/LOW and floating GPIO searches.
- Search intent: User sees unstable ESP32 digital input readings and needs to understand floating pins before choosing pull-up or pull-down wiring.
- CTR issue: The old title led with digital inputs; the query opportunity is more directly about floating pins and random readings.
- Content gap: The first section must make clear that INPUT does not enable a default pull resistor.
- Internal linking gap: The page should naturally point readers to the pull-up/pull-down guide rather than duplicating it.
- Snippet opportunity: The lead and first concept block now explain floating GPIO behavior directly.
- Recommended change: Keep the floating-pin-first title/meta and existing path link to the pull resistor guide.
- Risk level: LOW

## 3. BME280 Component Page

- Current title: BME280 ESP32 Sensor Wiring and Code
- Current meta: Wire a BME280 sensor to ESP32 over I2C with GPIO21/GPIO22, 3.3 V power, Arduino code, 0x76/0x77 address handling, and temperature, humidity, pressure, and altitude-estimate guidance.
- Current H1: BME280 ESP32 Sensor Wiring and Code
- Ranking opportunity: Search Console shows ESP32-specific BME280 intent with room to improve CTR and relevance.
- Search intent: User wants BME280 wiring, ESP32 I2C pins, address handling, readings, and practical weather-project use.
- CTR issue: Broad BME280 wording can compete poorly with generic component searches; ESP32 wiring/code language is stronger.
- Content gap: The page must quickly distinguish BME280 from BMP280 and clarify I2C, addresses, and weather-project links.
- Internal linking gap: Strong connections to IoT Weather Station, OLED Weather Clock, MQTT Sensor Dashboard, I2C, and OLED display content are useful.
- Snippet opportunity: The summary and opening ELI12 copy now name I2C, GPIO21/GPIO22, 0x76/0x77, and the measured values.
- Recommended change: Keep ESP32-specific title/summary and weather-project links. Do not chase generic "BME280" rankings.
- Risk level: LOW

## 4. ESP32 LED Matrix Display

- Current title: ESP32 LED Matrix Display: MAX7219 Scrolling Text
- Current meta: Build an ESP32 MAX7219 LED matrix display with SPI wiring, 5 V matrix power, MD_Parola scrolling text code, brightness control, and troubleshooting.
- Current H1: Build an LED Matrix Display
- Ranking opportunity: Near top 10; adding MAX7219 and scrolling text specificity should improve query match.
- Search intent: User wants to build an ESP32 LED matrix, usually with a MAX7219 module and scrolling message code.
- CTR issue: The previous title was broad and did not expose the strongest hardware and behavior terms.
- Content gap: The page should say what the learner builds before broader display theory.
- Internal linking gap: OLED display and OLED Weather Clock links are useful comparisons without diluting the LED matrix page.
- Snippet opportunity: The title/meta and project story now foreground MAX7219, scrolling text, SPI wiring, and brightness.
- Recommended change: Keep the tightened title/meta/story. Avoid turning the project into a generic display guide.
- Risk level: LOW

## 5. ESP32 IR Remote Control

- Current title: ESP32 IR Remote Control: IRremote Receive and Send
- Current meta: Build an ESP32 IR remote with TSOP38238 receiver wiring, transistor IR LED driver, IRremote NEC receive/send code, line-of-sight testing, and safety limits.
- Current H1: Build an ESP32 IR Remote Control Demo
- Ranking opportunity: Positions around the low teens can improve with clearer receive/send, IRremote, and NEC wording.
- Search intent: User wants to receive IR codes, decode remote buttons, and possibly send known commands with ESP32.
- CTR issue: The old wording did not expose receive/send behavior as clearly.
- Content gap: The page must distinguish NEC replay from universal IR compatibility and avoid unsafe claims.
- Internal linking gap: Digital inputs and pull-up/pull-down links are useful for receiver debugging; smart door lock link supports safety boundaries.
- Snippet opportunity: Title/meta and FAQ now name TSOP38238, transistor IR LED driver, IRremote, NEC, line of sight, and limits.
- Recommended change: Keep receive/send wording only because the actual page supports NEC learning and replay. Do not claim universal transmit.
- Risk level: LOW
