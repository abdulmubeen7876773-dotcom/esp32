<?php
/* ESP32 Engine — Phase 3 Guide Data (Guides 1–5): GPIO & Hardware */
return [

/* ─── Guide 1: Digital Inputs ─── */
[
  'slug'      => 'digital-inputs-esp32',
  'title'     => 'Digital Inputs on ESP32: Complete GPIO Input Guide',
  'meta_desc' => 'Master digital inputs on ESP32 — configure INPUT, INPUT_PULLUP, INPUT_PULLDOWN, use digitalRead(), hardware interrupts, and protect against 5V signals.',
  'read_time' => '14 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['digital-outputs-esp32','reading-buttons-esp32','pull-up-pull-down-resistors','safe-gpio-pins-esp32'],
  'faqs'      => [
    ['q'=>'What voltage does ESP32 read as digital HIGH?','a'=>'ESP32 uses 3.3V logic. A pin reads HIGH when voltage is above roughly 2.64V, and LOW when below about 0.66V. The 0.66V–2.64V range is indeterminate — avoid driving inputs into this zone.'],
    ['q'=>'How do I configure an ESP32 pin as digital input?','a'=>'Call pinMode(pin, INPUT) in setup() for a bare input. Use INPUT_PULLUP to enable the built-in ~47kΩ pull-up (pin reads HIGH by default), or INPUT_PULLDOWN for the pull-down (pin reads LOW by default). Then call digitalRead(pin) to read the state.'],
    ['q'=>'What is a floating pin and why is it dangerous?','a'=>'A floating pin is not connected to any defined voltage. Environmental noise causes it to read randomly as HIGH or LOW, triggering false events. Always connect a pull-up or pull-down resistor, or use INPUT_PULLUP / INPUT_PULLDOWN mode.'],
    ['q'=>'Can all ESP32 GPIOs be used as digital inputs?','a'=>'Most can. GPIO34, 35, 36 (VP), and 39 (VN) are input-only — they cannot be configured as outputs and have no internal pull resistors. GPIO6–GPIO11 are connected to internal flash and should not be used.'],
    ['q'=>'Can I use interrupts on ESP32 digital inputs?','a'=>'Yes — every GPIO supports hardware interrupts. Call attachInterrupt(digitalPinToInterrupt(pin), myISR, RISING/FALLING/CHANGE) and mark the ISR with IRAM_ATTR. Keep ISR functions very short — no Serial.print or delay inside them.'],
    ['q'=>'Are ESP32 GPIO pins 5V tolerant?','a'=>'No. ESP32 GPIO pins have a maximum voltage of 3.6V. Applying 5V will permanently damage the chip. Use a voltage divider (10kΩ + 20kΩ) or a dedicated logic-level converter when interfacing with 5V sensors or microcontrollers.'],
    ['q'=>'What is the difference between INPUT_PULLUP and INPUT_PULLDOWN?','a'=>'INPUT_PULLUP enables an internal ~47kΩ resistor between the pin and 3.3V, so the pin reads HIGH by default. INPUT_PULLDOWN connects an internal resistor to GND, so the pin reads LOW by default. Use PULLUP when wiring a button to GND, and PULLDOWN when wiring to 3.3V.'],
    ['q'=>'Why does my digital input read random values with nothing connected?','a'=>'This is the classic floating-pin problem. Without a pull resistor, the GPIO picks up electromagnetic interference and toggles unpredictably. The fix is always to add a pull-up or pull-down — either external (10kΩ) or via INPUT_PULLUP / INPUT_PULLDOWN in code.'],
    ['q'=>'What is the maximum sampling speed for digital inputs?','a'=>'In Arduino loop mode, practical digitalRead() speed is roughly 1 MHz with no other processing. For faster signals, use hardware interrupts (triggered within ~1–5 µs) or the ESP32 PCNT (Pulse Counter) peripheral which can count MHz-range pulses autonomously.'],
    ['q'=>'Can GPIO34–GPIO39 use INPUT_PULLUP?','a'=>'No. GPIO34, GPIO35, GPIO36, and GPIO39 are input-only and have no internal pull resistors. If you use these pins for buttons or switches, you must add an external pull-up or pull-down resistor on the PCB or breadboard.'],
  ],
  'body_html' => <<<'BODY'
<h2>Introduction to Digital Inputs on ESP32</h2>
<p>Digital inputs are the bedrock of interactive ESP32 projects. Every button press, door sensor, limit switch, and motion detector relies on reading a binary HIGH or LOW voltage from a GPIO pin. ESP32 has up to 34 GPIO pins with hardware pull-up and pull-down resistors built in, making it one of the most flexible microcontrollers for digital input applications.</p>
<p>This guide covers everything from basic <code>digitalRead()</code> usage through hardware interrupts, input-only pins, voltage protection, and real-world project examples. After reading this, you will be able to wire and code any digital input scenario confidently.</p>

<h2>How Digital Logic Levels Work on ESP32</h2>
<p>ESP32 is a 3.3V device. Its GPIO pins interpret voltages in three regions:</p>
<table>
  <thead><tr><th>Voltage</th><th>Logic State</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>0 V – 0.66 V</td><td>LOW</td><td>digitalRead() returns 0</td></tr>
    <tr><td>0.66 V – 2.64 V</td><td>Undefined</td><td>Unpredictable — avoid</td></tr>
    <tr><td>2.64 V – 3.3 V</td><td>HIGH</td><td>digitalRead() returns 1</td></tr>
  </tbody>
</table>
<p>You must drive the input firmly into the HIGH or LOW region. Leaving a pin floating (no connection, no pull resistor) places it in the undefined zone where noise dominates.</p>

<h2>ESP32 GPIO Pin Capabilities at a Glance</h2>
<table>
  <thead><tr><th>GPIO Range</th><th>Input?</th><th>Output?</th><th>Pull Resistors?</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>GPIO0–GPIO5</td><td>Yes</td><td>Yes</td><td>Yes</td><td>GPIO0, GPIO2 affect boot; use carefully</td></tr>
    <tr><td>GPIO6–GPIO11</td><td>Avoid</td><td>Avoid</td><td>Yes</td><td>Tied to internal SPI flash — do not use</td></tr>
    <tr><td>GPIO12–GPIO33</td><td>Yes</td><td>Yes</td><td>Yes</td><td>General purpose, safest for projects</td></tr>
    <tr><td>GPIO34–GPIO39</td><td>Yes</td><td>No</td><td>No</td><td>Input-only; needs external pull resistors</td></tr>
  </tbody>
</table>
<p><strong>Recommended safe input pins:</strong> GPIO4, GPIO13, GPIO14, GPIO16, GPIO17, GPIO18, GPIO19, GPIO21, GPIO22, GPIO23, GPIO25, GPIO26, GPIO27, GPIO32, GPIO33, GPIO34, GPIO35.</p>

<h2>Configuring Pins: INPUT, INPUT_PULLUP, INPUT_PULLDOWN</h2>
<p>The <code>pinMode()</code> function in <code>setup()</code> sets the electrical mode of a GPIO:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>void setup() {
  Serial.begin(115200);

  pinMode(4,  INPUT);           // Floating — needs external resistor
  pinMode(16, INPUT_PULLUP);    // Internal ~47kΩ pull-up → reads HIGH by default
  pinMode(17, INPUT_PULLDOWN);  // Internal ~47kΩ pull-down → reads LOW by default
}

void loop() {
  Serial.printf("GPIO4=%d  GPIO16=%d  GPIO17=%d\n",
    digitalRead(4), digitalRead(16), digitalRead(17));
  delay(300);
}</pre>
</div>
<p>The most common choice for buttons is <strong>INPUT_PULLUP</strong> with the other end of the button wired to GND. When the button is pressed the pin is pulled LOW — this is called <em>active-LOW logic</em>.</p>

<h2>The Floating Pin Problem (and How to Solve It)</h2>
<p>A floating pin is a GPIO connected to nothing — no voltage source, no pull resistor. Electromagnetic fields from nearby wires, the MCU itself, and even your hand induce tiny currents that cause the pin to oscillate between HIGH and LOW randomly. The fix is simple:</p>
<ul>
  <li><strong>Software pull-up:</strong> use <code>INPUT_PULLUP</code> in <code>pinMode()</code></li>
  <li><strong>Software pull-down:</strong> use <code>INPUT_PULLDOWN</code> in <code>pinMode()</code></li>
  <li><strong>External pull-up:</strong> connect a 10 kΩ resistor between the pin and 3.3 V</li>
  <li><strong>External pull-down:</strong> connect a 10 kΩ resistor between the pin and GND</li>
</ul>
<p>External resistors are slightly preferred in noisy environments or when the pin travels off-board on a long wire, because the internal ~47 kΩ resistors are weaker and more susceptible to interference.</p>

<h2>Reading a Button: Step-by-Step Project</h2>
<p>Wire a momentary push button between GPIO16 and GND. No external resistor needed — we'll use INPUT_PULLUP.</p>
<table>
  <thead><tr><th>Button Terminal</th><th>Connect To</th></tr></thead>
  <tbody>
    <tr><td>Terminal A</td><td>ESP32 GPIO16</td></tr>
    <tr><td>Terminal B</td><td>ESP32 GND</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16
#define LED_PIN     2   // Built-in LED on most ESP32 dev boards

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // HIGH normally, LOW when pressed
  pinMode(LED_PIN,    OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {   // Active-LOW: button pressed
    digitalWrite(LED_PIN, HIGH);
    Serial.println("PRESSED");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("released");
  }
  delay(50);
}</pre>
</div>

<h2>Reading Multiple Inputs Simultaneously</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>const int BUTTONS[]  = {16, 17, 18, 19};
const int NUM_BTN    = 4;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_BTN; i++)
    pinMode(BUTTONS[i], INPUT_PULLUP);
}

