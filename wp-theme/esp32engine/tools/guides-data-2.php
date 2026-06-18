<?php
/* Phase 1 guide data — guides 6-9 */
return [

/* ============================================================ */
[
'slug'         => 'esp32-memory-architecture',
'title'        => 'ESP32 Memory Architecture: Flash, SRAM, PSRAM, and RTC Memory Explained',
'meta_desc'    => 'Understand every memory region on the ESP32 — internal SRAM, IRAM, DRAM, flash partitions, RTC memory, and PSRAM — and learn how to use each type effectively.',
'read_time'    => '14 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'How much RAM does the ESP32 actually have available for my code?','answer'=>'The ESP32 has 520 KB of SRAM total. After the Wi-Fi stack, Bluetooth stack (if enabled), and operating system overhead load, you typically have 280–330 KB of free heap available in a minimal Arduino sketch. Large String objects, JSON buffers, and HTTP response bodies quickly consume this. Monitor with ESP.getFreeHeap() to track usage.'],
  ['question'=>'What is the difference between IRAM and DRAM on ESP32?','answer'=>'IRAM (Instruction RAM) is used for storing executable code that must run directly from RAM rather than flash. Code in IRAM runs faster because RAM access avoids the flash cache latency. DRAM (Data RAM) stores global variables, heap allocations, and the stack. Both are physically part of the same 520 KB SRAM bank, just at different address regions.'],
  ['question'=>'When do I need PSRAM and how do I enable it?','answer'=>'You need PSRAM when your project buffers large data — image frames, audio buffers, web server response bodies, large JSON documents. Enable it in Arduino IDE under Tools → PSRAM → "Enabled". Allocate to PSRAM with ps_malloc() instead of malloc(). Note PSRAM access is ~5× slower than internal SRAM, so it is suited for large buffers, not for time-critical code paths.'],
  ['question'=>'How are the 4 MB of flash memory organised?','answer'=>'The 4 MB flash is divided into partitions defined by a partition table (usually a CSV file). A typical layout: bootloader (0x1000, 4 KB), partition table (0x8000, 4 KB), NVS (0x9000, 20 KB), OTA data (0xe000, 8 KB), app0 firmware (0x10000, 1.9 MB), app1 OTA firmware (same size), and SPIFFS/LittleFS file system. These regions can be customised.'],
  ['question'=>'What is NVS and when should I use it?','answer'=>'NVS (Non-Volatile Storage) is a key-value store in flash that persists across reboots and deep sleep cycles. It is the correct place to store Wi-Fi credentials, user settings, calibration values, and session tokens. Use the Preferences library (a wrapper around the NVS API) to read and write values with namespaced keys. It handles flash wear levelling internally.'],
  ['question'=>'Can data survive a deep sleep cycle in ESP32 RAM?','answer'=>'Standard internal SRAM is cleared on deep sleep. However, the RTC slow memory (8 KB) and RTC fast memory (8 KB) remain powered during deep sleep. Variables declared with the RTC_DATA_ATTR attribute are stored in RTC slow memory and survive deep sleep cycles. Use this for counters, sensor accumulation buffers, and wake-up reason tracking.'],
  ['question'=>'What happens when ESP32 heap fragmentation occurs?','answer'=>'When you allocate and free memory repeatedly in different sizes, the heap develops gaps (fragments). You may have 100 KB free total but no single contiguous block large enough for a 50 KB allocation, causing malloc() to return NULL. Avoid frequent small dynamic allocations; prefer fixed-size buffers declared globally where possible. Use ESP.getMaxAllocHeap() to check the largest available contiguous block.'],
  ['question'=>'How large can a SPIFFS or LittleFS file be?','answer'=>'The file system partition is typically 1–1.4 MB on a 4 MB flash layout, depending on your partition table. Individual files can be as large as the remaining free space in the partition, minus wear levelling overhead. LittleFS is recommended over SPIFFS for most new projects because it handles power-loss corruption more gracefully and supports directories.'],
  ['question'=>'What is the flash cache on ESP32?','answer'=>'The ESP32 has a 64 KB instruction cache and a 32 KB data cache that mirror frequently accessed flash content into fast on-chip SRAM. Code and read-only data stored in flash (including most Arduino sketch code) are transparently read through the cache. The cache is bypassed for flash write operations (which require erasing full 4 KB sectors).'],
  ['question'=>'Can I use both SRAM and PSRAM allocations in the same program?','answer'=>'Yes. Standard malloc(), new, and stack allocations go to internal SRAM by default. ps_malloc() specifically targets PSRAM. You can mix them freely: store time-critical buffers in SRAM and large but infrequently accessed data in PSRAM. The heap allocator will also fall back to PSRAM automatically when internal SRAM is exhausted if you compiled with the PSRAM heap allocation mode enabled.'],
],
'related'      => [
  ['title'=>'ESP32 Power Consumption Guide','slug'=>'esp32-power-consumption'],
  ['title'=>'ESP32 Variants Explained','slug'=>'esp32-variants-explained'],
  ['title'=>'What is ESP32?','slug'=>'what-is-esp32'],
  ['title'=>'Common ESP32 Beginner Mistakes','slug'=>'esp32-beginner-mistakes'],
],
'body_html'    => <<<'HTML'
<h2>Memory is the Resource You Will Run Out Of First</h2>
<p>Of all the ESP32's resources — processing cycles, GPIO pins, peripheral channels — memory is the one that limits projects most frequently. A sketch that compiles cleanly and runs perfectly with Wi-Fi disabled may crash or behave erratically when Wi-Fi connects, because the Wi-Fi stack consumes roughly 90 KB of heap at runtime. An HTTP client with TLS encryption adds another 40–60 KB. Add a JSON parser and a sensor data buffer, and you can exhaust the available 300 KB remarkably fast.</p>

<p>Understanding the ESP32's memory architecture — what types of memory exist, where they are mapped, and which is appropriate for each use case — transforms these crashes from mysterious failures into predictable, solvable engineering problems.</p>

<h2>The Five Memory Regions</h2>
<p>The ESP32 has five distinct memory regions, each with different characteristics, speeds, and lifetimes. They are not interchangeable.</p>

<h3>1. Internal SRAM (520 KB)</h3>
<p>The ESP32 has 520 KB of static RAM on the chip itself, divided into three banks at the hardware level. From the software perspective, this SRAM splits into two main categories:</p>

<p><strong>DRAM (Data RAM)</strong> — addresses 0x3FFB0000 to 0x3FFFFFFF — stores your global variables, heap allocations, and the task stacks managed by FreeRTOS. This is the memory returned by <code>malloc()</code>, <code>new</code>, and <code>String</code> object creation. The first region (0x3FFB0000–0x3FFB7FFF, 32 KB) is reserved for data used during ROM boot; the rest is available to applications. Typical free DRAM heap in a minimal Arduino sketch with Wi-Fi enabled: 280–330 KB.</p>

<p><strong>IRAM (Instruction RAM)</strong> — addresses 0x40070000 to 0x4009FFFF — stores executable code that must reside in RAM rather than being fetched from flash. Time-critical interrupt service routines and functions marked with <code>IRAM_ATTR</code> are placed here. IRAM access is faster than flash cache access because it has no cache latency. The tradeoff is that IRAM is smaller and its capacity is mostly consumed by the Wi-Fi and Bluetooth stacks in the default configuration.</p>

<h3>2. External Flash (4–16 MB)</h3>
<p>The ESP32 chip itself has no embedded flash. External flash is a separate SPI NOR flash chip connected to the ESP32 via a dedicated quad-SPI interface running at 80 MHz. The flash chip sits inside the WROOM-32 metal shield next to the ESP32 die.</p>

<p>Flash is accessed through a transparent cache system. When the CPU fetches an instruction that is not in the 64 KB instruction cache, the cache controller reads a 32-byte line from flash automatically. From the programmer's perspective, code stored in flash runs as if it were in RAM — just slightly slower due to occasional cache misses. Read-only data (string literals, lookup tables marked <code>PROGMEM</code> or placed in flash sections) is also cached through a separate 32 KB data cache.</p>

<p>Flash cannot be written at arbitrary addresses like RAM. It must be erased in 4 KB sectors before writing, and each sector supports approximately 100,000 erase cycles before wear causes bit errors. This is why logging sensor data to flash in a tight loop is a bad idea — the ESP32's flash will wear out within days. Use RTC memory or PSRAM for frequent writes, and write to flash only when data must persist across power cycles.</p>

<h3>3. Flash Partition Table</h3>
<p>The flash address space is divided into named partitions by a partition table stored at flash offset 0x8000. Each partition has a type (app or data), a subtype (factory firmware, OTA slot, NVS, SPIFFS, etc.), a start address, and a size. The standard partition table for a 4 MB flash device looks like this:</p>

<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Name</th><th>Type</th><th>Offset</th><th>Size</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td>nvs</td><td>data</td><td>0x9000</td><td>20 KB</td><td>Key-value persistent storage</td></tr>
<tr><td>phy_init</td><td>data</td><td>0xF000</td><td>4 KB</td><td>PHY calibration data</td></tr>
<tr><td>app0</td><td>app</td><td>0x10000</td><td>1.9 MB</td><td>Main firmware</td></tr>
<tr><td>app1</td><td>app</td><td>0x1F0000</td><td>1.9 MB</td><td>OTA update target</td></tr>
<tr><td>spiffs</td><td>data</td><td>0x3D0000</td><td>192 KB</td><td>File system</td></tr>
</tbody>
</table>
</div>

<p>You can customise this table to suit your project. A project that never uses OTA updates can remove one app partition and dedicate that space to a larger file system. A project that serves large HTML, CSS, and JS files from SPIFFS may use a "huge app" partition scheme that allocates 3 MB to the file system.</p>

<h3>4. NVS — Non-Volatile Storage</h3>
<p>NVS is a key-value store in flash that uses a wear-levelling algorithm to distribute writes across multiple flash pages, extending the effective write endurance from 100,000 cycles per sector to millions of cycles across the NVS partition. The NVS page-level format handles power loss corruption gracefully — a partial write is detected and rolled back on the next boot.</p>

<p>In Arduino IDE, the <code>Preferences</code> library wraps NVS. You open a namespace (like a database table), then read and write typed values:</p>
<pre><code>Preferences prefs;
prefs.begin("wifi", false);           // namespace "wifi", read/write
prefs.putString("ssid", "MyNetwork");
prefs.putString("pass", "secret123");
prefs.end();

// On next boot:
prefs.begin("wifi", true);            // read-only
String ssid = prefs.getString("ssid", "");
prefs.end();</code></pre>

<p>NVS is the correct storage location for: Wi-Fi credentials, device names, calibration offsets, user configuration settings, and session tokens. Do not store large data blobs in NVS — it is not designed for files. Keep individual values under a few hundred bytes.</p>

<h3>5. RTC Memory (8 KB + 8 KB)</h3>
<p>RTC (Real-Time Clock) slow memory (8 KB) and RTC fast memory (8 KB) are powered by the ESP32's RTC domain, which remains active during deep sleep. This is the only RAM that survives a deep sleep cycle — all other SRAM contents are lost when the main power domains shut down.</p>

<p>Declare variables in RTC slow memory with the <code>RTC_DATA_ATTR</code> attribute:</p>
<pre><code>RTC_DATA_ATTR int boot_count = 0;
RTC_DATA_ATTR float last_temperature = 0.0;

void setup() {
  boot_count++;
  Serial.printf("Boot number: %d\n", boot_count);
}</code></pre>

<p>On each wake from deep sleep, <code>boot_count</code> retains its previous value. Use RTC memory for: wake-up counters, accumulated sensor readings between uploads, last-known sensor values, and deep sleep timeout tracking. The ULP co-processor's code and data also reside in RTC slow memory, allowing sensor reads during deep sleep without waking the main cores.</p>

<h2>PSRAM — External Pseudo-Static RAM</h2>
<p>PSRAM (also called SPI RAM or SPIRAM) is an external RAM chip mounted inside WROVER modules alongside the ESP32 chip and flash. Standard WROVER modules include 4 MB PSRAM; newer S3-based WROVER modules may include 8 MB octal-SPI PSRAM. PSRAM connects via the SPI bus at up to 80 MHz and has access latency roughly 5× higher than internal SRAM — significant but not prohibitive for bulk data buffers.</p>

<p>Enable PSRAM in the Arduino IDE under <em>Tools → PSRAM → Enabled</em>. Allocate to PSRAM explicitly:</p>
<pre><code>uint8_t *image_buf = (uint8_t*) ps_malloc(320 * 240 * 2);  // 150 KB frame buffer
if (!image_buf) {
  Serial.println("PSRAM allocation failed");
}</code></pre>

<p>Without PSRAM, a 320×240 RGB565 frame buffer (150 KB) would consume half the available internal SRAM heap, leaving almost nothing for Wi-Fi, the web server, and other buffers. With PSRAM, the frame buffer lives externally and internal SRAM remains available for latency-sensitive operations.</p>

<h2>Memory Monitoring in Practice</h2>
<p>Add these calls to your setup() to baseline memory usage before deep sleep, OTA updates, or large operations:</p>
<pre><code>Serial.printf("Free heap:      %d bytes\n", ESP.getFreeHeap());
Serial.printf("Min free heap:  %d bytes\n", ESP.getMinFreeHeap());
Serial.printf("Max alloc:      %d bytes\n", ESP.getMaxAllocHeap());
if (psramFound()) {
  Serial.printf("Free PSRAM:   %d bytes\n", ESP.getFreePsram());
}</code></pre>

<p>Watch <code>getMinFreeHeap()</code> — it shows the lowest heap level reached since boot, revealing peak usage spikes that a snapshot <code>getFreeHeap()</code> call might miss. If <code>getMinFreeHeap()</code> drops below 20 KB, you are at risk of allocation failures.</p>

<h2>Avoiding Memory Problems</h2>
<p>Prefer fixed-size global arrays over dynamic heap allocations for buffers whose maximum size is known. Avoid the Arduino <code>String</code> class for repeated concatenation — it fragments the heap with repeated alloc/free cycles; use <code>char[]</code> arrays and <code>snprintf()</code> instead. For JSON, use ArduinoJSON's JsonDocument with a size calculated by the library's ArduinoJSON Assistant tool before allocating. For HTTP responses, stream them in chunks rather than buffering the entire body before processing. These practices extend the effective RAM budget of any ESP32 project without requiring more hardware.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'esp32-power-consumption',
'title'        => 'ESP32 Power Consumption Guide: Sleep Modes, Battery Life, and Optimisation',
'meta_desc'    => 'Master ESP32 power management — active mode, modem sleep, light sleep, deep sleep, and ULP. Calculate battery runtime and optimise your IoT device for months of operation.',
'read_time'    => '15 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'How long will a 2000 mAh battery last with an ESP32 in deep sleep waking every 30 seconds?','answer'=>'A rough calculation: active phase ~100 mA for 0.5 seconds + deep sleep ~10 µA for 29.5 seconds. Average current = (100,000 µA × 0.5 + 10 × 29.5) / 30 = (50000 + 295) / 30 ≈ 1677 µA = 1.68 mA. Battery life = 2000 mAh / 1.68 mA ≈ 1190 hours ≈ 50 days. Real-world results are 30–40% lower due to regulator efficiency and wake-up spikes.'],
  ['question'=>'What is the difference between deep sleep and hibernate on ESP32?','answer'=>'In deep sleep, the RTC controller, RTC memory, and ULP co-processor remain powered, allowing timer wake-ups and GPIO wake-ups. In hibernate mode (a subset of deep sleep), even the RTC memory is unpowered, reducing current to ~2–5 µA. Variables marked RTC_DATA_ATTR will NOT survive hibernate. Only an external signal on GPIO 0 (EXT0) can wake from hibernate, not the RTC timer.'],
  ['question'=>'How do I reduce power consumption during Wi-Fi connection?','answer'=>'Use static IP assignment instead of DHCP (saves 200–500 ms of negotiation time), store Wi-Fi channel and BSSID in RTC memory to skip scanning, use WiFi.begin(ssid, pass, channel, bssid) on wake-up, and set a short connection timeout. Each second of active Wi-Fi searching at 170 mA significantly increases average current consumption.'],
  ['question'=>'Can ESP32 run on solar power?','answer'=>'Yes. A 0.5 W solar panel paired with a 3.7 V lithium cell and an TP4056 or CN3791 MPPT charger module can power an ESP32 sensor node that wakes every 5–15 minutes. Size the panel for worst-case low-sun days in your location. Indoor solar (window-facing) requires at least 1–2 W panels due to dramatically lower irradiance.'],
  ['question'=>'What is modem sleep and when does it activate?','answer'=>'Modem sleep is an automatic power-saving mode where the Wi-Fi radio powers down between DTIM beacon intervals (typically every 100 ms). It activates automatically when your ESP32 is connected to a Wi-Fi AP and not actively transmitting. Average current drops from 80 mA to 20 mA with modem sleep. It is enabled by default in Arduino ESP32; no code is required to activate it.'],
  ['question'=>'Does Bluetooth LE consume more or less power than Wi-Fi?','answer'=>'BLE advertising at 100 ms interval consumes approximately 0.5–2 mA average — far less than Wi-Fi. BLE connection mode (GATT server/client) is 5–10 mA during active data exchange. If your application can use BLE instead of Wi-Fi for local data transfer (e.g., to a smartphone rather than a router), it offers significant battery savings.'],
  ['question'=>'How do I wake the ESP32 from deep sleep using a GPIO pin?','answer'=>'Use esp_sleep_enable_ext0_wakeup(GPIO_NUM_X, level) for a single GPIO trigger or esp_sleep_enable_ext1_wakeup(pin_mask, mode) for multiple GPIO. Then call esp_deep_sleep_start(). The ESP32 wakes when the pin reaches the specified level. Note: only RTC-capable GPIO pins (0, 2, 4, 12–15, 25–27, 32–39) can wake the chip from sleep.'],
  ['question'=>'What is the ULP co-processor and how much power does it use?','answer'=>'The ULP (Ultra Low Power) co-processor is a simple 8 MHz RISC processor that runs while the main cores are in deep sleep. It consumes approximately 25 µA while active. You can program it to read ADC values, toggle GPIO, and communicate with I²C sensors, waking the main CPU only when data crosses a threshold — avoiding the 100+ mA wake-up cost for routine sensor polling.'],
  ['question'=>'Should I use a 3.3 V LDO or a buck converter to power ESP32 from a LiPo battery?','answer'=>'For very low-power applications, a buck (switching) converter is more efficient (85–95% efficiency vs 60–70% for an LDO at low loads). However, switching converters generate RF noise that can slightly degrade Wi-Fi sensitivity. LDOs (AMS1117, MIC5219) are simpler and quieter but waste more power as heat. For battery life below 1 month use a buck converter; for shorter deployments an LDO is simpler.'],
  ['question'=>'How much current does the ESP32 draw during OTA update?','answer'=>'OTA update keeps both cores active, Wi-Fi receiving at full speed, and flash writing simultaneously. Expect 150–200 mA sustained for the duration of the update (typically 10–30 seconds for a 1 MB firmware image). Ensure your power supply can sustain this — thin breadboard wires or a weak USB hub can cause brownout resets mid-update, corrupting the OTA partition.'],
],
'related'      => [
  ['title'=>'ESP32 Memory Architecture','slug'=>'esp32-memory-architecture'],
  ['title'=>'Choosing the Right ESP32 Board','slug'=>'choosing-esp32-board'],
  ['title'=>'Common ESP32 Beginner Mistakes','slug'=>'esp32-beginner-mistakes'],
  ['title'=>'ESP32 vs ESP8266','slug'=>'esp32-vs-esp8266'],
],
'body_html'    => <<<'HTML'
<h2>Power is the Hidden Design Constraint</h2>
<p>When designing a mains-powered ESP32 project, power consumption rarely matters — the wall outlet supplies more current than any ESP32 configuration could demand. But the moment you target battery operation — a remote soil moisture sensor, a doorbell notifier, a wildlife camera trap — power consumption becomes the central design parameter. An ESP32 running at full speed with Wi-Fi active draws 80–240 mA, which would drain a 2000 mAh LiPo battery in less than a day. The same device, carefully managed with deep sleep, can run for months on the same battery.</p>

