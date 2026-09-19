# Visual Batch 3 Production Specs

Batch: Guide Concept Illustrations

Scope: Production specifications for Batch 3 only. These are concept/process illustrations, not wiring diagrams. No YAML references, HTML, CSS, sitemap, metadata, or page structure are modified in this phase.

## V029 - ESP32 Analog Inputs: Reading the Real World

- Asset ID: V029
- Page title: ESP32 Analog Inputs: Reading the Real World | ESP32 Engine
- Page URL: /guides/analog-inputs-reading-real-world.html
- Source file: content/guides/analog-inputs-reading-real-world.yaml
- Target filename: analog-inputs-reading-real-world-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Analog voltage becomes ADC numbers and a percent reading.
- Exact flow / architecture: Potentiometer wiper -> ESP32 ADC on GPIO34 -> Serial raw ADC and percent
- Required labels: 0 to 3.3 V only; GPIO34 input-only ADC1; analogRead(); 0 to 4095 ADC; map() to percent
- Required arrows: Voltage into ADC; Sample and convert; Print human value
- Required hardware/icons: ESP32 DevKit; Potentiometer icon; Serial output block
- Important technical limitations: Do not show 5 V into GPIO. Do not show a breadboard wiring diagram. Do not invent sensor readings.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 ADC concept showing 0 to 3.3 V on GPIO34 becoming raw values and percent output.
- TechnicalVerification: YES

## V030 - ESP32 Analog Inputs Tutorial

- Asset ID: V030
- Page title: ESP32 Analog Inputs Tutorial | ESP32 Engine
- Page URL: /guides/analog-inputs.html
- Source file: content/guides/analog-inputs.yaml
- Target filename: analog-inputs-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Analog range versus digital HIGH or LOW.
- Exact flow / architecture: Changing dial voltage -> ESP32 ADC on GPIO34 -> Many possible readings
- Required labels: Digital: LOW or HIGH; Analog: range; 0 to 3.3 V safe range; GPIO34 ADC; 0 to 4095
- Required arrows: Voltage varies; ADC samples; Number changes
- Required hardware/icons: ESP32 DevKit; Dial icon; Range scale
- Important technical limitations: Do not imply true analog output. Do not show 5 V safe on GPIO. Do not duplicate the wiring diagram.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 analog input concept comparing digital HIGH LOW with GPIO34 ADC values from 0 to 4095.
- TechnicalVerification: YES

## V031 - Blink an LED with ESP32

- Asset ID: V031
- Page title: Blink an LED with ESP32 | ESP32 Engine
- Page URL: /guides/blink-led-esp32.html
- Source file: content/guides/blink-led-esp32.yaml
- Target filename: blink-led-esp32-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: GPIO output state changes create LED blink timing.
- Exact flow / architecture: Code loop -> GPIO2 output -> LED on then off
- Required labels: digitalWrite(HIGH); delay(); digitalWrite(LOW); GPIO2; 220 ohm resistor required
- Required arrows: Set output HIGH; Wait; Set output LOW
- Required hardware/icons: ESP32 GPIO icon; LED state icon; Timing wave
- Important technical limitations: Do not replace current wiring diagram. Do not omit current-limit resistor note. Do not label Arduino D pins.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 blink concept showing code toggling GPIO2 HIGH and LOW to turn an LED on and off.
- TechnicalVerification: YES

## V032 - ESP32 Button Controls LED Tutorial

- Asset ID: V032
- Page title: ESP32 Button Controls LED Tutorial | ESP32 Engine
- Page URL: /guides/button-led-control.html
- Source file: content/guides/button-led-control.yaml
- Target filename: button-led-control-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Button input logic controls an LED output.
- Exact flow / architecture: Button press -> ESP32 reads GPIO27 -> GPIO2 LED output
- Required labels: INPUT_PULLUP; Released = HIGH; Pressed = LOW; if pressed; LED on GPIO2
- Required arrows: User presses; Code decides; Output changes
- Required hardware/icons: Button icon; ESP32 logic block; LED icon
- Important technical limitations: Do not show external pull resistor. Do not invent a different button pin. Do not make a wiring diagram.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 button control concept showing GPIO27 INPUT_PULLUP logic controlling an LED on GPIO2.
- TechnicalVerification: YES

## V033 - Connect OLED Display with ESP32

