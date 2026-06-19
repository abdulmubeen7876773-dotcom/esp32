<?php
/* ESP32 Engine — Phase 3 Guide Data (Guides 6–10): GPIO & Hardware */
return [

/* ─── Guide 6: Driving LEDs ─── */
[
  'slug'      => 'driving-leds-esp32',
  'title'     => 'Driving LEDs with ESP32: Resistors, PWM, RGB, and NeoPixels',
  'meta_desc' => 'Complete guide to driving LEDs with ESP32 — calculate resistor values, control brightness with PWM (LEDC), drive RGB LEDs, and use WS2812B NeoPixels.',
  'read_time' => '14 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['digital-outputs-esp32','using-relays-safely-esp32','reading-analog-signals-esp32','adc-explained-esp32'],
  'faqs'      => [
    ['q'=>'How do I calculate the correct resistor for an LED with ESP32?','a'=>'Use R = (Vsupply - Vf) / If. For a red LED (Vf=2V, If=20mA) on 3.3V: R = (3.3 - 2.0) / 0.020 = 65Ω. Round up to 68Ω or 100Ω. For blue/white LEDs (Vf=3.2V), reduce current to 5–10mA to stay in the comfortable 100–200Ω range.'],
    ['q'=>'How do I control LED brightness on ESP32?','a'=>'Use the LEDC (LED Controller) hardware peripheral. Call ledcSetup(channel, frequency, resolution) to configure the channel, ledcAttachPin(pin, channel) to bind the GPIO, then ledcWrite(channel, dutyCycle) where duty cycle ranges from 0 (off) to 2^resolution-1 (full brightness).'],
    ['q'=>'Can I use analogWrite() on ESP32 like Arduino?','a'=>'ESP32 with newer Arduino core (3.x) supports analogWrite(pin, value) where value is 0–255. On older cores (2.x) you must use the LEDC functions directly. The LEDC approach gives more control over frequency and resolution, so it is always preferred.'],
    ['q'=>'How many LEDs can I connect directly to ESP32 GPIO pins?','a'=>'Each GPIO can source/sink 12 mA safely (40 mA max). A standard LED draws 5–20 mA. You could drive 20+ LEDs from individual GPIO pins within current limits, but total chip current across all GPIOs should stay under 1200 mA. For many LEDs, use a shift register or dedicated LED driver IC.'],
    ['q'=>'How do I control an RGB LED with ESP32?','a'=>'An RGB LED has four pins: one common (anode or cathode) and three color pins (R, G, B). Use three GPIO pins with LEDC PWM on each channel. ledcWrite(R_channel, 255) sets red full brightness. Mixing values creates any color in the 16-million-color 24-bit space.'],
    ['q'=>'What is a WS2812B NeoPixel and how is it different from a regular LED?','a'=>'WS2812B (NeoPixel) LEDs have a built-in controller chip. They are controlled via a single-wire serial protocol, and you can chain hundreds together on one GPIO. Each LED stores its own color value. Use the Adafruit NeoPixel or FastLED library with the ESP32 to drive them.'],
    ['q'=>'What frequency should I use for LED PWM on ESP32?','a'=>'For LED dimming, 1 kHz is standard and well above the 50 Hz flicker threshold visible to the human eye. For motor or audio PWM you may need 25–50 kHz. Use 5000 Hz (5 kHz) as a safe default: ledcSetup(0, 5000, 8) gives 8-bit resolution at 5 kHz.'],
    ['q'=>'Can I connect a 5V LED strip directly to ESP32?','a'=>'No — 5V LED strips run at 5V and typically draw much more current than a GPIO can provide. Power the strip from a 5V supply (USB or regulator), connect the strip GND to ESP32 GND, and control the strip via a logic-level MOSFET (e.g. IRLZ44N) driven by a PWM GPIO.'],
    ['q'=>'Why does my LED flicker with ESP32 PWM?','a'=>'Common causes: PWM frequency too low (below 100 Hz is visible flicker — increase to 1 kHz+), duty cycle at 0 briefly during PWM reconfiguration, or power supply noise. Also, some phones cameras show flicker due to their rolling shutter interacting with the PWM frequency — this is camera artifact, not real flicker.'],
    ['q'=>'How do I fade an LED smoothly from off to full brightness?','a'=>'Use a for loop incrementing the LEDC duty cycle from 0 to the maximum value (e.g. 255 for 8-bit resolution) with a short delay between steps. For a 1-second fade: step every 4 ms (256 steps × 4 ms = ~1 second).'],
  ],
  'body_html' => <<<'BODY'
<h2>LED Basics and Why Resistors are Mandatory</h2>
<p>An LED (Light Emitting Diode) has no internal current limiting. Without a resistor, Ohm's law gives infinite current through a forward-biased diode until it burns out — typically in under a second. Every LED circuit must include a current-limiting resistor between the GPIO pin and the LED anode (positive leg).</p>
<p>LEDs have two important parameters: forward voltage (Vf) — the voltage drop across the LED when conducting — and forward current (If) — the current needed for the desired brightness.</p>
<table>
  <thead><tr><th>LED Color</th><th>Typical Vf</th><th>Recommended If</th><th>Resistor (3.3V supply)</th></tr></thead>
  <tbody>
    <tr><td>Red</td><td>1.8–2.2 V</td><td>10–20 mA</td><td>68–150 Ω</td></tr>
    <tr><td>Yellow / Orange</td><td>2.0–2.2 V</td><td>10–20 mA</td><td>56–130 Ω</td></tr>
    <tr><td>Green</td><td>2.0–3.0 V</td><td>10–20 mA</td><td>15–130 Ω</td></tr>
    <tr><td>Blue</td><td>3.0–3.4 V</td><td>5–10 mA</td><td>0–33 Ω (use 33 Ω min)</td></tr>
    <tr><td>White</td><td>3.0–3.4 V</td><td>5–10 mA</td><td>0–33 Ω (use 33 Ω min)</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Resistor Formula</span><button class="copy-btn">Copy</button></div>
  <pre>R = (Vsupply - Vf) / If

Red LED on 3.3V at 15 mA:
R = (3.3 - 2.0) / 0.015 = 86.7 Ω → use 100 Ω

Blue LED on 3.3V at 8 mA:
R = (3.3 - 3.2) / 0.008 = 12.5 Ω → use 33 Ω (safer margin)</pre>
</div>

<h2>Simple LED Wiring</h2>
<table>
  <thead><tr><th>Component</th><th>Connection</th></tr></thead>
  <tbody>
    <tr><td>LED Anode (+) long leg</td><td>100 Ω resistor → ESP32 GPIO</td></tr>
    <tr><td>LED Cathode (–) short leg</td><td>ESP32 GND</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Basic LED blink</span><button class="copy-btn">Copy</button></div>
  <pre>#define LED_PIN 16

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);   // LED on
  delay(500);
  digitalWrite(LED_PIN, LOW);    // LED off
  delay(500);
}</pre>
</div>

<h2>PWM Brightness Control with LEDC</h2>
<p>ESP32 has a dedicated LEDC peripheral with 16 channels capable of high-frequency PWM. This is the correct way to control LED brightness:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — LEDC fade</span><button class="copy-btn">Copy</button></div>
  <pre>#define LED_PIN  16
#define CHANNEL   0
#define FREQ   5000    // 5 kHz
#define BITS      8    // 8-bit → 0–255

void setup() {
  ledcSetup(CHANNEL, FREQ, BITS);   // Configure channel
  ledcAttachPin(LED_PIN, CHANNEL);  // Bind GPIO to channel
}