<p>This guide walks through every power mode the ESP32 supports, shows how to calculate realistic battery life, and gives you the practical code patterns to implement each mode in Arduino.</p>

<h2>Understanding ESP32 Current Draw</h2>
<p>The ESP32's power consumption has three major contributors: the CPU cores, the Wi-Fi/Bluetooth radio, and peripheral clocks. Active current is dominated by the radio — a Wi-Fi transmit burst at maximum output power consumes up to 240 mA momentarily. The CPU running at 240 MHz adds about 30–40 mA on top. When you turn off the radio and the CPU, the remaining leakage from RTC circuitry, RTC memory, and crystal oscillators drops to microamp levels.</p>

<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Mode</th><th>CPU</th><th>Wi-Fi Radio</th><th>Current</th><th>Wake Source</th></tr></thead>
<tbody>
<tr><td>Active (TX)</td><td>ON</td><td>Transmitting</td><td>160–240 mA</td><td>—</td></tr>
<tr><td>Active (RX)</td><td>ON</td><td>Receiving</td><td>80–100 mA</td><td>—</td></tr>
<tr><td>Active (idle)</td><td>ON</td><td>OFF</td><td>30–40 mA</td><td>—</td></tr>
<tr><td>Modem Sleep</td><td>ON</td><td>Periodic</td><td>15–20 mA avg</td><td>Timer</td></tr>
<tr><td>Light Sleep</td><td>Paused</td><td>Periodic</td><td>0.8–1.0 mA avg</td><td>Timer, GPIO, UART</td></tr>
<tr><td>Deep Sleep</td><td>OFF</td><td>OFF</td><td>10–50 µA</td><td>Timer, GPIO, ULP</td></tr>
<tr><td>Hibernate</td><td>OFF</td><td>OFF</td><td>2–5 µA</td><td>GPIO only</td></tr>
</tbody>
</table>
</div>

