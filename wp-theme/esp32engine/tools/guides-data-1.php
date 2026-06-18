<?php
/* Phase 1 guide data — guides 1-5 */
return [

/* ============================================================ */
[
'slug'         => 'esp32-vs-esp8266',
'title'        => 'ESP32 vs ESP8266: Which Wi-Fi Microcontroller Should You Use?',
'meta_desc'    => 'Compare ESP32 and ESP8266 across dual-core speed, GPIO count, memory, Bluetooth, power modes, and price to pick the right chip for your IoT project.',
'read_time'    => '14 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'Can I run the same Arduino sketch on both ESP32 and ESP8266?','answer'=>'Mostly, if you use platform-agnostic libraries. Anything that calls ESP8266-specific headers (ESP8266WiFi.h, ESP8266WebServer.h) must be replaced with ESP32 equivalents (WiFi.h, WebServer.h). Analog reads, interrupt attachment, and timer syntax also differ slightly.'],
  ['question'=>'Does the ESP32 have more ADC channels than the ESP8266?','answer'=>'Yes. The ESP32 exposes up to 18 ADC channels across two SAR ADC units (ADC1 and ADC2), whereas the ESP8266 has a single 10-bit ADC on pin A0. Note that ADC2 channels are shared with Wi-Fi and cannot be used while Wi-Fi is active.'],
  ['question'=>'Is Bluetooth available on the ESP8266?','answer'=>'No. The ESP8266 only supports 802.11 b/g/n Wi-Fi. For Bluetooth you need the ESP32, which includes both Classic Bluetooth (BR/EDR) and Bluetooth Low Energy (BLE 4.2).'],
  ['question'=>'Which chip consumes less power in deep sleep?','answer'=>'Both achieve similar deep-sleep current (around 10–20 µA), but the ESP32 supports more granular sleep modes (modem sleep, light sleep, deep sleep, and hibernation) giving you finer control over the power budget.'],
  ['question'=>'Is the ESP8266 discontinued?','answer'=>'No, but it is a mature product with no new silicon revisions. Espressif continues to sell it, and it remains popular for price-sensitive single-function Wi-Fi tasks. The ESP32 line, however, receives active firmware development.'],
  ['question'=>'Can the ESP32 act as a Bluetooth serial replacement for HC-05/HC-06 modules?','answer'=>'Yes. Using the BluetoothSerial library the ESP32 creates a Classic Bluetooth SPP (Serial Port Profile) connection that pairs with standard Bluetooth serial apps, eliminating the need for a separate HC-05 module.'],
  ['question'=>'Which board is better for battery-powered sensors?','answer'=>'Both work, but the ESP32 gives more flexibility because its ultra-low-power (ULP) co-processor can read sensors while the main cores stay asleep. For pure Wi-Fi MQTT sensors the ESP8266 is marginally simpler to optimise at low cost.'],
  ['question'=>'Does the ESP32 support 5 GHz Wi-Fi?','answer'=>'No. Standard ESP32 and ESP8266 both support only 2.4 GHz 802.11 b/g/n. The ESP32-S3 and ESP32-C6 also remain 2.4 GHz only.'],
  ['question'=>'Are ESP32 development boards pin-compatible with ESP8266 NodeMCU boards?','answer'=>'Not physically. NodeMCU ESP8266 boards have 30-pin form-factors; ESP32 DevKit C boards are wider (38-pin). Breadboard projects need minor rewiring. Library and sketch porting is the larger task.'],
  ['question'=>'What is the maximum clock speed of the ESP32 vs ESP8266?','answer'=>'The ESP8266 runs at up to 160 MHz (single core). The ESP32 has two Xtensa LX6 cores each clocked up to 240 MHz, giving roughly three times the raw processing throughput on CPU-bound tasks.'],
],
'related'      => [
  ['title'=>'What is ESP32?','slug'=>'what-is-esp32'],
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
  ['title'=>'ESP32 Variants Explained','slug'=>'esp32-variants-explained'],
  ['title'=>'Choosing the Right ESP32 Board','slug'=>'choosing-esp32-board'],
],
'body_html'    => <<<'HTML'
<h2>Why the Comparison Matters</h2>
<p>When Espressif launched the ESP8266 in 2014 it quietly revolutionised the hobbyist internet-of-things space. For the first time a Wi-Fi capable microcontroller could be purchased for less than two US dollars, and the Arduino IDE made it accessible to anyone who could write a blink sketch. By 2016 the follow-up ESP32 arrived with a dual-core processor, integrated Bluetooth, and a dramatically expanded peripheral set. Today both chips remain in active production and both appear on the shelves of every electronics supplier in the world — so the question "which one should I use?" is entirely valid, and the answer depends on your project requirements.</p>

<p>This guide walks through every meaningful dimension of the comparison: processor architecture, memory, connectivity, GPIO count and capabilities, power consumption, toolchain maturity, and real-world cost. By the end you will have a clear mental framework for choosing the right chip on the first attempt, rather than discovering mid-project that you need to swap hardware.</p>

<h2>Architecture and Processing Power</h2>
<p>The ESP8266 is built around a single Tensilica L106 core running at 80 MHz by default and overclockable to 160 MHz. This is a 32-bit RISC core that handles Wi-Fi stack processing alongside your application code. When the radio fires up — which happens frequently during Wi-Fi operations — the core is partially occupied by the network stack, leaving less headroom for user code. This is why heavy computation such as JPEG encoding or sensor fusion can cause the ESP8266 to miss network packets or watchdog-reset.</p>

<p>The ESP32 pairs two Xtensa LX6 cores at up to 240 MHz. Core 0 (called "PRO_CPU") handles the Wi-Fi and Bluetooth stack by default; Core 1 ("APP_CPU") runs your Arduino sketch. This separation means your application logic receives a dedicated processor and is not interrupted by radio housekeeping. On FreeRTOS you can explicitly pin tasks to either core, schedule them with priorities, and use inter-core messaging queues. The result is a platform that can comfortably run real-time sensor acquisition on one core while streaming data over Wi-Fi on the other.</p>

<p>The ULP (Ultra Low Power) co-processor is a third, often overlooked compute element on the ESP32. It is a simple 8 MHz RISC core that runs while the main cores are asleep, capable of reading ADC values, toggling GPIO, and waking the main CPU when a threshold is crossed. There is no ULP equivalent on the ESP8266.</p>

<h2>Memory: Flash, RAM, and Heap</h2>
<p>Memory is where the ESP8266 feels most constrained in modern projects. The chip itself has no embedded flash; it relies entirely on an external SPI flash chip, typically 4 MB on NodeMCU and Wemos D1 Mini boards. Its SRAM is 160 KB total, of which approximately 80 KB is available to user code as heap once the Wi-Fi libraries are loaded. That 80 KB goes quickly when you start using JSON parsing libraries, TLS buffers for HTTPS connections, or web server frameworks.</p>

<p>The ESP32 has 520 KB of internal SRAM, with around 300–330 KB accessible as heap in a typical Arduino build. Many popular ESP32 modules (WROOM-32, WROVER) also include external PSRAM — 4 MB or 8 MB of pseudo-static RAM accessible via the SPI bus — which expands effective RAM into the megabytes at the cost of slightly lower access speed. This is enough headroom to decode JPEG thumbnails, run a small language model inference, or hold a full HTTP response body without gymnastics.</p>

<p>Flash storage defaults to 4 MB on most modules. The ESP32 supports flash sizes up to 16 MB depending on the module variant, and its flash partitioning system allows OTA update partitions, SPIFFS or LittleFS file-system partitions, and NVS (non-volatile storage) key-value partitions to coexist cleanly.</p>

<h2>GPIO Count and Peripheral Multiplexing</h2>
<p>The ESP8266 exposes 17 GPIO pins on the chip, though usable GPIOs on a NodeMCU board number around 11 once you exclude pins used for boot strapping, UART programming, and flash SPI. All GPIO are 3.3 V only and must not be driven above that voltage. One single-ended ADC pin is available, measuring 0–1 V (the NodeMCU voltage divider stretches this to 0–3.3 V externally). There is one hardware UART for programming and a second UART that can be mapped to alternate pins. I²C and SPI are bit-banged or hardware-assisted on fixed pins.</p>

<p>The ESP32 offers up to 34 GPIO pins, of which 18 can be configured as ADC inputs, 2 as true 8-bit DAC outputs, and many as capacitive touch sensors. Unlike the ESP8266, the ESP32 has a GPIO matrix that allows almost any peripheral function (UART, SPI, I²C, PWM, etc.) to be routed to almost any GPIO pin. This flexibility eliminates the rigid pin-mapping constraints that ESP8266 developers frequently encounter. The ESP32 also exposes four hardware SPI controllers, two I²C controllers, and two I²S interfaces for audio, which the ESP8266 lacks entirely.</p>

<h2>Connectivity: Wi-Fi, Bluetooth, and More</h2>
<p>Both chips support 802.11 b/g/n Wi-Fi on the 2.4 GHz band. They can operate as a Wi-Fi station (connecting to a router), as a software access point, or simultaneously in station+AP mode. Range and throughput are broadly similar because both use the same RF front-end design philosophies and typically achieve 50–100 Mbps theoretical peak (though real-world throughput through the Arduino API is far lower due to TCP/HTTP overhead).</p>

<p>The ESP32 adds Classic Bluetooth 4.2 (BR/EDR) for audio and SPP serial profiles, plus Bluetooth Low Energy (BLE) for sensor beacons, GATT services, and mesh networking. This is a genuine hardware addition, not an emulation — the same radio module that handles Wi-Fi switches to the Bluetooth band without an external antenna in dual-radio configurations. Classic BT and BLE can run concurrently. The ESP8266 has no Bluetooth capability whatsoever.</p>

<p>Some ESP32 variants extend connectivity further: the ESP32-C6 adds IEEE 802.15.4 (Thread and Zigbee), and the ESP32-H2 is purpose-built for Thread and Zigbee mesh networks. These are separate chip families rather than the base ESP32, but they demonstrate the ecosystem breadth that Espressif has built on top of the original design.</p>

<h2>Power Consumption Modes</h2>
<p>The ESP8266 active current draw hovers between 60 mA and 170 mA depending on transmit power. Modem-sleep mode (Wi-Fi radio off between DTIM beacon intervals) reduces average draw to 15–20 mA. Deep sleep — where most of the chip is powered down — reaches approximately 20 µA, with wake-up requiring an external reset signal on the RST pin connected to GPIO16.</p>

<p>The ESP32 active current is similar at 80–240 mA depending on both cores running and Wi-Fi transmitting. Its deep sleep current is around 10–50 µA depending on whether ULP is active. Light sleep suspends the CPU clocks while keeping SRAM contents alive and the Wi-Fi association intact — a mode the ESP8266 does not implement cleanly. The ULP co-processor adds a unique power tier: it reads sensors at microamp-level current while main cores hibernate, waking the system only when data crosses a threshold.</p>

<h2>Comparison Table</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Feature</th><th>ESP8266</th><th>ESP32</th></tr></thead>
<tbody>
<tr><td>CPU Cores</td><td>1 × Tensilica L106</td><td>2 × Xtensa LX6</td></tr>
<tr><td>Max Clock</td><td>160 MHz</td><td>240 MHz</td></tr>
<tr><td>SRAM</td><td>~80 KB usable</td><td>~300 KB usable + optional PSRAM</td></tr>
<tr><td>GPIO</td><td>11 usable (NodeMCU)</td><td>Up to 34</td></tr>
<tr><td>ADC</td><td>1 channel, 10-bit</td><td>18 channels, 12-bit</td></tr>
<tr><td>DAC</td><td>None</td><td>2 × 8-bit</td></tr>
<tr><td>Wi-Fi</td><td>802.11 b/g/n 2.4 GHz</td><td>802.11 b/g/n 2.4 GHz</td></tr>
<tr><td>Bluetooth</td><td>None</td><td>BT Classic + BLE 4.2</td></tr>
<tr><td>Touch Pins</td><td>None</td><td>10</td></tr>
<tr><td>Deep Sleep µA</td><td>~20 µA</td><td>~10 µA</td></tr>
<tr><td>I²S Audio</td><td>None</td><td>2 controllers</td></tr>
<tr><td>Typical Board Price</td><td>$2–4</td><td>$4–8</td></tr>
</tbody>
</table>
</div>

<h2>Toolchain, Libraries, and Community</h2>
<p>The ESP8266 Arduino core has been in active use since 2015 and has accumulated a decade of tutorials, forum posts, and library ports. If you encounter a problem there is almost certainly a Stack Overflow thread about it. The core is stable and bug-fix focused; do not expect new features.</p>

<p>The ESP32 Arduino core is newer but equally mature by now. Espressif maintains it directly and ships regular updates aligned with their IDF (IoT Development Framework) releases. Library support is excellent — every major sensor library that supports ESP8266 has an ESP32 variant. Additionally, for advanced users, the ESP-IDF (FreeRTOS-based native SDK) offers direct access to the dual-core RTOS, power management APIs, and hardware security features unavailable through Arduino abstractions.</p>

<h2>When to Choose ESP8266</h2>
<p>Choose the ESP8266 when your project demands the lowest component cost, requires nothing more than Wi-Fi connectivity, uses only one or two sensors, and can be powered from mains or a large battery. Classic use cases are smart plugs, temperature loggers that POST to a server every few minutes, simple web-controlled relays, and anything where you are shipping hardware at volume and every cent counts. The ESP8266 is also ideal when you are migrating an existing project that already has tested ESP8266 firmware and you do not need any new peripheral capabilities.</p>

<h2>When to Choose ESP32</h2>
<p>Choose the ESP32 for virtually every new project that does not have aggressive cost constraints. The $2–4 price premium buys dual-core processing headroom, Bluetooth, more GPIO, better ADC, DAC outputs, touch sensing, and expanded sleep modes. Real-time audio, camera projects (with ESP32-CAM), TLS-secured HTTPS, BLE advertising, OTA updates with dual-partition fallback, and any task that benefits from FreeRTOS task pinning all belong in ESP32 territory. It is the safer long-term bet because the chip family is still receiving new silicon variants from Espressif, whereas the ESP8266 is architecturally frozen.</p>

<h2>Migration Tips</h2>
<p>If you are porting an existing ESP8266 project to ESP32, start by replacing the library includes: <code>ESP8266WiFi.h</code> becomes <code>WiFi.h</code>, <code>ESP8266WebServer.h</code> becomes <code>WebServer.h</code>, <code>ESP8266HTTPClient.h</code> becomes <code>HTTPClient.h</code>. Most application logic transfers verbatim. Check your pin assignments — D0 through D8 map differently between boards, so use numeric GPIO numbers rather than D-prefixed aliases. <code>analogRead(A0)</code> on the ESP8266 returns 0–1023 for 0–1 V; on the ESP32 it returns 0–4095 for 0–3.3 V. Adjust any threshold comparisons accordingly.</p>

<p>If your ESP8266 project uses deep sleep, note that on ESP32 you call <code>esp_sleep_enable_timer_wakeup(microseconds)</code> before <code>esp_deep_sleep_start()</code> — there is no separate GPIO16-to-RST wiring required. The ESP32 wakes from its own internal RTC timer.</p>

<p>Finally, check your power supply. ESP32 boards draw more peak current (up to 500 mA during Wi-Fi transmit bursts) and are less tolerant of weak 3.3 V regulators on breadboard power rails. A quality AMS1117-3.3 or LDO with at least 600 mA capacity and 100 µF decoupling keeps the chip stable.</p>

<h2>Conclusion</h2>
<p>The ESP8266 is a proven, inexpensive chip that solves simple Wi-Fi tasks elegantly. The ESP32 is everything the ESP8266 is, plus dual cores, Bluetooth, more peripherals, and a richer power management story. For new designs in 2024 and beyond, start with the ESP32 — the modest price increase is almost always justified by the capabilities you gain. Reserve the ESP8266 for cost-sensitive volume builds where you need nothing beyond basic Wi-Fi and have an existing codebase to maintain.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'esp32-pinout-guide',
'title'        => 'ESP32 Pinout Guide: Every Pin Explained with Functions and Limits',
'meta_desc'    => 'Complete ESP32 pinout reference covering GPIO functions, ADC channels, DAC outputs, PWM, I2C, SPI, UART, touch pins, power rails, and safe voltage limits.',
'read_time'    => '16 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'How many GPIOs does the ESP32 have?','answer'=>'The ESP32 chip itself has 34 GPIO pins numbered 0–39. GPIO 34–39 are input-only and have no internal pull resistors. On a 38-pin DevKitC board, 34 of those are exposed; a 30-pin DevKit exposes fewer. GPIO 6–11 are reserved for the internal flash SPI and must never be used in user sketches.'],
  ['question'=>'Which ESP32 pins are output-only?','answer'=>'No pins are output-only on standard ESP32. GPIO 34, 35, 36, and 39 are input-only — they have no output driver. All other GPIOs can be configured as either input or output.'],
  ['question'=>'Can I connect a 5 V sensor directly to ESP32 GPIO?','answer'=>'No. ESP32 GPIO pins are 3.3 V logic and are not 5 V tolerant. Applying 5 V directly risks permanent damage. Use a resistor voltage divider (1kΩ/2kΩ) or a dedicated level shifter module between 5 V outputs and ESP32 inputs.'],
  ['question'=>'How many PWM channels does the ESP32 have?','answer'=>'The ESP32 LEDC peripheral provides 16 PWM channels organised into two groups of 8. Each channel has independently configurable frequency and duty cycle (up to 20-bit resolution). You can route any PWM channel to almost any GPIO through the GPIO matrix.'],
  ['question'=>'Can ADC2 pins be used while Wi-Fi is active?','answer'=>'No. ADC2 is shared with the Wi-Fi RF circuitry. When Wi-Fi is active, any attempt to call analogRead() on an ADC2 pin returns an error or garbage. Use only ADC1 pins (GPIO 32–39 on the 38-pin DevKit) for analog measurements in Wi-Fi projects.'],
  ['question'=>'What is the maximum current each GPIO pin can sink or source?','answer'=>'Each ESP32 GPIO can source or sink up to 40 mA individually. The total current across all GPIO together must not exceed 1,200 mA. For LEDs use a current-limiting resistor (330 Ω for a 20 mA LED on 3.3 V) — never drive LEDs directly without one.'],
  ['question'=>'Which pins support the capacitive touch feature?','answer'=>'GPIO 0, 2, 4, 12, 13, 14, 15, 27, 32, and 33 support capacitive touch sensing via the touchRead() function. Each pin measures capacitance; lower return values indicate a touch.'],
  ['question'=>'Where are the UART pins on a standard ESP32 DevKit?','answer'=>'UART0 is on GPIO 1 (TX) and GPIO 3 (RX) — this is also the USB programming port, so avoid using it at runtime. UART1 defaults to GPIO 10 (TX) and GPIO 9 (RX), but since those overlap with flash SPI, remap it with Serial1.begin(baud, SERIAL_8N1, rxPin, txPin). UART2 defaults to GPIO 17 (TX) and GPIO 16 (RX) and is safe for general use.'],
  ['question'=>'What voltage does the ESP32 operate at?','answer'=>'The ESP32 core logic operates at 3.3 V. The VCC supply pin accepts 3.0–3.6 V. DevKit boards include an onboard LDO regulator that accepts 5 V on the USB or VIN pin and steps it down to 3.3 V. Always power external sensors from the 3V3 pin, not from 5 V, unless you use level shifters.'],
  ['question'=>'Can I use GPIO 0 as a regular output pin?','answer'=>'With caution. GPIO 0 is a boot-strapping pin — it must be high during normal boot. If you drive it low at power-on (e.g., via a connected circuit), the chip enters download mode and will not run your sketch. In running code you can use it as an output after boot completes, but avoid sinking it to ground during power cycling.'],
],
'related'      => [
  ['title'=>'Safe GPIO Pins on ESP32','slug'=>'safe-gpio-pins-esp32'],
  ['title'=>'Boot Strapping Pins Explained','slug'=>'esp32-boot-strapping-pins'],
  ['title'=>'ESP32 vs ESP8266','slug'=>'esp32-vs-esp8266'],
  ['title'=>'What is ESP32?','slug'=>'what-is-esp32'],
],
'body_html'    => <<<'HTML'
<h2>Understanding the ESP32 Pin Numbering System</h2>
<p>The ESP32's GPIO numbering can initially confuse beginners because the chip-level GPIO numbers do not always match the silkscreen labels on popular development boards. Every GPIO is identified by a number from 0 to 39, and Espressif's datasheets and Arduino API functions always refer to these numbers — not D0, D1-style aliases. On the 38-pin DevKitC board, most silkscreen labels print the GPIO number directly, making it one of the cleaner boards to use. Always cross-reference the GPIO number printed on the board edge with the functional table below before wiring.</p>

