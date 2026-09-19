# Visual Batch 4 Production Specs

Batch 4 resolves the seven remaining component wiring-diagram warnings only. Source truth was checked against the component YAML/source content before creating assets.

### V022 - DHT22 Sensor with ESP32

- Page URL: /components/dht22.html
- Source file: content/components/dht22.yaml
- Target filename: dht22-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Digital sensor wiring diagram
- Exact hardware shown: ESP32 DevKit, DHT22 sensor, optional 10 k ohm pull-up resistor
- Exact GPIO mapping: DATA -> GPIO4
- Exact power mapping: ESP32 3.3V -> DHT22 VCC; ESP32 GND -> DHT22 GND
- Exact resistor values: Optional 10 k ohm pull-up from DATA to 3.3V for bare sensor
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Use 3.3V for ESP32-friendly logic; leave NC disconnected.
- Safety note: Use 3.3V for ESP32-friendly logic; leave NC disconnected.
- What must NOT appear: 5V data drive, Arduino Uno pins, fake temperature readings, duplicate sensors
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: DHT22 VCC to ESP32 3.3 V, GND to ESP32 GND, DATA to ESP32 GPIO4, optional 10 k ohm pull-up from DATA to 3.3 V.
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V023 - ESP32-CAM (AI-Thinker)

- Page URL: /components/esp32-cam.html
- Source file: content/components/esp32-cam.yaml
- Target filename: esp32-cam-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Programming wiring diagram
- Exact hardware shown: AI-Thinker ESP32-CAM and FTDI/CP2102 USB-to-serial adapter
- Exact GPIO mapping: FTDI TX -> U0R/RX0; FTDI RX -> U0T/TX0; IO0 -> GND only while uploading
- Exact power mapping: Stable 5V -> ESP32-CAM 5V; adapter/supply GND -> ESP32-CAM GND
- Exact resistor values: None
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Use stable 5V with current headroom. Disconnect IO0 from GND after flashing.
- Safety note: Use stable 5V with current headroom. Disconnect IO0 from GND after flashing.
- What must NOT appear: ESP32 DevKit board, fake web dashboard, privacy-invasive scene, 3.3V camera power recommendation
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: ESP32-CAM connected to an FTDI programmer: 5V to 5V, GND to GND, FTDI TX to U0R, FTDI RX to U0T, and IO0 to GND only for programming mode; IO0 is disconnected for normal run mode.
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V024 - ESP32 DevKit Pinout and Board Guide

- Page URL: /components/esp32-devkit.html
- Source file: content/components/esp32-devkit.yaml
- Target filename: esp32-devkit-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Beginner board wiring diagram
- Exact hardware shown: ESP32 DevKit on breadboard, USB cable, external LED, 220 ohm resistor, I2C pin callouts
- Exact GPIO mapping: GPIO16 -> 220 ohm resistor -> LED anode; LED cathode -> GND; GPIO21 SDA and GPIO22 SCL marked as common I2C defaults
- Exact power mapping: USB powers board; 3V3, 5V/VIN, and GND rails labeled
- Exact resistor values: 220 ohm current-limiting resistor from GPIO16 to LED long leg
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: GPIO is 3.3V logic; do not feed 5V into signal pins.
- Safety note: GPIO is 3.3V logic; do not feed 5V into signal pins.
- What must NOT appear: Onboard LED assumption, Arduino Uno D-pin labels, motors/relay loads powered from GPIO
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: ESP32 DevKit on breadboard with USB power, GND shared, GPIO16 through resistor to an external LED, and GPIO21/GPIO22 marked as common I2C defaults
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V025 - HC-SR04 Ultrasonic Distance Sensor

- Page URL: /components/hc-sr04.html
- Source file: content/components/hc-sr04.yaml
- Target filename: hc-sr04-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Sensor wiring diagram with voltage divider
- Exact hardware shown: ESP32 DevKit, HC-SR04 ultrasonic sensor, 10 k ohm / 20 k ohm ECHO divider
- Exact GPIO mapping: TRIG -> GPIO5; divided ECHO -> GPIO18
- Exact power mapping: ESP32 5V/VIN -> HC-SR04 VCC; ESP32 GND -> HC-SR04 GND and divider ground
- Exact resistor values: 10 k ohm from ECHO to divider node; 20 k ohm from node to GND
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Do not connect 5V ECHO directly to ESP32; level shift to 3.3V.
- Safety note: Do not connect 5V ECHO directly to ESP32; level shift to 3.3V.
- What must NOT appear: Direct ECHO-to-GPIO wire bypassing divider, 3.3V module power as default, fake distance readout
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: HC-SR04 VCC to 5 V, GND to GND, TRIG to GPIO5, ECHO through voltage divider to GPIO18
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V026 - HC-SR501 PIR Motion Sensor

