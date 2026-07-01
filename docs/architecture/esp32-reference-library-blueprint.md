\# ESP32 Engine



\## Reference Library Blueprint



\*\*Status:\*\* Approved Architecture

\*\*Purpose:\*\* Internal planning document. Not part of the public website.

\*\*Last Updated:\*\* July 2026



\---



\## 1. Reference Library Structure



A reference library is different from Academy — Academy teaches step-by-step, Reference answers "what is X and how does it work" in under 30 seconds. Structure it as a standalone hub: `esp32engine.com/reference/`



```

/reference/

├── /gpio/

├── /adc/

├── /dac/

├── /pwm/

├── /i2c/

├── /spi/

├── /uart/

├── /interrupts/

├── /timers/

├── /deep-sleep/

├── /wifi/

├── /bluetooth-ble/

├── /esp-now/

├── /boot-pins/

├── /pinout/

├── /power/

├── /flash-psram/

├── /freertos-basics/

└── /esp-idf-basics/

```



\*\*Three-tier grouping\*\* (for navigation menu, not URLs):



\- \*\*Core I/O\*\* — GPIO, ADC, DAC, PWM, Boot Pins, Pinout

\- \*\*Communication\*\* — I2C, SPI, UART, WiFi, BLE, ESP-NOW

\- \*\*System \& Power\*\* — Interrupts, Timers, Deep Sleep, Power, Flash/PSRAM, FreeRTOS, ESP-IDF



Each reference page cross-links to Academy missions (teaching) and Components/Projects (application) — this is what turns a dictionary into a library.



\---



\## 2. Topic-by-Topic Blueprint



Format per topic: Search intent → Who needs it → Must answer → Tables → Mistakes → Academy links → Components → Projects → SEO title → Meta description



\### GPIO



| Field | Content |

|---|---|

| Search intent | "ESP32 GPIO pins", "which GPIO can I use" |

| Who needs it | Absolute beginners + engineers double-checking pin safety |

| Must answer | Which pins are input-only, which are safe at boot, max current per pin |

| Tables | Full GPIO list (input/output/input-only/strapping), max current table |

| Mistakes | Using GPIO 34–39 as output, ignoring strapping pin states |

| Academy | "Blink LED", "Button Input" |

| Components | LED, pushbutton, resistor |

| Projects | Traffic light, button counter |

| SEO title | ESP32 GPIO Pinout \& Rules — Full Reference |

| Meta description | Complete ESP32 GPIO reference: input-only pins, safe pins, current limits, and common mistakes explained simply. |



\### ADC



| Field | Content |

|---|---|

| Search intent | "ESP32 ADC pins", "ESP32 analog read accuracy" |

| Who needs it | Beginners reading sensors + engineers debugging noisy readings |

| Must answer | Which pins support ADC, why WiFi affects ADC2, resolution/voltage range |

| Tables | ADC1 vs ADC2 pin list, resolution/voltage table |

| Mistakes | Using ADC2 while WiFi is on, expecting linear 0–3.3V without calibration |

| Academy | "Read a Potentiometer", "Light Sensor Basics" |

| Components | Potentiometer, LDR, soil moisture sensor |

| Projects | Light-based night lamp, soil moisture alarm |

| SEO title | ESP32 ADC Guide — Pins, Accuracy \& Limitations |

| Meta description | Learn which ESP32 pins support ADC, why readings drift, and how to get accurate analog values. |



\### DAC



| Field | Content |

|---|---|

| Search intent | "ESP32 DAC pins", "ESP32 analog output" |

| Who needs it | Engineers building audio/analog output projects |

| Must answer | Which 2 pins support DAC, resolution, use cases |

| Tables | DAC pin table, resolution comparison vs ADC |

| Mistakes | Expecting DAC on any pin, confusing DAC with PWM |

| Academy | "Simple Audio Tone Output" |

| Components | Speaker, buzzer |

| Projects | Basic waveform generator |

