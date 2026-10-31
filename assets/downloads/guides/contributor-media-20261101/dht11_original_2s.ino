#include "DHT.h"

// DHT11 data pin connected to ESP32 GPIO4.
#define DHTPIN 4

// Tell the library which DHT sensor model you are using.
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(2000);

  dht.begin();
  Serial.println("DHT11 ESP32 room sensor ready");
  Serial.println("Reading every 2 seconds...");
}

void loop() {
  float humidity = dht.readHumidity();
  float temperatureC = dht.readTemperature();
  float temperatureF = dht.readTemperature(true);

  if (isnan(humidity) || isnan(temperatureC) || isnan(temperatureF)) {
    Serial.println("Read failed. Check wiring, power, pull-up resistor, and library setup.");
    delay(2000);
    return;
  }

  float heatIndexC = dht.computeHeatIndex(temperatureC, humidity, false);

  Serial.print("Temperature: ");
  Serial.print(temperatureC, 1);
  Serial.print(" C / ");
  Serial.print(temperatureF, 1);
  Serial.print(" F  |  Humidity: ");
  Serial.print(humidity, 1);
  Serial.print(" %  |  Heat index: ");
  Serial.print(heatIndexC, 1);
  Serial.println(" C");

  delay(2000);
}