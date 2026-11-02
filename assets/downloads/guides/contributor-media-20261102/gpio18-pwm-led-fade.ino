const int LED_PIN = 18;

const int PWM_FREQUENCY = 5000;
const int PWM_RESOLUTION = 8;

void setup() {
  Serial.begin(115200);

  if (!ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION)) {
    Serial.println("PWM attachment failed");
    while (true) delay(1000);
  }

  Serial.println("Mission 07: PWM LED fade ready");
}

void loop() {
  for (int duty = 0; duty <= 255; duty += 5) {
    ledcWrite(LED_PIN, duty);
    Serial.print("Duty value: ");
    Serial.println(duty);
    delay(25);
  }

  for (int duty = 255; duty >= 0; duty -= 5) {
    ledcWrite(LED_PIN, duty);
    Serial.print("Duty value: ");
    Serial.println(duty);
    delay(25);
  }
}