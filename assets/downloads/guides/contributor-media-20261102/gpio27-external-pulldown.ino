const int BUTTON_PIN = 27;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT);
}

void loop() {
  bool pressed = digitalRead(BUTTON_PIN) == HIGH;
  Serial.println(pressed ? "PRESSED" : "RELEASED");
  delay(250);
}