void loop() {
  for (int i = 0; i < NUM_BTN; i++) {
    Serial.printf("B%d=%s ", i + 1, digitalRead(BUTTONS[i]) == LOW ? "ON " : "off");
  }
  Serial.println();
  delay(200);
}</pre>
</div>

<h2>Hardware Interrupts for Fast Response</h2>
<p>Polling <code>digitalRead()</code> in <code>loop()</code> may miss very brief signals. Hardware interrupts trigger immediately when the pin changes state, regardless of what the main loop is doing.</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BTN_PIN 16
#define LED_PIN  2

volatile bool btnFlag = false;   // shared between ISR and main

void IRAM_ATTR onButtonPress() { // IRAM_ATTR = runs from RAM, not flash
  btnFlag = true;                // keep ISR short — no delay/Serial here
}

void setup() {
  Serial.begin(115200);
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(BTN_PIN), onButtonPress, FALLING);
}

void loop() {
  if (btnFlag) {
    btnFlag = false;
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));   // toggle LED
    Serial.println("Interrupt fired — button pressed!");
  }
}</pre>
</div>
<p>Key rules for ISR functions: always use <code>IRAM_ATTR</code>, keep the function to a few lines, use <code>volatile</code> on any variable the ISR writes, and never call <code>Serial</code>, <code>delay()</code>, or <code>millis()</code> inside the ISR.</p>

<h2>Input-Only Pins: GPIO34–GPIO39</h2>
<p>These four pins are special — they can only ever be inputs, and they have no internal pull resistors. They are ideal for clean analog signals (they double as high-quality ADC channels) and for digital inputs that arrive from clean, well-driven sources like sensors that actively output 3.3 V or 0 V.</p>
<p>If you must use them with a button or switch, add a 10 kΩ external pull-up (to 3.3 V) or pull-down (to GND) on the breadboard.</p>

<h2>Protecting ESP32 from 5 V Signals</h2>
<p>Many sensors, modules, and older Arduino peripherals run on 5 V logic. Connecting them directly to ESP32 GPIO pins will exceed the 3.6 V maximum and can permanently damage the chip. Two safe solutions:</p>
<table>
  <thead><tr><th>Method</th><th>Parts Needed</th><th>Best For</th></tr></thead>
  <tbody>
    <tr><td>Voltage Divider</td><td>10 kΩ + 20 kΩ resistors</td><td>Slow signals, sensors</td></tr>
    <tr><td>Logic Level Converter</td><td>TXS0108E / BSS138</td><td>Fast signals, I2C, SPI</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Voltage Divider (5 V → 3.3 V)</span><button class="copy-btn">Copy</button></div>
  <pre>5V_signal ──── 10kΩ ──── GPIO_pin (3.3V max)
                    |
                   20kΩ
                    |
                   GND

Vout = 5 × (20k / (10k + 20k)) = 3.33 V ✓</pre>
</div>

<h2>PIR Motion Sensor Project</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define PIR_PIN 32
#define LED_PIN  2

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);   // PIR actively drives HIGH or LOW
  pinMode(LED_PIN, OUTPUT);
  delay(2000);               // PIR initialisation warm-up
  Serial.println("PIR ready — monitoring motion...");
}

void loop() {
  if (digitalRead(PIR_PIN) == HIGH) {
    Serial.println("Motion detected!");
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(100);
}</pre>
</div>

<h2>Summary</h2>
<p>Digital inputs on ESP32 revolve around three key concepts: logic levels (3.3 V system, avoid voltages above 3.6 V), pull resistors (always define a resting state — never float), and timing (polling for slow events, interrupts for fast ones). Master these and any button, sensor, or switch becomes straightforward.</p>
BODY,
],