- Asset ID: V033
- Page title: Connect OLED Display with ESP32 | ESP32 Engine
- Page URL: /guides/connect-oled-esp32.html
- Source file: content/guides/connect-oled-esp32.yaml
- Target filename: connect-oled-esp32-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: I2C data and clock flow from ESP32 to SSD1306 OLED address.
- Exact flow / architecture: ESP32 controller -> I2C bus -> SSD1306 OLED
- Required labels: SDA GPIO21; SCL GPIO22; Address 0x3C or 0x3D; display.println(); display.display()
- Required arrows: Commands and pixels; Clocked data; Screen refresh
- Required hardware/icons: ESP32 DevKit; I2C bus icon; OLED icon
- Important technical limitations: Do not show SPI pins such as MOSI CLK DC CS. Do not show 5 V as preferred power. Do not duplicate wiring.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 OLED concept showing GPIO21 SDA and GPIO22 SCL carrying I2C commands to SSD1306 address 0x3C or 0x3D.
- TechnicalVerification: YES

## V034 - ESP32 Button Debounce with millis()

- Asset ID: V034
- Page title: ESP32 Button Debounce with millis() | ESP32 Engine
- Page URL: /guides/debouncing-buttons.html
- Source file: content/guides/debouncing-buttons.yaml
- Target filename: debouncing-buttons-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Raw button bounce becomes one stable press after debounce timing.
- Exact flow / architecture: Noisy button edge -> Debounce timer -> One clean event
- Required labels: GPIO27 input; Bounce transitions; millis() timing; DEBOUNCE_MS; single press event
- Required arrows: Raw changes; Wait for stable; Accept event
- Required hardware/icons: Button icon; Timing filter; Event output
- Important technical limitations: Do not show fake oscilloscope values. Do not show breadboard wiring. Do not claim bounce duration beyond source constants.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 debounce concept showing GPIO27 raw button bounce filtered by millis timing into one stable press event.
- TechnicalVerification: YES

## V035 - ESP32 Floating Pins and Digital Inputs Explained

- Asset ID: V035
- Page title: ESP32 Floating Pins and Digital Inputs Explained | ESP32 Engine
- Page URL: /guides/digital-inputs-floating-pins.html
- Source file: content/guides/digital-inputs-floating-pins.yaml
- Target filename: digital-inputs-floating-pins-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: A floating GPIO is undefined until forced HIGH or LOW.
- Exact flow / architecture: Floating GPIO27 -> No default path -> Unstable HIGH or LOW
- Required labels: INPUT mode; No pull resistor; Forced to GND = LOW; Forced to 3.3 V = HIGH; Fix with pull-up or pull-down
- Required arrows: Undefined input; Environment affects threshold; Define a default state
- Required hardware/icons: ESP32 GPIO icon; State comparison; Stability marker
- Important technical limitations: Do not invent random numeric readings. Do not show fake warning poster. Do not show full wiring diagram.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 floating input concept comparing GPIO27 floating state with forced LOW at GND and forced HIGH at 3.3 V.
- TechnicalVerification: YES

## V036 - ESP32 Environmental Sensors Tutorial

- Asset ID: V036
- Page title: ESP32 Environmental Sensors Tutorial | ESP32 Engine
- Page URL: /guides/environmental-sensors.html
- Source file: content/guides/environmental-sensors.yaml
- Target filename: environmental-sensors-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: BME280 air readings flow through ESP32 to OLED and Serial output.
- Exact flow / architecture: BME280 measures air -> ESP32 reads over I2C -> OLED and Serial show values
- Required labels: Temperature; Humidity; Pressure; GPIO21 SDA / GPIO22 SCL; 0x76 or 0x77
- Required arrows: Digital sensor data; Format readings; Display and print
- Required hardware/icons: BME280 icon; ESP32 DevKit; OLED icon
- Important technical limitations: Do not show fake weather dashboard. Do not invent exact room values. Do not duplicate shared I2C wiring.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 environmental sensor concept showing BME280 temperature humidity and pressure data flowing to ESP32 and OLED.
- TechnicalVerification: YES

## V037 - ESP32 I2C Communication Tutorial

