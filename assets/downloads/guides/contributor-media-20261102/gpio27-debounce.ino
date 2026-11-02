const int BUTTON_PIN = 27;

const unsigned long DEBOUNCE_DELAY = 50;

int lastRawReading = HIGH;
int stableButtonState = HIGH;
unsigned long lastChangeTime = 0;
int pressCount = 0;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("Mission 05: Button debounce counter ready");
  Serial.println("Press the button and watch the count increase once.");
}

void loop() {
  int rawReading = digitalRead(BUTTON_PIN);

  if (rawReading != lastRawReading) {
    lastChangeTime = millis();
    lastRawReading = rawReading;
  }

  bool readingHasSettled = (millis() - lastChangeTime) > DEBOUNCE_DELAY;

  if (readingHasSettled && rawReading != stableButtonState) {
    stableButtonState = rawReading;

    if (stableButtonState == LOW) {
      pressCount++;
      Serial.print("Clean press count: ");
      Serial.println(pressCount);
    } else {
      Serial.println("Button released cleanly");
    }
  }
}