void loop() {
  // Fade in
  for (int duty = 0; duty <= 255; duty++) {
    ledcWrite(CHANNEL, duty);
    delay(8);   // 256 steps × 8ms ≈ 2 second fade
  }
  // Fade out
  for (int duty = 255; duty >= 0; duty--) {
    ledcWrite(CHANNEL, duty);
    delay(8);
  }
}</pre>
</div>

<h2>RGB LED Control</h2>
<p>A common-cathode RGB LED has 4 pins: GND (common), R, G, B. Connect each color pin through a 100 Ω resistor to a separate GPIO. Use LEDC on all three channels for full color mixing:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — RGB LED full color</span><button class="copy-btn">Copy</button></div>
  <pre>#define R_PIN 16
#define G_PIN 17
#define B_PIN 18

void setupLEDC(int pin, int ch) {
  ledcSetup(ch, 5000, 8);
  ledcAttachPin(pin, ch);
}

void setColor(int r, int g, int b) {
  ledcWrite(0, r);   // R channel
  ledcWrite(1, g);   // G channel
  ledcWrite(2, b);   // B channel
}

void setup() {
  setupLEDC(R_PIN, 0);
  setupLEDC(G_PIN, 1);
  setupLEDC(B_PIN, 2);
}

void loop() {
  setColor(255,   0,   0);  delay(1000);  // Red
  setColor(  0, 255,   0);  delay(1000);  // Green
  setColor(  0,   0, 255);  delay(1000);  // Blue
  setColor(255, 100,   0);  delay(1000);  // Orange
  setColor(128,   0, 128);  delay(1000);  // Purple
  setColor(255, 255, 255);  delay(1000);  // White
  setColor(  0,   0,   0);  delay(500);   // Off
}</pre>
</div>

<h2>WS2812B NeoPixel LEDs</h2>
<p>NeoPixels are individually addressable RGB LEDs with a built-in driver chip. One GPIO pin can control a strip of 60, 100, or even 300 LEDs via a high-speed serial protocol. Install the <strong>Adafruit NeoPixel</strong> library from the Arduino Library Manager.</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — NeoPixel rainbow</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;Adafruit_NeoPixel.h&gt;

#define LED_PIN    16
#define NUM_LEDS   12   // Number of pixels in strip

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(80);   // 0–255, limit for power safety
  strip.show();
}

void loop() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));  // Red
    strip.show();
    delay(50);
    strip.setPixelColor(i, strip.Color(0, 0, 0));    // Off
  }
}</pre>
</div>
<p><strong>Power note:</strong> Each WS2812B LED can draw up to 60 mA at full white. A strip of 30 LEDs = 1.8 A. Always power LED strips from a dedicated 5V supply, not from the ESP32 5V pin.</p>

<h2>Driving High-Power LEDs via MOSFET</h2>
<div class="code-block">
  <div class="code-bar"><span>MOSFET LED Driver Circuit</span><button class="copy-btn">Copy</button></div>
  <pre>12V LED strip (+) ──── 12V PSU (+)
12V LED strip (–) ──── MOSFET Drain (IRLZ44N)
MOSFET Source ──── GND (common with ESP32 GND)
ESP32 GPIO16 ──── 10kΩ ──── MOSFET Gate

Use PWM on GPIO16 to dim a 12V LED strip via IRLZ44N logic-level MOSFET.
IRLZ44N can handle 47A — vast overkill, but it runs cool at low currents.</pre>
</div>

<h2>Summary</h2>
<p>Always use a current-limiting resistor with individual LEDs. Use the LEDC peripheral (ledcSetup / ledcAttachPin / ledcWrite) for smooth brightness control. Drive RGB LEDs with three LEDC channels for 16 million colors. For addressable strips, use the Adafruit NeoPixel or FastLED library. Power any high-current load from a separate supply, not the GPIO pin.</p>
BODY,
],