/* ─── Guide 2: Digital Outputs ─── */
[
  'slug'      => 'digital-outputs-esp32',
  'title'     => 'Digital Outputs on ESP32: Control LEDs, Relays, and More',
  'meta_desc' => 'Learn how to control digital outputs on ESP32 with digitalWrite(), manage output current, drive LEDs and relays, and use safe GPIO output pins.',
  'read_time' => '12 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['digital-inputs-esp32','driving-leds-esp32','using-relays-safely-esp32','safe-gpio-pins-esp32'],
  'faqs'      => [
    ['q'=>'How much current can each ESP32 GPIO output pin source?','a'=>'Each ESP32 GPIO can source (output HIGH) or sink (output LOW) a maximum of 40 mA, but the recommended safe limit is 12 mA per pin. The total current across all GPIOs should not exceed 1200 mA. For loads above 40 mA use a transistor or MOSFET.'],
    ['q'=>'How do I configure a GPIO as digital output?','a'=>'Call pinMode(pin, OUTPUT) in setup() then use digitalWrite(pin, HIGH) to drive the pin to 3.3V or digitalWrite(pin, LOW) to drive it to 0V (GND).'],
    ['q'=>'Which ESP32 pins should I avoid for digital output?','a'=>'Avoid GPIO0 (boot mode), GPIO2 (connected to built-in LED on some boards, affects boot), GPIO5 (outputs PWM at boot), GPIO12 (affects flash voltage), and GPIO6–GPIO11 (connected to internal flash). GPIO34–GPIO39 cannot be outputs at all.'],
    ['q'=>'What is the output voltage of an ESP32 GPIO pin set HIGH?','a'=>'When set HIGH, an ESP32 GPIO pin outputs approximately 3.3 V. It is not 5 V. If you need 5 V output to drive 5 V peripherals, use a transistor or level-shifting circuit.'],
    ['q'=>'Can I drive a relay directly from an ESP32 GPIO pin?','a'=>'Not directly. A relay coil typically draws 60–100 mA which far exceeds the 40 mA GPIO maximum. Use a relay module with a built-in transistor driver, or add your own NPN transistor (e.g. 2N2222) between the GPIO and the relay coil.'],
    ['q'=>'What is the difference between OUTPUT and INPUT mode?','a'=>'In OUTPUT mode the GPIO actively drives the pin to either 3.3V (HIGH) or GND (LOW). In INPUT mode the pin is high-impedance and reads the external voltage. Setting a pin to OUTPUT while something external also tries to drive it can short-circuit and damage the GPIO.'],
    ['q'=>'Can I toggle an ESP32 GPIO faster than digitalWrite()?','a'=>'Yes. For maximum speed use direct register writes: GPIO.out_w1ts.val = (1 << pin) for HIGH and GPIO.out_w1tc.val = (1 << pin) for LOW. This can toggle pins in the 10–80 MHz range. For most projects, digitalWrite() at ~1 µs per call is plenty fast.'],
    ['q'=>'What happens if I connect two OUTPUT pins together?','a'=>'If one pin is HIGH and the other LOW, you create a short circuit through the GPIO drivers, potentially damaging both pins and the chip. Never connect two OUTPUT pins directly together. Use OUTPUT only when you own the signal.'],
    ['q'=>'Does the ESP32 remember its output state after deep sleep?','a'=>'No. GPIO output states are not preserved through deep sleep by default. Pins return to their boot-state configuration when the ESP32 wakes up. You can hold output states during light sleep, but deep sleep resets GPIO.'],
    ['q'=>'How do I control output speed or create PWM from a digital output?','a'=>'For PWM use ledcSetup(), ledcAttachPin(), and ledcWrite() which drive the hardware LEDC peripheral. For simple on/off patterns, digitalWrite() with delay() or millis() timing is sufficient. True digital output has no intermediate speeds.'],
  ],
  'body_html' => <<<'BODY'
<h2>Introduction to Digital Outputs on ESP32</h2>
<p>A digital output pin actively drives a voltage: either 3.3 V (HIGH, logic 1) or 0 V (LOW, logic 0). Through digital outputs you turn LEDs on and off, trigger relay coils, control motor drivers, signal other microcontrollers, and create timing signals. The ESP32 provides up to 30 usable output-capable GPIOs with a maximum of 40 mA per pin — powerful enough for most direct-drive applications.</p>

<h2>Output Current Capabilities</h2>
<p>Staying within safe current limits is critical to protect your ESP32 from damage:</p>
<table>
  <thead><tr><th>Limit</th><th>Value</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>Max per GPIO pin</td><td>40 mA</td><td>Absolute maximum — do not exceed</td></tr>
    <tr><td>Recommended per pin</td><td>12 mA</td><td>Safe for continuous operation</td></tr>
    <tr><td>Total across all GPIOs</td><td>1200 mA</td><td>Chip-wide limit</td></tr>
    <tr><td>3.3 V rail (VDD)</td><td>600 mA</td><td>Combined board regulator output</td></tr>
  </tbody>
</table>
<p>Standard 5 mm LEDs draw ~20 mA, which is fine. Relay coils (60–100 mA), buzzers, and DC motors far exceed GPIO limits — use a transistor or dedicated driver IC for those.</p>

<h2>Safe Output Pins on ESP32</h2>
<table>
  <thead><tr><th>Pin Group</th><th>Use As Output?</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>GPIO4, GPIO13, GPIO14</td><td>Safe ✓</td><td>General purpose, no boot concerns</td></tr>
    <tr><td>GPIO16, GPIO17, GPIO18, GPIO19</td><td>Safe ✓</td><td>Excellent general-purpose outputs</td></tr>
    <tr><td>GPIO21, GPIO22, GPIO23</td><td>Safe ✓</td><td>Also used for I2C/SPI — share carefully</td></tr>
    <tr><td>GPIO25, GPIO26, GPIO27</td><td>Safe ✓</td><td>Also DAC-capable (GPIO25, GPIO26)</td></tr>
    <tr><td>GPIO32, GPIO33</td><td>Safe ✓</td><td>Also good ADC channels</td></tr>
    <tr><td>GPIO0, GPIO2, GPIO5, GPIO12</td><td>Careful ⚠</td><td>Affect boot mode or flash voltage</td></tr>
    <tr><td>GPIO6–GPIO11</td><td>Avoid ✗</td><td>Internal flash — do not use</td></tr>
    <tr><td>GPIO34–GPIO39</td><td>Never ✗</td><td>Input only — no output capability</td></tr>
  </tbody>
</table>

<h2>Basic Digital Output: The Blink Sketch</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define LED_PIN 2   // Built-in LED on ESP32 DevKit

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  Serial.println("Blink demo running...");
}

void loop() {
  digitalWrite(LED_PIN, HIGH);   // LED on  (3.3 V on pin)
  Serial.println("LED ON");
  delay(1000);

  digitalWrite(LED_PIN, LOW);    // LED off (0 V on pin)
  Serial.println("LED OFF");
  delay(1000);
}</pre>
</div>

<h2>Controlling Multiple Outputs</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>const int LEDS[]  = {16, 17, 18, 19};
const int NUM_LED = 4;

void setup() {
  for (int i = 0; i < NUM_LED; i++)
    pinMode(LEDS[i], OUTPUT);
}

void loop() {
  // Knight Rider scan
  for (int i = 0; i < NUM_LED; i++) {
    digitalWrite(LEDS[i], HIGH);
    delay(100);
    digitalWrite(LEDS[i], LOW);
  }
  for (int i = NUM_LED - 2; i > 0; i--) {
    digitalWrite(LEDS[i], HIGH);
    delay(100);
    digitalWrite(LEDS[i], LOW);
  }
}</pre>
</div>

<h2>Non-Blocking Output Timing with millis()</h2>
<p>Using <code>delay()</code> blocks the entire processor. For projects that must do other things while toggling outputs, use <code>millis()</code>:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define LED_PIN    2
#define INTERVAL 500   // ms between toggles

unsigned long lastToggle = 0;
bool ledState = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  if (now - lastToggle >= INTERVAL) {
    lastToggle = now;
    ledState   = !ledState;
    digitalWrite(LED_PIN, ledState);
    Serial.printf("LED is now %s\n", ledState ? "ON" : "OFF");
  }
  // Other code here runs continuously without blocking
}</pre>
</div>