| SEO title | ESP32 DAC Pins Explained — Analog Output Reference |

| Meta description | Which ESP32 pins output true analog signals, and how DAC differs from PWM. |



\### PWM



| Field | Content |

|---|---|

| Search intent | "ESP32 PWM", "ESP32 servo control", "LEDC" |

| Who needs it | Beginners dimming LEDs/servos + engineers tuning frequency |

| Must answer | How LEDC channels work, frequency vs resolution tradeoff |

| Tables | Channel count, frequency/resolution tradeoff table |

| Mistakes | Assuming Arduino-style analogWrite works identically, channel conflicts |

| Academy | "Dim an LED", "Control a Servo" |

| Components | Servo motor, RGB LED |

| Projects | Mood lamp, robotic arm |

| SEO title | ESP32 PWM \& LEDC Reference — Servo and LED Control |

| Meta description | Full ESP32 PWM reference: LEDC channels, frequency limits, and servo control basics. |



\### I2C



| Field | Content |

|---|---|

| Search intent | "ESP32 I2C pins", "I2C address conflict" |

| Who needs it | Beginners connecting sensors + engineers debugging bus errors |

| Must answer | Default SDA/SCL pins, pull-up requirement, multi-device addressing |

| Tables | Default pin table, common sensor addresses |

| Mistakes | Missing pull-up resistors, address collisions |

| Academy | "Connect an OLED Display", "Read a Temperature Sensor" |

| Components | OLED, BME280, RTC module |

| Projects | Weather station, mini clock |

| SEO title | ESP32 I2C Pinout \& Setup Reference |

| Meta description | ESP32 I2C reference: default pins, pull-up resistors, and fixing address conflicts. |



\### SPI



| Field | Content |

|---|---|

| Search intent | "ESP32 SPI pins", "HSPI vs VSPI" |

| Who needs it | Engineers using SD cards, displays, sensors |

| Must answer | Default SPI pins, dual SPI buses, speed limits |

| Tables | HSPI/VSPI pin table, max clock speed |

| Mistakes | Sharing CS pins incorrectly, wiring MISO/MOSI swapped |

| Academy | "SD Card Logger", "TFT Display Basics" |

| Components | SD card module, TFT display |

| Projects | Data logger, mini gallery display |

| SEO title | ESP32 SPI Reference — Pins, Buses \& Speed |

| Meta description | Complete ESP32 SPI guide: HSPI vs VSPI pins, wiring rules, and speed limits. |



\### UART



| Field | Content |

|---|---|

| Search intent | "ESP32 UART pins", "ESP32 Serial2" |

| Who needs it | Beginners debugging via Serial Monitor + engineers using GPS/modules |

| Must answer | Number of UARTs, default pins, baud rate basics |

| Tables | UART0/1/2 pin table |

| Mistakes | Using UART0 pins for other purposes, mismatched baud rates |

| Academy | "Serial Monitor Basics", "Connect a GPS Module" |

| Components | GPS module, Bluetooth serial module |

| Projects | GPS tracker |

| SEO title | ESP32 UART Reference — Pins \& Serial Communication |

| Meta description | ESP32 UART pin reference and serial communication basics for beginners and engineers. |



\### Interrupts



| Field | Content |

|---|---|

| Search intent | "ESP32 interrupt example", "attachInterrupt ESP32" |

| Who needs it | Intermediate learners + engineers handling real-time events |

| Must answer | Which pins support interrupts, IRAM\_ATTR requirement, debouncing |

| Tables | Interrupt-capable pins, trigger mode table (RISING/FALLING/CHANGE) |

| Mistakes | Doing heavy work inside ISR, missing debounce |

| Academy | "Button Interrupt Basics" |

| Components | Pushbutton, PIR sensor |

| Projects | Motion alarm |

| SEO title | ESP32 Interrupts Reference — Pins \& Best Practices |

| Meta description | Learn which ESP32 pins support interrupts and how to avoid common ISR mistakes. |