/* ─── Guide 7: Using Relays Safely ─── */
[
  'slug'      => 'using-relays-safely-esp32',
  'title'     => 'Using Relays Safely with ESP32: Wiring, Code, and AC Safety',
  'meta_desc' => 'Learn to control relays with ESP32 safely — understand relay modules, flyback diodes, 3.3V logic compatibility, active-LOW vs active-HIGH, and AC mains precautions.',
  'read_time' => '15 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['digital-outputs-esp32','driving-leds-esp32','digital-inputs-esp32'],
  'faqs'      => [
    ['q'=>'Can I connect a relay directly to an ESP32 GPIO pin?','a'=>'No. A bare relay coil draws 60–100 mA which exceeds the GPIO 40 mA maximum and will damage the ESP32. Always use a relay module with a built-in transistor driver, or add your own NPN transistor (2N2222 / BC547) between the GPIO and relay coil.'],
    ['q'=>'What is a flyback diode and why is it critical for relays?','a'=>'A relay coil is an inductor. When you switch it off, the collapsing magnetic field generates a voltage spike (back-EMF) that can be 10× the supply voltage. A flyback diode (1N4007) placed in reverse across the coil clamps this spike, protecting the transistor and ESP32. Quality relay modules include this diode.'],
    ['q'=>'What is the difference between active-LOW and active-HIGH relay modules?','a'=>'Active-LOW modules trigger the relay when the control pin is driven LOW (0V). Active-HIGH modules trigger on HIGH (3.3V or 5V). Most cheap relay modules are active-LOW. This means writing LOW to the GPIO activates the relay — which can be confusing. Check your module datasheet.'],
    ['q'=>'Are 5V relay modules compatible with ESP32?','a'=>'Most relay modules need 5V to power the coil but accept a 3.3V control signal on the IN pin. However, some modules use BJT transistors that need at least 3.3V on the base — which is the full output of ESP32. Test with a multimeter. If the relay does not trigger at 3.3V, add an external 5V-tolerant driver stage.'],
    ['q'=>'What is NO (Normally Open) vs NC (Normally Closed) on a relay?','a'=>'NO (Normally Open): load is disconnected when relay is off, connected when relay is ON. NC (Normally Closed): load is connected when relay is off, disconnected when relay is ON. NO is used for most switching applications. NC is used for fail-safe circuits where the load must be ON if the control loses power.'],
    ['q'=>'How do I safely switch AC mains with an ESP32 and relay?','a'=>'Use an optocoupler-isolated relay module (inputs fully isolated from AC side), work only with the relay terminal block disconnected from AC, never touch the AC wiring while powered, use enclosures that prevent accidental contact, follow local electrical codes, and consider hiring a licensed electrician for permanent AC installations.'],
    ['q'=>'How do I avoid the relay clicking at startup?','a'=>'Many relay modules are active-LOW: they energize when the control pin is LOW (which happens by default at GPIO boot). To prevent startup click, initialise the GPIO HIGH before setup(): use gpio_config() with pull-up in esp32 or call digitalWrite(RELAY_PIN, HIGH) as the very first line of setup() before pinMode().'],
    ['q'=>'Can I control multiple relays from one ESP32?','a'=>'Yes. Each relay module needs one GPIO pin. An 8-relay module board uses 8 GPIOs and a common power supply. Connect all IN pins to separate GPIOs, share the GND connection, and power the module from an external 5V source (not the ESP32 3.3V regulator, which cannot supply enough current for multiple coils).'],
    ['q'=>'What is the switching time of a typical relay?','a'=>'Electromechanical relays typically switch in 5–15 ms (coil energise time) and release in 3–10 ms. For faster switching (microseconds), use a solid-state relay (SSR) or a MOSFET. Relay modules are suitable for on/off control of AC loads, not for audio or fast PWM switching.'],
    ['q'=>'How do I add delay between relay activations to prevent inrush current issues?','a'=>'For motor or capacitive loads that draw high inrush current at startup, add 200–500 ms between activating multiple relays. This prevents simultaneous inrush from overloading your power supply. Use millis() timing rather than delay() to avoid blocking your main loop.'],
  ],
  'body_html' => <<<'BODY'
<h2>What is a Relay and Why Use One?</h2>
<p>A relay is an electrically operated switch. A small control current in the coil creates a magnetic field that mechanically moves a switch contact, connecting or disconnecting a much higher-power circuit. Relays let an ESP32 operating at 3.3V, 40 mA per pin safely switch 240V AC at 10A — a power ratio of 10,000:1.</p>
<p>Common relay applications with ESP32: smart home light switches, automatic irrigation valves, garage door openers, HVAC control, motorised blinds, and industrial solenoid control.</p>

<h2>Anatomy of a Relay Module</h2>
<p>Never use a bare relay with ESP32. Relay modules include the transistor driver, flyback diode, and status LED:</p>
<table>
  <thead><tr><th>Module Component</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td>Relay coil (5V)</td><td>Electromechanical switch actuator</td></tr>
    <tr><td>NPN transistor (driver)</td><td>Amplifies weak ESP32 signal to drive coil</td></tr>
    <tr><td>Flyback diode (1N4007)</td><td>Suppresses back-EMF voltage spike on coil off</td></tr>
    <tr><td>Optocoupler (better modules)</td><td>Fully isolates ESP32 ground from relay coil circuit</td></tr>
    <tr><td>Status LED</td><td>Visual indicator of relay state</td></tr>
    <tr><td>Screw terminals (COM, NO, NC)</td><td>Connection points for the switched load</td></tr>
  </tbody>
</table>

<h2>Relay Terminal Definitions</h2>
<table>
  <thead><tr><th>Terminal</th><th>Full Name</th><th>Behaviour</th></tr></thead>
  <tbody>
    <tr><td>COM</td><td>Common</td><td>Always connected — attach power line here</td></tr>
    <tr><td>NO</td><td>Normally Open</td><td>Open when relay OFF, closed when relay ON → load ON when relay ON</td></tr>
    <tr><td>NC</td><td>Normally Closed</td><td>Closed when relay OFF, open when relay ON → load OFF when relay ON</td></tr>
  </tbody>
</table>
<p>For a light switch: wire COM to live, NO to the lamp, and neutral directly to the lamp. When ESP32 activates the relay, the circuit completes and the lamp turns on.</p>

<h2>Wiring ESP32 to a Single Relay Module</h2>
<table>
  <thead><tr><th>Relay Module Pin</th><th>Connect To</th></tr></thead>
  <tbody>
    <tr><td>VCC</td><td>External 5V supply (or ESP32 VIN if powered by USB)</td></tr>
    <tr><td>GND</td><td>GND (common with ESP32)</td></tr>
    <tr><td>IN</td><td>ESP32 GPIO16</td></tr>
    <tr><td>COM</td><td>Load power supply positive</td></tr>
    <tr><td>NO</td><td>Load positive terminal</td></tr>
  </tbody>
</table>

<h2>Code: Active-LOW Relay (Most Common)</h2>
<p>Most relay modules are active-LOW: LOW on IN = relay ON, HIGH on IN = relay OFF.</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Active-LOW relay</span><button class="copy-btn">Copy</button></div>
  <pre>#define RELAY_PIN 16

void setup() {
  Serial.begin(115200);
  // Set HIGH FIRST to prevent relay click at startup
  digitalWrite(RELAY_PIN, HIGH);
  pinMode(RELAY_PIN, OUTPUT);
  Serial.println("Relay control ready");
}

void relayOn()  { digitalWrite(RELAY_PIN, LOW);  Serial.println("Relay ON"); }
void relayOff() { digitalWrite(RELAY_PIN, HIGH); Serial.println("Relay OFF"); }

void loop() {
  relayOn();
  delay(3000);   // Load ON for 3 seconds
  relayOff();
  delay(3000);   // Load OFF for 3 seconds
}</pre>
</div>

<h2>Code: Active-HIGH Relay</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Active-HIGH relay</span><button class="copy-btn">Copy</button></div>
  <pre>#define RELAY_PIN 16

void setup() {
  digitalWrite(RELAY_PIN, LOW);   // Ensure relay off at start
  pinMode(RELAY_PIN, OUTPUT);
  Serial.begin(115200);
}

void relayOn()  { digitalWrite(RELAY_PIN, HIGH); }
void relayOff() { digitalWrite(RELAY_PIN, LOW);  }

void loop() {
  Serial.println("Relay ON for 5 seconds");
  relayOn();  delay(5000);
  Serial.println("Relay OFF for 5 seconds");
  relayOff(); delay(5000);
}</pre>
</div>

<h2>Non-Blocking Relay Timer with millis()</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define RELAY_PIN   16
#define ON_DURATION  5000UL   // 5 seconds ON
#define OFF_DURATION 2000UL   // 2 seconds OFF

unsigned long lastChange = 0;
bool relayState = false;

void setup() {
  digitalWrite(RELAY_PIN, HIGH);  // Active-LOW: start OFF
  pinMode(RELAY_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  unsigned long duration = relayState ? ON_DURATION : OFF_DURATION;

  if (now - lastChange >= duration) {
    lastChange  = now;
    relayState  = !relayState;
    digitalWrite(RELAY_PIN, relayState ? LOW : HIGH);  // Active-LOW
    Serial.printf("Relay: %s\n", relayState ? "ON" : "OFF");
  }

  // Loop free for Wi-Fi, sensors, OLED, etc.
}</pre>
</div>

<h2>Button-Controlled Relay Toggle</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define RELAY_PIN  16
#define BUTTON_PIN 17

bool relayOn    = false;
bool lastBtn    = HIGH;

void setup() {
  Serial.begin(115200);
  digitalWrite(RELAY_PIN, HIGH);   // Start OFF (active-LOW)
  pinMode(RELAY_PIN,  OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  bool btn = digitalRead(BUTTON_PIN);
  if (lastBtn == HIGH && btn == LOW) {   // Falling edge — button pressed
    relayOn = !relayOn;
    digitalWrite(RELAY_PIN, relayOn ? LOW : HIGH);
    Serial.printf("Relay toggled: %s\n", relayOn ? "ON" : "OFF");
    delay(50);   // Debounce
  }
  lastBtn = btn;
}</pre>
</div>

<h2>AC Mains Safety Rules</h2>
<p>Switching mains voltage (110V or 240V AC) is inherently dangerous. Follow all of these rules:</p>
<ul>
  <li><strong>Use an optocoupler-isolated relay module</strong> — isolation separates the ESP32 low-voltage circuit from AC mains</li>
  <li><strong>Always work with AC disconnected</strong> — wire the relay board before connecting to the mains socket</li>
  <li><strong>Use appropriately rated relay</strong> — relay rated for 10A/250VAC for home appliances</li>
  <li><strong>Enclose AC wiring completely</strong> — no exposed terminals, use junction boxes</li>
  <li><strong>Never exceed relay current rating</strong> — a 10A relay cannot safely switch a 15A appliance</li>
  <li><strong>Add a fuse</strong> on the AC line as a safety backup</li>
  <li><strong>Follow local electrical codes</strong> — in many regions, permanent AC wiring requires a licensed electrician</li>
</ul>

<h2>Multiple Relay Control (8-Channel Module)</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — 8-channel relay</span><button class="copy-btn">Copy</button></div>
  <pre>const int RELAYS[] = {16, 17, 18, 19, 21, 22, 23, 25};
const int N = 8;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) {
    digitalWrite(RELAYS[i], HIGH);   // All OFF at start (active-LOW)
    pinMode(RELAYS[i], OUTPUT);
  }
}

void allOn()  { for (int i=0;i<N;i++) digitalWrite(RELAYS[i], LOW);  }
void allOff() { for (int i=0;i<N;i++) digitalWrite(RELAYS[i], HIGH); }

void loop() {
  // Sequence: turn on one by one with 200ms gap
  for (int i = 0; i < N; i++) {
    digitalWrite(RELAYS[i], LOW);    // ON
    delay(200);
    digitalWrite(RELAYS[i], HIGH);   // OFF
  }
  delay(1000);
}</pre>
</div>

<h2>Summary</h2>
<p>Always use a relay module — never connect a bare relay coil to ESP32 GPIO. Initialise GPIO HIGH before calling pinMode() to prevent startup clicks on active-LOW modules. Use millis() for non-blocking timing. For AC applications, use optocoupler-isolated modules and follow strict electrical safety practices.</p>
BODY,
],