<p>There are 34 GPIO pins in total (GPIO 0–33 plus GPIO 34–39 as input-only). GPIO 6 through 11 are internally connected to the SPI flash memory chip that stores your firmware — connecting anything to these pins will corrupt flash access and cause resets. This leaves 28 usable general-purpose GPIO on most 38-pin boards.</p>

<h2>Power Pins</h2>
<p>Before touching any GPIO, understand the power rails. The 38-pin DevKitC exposes: <strong>3V3</strong> (3.3 V regulated output, up to ~600 mA depending on the board's LDO), <strong>5V / VIN</strong> (5 V input from USB or external supply — do not use as a regulated output), <strong>GND</strong> (two or more ground pins), and <strong>EN</strong> (chip enable — pulling low resets the chip). The 3V3 pin can power external sensors and modules rated for 3.3 V. Never connect 5 V peripherals directly to GPIO without level shifting.</p>

<h2>GPIO 0–5: Boot-Sensitive Multi-Function Pins</h2>
<p><strong>GPIO 0</strong> doubles as a boot-mode selector. It must be pulled high through its internal pull-up during normal boot. Espressif's DevKit boards include a 10 kΩ pull-up resistor on this pin plus a BOOT button that grounds it. You can use GPIO 0 as output after boot, but be careful not to ground it externally during power-up.</p>
<p><strong>GPIO 1 (TX0) and GPIO 3 (RX0)</strong> are UART0 — the serial port used by the USB-to-serial chip for programming and the Arduino Serial monitor. Avoid using these for user purposes when you need the serial console. Output on GPIO 1 can be seen in the Serial Monitor.</p>
<p><strong>GPIO 2</strong> is another boot-strapping pin (must be low or floating for normal boot on some modules). The blue LED on the DevKitC is connected to GPIO 2. It is also an ADC1 channel (ADC1_CH2) and a touch pin (T2). After boot it can be used freely.</p>
<p><strong>GPIO 4</strong> is a safe general-purpose pin with no boot constraints. It supports ADC2 (not recommended with Wi-Fi), PWM, I²C SDA, and touch sensing.</p>
<p><strong>GPIO 5</strong> must be high during boot (another boot-strapping pin controlling the SD0 startup behaviour). It is connected to an onboard LED on some clone boards. After boot it is a safe GPIO with SPI-CS capability.</p>

<h2>GPIO 6–11: Never Use — Flash SPI Pins</h2>
<p>GPIO 6 (CLK), 7 (SD0/MISO), 8 (SD1/MOSI), 9 (SD2), 10 (SD3), and 11 (CMD) are the six lines of the internal quad-SPI interface that communicates with the external flash chip holding your firmware. Attempting to use any of these pins in your sketch will cause the ESP32 to crash or fail to program. Consider them permanently reserved. On the 38-pin DevKitC they are physically absent from the pin header.</p>

<h2>GPIO 12–15: JTAG and Boot-Sensitive</h2>
<p><strong>GPIO 12 (TDI)</strong> is a boot-strapping pin that sets the flash voltage level. If it reads high during boot, the chip selects a 1.8 V flash supply instead of 3.3 V. Most modules (WROOM-32, WROVER) have the flash strapped for 3.3 V, making GPIO 12 safe after boot — but connecting a pull-up resistor to 3.3 V before boot can prevent the chip from starting. The safest practice: use GPIO 12 only as an input without pull-up, or as an output driven after boot.</p>
<p><strong>GPIO 13 (TCK), GPIO 14 (TMS), GPIO 15 (TDO)</strong> are the remaining JTAG pins. They can be remapped for general use. GPIO 15 also controls boot log printing: when low, the ROM bootloader suppresses startup messages on UART0. After boot all four JTAG pins are available as regular GPIOs with ADC2 capability.</p>

<h2>GPIO 16–23: Most Reliable General-Purpose Pins</h2>
<p>This range contains the most reliable pins for beginners. <strong>GPIO 16 (RX2)</strong> and <strong>GPIO 17 (TX2)</strong> are the default UART2 hardware serial port — safe for RS232 adapters, GPS modules, and other UARTs. GPIO 18 is the default SPI clock (SCK), GPIO 19 the SPI data input (MISO), GPIO 21 the default I²C data (SDA), GPIO 22 the I²C clock (SCL), and GPIO 23 the SPI data output (MOSI). These functions are defaults only — the GPIO matrix lets you remap any peripheral to any pin, so you are not forced to use these specific pins.</p>
<p>GPIO 20 is not exposed on the standard 38-pin DevKitC. GPIO 22 is useful for I²C SCL but shares with an onboard LED on some development boards — check your board's schematic.</p>

<h2>GPIO 25–27: ADC2, DAC, and General Use</h2>
<p><strong>GPIO 25</strong> and <strong>GPIO 26</strong> are the two true 8-bit Digital-to-Analog Converter (DAC) outputs. Use <code>dacWrite(25, value)</code> where value is 0–255, corresponding to 0–3.3 V. These are the only pins that can output an arbitrary analog voltage without PWM filtering. They are ideal for driving audio amplifiers or generating simple waveforms. Both pins are also ADC2 channels, but since they are shared with Wi-Fi radio circuitry, they should not be used for analogRead() while Wi-Fi is active.</p>
<p><strong>GPIO 27</strong> is a general GPIO with ADC2 and touch pin capability (T7). It has no special constraints after boot.</p>

<h2>GPIO 32–33: ADC1 and Touch Pins</h2>
<p>GPIO 32 (ADC1_CH4, T9) and GPIO 33 (ADC1_CH5, T8) are part of the ADC1 group, making them safe for analog reads even when Wi-Fi is running. Both also support capacitive touch sensing and 32.768 kHz crystal input for the RTC clock. These are among the most versatile pins on the board for sensor projects.</p>

<h2>GPIO 34–39: Input Only</h2>
<p>GPIO 34, 35, 36, and 39 have no output driver circuit and no internal pull-up or pull-down resistors. They can only be configured as digital inputs or ADC inputs. GPIO 36 (SVP, ADC1_CH0) and GPIO 39 (SVN, ADC1_CH3) are the most common choices for voltage monitoring because they belong to ADC1 and work reliably with Wi-Fi active. Use these pins for reading analog sensors, voltage dividers, and light-dependent resistors.</p>

<h2>PWM: Anywhere You Need It</h2>
<p>Unlike AVR-based Arduinos where PWM is limited to specific marked pins, the ESP32 LEDC peripheral provides 16 PWM channels that can be routed to any output-capable GPIO. In Arduino IDE use <code>ledcSetup(channel, frequency, resolution)</code> and <code>ledcAttachPin(pin, channel)</code> to assign a PWM channel to a pin. Common frequencies: 5 kHz for motor control, 1 kHz for LED dimming, 38 kHz for IR transmission. Resolution up to 20 bits (1,048,576 steps), though 8-bit (255 steps) is standard for simple dimming.</p>

<h2>I²C: Flexible Remapping</h2>
<p>The ESP32 has two hardware I²C controllers. Wire (I²C bus 0) defaults to GPIO 21 (SDA) and GPIO 22 (SCL). Wire1 (I²C bus 1) can be assigned to any pins. Initialise with <code>Wire.begin(sda, scl)</code> to override defaults. The standard 100 kHz and 400 kHz clock speeds are supported; some libraries push to 800 kHz or 1 MHz. The ESP32 can host up to 112 I²C devices on a single bus (7-bit addressing), though bus capacitance limits practical numbers to 20–30 devices in typical wiring setups.</p>

<h2>SPI: Multiple Buses</h2>
<p>The ESP32 has four SPI controllers (SPI0 and SPI1 reserved for flash, HSPI and VSPI for user code). HSPI defaults to GPIO 14 (CLK), 12 (MISO), 13 (MOSI), 15 (CS). VSPI defaults to GPIO 18 (CLK), 19 (MISO), 23 (MOSI), 5 (CS). Both can be remapped. You can drive two independent SPI devices simultaneously on the two buses, which is useful for projects combining an SD card reader with an SPI display.</p>

<h2>Quick Reference Table</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>GPIO</th><th>Key Functions</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>0</td><td>Boot mode, ADC2_CH1, Touch T1</td><td>Boot-strapping — must be high on boot</td></tr>
<tr><td>1</td><td>UART0 TX</td><td>USB serial TX — avoid for user IO</td></tr>
<tr><td>2</td><td>ADC2_CH2, Touch T2, Blue LED</td><td>Boot-strapping (low or float) on some modules</td></tr>
<tr><td>3</td><td>UART0 RX</td><td>USB serial RX — avoid for user IO</td></tr>
<tr><td>4</td><td>ADC2_CH0, Touch T0</td><td>Safe general IO</td></tr>
<tr><td>5</td><td>SPI CS, VSPI default CS</td><td>Boot-strapping — must be high on boot</td></tr>
<tr><td>6–11</td><td>Flash SPI (CLK, MISO, MOSI…)</td><td>NEVER USE in user sketches</td></tr>
<tr><td>12</td><td>TDI, ADC2_CH5, Touch T5</td><td>Flash voltage strapping — no pull-up</td></tr>
<tr><td>13</td><td>TCK, ADC2_CH4, Touch T4</td><td>Safe after boot; JTAG</td></tr>
<tr><td>14</td><td>TMS, ADC2_CH6, HSPI CLK, Touch T6</td><td>Safe after boot</td></tr>
<tr><td>15</td><td>TDO, ADC2_CH3, HSPI CS, Touch T3</td><td>Boot log pin</td></tr>
<tr><td>16</td><td>UART2 RX</td><td>Safe, recommended UART2 RX</td></tr>
<tr><td>17</td><td>UART2 TX</td><td>Safe, recommended UART2 TX</td></tr>
<tr><td>18</td><td>VSPI CLK</td><td>SPI clock default</td></tr>
<tr><td>19</td><td>VSPI MISO</td><td>SPI data in default</td></tr>
<tr><td>21</td><td>I²C SDA</td><td>Wire default SDA</td></tr>
<tr><td>22</td><td>I²C SCL</td><td>Wire default SCL</td></tr>
<tr><td>23</td><td>VSPI MOSI</td><td>SPI data out default</td></tr>
<tr><td>25</td><td>DAC1, ADC2_CH8</td><td>True analog output</td></tr>
<tr><td>26</td><td>DAC2, ADC2_CH9</td><td>True analog output</td></tr>
<tr><td>27</td><td>ADC2_CH7, Touch T7</td><td>Safe general IO</td></tr>
<tr><td>32</td><td>ADC1_CH4, Touch T9, XTAL</td><td>Safe; ADC1 works with Wi-Fi</td></tr>
<tr><td>33</td><td>ADC1_CH5, Touch T8, XTAL</td><td>Safe; ADC1 works with Wi-Fi</td></tr>
<tr><td>34</td><td>ADC1_CH6</td><td>Input only, no pull resistors</td></tr>
<tr><td>35</td><td>ADC1_CH7</td><td>Input only, no pull resistors</td></tr>
<tr><td>36 (VP)</td><td>ADC1_CH0</td><td>Input only — good for analog</td></tr>
<tr><td>39 (VN)</td><td>ADC1_CH3</td><td>Input only — good for analog</td></tr>
</tbody>
</table>
</div>

<h2>Voltage and Current Limits</h2>
<p>Every GPIO pin on the ESP32 operates at 3.3 V logic. The absolute maximum input voltage is 3.6 V — exceeding this even briefly risks electrostatic damage to the input protection circuit. Maximum current per GPIO output pin is 40 mA source or sink. Always use a current-limiting resistor for LEDs: for a standard 20 mA LED with 2.0 V forward voltage on a 3.3 V supply, a 68 Ω resistor is the minimum (3.3 − 2.0 ÷ 0.02 = 65 Ω). A 100 Ω or 220 Ω resistor reduces brightness slightly and extends LED life.</p>

<p>The onboard 3V3 LDO regulator on typical DevKit boards supplies 600–800 mA maximum. If you are powering multiple servos, LCD modules, or a large LED strip from the board, power them from an external 3.3 V supply instead of from the 3V3 pin to avoid brownout resets.</p>

<h2>Practical Wiring Tips</h2>
<p>Use breadboard-friendly 30 AWG solid wire for short jumper connections and keep wire lengths under 20 cm for SPI and I²C to minimise signal reflections. Add 100 nF decoupling capacitors across the 3V3 and GND pins near sensitive analog sensors — even a small ceramic capacitor reduces ADC noise significantly. When reading capacitive touch pins, avoid running wires parallel to power or motor drive lines as they couple noise into the touch measurement.</p>

<p>For prototyping, number your GPIOs with sticky tape labels on the breadboard. The DevKitC's two rows of pins bridge the breadboard centre rails, leaving only one column of holes on each side. Consider a 30 AWG wire extension that breaks the pin rows out to a more accessible position for complex builds.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'esp32-variants-explained',
'title'        => 'ESP32 Variants Explained: S2, S3, C3, C6, H2, and CAM Compared',
'meta_desc'    => 'Understand every ESP32 family member — original ESP32, S2, S3, C3, C6, H2, and ESP32-CAM — with core count, connectivity, USB, and use-case comparisons.',
'read_time'    => '15 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'Is the ESP32-S3 better than the original ESP32?','answer'=>'For most new projects, yes. The ESP32-S3 has the same dual Xtensa LX7 (newer generation than LX6) cores at 240 MHz, more GPIO, native USB, better AI acceleration with vector instructions, and improved power management. The original ESP32 still wins on library maturity for very specific use cases like Classic Bluetooth.'],
  ['question'=>'Which ESP32 variant supports Matter/Thread/Zigbee?','answer'=>'The ESP32-C6 and ESP32-H2 both support IEEE 802.15.4, which is required for Thread and Zigbee. The C6 additionally supports Wi-Fi 6 (802.11ax). The H2 is 802.15.4 only — no Wi-Fi.'],
  ['question'=>'Does the ESP32-C3 have a dual core?','answer'=>'No. The ESP32-C3 has a single 32-bit RISC-V core running at up to 160 MHz. It supports Wi-Fi and BLE but lacks Classic Bluetooth and the second processing core of the original ESP32. It is designed for low-cost connected devices.'],
  ['question'=>'What makes the ESP32-S2 different from the original ESP32?','answer'=>'The ESP32-S2 is single-core (Xtensa LX7, 240 MHz), has native USB OTG support, and deliberately excludes Bluetooth to reduce cost and power. It has more GPIO (43 vs 34) and a 43-channel capacitive touch sensor system. It targets USB-connected peripherals and high-GPIO-count applications.'],
  ['question'=>'Can I use the ESP32-CAM without an FTDI programmer?','answer'=>'The standard AI-Thinker ESP32-CAM board has no onboard USB-to-serial chip. You need an external FTDI adapter (FT232RL or CH340) wired to the U0R and U0T pins to program it. Some third-party boards add a CH340 directly.'],
  ['question'=>'Is the ESP32-C6 backward compatible with ESP32 sketches?','answer'=>'Mostly, for sketches that use Wi-Fi, Serial, and basic GPIO. The C6 uses a RISC-V core, so Xtensa-assembly optimisations will not compile. Classic Bluetooth is absent. Most Arduino-level sketches port easily because the Arduino ESP32 core abstracts the hardware differences.'],
  ['question'=>'What is the difference between ESP32 modules and development boards?','answer'=>'A module (WROOM-32, WROVER, MINI-1) is a self-contained component with the ESP32 chip, flash, RF shielding, and antenna. A development board (DevKitC, NodeMCU-32S) adds a USB-to-serial programmer, voltage regulator, reset/boot buttons, and pin headers to a module, making it plug-and-play for breadboarding.'],
  ['question'=>'Does the ESP32-S3 support Bluetooth Classic?','answer'=>'No. The ESP32-S3 supports only Bluetooth Low Energy 5.0. Classic Bluetooth (BR/EDR), which is needed for Bluetooth audio A2DP and SPP serial profiles, is only available on the original ESP32.'],
  ['question'=>'Which variant has the most GPIO?','answer'=>'The ESP32-S2 exposes up to 43 GPIO pins, the most in the family. The ESP32-S3 exposes up to 45 GPIO. The original ESP32 has 34, and the ESP32-C3 has 22.'],
  ['question'=>'Is the ESP32-H2 suitable for general hobbyist projects?','answer'=>'It depends. The H2 has no Wi-Fi, so it cannot connect to a home router. It is purpose-built for battery-powered Thread/Zigbee mesh sensors where a coordinator (like a Home Assistant hub with a Thread border router) handles the internet connection. For beginners starting with Wi-Fi projects, choose the original ESP32 or ESP32-C3 instead.'],
],
'related'      => [
  ['title'=>'ESP32 vs ESP8266','slug'=>'esp32-vs-esp8266'],
  ['title'=>'Choosing the Right ESP32 Board','slug'=>'choosing-esp32-board'],
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
  ['title'=>'What is ESP32?','slug'=>'what-is-esp32'],
],
'body_html'    => <<<'HTML'
<h2>The ESP32 Family is Not a Single Chip</h2>
<p>When engineers and hobbyists say "ESP32" they often mean the original dual-core module released in 2016. In reality, Espressif has since built a family of six distinct silicon variants under the ESP32 brand, each optimised for a different balance of performance, connectivity, power, and price. Understanding the differences saves you from buying a chip that lacks a feature you need, or overpaying for capabilities your project will never use.</p>

