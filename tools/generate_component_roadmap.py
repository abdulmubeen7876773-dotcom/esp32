from pathlib import Path

import yaml

COMPLETE = {
    "dht22",
    "hc-sr04",
    "pir-sensor",
    "ssd1306-oled",
    "relay-module",
    "esp32-devkit",
}

S = "Sensors"
D = "Displays"
C = "Communication Modules"
A = "Actuators"
B = "Development Boards"
P = "Power Components"
I = "Input Devices"
O = "Output Devices"
M = "Miscellaneous"


def entry(slug, name, cat, diff, volt, proto):
    return {
        "slug": slug,
        "name": name,
        "category": cat,
        "difficulty": diff,
        "voltage": volt,
        "protocol": proto,
        "status": "Complete" if slug in COMPLETE else "Coming Soon",
    }


def main():
    items = []

    sensors = [
        ("dht22", "DHT22 Temp & Humidity", "Beginner", "3.3V/5V", "Digital"),
        ("dht11", "DHT11 Temp & Humidity", "Beginner", "3.3V/5V", "Digital"),
        ("ds18b20", "DS18B20 Temperature", "Beginner", "3.3V/5V", "One-Wire"),
        ("bme280", "BME280 Env Sensor", "Beginner", "3.3V", "I2C"),
        ("bmp280", "BMP280 Pressure", "Beginner", "3.3V", "I2C"),
        ("bme680", "BME680 Air Quality", "Intermediate", "3.3V", "I2C"),
        ("htu21d", "HTU21D Humidity", "Beginner", "3.3V", "I2C"),
        ("sht31", "SHT31 Precision RH/Temp", "Intermediate", "3.3V", "I2C"),
        ("aht20", "AHT20 Temp & Humidity", "Beginner", "3.3V", "I2C"),
        ("am2320", "AM2320 Temp & Humidity", "Beginner", "3.3V", "I2C"),
        ("mq2", "MQ-2 Gas Sensor", "Beginner", "5V", "Analog"),
        ("mq135", "MQ-135 Air Quality", "Beginner", "5V", "Analog"),
        ("mq7", "MQ-7 Carbon Monoxide", "Beginner", "5V", "Analog"),
        ("mq9", "MQ-9 CO & Combustible", "Beginner", "5V", "Analog"),
        ("ccs811", "CCS811 eCO2/TVOC", "Intermediate", "3.3V", "I2C"),
        ("sgp30", "SGP30 TVOC/eCO2", "Intermediate", "3.3V", "I2C"),
        ("hc-sr04", "HC-SR04 Ultrasonic", "Beginner", "5V", "GPIO"),
        ("hcsr501", "HC-SR501 PIR Motion", "Beginner", "5V", "GPIO"),
        ("pir-sensor", "PIR Motion Sensor", "Beginner", "3.3V/5V", "GPIO"),
        ("ldr", "Photoresistor LDR", "Beginner", "3.3V", "Analog"),
        ("soil-moisture", "Capacitive Soil Moisture", "Beginner", "3.3V", "Analog"),
        ("rain-sensor", "Rain Detection Module", "Beginner", "5V", "Digital/Analog"),
        ("water-level", "Water Level Sensor", "Beginner", "5V", "Analog"),
        ("flame-sensor", "Flame Detection Module", "Beginner", "3.3V/5V", "Analog/Digital"),
        ("sound-sensor", "Sound Detection Module", "Beginner", "3.3V/5V", "Analog"),
        ("ky038", "KY-038 Microphone", "Beginner", "3.3V/5V", "Analog"),
        ("vibration-sensor", "Vibration Switch SW-420", "Beginner", "3.3V/5V", "Digital"),
        ("tilt-sensor", "Tilt Ball Switch", "Beginner", "3.3V/5V", "Digital"),
        ("hall-a3144", "A3144 Hall Effect", "Beginner", "3.3V/5V", "Digital"),
        ("reed-switch", "Magnetic Reed Switch", "Beginner", "3.3V/5V", "Digital"),
        ("ir-obstacle", "IR Obstacle Avoidance", "Beginner", "3.3V/5V", "Digital"),
        ("tcrt5000", "TCRT5000 Line Tracker", "Beginner", "3.3V/5V", "Analog/Digital"),
        ("tcs3200", "TCS3200 Color Sensor", "Intermediate", "3.3V/5V", "GPIO"),
        ("tcs34725", "TCS34725 RGB Color", "Intermediate", "3.3V", "I2C"),
        ("apds9960", "APDS-9960 Gesture/Color", "Intermediate", "3.3V", "I2C"),
        ("mpu6050", "MPU6050 IMU", "Intermediate", "3.3V", "I2C"),
        ("mpu9250", "MPU9250 9-Axis IMU", "Advanced", "3.3V", "I2C"),
        ("adxl345", "ADXL345 Accelerometer", "Intermediate", "3.3V", "I2C/SPI"),
        ("hmc5883l", "HMC5883L Magnetometer", "Intermediate", "3.3V", "I2C"),
        ("bh1750", "BH1750 Light Sensor", "Beginner", "3.3V", "I2C"),
        ("uv-guva-s12sd", "GUVA-S12SD UV Sensor", "Intermediate", "3.3V/5V", "Analog"),
        ("ph-sensor", "pH Sensor Module", "Advanced", "5V", "Analog"),
        ("turbidity-sensor", "Turbidity Sensor", "Intermediate", "5V", "Analog"),
        ("hx711-load-cell", "HX711 Load Cell Amp", "Intermediate", "3.3V/5V", "GPIO"),
        ("flex-sensor", "Flex Bend Sensor", "Beginner", "3.3V/5V", "Analog"),
        ("max30102", "MAX30102 Pulse Oximeter", "Advanced", "3.3V", "I2C"),
        ("max30105", "MAX30105 Heart Rate", "Advanced", "3.3V", "I2C"),
        ("gp2y1010", "GP2Y1010 Dust Sensor", "Intermediate", "5V", "Analog"),
        ("pms5003", "PMS5003 PM2.5 Sensor", "Advanced", "5V", "UART"),
        ("scd30", "SCD30 CO2 Sensor", "Advanced", "3.3V/5V", "I2C"),
    ]

    displays = [
        ("ssd1306-oled", "SSD1306 OLED 128x64", "Beginner", "3.3V", "I2C"),
        ("sh1106-oled", "SH1106 OLED 128x64", "Beginner", "3.3V", "I2C"),
        ("st7789-tft", "ST7789 TFT 240x240", "Intermediate", "3.3V", "SPI"),
        ("ili9341-tft", "ILI9341 TFT 320x240", "Intermediate", "3.3V/5V", "SPI"),
        ("ili9488-tft", "ILI9488 TFT 480x320", "Advanced", "3.3V/5V", "SPI"),
        ("st7735-tft", "ST7735 TFT 128x160", "Intermediate", "3.3V", "SPI"),
        ("nokia5110-lcd", "Nokia 5110 LCD", "Beginner", "3.3V", "SPI"),
        ("max7219-matrix", "MAX7219 LED Matrix", "Beginner", "3.3V/5V", "SPI"),
        ("tm1637-7segment", "TM1637 7-Segment", "Beginner", "3.3V/5V", "GPIO"),
        ("ht16k33-matrix", "HT16K33 LED Matrix", "Beginner", "3.3V/5V", "I2C"),
        ("lcd1602-i2c", "LCD 16x2 I2C Backpack", "Beginner", "5V", "I2C"),
        ("lcd2004-i2c", "LCD 20x4 I2C Backpack", "Beginner", "5V", "I2C"),
        ("nextion-hmi", "Nextion HMI Display", "Advanced", "5V", "UART"),
        ("epaper-154", "E-Paper 1.54 inch", "Intermediate", "3.3V", "SPI"),
        ("epaper-290", "E-Paper 2.9 inch", "Intermediate", "3.3V", "SPI"),
        ("gc9a01-round", "GC9A01 Round TFT", "Intermediate", "3.3V", "SPI"),
        ("ws2812-matrix", "WS2812B LED Matrix", "Beginner", "5V", "One-Wire"),
        ("sh1107-oled", "SH1107 OLED 128x128", "Beginner", "3.3V", "I2C"),
        ("rgb-lcd1602", "RGB Backlight LCD 16x2", "Beginner", "5V", "Parallel/I2C"),
        ("tft-18-spi", "1.8 inch SPI TFT Color", "Beginner", "3.3V/5V", "SPI"),
    ]

    comm = [
        ("esp8266-01", "ESP8266-01 Wi-Fi", "Intermediate", "3.3V", "Wi-Fi/UART"),
        ("sim800l", "SIM800L GSM Module", "Advanced", "3.7-4.2V", "UART"),
        ("sim7600", "SIM7600 LTE Module", "Advanced", "3.3V/5V", "UART/USB"),
        ("sx1278-lora", "SX1278 LoRa 433MHz", "Intermediate", "3.3V", "SPI"),
        ("sx1262-lora", "SX1262 LoRa Transceiver", "Advanced", "3.3V", "SPI"),
        ("nrf24l01", "nRF24L01 2.4GHz", "Beginner", "3.3V", "SPI"),
        ("hc05-bluetooth", "HC-05 Bluetooth", "Beginner", "3.3V/5V", "UART"),
        ("hc06-bluetooth", "HC-06 Bluetooth", "Beginner", "3.3V/5V", "UART"),
        ("w5500-ethernet", "W5500 Ethernet", "Intermediate", "3.3V", "SPI"),
        ("lan8720-ethernet", "LAN8720 Ethernet PHY", "Advanced", "3.3V", "RMII"),
        ("max485-rs485", "MAX485 RS485", "Intermediate", "3.3V/5V", "UART"),
        ("mcp2515-can", "MCP2515 CAN Bus", "Advanced", "3.3V/5V", "SPI"),
        ("rf433-tx", "433MHz RF Transmitter", "Beginner", "3.3V/5V", "GPIO"),
        ("rf433-rx", "433MHz RF Receiver", "Beginner", "3.3V/5V", "GPIO"),
        ("ir-transceiver", "IR Transceiver Module", "Beginner", "3.3V/5V", "GPIO"),
        ("cc2530-zigbee", "CC2530 Zigbee", "Advanced", "3.3V", "UART/SPI"),
        ("nrf52840-ble", "nRF52840 BLE Mesh", "Advanced", "3.3V", "BLE/UART"),
        ("neo6m-gps", "NEO-6M GPS", "Intermediate", "3.3V/5V", "UART"),
        ("neom8n-gps", "NEO-M8N GPS", "Advanced", "3.3V", "UART/I2C"),
        ("esp-now-bridge", "ESP-NOW Peer Module", "Intermediate", "3.3V", "Wi-Fi"),
    ]

    actuators = [
        ("relay-module", "1-Channel Relay Module", "Beginner", "5V", "GPIO"),
        ("relay-2ch", "2-Channel Relay Module", "Beginner", "5V", "GPIO"),
        ("relay-4ch", "4-Channel Relay Module", "Beginner", "5V", "GPIO"),
        ("relay-8ch", "8-Channel Relay Module", "Intermediate", "5V/12V", "GPIO"),
        ("mosfet-driver", "MOSFET Switch Module", "Beginner", "3.3V/5V", "GPIO/PWM"),
        ("l298n-motor", "L298N Motor Driver", "Beginner", "5V/12V", "GPIO/PWM"),
        ("tb6612-motor", "TB6612 Motor Driver", "Intermediate", "3.3V/5V", "GPIO/PWM"),
        ("a4988-stepper", "A4988 Stepper Driver", "Intermediate", "3.3V/5V", "GPIO/Step"),
        ("drv8825-stepper", "DRV8825 Stepper Driver", "Intermediate", "3.3V/5V", "GPIO/Step"),
        ("uln2003-stepper", "ULN2003 Stepper Driver", "Beginner", "5V", "GPIO"),
        ("sg90-servo", "SG90 Micro Servo", "Beginner", "5V", "PWM"),
        ("mg996r-servo", "MG996R High-Torque Servo", "Intermediate", "5V/6V", "PWM"),
        ("dc-gear-motor", "DC Gear Motor", "Beginner", "3V-12V", "PWM"),
        ("solenoid-valve", "12V Solenoid Valve", "Intermediate", "12V", "GPIO/Relay"),
        ("water-pump-12v", "12V Mini Water Pump", "Beginner", "5V/12V", "GPIO/Relay"),
        ("passive-buzzer", "Passive Buzzer", "Beginner", "3.3V/5V", "PWM"),
        ("active-buzzer", "Active Buzzer Module", "Beginner", "3.3V/5V", "GPIO"),
        ("vibration-motor", "Coin Vibration Motor", "Beginner", "3V-5V", "GPIO/PWM"),
        ("linear-actuator", "Linear Actuator Driver", "Advanced", "12V", "GPIO/Relay"),
        ("pneumatic-relay", "Pneumatic Valve Relay", "Advanced", "12V/24V", "GPIO"),
    ]

    boards = [
        ("esp32-devkit", "ESP32 DevKit WROOM", "Beginner", "3.3V/5V USB", "Wi-Fi/BLE/UART"),
        ("esp32-s3-devkit", "ESP32-S3 DevKit", "Intermediate", "3.3V USB", "Wi-Fi/BLE/USB"),
        ("esp32-c3-mini", "ESP32-C3 Mini", "Beginner", "3.3V USB", "Wi-Fi/BLE"),
        ("esp32-c6-devkit", "ESP32-C6 DevKit", "Intermediate", "3.3V USB", "Wi-Fi 6/BLE/Zigbee"),
        ("esp32-h2-devkit", "ESP32-H2 DevKit", "Advanced", "3.3V USB", "BLE/Zigbee/802.15.4"),
        ("nodemcu-esp8266", "NodeMCU ESP8266", "Beginner", "3.3V USB", "Wi-Fi"),
        ("esp32-cam", "ESP32-CAM Module", "Intermediate", "5V", "Wi-Fi/Camera"),
        ("esp32-s2-saola", "ESP32-S2 Saola", "Intermediate", "3.3V USB", "Wi-Fi/USB-OTG"),
        ("lilygo-t-display", "LilyGO T-Display", "Intermediate", "3.3V USB", "Wi-Fi/SPI"),
        ("lilygo-t-beam", "LilyGO T-Beam LoRa", "Advanced", "3.3V USB", "Wi-Fi/GPS/LoRa"),
        ("m5stack-core", "M5Stack Core ESP32", "Intermediate", "5V USB", "Wi-Fi/I2C"),
        ("m5stickc-plus", "M5StickC Plus", "Intermediate", "5V USB", "Wi-Fi/I2C"),
        ("wemos-d1-mini", "Wemos D1 Mini", "Beginner", "3.3V USB", "Wi-Fi"),
        ("firebeetle-esp32", "FireBeetle ESP32", "Beginner", "3.3V USB", "Wi-Fi/BLE"),
        ("feather-esp32", "Adafruit Feather ESP32", "Intermediate", "3.3V USB/LiPo", "Wi-Fi/BLE"),
        ("esp32-wrover-kit", "ESP32-WROVER Kit", "Advanced", "3.3V USB", "Wi-Fi/BLE/PSRAM"),
        ("esp32-poe", "ESP32-POE Ethernet Board", "Advanced", "PoE/5V", "Ethernet/Wi-Fi"),
        ("nano-esp32", "Arduino Nano ESP32", "Beginner", "3.3V USB", "Wi-Fi/BLE"),
        ("xiao-esp32c3", "Seeed XIAO ESP32-C3", "Beginner", "3.3V USB", "Wi-Fi/BLE"),
        ("esp32-s3-box", "ESP32-S3-Box AI Dev Kit", "Advanced", "5V USB", "Wi-Fi/I2S/Mic"),
    ]

    power = [
        ("ams1117-33", "AMS1117 3.3V LDO", "Beginner", "5V in / 3.3V out", "Power"),
        ("lm2596-buck", "LM2596 Buck Converter", "Beginner", "4-40V", "Power"),
        ("tp4056-charger", "TP4056 Li-ion Charger", "Beginner", "5V USB", "Power"),
        ("18650-holder", "18650 Battery Holder", "Beginner", "3.7V", "Power"),
        ("lipo-1s-3v7", "1S LiPo 3.7V Pack", "Beginner", "3.7V", "Power"),
        ("usb-power-bank", "USB Power Bank Module", "Beginner", "5V USB", "Power"),
        ("mt3608-boost", "MT3608 Boost Converter", "Intermediate", "2-24V", "Power"),
        ("xl4015-buck", "XL4015 Buck 5A", "Intermediate", "4-38V", "Power"),
        ("solar-panel-6v", "6V Solar Panel", "Beginner", "6V", "Power"),
        ("cn3065-solar", "CN3065 Solar Charger", "Intermediate", "Solar/5V", "Power"),
        ("power-path-module", "Power Path Manager", "Advanced", "3.3V/5V", "Power"),
        ("ups-hat-switch", "UPS HAT Auto Switch", "Advanced", "5V/12V", "Power"),
        ("max17048-fuel", "MAX17048 Fuel Gauge", "Intermediate", "3.3V", "I2C"),
        ("ina219-current", "INA219 Current Monitor", "Intermediate", "3.3V", "I2C"),
        ("ina226-current", "INA226 Precision Current", "Advanced", "3.3V", "I2C"),
        ("dc-barrel-jack", "DC Barrel Jack Adapter", "Beginner", "5V-12V", "Power"),
        ("breadboard-psu", "Breadboard Power Supply", "Beginner", "3.3V/5V", "Power"),
        ("usb-c-pd-trigger", "USB-C PD Trigger", "Advanced", "5V-20V", "Power"),
        ("pololu-switch", "Pololu Pushbutton Power Switch", "Intermediate", "3.3V/5V", "Power"),
        ("lp5907-ldo", "LP5907 Low-Noise LDO", "Advanced", "3.3V", "Power"),
    ]

    inputs = [
        ("ttp223-touch", "TTP223 Touch Sensor", "Beginner", "3.3V/5V", "Digital"),
        ("rotary-encoder", "Rotary Encoder KY-040", "Beginner", "3.3V/5V", "GPIO"),
        ("joystick-module", "Dual-Axis Joystick", "Beginner", "3.3V/5V", "Analog"),
        ("keypad-4x4", "4x4 Matrix Keypad", "Beginner", "3.3V/5V", "GPIO"),
        ("membrane-keypad", "Membrane Keypad 4x3", "Beginner", "3.3V/5V", "GPIO"),
        ("limit-switch", "Mechanical Limit Switch", "Beginner", "3.3V/5V", "Digital"),
        ("micro-switch", "Micro Switch SS-5GL", "Beginner", "3.3V/5V", "Digital"),
        ("tactile-button", "Tactile Push Button", "Beginner", "3.3V/5V", "Digital"),
        ("cap-touch-pad", "Capacitive Touch Pad", "Beginner", "3.3V/5V", "Digital"),
        ("slide-pot", "Slide Potentiometer 10K", "Beginner", "3.3V/5V", "Analog"),
        ("rotary-pot-10k", "Rotary Potentiometer 10K", "Beginner", "3.3V/5V", "Analog"),
        ("fsr-force", "Force Sensitive Resistor", "Beginner", "3.3V/5V", "Analog"),
        ("rc522-rfid", "RC522 RFID Reader", "Intermediate", "3.3V", "SPI"),
        ("pn532-nfc", "PN532 NFC Module", "Intermediate", "3.3V", "I2C/SPI/UART"),
        ("r307-fingerprint", "R307 Fingerprint Sensor", "Advanced", "3.3V/5V", "UART"),
        ("barcode-ttl", "TTL Barcode Scanner", "Advanced", "5V", "UART"),
        ("vs1838b-ir-remote", "VS1838B IR Receiver", "Beginner", "3.3V/5V", "IR"),
        ("ps2-keyboard", "PS/2 Keyboard Adapter", "Intermediate", "3.3V/5V", "PS/2"),
        ("rotary-phone-dial", "Pulse Dial Input", "Advanced", "3.3V/5V", "GPIO"),
        ("cap-slider", "Capacitive Touch Slider", "Intermediate", "3.3V", "I2C"),
    ]

    outputs = [
        ("led-5mm", "5mm LED", "Beginner", "3.3V", "GPIO"),
        ("rgb-led-cc", "RGB LED Common Cathode", "Beginner", "3.3V/5V", "GPIO/PWM"),
        ("ws2812b-strip", "WS2812B Addressable LED Strip", "Beginner", "5V", "One-Wire"),
        ("laser-module", "650nm Laser Diode Module", "Intermediate", "3.3V/5V", "GPIO"),
        ("status-tower-light", "3-Color Status Tower LED", "Intermediate", "12V/24V", "GPIO/Relay"),
        ("cooling-fan-5v", "5V DC Cooling Fan", "Beginner", "5V", "GPIO/PWM"),
        ("led-strip-driver", "12V LED Strip MOSFET Driver", "Intermediate", "12V", "PWM"),
        ("mcp4725-dac", "MCP4725 DAC Module", "Intermediate", "3.3V/5V", "I2C"),
        ("pwm-dimmer", "PWM LED Dimmer Module", "Beginner", "3.3V/5V", "PWM"),
        ("ir-led-transmitter", "IR LED Transmitter", "Beginner", "3.3V/5V", "GPIO/PWM"),
        ("electromagnetic-lock", "Electromagnetic Lock Driver", "Advanced", "12V", "GPIO/Relay"),
        ("ssr-heater", "Solid State Relay Heater", "Advanced", "120V AC", "GPIO"),
        ("pam8403-amp", "PAM8403 Audio Amplifier", "Intermediate", "3.3V/5V", "Analog/PWM"),
        ("step-relay-bank", "Step Relay Output Bank", "Advanced", "12V", "GPIO"),
        ("neopixel-ring-16", "NeoPixel 16-LED Ring", "Beginner", "5V", "One-Wire"),
        ("dotstar-strip", "APA102 DotStar Strip", "Intermediate", "5V", "SPI"),
        ("oled-status-module", "OLED Status Indicator", "Beginner", "3.3V", "I2C"),
        ("solenoid-push", "Push Solenoid 12V", "Intermediate", "12V", "GPIO/Relay"),
        ("piezo-disc-output", "Piezo Disc Output", "Beginner", "3.3V/5V", "PWM"),
        ("relay-latching", "Latching Relay Output", "Advanced", "5V/12V", "GPIO"),
    ]

    misc = [
        ("breadboard-half", "Half-Size Breadboard", "Beginner", "N/A", "Mechanical"),
        ("jumper-wire-m-m", "Male-Male Jumper Wires", "Beginner", "N/A", "Mechanical"),
        ("jumper-wire-m-f", "Male-Female Jumper Wires", "Beginner", "N/A", "Mechanical"),
        ("resistor-kit", "Resistor Assortment Kit", "Beginner", "N/A", "Passive"),
        ("capacitor-kit", "Capacitor Assortment Kit", "Beginner", "N/A", "Passive"),
        ("diode-kit", "Diode Assortment Kit", "Beginner", "N/A", "Passive"),
        ("transistor-kit", "Transistor Assortment Kit", "Intermediate", "N/A", "Passive"),
        ("logic-level-shifter", "4-Channel Logic Level Shifter", "Beginner", "3.3V/5V", "GPIO"),
        ("i2c-multiplexer", "TCA9548A I2C Multiplexer", "Advanced", "3.3V", "I2C"),
        ("shift-register-595", "74HC595 Shift Register", "Intermediate", "3.3V/5V", "SPI/GPIO"),
        ("opamp-module", "LM358 Op-Amp Module", "Intermediate", "3.3V/5V", "Analog"),
        ("voltage-divider", "Precision Voltage Divider", "Beginner", "3.3V/5V", "Analog"),
        ("prototype-pcb", "Prototype PCB Board", "Beginner", "N/A", "Mechanical"),
        ("heat-shrink-kit", "Heat Shrink Tubing Kit", "Beginner", "N/A", "Mechanical"),
        ("esp32-proto-shield", "ESP32 Prototype Shield", "Beginner", "3.3V", "GPIO"),
        ("sd-card-module", "MicroSD Card Module", "Beginner", "3.3V/5V", "SPI"),
        ("rtc-ds3231", "DS3231 Real-Time Clock", "Beginner", "3.3V/5V", "I2C"),
        ("watchdog-timer", "External Watchdog Timer", "Advanced", "3.3V", "GPIO"),
        ("esd-safe-mat", "ESD Safe Work Mat", "Beginner", "N/A", "Mechanical"),
        ("tool-kit-minimal", "Minimal Electronics Tool Kit", "Beginner", "N/A", "Mechanical"),
    ]

    groups = [
        (S, sensors),
        (D, displays),
        (C, comm),
        (A, actuators),
        (B, boards),
        (P, power),
        (I, inputs),
        (O, outputs),
        (M, misc),
    ]
    for cat, group in groups:
        for row in group:
            items.append(entry(row[0], row[1], cat, row[2], row[3], row[4]))

    counts = {}
    for item in items:
        counts[item["category"]] = counts.get(item["category"], 0) + 1

    roadmap = {
        "version": 1,
        "title": "ESP32 Component Encyclopedia Roadmap",
        "target_total": 210,
        "actual_total": len(items),
        "complete_count": sum(1 for i in items if i["status"] == "Complete"),
        "coming_soon_count": sum(1 for i in items if i["status"] == "Coming Soon"),
        "category_targets": {
            "Sensors": 50,
            "Displays": 20,
            "Communication Modules": 20,
            "Actuators": 20,
            "Development Boards": 20,
            "Power Components": 20,
            "Input Devices": 20,
            "Output Devices": 20,
            "Miscellaneous": 20,
        },
        "category_counts": counts,
        "components": items,
    }

    out = Path(__file__).resolve().parent.parent / "content" / "component-roadmap.yaml"
    with out.open("w", encoding="utf-8") as f:
        yaml.dump(roadmap, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100)
    print(f"Wrote {out} ({len(items)} components)")


if __name__ == "__main__":
    main()