/* ─── Guide 8: Reading Analog Signals ─── */
[
  'slug'      => 'reading-analog-signals-esp32',
  'title'     => 'Reading Analog Signals on ESP32: analogRead, Sensors, and ADC Tips',
  'meta_desc' => 'Learn to read analog signals on ESP32 — use analogRead(), map sensor values, interface potentiometers, LDR, NTC thermistors, and fix ADC non-linearity issues.',
  'read_time' => '13 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['adc-explained-esp32','dac-explained-esp32','digital-inputs-esp32','safe-gpio-pins-esp32'],
  'faqs'      => [
    ['q'=>'Which pins can read analog signals on ESP32?','a'=>'ESP32 has two ADCs: ADC1 (GPIO32–GPIO39) and ADC2 (GPIO0, GPIO2, GPIO4, GPIO12–GPIO15, GPIO25–GPIO27). ADC1 is preferred because ADC2 is shared with Wi-Fi and returns errors when Wi-Fi is active. Use GPIO32, GPIO33, GPIO34, GPIO35, GPIO36, GPIO39 for reliable analog readings.'],
    ['q'=>'What is the voltage range for analogRead() on ESP32?','a'=>'By default, ESP32 ADC reads 0–1.1V (with default 0dB attenuation) and maps it to 0–4095 (12-bit). For a 0–3.3V range, set 11dB attenuation: analogSetAttenuation(ADC_11db). Most sensor projects need 11dB attenuation.'],
    ['q'=>'How do I convert an analogRead() value to voltage?','a'=>'voltage = analogRead(pin) * (3.3 / 4095.0) — for 12-bit ADC with 11dB attenuation. Due to ADC non-linearity, this is only approximate at the extremes. For accurate voltage readings, use the ESP32 ADC calibration API from the ESP-IDF.'],
    ['q'=>'Why is ESP32 ADC2 unreliable when using Wi-Fi?','a'=>'ADC2 shares its hardware with the Wi-Fi RF subsystem. When Wi-Fi is active (which includes any ESP32 sketch that calls WiFi.begin()), ADC2 analogRead() returns -1 or incorrect values. Always use ADC1 pins (GPIO32–GPIO39) for analog readings in Wi-Fi projects.'],
    ['q'=>'How do I reduce ADC noise on ESP32?','a'=>'Take multiple readings and average them: int avg = 0; for (int i=0;i<16;i++) avg += analogRead(pin); avg /= 16; This reduces random noise significantly. Also add a 100nF decoupling capacitor from the sensor output to GND near the GPIO pin.'],
    ['q'=>'How do I read a potentiometer with ESP32?','a'=>'Connect the potentiometer outer terminals to 3.3V and GND, and the wiper (middle pin) to an ADC1 GPIO (e.g. GPIO34). Call analogSetAttenuation(ADC_11db) and analogRead(34) to get 0–4095. Map to percentage: int pct = map(analogRead(34), 0, 4095, 0, 100).'],
    ['q'=>'Can I use 5V sensors with ESP32 ADC?','a'=>'No. ESP32 GPIO pins (including ADC pins) have a 3.6V maximum input voltage. A 5V sensor output must be attenuated through a voltage divider (10kΩ + 20kΩ to give 3.33V from 5V) before connecting to an ADC pin. Without protection, 5V will permanently damage the chip.'],
    ['q'=>'What ADC resolution does ESP32 support?','a'=>'ESP32 ADC supports 9-bit (0–511), 10-bit (0–1023), 11-bit (0–2047), and 12-bit (0–4095) resolution. 12-bit (default) gives the highest resolution. Set it with analogReadResolution(12) in setup(). Note that due to noise and non-linearity, effective resolution is closer to 10–11 bits.'],
    ['q'=>'How do I read temperature from an NTC thermistor with ESP32?','a'=>'Use a voltage divider with the NTC and a 10kΩ fixed resistor. Connect 3.3V → NTC → GPIO34 → 10kΩ → GND. analogRead(34) gives raw value. Convert to resistance, then apply the Steinhart-Hart equation (or simplified Beta equation) to get temperature in degrees Celsius.'],
    ['q'=>'What is ADC attenuation on ESP32?','a'=>'Attenuation sets the full-scale input voltage of the ADC. 0dB = 0–1.1V, 2.5dB = 0–1.5V, 6dB = 0–2.2V, 11dB = 0–3.3V. Use 11dB (ADC_11db) for most sensor work. Set per-pin with analogSetPinAttenuation(pin, ADC_11db) or globally with analogSetAttenuation(ADC_11db).'],
  ],
  'body_html' => <<<'BODY'
<h2>Analog vs Digital Signals</h2>
<p>Digital signals are binary: they are either HIGH or LOW. Analog signals vary continuously across a range of voltages — a temperature sensor might output 0.5V at 0°C and 2.5V at 100°C. ESP32 includes an Analog-to-Digital Converter (ADC) that samples this continuous voltage and converts it to a number your code can work with.</p>

<h2>ESP32 ADC Pins</h2>
<table>
  <thead><tr><th>ADC</th><th>GPIO Pins</th><th>Wi-Fi Compatible?</th><th>Recommended?</th></tr></thead>
  <tbody>
    <tr><td>ADC1</td><td>GPIO32, GPIO33, GPIO34, GPIO35, GPIO36, GPIO39</td><td>Yes ✓</td><td>Always use ADC1</td></tr>
    <tr><td>ADC2</td><td>GPIO0, GPIO2, GPIO4, GPIO12–GPIO15, GPIO25–GPIO27</td><td>No ✗</td><td>Avoid when Wi-Fi active</td></tr>
  </tbody>
</table>
<p><strong>Best practice:</strong> Use GPIO34, GPIO35, GPIO36 (VP), GPIO39 (VN) for analog readings — these are input-only pins with no boot-strapping concerns and dedicated ADC channels.</p>

<h2>Basic analogRead() Setup</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#define ADC_PIN 34   // ADC1_CH6 — input-only, no boot concern

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);                // 12-bit: 0–4095
  analogSetAttenuation(ADC_11db);          // Full range: 0–3.3V
  // OR per-pin: analogSetPinAttenuation(ADC_PIN, ADC_11db);
}

void loop() {
  int raw     = analogRead(ADC_PIN);
  float volts = raw * (3.3f / 4095.0f);
  Serial.printf("Raw: %4d  Voltage: %.3f V\n", raw, volts);
  delay(200);
}</pre>
</div>

