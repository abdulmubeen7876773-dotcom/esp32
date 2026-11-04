#include <Arduino.h>
#include <math.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BME280.h>

const int I2C_SDA = 21;
const int I2C_SCL = 22;

const int GREEN_LED_PIN = 18;
const int RED_LED_PIN = 19;
const int BUTTON_PIN = 23;

const int SCREEN_WIDTH = 128;
const int SCREEN_HEIGHT = 64;
const int OLED_RESET = -1;
const int OLED_ADDRESS = 0x3C;

const float TEMP_APPROACH_C = 28.0;
const float TEMP_WARNING_C = 30.0;

const unsigned long SAMPLE_INTERVAL_MS = 2000;
const unsigned long DEBOUNCE_MS = 40;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_BME280 bme;
uint8_t bmeAddress = 0;

float temperatureC = NAN;
float humidity = NAN;
float pressureHpa = NAN;
bool sampleValid = false;

int currentPage = 0;
int lastButtonReading = HIGH;
int stableButtonState = HIGH;
unsigned long lastButtonChangeTime = 0;
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

  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

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
    showMessage("BME280 not found", "Check I2C wiring");
    while (true) {
      delay(1000);
    }
  }

  showMessage("Course 01", "Capstone ready");
  Serial.println("Mission 12: Smart Environment Monitor ready");
  delay(1500);
}

void loop() {
  handleButton();

  unsigned long now = millis();
  if (now - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = now;
    readSensorData();
    updateAlerts();
    printSerialReport();
    updateDisplay();
  }
}

void handleButton() {
  int reading = digitalRead(BUTTON_PIN);

  if (reading != lastButtonReading) {
    lastButtonChangeTime = millis();
    lastButtonReading = reading;
  }

  if ((millis() - lastButtonChangeTime) > DEBOUNCE_MS) {
    if (reading != stableButtonState) {
      stableButtonState = reading;

      if (stableButtonState == LOW) {
        currentPage = 1 - currentPage;
        updateDisplay();
      }
    }
  }
}

void readSensorData() {
  sampleValid = false;
  temperatureC = humidity = pressureHpa = NAN;
  if (!bmeResponds()) return;
  temperatureC = bme.readTemperature();
  humidity = bme.readHumidity();
  pressureHpa = bme.readPressure() / 100.0;
  sampleValid = valuesPlausible(temperatureC, humidity, pressureHpa);
}

String environmentStatus() {
  if (!sampleValid) return "UNAVAILABLE";
  if (temperatureC >= TEMP_WARNING_C) {
    return "WARNING";
  }

  if (temperatureC >= TEMP_APPROACH_C) {
    return "WARM";
  }

  return "NORMAL";
}

void updateAlerts() {
  String status = environmentStatus();

  digitalWrite(GREEN_LED_PIN, status == "NORMAL" ? HIGH : LOW);
  digitalWrite(RED_LED_PIN, status == "WARNING" ? HIGH : LOW);
}

void updateDisplay() {
  if (!sampleValid) { showMessage("Sensor unavailable", "Check bus; see Serial"); return; }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  if (currentPage == 0) {
    display.setCursor(0, 0);
    display.println("Page 1: Climate");
    display.setCursor(0, 20);
    display.print("Temp: ");
    display.print(temperatureC, 1);
    display.println(" C");
    display.setCursor(0, 38);
    display.print("Hum:  ");
    display.print(humidity, 1);
    display.println(" %");
  } else {
    display.setCursor(0, 0);
    display.println("Page 2: Status");
    display.setCursor(0, 20);
    display.print("Pres: ");
    display.print(pressureHpa, 1);
    display.println(" hPa");
    display.setCursor(0, 42);
    display.print("Status: ");
    display.println(environmentStatus());
  }

  display.display();
}

void printSerialReport() {
  if (!sampleValid) { Serial.println("Sensor unavailable | Status: UNAVAILABLE"); return; }
  Serial.print("Temperature: ");
  Serial.print(temperatureC, 1);
  Serial.print(" C | Humidity: ");
  Serial.print(humidity, 1);
  Serial.print(" % | Pressure: ");
  Serial.print(pressureHpa, 1);
  Serial.print(" hPa | Status: ");
  Serial.println(environmentStatus());
}

void showMessage(const char* line1, const char* line2) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 14);
  display.println(line1);
  display.setCursor(0, 34);
  display.println(line2);
  display.display();
}