<h2>Active Mode</h2>
<p>Active mode is the default state after boot — both cores running, clocks at full frequency, Wi-Fi stack initialised. This is where your Arduino loop() executes. For mains-powered applications, you operate entirely in active mode. For battery-powered applications, you should minimise time in active mode and transition to sleep as quickly as possible after completing the task at hand.</p>

<p>You can reduce active mode power without sleeping by reducing CPU clock speed. Use <code>setCpuFrequencyMhz(80)</code> to drop from 240 MHz to 80 MHz — current drops roughly proportionally (from ~35 mA CPU to ~12 mA). At 80 MHz the ESP32 handles Wi-Fi, I²C sensors, and serial communication comfortably for most IoT tasks. At 10 MHz (the minimum stable frequency with Wi-Fi) you can reduce further but Wi-Fi may be unreliable.</p>

<h2>Modem Sleep</h2>
<p>Modem sleep is the simplest form of power saving and activates automatically when connected to a Wi-Fi access point and not transmitting. The radio powers down between the access point's DTIM beacon intervals (every 100–1000 ms depending on router configuration). The CPU stays active. Average current drops from 80 mA to roughly 15–20 mA.</p>

<p>No code is required to enable modem sleep — it is on by default in the Arduino ESP32 core when connected. You can also force the radio off manually while keeping Wi-Fi association alive with <code>WiFi.setSleep(true)</code>. This helps in sketches that poll a sensor on a schedule but only transmit occasionally.</p>