<p>This guide covers: the original ESP32, the ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-H2, and the popular ESP32-CAM module. By the end you will know which variant belongs in which type of project.</p>

<h2>Original ESP32 (2016)</h2>
<p>The original chip pairs two Xtensa LX6 cores at up to 240 MHz with 520 KB SRAM and support for up to 16 MB of external SPI flash. It combines 2.4 GHz Wi-Fi 802.11 b/g/n with Classic Bluetooth 4.2 and Bluetooth Low Energy in the same radio. The 34 GPIO pins include two 8-bit DAC outputs, 18 ADC channels across two units, 10 capacitive touch sensors, an I²S audio interface, and an ultra-low-power (ULP) co-processor for sensor monitoring during deep sleep.</p>

<p>The most common module is the <strong>ESP32-WROOM-32</strong> — a metal-shielded rectangular module 18 mm × 25.5 mm housing the chip, 4 MB flash, and a PCB trace antenna. The <strong>ESP32-WROVER</strong> variant adds 4 MB or 8 MB of SPI PSRAM for memory-intensive applications like JPEG decoding and web serving. Development boards like the DevKitC and NodeMCU-32S mount these modules on a PCB with USB programming circuitry.</p>

<p>The original ESP32 is the best choice when you need Classic Bluetooth (A2DP audio, SPP serial), require the most mature Arduino library ecosystem, or are porting an existing project with well-tested ESP32 firmware. Its only weaknesses relative to newer variants are the lack of native USB and slightly higher idle power draw.</p>

