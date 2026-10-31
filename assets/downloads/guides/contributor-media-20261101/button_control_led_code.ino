const int BUTTON_PIN = 22;
const int LED_PIN = 2;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.println("Button controls LED mission ready");
}

void loop() {
  int buttonReading = digitalRead(BUTTON_PIN);
  bool buttonPressed = (buttonReading == LOW);

  digitalWrite(LED_PIN, buttonPressed ? HIGH : LOW);

  if (buttonPressed) {
    Serial.println("Button: PRESSED | LED: ON");
  } else {
    Serial.println("Button: RELEASED | LED: OFF");
  }

  delay(100);
}