<h2>Attenuation Settings</h2>
<table>
  <thead><tr><th>Attenuation</th><th>Constant</th><th>Input Range</th><th>Use When</th></tr></thead>
  <tbody>
    <tr><td>0 dB</td><td>ADC_0db</td><td>0 – 1.1 V</td><td>Low-voltage precision sensors</td></tr>
    <tr><td>2.5 dB</td><td>ADC_2_5db</td><td>0 – 1.5 V</td><td>Audio input signals</td></tr>
    <tr><td>6 dB</td><td>ADC_6db</td><td>0 – 2.2 V</td><td>Half-scale 3.3V sensors</td></tr>
    <tr><td>11 dB</td><td>ADC_11db</td><td>0 – 3.3 V</td><td>Potentiometers, most sensors</td></tr>
  </tbody>
</table>

<h2>Reading a Potentiometer</h2>
<table>
  <thead><tr><th>Potentiometer Pin</th><th>Connect To</th></tr></thead>
  <tbody>
    <tr><td>Left terminal</td><td>ESP32 GND</td></tr>
    <tr><td>Right terminal</td><td>ESP32 3.3V</td></tr>
    <tr><td>Wiper (middle)</td><td>ESP32 GPIO34</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Potentiometer to LED brightness</span><button class="copy-btn">Copy</button></div>
  <pre>#define POT_PIN 34
#define LED_PIN 16

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  ledcSetup(0, 5000, 8);
  ledcAttachPin(LED_PIN, 0);
}

void loop() {
  int raw       = analogRead(POT_PIN);          // 0–4095
  int brightness = map(raw, 0, 4095, 0, 255);   // Scale to 8-bit PWM
  ledcWrite(0, brightness);
  Serial.printf("Pot: %4d  Brightness: %3d\n", raw, brightness);
  delay(50);
}</pre>
</div>

<h2>Averaging to Reduce Noise</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — 16-sample average</span><button class="copy-btn">Copy</button></div>
  <pre>int readADCAverage(int pin, int samples = 16) {
  long sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(pin);
    delayMicroseconds(100);   // Small gap between samples
  }
  return sum / samples;
}

void loop() {
  int smooth = readADCAverage(34, 16);
  float v    = smooth * (3.3f / 4095.0f);
  Serial.printf("Averaged: %4d  (%.3f V)\n", smooth, v);
  delay(100);
}</pre>
</div>

<h2>Reading an LDR (Light Sensor)</h2>
<p>An LDR (Light Dependent Resistor) changes resistance with light level. Wire it as a voltage divider:</p>
<table>
  <thead><tr><th>Component</th><th>Connection</th></tr></thead>
  <tbody>
    <tr><td>LDR leg 1</td><td>ESP32 3.3V</td></tr>
    <tr><td>LDR leg 2</td><td>GPIO35 AND 10kΩ resistor to GND</td></tr>
  </tbody>
</table>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — LDR light level</span><button class="copy-btn">Copy</button></div>
  <pre>#define LDR_PIN 35

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(LDR_PIN, ADC_11db);
}

void loop() {
  int raw   = analogRead(LDR_PIN);
  int light = map(raw, 0, 4095, 0, 100);   // 0 = dark, 100 = bright
  Serial.printf("LDR raw: %4d  Light: %3d%%\n", raw, light);

  if (light < 20) Serial.println("  ← Dark — turn on lights");
  else            Serial.println("  ← Bright enough");
  delay(500);
}</pre>
</div>

<h2>Reading an NTC Thermistor</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Temperature from NTC</span><button class="copy-btn">Copy</button></div>
  <pre>#define NTC_PIN    34
#define NOMINAL_R  10000.0f   // 10kΩ at 25°C
#define NOMINAL_T  25.0f      // Reference temperature
#define BETA       3950.0f    // Beta coefficient (from datasheet)
#define SERIES_R   10000.0f   // Fixed 10kΩ resistor in divider

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(NTC_PIN, ADC_11db);
}

void loop() {
  int raw = analogRead(NTC_PIN);

  // Calculate NTC resistance from voltage divider
  float voltage = raw * (3.3f / 4095.0f);
  float ntcR    = SERIES_R * voltage / (3.3f - voltage);

  // Steinhart-Hart simplified (Beta equation)
  float steinhart = ntcR / NOMINAL_R;
  steinhart = log(steinhart);
  steinhart /= BETA;
  steinhart += 1.0f / (NOMINAL_T + 273.15f);
  float tempC = (1.0f / steinhart) - 273.15f;

  Serial.printf("Temperature: %.1f °C\n", tempC);
  delay(1000);
}</pre>
</div>

<h2>ADC Non-Linearity Warning</h2>
<p>ESP32 ADC has a known non-linearity issue: readings near 0 and near 4095 are less accurate. The ADC is most linear between approximately 100–3900 (out of 4095). For precision measurements, use Espressif's calibration API or an external 16-bit ADC (ADS1115 over I2C) which provides far better accuracy.</p>

<h2>Summary</h2>
<p>Use ADC1 pins (GPIO32–GPIO39) for reliable analog readings, especially in Wi-Fi projects. Set 11 dB attenuation for full 0–3.3V range. Average multiple readings to reduce noise. Be aware of the non-linearity in the 0–100 and 3980–4095 ranges. For sensors requiring higher accuracy (medical, precision control), use an external I2C ADC.</p>
BODY,
],