<h2>ESP32-S2 (2019)</h2>
<p>The S2 replaced one of the two Xtensa LX6 cores with a single faster Xtensa LX7 core at 240 MHz and removed Bluetooth entirely. The rationale: many USB-connected devices — HID keyboards, MIDI controllers, CDC serial adapters — need USB connectivity but not Bluetooth. Adding native USB OTG (Full-Speed 12 Mbps) directly to the chip eliminates the external CH340 or CP2102 USB-to-serial chip that development boards previously required, lowering BOM cost and enabling the ESP32-S2 to enumerate as a composite USB device in user firmware.</p>

<p>The S2 expanded GPIO to 43 pins and added a 43-channel capacitive touch controller. It introduced a hardware security engine (RSA-3072, AES-256, SHA-2) and a digital signature peripheral for secure provisioning — features aimed at product developers shipping connected consumer goods.</p>

<p>Use the ESP32-S2 when your project connects via USB to a host computer (keyboards, MIDI, custom HID devices), needs a large number of GPIO, or requires hardware cryptography. Avoid it when you need Bluetooth — the S2 has none.</p>

<h2>ESP32-S3 (2021)</h2>
<p>The S3 is the current flagship for performance-sensitive applications. It pairs two Xtensa LX7 cores at 240 MHz (the same generation as S2 but dual-core), adds vector processing instructions for AI/ML inference acceleration, keeps the native USB OTG from S2, supports Bluetooth Low Energy 5.0, and exposes 45 GPIO pins. Internal SRAM is 512 KB; modules typically add 8 MB of octal-SPI PSRAM (a faster PSRAM variant than in WROVER) and 8 MB of octal-SPI flash.</p>