<h2>Driving an LED with Current Limiting</h2>
<p>Never connect an LED directly between GPIO and GND — it will draw unlimited current and burn out the LED or damage the GPIO. Always use a current-limiting resistor:</p>
<div class="code-block">
  <div class="code-bar"><span>Resistor Calculation</span><button class="copy-btn">Copy</button></div>
  <pre>R = (Vsupply - Vf) / If

Standard red LED:   Vf = 2.0V, If = 20mA
R = (3.3 - 2.0) / 0.020 = 65Ω → use 68Ω or 100Ω

Blue/white LED:     Vf = 3.2V, If = 20mA
R = (3.3 - 3.2) / 0.020 = 5Ω → too low! Limit to 5–10mA instead
R = (3.3 - 3.2) / 0.010 = 10Ω</pre>
</div>
<table>
  <thead><tr><th>Component</th><th>Connection</th></tr></thead>
  <tbody>
    <tr><td>LED anode (+)</td><td>Via 100 Ω resistor to ESP32 GPIO</td></tr>
    <tr><td>LED cathode (–)</td><td>ESP32 GND</td></tr>
  </tbody>
</table>

<h2>Driving High-Current Loads via Transistor</h2>
<p>When you need to switch loads above 40 mA (buzzers, motors, relay coils), a small NPN transistor like the 2N2222 or BC547 lets the GPIO control the load safely:</p>
<div class="code-block">
  <div class="code-bar"><span>NPN Transistor Switch Wiring</span><button class="copy-btn">Copy</button></div>
  <pre>3.3V or 5V ──────────── Relay coil (+)
                               |
                        Relay coil (–)
                               |
                          Collector (NPN)
                           Emitter ──── GND

ESP32 GPIO ── 1kΩ ── Base (NPN)

Add flyback diode across relay coil: anode to GND, cathode to VCC.</pre>
</div>

<h2>GPIO State at Boot</h2>
<p>Several ESP32 GPIOs are sampled at boot to determine the boot mode. Placing an output device on a strapping pin can cause boot failures:</p>
<ul>
  <li><strong>GPIO0</strong>: LOW at boot → enters flash download mode (avoid for general output)</li>
  <li><strong>GPIO2</strong>: Must be LOW or floating at boot for normal operation</li>
  <li><strong>GPIO5</strong>: Outputs 1 kHz PWM signal during boot</li>
  <li><strong>GPIO12</strong>: HIGH at boot selects 1.8 V flash voltage (very dangerous)</li>
</ul>
<p>For reliable output control, stick to GPIO16, GPIO17, GPIO18, GPIO19, GPIO21, GPIO22, GPIO23, GPIO25, GPIO26, GPIO27, GPIO32, GPIO33.</p>

<h2>Summary</h2>
<p>Digital outputs on ESP32 are simple but require awareness of three constraints: current limits (40 mA max per pin, 12 mA recommended), boot-strapping conflicts (avoid GPIO0, GPIO2, GPIO5, GPIO12), and input-only pins (GPIO34–GPIO39 cannot be outputs). Use millis() instead of delay() for non-blocking timing, a transistor for loads above 40 mA, and always include current-limiting resistors for LEDs.</p>
BODY,
],

