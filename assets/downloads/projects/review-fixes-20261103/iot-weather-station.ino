#include <Wire.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;

bool beginBME280() {
  if (bme.begin(0x76)) {
    Serial.println("BME280 found at I2C address 0x76");
    return true;
  }

  if (bme.begin(0x77)) {
    Serial.println("BME280 found at I2C address 0x77");
    return true;
  }

  return false;
}

void setup() {
  Serial.begin(115200);
  delay(200);

  Serial.println("ESP32 BME280 weather station");
  if (!beginBME280()) {
    Serial.println("BME280 not found at 0x76 or 0x77.");
    Serial.println("Check 3.3 V, GND, SDA=GPIO21, SCL=GPIO22, and module address.");
    while (true) delay(100);
  }

  Serial.println("Reading temperature, humidity, and pressure every 2 seconds");
}

void loop() {
  float tempC = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressureHpa = bme.readPressure() / 100.0F;

  Serial.print("Temperature C: ");
  Serial.print(tempC, 1);
  Serial.print(" | Humidity %: ");
  Serial.print(humidity, 1);
  Serial.print(" | Pressure hPa: ");
  Serial.println(pressureHpa, 1);

  delay(2000);
}
