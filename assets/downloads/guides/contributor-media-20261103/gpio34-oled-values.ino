#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int SCREEN_WIDTH = 128;
const int SCREEN_HEIGHT = 64;
const int OLED_RESET = -1;
const int POT_PIN = 34;

const int I2C_SDA = 21;
const int I2C_SCL = 22;
const int OLED_ADDRESS = 0x3C;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool oledResponds() {
  Wire.beginTransmission(OLED_ADDRESS);
  return Wire.endTransmission() == 0; // ACK only, not controller identification.
}

void setup() {
  Serial.begin(115200);

  Wire.begin(I2C_SDA, I2C_SCL);
  analogReadResolution(12);
  analogSetPinAttenuation(POT_PIN, ADC_11db);

  Wire.setTimeOut(50); // Per bus operation, not a whole-sketch deadline.
  if (!oledResponds()) {
    Serial.println("No I2C ACK at OLED_ADDRESS; check power, bus and address, then reset");
    while (true) delay(1000);
  }
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS, true, false)) {
    Serial.println("SSD1306 buffer/init failed; this is not a presence test");
    while (true) delay(1000);
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("ESP32 Engine");
  display.println("OLED ready");
  display.display();

  delay(1500);
}

void loop() {
  int rawValue = analogRead(POT_PIN);
  uint32_t millivolts = analogReadMilliVolts(POT_PIN); // A separate conversion.

  Serial.print("ADC: ");
  Serial.print(rawValue);
  Serial.print(" | mV estimate: ");
  Serial.print(millivolts);
  Serial.println(" mV");

  display.clearDisplay();

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Mission 09 OLED");

  display.setCursor(0, 18);
  display.print("ADC: ");
  display.println(rawValue);

  display.setCursor(0, 34);
  display.print("mV est: ");
  display.print(millivolts);
  display.println(" mV");

  display.setCursor(0, 52);
  display.println("GPIO34 -> screen");

  display.display();
  delay(250);
}