/* ─── Guide 3: Pull-Up vs Pull-Down ─── */
[
  'slug'      => 'pull-up-pull-down-resistors',
  'title'     => 'Pull-Up vs Pull-Down Resistors on ESP32: Full Explanation',
  'meta_desc' => 'Understand pull-up and pull-down resistors for ESP32 GPIO — when to use external vs internal resistors, resistor values, wiring diagrams, and power implications.',
  'read_time' => '11 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['digital-inputs-esp32','reading-buttons-esp32','debouncing-buttons-esp32','safe-gpio-pins-esp32'],
  'faqs'      => [
    ['q'=>'What is the purpose of a pull-up resistor?','a'=>'A pull-up resistor connects the GPIO pin to the supply voltage (3.3V on ESP32) through a resistor, ensuring the pin reads HIGH by default when nothing is actively driving it. When a button or switch connects the pin to GND, it overrides the pull-up and the pin reads LOW.'],
    ['q'=>'What is the purpose of a pull-down resistor?','a'=>'A pull-down resistor connects the GPIO pin to GND through a resistor, ensuring the pin reads LOW by default. When a button connects the pin to 3.3V, it overrides the pull-down and the pin reads HIGH. Pull-downs are used for active-HIGH button circuits.'],
    ['q'=>'What resistor value should I use for a pull-up or pull-down?','a'=>'The standard value is 10 kΩ. This is low enough to overcome electrical noise but high enough to limit current when the button is pressed (3.3V / 10kΩ = 0.33 mA — negligible power consumption). Values from 4.7 kΩ to 47 kΩ are all acceptable.'],
    ['q'=>'What is the internal pull-up resistance on ESP32?','a'=>'ESP32 internal pull-up and pull-down resistors are approximately 45–47 kΩ. This is weaker than a typical 10 kΩ external resistor, making them more susceptible to noise on long wires or in electrically noisy environments.'],
    ['q'=>'When should I use an external resistor instead of INPUT_PULLUP?','a'=>'Use external resistors when: the wire from button to ESP32 is longer than 30 cm, the environment is electrically noisy (near motors or RF transmitters), you need faster response times, or the pin is input-only (GPIO34–39, which have no internal resistors).'],
    ['q'=>'Does leaving an ESP32 button input floating use more power?','a'=>'Yes, indirectly. A floating pin may oscillate between HIGH and LOW, causing spurious interrupts or extra processing. This increases average power consumption in battery-powered designs. Always define a resting state with a pull resistor to minimise this.'],
    ['q'=>'Can I use a pull-up and pull-down resistor on the same pin?','a'=>'Technically yes, but it is wasteful and unusual. The two resistors would form a voltage divider, leaving the pin at half the supply voltage (neither a clean HIGH nor a clean LOW), which creates the indeterminate zone. Use one or the other, not both.'],
    ['q'=>'How does INPUT_PULLUP affect button wiring?','a'=>'With INPUT_PULLUP, the pin rests at HIGH (3.3V). Connect one button terminal to the GPIO pin and the other to GND. When pressed, the pin is pulled to GND (LOW). This is active-LOW logic: button pressed = LOW state.'],
    ['q'=>'How does INPUT_PULLDOWN affect button wiring?','a'=>'With INPUT_PULLDOWN, the pin rests at LOW (GND). Connect one button terminal to the GPIO pin and the other to 3.3V. When pressed, the pin is pulled HIGH. This is active-HIGH logic: button pressed = HIGH state.'],
    ['q'=>'Do pull resistors affect ADC readings on ESP32?','a'=>'Yes. If you use a GPIO pin with an internal pull-up for ADC reading (analogRead), the pull-up resistor adds current to the measurement and skews the voltage. Always use INPUT mode (no pull resistors) on ADC pins and place any conditioning externally.'],
  ],
  'body_html' => <<<'BODY'
<h2>Why Pull Resistors Exist</h2>
<p>GPIO pins in INPUT mode have very high impedance — almost no current flows through them. This means they are extremely sensitive to tiny voltages induced by nearby electrical fields. Without a defined reference voltage, the pin reads randomly: sometimes HIGH, sometimes LOW, with no button pressed at all. Pull resistors solve this by providing a weak, continuous connection to either 3.3 V (pull-up) or GND (pull-down), establishing a clear resting state that noise cannot overcome.</p>

<h2>How a Pull-Up Resistor Works</h2>
<p>A pull-up resistor connects the GPIO pin to the supply voltage (3.3 V on ESP32) through a resistor:</p>
<div class="code-block">
  <div class="code-bar"><span>Pull-Up Circuit</span><button class="copy-btn">Copy</button></div>
  <pre>  3.3V ──── 10kΩ ──── GPIO pin ──── Button ──── GND

Resting state (button open):  pin = HIGH (3.3V via resistor)
Active state (button closed):  pin = LOW  (shorted to GND)
→ Active-LOW logic</pre>
</div>
<p>When the button is open, the resistor holds the pin at 3.3 V. When the button is pressed, it connects the pin directly to GND, overriding the resistor (0.33 mA flows through the 10 kΩ — harmless). The GPIO now reads LOW.</p>

<h2>How a Pull-Down Resistor Works</h2>
<div class="code-block">
  <div class="code-bar"><span>Pull-Down Circuit</span><button class="copy-btn">Copy</button></div>
  <pre>  3.3V ──── Button ──── GPIO pin ──── 10kΩ ──── GND

Resting state (button open):  pin = LOW  (GND via resistor)
Active state (button closed):  pin = HIGH (3.3V via button)
→ Active-HIGH logic</pre>
</div>
<p>Pull-downs are less common in ESP32 projects because the INPUT_PULLUP mode is the default convenience option. However, some sensors actively drive their output HIGH when triggered (PIR sensors, active-HIGH reed switches), where a pull-down keeps the idle state clean.</p>

<h2>Comparing Pull-Up vs Pull-Down</h2>
<table>
  <thead><tr><th>Feature</th><th>Pull-Up</th><th>Pull-Down</th></tr></thead>
  <tbody>
    <tr><td>Resting pin state</td><td>HIGH (3.3V)</td><td>LOW (GND)</td></tr>
    <tr><td>Button wired to</td><td>GND</td><td>3.3V</td></tr>
    <tr><td>Button pressed = </td><td>LOW (active-LOW)</td><td>HIGH (active-HIGH)</td></tr>
    <tr><td>ESP32 mode</td><td>INPUT_PULLUP</td><td>INPUT_PULLDOWN</td></tr>
    <tr><td>More common?</td><td>Yes ✓</td><td>Less common</td></tr>
    <tr><td>Used by default I2C</td><td>Yes (SDA, SCL)</td><td>No</td></tr>
  </tbody>
</table>

<h2>Internal vs External Resistors</h2>
<p>ESP32 has built-in pull-up and pull-down resistors accessible through software. Here is when to use each:</p>
<table>
  <thead><tr><th>Scenario</th><th>Use Internal?</th><th>Use External?</th></tr></thead>
  <tbody>
    <tr><td>Button on short wire (&lt;15 cm)</td><td>Yes ✓</td><td>Optional</td></tr>
    <tr><td>Button on long wire (&gt;30 cm)</td><td>No — too weak</td><td>Yes (10 kΩ)</td></tr>
    <tr><td>Industrial/noisy environment</td><td>No</td><td>Yes (4.7 kΩ)</td></tr>
    <tr><td>GPIO34–GPIO39 (no internal)</td><td>N/A</td><td>Required</td></tr>
    <tr><td>I2C bus (SDA/SCL)</td><td>Not recommended</td><td>Yes (4.7 kΩ)</td></tr>
    <tr><td>Battery-powered, low power</td><td>Yes ✓</td><td>Higher value (100 kΩ)</td></tr>
  </tbody>
</table>

<h2>Using Internal Pull Resistors in Code</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>void setup() {
  Serial.begin(115200);

  // Internal pull-up — pin rests HIGH, reads LOW when button pressed to GND
  pinMode(16, INPUT_PULLUP);

  // Internal pull-down — pin rests LOW, reads HIGH when button pressed to 3.3V
  pinMode(17, INPUT_PULLDOWN);
}

void loop() {
  int p16 = digitalRead(16);  // LOW = button pressed (active-LOW)
  int p17 = digitalRead(17);  // HIGH = button pressed (active-HIGH)

  Serial.printf("P16=%d (active-LOW)  P17=%d (active-HIGH)\n", p16, p17);
  delay(200);
}</pre>
</div>

<h2>External Pull Resistor Wiring</h2>
<p>For a 10 kΩ external pull-up:</p>
<table>
  <thead><tr><th>Connection Point</th><th>Connects To</th></tr></thead>
  <tbody>
    <tr><td>Resistor leg 1</td><td>ESP32 3.3V</td></tr>
    <tr><td>Resistor leg 2</td><td>ESP32 GPIO pin AND button terminal A</td></tr>
    <tr><td>Button terminal B</td><td>ESP32 GND</td></tr>
  </tbody>
</table>
<p>In code use plain <code>INPUT</code> mode (not INPUT_PULLUP) because the resistor is external:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>// External 10kΩ pull-up wired on breadboard
void setup() {
  Serial.begin(115200);
  pinMode(34, INPUT);   // GPIO34: input-only, needs external resistor
}

void loop() {
  Serial.printf("GPIO34 = %d\n", digitalRead(34));
  delay(200);
}</pre>
</div>

<h2>Power Consumption Considerations</h2>
<p>Pull resistors consume a small continuous current whenever the button is pressed (or whenever the logic is in the opposite state to the rail):</p>
<div class="code-block">
  <div class="code-bar"><span>Current Calculation</span><button class="copy-btn">Copy</button></div>
  <pre>External 10kΩ pull-up, button pressed (pin shorted to GND):
I = 3.3V / 10,000Ω = 0.33 mA

External 10kΩ pull-up, button released (no current from GPIO):
I ≈ 0 mA (tiny leakage only)

Internal ~47kΩ pull-up, button pressed:
I = 3.3V / 47,000Ω = 0.07 mA

For battery-powered designs: use higher value external resistors (47kΩ–100kΩ)
or enable internal pull-ups only when actively reading the button.</pre>
</div>

<h2>Pull Resistors and I2C</h2>
<p>I2C buses (SDA and SCL lines) always require pull-up resistors on the bus lines. Internal pull-ups are too weak (~47 kΩ) for reliable I2C communication. Use 4.7 kΩ external pull-ups to 3.3 V on both SDA and SCL. Many I2C breakout boards (BME280, SSD1306, etc.) include these resistors on-board, so check the datasheet before adding more.</p>

<h2>Troubleshooting Pull Resistor Problems</h2>
<ul>
  <li><strong>Random readings with button not pressed:</strong> The pull resistor is missing or too weak. Add or lower the resistor value.</li>
  <li><strong>Button press not detected:</strong> The pull-down resistor is fighting the signal. Check wiring orientation.</li>
  <li><strong>Inverted logic:</strong> You used INPUT_PULLUP but code checks for HIGH. Change to check for LOW (active-LOW).</li>
  <li><strong>GPIO34 always floats:</strong> No internal pull available — add a physical 10 kΩ resistor to 3.3 V.</li>
</ul>

<h2>Summary</h2>
<p>Pull-up and pull-down resistors define the resting state of a GPIO input and prevent the floating pin problem. Use INPUT_PULLUP (active-LOW, button to GND) for most buttons. Use INPUT_PULLDOWN (active-HIGH, button to 3.3V) when the signal naturally drives HIGH. Add external 10 kΩ resistors for long wires, noisy environments, and input-only GPIO34–GPIO39 pins.</p>
BODY,
],

