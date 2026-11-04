#include <Arduino.h>
#include <math.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BME280.h>

const int I2C_SDA = 21;
const int I2C_SCL = 22;

const int SCREEN_WIDTH = 128;
const int SCREEN_HEIGHT = 64;
const int OLED_RESET = -1;
const int OLED_ADDRESS = 0x3C;

const unsigned long SAMPLE_INTERVAL_MS = 2000;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_BME280 bme;
uint8_t bmeAddress = 0;

unsigned long lastSampleTime = 0;

bool oledResponds() {
  Wire.beginTransmission(OLED_ADDRESS);
  return Wire.endTransmission() == 0; // ACK only, not controller identification.
}

bool bmeResponds() {
  Wire.beginTransmission(bmeAddress); Wire.write(0xD0);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(bmeAddress, uint8_t(1)) != 1) return false;
  return Wire.read() == 0x60; // Compatibility check, not authenticity/calibration.
}
bool valuesPlausible(float t, float rh, float hpa) {
  return isfinite(t) && isfinite(rh) && isfinite(hpa) &&
    t >= -40 && t <= 85 && rh >= 0 && rh <= 100 && hpa >= 300 && hpa <= 1100;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(I2C_SDA, I2C_SCL);

  Wire.setTimeOut(50); // Per bus operation, not a whole-sketch deadline.
  if (!oledResponds()) {
    Serial.println("No I2C ACK at OLED_ADDRESS; check power, bus and address, then reset");
    while (true) delay(1000);
  }
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS, true, false)) {
    Serial.println("SSD1306 buffer/init failed; this is not a presence test");
    while (true) delay(1000);
  }

  bmeAddress = 0x76;
  bool bmeReady = bme.begin(bmeAddress, &Wire);

  if (!bmeReady) {
    bmeAddress = 0x77;
    bmeReady = bme.begin(bmeAddress, &Wire);
  }

  if (!bmeReady) {
    Serial.println("BME280 not found at 0x76 or 0x77.");
    showMessage("BME280 not found", "Check wiring");
    while (true) {
      delay(1000);
    }
  }

  Serial.println("Mission 11: Environmental sensor ready");
  showMessage("ESP32 Engine", "BME280 ready");
  delay(1500);
}

void loop() {
  unsigned long now = millis();

  if (now - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = now;

    if (!bmeResponds()) {
      Serial.println("Sensor unavailable: bus/chip check failed");
      showMessage("Sensor unavailable", "Check bus; see Serial");
      return; // Next scheduled sample retries; no stale values substituted.
    }
    float temperatureC = bme.readTemperature();
    float humidity = bme.readHumidity();
    float pressureHpa = bme.readPressure() / 100.0;

    if (!valuesPlausible(temperatureC, humidity, pressureHpa)) {
      Serial.println("Sensor unavailable: invalid sample");
      showMessage("Sensor unavailable", "Invalid sample");
      return;
    }
    printToSerial(temperatureC, humidity, pressureHpa);
    showOnDisplay(temperatureC, humidity, pressureHpa);
  }
}

void printToSerial(float temperatureC, float humidity, float pressureHpa) {
  Serial.print("Temperature: ");
  Serial.print(temperatureC, 1);
  Serial.print(" C | Humidity: ");
  Serial.print(humidity, 1);
  Serial.print(" % | Pressure: ");
  Serial.print(pressureHpa, 1);
  Serial.println(" hPa");
}

void showOnDisplay(float temperatureC, float humidity, float pressureHpa) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  display.setCursor(0, 0);
  display.println("Environment");

  display.setCursor(0, 16);
  display.print("Temp: ");
  display.print(temperatureC, 1);
  display.println(" C");

  display.setCursor(0, 32);
  display.print("Hum:  ");
  display.print(humidity, 1);
  display.println(" %");

  display.setCursor(0, 48);
  display.print("Pres: ");
  display.print(pressureHpa, 1);
  display.println(" hPa");

  display.display();
}

void showMessage(const char* line1, const char* line2) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 12);
  display.println(line1);
  display.setCursor(0, 32);
  display.println(line2);
  display.display();
}