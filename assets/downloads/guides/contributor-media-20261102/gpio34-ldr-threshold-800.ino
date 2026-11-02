constexpr uint8_t LDR_PIN = 34;
constexpr uint16_t LIGHT_THRESHOLD = 800;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(LDR_PIN, ADC_11db);
  delay(500);
  Serial.println("Mission 09: Analog light sensor ready");
  Serial.println("Cover the LDR, then shine light on it, and watch the raw values.");
}

void loop() {
  const uint16_t rawLight = analogRead(LDR_PIN);
  
  Serial.print("Light ADC: ");
  Serial.print(rawLight);
  
  if (rawLight < LIGHT_THRESHOLD) {
    Serial.println(" | DARK");
  } else {
    Serial.println(" | BRIGHT");
  }
  
  delay(250);
}