/* ─── Guide 4: Reading Buttons ─── */
[
  'slug'      => 'reading-buttons-esp32',
  'title'     => 'Reading Buttons on ESP32: Wiring, Code, and Projects',
  'meta_desc' => 'Learn how to read button inputs on ESP32 — wiring normally-open switches, active-LOW vs active-HIGH logic, debouncing, toggle buttons, and complete Arduino code.',
  'read_time' => '13 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['debouncing-buttons-esp32','pull-up-pull-down-resistors','digital-inputs-esp32','driving-leds-esp32'],
  'faqs'      => [
    ['q'=>'How do I wire a push button to ESP32?','a'=>'The simplest wiring: connect one button terminal to a GPIO pin and the other to GND. In code, use pinMode(pin, INPUT_PULLUP). The pin reads HIGH by default and LOW when the button is pressed (active-LOW logic). No external resistor is needed.'],
    ['q'=>'What is active-LOW vs active-HIGH button logic?','a'=>'Active-LOW means the button press drives the pin to LOW (GND). With INPUT_PULLUP and button wired to GND, pressing the button gives LOW. Active-HIGH is the opposite — pin goes HIGH when pressed, using INPUT_PULLDOWN with button wired to 3.3V.'],
    ['q'=>'What is the difference between normally-open and normally-closed buttons?','a'=>'A normally-open (NO) button is open (disconnected) by default and closed (connected) when pressed. A normally-closed (NC) button is connected by default and opens when pressed. Most breadboard push buttons are normally-open.'],
    ['q'=>'Why does my button trigger multiple times for one press?','a'=>'This is button bounce — the mechanical contacts bounce open and closed several times within the first 5–50 ms of a press. The ESP32 is fast enough to read each bounce as a separate press. Fix this with debouncing: either a 10–100 ms delay or the millis() timing method.'],
    ['q'=>'Can I read a button press without using delay()?','a'=>'Yes — use the millis() debouncing method. Record the time of the last state change, and only register a new press if at least 50 ms have passed since the last change. This keeps the loop() running freely while still detecting clean button presses.'],
    ['q'=>'How do I detect a button toggle (press to turn on, press again to turn off)?','a'=>'Use a state variable. When a button press is detected (and debounced), flip a boolean: toggleState = !toggleState. Then control your output based on toggleState, not the raw button reading.'],
    ['q'=>'Can I read a button connected to GPIO34 on ESP32?','a'=>'Yes, but GPIO34 (and GPIO35, GPIO36, GPIO39) have no internal pull resistors. You must add an external 10 kΩ pull-up resistor between GPIO34 and 3.3V, then use pinMode(34, INPUT) in code.'],
    ['q'=>'How do I detect a long press vs a short press?','a'=>'Record millis() when the button goes LOW. When the button is released (goes HIGH), compare the elapsed time to a threshold (e.g. 1000 ms). If elapsed >= 1000 ms it is a long press; otherwise short press.'],
    ['q'=>'How many buttons can I connect to ESP32 simultaneously?','a'=>'Up to 34 buttons (one per GPIO), though practically you would use GPIO4, GPIO13–GPIO14, GPIO16–GPIO19, GPIO21–GPIO23, GPIO25–GPIO27, GPIO32–GPIO35 for reliable input. For more buttons, use a shift register (74HC165) or I2C expander (PCF8574).'],
    ['q'=>'Should I use interrupts or polling for reading buttons?','a'=>'For buttons in a simple loop, polling with millis() debouncing is simpler and reliable. Use interrupts only when the press must be detected even while the main loop is blocked (e.g. during a long computation or HTTP request). Most button projects work fine with polling.'],
  ],
  'body_html' => <<<'BODY'
<h2>Button Types and Terminology</h2>
<p>Before writing a single line of code, understanding button mechanics prevents many common mistakes. The push buttons used on breadboards are typically <strong>momentary tactile switches</strong>: they connect the circuit only while you hold them. Two subtypes exist:</p>
<ul>
  <li><strong>Normally Open (NO):</strong> Circuit is open (disconnected) at rest, closes when pressed. This is the standard breadboard button.</li>
  <li><strong>Normally Closed (NC):</strong> Circuit is closed at rest, opens when pressed. Used in safety applications (detecting a door opening breaks the circuit).</li>
</ul>
<p>Most of this guide uses normally-open buttons, which are by far the most common in ESP32 projects.</p>

<h2>Wiring a Button to ESP32 (Active-LOW)</h2>
<p>The simplest and most robust approach uses <code>INPUT_PULLUP</code> — no extra resistor needed:</p>
<table>
  <thead><tr><th>Button Terminal</th><th>Connect To</th></tr></thead>
  <tbody>
    <tr><td>Terminal A</td><td>ESP32 GPIO16</td></tr>
    <tr><td>Terminal B</td><td>ESP32 GND</td></tr>
  </tbody>
</table>
<p>With <code>INPUT_PULLUP</code> the pin reads HIGH at rest (3.3V via internal resistor). Pressing the button shorts the pin to GND → reads LOW. This is <strong>active-LOW logic</strong>: LOW means pressed.</p>

<h2>Basic Button Read — Complete Code</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16
#define LED_PIN     2

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);   // HIGH at rest, LOW when pressed
  pinMode(LED_PIN,    OUTPUT);
  Serial.println("Button demo — press the button!");
}

void loop() {
  int state = digitalRead(BUTTON_PIN);

  if (state == LOW) {              // Active-LOW: LOW = pressed
    digitalWrite(LED_PIN, HIGH);
    Serial.println("PRESSED");
  } else {
    digitalWrite(LED_PIN, LOW);
    // Serial.println("released");  // Comment out to reduce Serial spam
  }
  delay(20);   // Small delay reduces Serial flood
}</pre>
</div>

<h2>Active-HIGH Wiring (Alternative)</h2>
<p>If your circuit naturally drives the GPIO HIGH when triggered (like some sensors), use INPUT_PULLDOWN:</p>
<table>
  <thead><tr><th>Button Terminal</th><th>Connect To</th></tr></thead>
  <tbody>
    <tr><td>Terminal A</td><td>ESP32 3.3V</td></tr>
    <tr><td>Terminal B</td><td>ESP32 GPIO17</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 17

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLDOWN);  // LOW at rest, HIGH when pressed
}

void loop() {
  if (digitalRead(BUTTON_PIN) == HIGH) {  // HIGH = pressed (active-HIGH)
    Serial.println("PRESSED (active-HIGH)");
  }
  delay(20);
}</pre>
</div>

<h2>Toggle Button: On/Off Control</h2>
<p>Many projects need a button that toggles a state rather than holding it active. The key is detecting only the falling edge (button going from HIGH to LOW):</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16
#define LED_PIN     2

bool ledState    = false;
bool lastState   = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN,    OUTPUT);
}