\### Timers



| Field | Content |

|---|---|

| Search intent | "ESP32 hardware timer", "ESP32 millis vs timer" |

| Who needs it | Engineers building precise timing tasks |

| Must answer | Hardware timer count, timer vs millis(), interrupt-driven timing |

| Tables | Timer group/count table |

| Mistakes | Using delay() in time-critical code |

| Academy | "Precise Timing with Hardware Timers" |

| Components | — |

| Projects | Metronome, precision blinker |

| SEO title | ESP32 Timers Reference — Hardware Timer Guide |

| Meta description | ESP32 hardware timer reference: how many timers, how they differ from millis(). |



\### Deep Sleep



| Field | Content |

|---|---|

| Search intent | "ESP32 deep sleep power saving", "ESP32 wake up sources" |

| Who needs it | Engineers building battery-powered projects |

| Must answer | Power consumption numbers, wake-up sources, RTC memory |

| Tables | Sleep mode comparison table, wake source table |

| Mistakes | Forgetting RTC\_DATA\_ATTR, wrong wake pin choice |

| Academy | "Battery-Powered Sensor Node" |

| Components | Battery holder, PIR sensor |

| Projects | Solar weather node |

| SEO title | ESP32 Deep Sleep Reference — Power Saving Guide |

| Meta description | ESP32 deep sleep modes, wake-up sources, and power consumption explained. |



\### WiFi



| Field | Content |

|---|---|

| Search intent | "ESP32 WiFi connect code", "ESP32 WiFi range" |

| Who needs it | Beginners connecting to internet + engineers optimizing range/power |

| Must answer | STA vs AP mode, connection troubleshooting, power draw |

| Tables | WiFi mode comparison, power draw table |

| Mistakes | Using ADC2 with WiFi on, weak power supply causing brownouts |

| Academy | "Connect ESP32 to WiFi", "Build a Web Server" |

| Components | — |

| Projects | Home automation dashboard |

| SEO title | ESP32 WiFi Reference — Modes, Setup \& Troubleshooting |

| Meta description | ESP32 WiFi reference: STA/AP modes, connection issues, and power considerations. |



\### Bluetooth / BLE



| Field | Content |

|---|---|

| Search intent | "ESP32 BLE vs Bluetooth Classic", "ESP32 BLE example" |

| Who needs it | Engineers building phone-connected projects |

| Must answer | Classic vs BLE difference, GATT basics, range/power |

| Tables | Classic vs BLE comparison table |

| Mistakes | Using Classic BT (not on all ESP32 variants), pairing confusion |

| Academy | "BLE Basics with a Phone App" |

| Components | — |

| Projects | BLE controlled robot |

| SEO title | ESP32 Bluetooth \& BLE Reference Guide |

| Meta description | ESP32 Bluetooth Classic vs BLE explained with GATT basics and common pitfalls. |



\### ESP-NOW



| Field | Content |

|---|---|

| Search intent | "ESP32 ESP-NOW vs WiFi", "ESP-NOW range" |

| Who needs it | Engineers building device-to-device projects without a router |

| Must answer | How ESP-NOW differs from WiFi, MAC address pairing, range/limits |

| Tables | ESP-NOW vs WiFi vs BLE comparison |

| Mistakes | Wrong MAC address, channel mismatch |

| Academy | "Two ESP32s Talking Without WiFi" |

| Components | Two ESP32 boards |

| Projects | Wireless remote control |

| SEO title | ESP32 ESP-NOW Reference — Fast Peer-to-Peer Communication |

| Meta description | ESP32 ESP-NOW reference: setup, MAC pairing, range, and common errors. |



\### Boot Pins



| Field | Content |

|---|---|

| Search intent | "ESP32 boot mode pins", "ESP32 won't upload code" |

| Who needs it | Beginners hitting upload errors + engineers designing custom PCBs |

| Must answer | Which pins are strapping pins, safe states at boot |

