// **Fixed Arduino code for ESP32 Core v3.3.12**
// This code resolves the linker error by providing the explicit setup() and loop() definitions.

const int INPUT_PIN = 27;
int lastState = -1; 

void setup() {
  // Initialize Serial Monitor at 115200 baud
  Serial.begin(115200);
  
  // Configures GPIO 27 as a standard digital input (floating test)
  pinMode(INPUT_PIN, INPUT); 
}

void loop() {
  // Read current voltage level on GPIO 27
  int currentState = digitalRead(INPUT_PIN);

  // Print only when a structural transition happens
  if (currentState != lastState) {
    if (currentState == HIGH) {
      Serial.println("GPIO 27 reads HIGH");
    } else {
      Serial.println("GPIO 27 reads LOW");
    }
    
    // Save current state value
    lastState = currentState;
  }
  
  // Brief pause for stability
  delay(50); 
}