void loop() {
  bool current = digitalRead(BUTTON_PIN);

  // Detect falling edge: was HIGH, now LOW
  if (lastState == HIGH && current == LOW) {
    ledState = !ledState;                       // Toggle
    digitalWrite(LED_PIN, ledState);
    Serial.printf("LED toggled %s\n", ledState ? "ON" : "OFF");
    delay(50);                                  // Simple debounce
  }

  lastState = current;
  delay(10);
}</pre>
</div>

<h2>Detecting Short vs Long Press</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN  16
#define LONG_MS   1000   // 1 second threshold

unsigned long pressStart = 0;
bool pressing = false;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  bool current = (digitalRead(BUTTON_PIN) == LOW);

  if (current && !pressing) {          // Button just pressed
    pressing   = true;
    pressStart = millis();
  }

  if (!current && pressing) {          // Button just released
    pressing = false;
    unsigned long held = millis() - pressStart;
    if (held >= LONG_MS) {
      Serial.printf("LONG PRESS (%lu ms)\n", held);
    } else {
      Serial.printf("SHORT PRESS (%lu ms)\n", held);
    }
  }
  delay(10);
}</pre>
</div>

<h2>Multiple Buttons with Array Management</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>const int BTNS[]    = {16, 17, 18, 19};
const int LEDS[]    = { 2, 13, 14, 27};
const int N         = 4;
bool prevState[N];

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) {
    pinMode(BTNS[i], INPUT_PULLUP);
    pinMode(LEDS[i], OUTPUT);
    prevState[i] = HIGH;
  }
}

void loop() {
  for (int i = 0; i < N; i++) {
    bool cur = digitalRead(BTNS[i]);
    if (prevState[i] == HIGH && cur == LOW) {   // Falling edge
      digitalWrite(LEDS[i], !digitalRead(LEDS[i]));  // Toggle LED
      Serial.printf("Button %d toggled LED %d\n", i+1, i+1);
      delay(50);
    }
    prevState[i] = cur;
  }
  delay(5);
}</pre>
</div>

<h2>Reading a Normally-Closed Button</h2>
<p>NC buttons invert the logic. With INPUT_PULLUP and an NC button wired between GPIO and GND:</p>
<ul>
  <li><strong>Button at rest (NC = connected):</strong> Pin is shorted to GND → reads LOW (pressed appearance)</li>
  <li><strong>Button pressed (NC opens):</strong> Pin pulled HIGH by resistor → reads HIGH (released appearance)</li>
</ul>
<p>Simply invert your comparison: <code>if (digitalRead(pin) == HIGH)</code> to detect the NC button being pressed (opened).</p>

<h2>Project: Morse Code Tapper</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16
#define BUZZ_PIN   25
#define DOT_MS    100
#define DASH_MS   300

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZ_PIN,   OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    unsigned long start = millis();
    tone(BUZZ_PIN, 800);            // Start tone
    while (digitalRead(BUTTON_PIN) == LOW);   // Wait for release
    tone(BUZZ_PIN, 0);              // Stop tone
    unsigned long held = millis() - start;
    Serial.print(held >= DASH_MS ? "-" : ".");
    delay(50);
  }
}</pre>
</div>

<h2>Summary</h2>
<p>Reading buttons on ESP32 boils down to: use INPUT_PULLUP with button wired to GND for the most reliable active-LOW setup, detect falling edges for clean toggle logic, measure press duration for short/long press differentiation, and add 50 ms of debounce delay to eliminate contact bounce. For more advanced debounce techniques, see the next guide on debouncing buttons.</p>
BODY,
],

/* ─── Guide 5: Debouncing Buttons ─── */
[
  'slug'      => 'debouncing-buttons-esp32',
  'title'     => 'Debouncing Buttons on ESP32: Software and Hardware Methods',
  'meta_desc' => 'Fix button bounce on ESP32 — learn software debouncing with millis(), the Bounce2 library, hardware RC debounce circuits, and interrupt-safe debouncing.',
  'read_time' => '13 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['reading-buttons-esp32','digital-inputs-esp32','pull-up-pull-down-resistors'],
  'faqs'      => [
    ['q'=>'What is button bounce and why does it cause problems?','a'=>'Button bounce is the rapid make-and-break of mechanical contacts when a switch is pressed or released. A button can bounce 5–50 times in the first 5–50 ms, and ESP32 reads each bounce as a separate press event. For a counter or toggle, this means one press registers as multiple events.'],
    ['q'=>'What is the simplest software debounce method?','a'=>'Add delay(50) after detecting a button press and before reading the state again. While this works, it blocks the main loop for 50 ms. The millis() debounce method is better because it is non-blocking.'],
    ['q'=>'How does millis() debouncing work?','a'=>'Record the time (millis()) when the button state first changes. Only accept the change as valid if the button has been in the new state for longer than the debounce threshold (typically 20–50 ms). This prevents counting rapid bounces as separate events.'],
    ['q'=>'What is the Bounce2 library and how do I use it on ESP32?','a'=>'Bounce2 is a lightweight Arduino library that handles button debouncing transparently. Install it via Arduino Library Manager, include Bounce2.h, create a Bounce object per button, call update() in loop(), then use rose() for a rising edge and fell() for a falling edge.'],
    ['q'=>'What are hardware debounce circuits?','a'=>'Hardware debounce uses an RC filter (resistor + capacitor) to slow down the signal transition, smoothing out the bounce. A 10 kΩ resistor and 100 nF capacitor give a time constant of 1 ms, which is enough for most switches. Schmitt-trigger inputs (like the 74HC14) can further clean the signal.'],
    ['q'=>'What debounce threshold time should I use?','a'=>'For most tactile push buttons, 20–50 ms is sufficient. Cheap buttons or microswitches may need up to 100 ms. Membrane keyboards often need only 5–10 ms. If in doubt, start with 50 ms and reduce if input feels sluggish.'],
    ['q'=>'Can I debounce a button connected via interrupt on ESP32?','a'=>'Yes. The safest method is to trigger the interrupt on the falling edge, record the time in the ISR, and ignore subsequent interrupts that arrive within the debounce window. A volatile timestamp variable shared between ISR and main loop handles this.'],
    ['q'=>'Does software debouncing work for encoder wheels?','a'=>'Rotary encoders require much faster debounce logic (microseconds rather than milliseconds) and it is better to use hardware debounce (RC filter + Schmitt trigger) or a dedicated encoder IC. Software millis() debounce is too slow for fast encoder rotation.'],
    ['q'=>'How do I debounce multiple buttons at once?','a'=>'Use an array of Debouncer objects from the Bounce2 library, or maintain a separate lastTime[] and lastState[] array per button and apply the same millis() logic to each. Both methods scale cleanly to 4, 8, or more buttons.'],
    ['q'=>'Is there any case where I should NOT debounce a button?','a'=>'Yes — if using the button as a manual signal where the user holds it down and you only care about the held state (not the press event), debouncing adds unnecessary delay. Also for capacitive touch sensors, which have no mechanical bounce.'],
  ],
  'body_html' => <<<'BODY'
<h2>What is Button Bounce?</h2>
<p>When you press a mechanical push button, the metal contacts do not make a clean, single connection. Instead, they bounce open and closed multiple times within the first few milliseconds due to their physical elasticity. A high-speed oscilloscope will show 5–50 transitions within the first 5–50 ms of a button press.</p>
<p>This is completely invisible to a human finger, but ESP32 running at 240 MHz can read each bounce as a separate event. Press a button once and your counter may jump by 3 or 7. This is button bounce — and debouncing is the solution.</p>

<h2>Visualising Bounce on the Serial Monitor</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Shows raw bouncing</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16

int pressCount = 0;
bool lastState = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("Counting raw presses (no debounce):");
}