<h2>Light Sleep</h2>
<p>Light sleep pauses both CPU cores and most peripherals while retaining the contents of all SRAM. Wi-Fi association is maintained, and the chip can resume in under 1 ms without reconnecting to the network. Average current with Wi-Fi in light sleep is approximately 0.8–1 mA — a 100× reduction from full active mode. This mode is ideal for devices that must respond to incoming data quickly but spend most of their time idle.</p>

<pre><code>// Enter light sleep for 2 seconds
esp_sleep_enable_timer_wakeup(2 * 1000000ULL);  // microseconds
esp_light_sleep_start();
// Execution resumes here after wake
Serial.println("Woke from light sleep");</code></pre>

<p>Light sleep supports multiple wake sources simultaneously: a timer, a GPIO edge, a UART activity detect, or a Wi-Fi packet receipt. This makes it suitable for devices that sleep between transmissions but need to wake immediately if data arrives from the server.</p>

<h2>Deep Sleep</h2>
<p>Deep sleep is the most powerful battery-saving mode for devices that do not need to maintain a persistent network connection. The CPU, SRAM, and most peripherals are fully powered off. Only the RTC controller, RTC memory (16 KB total), and optionally the ULP co-processor remain active. Current drops to 10–50 µA depending on whether ULP is running and whether the 32.768 kHz crystal is active.</p>

<pre><code>// Wake after 30 seconds
esp_sleep_enable_timer_wakeup(30 * 1000000ULL);

// Optional: also wake on GPIO 33 going high
esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 1);

// Save data in RTC memory before sleeping
RTC_DATA_ATTR int readings_count = 0;
readings_count++;

esp_deep_sleep_start();
// ESP32 resets after this — setup() runs again on wake</code></pre>

<p>Note the important distinction from light sleep: <strong>deep sleep performs a full reset</strong>. setup() runs again after wake-up. Variables declared with <code>RTC_DATA_ATTR</code> survive, but all other state is lost. Wi-Fi must reconnect on each wake cycle. This reconnection cost (typically 0.5–2 seconds at 80–170 mA) dominates power consumption for devices that wake frequently. Optimise by storing Wi-Fi channel and BSSID in RTC memory and using <code>WiFi.begin(ssid, pass, channel, bssid)</code> to skip the channel scan.</p>

<h2>Wake-Up Causes and Optimising Reconnection</h2>
<p>Call <code>esp_sleep_get_wakeup_cause()</code> at the start of setup() to determine why the ESP32 woke:</p>
<pre><code>RTC_DATA_ATTR uint8_t wifi_channel = 0;
RTC_DATA_ATTR uint8_t wifi_bssid[6] = {};

void setup() {
  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER) {
    // Use cached channel/BSSID to reconnect faster
    if (wifi_channel > 0) {
      WiFi.begin(SSID, PASS, wifi_channel, wifi_bssid);
    } else {
      WiFi.begin(SSID, PASS);
    }
    // After connect, cache the channel and BSSID
    wifi_channel = WiFi.channel();
    memcpy(wifi_bssid, WiFi.BSSID(), 6);
  }
  // read sensor, transmit, sleep...
}</code></pre>

<p>This pattern reduces Wi-Fi reconnect time from 2–4 seconds to 0.5–1 second in stable environments, cutting average current consumption by 50% or more for 30-second wake cycles.</p>

<h2>ULP Co-Processor for Sensor Polling</h2>
<p>The ULP (Ultra Low Power) co-processor is a small 8 MHz processor that can execute simple programs while the main ESP32 cores are in deep sleep. Its primary use case is reading ADC values, checking GPIO states, or communicating via bit-bang I²C with sensors — tasks that happen frequently but do not require the full main core CPU.</p>

<p>Programming the ULP is more complex than writing Arduino sketches — it uses a simple assembly language or ULP RISC-V C code on the ESP32-S2 and S3. The payoff is dramatic: instead of waking the full core every 30 seconds to check a soil moisture sensor (100 mA for 0.5 seconds = 50 mAs per sample), the ULP reads the sensor at 25 µA continuously and wakes the main core only when moisture drops below a threshold — perhaps once per day. The energy savings can be 1000× or more for slow-changing environmental sensors.</p>

<h2>Battery Life Calculation</h2>
<p>For a sensor that wakes every 5 minutes, connects to Wi-Fi, reads a BME280 sensor, posts to MQTT, and sleeps again:</p>
<ul>
<li>Active time: ~2 seconds at 120 mA average = 240 mAs = 0.067 mAh per cycle</li>
<li>Sleep time: 298 seconds at 15 µA = 4,470 µAs = 0.00124 mAh per cycle</li>
<li>Total per cycle: ~0.068 mAh</li>
<li>Cycles per hour: 12</li>
<li>Consumption per hour: 12 × 0.068 = 0.82 mAh</li>
<li>Battery life on 2000 mAh: 2000 / 0.82 ≈ 2440 hours ≈ 102 days</li>
</ul>
<p>Apply a 0.7 efficiency factor for the LDO regulator, self-discharge, and LiPo capacity at temperature: ~71 days. Real-world results of 6–10 weeks are typical for this configuration.</p>