| Tables | Strapping pin table with required boot-time state |

| Mistakes | Connecting pull-down to GPIO0/2 incorrectly, blocking upload mode |

| Academy | "Fixing Upload Errors" |

| Components | — |

| Projects | — |

| SEO title | ESP32 Boot Pins \& Strapping Pins Reference |

| Meta description | ESP32 boot pin reference: strapping pins, safe states, and fixing upload failures. |



\### Pinout



| Field | Content |

|---|---|

| Search intent | "ESP32 pinout diagram", "ESP32 devkit pinout" |

| Who needs it | Everyone — the single most-searched reference page |

| Must answer | Full labeled pinout for common boards (DevKit V1, WROOM-32) |

| Tables | Master pinout table by board variant |

| Mistakes | Assuming all ESP32 boards have identical pinouts |

| Academy | All missions link here |

| Components | — |

| Projects | — |

| SEO title | ESP32 Pinout Diagram — Complete Reference (DevKit V1) |

| Meta description | Full labeled ESP32 pinout diagram covering DevKit V1 and WROOM-32 boards. |



\### Power



| Field | Content |

|---|---|

| Search intent | "ESP32 power supply requirements", "ESP32 brownout" |

| Who needs it | Engineers debugging resets/brownouts |

| Must answer | Voltage/current requirements, brownout causes, USB vs battery power |

| Tables | Voltage tolerance table, current draw by mode |

| Mistakes | Underpowered USB cable, using 5V directly on 3.3V pins |

| Academy | "Fixing Random Resets" |

| Components | Voltage regulator, battery |

| Projects | — |

| SEO title | ESP32 Power Supply Reference — Voltage, Current \& Brownouts |

| Meta description | ESP32 power reference: voltage tolerances, current needs, and fixing brownout resets. |



\### Flash / PSRAM



| Field | Content |

|---|---|

| Search intent | "ESP32 flash size", "ESP32 PSRAM enable" |

| Who needs it | Engineers running large/memory-heavy projects |

| Must answer | Flash size variants, how to check/enable PSRAM |

| Tables | Flash size comparison, PSRAM-enabled board list |

| Mistakes | Assuming all boards have PSRAM, wrong partition scheme |

| Academy | "Memory Basics on ESP32" |

| Components | — |

| Projects | Camera-based project |

| SEO title | ESP32 Flash \& PSRAM Reference Guide |

| Meta description | ESP32 flash size and PSRAM reference: variants, detection, and configuration. |



\### FreeRTOS Basics



| Field | Content |

|---|---|

| Search intent | "ESP32 FreeRTOS tasks", "ESP32 multitasking" |

| Who needs it | Intermediate/advanced engineers writing concurrent code |

| Must answer | What a task is, core pinning, priority basics |

| Tables | Task priority table, core assignment table |

| Mistakes | Blocking a task forever, priority inversion |

| Academy | "Multitasking on ESP32" |

| Components | — |

| Projects | Multi-sensor logger |

| SEO title | ESP32 FreeRTOS Basics — Tasks \& Multitasking Reference |

| Meta description | ESP32 FreeRTOS reference: tasks, core pinning, and priority basics explained simply. |



\### ESP-IDF Basics



| Field | Content |

|---|---|

| Search intent | "ESP-IDF vs Arduino", "ESP-IDF getting started" |

| Who needs it | Engineers moving beyond Arduino framework |

| Must answer | When to use ESP-IDF over Arduino, toolchain basics |

| Tables | Arduino vs ESP-IDF comparison table |

| Mistakes | Mixing frameworks incorrectly, skipping menuconfig |

| Academy | "Beyond Arduino: Intro to ESP-IDF" |

| Components | — |

| Projects | — |

| SEO title | ESP-IDF Basics — Reference Guide for ESP32 |

| Meta description | ESP-IDF vs Arduino framework compared, plus toolchain basics for ESP32 engineers. |



\---