/* ─── Guide 9: ADC Explained ─── */
[
  'slug'      => 'adc-explained-esp32',
  'title'     => 'ADC Explained on ESP32: Resolution, Attenuation, and Calibration',
  'meta_desc' => 'Deep dive into ESP32 ADC — understand SAR ADC architecture, ADC1 vs ADC2, 12-bit resolution, attenuation, calibration methods, and how to get accurate voltage readings.',
  'read_time' => '14 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['reading-analog-signals-esp32','dac-explained-esp32','safe-gpio-pins-esp32'],
  'faqs'      => [
    ['q'=>'What does ADC stand for and what does it do?','a'=>'ADC stands for Analog-to-Digital Converter. It converts a continuous analog voltage into a discrete digital number that a microcontroller can process. ESP32 ADC converts voltages between 0V and 3.3V into integers between 0 and 4095 (12-bit resolution).'],
    ['q'=>'What is the ADC resolution on ESP32?','a'=>'ESP32 supports 9-bit, 10-bit, 11-bit, and 12-bit ADC resolution. At 12-bit (default), the output ranges from 0 to 4095, giving 4096 discrete voltage steps. Effective resolution is around 10–11 bits due to built-in noise.'],
    ['q'=>'What is SAR ADC and how does ESP32 use it?','a'=>'SAR (Successive Approximation Register) ADC is the architecture used in ESP32. It works by binary-searching the input voltage: starting from the midpoint, it halves the search range in each step, requiring N steps for N-bit resolution. ESP32 performs 12 comparison steps to produce a 12-bit result.'],
    ['q'=>'What is the difference between ADC1 and ADC2 on ESP32?','a'=>'ADC1 uses GPIO32–GPIO39 and is fully independent of Wi-Fi/Bluetooth. ADC2 (GPIO0, GPIO2, GPIO4, GPIO12–GPIO15, GPIO25–GPIO27) is shared with the RF subsystem. When Wi-Fi is enabled, ADC2 is taken over by the RF hardware and returns errors. Always use ADC1 in wireless projects.'],
    ['q'=>'How do I improve ADC accuracy on ESP32?','a'=>'Techniques: 1) Use 11dB attenuation for full 0–3.3V range. 2) Average 8–64 samples to reduce noise. 3) Apply Espressif ADC calibration (esp_adc_cal_characterize) for offset correction. 4) Add a 100nF capacitor from the ADC input pin to GND. 5) Use GPIO34–GPIO39 which have cleaner ADC channels.'],
    ['q'=>'What is ADC attenuation and when should I change it?','a'=>'Attenuation scales the input voltage range to match the ADC full-scale. At 0dB the ADC reads 0–1.1V. At 11dB it reads 0–3.3V. Change attenuation when your sensor output is in a specific range: use 0dB for precision low-voltage signals (thermocouples, strain gauges) and 11dB for most common sensors.'],
    ['q'=>'What causes ESP32 ADC readings to be inaccurate?','a'=>'Known causes: ADC non-linearity (especially near 0V and 3.3V), power supply noise coupling into the ADC reference, switching noise from PWM or motors, Wi-Fi RF interference when using ADC2, and ground loops between sensors and ESP32. Use ADC calibration, averaging, and good power supply decoupling to mitigate.'],
    ['q'=>'Can ESP32 ADC be used for audio input?','a'=>'Yes, but with limitations. ESP32 ADC maximum sample rate is about 100 kSPS, sufficient for audio up to 50 kHz. However, ADC noise levels limit usable dynamic range to about 50 dB. For quality audio input use an external I2S ADC (ES8388, PCM1808) connected to the I2S peripheral.'],
    ['q'=>'What is ADC calibration on ESP32?','a'=>'ESP32 stores factory calibration data in eFuses (or external flash) that corrects for reference voltage variations between individual chips. The esp_adc_cal library reads this data and computes a correction polynomial. Result: voltage readings accurate to ±5% instead of the ±30% raw ADC error.'],
    ['q'=>'What are the practical limitations of ESP32 ADC?','a'=>'Practical limits: 12-bit resolution but ~10-bit effective; non-linear near 0V and 3.3V; ADC2 unavailable during Wi-Fi; maximum input voltage 3.6V; no differential input mode; no built-in oversampling hardware; sample rate limited to ~100 kSPS. For higher precision use an external ADC via SPI or I2C.'],
  ],
  'body_html' => <<<'BODY'
<h2>What is an ADC?</h2>
<p>An ADC (Analog-to-Digital Converter) bridges the gap between the continuous analog world (temperatures, pressures, light levels) and the discrete digital world inside a microcontroller. It samples an input voltage at a moment in time and produces a binary number representing that voltage.</p>
<p>ESP32 has two built-in 12-bit SAR ADCs capable of reading up to 18 channels. They are fundamental to interfacing with potentiometers, temperature sensors, pH sensors, accelerometers with analog output, and many other transducers.</p>

<h2>How SAR ADC Works (Simplified)</h2>
<p>ESP32 uses a Successive Approximation Register (SAR) architecture:</p>
<ol>
  <li>The ADC samples the input voltage and holds it steady (sample-and-hold)</li>
  <li>It starts with a guess of half the full-scale range (2048 for 12-bit)</li>
  <li>It compares the guess to the actual voltage: too high → go lower; too low → go higher</li>
  <li>Repeating 12 times, it narrows down to the exact 12-bit number</li>
  <li>The result (0–4095) is returned to your code via <code>analogRead()</code></li>
</ol>
<div class="code-block">
  <div class="code-bar"><span>SAR ADC Example: 1.65V on 3.3V range</span><button class="copy-btn">Copy</button></div>
  <pre>Step 1: Guess 2048 (1.65V) — exact match for this example
Result: 2048 out of 4095

Voltage resolution = 3.3V / 4095 = 0.000806V per step ≈ 0.8 mV/LSB

In practice, with noise: expect ±2–5 LSB variation on stable inputs.</pre>
</div>

<h2>ADC1 vs ADC2 Channel Map</h2>
<table>
  <thead><tr><th>GPIO</th><th>ADC</th><th>Channel</th><th>Wi-Fi Safe?</th></tr></thead>
  <tbody>
    <tr><td>GPIO36 (VP)</td><td>ADC1</td><td>CH0</td><td>Yes ✓</td></tr>
    <tr><td>GPIO37</td><td>ADC1</td><td>CH1</td><td>Yes ✓</td></tr>
    <tr><td>GPIO38</td><td>ADC1</td><td>CH2</td><td>Yes ✓</td></tr>
    <tr><td>GPIO39 (VN)</td><td>ADC1</td><td>CH3</td><td>Yes ✓</td></tr>
    <tr><td>GPIO32</td><td>ADC1</td><td>CH4</td><td>Yes ✓</td></tr>
    <tr><td>GPIO33</td><td>ADC1</td><td>CH5</td><td>Yes ✓</td></tr>
    <tr><td>GPIO34</td><td>ADC1</td><td>CH6</td><td>Yes ✓</td></tr>
    <tr><td>GPIO35</td><td>ADC1</td><td>CH7</td><td>Yes ✓</td></tr>
    <tr><td>GPIO4</td><td>ADC2</td><td>CH0</td><td>No ✗</td></tr>
    <tr><td>GPIO25</td><td>ADC2</td><td>CH8</td><td>No ✗</td></tr>
    <tr><td>GPIO26</td><td>ADC2</td><td>CH9</td><td>No ✗</td></tr>
  </tbody>
</table>

<h2>Resolution and Voltage Mapping</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Resolution configuration</span><button class="copy-btn">Copy</button></div>
  <pre>void setup() {
  Serial.begin(115200);

  analogReadResolution(12);         // 12-bit: 0–4095 (default)
  // analogReadResolution(10);      // 10-bit: 0–1023 (Arduino style)
  // analogReadResolution(9);       //  9-bit: 0–511

  analogSetAttenuation(ADC_11db);   // Input range: 0–3.3V
}

void loop() {
  int raw12  = analogRead(34);               // 12-bit raw
  float volts = raw12 * (3.3f / 4095.0f);   // Convert to voltage
  Serial.printf("12-bit raw=%4d  Voltage=%.4f V\n", raw12, volts);
  delay(500);
}</pre>
</div>

<h2>Attenuation Deep Dive</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — All attenuation modes</span><button class="copy-btn">Copy</button></div>
  <pre>void setup() {
  Serial.begin(115200);
  analogReadResolution(12);

  // Set different attenuation on different pins:
  analogSetPinAttenuation(34, ADC_0db);     // GPIO34: 0–1.1V (highest precision)
  analogSetPinAttenuation(35, ADC_6db);     // GPIO35: 0–2.2V
  analogSetPinAttenuation(36, ADC_11db);    // GPIO36: 0–3.3V (full range)
}

void loop() {
  Serial.printf("GPIO34(0dB)=%.3fV  GPIO35(6dB)=%.3fV  GPIO36(11dB)=%.3fV\n",
    analogRead(34) * (1.1f/4095.0f),
    analogRead(35) * (2.2f/4095.0f),
    analogRead(36) * (3.3f/4095.0f));
  delay(500);
}</pre>
</div>

<h2>ADC Non-Linearity Problem</h2>
<p>ESP32 ADC has a documented non-linearity, especially near 0V and 3.3V. The characteristic S-curve means readings in the 0–100 and 3900–4095 ranges are unreliable:</p>
<table>
  <thead><tr><th>ADC Raw Range</th><th>Accuracy</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>0–100</td><td>Poor (non-linear)</td><td>Avoid reading near 0V</td></tr>
    <tr><td>100–3900</td><td>Good (±1–3%)</td><td>Safe operating range</td></tr>
    <tr><td>3900–4095</td><td>Poor (saturates)</td><td>Avoid readings near 3.3V</td></tr>
  </tbody>
</table>
<p>Workaround: Ensure your sensor signal stays between 0.1V and 3.1V (raw 100–3900) for the best accuracy.</p>

<h2>ADC Calibration with esp_adc_cal</h2>
<p>Espressif provides a calibration library that dramatically improves accuracy:</p>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — ADC calibration</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;esp_adc_cal.h&gt;
#include &lt;driver/adc.h&gt;

esp_adc_cal_characteristics_t adcChars;

void setup() {
  Serial.begin(115200);

  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);  // GPIO34

  esp_adc_cal_characterize(
    ADC_UNIT_1,
    ADC_ATTEN_DB_11,
    ADC_WIDTH_BIT_12,
    1100,              // Default Vref (mV) — use 1100 if no eFuse calibration
    &adcChars
  );
}

