#include <Arduino.h>
#include <Wire.h>

constexpr int I2C_SDA = 21;
constexpr int I2C_SCL = 22;

void setup() {
  Serial.begin(115200);
  delay(1000);
  if (!Wire.begin(I2C_SDA, I2C_SCL, 100000)) {
    Serial.println("I2C initialization failed: check board and pin selection.");
    while (true) delay(1000);
  }
  Wire.setTimeOut(50); // Milliseconds per transaction, not the scan interval.
  Serial.println("I2C scanner: SDA GPIO21, SCL GPIO22, 100 kHz");
}

void loop() {
  unsigned int found = 0;
  unsigned int faults = 0;
  for (uint8_t address = 0x08; address <= 0x77; ++address) {
    Wire.beginTransmission(address);
    const uint8_t status = Wire.endTransmission();
    if (status == 0) {
      Serial.printf("ACK at 7-bit address 0x%02X (identity not checked)\n", address);
      ++found;
    } else if (status != 2) { // 2: address NACK; no response at this address.
      Serial.printf("Bus error %u at 0x%02X\n", status, address);
      ++faults;
    }
  }
  Serial.printf("Scan: %u responding address(es), %u bus error(s)\n", found, faults);
  if (found == 0) Serial.println("Check power, common GND, pins and pull-ups.");
  delay(5000);
}