- Asset ID: V037
- Page title: ESP32 I2C Communication Tutorial | ESP32 Engine
- Page URL: /guides/i2c-communication.html
- Source file: content/guides/i2c-communication.yaml
- Target filename: i2c-communication-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: One ESP32 controller scans shared I2C devices by address.
- Exact flow / architecture: ESP32 controller -> Shared SDA and SCL bus -> Addressed devices respond
- Required labels: SDA GPIO21; SCL GPIO22; OLED 0x3C or 0x3D; BME280 0x76 or 0x77; I2C scanner
- Required arrows: Scan addresses; Only addressed device answers; Report found devices
- Required hardware/icons: ESP32 icon; Bus icon; OLED + BME280 nodes
- Important technical limitations: Do not show separate private wires per device. Do not show long cable use. Do not use master/slave labels.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 I2C concept showing GPIO21 SDA and GPIO22 SCL shared by OLED and BME280 devices with different addresses.
- TechnicalVerification: YES

## V038 - ESP32 Multiple Buttons and State Detection Tutorial

- Asset ID: V038
- Page title: ESP32 Multiple Buttons and State Detection Tutorial | ESP32 Engine
- Page URL: /guides/multiple-buttons-state-detection.html
- Source file: content/guides/multiple-buttons-state-detection.yaml
- Target filename: multiple-buttons-state-detection-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Multiple INPUT_PULLUP buttons produce independent state events.
- Exact flow / architecture: Three button inputs -> ESP32 reads states -> Separate actions or reports
- Required labels: GPIO25 button A; GPIO26 button B; GPIO27 button C; Released = HIGH; Pressed = LOW
- Required arrows: Independent inputs; State tracking; Button events
- Required hardware/icons: Three button icons; ESP32 logic block; Event list
- Important technical limitations: Do not merge buttons into one input. Do not invent extra buttons. Do not show wiring diagram.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 multiple button concept showing GPIO25 GPIO26 and GPIO27 INPUT_PULLUP states tracked independently.
- TechnicalVerification: YES

## V039 - ESP32 OLED Display Tutorial: SSD1306 Wiring and Arduino Code

- Asset ID: V039
- Page title: ESP32 OLED Display Tutorial: SSD1306 Wiring and Arduino Code | ESP32 Engine
- Page URL: /guides/oled-display-esp32.html
- Source file: content/guides/oled-display-esp32.yaml
- Target filename: oled-display-esp32-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Analog input is read by ESP32 and formatted for OLED output.
- Exact flow / architecture: Potentiometer on GPIO34 -> ESP32 formats value -> SSD1306 OLED shows text
- Required labels: GPIO34 ADC input; 0 to 4095 raw; percent value; SDA GPIO21; SCL GPIO22
- Required arrows: Read analog value; Convert and format; Update display
- Required hardware/icons: Dial icon; ESP32 processing; OLED screen icon
- Important technical limitations: Do not show fake UI screenshot. Do not claim true analog output. Do not duplicate wiring.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 OLED display concept showing GPIO34 analog input formatted by ESP32 and sent to SSD1306 OLED over GPIO21 and GPIO22.
- TechnicalVerification: YES

## V040 - ESP32 Pull-up vs Pull-down Resistors: Button Wiring

- Asset ID: V040
- Page title: ESP32 Pull-up vs Pull-down Resistors: Button Wiring | ESP32 Engine
- Page URL: /guides/pull-up-vs-pull-down-resistors.html
- Source file: content/guides/pull-up-vs-pull-down-resistors.yaml
- Target filename: pull-up-vs-pull-down-resistors-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Pull-down and pull-up create opposite stable idle states.
- Exact flow / architecture: External pull-down -> GPIO27 default LOW -> Internal pull-up default HIGH
- Required labels: 10 kohm to GND; Button to 3.3 V; INPUT_PULLUP; Button to GND; Pressed state flips
- Required arrows: Idle LOW pattern; Compare; Idle HIGH pattern
- Required hardware/icons: Two logic panels; ESP32 GPIO27 marker; State labels
- Important technical limitations: Do not show a full breadboard layout. Do not swap pressed/released logic. Do not invent resistor values beyond source.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 pull-up versus pull-down concept comparing GPIO27 idle LOW and idle HIGH button input behavior.
- TechnicalVerification: YES

## V041 - ESP32 PWM Fundamentals Tutorial

- Asset ID: V041
- Page title: ESP32 PWM Fundamentals Tutorial | ESP32 Engine
- Page URL: /guides/pwm-fundamentals.html
- Source file: content/guides/pwm-fundamentals.yaml
- Target filename: pwm-fundamentals-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Duty cycle changes average energy while GPIO18 still switches digitally.
- Exact flow / architecture: ledcWrite duty -> GPIO18 PWM pulses -> LED perceived brightness
- Required labels: 8-bit duty 0 to 255; 0 percent off; 50 percent medium; 100 percent full; PWM frequency 5000 Hz
- Required arrows: Set duty; Fast ON/OFF switching; Eye averages brightness
- Required hardware/icons: ESP32 PWM block; Waveform strips; LED brightness scale
- Important technical limitations: Do not label GPIO8. Do not show a motor wired directly to ESP32. Do not imply a true analog voltage.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 PWM concept showing GPIO18 duty cycle pulses from 0 to 255 controlling perceived LED brightness.
- TechnicalVerification: YES