- Page URL: /components/pir-sensor.html
- Source file: content/components/pir-sensor.yaml
- Target filename: pir-sensor-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Digital motion sensor wiring diagram
- Exact hardware shown: ESP32 DevKit and HC-SR501 PIR motion sensor module with lens, delay and sensitivity controls
- Exact GPIO mapping: OUT -> GPIO27
- Exact power mapping: ESP32 5V/VIN typical -> PIR VCC; ESP32 GND -> PIR GND
- Exact resistor values: None
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Wait 30-60 seconds after power-up before judging motion output.
- Safety note: Wait 30-60 seconds after power-up before judging motion output.
- What must NOT appear: Camera imagery, distance measurement, analog readings, extra sensors
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: HC-SR501 PIR VCC to 5 V, GND to ESP32 GND, OUT to ESP32 GPIO27
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V027 - 1-Channel Relay Module

- Page URL: /components/relay-module.html
- Source file: content/components/relay-module.yaml
- Target filename: relay-module-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: Relay control and low-voltage load wiring diagram
- Exact hardware shown: ESP32 DevKit, 1-channel relay module, low-voltage DC supply, low-voltage load
- Exact GPIO mapping: IN -> GPIO26
- Exact power mapping: 5V supply -> relay VCC; relay GND -> ESP32 GND; low-voltage load supply positive -> COM -> NO -> load positive; load negative -> supply negative
- Exact resistor values: None
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Beginner diagram shows low-voltage DC load only. Do not put hazardous voltage on a breadboard.
- Safety note: Beginner diagram shows low-voltage DC load only. Do not put hazardous voltage on a breadboard.
- What must NOT appear: House wiring, outlet wiring, bare relay coil on GPIO, PWM dimming
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: Relay module VCC to 5 V, GND to ESP32 GND, IN to GPIO26, load wired through COM and NO on low-voltage supply
- Generation-ready status: TECHNICALLY VERIFIED: YES

### V028 - SSD1306 OLED Display with ESP32

- Page URL: /components/ssd1306-oled.html
- Source file: content/components/ssd1306-oled.yaml
- Target filename: ssd1306-oled-wiring.svg
- Target folder: assets/visuals/components/wiring
- Asset type: I2C display wiring diagram
- Exact hardware shown: ESP32 DevKit and SSD1306 I2C OLED display
- Exact GPIO mapping: SDA -> GPIO21; SCL -> GPIO22
- Exact power mapping: ESP32 3.3V -> OLED VCC; ESP32 GND -> OLED GND
- Exact resistor values: None external; typical breakout includes pull-ups
- Exact wire colors: red=VCC, black=GND, orange=digital/control, blue=secondary/switched/echo, green=I2C SDA, purple=I2C SCL, yellow=UART TX where used
- Required labels: visible ESP32 GPIO labels, module pins, voltage labels, and safety/timing notes where relevant
- Required annotations: Use module labels and scan for 0x3C/0x3D address if display is blank.
- Safety note: Use module labels and scan for 0x3C/0x3D address if display is blank.
- What must NOT appear: SPI wiring, fake weather dashboard, Arduino Uno pin labels, extra sensors
- Aspect ratio: 16:9, 1600x900 SVG
- Recommended placement: component wiring section via wiring.image
- Alt text: SSD1306 OLED VCC to 3.3 V, GND to GND, SDA to GPIO21, SCL to GPIO22 on ESP32
- Generation-ready status: TECHNICALLY VERIFIED: YES

## Batch Summary

- Number of Batch 4 assets: 7
- Technically verified: 7
- Blocked: 0
- Exact filenames: dht22-wiring.svg, esp32-cam-wiring.svg, esp32-devkit-wiring.svg, hc-sr04-wiring.svg, pir-sensor-wiring.svg, relay-module-wiring.svg, ssd1306-oled-wiring.svg
- Pages covered: /components/dht22.html, /components/esp32-cam.html, /components/esp32-devkit.html, /components/hc-sr04.html, /components/pir-sensor.html, /components/relay-module.html, /components/ssd1306-oled.html
- Final status: BATCH 4 READY FOR GENERATION
