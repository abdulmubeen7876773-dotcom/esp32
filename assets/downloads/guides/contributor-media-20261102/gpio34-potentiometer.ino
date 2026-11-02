#include <Arduino.h>
constexpr uint8_t POT_PIN = 34;
void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(POT_PIN, ADC_11db);
  Serial.println("Analog input ready: raw counts, not dial percent");
}
void loop() {
  const uint16_t raw = analogRead(POT_PIN);
  Serial.print("Raw ADC: ");
  Serial.println(raw);
  delay(200);
}