<p>The vector extensions let the S3 run TensorFlow Lite Micro models and audio DSP algorithms significantly faster than the original ESP32 — Espressif's own benchmarks show 5× to 10× improvement on convolution-heavy inference tasks. This makes the S3 the chip of choice for edge AI: wake-word detection, image classification on camera frames, gesture recognition, and similar on-device inference workloads. The ESP32-S3-based boards also commonly mount the camera interface (DVP) directly, making camera-AI combinations more straightforward than on the original ESP32-CAM.</p>

<p>Use the ESP32-S3 for any new project that could benefit from AI inference, large RAM buffers, native USB, BLE 5.0, or simply the most modern ESP32 architecture available. The increased GPIO count also makes it attractive for multiplexed matrix keyboards and large LED arrays.</p>

<h2>ESP32-C3 (2020)</h2>
<p>The C3 was Espressif's first RISC-V chip — a strategic move away from the licensed Xtensa architecture toward an open-source ISA. The 32-bit RISC-V core runs at up to 160 MHz, making it slightly slower than the dual-core ESP32 on raw throughput but extremely competitive on cost. Wi-Fi 802.11 b/g/n and BLE 5.0 are included; Classic Bluetooth is not. GPIO count is 22, with 6 ADC channels and 5 PWM outputs.</p>

<p>The C3's primary advantage is price. In volume, ESP32-C3 modules cost roughly 30–40% less than original ESP32 modules, making it attractive for any connected device where the project does not need two cores, analog audio, or the expanded GPIO of the S-series. It also has native USB Serial/JTAG — not full USB OTG, but enough to program it without an external USB-to-serial chip, which simplifies hardware design.</p>

<p>Choose the ESP32-C3 for simple sensor nodes, smart plugs, light controllers, and any battery-powered BLE beacon where you want Wi-Fi provisioning but the lowest possible module cost. The RISC-V architecture does not affect Arduino sketch development — the ESP32 Arduino core supports C3 identically at the API level.</p>

<h2>ESP32-C6 (2022)</h2>
<p>The C6 upgrades the RISC-V core to a higher-performance implementation (160 MHz LP core + 160 MHz HP core), adds Wi-Fi 6 (802.11ax) with OFDMA and Target Wake Time for significantly improved power efficiency in dense Wi-Fi environments, includes BLE 5.0, and — most importantly — adds an IEEE 802.15.4 radio for Thread and Zigbee mesh networking. This is the first ESP32 variant to combine Wi-Fi, BLE, and a Thread/Zigbee radio on a single chip.</p>

<p>For smart home developers building Matter-certified devices, the C6 is compelling because Matter over Thread requires exactly this combination of radios. The chip can act as a Thread router, a Zigbee coordinator, or a BLE gateway while simultaneously connected to Wi-Fi. Espressif ships a full Matter SDK (esp-matter) targeting the C6 and H2.</p>