void loop() {
  uint32_t raw     = adc1_get_raw(ADC1_CHANNEL_6);  // GPIO34
  uint32_t voltage = esp_adc_cal_raw_to_voltage(raw, &adcChars);  // mV
  Serial.printf("Raw: %4d  Calibrated: %4d mV  (%.3f V)\n",
                raw, voltage, voltage / 1000.0f);
  delay(500);
}</pre>
</div>

<h2>Oversampling for Better Effective Resolution</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — 16× oversampling (+2 bits)</span><button class="copy-btn">Copy</button></div>
  <pre>// Oversampling: 4^n samples → n extra bits of resolution
// 16 samples → 2 extra bits (12+2 = 14-bit effective)

uint16_t oversample(int pin, int samples = 16) {
  uint32_t acc = 0;
  for (int i = 0; i < samples; i++) {
    acc += analogRead(pin);
    delayMicroseconds(50);
  }
  return acc / samples;   // Average (for 16 samples, decimation gives +2 bits)
}

void loop() {
  Serial.printf("12-bit: %4d   Oversampled: %5d\n",
    analogRead(34), oversample(34, 64));
  delay(200);
}</pre>
</div>

<h2>External ADC: When ESP32 Built-in is Not Enough</h2>
<table>
  <thead><tr><th>ADC</th><th>Resolution</th><th>Interface</th><th>Best For</th></tr></thead>
  <tbody>
    <tr><td>ESP32 Built-in</td><td>12-bit (~10 eff)</td><td>Native</td><td>General sensing</td></tr>
    <tr><td>ADS1115</td><td>16-bit</td><td>I2C</td><td>Precision sensors</td></tr>
    <tr><td>ADS1256</td><td>24-bit</td><td>SPI</td><td>Scientific/industrial</td></tr>
    <tr><td>MCP3208</td><td>12-bit</td><td>SPI</td><td>Multiple channels</td></tr>
  </tbody>
</table>

<h2>Summary</h2>
<p>ESP32's built-in 12-bit SAR ADC is capable and convenient. For best results: use ADC1 channels (GPIO32–GPIO39), set 11 dB attenuation for full 3.3V range, average multiple samples, and apply factory calibration when accuracy matters. For measurements needing better than ±1% accuracy, use an external I2C ADC like the ADS1115.</p>
BODY,
],

/* ─── Guide 10: DAC Explained ─── */
[
  'slug'      => 'dac-explained-esp32',
  'title'     => 'DAC Explained on ESP32: Generate Analog Voltages and Audio Signals',
  'meta_desc' => 'Learn how to use the ESP32 built-in 8-bit DAC — output analog voltages on GPIO25/GPIO26, generate sine waves, audio signals, and understand DAC vs PWM differences.',
  'read_time' => '12 min',
  'phase'     => 'Phase 3: GPIO & Hardware',
  'related'   => ['adc-explained-esp32','reading-analog-signals-esp32','driving-leds-esp32'],
  'faqs'      => [
    ['q'=>'What is a DAC and what does it do?','a'=>'A DAC (Digital-to-Analog Converter) converts a digital number into a proportional analog voltage. ESP32 has two 8-bit DAC channels that output voltages between 0V and 3.3V on GPIO25 and GPIO26, controlled by the dacWrite() function with values from 0 (0V) to 255 (3.3V).'],
    ['q'=>'Which GPIO pins have DAC output on ESP32?','a'=>'Only GPIO25 (DAC1) and GPIO26 (DAC2) have hardware DAC capability on ESP32. No other GPIO pins can produce true analog voltage output. GPIO25 and GPIO26 are dedicated to DAC and should not be used for other analog or digital functions when DAC is active.'],
    ['q'=>'How is DAC different from PWM?','a'=>'PWM (Pulse Width Modulation) rapidly switches a pin between 0V and 3.3V. The average voltage simulates analog but still has switching noise. True DAC output is a steady DC voltage with no switching — appropriate for analog circuits, audio, and precision voltage references that cannot tolerate PWM ripple.'],
    ['q'=>'What is the voltage resolution of ESP32 DAC?','a'=>'ESP32 DAC is 8-bit: 256 steps over 0–3.3V. Each step is 3.3/255 = 0.0129V (12.9 mV) per increment. This is adequate for simple audio and rough voltage control but insufficient for precision applications requiring less than 1% error.'],
    ['q'=>'Can I output audio through ESP32 DAC?','a'=>'Yes. ESP32 DAC supports DMA-driven audio output at sample rates up to 16 kHz using I2S peripheral routed to the DAC. For better audio quality, use an external I2S DAC (PCM5102, MAX98357A) which provides 32-bit resolution and better SNR.'],
    ['q'=>'What current can the ESP32 DAC pins source?','a'=>'ESP32 DAC pins can source about 1 mA maximum. They are voltage reference outputs, not power outputs. To drive a speaker or any load needing more than 1 mA, add a buffer amplifier (LM358 op-amp) or audio amplifier IC between the DAC pin and the load.'],
    ['q'=>'Can I use GPIO25 or GPIO26 for digital I/O when not using DAC?','a'=>'Yes. If you do not call dacWrite() or initialise the DAC peripheral, GPIO25 and GPIO26 function as normal digital GPIO pins. They can also be used as ADC2 channels (though ADC2 is unreliable when Wi-Fi is active). To switch back to GPIO mode after using DAC, call dac_output_disable(DAC_CHANNEL_1).'],
    ['q'=>'How fast can ESP32 DAC generate waveforms?','a'=>'Using dacWrite() in loop(), update rates reach about 100 kSPS. Using the I2S-DAC interface with DMA, sample rates up to ~44.1 kHz are achievable, enabling full audio-quality waveforms. The theoretical Nyquist limit for 44.1 kHz sampling is 22 kHz — covering the full audible range.'],
    ['q'=>'Can I generate a true sine wave with ESP32 DAC?','a'=>'Yes. Pre-calculate a lookup table of sine values (0–255 for 8-bit), then output each value to dacWrite() in a timed loop or using the cosine waveform generator built into ESP32 (accessed via ESP-IDF). The hardware cosine oscillator can generate sine/cosine waves up to 40 MHz without CPU involvement.'],
    ['q'=>'What is the ESP32 hardware cosine oscillator?','a'=>'ESP32 has a hardware cosine wave generator (CW generator) inside the DAC peripheral. It can produce sine/cosine waves from a few Hz up to 40 MHz with programmable frequency, amplitude, and phase offset — all without CPU load. Access it through ESP-IDF or the dacCosineEnable() function in some Arduino core variants.'],
  ],
  'body_html' => <<<'BODY'
<h2>What is a DAC?</h2>
<p>A Digital-to-Analog Converter (DAC) is the opposite of an ADC. Where an ADC reads a voltage and converts it to a number, a DAC takes a number and generates a proportional analog voltage. ESP32 includes two 8-bit DAC channels, letting you output any voltage between 0V and 3.3V from GPIO25 and GPIO26.</p>
<p>Applications include audio output, voltage reference generation, waveform synthesis, analog control signals for external amplifiers, and smooth LED dimming without PWM ripple.</p>

<h2>ESP32 DAC Pins and Characteristics</h2>
<table>
  <thead><tr><th>Feature</th><th>Specification</th></tr></thead>
  <tbody>
    <tr><td>DAC channels</td><td>2 (DAC1 = GPIO25, DAC2 = GPIO26)</td></tr>
    <tr><td>Resolution</td><td>8-bit (0–255)</td></tr>
    <tr><td>Output range</td><td>0 V to 3.3 V (VDD)</td></tr>
    <tr><td>Voltage per step</td><td>3.3 V / 255 ≈ 12.9 mV</td></tr>
    <tr><td>Maximum output current</td><td>~1 mA (buffer amplifier needed for loads)</td></tr>
    <tr><td>Settling time</td><td>~1 µs</td></tr>
    <tr><td>Waveform generator</td><td>Hardware cosine oscillator built-in</td></tr>
  </tbody>
</table>

<h2>Basic dacWrite() Usage</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++)</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;Arduino.h&gt;

