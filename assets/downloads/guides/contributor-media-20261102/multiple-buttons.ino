 const byte BUTTON_COUNT = 3;

const byte buttonPins[BUTTON_COUNT] = {25, 26, 27};
const char* buttonNames[BUTTON_COUNT] = {"START", "STOP", "MODE"};

const unsigned long DEBOUNCE_DELAY = 50;

int lastRawReading[BUTTON_COUNT] = {HIGH, HIGH, HIGH};
int stableState[BUTTON_COUNT] = {HIGH, HIGH, HIGH};
unsigned long lastChangeTime[BUTTON_COUNT] = {0, 0, 0};

void setup() {
  Serial.begin(115200);

  for (byte i = 0; i < BUTTON_COUNT; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }

  Serial.println("Mission 06: Multiple buttons ready");
  Serial.println("Press START, STOP, or MODE.");
}

void loop() {
  for (byte i = 0; i < BUTTON_COUNT; i++) {
    checkButton(i);
  }
}

void checkButton(byte index) {
  int rawReading = digitalRead(buttonPins[index]);

  if (rawReading != lastRawReading[index]) {
    lastChangeTime[index] = millis();
    lastRawReading[index] = rawReading;
  }

  bool readingHasSettled = (millis() - lastChangeTime[index]) > DEBOUNCE_DELAY;

  if (readingHasSettled && rawReading != stableState[index]) {
    stableState[index] = rawReading;

    if (stableState[index] == LOW) {
      Serial.print(buttonNames[index]);
      Serial.println(" pressed");
    } else {
      Serial.print(buttonNames[index]);
      Serial.println(" released");
    }
  }
}