<p>Use the C6 when you are targeting Matter, Thread, or Zigbee connectivity, building smart home devices that need to coexist in a crowded 2.4 GHz environment (Wi-Fi 6's orthogonal frequency division helps), or developing products for ecosystems like Apple HomeKit or Google Home that are adopting Matter.</p>

<h2>ESP32-H2 (2022)</h2>
<p>The H2 is the specialist in the family: it has a single RISC-V core at 96 MHz, IEEE 802.15.4 (Thread/Zigbee), BLE 5.3, and <em>no Wi-Fi whatsoever</em>. Removing Wi-Fi dramatically cuts power draw and silicon area. The H2 is designed for battery-powered mesh sensor nodes that relay data through a Thread network to a border router with internet access, rather than connecting directly to Wi-Fi. Think door/window sensors, occupancy detectors, and climate sensors that report through a hub.</p>

<p>On its own the H2 cannot talk to the internet or your home router. It is always paired with a border router device (a hub running Home Assistant with a Thread-capable radio dongle, for example). For beginners this makes it a more complex starting point. If you are building a Thread/Zigbee mesh from scratch, start with the C6 (which also has Wi-Fi for provisioning) and add H2 nodes as pure mesh endpoints once the infrastructure is established.</p>

<h2>ESP32-CAM</h2>
<p>The ESP32-CAM is not a distinct chip variant — it is a development module by AI-Thinker (and clones) that mounts an original ESP32 chip alongside a 2 MP OV2640 camera sensor, 4 MB of SPI PSRAM, an SD card slot, and a small onboard LED and flash LED. It is one of the most cost-effective camera-enabled microcontroller platforms available, often selling for $5–8.</p>

<p>The tradeoff for its low price is inconvenience: the board has no onboard USB-to-serial chip, so programming requires an external FTDI adapter connected to pins U0T, U0R, GND, and 5V, with GPIO 0 grounded during upload. The camera connector uses most of the available GPIO (GPIO 0, 2, 4, 5, 18, 19, 21, 22, 25, 26, 27, 32, 33, 34, 35), leaving only GPIO 1, 3, and 16 for user peripherals during camera operation. Despite these constraints, the ESP32-CAM is widely used for face recognition, motion detection streaming, QR code scanning, and simple surveillance applications.</p>

<p>If you need a camera without severe GPIO constraints, consider the newer ESP32-S3 based boards that mount a camera while still exposing more user GPIO through the expanded 45-pin array.</p>

<h2>Variant Comparison Table</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Variant</th><th>Core</th><th>Wi-Fi</th><th>BT</th><th>802.15.4</th><th>USB OTG</th><th>GPIO</th></tr></thead>
<tbody>
<tr><td>ESP32</td><td>2×LX6 240MHz</td><td>b/g/n</td><td>BT4.2+BLE</td><td>No</td><td>No</td><td>34</td></tr>
<tr><td>ESP32-S2</td><td>1×LX7 240MHz</td><td>b/g/n</td><td>No</td><td>No</td><td>Yes</td><td>43</td></tr>
<tr><td>ESP32-S3</td><td>2×LX7 240MHz</td><td>b/g/n</td><td>BLE5</td><td>No</td><td>Yes</td><td>45</td></tr>
<tr><td>ESP32-C3</td><td>1×RV32 160MHz</td><td>b/g/n</td><td>BLE5</td><td>No</td><td>Serial</td><td>22</td></tr>
<tr><td>ESP32-C6</td><td>1×RV32 160MHz</td><td>ax (Wi-Fi 6)</td><td>BLE5</td><td>Yes</td><td>Serial</td><td>30</td></tr>
<tr><td>ESP32-H2</td><td>1×RV32 96MHz</td><td>No</td><td>BLE5.3</td><td>Yes</td><td>Serial</td><td>19</td></tr>
<tr><td>ESP32-CAM</td><td>ESP32 +Camera</td><td>b/g/n</td><td>BT4.2+BLE</td><td>No</td><td>No</td><td>4 free</td></tr>
</tbody>
</table>
</div>

<h2>Which Variant Should a Beginner Choose?</h2>
<p>If you are just starting with ESP32 and want the widest tutorial support, the most libraries, and the smoothest on-ramp: start with the original <strong>ESP32 DevKitC</strong>. It has been the community standard board for years, and every tutorial you find online will either be written for it specifically or translate directly. Once you understand the fundamentals — GPIO, Wi-Fi, deep sleep — you will have the context to choose a more specialised variant for your next project with confidence.</p>

<p>For new products or projects where you know you need USB, BLE 5, or AI inference: jump straight to the <strong>ESP32-S3</strong>. For cost-optimised connected sensors: <strong>ESP32-C3</strong>. For Matter and smart home mesh: <strong>ESP32-C6</strong>. For a camera on a budget: <strong>ESP32-CAM</strong>.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'safe-gpio-pins-esp32',
'title'        => 'Safe GPIO Pins on ESP32: Which Pins to Use and Which to Avoid',
'meta_desc'    => 'A practical guide to safe ESP32 GPIO selection. Learn which pins are safe for any use, which are restricted to input-only, and which cause boot failures if misused.',
'read_time'    => '12 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'Which ESP32 GPIO pins are completely safe for beginner projects?','answer'=>'GPIO 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, and 33 are the safest for general use on a 38-pin DevKitC. None of these have boot-strapping constraints, flash SPI conflicts, or input-only restrictions. GPIO 32 and 33 are especially good for analog readings because they belong to ADC1, which works reliably with Wi-Fi active.'],
  ['question'=>'What happens if I use GPIO 6, 7, 8, 9, 10, or 11 in my sketch?','answer'=>'The ESP32 will likely crash, reset in a boot loop, or fail to program. These six pins are hardwired to the internal SPI flash chip and cannot be safely used in user code. They are physically absent from the pin header on most DevKitC boards specifically to prevent accidental use.'],
  ['question'=>'Can I use GPIO 34–39 as digital outputs?','answer'=>'No. GPIO 34, 35, 36 (VP), and 39 (VN) are strictly input-only pins with no output driver circuitry. They also lack internal pull-up and pull-down resistors. They are best used for analog sensor readings on ADC1, which is why they are popular for voltage monitoring.'],
  ['question'=>'Why does my project fail to boot when GPIO 12 is connected to 3.3 V?','answer'=>'GPIO 12 (TDI) is a flash voltage strapping pin. If it reads high during power-on, the chip selects 1.8 V flash supply voltage instead of 3.3 V. Most WROOM-32 modules use a 3.3 V flash, so a high signal on GPIO 12 at boot causes a flash read failure and boot loop. Use GPIO 12 only as input without a pull-up, or drive it only after the boot sequence completes.'],
  ['question'=>'Is GPIO 2 safe for driving an LED?','answer'=>'Yes, after boot completes. GPIO 2 is connected to the blue onboard LED on the DevKitC and is a boot-strapping pin that should be low or floating at power-on. During boot, ensure no external circuit pulls it high. In running code (after boot) you can use it as an output freely — toggling the LED with digitalWrite(2, HIGH) works perfectly.'],
  ['question'=>'Can I use GPIO 1 and GPIO 3 for a second UART or other peripheral?','answer'=>'Technically yes, but they are also UART0 connected to the USB serial chip. If you use Serial.begin() in your sketch (which most tutorials do for debugging), these pins are occupied and cannot simultaneously serve another peripheral. Disable Serial or use Serial2 on GPIO 16/17 instead.'],
  ['question'=>'Do input-only pins have internal pull-up resistors?','answer'=>'No. GPIO 34, 35, 36, and 39 have no internal pull-up or pull-down resistors. If you use them as digital inputs with a switch, you must add an external 10 kΩ pull-up resistor to 3.3 V (or pull-down to GND) to prevent the pin from floating.'],
  ['question'=>'Is GPIO 5 safe for general use after boot?','answer'=>'Yes. GPIO 5 must be high at boot (a strapping pin that affects SDIO slave timing). The DevKitC provides a 10 kΩ pull-up for this. After boot you can use GPIO 5 as any general GPIO, SPI chip-select, or PWM output.'],
  ['question'=>'Which pins should I avoid on the ESP32-CAM specifically?','answer'=>'On the AI-Thinker ESP32-CAM, GPIO 0, 2, 4, 5, 18, 19, 21, 22, 25, 26, 27, 32, 33, 34, and 35 are used by the camera and SD card. That leaves only GPIO 1 (UART TX), 3 (UART RX), and 16 (accessible via jumper) for user peripherals during camera operation.'],
  ['question'=>'Can I use GPIO 0 as a button input while the sketch is running?','answer'=>'Yes — the BOOT button on the DevKitC is wired to GPIO 0 and can be read with digitalRead(0) while the sketch runs. It reads HIGH when released and LOW when pressed. This is convenient for adding user input without extra components.'],
],
'related'      => [
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
  ['title'=>'Boot Strapping Pins Explained','slug'=>'esp32-boot-strapping-pins'],
  ['title'=>'Common ESP32 Beginner Mistakes','slug'=>'esp32-beginner-mistakes'],
],
'body_html'    => <<<'HTML'
<h2>Why GPIO Safety Matters Before You Wire Anything</h2>
<p>One of the most common frustrations for ESP32 beginners is a board that boots into an endless reset loop or refuses to accept a firmware upload — and the cause is almost always a GPIO misused as an output, a pull-up on the wrong pin, or a wire connected to a flash SPI pin. Unlike AVR-based Arduinos where you can safely use most digital pins interchangeably, the ESP32 has pins that influence boot mode, pins that are hardwired to internal peripherals, and pins that are physically incapable of driving output. Knowing these before you place your first wire saves hours of debugging.</p>

<p>This guide gives you a clear mental model for safe pin selection organised into four categories: pins that are always safe to use, pins with boot-time constraints, input-only pins, and pins that should never be touched.</p>

<h2>Category 1: Always-Safe Output and Input Pins</h2>
<p>These GPIO pins can be freely used as digital input, digital output, PWM, UART, SPI, or I²C without any boot constraints or hidden conflicts on a standard 38-pin DevKitC running WROOM-32:</p>

<ul>
<li><strong>GPIO 16, 17</strong> — UART2 (RX, TX). Safe for any use; excellent for connecting GPS, GSM, or other serial devices without interfering with the USB programming port.</li>
<li><strong>GPIO 18, 19, 23</strong> — Default VSPI clock, MISO, MOSI. Ideal for SPI devices (SD cards, displays, radio modules). Safe as general GPIO when not used for SPI.</li>
<li><strong>GPIO 21, 22</strong> — Default I²C SDA and SCL. Safe for any use. Nearly every I²C sensor library defaults to these pins.</li>
<li><strong>GPIO 25, 26</strong> — DAC1 and DAC2. The only GPIO with true analog output capability. Also ADC2 channels (avoid analogRead on these with Wi-Fi active).</li>
<li><strong>GPIO 27</strong> — No conflicts, no boot constraints. ADC2 channel and touch pin T7. Reliable for any general digital use.</li>
<li><strong>GPIO 32, 33</strong> — ADC1 channels CH4 and CH5. Touch pins T9 and T8. Can connect to a 32.768 kHz crystal for RTC. These are the best pins for analog reads in Wi-Fi projects because ADC1 does not conflict with the Wi-Fi radio.</li>
</ul>

<p>If you are building a new project and unsure which pin to use, start from this list and work outward only if you run out of pins.</p>

<h2>Category 2: Usable After Boot — Handle Boot-Time Carefully</h2>
<p>These pins are perfectly functional in running firmware but must not be externally driven high or low during the power-on boot sequence, because they influence the ESP32's startup configuration.</p>

<h3>GPIO 0 — Boot Mode Selector</h3>
<p>GPIO 0 is held high by an internal pull-up (and an external 10 kΩ on the DevKitC). Grounding it at power-up puts the chip into download (programming) mode. In running firmware you can use it freely — the onboard BOOT button is wired to it for exactly this reason. Avoid connecting external circuits that might pull GPIO 0 low at power-up. A momentary switch that grounds it is safe as long as you are not pressing it when power is applied.</p>

<h3>GPIO 2 — Blue LED, Secondary Boot Strapping</h3>
<p>GPIO 2 participates in the boot sequence together with GPIO 0. On some module variants it must be low (or floating) during boot to initiate normal operation. The DevKitC handles this automatically, but if you have a pull-up resistor wired to GPIO 2 externally and the chip was not booting before — this pin is your first suspect. In running code it works perfectly; toggling it blinks the blue onboard LED.</p>