#define DAC_PIN_1 25   // DAC1
#define DAC_PIN_2 26   // DAC2

void setup() {
  Serial.begin(115200);
  // No pinMode needed for DAC pins — dacWrite() handles it
}

void loop() {
  // Step through all 256 voltage levels
  for (int val = 0; val <= 255; val++) {
    dacWrite(DAC_PIN_1, val);
    float volts = val * (3.3f / 255.0f);
    Serial.printf("DAC value: %3d  Voltage: %.3f V\n", val, volts);
    delay(20);
  }
  delay(500);
}</pre>
</div>

<h2>DAC vs PWM Comparison</h2>
<table>
  <thead><tr><th>Feature</th><th>DAC (True Analog)</th><th>PWM (Simulated Analog)</th></tr></thead>
  <tbody>
    <tr><td>Output type</td><td>Steady DC voltage</td><td>Pulsed 0V/3.3V switching</td></tr>
    <tr><td>Resolution</td><td>8-bit (256 steps)</td><td>Up to 16-bit (65536 steps)</td></tr>
    <tr><td>Switching noise</td><td>None ✓</td><td>Present (filterable)</td></tr>
    <tr><td>Available pins</td><td>GPIO25, GPIO26 only</td><td>All output-capable GPIOs</td></tr>
    <tr><td>For audio output?</td><td>Better ✓</td><td>Requires filter</td></tr>
    <tr><td>For LED dimming?</td><td>Works (1 mA limit)</td><td>Better (higher current)</td></tr>
    <tr><td>For motor speed?</td><td>No (insufficient current)</td><td>Yes ✓</td></tr>
  </tbody>
</table>

<h2>Generating a Sine Wave</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Software sine wave</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;math.h&gt;

#define DAC_PIN  25
#define SAMPLES  100    // Points per cycle
#define FREQ_HZ  50     // Target frequency: 50 Hz

uint8_t sineTable[SAMPLES];

void setup() {
  Serial.begin(115200);
  // Pre-calculate sine lookup table
  for (int i = 0; i < SAMPLES; i++) {
    float angle = 2.0f * M_PI * i / SAMPLES;
    sineTable[i] = (uint8_t)((sin(angle) + 1.0f) * 127.5f);  // 0–255
  }
}

void loop() {
  unsigned long delayUs = 1000000UL / (FREQ_HZ * SAMPLES);  // µs per step
  for (int i = 0; i < SAMPLES; i++) {
    dacWrite(DAC_PIN, sineTable[i]);
    delayMicroseconds(delayUs);
  }
}</pre>
</div>
<p>At 50 Hz with 100 samples, each step needs a 200 µs delay. This is achievable but CPU-blocking. For higher frequencies or non-blocking operation, use the I2S-DAC interface with DMA.</p>

<h2>Simple Audio Tone</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — 440 Hz tone (A4 note)</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;math.h&gt;

#define DAC_PIN 25
#define TONE_HZ 440

void setup() {
  Serial.begin(115200);
  Serial.println("Playing 440 Hz tone on DAC...");
}

void loop() {
  static unsigned long lastMicros = 0;
  static int phase = 0;
  const int STEPS = 50;
  unsigned long stepUs = 1000000UL / (TONE_HZ * STEPS);

  if (micros() - lastMicros >= stepUs) {
    lastMicros = micros();
    float angle = 2.0f * M_PI * phase / STEPS;
    dacWrite(DAC_PIN, (uint8_t)((sin(angle) + 1.0f) * 127));
    phase = (phase + 1) % STEPS;
  }
}</pre>
</div>

<h2>Dual DAC: Two-Phase Signal</h2>
<div class="code-block">
  <div class="code-bar"><span>Arduino (C++) — Quadrature (I/Q) signals</span><button class="copy-btn">Copy</button></div>
  <pre>#include &lt;math.h&gt;

#define DAC1_PIN 25   // In-phase
#define DAC2_PIN 26   // Quadrature (90° offset)
#define STEPS    64

void setup() { }

void loop() {
  for (int i = 0; i < STEPS; i++) {
    float angle = 2.0f * M_PI * i / STEPS;
    dacWrite(DAC1_PIN, (uint8_t)((sin(angle)        + 1.0f) * 127));
    dacWrite(DAC2_PIN, (uint8_t)((sin(angle + M_PI/2) + 1.0f) * 127));
    delayMicroseconds(100);
  }
}</pre>
</div>

<h2>Adding an Op-Amp Buffer for Driving Loads</h2>
<p>ESP32 DAC pins can only source ~1 mA. For driving a small speaker, headphone, or any analog circuit requiring more current, add an LM358 op-amp configured as a unity-gain voltage follower:</p>
<div class="code-block">
  <div class="code-bar"><span>Op-Amp Buffer Circuit</span><button class="copy-btn">Copy</button></div>
  <pre>ESP32 GPIO25 ──── LM358 IN+ (non-inverting)
LM358 OUT ──── LM358 IN– (inverting, direct feedback = unity gain)
LM358 OUT ──── Load (speaker, analog input, etc.)

LM358 VCC: 3.3V–12V (higher voltage allows more output swing)
LM358 GND: shared with ESP32 GND

Output follows input with up to 20 mA drive capability.</pre>
</div>

<h2>Practical Limitations and When to Use External DAC</h2>
<table>
  <thead><tr><th>Need</th><th>ESP32 DAC</th><th>External DAC Recommendation</th></tr></thead>
  <tbody>
    <tr><td>8-bit rough voltage</td><td>Sufficient ✓</td><td>—</td></tr>
    <tr><td>Audio output (low quality)</td><td>Sufficient ✓</td><td>—</td></tr>
    <tr><td>High-quality audio</td><td>Insufficient</td><td>PCM5102A (32-bit I2S)</td></tr>
    <tr><td>12-bit precision voltage</td><td>Insufficient</td><td>MCP4725 (12-bit I2C)</td></tr>
    <tr><td>16-bit output</td><td>Insufficient</td><td>DAC8552 (16-bit SPI)</td></tr>
    <tr><td>Multiple channels</td><td>2 channels max</td><td>MCP4728 (4-ch, 12-bit I2C)</td></tr>
  </tbody>
</table>

<h2>Summary</h2>
<p>ESP32's built-in 8-bit DAC on GPIO25 and GPIO26 provides true analog voltage output without PWM noise, making it ideal for audio tones, waveform generation, and smooth analog control signals. Its main limitations are 8-bit resolution (12.9 mV steps) and 1 mA current output. Add an op-amp buffer for driving loads and consider an external I2S DAC for high-quality audio applications.</p>
BODY,
],

]; // end return