## V042 - ESP32 DHT22 Temperature and Humidity Sensor Tutorial

- Asset ID: V042
- Page title: ESP32 DHT22 Temperature and Humidity Sensor Tutorial | ESP32 Engine
- Page URL: /guides/read-temperature-dht22.html
- Source file: content/guides/read-temperature-dht22.yaml
- Target filename: read-temperature-dht22-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: DHT22 sends timed data pulses slowly on one GPIO.
- Exact flow / architecture: DHT22 senses air -> DATA pulses on GPIO4 -> ESP32 prints readings
- Required labels: 3.3 V pull-up behavior; GPIO4 DATA; Temperature; Humidity; 2 second reading pace
- Required arrows: Sensor prepares data; Pulse train; Library decodes
- Required hardware/icons: DHT22 icon; ESP32 data input; Serial output block
- Important technical limitations: Do not power data line from 5 V. Do not invent live temperature values. Do not show BME280 or I2C.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 DHT22 concept showing temperature and humidity data pulses on GPIO4 decoded by the ESP32.
- TechnicalVerification: YES

## V043 - ESP32 Reading Analog Sensors Tutorial

- Asset ID: V043
- Page title: ESP32 Reading Analog Sensors Tutorial | ESP32 Engine
- Page URL: /guides/reading-analog-sensors.html
- Source file: content/guides/reading-analog-sensors.yaml
- Target filename: reading-analog-sensors-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Light changes an LDR voltage divider, which changes GPIO34 ADC readings.
- Exact flow / architecture: Light on LDR -> Voltage divider output -> GPIO34 ADC threshold logic
- Required labels: LDR + 10 kohm divider; 3.3 V safe range; GPIO34; Calibrate dark and bright; Choose threshold
- Required arrows: Light changes resistance; Voltage changes; Code decides light or dark
- Required hardware/icons: LDR icon; ESP32 ADC block; Threshold scale
- Important technical limitations: Do not invent exact lux values. Do not show 5 V into GPIO. Do not duplicate wiring.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 analog sensor concept showing an LDR voltage divider feeding GPIO34 and threshold logic.
- TechnicalVerification: YES

## V044 - ESP32 Smart Environment Monitor Capstone

- Asset ID: V044
- Page title: ESP32 Smart Environment Monitor Capstone | ESP32 Engine
- Page URL: /guides/smart-environment-monitor-capstone.html
- Source file: content/guides/smart-environment-monitor-capstone.yaml
- Target filename: smart-environment-monitor-capstone-concept.svg
- Target folder: /assets/visuals/guides/concepts
- Asset type: CONCEPT_ILLUSTRATION
- Concept being explained: Sensor readings move through ESP32 logic to OLED pages and LED alerts.
- Exact flow / architecture: BME280 readings -> ESP32 threshold logic -> OLED pages and LED alerts
- Required labels: GPIO21 / GPIO22 I2C; Temp humidity pressure; TEMP_APPROACH_C; TEMP_WARNING_C; Green normal / red warning
- Required arrows: Measure; Process status; Display and alert
- Required hardware/icons: BME280 icon; ESP32 logic; OLED + LEDs + button
- Important technical limitations: Do not show a yellow LED hardware part. Do not invent dashboard values. Do not make this a wiring diagram.
- What must NOT appear: breadboard wiring, fake jumper wires, fake GPIO circuits beyond supported labels, decorative posters, fake dashboards, fake screenshots, marketing panels, or unsupported output values.
- Aspect ratio: 16:9, 1600x900 SVG viewport.
- Recommended placement: Concept section near the top of the guide, before wiring/code detail.
- Alt text: ESP32 environment monitor concept showing BME280 readings processed into OLED pages and green or red LED status.
- TechnicalVerification: YES

## Batch Summary

- Batch 3 assets: 16
- Technically verified: 16
- Blocked: 0
- Output folder: /assets/visuals/guides/concepts

Final status: BATCH 3 SPECS READY