<h3>GPIO 5 — SDIO Slave Timing</h3>
<p>GPIO 5 must be high during boot (controls SDIO slave timing). The DevKitC has a 10 kΩ pull-up. Do not connect GPIO 5 to a device that holds it low before power-on. After boot, use it freely — it is a common choice for SPI chip-select because it defaults high (deselecting the SPI device until you actively pull it low).</p>

<h3>GPIO 12 — Flash Voltage Strapping</h3>
<p>This is the most dangerous safe pin. GPIO 12 sets the internal flash operating voltage at boot: floating or low selects 3.3 V flash (correct for WROOM-32 modules), high selects 1.8 V flash (used only in certain embedded module variants). Never connect a pull-up resistor to GPIO 12 externally on a standard WROOM-32 or WROVER module. Use it as input or output only, with no pull-up. Read the warning in your project documentation before adding anything to this pin.</p>

<h3>GPIO 15 — Boot Log Enable</h3>
<p>GPIO 15 controls whether the ROM bootloader prints startup messages to UART0. When high (default with internal pull-up), the boot log is printed. When low, it is suppressed — sometimes used in production firmware to hide device information. Use GPIO 15 freely in running code, but be aware that pulling it low may suppress boot messages that help diagnose startup failures.</p>

<h2>Category 3: Input-Only Pins</h2>
<p>GPIO 34, 35, 36 (VP), and 39 (VN) have no output driver circuit. <code>pinMode(34, OUTPUT)</code> compiles without error but does nothing — the pin cannot drive a signal. They also have no internal pull-up or pull-down resistors. Any external switch or sensor connected to these pins needs its own pull resistor.</p>

<p>Despite these limitations, the input-only pins are excellent for their intended purpose: reading analog voltages via ADC1. GPIO 36 (VP, ADC1_CH0) and GPIO 39 (VN, ADC1_CH3) are particularly valuable because ADC1 works reliably while Wi-Fi is active, making them the default pins for battery voltage monitoring dividers, light sensor readings, and pot inputs in Wi-Fi-connected projects.</p>

<h2>Category 4: Pins You Must Never Use</h2>
<p>GPIO 6, 7, 8, 9, 10, and 11 are internally wired to the quad-SPI flash interface. On the 38-pin DevKitC these six pins are physically missing from the pin headers — Espressif intentionally omitted them to prevent the very mistake this section warns about. On bare ESP32 chips wired into custom PCBs, these pads exist and can be mistakenly connected to external components. If you ever encounter an ESP32 that enters a boot loop regardless of sketch state, check whether any wire is touching these physical pads or any net connected to them on your PCB.</p>

<h2>GPIO 1 and GPIO 3: Serial Console Overlap</h2>
<p>GPIO 1 (TX0) and GPIO 3 (RX0) are not in the "never use" category, but they are frequently overloaded by the Arduino <code>Serial</code> library. As long as your sketch calls <code>Serial.begin()</code>, these pins are owned by UART0 and will output garbage or miss data if you try to use them for other purposes simultaneously. If you need all 28 GPIO on the DevKitC, you can disable Serial and reclaim GPIO 1 and 3 — but you lose the Serial Monitor for debugging, which makes development significantly harder. The practical advice: avoid GPIO 1 and 3 during development; reassign them only after the project is stable and tested.</p>

<h2>Safe Pin Selection Cheatsheet</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Category</th><th>Pins</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Always safe</td><td>16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33</td><td>No restrictions in normal operation</td></tr>
<tr><td>Safe after boot</td><td>0, 2, 4, 5, 12, 13, 14, 15</td><td>Mind external circuits at power-on</td></tr>
<tr><td>Input only</td><td>34, 35, 36, 39</td><td>No output, no internal pull resistors</td></tr>
<tr><td>Serial conflict</td><td>1, 3</td><td>Shared with USB programming UART</td></tr>
<tr><td>Never use</td><td>6, 7, 8, 9, 10, 11</td><td>Internal flash SPI — will crash ESP32</td></tr>
</tbody>
</table>
</div>

<h2>Practical Rules for New Projects</h2>
<p>Follow these rules and you will avoid the most common GPIO-related mistakes:</p>
<ol>
<li>Start your pin list from the "always safe" category and work outward only if you need more pins.</li>
<li>Never wire pull-up resistors to GPIO 0, 2, 5, or 12 before understanding whether they are boot-strapping pins for your specific module variant.</li>
<li>Use GPIO 32 or 33 for your first ADC sensor — they are in ADC1 and produce reliable readings alongside Wi-Fi.</li>
<li>Assign UART2 (GPIO 16 RX, 17 TX) for any serial sensor like GPS or GSM, keeping UART0 (GPIO 1/3) free for the Serial Monitor during development.</li>
<li>If a circuit requires GPIO 12, add a note to your project documentation — every future maintainer needs to know it is a boot-sensitive pin.</li>
<li>For input-only pins (34, 35, 36, 39), always add an external pull resistor if connecting a switch or button; these pins float freely without one.</li>
</ol>
HTML,
],

/* ============================================================ */
[
'slug'         => 'esp32-boot-strapping-pins',
'title'        => 'ESP32 Boot Strapping Pins Explained: GPIO 0, 2, 5, 12, and 15',
'meta_desc'    => 'Learn how ESP32 boot strapping pins work, what each pin controls at power-on, and how to avoid boot loops caused by incorrect GPIO voltage levels during startup.',
'read_time'    => '13 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'What are boot strapping pins?','answer'=>'Boot strapping pins are GPIO lines that the ESP32 ROM reads at power-on (before any user firmware runs) to determine the boot mode and hardware configuration. Their voltage at the moment of reset determines whether the chip starts normally, enters download mode, or selects a different hardware configuration like flash voltage. After boot the pins function as regular GPIO.'],
  ['question'=>'How do I enter download mode to program the ESP32?','answer'=>'Ground GPIO 0 (press and hold the BOOT button), then apply a reset pulse (press and release EN/RST), then release GPIO 0. The ROM detects GPIO 0 low at reset and starts the UART download protocol. On DevKitC boards the USB-to-serial chip handles the GPIO 0 and EN signals automatically via DTR/RTS handshake, so you typically just click Upload in the IDE.'],
  ['question'=>'My ESP32 keeps resetting. Could a strapping pin be the cause?','answer'=>'Yes, this is one of the most common causes. If an external circuit accidentally drives GPIO 0 low at power-on, the chip enters download mode and never runs your sketch. If GPIO 12 is pulled high, the chip selects 1.8 V flash voltage and crashes reading flash. Check all five strapping pins and ensure no external wiring overrides their default pull levels during boot.'],
  ['question'=>'Does my ESP32-WROOM-32 require a specific GPIO 12 voltage at boot?','answer'=>'The WROOM-32 module uses 3.3 V flash (GD25Q32C or equivalent). GPIO 12 must be low or floating at boot to select the 3.3 V voltage. If GPIO 12 reads high during reset, the chip tries to operate the flash at 1.8 V and fails to read firmware. Never connect a pull-up resistor to GPIO 12 on a WROOM-32 module.'],
  ['question'=>'Can I disable the boot log messages printed at startup?','answer'=>'Yes. GPIO 15 low at boot suppresses ROM boot log messages on UART0. This is useful in production devices where you do not want the startup log visible on the UART. Pull GPIO 15 low through a resistor (not hard to ground, in case you need the log during debugging) or use efuse programming to make the setting permanent.'],
  ['question'=>'What does the ESP32 boot in SPI Boot mode vs Download mode?','answer'=>'In SPI Boot mode (GPIO 0 high at reset), the chip reads firmware from the external SPI flash and executes it. In Download mode (GPIO 0 low at reset), the chip runs a UART bootloader that accepts new firmware from the Arduino IDE or esptool.py. There is no user firmware execution in Download mode.'],
  ['question'=>'Is it safe to use the BOOT button (GPIO 0) as a user input after the sketch starts?','answer'=>'Yes. Once the boot sequence is complete and your sketch is running, GPIO 0 behaves as a normal input pin. Pressing BOOT while the sketch runs does not reset the chip (unless your sketch explicitly monitors GPIO 0 and calls ESP.restart()). Many projects use it as a configuration or factory-reset button.'],
  ['question'=>'What happens if all strapping pins are floating at boot?','answer'=>'The ESP32 has internal pull-up and pull-down resistors on most strapping pins that define the default behaviour when floating. GPIO 0 has an internal pull-up (defaults to SPI Boot mode), GPIO 12 has an internal pull-down (defaults to 3.3 V flash voltage), GPIO 15 has an internal pull-up (boot log enabled), and GPIO 5 has an internal pull-up. In the absence of external wiring the defaults produce normal boot behaviour.'],
  ['question'=>'Can I use GPIO 2 as an output during the boot strapping phase?','answer'=>'No external circuit should drive GPIO 2 to a specific state before the CPU finishes initialising. The ROM checks GPIO 0 and GPIO 2 together: if GPIO 0 is high and GPIO 2 is high on certain module configurations, the chip may not progress past ROM. Allow GPIO 2 to float or be driven only by the onboard pull-down/LED circuit until boot is confirmed by your sketch running.'],
  ['question'=>'How can I permanently change boot-strapping defaults without hardware?','answer'=>'The ESP32 has eFuses — one-time programmable memory cells — that can permanently override several strapping pin defaults including flash voltage selection (normally set by GPIO 12) and UART download mode enable/disable. Burning eFuses is irreversible, so it is a production/security measure rather than a debugging tool. Use esptool.py or idf.py efuse_common_table for this operation with extreme caution.'],
],
'related'      => [
  ['title'=>'Safe GPIO Pins on ESP32','slug'=>'safe-gpio-pins-esp32'],
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
  ['title'=>'Common ESP32 Beginner Mistakes','slug'=>'esp32-beginner-mistakes'],
],
'body_html'    => <<<'HTML'
<h2>What Happens in the First Milliseconds After Power-On</h2>
<p>When you apply power or press the reset button on an ESP32, a small piece of code permanently burned into the chip's ROM (read-only memory) runs before any of your Arduino sketch executes. This ROM bootloader performs a sequence of checks: it tests the integrity of the chip's clock, samples a handful of GPIO pins to determine the boot configuration, and then decides whether to load firmware from flash or wait for new firmware over UART. The GPIO pins it samples during this window are the boot strapping pins.</p>

