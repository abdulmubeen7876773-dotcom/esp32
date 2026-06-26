from pathlib import Path

import yaml

COMPLETE = {
    "what-is-esp32",
    "installing-arduino-ide-esp32",
    "blink-led-esp32",
    "read-temperature-dht22",
    "connect-oled-esp32",
}

LEVELS = [
    "First Spark",
    "Sensors",
    "Displays",
    "Motors",
    "Communication",
    "IoT Projects",
    "AI Projects",
    "Advanced ESP32",
]

LEVEL_TARGETS = {
    "First Spark": 12,
    "Sensors": 13,
    "Displays": 12,
    "Motors": 13,
    "Communication": 13,
    "IoT Projects": 13,
    "AI Projects": 12,
    "Advanced ESP32": 12,
}


def mission(slug, title, mission_name, level, category, difficulty, estimated_time):
    return {
        "slug": slug,
        "title": title,
        "mission_name": mission_name,
        "level": level,
        "category": category,
        "difficulty": difficulty,
        "estimated_time": estimated_time,
    }


def build_missions():
    items = []

    first_spark = [
        mission("what-is-esp32", "What Is ESP32?", "Meet Your ESP32 Brain", "First Spark", "ESP32 Basics", "Beginner", "10-15 min"),
        mission("installing-arduino-ide-esp32", "Install Arduino IDE for ESP32", "Set Up Your Maker Workshop", "First Spark", "Development Setup", "Beginner", "15-20 min"),
        mission("blink-led-esp32", "Blink an LED with ESP32", "Make Your First Light Blink", "First Spark", "GPIO Output", "Beginner", "10-15 min"),
        mission("blink-two-leds", "Blink Two LEDs in Pattern", "Double Blink Challenge", "First Spark", "GPIO Output", "Beginner", "10-15 min"),
        mission("button-led-control", "Button Controls an LED", "Press to Light Up", "First Spark", "Digital Input", "Beginner", "10-15 min"),
        mission("serial-monitor-hello", "Hello Serial Monitor", "Talk to Your Computer", "First Spark", "Serial Debug", "Beginner", "10 min"),
        mission("serial-read-number", "Read Numbers on Serial", "Send Data Back", "First Spark", "Serial Debug", "Beginner", "10 min"),
        mission("onboard-led-blink", "Use the Onboard LED", "Blink Without Breadboard", "First Spark", "GPIO Output", "Beginner", "10 min"),
        mission("pwm-dim-led", "Dim an LED with PWM", "Fade Lights Smoothly", "First Spark", "PWM Output", "Beginner", "12 min"),
        mission("rgb-led-colors", "Mix Colors on RGB LED", "Paint with Light", "First Spark", "PWM Output", "Beginner", "12 min"),
        mission("buzzer-first-beep", "Play Your First Beep", "Make Some Noise", "First Spark", "Sound Output", "Beginner", "10 min"),
        mission("breadboard-clean-build", "Build a Clean Breadboard Circuit", "Tidy Wires, Strong Builds", "First Spark", "Fundamentals", "Beginner", "10 min"),
    ]

    sensors = [
        mission("read-temperature-dht22", "Read Temperature with DHT22", "Teach Your ESP32 to Feel the Weather", "Sensors", "Temperature", "Beginner", "10-15 min"),
        mission("read-humidity-dht11", "Read Humidity with DHT11", "Measure Sticky Air", "Sensors", "Temperature", "Beginner", "10-15 min"),
        mission("ds18b20-precision-temp", "Precise Temp with DS18B20", "One-Wire Temperature Pro", "Sensors", "Temperature", "Beginner", "12 min"),
        mission("bme280-weather-read", "Read Weather with BME280", "Tiny Weather Chip", "Sensors", "Environment", "Intermediate", "15 min"),
        mission("ldr-light-meter", "Measure Light with LDR", "How Bright Is It?", "Sensors", "Light", "Beginner", "10 min"),
        mission("bh1750-lux-meter", "Lux Meter with BH1750", "Professional Light Reading", "Sensors", "Light", "Intermediate", "12 min"),
        mission("pir-motion-alert", "PIR Motion Alert", "Who Moved?", "Sensors", "Motion", "Beginner", "10-15 min"),
        mission("ultrasonic-distance-ruler", "Ultrasonic Distance Ruler", "Measure Without Touching", "Sensors", "Distance", "Beginner", "12 min"),
        mission("soil-moisture-plant-care", "Soil Moisture for Plants", "Save the Basil", "Sensors", "Environment", "Beginner", "12 min"),
        mission("rain-sensor-warning", "Rain Sensor Warning", "Storm Is Coming", "Sensors", "Environment", "Beginner", "10 min"),
        mission("flame-sensor-alarm", "Flame Sensor Safety Alarm", "Fire Watch Mission", "Sensors", "Safety", "Beginner", "10 min"),
        mission("sound-level-meter", "Simple Sound Level Meter", "How Loud Is the Room?", "Sensors", "Sound", "Beginner", "12 min"),
        mission("mpu6050-tilt-detector", "Tilt Detector with MPU6050", "Don't Tip Over", "Sensors", "Motion", "Intermediate", "15 min"),
    ]

    displays = [
        mission("connect-oled-esp32", "Connect OLED Display with ESP32", "Give Your Project a Face", "Displays", "OLED", "Beginner", "10-15 min"),
        mission("oled-scrolling-text", "Scrolling Text on OLED", "Marquee Messages", "Displays", "OLED", "Beginner", "12 min"),
        mission("oled-sensor-dashboard", "OLED Sensor Dashboard", "Numbers on Screen", "Displays", "OLED", "Beginner", "15 min"),
        mission("lcd1602-hello-world", "Hello World on LCD 16x2", "Classic Text Display", "Displays", "Character LCD", "Beginner", "12 min"),
        mission("tm1637-counter-display", "TM1637 Counter Display", "Big Bright Digits", "Displays", "7-Segment", "Beginner", "10 min"),
        mission("max7219-matrix-scroll", "LED Matrix Scrolling Text", "Mini Times Square", "Displays", "LED Matrix", "Intermediate", "15 min"),
        mission("st7735-color-shapes", "Draw Shapes on ST7735 TFT", "Color Graphics Time", "Displays", "TFT Color", "Intermediate", "15 min"),
        mission("tft-gauge-meter", "Build a TFT Gauge Meter", "Needle on Screen", "Displays", "TFT Color", "Intermediate", "18 min"),
        mission("epaper-quote-frame", "E-Paper Quote Frame", "Low Power Message Board", "Displays", "E-Paper", "Intermediate", "18 min"),
        mission("nokia5110-mini-menu", "Nokia 5110 Mini Menu", "Retro Pixel Menu", "Displays", "Monochrome LCD", "Intermediate", "15 min"),
        mission("oled-icon-status", "OLED Icon Status Bar", "Wi-Fi Battery Signal Icons", "Displays", "OLED", "Intermediate", "12 min"),
        mission("display-multi-screen", "Switch Between Display Screens", "Tap Through Pages", "Displays", "UI Patterns", "Intermediate", "15 min"),
    ]

    motors = [
        mission("sg90-servo-sweep", "Sweep a SG90 Servo", "Robot Arm Wave", "Motors", "Servo", "Beginner", "12 min"),
        mission("servo-knob-control", "Control Servo with Knob", "Turn the Dial", "Motors", "Servo", "Beginner", "12 min"),
        mission("dc-motor-speed-pwm", "DC Motor Speed with PWM", "Faster Slower Stop", "Motors", "DC Motor", "Beginner", "15 min"),
        mission("l298n-forward-reverse", "Forward and Reverse Motor", "Spin Both Ways", "Motors", "Motor Driver", "Intermediate", "15 min"),
        mission("tb6612-smooth-drive", "Smooth Drive with TB6612", "Better Motor Control", "Motors", "Motor Driver", "Intermediate", "18 min"),
        mission("stepper-single-rev", "Turn a Stepper One Revolution", "Click Click Spin", "Motors", "Stepper", "Intermediate", "18 min"),
        mission("stepper-position-home", "Home a Stepper Motor", "Find Zero Position", "Motors", "Stepper", "Intermediate", "20 min"),
        mission("relay-lamp-switch", "Switch a Lamp with Relay", "Big Power Small Signal", "Motors", "Relay", "Beginner", "12 min"),
        mission("pump-auto-fill", "Auto Fill with Water Pump", "Plant Watering Actuator", "Motors", "Pump", "Intermediate", "18 min"),
        mission("fan-temp-control", "Temperature Fan Control", "Cool Down Automatically", "Motors", "Fan", "Intermediate", "15 min"),
        mission("servo-pick-place", "Servo Pick and Place", "Mini Robot Grip", "Motors", "Servo", "Advanced", "20 min"),
        mission("motor-button-states", "Motor States with Buttons", "Forward Stop Reverse", "Motors", "DC Motor", "Beginner", "12 min"),
        mission("h-bridge-brake-mode", "H-Bridge Brake Mode", "Stop Fast Safely", "Motors", "Motor Driver", "Advanced", "18 min"),
    ]

    communication = [
        mission("wifi-connect-home", "Connect ESP32 to Wi-Fi", "Join the Internet", "Communication", "Wi-Fi", "Beginner", "12 min"),
        mission("wifi-webserver-page", "Build a Wi-Fi Web Page", "Control from Browser", "Communication", "Wi-Fi", "Intermediate", "18 min"),
        mission("wifi-client-fetch", "Fetch Data from the Web", "Ask the Internet a Question", "Communication", "Wi-Fi", "Intermediate", "15 min"),
        mission("mqtt-publish-sensor", "Publish Sensor Data with MQTT", "Send to the Cloud", "Communication", "MQTT", "Intermediate", "18 min"),
        mission("mqtt-subscribe-control", "Subscribe and Control with MQTT", "Remote On Off Switch", "Communication", "MQTT", "Intermediate", "18 min"),
        mission("ble-notify-sensor", "BLE Notify Sensor Values", "Phone Sees Live Data", "Communication", "Bluetooth", "Intermediate", "20 min"),
        mission("nrf24l01-wireless-ping", "nRF24L01 Wireless Ping", "Two Boards Talking", "Communication", "RF", "Intermediate", "18 min"),
        mission("lora-send-message", "Send a LoRa Message", "Long Range Whisper", "Communication", "LoRa", "Advanced", "20 min"),
        mission("gps-read-location", "Read GPS Location", "Where Am I?", "Communication", "GPS", "Intermediate", "18 min"),
        mission("esp-now-peer-chat", "ESP-NOW Peer Chat", "Fast Board to Board", "Communication", "ESP-NOW", "Intermediate", "15 min"),
        mission("websocket-live-chart", "WebSocket Live Chart", "Graphs That Move", "Communication", "WebSocket", "Advanced", "22 min"),
        mission("telegram-bot-alert", "Telegram Bot Alert", "Phone Notification Mission", "Communication", "Cloud API", "Advanced", "20 min"),
        mission("ntp-sync-clock", "Sync Clock with NTP", "Always Correct Time", "Communication", "Time Sync", "Intermediate", "12 min"),
    ]

    iot = [
        mission("iot-weather-station", "Mini IoT Weather Station", "Backyard Weather Hub", "IoT Projects", "Weather", "Intermediate", "25 min"),
        mission("iot-smart-plug", "Smart Plug with Relay", "Phone Controls Power", "IoT Projects", "Smart Home", "Intermediate", "22 min"),
        mission("iot-plant-monitor", "Connected Plant Monitor", "Thirsty Plant Alert", "IoT Projects", "Garden", "Intermediate", "22 min"),
        mission("iot-door-alert", "Door Open Email Alert", "Did Someone Open It?", "IoT Projects", "Security", "Intermediate", "20 min"),
        mission("iot-rgb-mood-lamp", "Wi-Fi RGB Mood Lamp", "Color from Your Phone", "IoT Projects", "Lighting", "Intermediate", "20 min"),
        mission("iot-energy-logger", "Home Energy Logger", "Track Power Usage", "IoT Projects", "Energy", "Advanced", "25 min"),
        mission("iot-garage-status", "Garage Door Status Page", "Open or Closed?", "IoT Projects", "Smart Home", "Intermediate", "20 min"),
        mission("iot-aquarium-monitor", "Aquarium Monitor Dashboard", "Happy Fish Check", "IoT Projects", "Environment", "Intermediate", "22 min"),
        mission("iot-thermostat-starter", "Starter Smart Thermostat", "Room Comfort Control", "IoT Projects", "Climate", "Advanced", "25 min"),
        mission("iot-motion-light", "Motion Activated IoT Light", "Light When You Enter", "IoT Projects", "Automation", "Intermediate", "20 min"),
        mission("iot-auto-irrigation", "Auto Irrigation Scheduler", "Water on a Timetable", "IoT Projects", "Garden", "Advanced", "25 min"),
        mission("iot-air-quality-hub", "Air Quality Cloud Hub", "City Room Air Tracker", "IoT Projects", "Health", "Advanced", "25 min"),
        mission("iot-security-trigger", "Security Camera Trigger", "Motion Starts Recording", "IoT Projects", "Security", "Advanced", "25 min"),
    ]

    ai = [
        mission("ai-sound-classifier", "On-Device Sound Classifier", "Clap Snap Knock Detect", "AI Projects", "Audio ML", "Advanced", "25 min"),
        mission("ai-keyword-spotting", "Keyword Spotting Mission", "Wake Word Detector", "AI Projects", "Audio ML", "Advanced", "25 min"),
        mission("ai-gesture-sensor", "Gesture Control with APDS9960", "Wave to Command", "AI Projects", "Sensor ML", "Intermediate", "22 min"),
        mission("ai-color-sorter-signal", "Color Sorting Signal", "Red Blue Green Decide", "AI Projects", "Vision Lite", "Intermediate", "20 min"),
        mission("ai-anomaly-threshold", "Anomaly Alert Thresholds", "Smart Warning Levels", "AI Projects", "Data ML", "Intermediate", "18 min"),
        mission("ai-tinyml-intro", "TinyML Intro on ESP32", "Machine Learning on Chip", "AI Projects", "TinyML", "Advanced", "25 min"),
        mission("ai-edge-impulse-deploy", "Deploy Edge Impulse Model", "Train Then Flash", "AI Projects", "TinyML", "Advanced", "30 min"),
        mission("ai-motion-pattern", "Motion Pattern Recognition", "Walk Jump Shake Detect", "AI Projects", "IMU ML", "Advanced", "25 min"),
        mission("ai-sensor-fusion", "Sensor Fusion Decision", "Combine Sensor Brains", "AI Projects", "Sensor ML", "Advanced", "25 min"),
        mission("ai-led-react-model", "LED Reacts to Model Output", "Light Shows AI Guess", "AI Projects", "TinyML", "Intermediate", "20 min"),
        mission("ai-voice-light-control", "Voice Light Control Demo", "Say On Say Off", "AI Projects", "Audio ML", "Advanced", "28 min"),
        mission("ai-on-device-inference", "Run Inference on Device", "No Cloud Needed", "AI Projects", "TinyML", "Advanced", "25 min"),
    ]

    advanced = [
        mission("adv-deep-sleep-battery", "Deep Sleep Battery Saver", "Nap to Save Power", "Advanced ESP32", "Power Management", "Intermediate", "18 min"),
        mission("adv-freertos-two-tasks", "Two Tasks with FreeRTOS", "Multitask Like a Pro", "Advanced ESP32", "RTOS", "Advanced", "25 min"),
        mission("adv-dual-core-split", "Split Work Across Dual Cores", "Two Brains One Board", "Advanced ESP32", "Architecture", "Advanced", "25 min"),
        mission("adv-i2c-bus-scanner", "I2C Bus Scanner Tool", "Find Hidden Addresses", "Advanced ESP32", "Debugging", "Beginner", "12 min"),
        mission("adv-spi-flash-storage", "Store Settings in SPI Flash", "Remember After Reboot", "Advanced ESP32", "Storage", "Intermediate", "20 min"),
        mission("adv-sd-card-data-logger", "SD Card Data Logger", "Big CSV Files", "Advanced ESP32", "Storage", "Intermediate", "22 min"),
        mission("adv-watchdog-recovery", "Watchdog Auto Recovery", "Reboot When Stuck", "Advanced ESP32", "Reliability", "Advanced", "20 min"),
        mission("adv-ota-firmware-update", "OTA Firmware Update", "Update Over Wi-Fi", "Advanced ESP32", "Deployment", "Advanced", "25 min"),
        mission("adv-secure-wifi-config", "Secure Wi-Fi Config Store", "Hide the Password", "Advanced ESP32", "Security", "Advanced", "22 min"),
        mission("adv-power-profile-test", "Power Profile Your Project", "Measure Milliamps", "Advanced ESP32", "Power Management", "Advanced", "20 min"),
        mission("adv-modbus-industrial-read", "Read Modbus Industrial Sensor", "Factory Floor Data", "Advanced ESP32", "Industrial", "Advanced", "28 min"),
        mission("adv-production-test-jig", "Production Self Test Jig", "Pass Fail on Boot", "Advanced ESP32", "Manufacturing", "Advanced", "25 min"),
    ]

    groups = [
        first_spark,
        sensors,
        displays,
        motors,
        communication,
        iot,
        ai,
        advanced,
    ]
    for group in groups:
        items.extend(group)

    for i, item in enumerate(items):
        item["prerequisites"] = [items[i - 1]["slug"]] if i > 0 else []
        item["next_guide"] = items[i + 1]["slug"] if i + 1 < len(items) else None
        item["status"] = "Complete" if item["slug"] in COMPLETE else "Coming Soon"

    return items


def main():
    missions = build_missions()
    counts = {}
    for m in missions:
        counts[m["level"]] = counts.get(m["level"], 0) + 1

    roadmap = {
        "version": 1,
        "title": "ESP32 Learning Missions Roadmap",
        "target_total": 100,
        "actual_total": len(missions),
        "complete_count": sum(1 for m in missions if m["status"] == "Complete"),
        "coming_soon_count": sum(1 for m in missions if m["status"] == "Coming Soon"),
        "learning_levels": LEVELS,
        "level_targets": LEVEL_TARGETS,
        "level_counts": counts,
        "missions": missions,
    }

    out = Path(__file__).resolve().parent.parent / "content" / "guide-roadmap.yaml"
    with out.open("w", encoding="utf-8") as f:
        yaml.dump(roadmap, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100)
    print(f"Wrote {out} ({len(missions)} missions, {roadmap['complete_count']} complete)")


if __name__ == "__main__":
    main()
