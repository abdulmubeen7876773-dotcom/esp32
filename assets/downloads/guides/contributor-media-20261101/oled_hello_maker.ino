#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool oledResponds() {
  Wire.beginTransmission(OLED_ADDRESS);
  return Wire.endTransmission() == 0; // ACK only, not controller identification.
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

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
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 20);
  display.println("Hello,");
  display.println("Maker!");
  display.display();
}

void loop() {
}