<h2>Hardware Considerations for Low-Power Designs</h2>
<p>Software sleep modes are only half the equation. Hardware choices matter equally: choose an LDO with low quiescent current (MCP1700 at 1.6 µA vs AMS1117 at 5–10 mA at no load — the AMS1117's own idle current can exceed your ESP32's deep sleep current); disable any power-on LEDs by removing or desoldering them; use sensors with shutdown modes and power them through a GPIO-controlled MOSFET so they draw zero current during sleep. On a custom PCB, add a 100 µF electrolytic capacitor across the 3.3 V rail to handle the initial power-on current spike without brownouting the regulator.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'choosing-esp32-board',
'title'        => 'Choosing the Right ESP32 Board: DevKitC, NodeMCU, WROOM, WROVER, and More',
'meta_desc'    => 'Compare ESP32 development boards and modules — DevKitC, NodeMCU-32S, WROOM-32, WROVER, Lolin32, and TinyPICO — to find the right form factor and features for your project.',
'read_time'    => '13 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'What is the difference between an ESP32 module and a development board?','answer'=>'A module (like WROOM-32 or WROVER) is a self-contained component with the ESP32 chip, flash, antenna, and RF shielding. It has castellated edge pads for soldering onto a carrier PCB, but no USB or voltage regulator. A development board mounts a module onto a PCB with USB-to-serial programmer, 5V-to-3.3V LDO, reset/boot buttons, and pin headers — everything needed to plug into a breadboard and start coding.'],
  ['question'=>'Can I use the ESP32 DevKitC with a full-size breadboard?','answer'=>'The 38-pin DevKitC is 28.2 mm wide, which straddles the centre of a standard 63 mm breadboard — only one row of holes remains on each side. Use two breadboards side by side, or a half-pitch adapter board. Alternatively, the 30-pin DevKit leaves two rows on each side.'],
  ['question'=>'Do I need the WROVER module with PSRAM for my project?','answer'=>'Only if your project requires large in-memory buffers. Camera projects (JPEG decode/encode), HTTPS servers with TLS buffers, large JSON responses, and audio processing are the main beneficiaries. For simple sensor logging, relay control, and MQTT clients, the 520 KB internal SRAM on a WROOM-32 board is more than sufficient.'],
  ['question'=>'What is a bare ESP32 chip vs a module?','answer'=>'A bare chip (ESP32-D0WDQ6, ESP32-D0WD-V3) is just the silicon die in a QFN package. It has no flash, no antenna, and no RF shielding. You must design a full PCB with the flash chip, RF matching network, antenna (PCB trace or external whip), decoupling capacitors, and crystal. Modules like WROOM-32 provide a pre-certified RF design so your final product does not require individual RF certification, saving significant regulatory cost.'],
  ['question'=>'Which boards have native USB without an external USB-to-serial chip?','answer'=>'Boards based on the ESP32-S2 or ESP32-S3 chip can use native USB OTG (Adafruit Feather ESP32-S2, Unexpected Maker FeatherS3, WeAct Studio ESP32-S3). The ESP32-C3 and C6 have USB Serial/JTAG for programming but not full USB OTG. All original ESP32 boards require an external CH340, CP2102, or similar USB-to-serial chip for programming.'],
  ['question'=>'Is TinyPICO suitable for battery-powered wearables?','answer'=>'Yes. The TinyPICO is specifically designed for ultra-low-power wearable and portable applications. It uses an ME6211 LDO with 40 µA quiescent current, has a LiPo connector, battery charging circuit, and 4 MB PSRAM in a 18 mm × 32 mm footprint. Deep sleep current is as low as 20 µA including the LDO — comparable to purpose-built low-power MCUs.'],
  ['question'=>'What is the Lolin D32 Pro and why does it have a battery connector?','answer'=>'The Lolin D32 Pro (WEMOS D32 Pro) is a compact ESP32 development board with a LiPo battery connector, onboard TP4056 charging circuit (charges the battery from USB), and TF/micro SD card slot. It is popular for portable data loggers and handheld projects where both USB programming convenience and battery operation are needed.'],
  ['question'=>'Do all ESP32 boards have the same antenna performance?','answer'=>'No. PCB trace antennas vary in quality based on PCB material, trace dimensions, and nearby ground planes. WROOM-32 modules have a well-characterised and FCC/CE-tested trace antenna. Budget clones sometimes use a smaller or poorly routed antenna, reducing range by 20–50%. For critical range requirements, use a module with an external antenna connector (WROOM-32U, WROOM-32E) and an external dipole or patch antenna.'],
  ['question'=>'Can I stack ESP32 boards with Arduino Mega or Uno?','answer'=>'Electrically possible but unusual. The ESP32 is a 3.3 V device and Arduino Uno is 5 V; direct pin connection without level shifting risks ESP32 GPIO damage. A common pattern is to connect the ESP32 via UART to an Arduino, using the Arduino for 5 V motor control and the ESP32 for Wi-Fi, communicating over a 3.3 V / 5 V level-shifted serial link. Alternatively, just use the ESP32 alone for projects that do not need 5 V logic.'],
  ['question'=>'Is it worth buying an official Espressif DevKitC versus a clone?','answer'=>'Clones (typically $4–5) work fine for prototyping and learning. For production or reliability-critical builds, genuine Espressif DevKitC boards or boards from reputable brands (Adafruit, SparkFun, Unexpected Maker) use higher-quality USB-to-serial chips (CP2102 vs cheap CH340 clones), better LDOs, and more accurately silkscreened pin labels. The main practical issue with clones is driver instability on Windows and occasional wrong GPIO labelling.'],
],
'related'      => [
  ['title'=>'ESP32 Variants Explained','slug'=>'esp32-variants-explained'],
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
  ['title'=>'Safe GPIO Pins on ESP32','slug'=>'safe-gpio-pins-esp32'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
],
'body_html'    => <<<'HTML'
<h2>More Boards Than You Think</h2>
<p>Search for "ESP32 board" online and you will encounter dozens of options at wildly different price points and form factors. Some have battery connectors; some have built-in displays; some are no larger than a postage stamp. Choosing the wrong board will not brick your project — the ESP32 chip inside is the same — but it will either waste money on features you do not use or leave you wishing you had capabilities that your board lacks. This guide maps the most common boards to the use cases they serve.</p>

<h2>The ESP32 DevKitC: The Default Starting Point</h2>
<p>The <strong>ESP32 DevKitC</strong> (Development Kit C) is Espressif's own reference design and the board that virtually every ESP32 tutorial is written for. It mounts an ESP32-WROOM-32 module on a 55 mm × 28 mm carrier PCB with a Micro-USB or USB-C connector, a CP2102 USB-to-serial chip, an AMS1117-3.3 LDO, and two buttons (EN for reset, BOOT for download mode). Pin headers expose all 38 GPIOs in two 19-pin rows.</p>

<p>The DevKitC is the right choice when: you are starting an ESP32 project for the first time, you want the widest tutorial compatibility, and you are prototyping on a breadboard. Its main limitation is its width — at 28.2 mm it bridges most of a standard 63 mm breadboard, leaving only one column of holes accessible on each side. Use two breadboards side by side or a wider half-pitch adapter to work comfortably.</p>

<p>The <strong>30-pin DevKit</strong> variant is slightly narrower and leaves two accessible breadboard columns per side. If you are ordering for a new project and expect to do heavy breadboarding, the 30-pin version is more convenient.</p>

<h2>NodeMCU-32S: Wide Compatibility and Accessible Pinout</h2>
<p>The NodeMCU-32S is a community-designed board inspired by the original NodeMCU for ESP8266. It is similar to the DevKitC but often uses a CH340 USB-to-serial chip (less reliable driver support on Windows than CP2102), includes voltage labels on silkscreen, and sometimes ships in a slightly narrower form factor that fits single breadboards better. Pin-for-pin the GPIO numbers are the same as the DevKitC. Library and sketch compatibility is identical.</p>

<p>Choose the NodeMCU-32S if it is significantly cheaper in your market and you are on Linux or macOS where CH340 drivers work seamlessly. On Windows, the CP2102-based DevKitC or LOLIN32 is more reliable out of the box.</p>

<h2>ESP32-WROOM-32 Module: For PCB Integration</h2>
<p>The WROOM-32 is the module that sits on the DevKitC and NodeMCU-32S boards. By itself it is a 18 mm × 25.5 mm rectangular component with castellated edges (half-holes along the perimeter for soldering) and a metal RF shield. It contains the ESP32-D0WD chip, 4 MB of SPI flash, passive components, and a PCB trace antenna — everything needed to add Wi-Fi to your own PCB design.</p>

<p>Use a bare WROOM-32 when designing a custom PCB for a finished product. You solder the module to your carrier board and add only the support circuitry your application needs. The WROOM-32U variant replaces the internal PCB antenna with a U.FL connector for an external antenna, useful when the board is installed inside a metal enclosure that would otherwise block the signal.</p>

<h2>ESP32-WROVER Module: When You Need PSRAM</h2>
<p>The WROVER adds 4 MB (or 8 MB in the WROVER-B) of SPI PSRAM to the WROOM-32 design in a slightly larger 18 mm × 31.4 mm package. This is the module to choose when your firmware buffers large data: a camera frame buffer, an audio stream, an HTTPS response body for a complex web server, or a large JSON document.</p>

<p>WROVER-based development boards include the <strong>ESP-WROVER-KIT</strong> (Espressif's official evaluation board with an onboard JTAG debugger, display connector, and microSD slot) and various third-party boards. The ESP-WROVER-KIT is expensive ($30–40) and best suited for firmware development work where hardware debugging via JTAG is needed. For most prototyping, a generic WROVER-I or WROVER-B development board at $8–12 is sufficient.</p>

<h2>LOLIN32 (WEMOS D32): Compact with LiPo Charging</h2>
<p>The LOLIN32 by WEMOS (now sold as the LOLIN D32) is a 26 mm × 51 mm board that adds a LiPo battery connector and charging circuit (via an IP5306 PMU chip) to the standard ESP32 feature set. Plug a single-cell 3.7 V LiPo into the JST connector and the board charges it from USB while simultaneously running the ESP32 from USB power. When USB is disconnected, the battery supplies the 3.3 V rail through a boost/buck converter.</p>

<p>The LOLIN D32 Pro extends this with a TF (micro SD) card slot and a second I²C header at the bottom edge for OLED displays and sensor shields. This makes it excellent for portable data loggers, handheld instruments, and wearables that need both USB convenience and battery operation.</p>

<h2>TinyPICO: Ultra-Low-Power in a Tiny Package</h2>
<p>TinyPICO by Unexpected Maker is a 18 mm × 32 mm board that prioritises power efficiency above all else. It uses an ME6211 LDO with 40 µA quiescent current (compared to 5–10 mA for the AMS1117 on most DevKitC boards), includes 4 MB PSRAM, a LiPo charging circuit, a battery voltage monitor, and a power enable pin for cutting power to external peripherals. Measured deep sleep current including the LDO is approximately 20–35 µA.</p>

<p>For wearables, environmental sensors, remote telemetry nodes, and any application where battery life is measured in months rather than days, TinyPICO (and its successor FeatherS2/S3 variants) is the correct choice. Its smaller size fits into enclosures that a full DevKitC would not.</p>

<h2>ESP32-CAM: Camera on a Budget</h2>
<p>The AI-Thinker ESP32-CAM mounts an OV2640 2 MP camera, 4 MB PSRAM, an SD card slot, and a white LED flash on a 40 mm × 27 mm board for approximately $5–8. It is one of the cheapest camera-capable embedded platforms available. The downside is the lack of a USB programming chip: you need an external FTDI adapter to upload firmware, connecting U0T to FTDI-RX, U0R to FTDI-TX, GND to GND, 5V to 5V, and GPIO 0 to GND during upload.</p>

<p>Use the ESP32-CAM for budget surveillance cameras, QR code scanners, face detection experiments, and remote monitoring applications where cost per unit is critical. For development comfort, budget $5 for a dedicated ESP32-CAM programmer board that integrates the FTDI chip and the GPIO 0 grounding circuit into a single USB-plug-in accessory.</p>

<h2>Board Selection Guide</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Board</th><th>Best For</th><th>PSRAM</th><th>Battery</th><th>Size</th><th>Approx Cost</th></tr></thead>
<tbody>
<tr><td>ESP32 DevKitC</td><td>Learning, tutorials, prototyping</td><td>No</td><td>No</td><td>55×28 mm</td><td>$5–8</td></tr>
<tr><td>NodeMCU-32S</td><td>Prototyping, Linux/Mac users</td><td>No</td><td>No</td><td>50×26 mm</td><td>$4–7</td></tr>
<tr><td>WROOM-32 module</td><td>Custom PCB integration</td><td>No</td><td>No</td><td>18×25 mm</td><td>$2–4</td></tr>
<tr><td>WROVER module</td><td>Camera, audio, large buffers</td><td>4/8 MB</td><td>No</td><td>18×31 mm</td><td>$4–8</td></tr>
<tr><td>LOLIN D32</td><td>Portable projects, LiPo power</td><td>No</td><td>Yes</td><td>26×51 mm</td><td>$6–10</td></tr>
<tr><td>LOLIN D32 Pro</td><td>Data loggers, SD card</td><td>4 MB</td><td>Yes</td><td>26×51 mm</td><td>$9–14</td></tr>
<tr><td>TinyPICO</td><td>Wearables, ultra-low power</td><td>4 MB</td><td>Yes</td><td>18×32 mm</td><td>$20–25</td></tr>
<tr><td>ESP32-CAM</td><td>Camera, surveillance, QR</td><td>4 MB</td><td>No</td><td>40×27 mm</td><td>$5–8</td></tr>
</tbody>
</table>
</div>

<h2>Key Advice for First-Time Buyers</h2>
<p>Start with an <strong>ESP32 DevKitC or NodeMCU-32S</strong>. Buy two — they are cheap and having a spare prevents days of delay if you accidentally damage a GPIO with a wiring mistake. Order from a reputable seller that stocks genuine Espressif modules (AliExpress tier-1 sellers, Amazon fulfilled, or direct from SparkFun/Adafruit for higher quality assurance). Avoid boards that do not show the GPIO silkscreen labels in the product photo — you will reference those labels constantly.</p>

<p>Once your project concept is proven on a DevKitC and you know exactly which GPIOs, peripheral interfaces, and power characteristics you need, choosing a more specialised board becomes straightforward. The DevKitC is an excellent development horse; specialised boards are for refined, space-constrained, or power-optimised production designs.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'esp32-beginner-mistakes',
'title'        => 'Common ESP32 Beginner Mistakes: 9 Errors That Waste Hours and How to Fix Them',
'meta_desc'    => 'Avoid the most common ESP32 beginner pitfalls — from boot loops and brownouts to ADC2 Wi-Fi conflicts, wrong baud rates, and Stack Overflow panics — with exact fixes.',
'read_time'    => '15 min read',
'phase'        => 'Phase 1: Beginner',
'faqs'         => [
  ['question'=>'Why does my ESP32 keep resetting with "Brownout detector was triggered"?','answer'=>'A brownout reset occurs when the 3.3 V supply voltage drops below ~2.4 V, usually caused by peak current during Wi-Fi transmit bursts (up to 500 mA). Fixes: use a USB cable under 1 m with 28 AWG or thicker power wires, add a 100 µF electrolytic capacitor between 3V3 and GND on the breadboard, use a powered USB hub or a dedicated 5 V/2 A supply instead of a laptop USB port.'],
  ['question'=>'My analogRead() returns noisy or wrong values. What is happening?','answer'=>'Several causes: (1) You are using an ADC2 pin while Wi-Fi is active — switch to ADC1 pins (GPIO 32–39). (2) The ADC reference is the 3.3 V supply, which fluctuates — add a 100 nF decoupling cap near the sensor. (3) Floating input — ensure the sensor or a pull-down resistor is always driving the pin. (4) Nonlinearity at the extremes — the ESP32 ADC is most accurate between 0.1 V and 3.1 V; avoid reading near 0 V and 3.3 V.'],
  ['question'=>'Why does my sketch upload successfully but the Serial Monitor shows nothing?','answer'=>'The Serial Monitor baud rate does not match Serial.begin(). The most common mismatch: Serial.begin(115200) in sketch but Serial Monitor set to 9600. Set both to 115200. Also ensure you are connecting to the correct COM port (Windows) or /dev/ttyUSBx port (Linux).'],
  ['question'=>'Why does my ESP32 enter an infinite boot loop after I upload a sketch?','answer'=>'Most common causes: (1) GPIO 0 is held low by a connected circuit — the chip stays in download mode. (2) GPIO 12 has a pull-up to 3.3 V, causing wrong flash voltage selection. (3) The sketch itself crashes immediately — watch the Serial Monitor at 115200 baud to see the panic message, which identifies the crashing line.'],
  ['question'=>'Can I connect two I2C sensors with the same address to one ESP32?','answer'=>'Not on the same I2C bus without hardware workarounds. Options: (1) If the sensor supports address selection via a pin (like BMP280 with SDO pin), set one sensor to each address. (2) Use the second I2C bus (Wire1) on different GPIO pins for the second sensor. (3) Use a TCA9548A I2C multiplexer to switch between sensors that cannot change address.'],
  ['question'=>'What causes "Guru Meditation Error: Core 1 panic\'d (LoadProhibited)"?','answer'=>'This is a memory access violation — usually a NULL pointer dereference or access to a freed or invalid memory address. Common causes: calling a library function before initialising it (e.g., calling display methods before display.begin()), accessing a String or array that went out of scope, or buffer overflow. Enable core dumps and read the backtrace to identify the crashing function.'],
  ['question'=>'Why do my GPIO outputs stay high briefly at boot before my sketch runs?','answer'=>'Some GPIO pins have boot-state values defined by the ESP32 hardware. GPIO 1 and 3 (UART TX/RX) toggle at boot as the ROM prints its startup log. GPIO 5 defaults high due to its strapping pull-up. These transient states can trigger connected relays, motors, or LEDs briefly. Add a small capacitor or RC delay on relay coil input, or use a normally-open relay so the brief HIGH does not cause an unintended action.'],
  ['question'=>'My Wi-Fi connection drops every few minutes. How do I fix it?','answer'=>'Check: (1) Signal strength — ESP32 Wi-Fi range is ~30 m indoors at best; move closer to the router. (2) Power — brownout resets cause Wi-Fi drops; fix power supply. (3) Add a watchdog and reconnect logic: if (WiFi.status() != WL_CONNECTED) { WiFi.reconnect(); }. (4) Check router DHCP lease time — some routers disconnect devices with short leases. (5) Disable power-saving on the router for the ESP32 MAC address.'],
  ['question'=>'Why does delay() stop working properly when I use millis() timing in the same sketch?','answer'=>'delay() and millis()-based timing are not incompatible in principle, but mixing them causes confusion. delay() blocks execution completely, including event processing; millis() is non-blocking and counts elapsed time. If your loop has long delay() calls, the millis() comparison will trigger as soon as the delay ends, causing unexpected behaviour. Refactor to use only millis()-based non-blocking timing patterns when multiple timed events exist.'],
  ['question'=>'I uploaded to the wrong ESP32 in my project. How do I fix it?','answer'=>'Select the correct COM port in the Arduino IDE Tools menu before uploading. On Windows open Device Manager to see which COM port corresponds to which USB connection. If both boards are connected simultaneously, unplug all but the target before uploading. For larger projects, add a unique board ID compiled into the firmware using #define BOARD_ID "sensor-01" so Serial output helps identify which device is which.'],
],
'related'      => [
  ['title'=>'Safe GPIO Pins on ESP32','slug'=>'safe-gpio-pins-esp32'],
  ['title'=>'Boot Strapping Pins Explained','slug'=>'esp32-boot-strapping-pins'],
  ['title'=>'ESP32 Power Consumption Guide','slug'=>'esp32-power-consumption'],
  ['title'=>'ESP32 Pinout Guide','slug'=>'esp32-pinout-guide'],
],
'body_html'    => <<<'HTML'
<h2>Mistakes Are Faster Than Reading Documentation</h2>
<p>Every ESP32 developer has a list of hours lost to debugging problems that, in retrospect, had obvious causes. The frustrating reality is that many of these mistakes are not obvious at all when you first encounter them — the error messages are cryptic, the behaviour is inconsistent, and the root cause often hides beneath an assumption you did not know you were making. This guide documents the nine most common ESP32 beginner mistakes, explains exactly why each one happens, and gives you the specific fix.</p>

<h2>Mistake 1: Using ADC2 Pins While Wi-Fi is Active</h2>
<p>ESP32 has two ADC units. ADC2 is shared with the Wi-Fi radio hardware. When Wi-Fi is enabled and connecting (or connected), any call to <code>analogRead()</code> on an ADC2 pin will fail, returning <code>-1</code> or a completely wrong value. The affected pins are GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, and 27.</p>

<p><strong>How it manifests:</strong> Your analog sensor reads fine during setup (before Wi-Fi connects), then returns garbage or <code>4095</code> constantly after <code>WiFi.begin()</code> completes.</p>

<p><strong>Fix:</strong> Use only ADC1 pins for analog reads in Wi-Fi projects. ADC1 pins are GPIO 32, 33, 34, 35, 36 (VP), and 39 (VN). Move your potentiometer, LDR, or analog sensor to GPIO 32 or 34 and <code>analogRead()</code> will return accurate values regardless of Wi-Fi state.</p>

<h2>Mistake 2: Power Supply Brownout Under Wi-Fi Load</h2>
<p>The ESP32's Wi-Fi transmitter draws up to 500 mA in short bursts. Most laptop USB ports are rated at 500 mA total — shared with the USB hub chip, the keyboard, and any other devices on the same hub. Long or thin USB cables add resistance, dropping voltage. The ESP32 has an onboard brownout detector that resets the chip when 3.3 V drops below ~2.4 V, producing the telltale message: <code>Brownout detector was triggered</code>.</p>

<p><strong>How it manifests:</strong> Random resets during Wi-Fi connection, OTA updates, or HTTP requests. The Serial Monitor prints "Brownout detector was triggered" followed by a reset reason code.</p>

<p><strong>Fix:</strong> Use a dedicated 5 V / 2 A USB wall adapter (not a laptop USB port or cheap phone charger). Use a USB cable under 1 m with 28 AWG or thicker power conductors. Add a 100 µF electrolytic capacitor between the 3.3 V and GND pins on your breadboard — this buffers peak current spikes. If the problem persists, measure the 3.3 V rail with a multimeter during a Wi-Fi transmit burst; any reading below 3.0 V indicates an inadequate supply.</p>

<h2>Mistake 3: Connecting GPIO 6–11 to External Circuits</h2>
<p>GPIO 6, 7, 8, 9, 10, and 11 are internally connected to the SPI flash interface. Any external connection to these pins disrupts communication between the ESP32 and the flash chip holding your firmware. The result is usually an immediate boot loop, or the ESP32 refusing to accept firmware uploads.</p>

<p><strong>How it manifests:</strong> The board endlessly prints boot messages and resets, or the Arduino IDE fails to upload with a "Failed to connect" error even though you can see the board in Device Manager. The problem started after you wired something to a GPIO in the 6–11 range.</p>

<p><strong>Fix:</strong> Disconnect anything wired to GPIO 6–11 immediately. On the 38-pin DevKitC these pins are physically absent from the headers — if you have a different board or a custom PCB, verify the silkscreen labels carefully. Never use GPIO 6–11 in user code.</p>

<h2>Mistake 4: String Heap Fragmentation and Memory Exhaustion</h2>
<p>The Arduino <code>String</code> class is convenient but dangerous in long-running ESP32 sketches. Each <code>String</code> concatenation with <code>+=</code> or <code>+</code> creates a new heap allocation and immediately frees the old one. With many small allocations and frees of different sizes, the heap becomes fragmented — you may have 100 KB free in total but no single contiguous block large enough to satisfy a 50 KB allocation. The symptom is a working sketch that crashes after hours or days, often in the middle of an HTTP request or JSON parse.</p>

<p><strong>How it manifests:</strong> The ESP32 runs fine for hours, then crashes with a "panic" or returns a NULL from malloc. <code>ESP.getFreeHeap()</code> may still show a non-zero value when the crash happens.</p>

<p><strong>Fix:</strong> Reserve fixed-size buffers and use <code>snprintf()</code> and <code>strcat()</code> instead of <code>String</code> concatenation in long-running code. Check <code>ESP.getMaxAllocHeap()</code> to see the largest available contiguous block. For JSON, use ArduinoJSON's <code>StaticJsonDocument&lt;N&gt;</code> with a stack-allocated buffer of known size. For HTTP bodies, stream the response in chunks rather than buffering the entire body as a <code>String</code>.</p>

<h2>Mistake 5: Wrong Baud Rate on Serial Monitor</h2>
<p>This mistake is common enough that it deserves a section. The Arduino IDE's Serial Monitor has a baud rate dropdown in its bottom-right corner. If it does not match the rate in <code>Serial.begin()</code>, the output is garbage characters or nothing at all.</p>

<p><strong>How it manifests:</strong> The Serial Monitor shows random characters like <code>???⸮⸮⸮</code> or shows nothing. Your sketch uploaded successfully and the device is running (you can tell because the LED blinks), but Serial output is missing.</p>

<p><strong>Fix:</strong> Set both <code>Serial.begin(115200)</code> in your sketch and the Serial Monitor dropdown to 115200. The ESP32 ROM bootloader also prints at 115200, so keeping everything at 115200 means you see both boot messages and sketch output in one monitor session. After changing the Serial Monitor baud rate, press Enter in the monitor to request fresh output.</p>

<h2>Mistake 6: Not Handling Wi-Fi Disconnection in Long-Running Sketches</h2>
<p>Wi-Fi connections are not permanent. A router restart, a signal drop, or DHCP lease expiry can disconnect an ESP32 that has been running for days. If your sketch assumes Wi-Fi is always connected and calls <code>client.connect()</code> or <code>http.GET()</code> on a disconnected socket, it will hang or return error codes silently, accumulating failures without recovering.</p>

<p><strong>How it manifests:</strong> Your ESP32 works perfectly for the first day, then stops posting data. The device is running (LED blinks on), but no data arrives at the server. A reboot fixes it temporarily.</p>

<p><strong>Fix:</strong> Add a connection check before every network operation:</p>
<pre><code>if (WiFi.status() != WL_CONNECTED) {
  Serial.println("Wi-Fi lost. Reconnecting...");
  WiFi.disconnect();
  WiFi.begin(SSID, PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(500);
  }
}
if (WiFi.status() == WL_CONNECTED) {
  // proceed with HTTP call
}</code></pre>
<p>Add a hardware watchdog as a last resort: <code>esp_task_wdt_init(30, true)</code> resets the chip if your main loop does not call <code>esp_task_wdt_reset()</code> within 30 seconds — catching truly stuck states.</p>

<h2>Mistake 7: GPIO Output State at Boot Causing Relay or Motor Triggers</h2>
<p>Several ESP32 GPIO pins have defined states before your sketch begins: GPIO 1 and 3 toggle during the ROM boot log, GPIO 5 starts high (boot strapping pull-up), and some pins may float briefly before being driven. If you connect a relay module directly to these pins, the brief transient can trigger the relay at power-on, even before your sketch runs — an alarming behaviour for mains-controlled devices.</p>

<p><strong>How it manifests:</strong> A relay or motor briefly activates the instant the ESP32 is powered, before the sketch logic could have turned it on.</p>

<p><strong>Fix:</strong> Use active-low relay modules (which require a LOW signal to energise the coil) and configure the control GPIO as OUTPUT with a HIGH initial state: <code>pinMode(relayPin, OUTPUT); digitalWrite(relayPin, HIGH);</code>. Set this in the first line of setup() and choose a relay control pin that starts high by default (GPIO 5, for example, which has a boot-time pull-up). For motor controllers, add an enable line that your sketch explicitly raises after initialising.</p>

<h2>Mistake 8: Forgetting to Call Wire.begin() or SPI.begin()</h2>
<p>I²C and SPI buses must be initialised before any sensor library can use them. The Arduino ESP32 core does not automatically start <code>Wire</code> or <code>SPI</code>. If you include a sensor library that uses I²C but forget <code>Wire.begin()</code>, the first <code>sensor.begin()</code> call may appear to succeed (some libraries do not check return values) but all subsequent reads return zero or garbage.</p>

<p><strong>How it manifests:</strong> BME280, MPU6050, SSD1306, and similar I²C sensors all read 0 or return NaN for every value. The sensor is wired correctly, the address matches, but data is always wrong.</p>

<p><strong>Fix:</strong> Always add these lines to setup() before any sensor initialisation:</p>
<pre><code>Wire.begin();         // default: SDA=GPIO21, SCL=GPIO22
// or with custom pins:
Wire.begin(sdaPin, sclPin);</code></pre>
<p>For SPI sensors: <code>SPI.begin();</code> or <code>SPI.begin(sckPin, misoPin, mosiPin, csPin);</code>. Use an I²C scanner sketch to confirm the sensor address is visible on the bus before adding it to your main project.</p>

<h2>Mistake 9: Blocking Loops That Starve the Wi-Fi Stack</h2>
<p>The ESP32's Arduino core runs the Wi-Fi stack as a FreeRTOS task on Core 0 with a specific priority. If your sketch runs a long blocking loop on Core 1 (where Arduino loop() executes) that never yields — a <code>while(true)</code> polling loop, a <code>delay(50000)</code> call, or intensive computation — the FreeRTOS scheduler may not give the Wi-Fi task enough processor time. The result is Wi-Fi disconnections, HTTP timeouts, or OTA update failures mid-transfer.</p>

<p><strong>How it manifests:</strong> MQTT clients disconnect during heavy computation. An HTTP POST that worked fine during idle fails when you add an FFT or image processing routine to the loop. OTA updates stall at 50% and time out.</p>

<p><strong>Fix:</strong> Prefer non-blocking code patterns using <code>millis()</code> instead of <code>delay()</code> for timing. For genuinely long computations, yield the CPU periodically with <code>yield()</code> or <code>vTaskDelay(1)</code> every few thousand iterations. For very long operations (audio processing, FFT of large buffers), pin the computation to Core 1 with a FreeRTOS task and keep loop() lightweight:</p>
<pre><code>void compute_task(void *params) {
  while (true) {
    do_heavy_computation();
    vTaskDelay(10);  // yield every cycle
  }
}

void setup() {
  xTaskCreatePinnedToCore(compute_task, "compute", 8192, NULL, 1, NULL, 1);
}</code></pre>

<h2>Building Good Habits Early</h2>
<p>Most of these mistakes share a common thread: they result from assumptions carried over from simpler microcontrollers (Arduino Uno, for example) that do not apply to the ESP32's more complex hardware. The ESP32 has a radio that shares ADC resources, a boot sequence that reads specific GPIO states, a memory model with a heap that can fragment, and an RTOS that requires cooperative scheduling. Internalising these differences early — rather than discovering them one crash at a time — is what separates an ESP32 developer who ships projects from one who spends days debugging inexplicable failures.</p>
HTML,
],

]; // end return
