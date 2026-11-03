    #include <Arduino.h>
    #include <math.h>
    #include <Wire.h>
    #include <Adafruit_BME280.h>
  
    // Example pins for a common original ESP32 DevKit. Adjust for your board.
    const int I2C_SDA = 21;
    const int I2C_SCL = 22;
  
    // Replace with a suitable local sea-level pressure reference for better altitude estimates.
    const float SEA_LEVEL_PRESSURE_HPA = 1013.25F;
  
    Adafruit_BME280 bme;
  
    void setup() {
      Serial.begin(115200);
      delay(100);
  
      Wire.begin(I2C_SDA, I2C_SCL);
  
      bool sensorFound = bme.begin(0x76, &Wire);
      if (!sensorFound) {
        sensorFound = bme.begin(0x77, &Wire);
      }
  
      if (!sensorFound) {
        Serial.println("BME280 not found. Check wiring and I2C address.");
        while (true) {
          delay(1000);
        }
      }
  
      Serial.println("BME280 ready");
    }
  
    void loop() {
      const float temperatureC = bme.readTemperature();
      const float humidityPercent = bme.readHumidity();
      const float pressureHpa = bme.readPressure() / 100.0F;
      const float altitudeMeters = bme.readAltitude(SEA_LEVEL_PRESSURE_HPA);
      if (!isfinite(temperatureC) || !isfinite(humidityPercent) ||
          !isfinite(pressureHpa) || !isfinite(altitudeMeters)) {
        Serial.println("Invalid BME280 sample; check wiring and reset if needed.");
        delay(1000);
        return;
      }
  
      Serial.print("Temperature: ");
      Serial.print(temperatureC, 2);
      Serial.println(" °C");
  
      Serial.print("Humidity: ");
      Serial.print(humidityPercent, 2);
      Serial.println(" %");
  
      Serial.print("Pressure: ");
      Serial.print(pressureHpa, 2);
      Serial.println(" hPa");
  
      Serial.print("Approx. altitude: ");
      Serial.print(altitudeMeters, 1);
      Serial.println(" m");
      Serial.println();
  
      delay(1000);
    }