void loop() {
  bool current = digitalRead(BUTTON_PIN);
  if (lastState == HIGH && current == LOW) {  // Falling edge
    pressCount++;
    Serial.printf("Press #%d detected\n", pressCount);
  }
  lastState = current;
  // No delay — catches every bounce
}</pre>
</div>
<p>Press the button once. You will likely see 2–6 "presses" registered. Run this first to confirm bounce is the problem, then apply a fix.</p>

<h2>Method 1: Simple Delay Debounce</h2>
<p>The naïve fix: after detecting a press, wait 50 ms and then continue. Simple but blocks the loop:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN 16
#define DEBOUNCE_MS 50

int count = 0;
bool lastState = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  bool current = digitalRead(BUTTON_PIN);
  if (lastState == HIGH && current == LOW) {
    delay(DEBOUNCE_MS);                         // Wait for bounce to settle
    if (digitalRead(BUTTON_PIN) == LOW) {       // Still pressed after wait?
      count++;
      Serial.printf("Valid press #%d\n", count);
    }
  }
  lastState = current;
}</pre>
</div>
<p>This works but the 50 ms blocking period means the MCU cannot do anything else — bad for Wi-Fi, sensor polling, or OLED updates happening in the same loop.</p>

<h2>Method 2: Non-Blocking millis() Debounce (Recommended)</h2>
<p>The millis() method records the time of the last state change and only accepts a new state after the debounce window has elapsed. The loop remains unblocked:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN  16
#define LED_PIN      2
#define DEBOUNCE_MS 50

bool buttonState    = HIGH;   // Current debounced state
bool lastRawState   = HIGH;   // Last raw reading
unsigned long lastChangeTime = 0;
int pressCount = 0;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN,    OUTPUT);
}

void loop() {
  bool rawReading = digitalRead(BUTTON_PIN);

  if (rawReading != lastRawState) {       // State changed
    lastChangeTime = millis();            // Reset timer
    lastRawState   = rawReading;
  }

  if ((millis() - lastChangeTime) > DEBOUNCE_MS) {
    if (rawReading != buttonState) {      // Stable new state
      buttonState = rawReading;
      if (buttonState == LOW) {           // Debounced press event
        pressCount++;
        Serial.printf("Debounced press #%d\n", pressCount);
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
      }
    }
  }

  // Loop free to do other work here — no blocking
}</pre>
</div>

<h2>Method 3: The Bounce2 Library</h2>
<p>The <a href="https://github.com/thomasfredericks/Bounce2">Bounce2 library</a> encapsulates debouncing logic cleanly. Install it from the Arduino Library Manager (Sketch → Include Library → Manage Libraries → search "Bounce2").</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Bounce2 library</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;Bounce2.h&gt;

#define BUTTON_PIN 16
#define LED_PIN     2

Bounce debouncer;   // One instance per button

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  debouncer.attach(BUTTON_PIN, INPUT_PULLUP);
  debouncer.interval(25);   // 25 ms debounce window
}

void loop() {
  debouncer.update();   // Must call every loop iteration

  if (debouncer.fell()) {     // Falling edge = button pressed
    Serial.println("Button fell (pressed)");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
  if (debouncer.rose()) {     // Rising edge = button released
    Serial.println("Button rose (released)");
  }
}</pre>
</div>

<h2>Multiple Buttons with Bounce2</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;Bounce2.h&gt;

const int BTNS[] = {16, 17, 18};
const int LEDS[] = { 2, 13, 14};
const int N      = 3;
Bounce debouncers[N];

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) {
    debouncers[i].attach(BTNS[i], INPUT_PULLUP);
    debouncers[i].interval(25);
    pinMode(LEDS[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < N; i++) {
    debouncers[i].update();
    if (debouncers[i].fell()) {
      Serial.printf("Button %d pressed\n", i + 1);
      digitalWrite(LEDS[i], !digitalRead(LEDS[i]));
    }
  }
}</pre>
</div>

<h2>Method 4: Hardware RC Debounce Circuit</h2>
<p>Hardware debouncing uses a resistor-capacitor (RC) filter to slow down the signal edge, smearing the bounces into a single clean transition:</p>
<div class="code-block">
  <div class="code-bar"><span>RC Debounce Circuit</span><button class="copy-btn">Copy</button></div>
  <pre>3.3V ──── 10kΩ (pull-up) ──── GPIO pin
                               |
                            100nF cap
                               |
Button ────────────────────── GND

Time constant τ = R × C = 10,000 × 0.0000001 = 1 ms

Bounce spikes &lt;1ms are smoothed. Only sustained state change passes through.
No software debounce needed — use plain INPUT mode in code.</pre>
</div>
<table>
  <thead><tr><th>Method</th><th>Complexity</th><th>Blocks Loop?</th><th>Best For</th></tr></thead>
  <tbody>
    <tr><td>delay() debounce</td><td>Simplest</td><td>Yes</td><td>Quick prototypes</td></tr>
    <tr><td>millis() debounce</td><td>Medium</td><td>No</td><td>Most projects</td></tr>
    <tr><td>Bounce2 library</td><td>Medium</td><td>No</td><td>Multiple buttons</td></tr>
    <tr><td>Hardware RC</td><td>Hardware</td><td>No</td><td>Noisy environments</td></tr>
  </tbody>
</table>

<h2>Interrupt-Safe Debouncing</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define BUTTON_PIN  16
#define DEBOUNCE_US 50000   // 50 ms in microseconds

volatile unsigned long lastISRTime = 0;
volatile int pressCnt = 0;

void IRAM_ATTR onPress() {
  unsigned long now = micros();
  if (now - lastISRTime > DEBOUNCE_US) {
    pressCnt++;
    lastISRTime = now;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onPress, FALLING);
}

void loop() {
  static int last = 0;
  if (pressCnt != last) {
    last = pressCnt;
    Serial.printf("Interrupt count (debounced): %d\n", pressCnt);
  }
}</pre>
</div>

<h2>Choosing the Right Debounce Time</h2>
<table>
  <thead><tr><th>Switch Type</th><th>Recommended Debounce</th></tr></thead>
  <tbody>
    <tr><td>Cheap tactile button</td><td>50 ms</td></tr>
    <tr><td>Quality tactile switch</td><td>20–25 ms</td></tr>
    <tr><td>Membrane keypad</td><td>5–10 ms</td></tr>
    <tr><td>Reed switch</td><td>50–100 ms</td></tr>
    <tr><td>Limit switch / microswitch</td><td>20–50 ms</td></tr>
    <tr><td>Capacitive touch sensor</td><td>None needed</td></tr>
  </tbody>
</table>

<h2>Summary</h2>
<p>Button bounce causes one physical press to register as multiple software events because mechanical contacts oscillate rapidly. For most projects, the non-blocking millis() method (50 ms window) or the Bounce2 library are the best solutions — clean, reliable, and loop-friendly. Hardware RC debounce is ideal when code simplicity matters or for input-only GPIO34–GPIO39 pins where you want zero software overhead.</p>
BODY,
],

]; // end return
