const int LEFT_SENSOR = 34;
const int RIGHT_SENSOR = 35;

const int L_IN1 = 16;
const int L_IN2 = 17;
const int R_IN1 = 18;
const int R_IN2 = 19;

// Calibrate these from your own dark line and light floor readings.
const int LEFT_THRESHOLD = 1800;
const int RIGHT_THRESHOLD = 1800;

// Set false if your sensors produce lower values on the dark line.
const bool LINE_IS_HIGH = true;

bool isOnLine(int value, int threshold) {
  return LINE_IS_HIGH ? value > threshold : value < threshold;
}

void leftMotor(bool forward) {
  digitalWrite(L_IN1, forward ? HIGH : LOW);
  digitalWrite(L_IN2, forward ? LOW : HIGH);
}

void rightMotor(bool forward) {
  digitalWrite(R_IN1, forward ? HIGH : LOW);
  digitalWrite(R_IN2, forward ? LOW : HIGH);
}

void stopLeftMotor() {
  digitalWrite(L_IN1, LOW);
  digitalWrite(L_IN2, LOW);
}

void stopRightMotor() {
  digitalWrite(R_IN1, LOW);
  digitalWrite(R_IN2, LOW);
}

void stopMotors() {
  stopLeftMotor();
  stopRightMotor();
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(L_IN1, OUTPUT); pinMode(L_IN2, OUTPUT);
  pinMode(R_IN1, OUTPUT); pinMode(R_IN2, OUTPUT);
  stopMotors();
  Serial.println("ESP32 line follower ready");
  Serial.println("Record raw values over LINE and FLOOR before running motors.");
}

void loop() {
  int leftValue = analogRead(LEFT_SENSOR);
  int rightValue = analogRead(RIGHT_SENSOR);

  bool leftOnLine = isOnLine(leftValue, LEFT_THRESHOLD);
  bool rightOnLine = isOnLine(rightValue, RIGHT_THRESHOLD);

  if (leftOnLine && rightOnLine) {
    leftMotor(true);
    rightMotor(true);
  } else if (leftOnLine && !rightOnLine) {
    stopLeftMotor();
    rightMotor(true);
  } else if (!leftOnLine && rightOnLine) {
    leftMotor(true);
    stopRightMotor();
  } else {
    stopMotors();
  }

  Serial.printf("L:%4d %s | R:%4d %s\n",
                leftValue, leftOnLine ? "LINE" : "FLOOR",
                rightValue, rightOnLine ? "LINE" : "FLOOR");
  delay(40);
}