\## 3. Top 10 Pages to Create First



Ranked by search demand × internal linking impact × learner value:



| Rank | Page | Why first |

|---|---|---|

| 1 | Pinout | Highest search volume, every other page links here |

| 2 | GPIO | Foundation page, needed before any project |

| 3 | WiFi | Most-searched functional topic, huge project fan-out |

| 4 | Boot Pins | Solves the #1 beginner frustration (upload failures) — high retention value |

| 5 | PWM | High project relevance (LEDs, servos), strong search demand |

| 6 | I2C | Gateway to most sensor/display projects |

| 7 | Deep Sleep | High engineer search demand, differentiates from beginner-only sites |

| 8 | ADC | Common beginner confusion point, frequent searches |

| 9 | Power | Solves recurring "random reset" support questions |

| 10 | Bluetooth/BLE | Growing search interest, project variety |



\*(SPI, UART, Interrupts, Timers, ESP-NOW, DAC, Flash/PSRAM, FreeRTOS, ESP-IDF form wave 2.)\*



\---



\## 4. Recommended Page Template



Every reference page follows the same skeleton — consistency builds trust and speeds production:



1\. \*\*Quick Answer box\*\* (2–3 lines, answers the search query instantly — for featured snippets)

2\. \*\*Reference Table\*\* (pins/values/specs — the "lookup" core)

3\. \*\*Explanation\*\* (plain-English, 150–250 words)

4\. \*\*Common Mistakes\*\* (bulleted, 3–5 items)

5\. \*\*Related Academy Missions\*\* (learn it hands-on)

6\. \*\*Related Components / Projects\*\* (apply it)

7\. \*\*FAQ block\*\* (3–5 Q\&A, schema-marked)

8\. \*\*"Next: related reference page"\*\* links



This template is repeatable across all 19 pages without redesigning anything.



\---



\## 5. Internal Linking Strategy



\- \*\*Pinout page = hub.\*\* Every other reference page links back to it; it links out to all 19.

\- \*\*Reference ↔ Academy (bidirectional):\*\* each Academy mission that uses a concept links to its reference page; each reference page links to the missions that use it. This turns "learning" and "lookup" into one ecosystem instead of two silos.

\- \*\*Reference ↔ Components/Projects:\*\* reference pages link to real components/projects using that concept, increasing time-on-site and project discovery.

\- \*\*Cluster linking:\*\* group pages link sideways (I2C ↔ SPI ↔ UART as "communication protocols"; GPIO ↔ ADC ↔ PWM as "core I/O") so Google sees topical clusters, not isolated pages.

\- \*\*Breadcrumbs\*\* on every page: Home → Reference → \[Category] → \[Page], reinforcing hierarchy for both users and crawlers.



\---



\## 6. Why This Library Strengthens ESP32 Engine's Authority



\- \*\*Captures a second search intent.\*\* Academy wins "how to learn ESP32"; Reference wins "ESP32 \[X] pinout/specs" — a much higher-volume, often higher-intent query type (engineers, not just kids).

\- \*\*Increases dwell time and return visits.\*\* Reference pages get bookmarked and revisited during actual project work, unlike one-time tutorial reads.

\- \*\*Builds topical authority for SEO.\*\* 19 interlinked, well-structured technical pages signal to Google that ESP32 Engine is a comprehensive ESP32 resource, not just a kids' tutorial site — this lifts rankings for Academy content too.

\- \*\*Bridges the two audiences you already serve.\*\* Kids/beginners get simplified answers; engineers get precise tables — same page, different sections, no separate site needed.

\- \*\*Differentiates from competitors.\*\* Most ESP32 tutorial sites (Random Nerd Tutorials, etc.) mix reference and tutorial content loosely; a dedicated, consistently templated Reference Library is a clear structural advantage.



\---



> \*\*Note:\*\* This document is internal repository documentation only. It must not be included in the sitemap, navigation, search index, website build, or any public-facing page.