<p>The sampling happens at the rising edge of the reset signal — the moment EN/RST goes from low to high. At that precise instant the ROM reads the logic level on GPIO 0, GPIO 2, GPIO 5, GPIO 12, and GPIO 15. These levels are set by internal pull resistors inside the chip, combined with any external wiring or devices you have connected. If an external component holds one of these pins at the wrong voltage, the ROM may select an unintended boot mode, select the wrong flash voltage, or behave unpredictably.</p>

<h2>The Five Strapping Pins and Their Roles</h2>

<h3>GPIO 0 — Boot Mode (SPI Boot vs UART Download)</h3>
<p>GPIO 0 is the primary boot mode selector. When GPIO 0 is high at reset, the ESP32 enters <strong>SPI Boot mode</strong> and loads your firmware from the SPI flash chip. When GPIO 0 is low at reset, the ESP32 enters <strong>UART Download mode</strong> and runs a serial bootloader that waits for new firmware from a host computer using the esptool.py protocol.</p>

<p>The internal state of GPIO 0 is a weak pull-up. The DevKitC adds a 10 kΩ external pull-up to 3.3 V to reinforce this default. The BOOT button on the DevKit shorts GPIO 0 to GND — you hold BOOT, press RST, release RST, then release BOOT to enter download mode manually. When using the Arduino IDE with a DevKitC, the USB-to-serial chip (CP2102 or CH340) automates this sequence using the DTR and RTS handshake lines, which is why pressing Upload works without manual button pressing on quality boards.</p>

<p>Problems caused by GPIO 0: Any external component that holds GPIO 0 low at power-on will trap the ESP32 in download mode. The most common culprits are I²C or SPI sensors connected with pull-down resistors, RC timing circuits, or MOSFET gate drivers whose output is low until the control signal rises. If your ESP32 appears to not run any sketch but accepts programming normally, check what is connected to GPIO 0.</p>

<h3>GPIO 2 — Boot Validation (Secondary UART Mode)</h3>
<p>GPIO 2 participates in boot mode configuration alongside GPIO 0. Specifically, when GPIO 0 is low (download mode), GPIO 2 must also be low for the download to work correctly on some chip revisions. When GPIO 0 is high (normal boot), GPIO 2 must not be pulled high externally on module configurations that include a pull-down in the boot sequence validation.</p>

<p>On the DevKitC, GPIO 2 connects to the blue LED through a resistor. The LED provides a small but non-zero load that typically holds the pin low enough during boot (the LED's forward voltage drop keeps the pin below the logic-high threshold when not driven). On custom boards, a pull-up to 3.3 V on GPIO 2 can prevent normal booting. The safest approach: leave GPIO 2 floating or with a weak pull-down, and drive it only from your sketch after boot confirms via LED blink or Serial.print.</p>

<h3>GPIO 5 — SDIO Slave Timing</h3>
<p>GPIO 5 controls the SDIO slave timing configuration at boot. When GPIO 5 is high, the SDIO slave interface uses the falling edge for data capture; when low, it uses the rising edge. For most projects that do not use the SDIO interface, this distinction is irrelevant — but the pin still needs to be high during boot to match the module defaults, otherwise the chip may initialise with an incorrect internal peripheral configuration.</p>

<p>The internal state is a pull-up, and the DevKitC reinforces this with a 10 kΩ external pull-up. GPIO 5 is also the default VSPI CS0 (chip-select) line, which happens to default-high — a convenient coincidence for SPI designs. After boot, drive GPIO 5 freely. Avoid connecting it to any device that pulls it low before the ESP32 powers on.</p>

<h3>GPIO 12 — Flash Voltage Selection (Most Dangerous)</h3>
<p>GPIO 12 is the most consequential strapping pin for hardware developers. It controls the voltage supplied to the SPI flash chip that holds your firmware. The internal state is a pull-down, selecting 3.3 V for the flash supply — correct for the GD25Q32, W25Q32, and similar flash chips used in WROOM-32, WROOM-32D, and WROVER modules. When GPIO 12 reads high at boot, the chip reconfigures the internal LDO to supply 1.8 V to the flash instead.</p>

<p>If your module uses 3.3 V flash (virtually all standard WROOM-32 modules do) and GPIO 12 is pulled high at boot, the flash operates at 1.8 V — below its rated minimum. The chip may read corrupted firmware, fail to boot, or enter a reset loop. This condition is silent and extremely confusing if you do not know the root cause.</p>

<p>The practical rules for GPIO 12: never connect a pull-up resistor to GPIO 12; use it only as a floating input or driven output; add a comment in your schematic noting the boot constraint. If you are using a module that genuinely uses 1.8 V flash (such as certain ESP32-D0WD-V3 based modules intended for low-voltage designs), you would intentionally pull GPIO 12 high — but verify this against your specific module's datasheet before doing so.</p>

<h3>GPIO 15 — Boot Log Suppression</h3>
<p>GPIO 15 has the least dramatic effect of the five strapping pins. When high (default, internal pull-up), the ROM bootloader prints a log of its startup sequence to UART0 at 115200 baud. This log includes the firmware load address, chip revision, flash size, and other diagnostic information. When GPIO 15 is low at boot, this log is suppressed.</p>

<p>Log suppression is useful in production devices where UART0 is exposed through an external connector — you do not want the boot log confusing a host device that expects application-level serial protocol from the start. During development, GPIO 15 high (or floating) is almost always the right choice because the boot log helps diagnose flash errors and brownout resets. After boot, GPIO 15 functions as a regular GPIO with ADC2 capability.</p>

<h2>Default Strapping Summary</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Pin</th><th>Internal Default</th><th>Low Selects</th><th>High Selects</th></tr></thead>
<tbody>
<tr><td>GPIO 0</td><td>Pull-up (High)</td><td>UART Download Mode</td><td>SPI Boot Mode ✓</td></tr>
<tr><td>GPIO 2</td><td>Pull-down (Low)</td><td>Normal boot ✓</td><td>Avoid externally</td></tr>
<tr><td>GPIO 5</td><td>Pull-up (High)</td><td>Avoid (SDIO timing)</td><td>Normal boot ✓</td></tr>
<tr><td>GPIO 12</td><td>Pull-down (Low)</td><td>3.3 V flash ✓</td><td>1.8 V flash (danger)</td></tr>
<tr><td>GPIO 15</td><td>Pull-up (High)</td><td>Boot log off</td><td>Boot log on ✓</td></tr>
</tbody>
</table>
</div>

<h2>How Development Boards Handle Strapping Automatically</h2>
<p>The DevKitC and NodeMCU-32S boards incorporate resistors and capacitors that keep all five strapping pins at their correct default values during power-on without requiring any user action. The 10 kΩ pull-ups on GPIO 0 and GPIO 5, the onboard LED providing a soft load on GPIO 2, and the absence of external pull-ups on GPIO 12 all contribute to reliable booting out of the box.</p>

<p>Custom PCB developers must replicate these conditions. The minimum strapping network for a stable WROOM-32 design is: 10 kΩ pull-up on GPIO 0 to 3.3 V, 10 kΩ pull-up on GPIO 5 to 3.3 V, GPIO 12 left floating with no external resistor, GPIO 15 left floating (or connected to a 10 kΩ pull-up if you want boot log). GPIO 2 should have a 10 kΩ pull-down or be left floating — never pull it up.</p>

<h2>Production Firmware and eFuse Overrides</h2>
<p>For devices deployed in the field, relying on external resistors to set strapping pin levels can be fragile. Espressif provides an eFuse mechanism to permanently override some boot defaults inside the chip itself. The JTAG_SEL_ENABLE and DL_ENABLE eFuses can disable download mode (preventing firmware extraction from stolen devices) and lock the flash voltage selection (removing the GPIO 12 dependency entirely). Burning eFuses is irreversible — once written they cannot be reset — so this is a step for final production firmware, not development.</p>

<h2>Diagnosing Boot Strapping Problems</h2>
<p>If your ESP32 is stuck in a boot loop or download mode, follow this checklist:</p>
<ol>
<li>Disconnect all GPIO wiring except power and USB. Press RST. Does it boot? If yes, reconnect devices one by one to identify which pin causes the problem.</li>
<li>Connect a USB serial adapter and open a terminal at 115200 baud. A boot loop typically prints a repeating "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)" sequence. A flash voltage mismatch may print no output at all or just garbage.</li>
<li>Measure GPIO 0 voltage at the moment you apply power (not after boot). It should be above 2.0 V for SPI Boot mode. If it reads below 0.8 V, something is holding it low.</li>
<li>Measure GPIO 12 at power-on. It should be below 0.5 V on a WROOM-32. Any voltage above 1.0 V is suspicious.</li>
<li>Try isolating the ESP32 on a breadboard with only power and USB. If it boots cleanly, the problem is in your connected circuit rather than the chip itself.</li>
</ol>
HTML,
],

]; // end return
