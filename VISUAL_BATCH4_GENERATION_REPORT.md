# Visual Batch 4 Generation Report

## Summary

- Assets generated: 7/7
- Format: standalone SVG
- Canvas: 1600x900
- Target folder: assets/visuals/components/wiring
- Source of truth: component YAML wiring, pinout, code, and planning files
- Technical verification: 7/7 YES

## Assets

- V022: dht22-wiring.svg for /components/dht22.html - DATA -> GPIO4; ESP32 3.3V -> DHT22 VCC; ESP32 GND -> DHT22 GND
- V023: esp32-cam-wiring.svg for /components/esp32-cam.html - FTDI TX -> U0R/RX0; FTDI RX -> U0T/TX0; IO0 -> GND only while uploading; Stable 5V -> ESP32-CAM 5V; adapter/supply GND -> ESP32-CAM GND
- V024: esp32-devkit-wiring.svg for /components/esp32-devkit.html - GPIO16 -> 220 ohm resistor -> LED anode; LED cathode -> GND; GPIO21 SDA and GPIO22 SCL marked as common I2C defaults; USB powers board; 3V3, 5V/VIN, and GND rails labeled
- V025: hc-sr04-wiring.svg for /components/hc-sr04.html - TRIG -> GPIO5; divided ECHO -> GPIO18; ESP32 5V/VIN -> HC-SR04 VCC; ESP32 GND -> HC-SR04 GND and divider ground
- V026: pir-sensor-wiring.svg for /components/pir-sensor.html - OUT -> GPIO27; ESP32 5V/VIN typical -> PIR VCC; ESP32 GND -> PIR GND
- V027: relay-module-wiring.svg for /components/relay-module.html - IN -> GPIO26; 5V supply -> relay VCC; relay GND -> ESP32 GND; low-voltage load supply positive -> COM -> NO -> load positive; load negative -> supply negative
- V028: ssd1306-oled-wiring.svg for /components/ssd1306-oled.html - SDA -> GPIO21; SCL -> GPIO22; ESP32 3.3V -> OLED VCC; ESP32 GND -> OLED GND

## QA Checklist

- GPIO labels are explicit and visible.
- Voltage labels are explicit and visible.
- Resistor values are shown where supported by source content.
- No Arduino Uno D-pin naming is used.
- No duplicate components are shown.
- No unapproved Batch 1, Batch 2, or Batch 3 assets were modified.

Final status: BATCH 4 GENERATED
