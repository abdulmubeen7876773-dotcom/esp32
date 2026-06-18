<?php
/* Phase 2 guide data — guides 1-5 */
return [

/* ============================================================ */
[
'slug'         => 'installing-arduino-ide-esp32',
'title'        => 'Installing Arduino IDE for ESP32: Complete Setup Guide for Windows, Mac, and Linux',
'meta_desc'    => 'Step-by-step guide to installing Arduino IDE 2.x and adding ESP32 board support via the Board Manager. Covers Windows, macOS, and Linux with driver installation and first upload.',
'read_time'    => '16 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'Which version of Arduino IDE should I use for ESP32?','answer'=>'Arduino IDE 2.x is recommended. It includes a built-in library manager, inline error highlighting, a debugging interface, and better auto-completion than IDE 1.x. The ESP32 Arduino core works identically on both versions. IDE 1.8.x is still supported but receives no new features — migrate to 2.x unless you have a specific compatibility reason not to.'],
  ['question'=>'Why does my ESP32 not appear in the Port list?','answer'=>'The most common cause is a missing USB-to-serial driver. DevKitC boards with CP2102 need the Silicon Labs CP210x driver; boards with CH340 need the CH340/CH341 driver. On Windows, open Device Manager and look for a device with a yellow warning triangle under Ports or Unknown Devices. Download the correct driver, install it, and replug the USB cable.'],
  ['question'=>'What is the correct Board Manager URL for ESP32?','answer'=>'The official Espressif Arduino core URL is: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json — Add this in Arduino IDE under File → Preferences → Additional Boards Manager URLs. Then open Tools → Board → Boards Manager, search "esp32 by Espressif Systems", and install.'],
  ['question'=>'How do I select the correct ESP32 board in Arduino IDE?','answer'=>'Go to Tools → Board → ESP32 Arduino → and select your board. For a standard 38-pin DevKitC use "ESP32 Dev Module". For NodeMCU-32S use "NodeMCU-32S". For ESP32-CAM use "AI Thinker ESP32-CAM". The board selection determines the default flash size, partition scheme, and PSRAM settings compiled into your sketch.'],
  ['question'=>'My upload fails with "Failed to connect to ESP32: Timed out waiting for packet header". How do I fix it?','answer'=>'Hold the BOOT button on the ESP32 board, click Upload in the IDE, and release BOOT when you see "Connecting..." in the IDE console. This manually triggers download mode. If this works but automatic upload does not, check that your board has a quality CP2102 or CH340 chip — cheap clones sometimes do not correctly implement the DTR/RTS boot sequence.'],
  ['question'=>'Can I install Arduino IDE without administrator rights?','answer'=>'On Windows, the full installer requires admin rights. Download the ZIP version instead (arduino.cc → Software → Windows ZIP file) and extract it to a folder in your user directory. The portable version runs without installation. On Linux, download the AppImage version which needs no installation. On macOS, drag the .app to your Applications folder with user write access.'],
  ['question'=>'How do I install ESP32 libraries like WiFi.h?','answer'=>'WiFi.h is included with the ESP32 Arduino core — no separate install needed. For third-party libraries (PubSubClient, ArduinoJSON, Adafruit sensors), use Tools → Manage Libraries in the IDE, search the library name, and click Install. Alternatively, download the ZIP from GitHub and install via Sketch → Include Library → Add .ZIP Library.'],
  ['question'=>'What upload speed should I use for ESP32?','answer'=>'921600 baud is the default and works on most quality boards with a direct USB connection. If uploads fail or are unreliable, drop to 460800 or 115200 baud in Tools → Upload Speed. On some laptops and USB hubs, high baud rates are unreliable; 460800 is a good compromise of speed and reliability.'],
  ['question'=>'Is there a way to verify my ESP32 setup before writing any code?','answer'=>'Yes. Open File → Examples → WiFi → WiFiScan in the Arduino IDE. Select your ESP32 board and port, click Upload. Open the Serial Monitor at 115200 baud. You should see a list of nearby Wi-Fi networks within a few seconds. If this works, your toolchain is correctly installed, the board communicates, and Wi-Fi hardware is functional.'],
  ['question'=>'How often should I update the ESP32 Arduino core?','answer'=>'Update when a new stable release fixes a bug you have encountered, adds support for a new board variant you need, or improves library compatibility. Do not update blindly mid-project — breaking changes in minor versions can require code changes. Check the ESP32 Arduino core release notes on GitHub before updating in the middle of active development.'],
],
'related' => [
  ['title'=>'ESP32 Board Manager Setup','slug'=>'esp32-board-manager-setup'],
  ['title'=>'First ESP32 Program','slug'=>'first-esp32-program'],
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
  ['title'=>'PlatformIO vs Arduino IDE','slug'=>'platformio-vs-arduino-ide'],
],
'body_html' => <<<'HTML'
<h2>What You Will Have at the End of This Guide</h2>
<p>By the time you finish this guide you will have Arduino IDE 2.x installed on your computer, the ESP32 board support package installed via the Board Manager, the correct USB driver for your board, and a verified end-to-end upload to your ESP32. This is the complete development environment that every project in this site is built on. The guide covers Windows 10/11, macOS 12+, and Ubuntu/Debian Linux.</p>

<h2>Step 1 — Download Arduino IDE 2.x</h2>
<p>Navigate to <strong>arduino.cc/en/software</strong> and download the installer for your operating system. Choose Arduino IDE 2.x (not the legacy 1.8.x). The differences matter: IDE 2 has a built-in debugger, real-time error highlighting as you type, a Serial Plotter that graphs data live, and a much-improved library manager. All three platforms offer installers and portable ZIP options.</p>

<p><strong>Windows:</strong> Download the .exe installer. Run it and accept the defaults. The installer adds Arduino to your Start Menu and optionally installs the standard Arduino USB driver (leave this checked — it does not conflict with ESP32 drivers). Do not install to a path with spaces or non-ASCII characters, as some Arduino tools have issues with such paths.</p>

<p><strong>macOS:</strong> Download the .dmg, open it, drag Arduino IDE to Applications. The first time you launch it, macOS may show a security warning — go to System Preferences → Security & Privacy and click Open Anyway. Grant the app permission to access Documents when prompted for the sketchbook folder.</p>

<p><strong>Linux (Ubuntu/Debian):</strong> Download the AppImage. Make it executable: <code>chmod +x arduino-ide_2.x.x_Linux_64bit.AppImage</code>. Run it: <code>./arduino-ide_2.x.x_Linux_64bit.AppImage</code>. For serial port access on Linux, add your user to the <code>dialout</code> group: <code>sudo usermod -aG dialout $USER</code> — then log out and back in for the change to take effect.</p>

<h2>Step 2 — Install the USB-to-Serial Driver</h2>
<p>The ESP32 DevKitC communicates with your computer through a USB-to-serial converter chip. Two chips are common:</p>

<ul>
<li><strong>CP2102 (Silicon Labs)</strong> — usually found on official Espressif DevKitC boards, Adafruit boards, and SparkFun boards. Download the CP210x driver from Silicon Labs' website. On Windows 10/11 the driver is often automatically installed from Windows Update when you first plug in the board.</li>
<li><strong>CH340 / CH341 (WCH)</strong> — found on most low-cost NodeMCU-32S and clone boards. Download the CH340 driver from wch.cn. On Windows 11, the inbox driver may work but the manufacturer's driver is more reliable.</li>
</ul>

<p>After installing the driver, plug in your ESP32 board via USB. On Windows, open Device Manager (right-click Start → Device Manager) and expand the "Ports (COM & LPT)" section. You should see "Silicon Labs CP210x USB to UART Bridge (COM3)" or "USB-SERIAL CH340 (COM4)" — the COM number varies by system. Note this number; you will need it shortly.</p>

<p>On macOS, the port appears as <code>/dev/cu.usbserial-xxxx</code> or <code>/dev/cu.SLAB_USBtoUART</code>. On Linux it appears as <code>/dev/ttyUSB0</code> or <code>/dev/ttyACM0</code>. Confirm with <code>ls /dev/tty*</code> before and after plugging in the board.</p>

<h2>Step 3 — Add the ESP32 Board Manager URL</h2>
<p>Launch Arduino IDE 2.x. Go to <strong>File → Preferences</strong> (macOS: Arduino IDE → Preferences). Find the "Additional boards manager URLs" field. Click the icon to the right of the field to open the multi-line editor. Add this URL on a new line:</p>

<pre><code>https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json</code></pre>

<p>Click OK to save. This URL tells the IDE where to find Espressif's board package index — a JSON file listing available ESP32 core versions, their download locations, and checksums. The URL itself is lightweight and only points to the index; the actual ~500 MB board package downloads in the next step.</p>

<p>If you are behind a corporate proxy or firewall, also configure the proxy settings in the Preferences dialog. The IDE requires internet access to download the board package and will fail silently if the proxy is not configured.</p>

<h2>Step 4 — Install the ESP32 Board Package</h2>
<p>Open the Boards Manager: click the board icon in the left sidebar of IDE 2.x (or go to Tools → Board → Boards Manager in IDE 1.x). In the search box, type <strong>esp32</strong>. You will see "esp32 by Espressif Systems" — this is the official core. Click <strong>Install</strong>.</p>

<p>The download is approximately 500 MB and includes: the Xtensa GCC compiler toolchain, the ESP32 Arduino core libraries (WiFi, BLE, SPIFFS, Preferences, etc.), esptool.py for flashing, and pre-built firmware blobs for the bootloader. On a slow connection this may take 15–30 minutes. A progress bar shows in the bottom of the IDE window.</p>

<p>Wait for "INSTALLED" to appear next to the version number. Do not interrupt the installation — a partial install can leave the toolchain in a broken state. If interrupted, uninstall the partial package and start again from the Boards Manager.</p>

<h2>Step 5 — Select Your Board and Port</h2>
<p>Go to <strong>Tools → Board → ESP32 Arduino</strong>. Scroll through the list and select your board:</p>

<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Physical Board</th><th>IDE Selection</th></tr></thead>
<tbody>
<tr><td>ESP32 DevKitC (38-pin or 30-pin)</td><td>ESP32 Dev Module</td></tr>
<tr><td>NodeMCU-32S</td><td>NodeMCU-32S</td></tr>
<tr><td>Lolin32 / WEMOS D32</td><td>WEMOS D1 MINI ESP32</td></tr>
<tr><td>AI-Thinker ESP32-CAM</td><td>AI Thinker ESP32-CAM</td></tr>
<tr><td>Adafruit HUZZAH32</td><td>Adafruit ESP32 Feather</td></tr>
<tr><td>SparkFun ESP32 Thing</td><td>SparkFun ESP32 Thing</td></tr>
<tr><td>Generic / unknown</td><td>ESP32 Dev Module</td></tr>
</tbody>
</table>
</div>

<p>Then set the port: <strong>Tools → Port</strong> and select the COM port (Windows) or /dev/tty* device (Linux/macOS) that appeared when you plugged in the board. If the port does not appear, review Step 2 — the driver is not correctly installed.</p>

<p>Leave all other settings at defaults for now. The default partition scheme is "Default 4MB with spiffs", upload speed is 921600, and CPU frequency is 240 MHz. These are correct for most projects on a standard WROOM-32 DevKitC.</p>

<h2>Step 6 — Upload Your First Sketch</h2>
<p>Open the built-in Blink example: <strong>File → Examples → 01.Basics → Blink</strong>. The sketch toggles the built-in LED on and off every second. Before uploading, change the LED_BUILTIN pin if needed — on the ESP32 DevKitC the built-in LED is on GPIO 2:</p>

<pre><code>#define LED_PIN 2

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}</code></pre>

<p>Click the Upload button (right-pointing arrow) or press Ctrl+U. The IDE compiles the sketch first — you will see compilation messages in the bottom console, ending with a binary size report like "Sketch uses 234,896 bytes (17%) of program storage space." Then the upload begins.</p>

<p>Watch the console for the upload progress. A successful upload looks like:</p>
<pre><code>Connecting...
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse
...
Writing at 0x00001000... (100 %)
Hash of data verified.
Leaving...
Hard resetting via RTS pin...</code></pre>

<p>The ESP32 resets automatically after upload (via the RTS line on the USB chip). The blue LED on the DevKitC should start blinking once per second. If it does, your environment is fully working.</p>

<h2>Troubleshooting Common Installation Issues</h2>
<h3>Upload stalls at "Connecting..."</h3>
<p>The board is not entering download mode. Manual fix: hold BOOT, click Upload, wait for "Connecting...", release BOOT. If this works but automatic upload does not, the USB-to-serial chip does not correctly drive the DTR/RTS lines. Try a different USB cable (some USB cables are charge-only with no data wires). On some boards, solder a 10 µF capacitor between EN and GND to control boot-mode entry via the DTR pulse.</p>

<h3>Port disappears after a few seconds</h3>
<p>A power surge from the USB enumeration is brownouting the ESP32, causing it to reset and re-enumerate. This breaks the COM port reference. Add a 100 µF capacitor across 3V3 and GND, or use a powered USB hub that can deliver 500 mA per port steadily.</p>

<h3>Compilation fails with "gcc: error: ..."</h3>
<p>The ESP32 toolchain install is corrupt or incomplete. In the Boards Manager, uninstall "esp32 by Espressif Systems" and reinstall it. Also check that your sketch path (the folder containing your .ino file) does not contain spaces or special characters — the Arduino build system occasionally fails on non-ASCII paths.</p>

<h3>Wrong COM port selected</h3>
<p>On Windows, if Tools → Port shows multiple COM ports, unplug the ESP32, note which ports disappear from the list, plug it back in, and select the reappeared port. You can also open Device Manager and expand "Ports (COM & LPT)" to see the exact port number with a description.</p>

<h2>Recommended First-Time Settings</h2>
<p>After successful upload, configure these IDE settings to make ongoing development smoother:</p>
<ul>
<li><strong>File → Preferences → Compiler warnings: All</strong> — surfaces potential issues in your own code and libraries before they become runtime bugs.</li>
<li><strong>File → Preferences → Show verbose output during: Upload</strong> — shows the full esptool.py command and output, invaluable for diagnosing upload failures.</li>
<li><strong>Serial Monitor baud rate: 115200</strong> — set the dropdown in the Serial Monitor to match the <code>Serial.begin(115200)</code> call most example sketches use.</li>
<li><strong>Tools → Erase All Flash Before Sketch Upload: Disabled</strong> — leave this off by default; enable it only when you need to reset NVS settings or clear a corrupted file system.</li>
</ul>

<h2>Keeping Your Environment Updated</h2>
<p>Espressif releases new Arduino core versions roughly every one to two months. Open the Boards Manager and click the version dropdown next to "esp32 by Espressif Systems" to install a newer version. New releases fix bugs, add support for new chip variants (C6, H2), and sometimes break API compatibility. Read the release notes before updating mid-project. The Boards Manager allows installing multiple versions simultaneously — you can roll back if a new version breaks something.</p>

<p>Update Arduino IDE itself through Help → Check for Updates. IDE updates are independent of board package updates — you can have IDE 2.3 with ESP32 core 2.0.17 or any other combination.</p>

<h2>What to Try Next</h2>
<p>With your environment working, explore the built-in examples under File → Examples → ESP32. WiFiScan shows nearby networks. WiFiClient connects to a network and fetches a web page. BluetoothSerial pairs with your phone. Each example is self-contained and well commented — they are the fastest way to learn what the ESP32's libraries can do without writing everything from scratch.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'installing-esp-idf',
'title'        => 'Installing ESP-IDF: Native Espressif Development Framework Setup Guide',
'meta_desc'    => 'Install ESP-IDF on Windows, macOS, and Linux for native FreeRTOS ESP32 development. Covers toolchain setup, environment variables, your first IDF project, and VS Code integration.',
'read_time'    => '18 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What is ESP-IDF and how is it different from Arduino?','answer'=>'ESP-IDF (IoT Development Framework) is Espressif\'s native SDK for ESP32. It is built on FreeRTOS and provides direct access to all hardware features — memory management, power domains, security engines, NVS, OTA, and the full networking stack. Arduino is a simplified abstraction layer on top of IDF. For most hobbyist projects, Arduino is faster to develop with. For production firmware, multi-task RTOS applications, or features not exposed by Arduino, IDF is the right choice.'],
  ['question'=>'Can I use both Arduino and IDF components in the same project?','answer'=>'Yes. The Arduino-ESP32 core is itself an IDF component and can be used inside an IDF project using arduino-esp32 as a managed component. This lets you use Arduino libraries (like displays, sensors) alongside IDF APIs (like esp_wifi_scan_start, esp_sleep_enable_timer_wakeup). The ESP32 Arduino core documentation describes the arduino-as-component setup.'],
  ['question'=>'Which version of ESP-IDF should I install?','answer'=>'Install the latest stable release from the v5.x series (currently v5.2 or later). The v5.x series introduced many improvements including simplified component management, better power management APIs, and Matter SDK support. Use v4.x only if you are maintaining an existing v4 project or need a library that has not been ported to v5.'],
  ['question'=>'How much disk space does ESP-IDF require?','answer'=>'The full ESP-IDF installation — framework, toolchain, Python environment, and tools — requires approximately 10–15 GB of disk space. The initial download is smaller but the build system downloads additional components on the first build of each project. Ensure you have at least 20 GB free before starting.'],
  ['question'=>'What Python version does ESP-IDF require?','answer'=>'ESP-IDF requires Python 3.8 or later. It creates an isolated Python virtual environment during setup (install.bat / install.sh) so it does not conflict with any system Python installation. Do not run IDF commands from a system Python — always activate the IDF environment first with export.bat (Windows) or . ./export.sh (Linux/macOS).'],
  ['question'=>'How do I build and flash an IDF project from the command line?','answer'=>'In the ESP-IDF environment: navigate to your project directory, run "idf.py set-target esp32" to configure the target chip, "idf.py menuconfig" to configure options, "idf.py build" to compile, "idf.py -p COM3 flash" (or your port) to upload, and "idf.py -p COM3 monitor" to open the serial console. "idf.py -p COM3 flash monitor" flashes and opens the monitor in one command.'],
  ['question'=>'Can I use ESP-IDF on a Raspberry Pi or other ARM Linux?','answer'=>'Yes, with limitations. The Xtensa GCC toolchain is available for arm64 Linux as of IDF v5.x. Install procedure is the same as on x86 Linux. Build times are significantly slower on a Pi 4 compared to a modern desktop — a project that builds in 30 seconds on x86 may take 5–10 minutes on a Pi 4.'],
  ['question'=>'What is Kconfig / menuconfig in ESP-IDF?','answer'=>'Kconfig is a configuration system (borrowed from the Linux kernel) that lets you configure your project by setting options in a menu interface. Run "idf.py menuconfig" to launch the text-based menu. Options include Wi-Fi AP SSID/password, partition table selection, log verbosity, component feature flags, and task stack sizes. Settings are saved in sdkconfig at the project root and included at compile time as #defines.'],
  ['question'=>'How do I add external components to an IDF project?','answer'=>'ESP-IDF v5.x supports the IDF Component Manager. Add a dependency in your project\'s idf_component.yml file: "espressif/led_strip: \"^2.0.0\"". Run "idf.py update-dependencies" to download it. Alternatively, manually clone a component into the "components/" subdirectory of your project. Components are self-contained directories with a CMakeLists.txt that the IDF build system discovers automatically.'],
  ['question'=>'Is there a GUI way to use ESP-IDF without the command line?','answer'=>'Yes. The ESP-IDF Extension for VS Code (ESP-IDF plugin by Espressif) provides a full GUI wrapper: one-click build, flash, monitor, and menuconfig accessible from the VS Code sidebar and command palette. It also integrates JTAG debugging with OpenOCD. For beginners uncomfortable with the terminal, this is the recommended way to use IDF.'],
],
'related' => [
  ['title'=>'VS Code with ESP32','slug'=>'vscode-with-esp32'],
  ['title'=>'PlatformIO vs Arduino IDE','slug'=>'platformio-vs-arduino-ide'],
  ['title'=>'Flashing ESP32 Firmware','slug'=>'flashing-esp32-firmware'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
],
'body_html' => <<<'HTML'
<h2>Why Learn ESP-IDF?</h2>
<p>The Arduino framework is an excellent starting point for ESP32 development. Its abstractions are consistent, its community libraries are vast, and a working project can be running within minutes. But Arduino is a layer built on top of Espressif's own native SDK — the ESP-IDF. Understanding and using IDF directly unlocks features that Arduino does not expose: fine-grained FreeRTOS task management, hardware security engines, symmetric multiprocessing across both cores, JTAG debugging, the full NVS API, partition table customisation, and the latest Matter/Thread connectivity stacks.</p>

<p>This guide walks through installing ESP-IDF on all three major platforms, setting up the environment, and building your first native IDF "Hello World" project. It is a longer process than installing Arduino, but the setup is stable — once done, it changes rarely.</p>

<h2>Prerequisites</h2>
<p>Before starting, ensure you have: a stable internet connection (15–20 GB download), Git installed (git-scm.com), Python 3.8+ installed (python.org), at least 20 GB free disk space, and the USB driver for your ESP32 board already installed (see the Arduino IDE setup guide for driver details). On Windows, also install CMake and Ninja from their official websites — the IDF installer script will prompt you if they are missing.</p>

<h2>Installing on Windows</h2>
<p>Espressif provides an all-in-one Windows installer that handles most dependencies automatically. Go to <strong>github.com/espressif/esp-idf/releases</strong> and download the latest stable <code>esp-idf-tools-setup-x.x.x.exe</code> file. Run it as administrator. The installer will:</p>
<ol>
<li>Let you choose the ESP-IDF version to install (choose the latest stable v5.x)</li>
<li>Download and extract ESP-IDF to <code>C:\Espressif\frameworks\esp-idf-v5.x</code></li>
<li>Download and install the Xtensa and RISC-V GCC toolchains</li>
<li>Install Python and create a virtual environment with all IDF dependencies</li>
<li>Install CMake, Ninja, and OpenOCD for JTAG debugging</li>
<li>Add a shortcut to the Windows Start Menu for "ESP-IDF 5.x CMD" — a pre-configured command prompt with all environment variables set</li>
</ol>

<p>Installation takes 20–40 minutes depending on connection speed. When finished, open the "ESP-IDF 5.x CMD" shortcut. You should see a command prompt with the IDF environment active. Type <code>idf.py --version</code> — it should print the installed version.</p>

<h2>Installing on macOS</h2>
<p>On macOS, the recommended approach uses the Homebrew package manager for system dependencies and the IDF install script for the Python environment and toolchain.</p>

<p>Install Homebrew if you do not have it: <code>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"</code></p>

<p>Then install prerequisites:</p>
<pre><code>brew install cmake ninja dfu-util python3 git</code></pre>

<p>Clone the ESP-IDF repository. Choose a permanent location — the path in your <code>IDF_PATH</code> environment variable must remain stable:</p>
<pre><code>mkdir -p ~/esp
cd ~/esp
git clone -b v5.2 --recursive https://github.com/espressif/esp-idf.git</code></pre>

<p>The <code>--recursive</code> flag clones all submodules (additional libraries the IDF depends on). This adds several gigabytes of data. Run the install script:</p>
<pre><code>cd ~/esp/esp-idf
./install.sh esp32</code></pre>

<p>The script installs the Xtensa toolchain into <code>~/.espressif/</code> and sets up a Python virtual environment. When it finishes, add these lines to your <code>~/.zshrc</code> or <code>~/.bashrc</code> for convenient activation:</p>
<pre><code>alias get_idf='. $HOME/esp/esp-idf/export.sh'</code></pre>

<p>Open a new terminal and run <code>get_idf</code> to activate the IDF environment. Then <code>idf.py --version</code> to confirm.</p>

<h2>Installing on Linux (Ubuntu/Debian)</h2>
<p>Install system dependencies:</p>
<pre><code>sudo apt-get update
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
sudo usermod -aG dialout $USER   # add yourself to dialout group for serial port access</code></pre>

<p>Log out and back in after the <code>usermod</code> command. Then clone and install:</p>
<pre><code>mkdir -p ~/esp && cd ~/esp
git clone -b v5.2 --recursive https://github.com/espressif/esp-idf.git
cd ~/esp/esp-idf
./install.sh esp32</code></pre>

<p>Add the activation alias to <code>~/.bashrc</code>:</p>
<pre><code>echo "alias get_idf='. \$HOME/esp/esp-idf/export.sh'" >> ~/.bashrc
source ~/.bashrc</code></pre>

<h2>Building Your First IDF Project: Hello World</h2>
<p>ESP-IDF includes a "Hello World" example that prints to UART0 and restarts every 10 seconds. It is the minimal sanity check for your IDF environment.</p>

<p>Activate the environment (run <code>get_idf</code> on macOS/Linux, open the ESP-IDF CMD on Windows). Copy the example to a working directory:</p>
<pre><code>cd ~/esp
cp -r $IDF_PATH/examples/get-started/hello_world .
cd hello_world</code></pre>

<p>Configure the target chip:</p>
<pre><code>idf.py set-target esp32</code></pre>

<p>This generates the <code>sdkconfig</code> file with default settings for the ESP32. For the hello_world example, no additional configuration is needed. Build:</p>
<pre><code>idf.py build</code></pre>

<p>The first build compiles the entire ESP-IDF framework from source — this takes 5–15 minutes depending on your hardware. Subsequent builds are incremental and take only seconds. When done, <code>build/hello_world.bin</code> is your firmware.</p>

<p>Flash to your board (replace PORT with your actual port — COM3 on Windows, /dev/ttyUSB0 on Linux, /dev/cu.usbserial on macOS):</p>
<pre><code>idf.py -p PORT flash</code></pre>

<p>Open the serial monitor immediately after flash:</p>
<pre><code>idf.py -p PORT monitor</code></pre>

<p>You should see:</p>
<pre><code>Hello world!
This is esp32 chip with 2 CPU core(s), WiFi/BT/BLE, silicon revision 1, 4MB external-flash
Minimum free heap size: 298252 bytes
Restarting in 10 seconds...
</code></pre>

<p>Press Ctrl+] to exit the monitor. Your IDF environment is confirmed working.</p>

<h2>Project Structure</h2>
<p>Understanding the IDF project layout helps you work with it confidently:</p>
<pre><code>hello_world/
├── CMakeLists.txt       ← top-level build definition
├── sdkconfig            ← generated config (do not edit manually)
├── main/
│   ├── CMakeLists.txt   ← registers main component
│   └── hello_world_main.c ← your application code
├── components/          ← optional custom components
└── build/               ← compiled output (git-ignore this)</code></pre>

<p>The <code>main/</code> directory is the primary component. All your application source files go there. Additional reusable modules go in <code>components/</code> subdirectories. The IDF build system (CMake + Ninja) discovers and compiles everything automatically.</p>

<h2>menuconfig — Configuring Your Project</h2>
<p>Run <code>idf.py menuconfig</code> to open the text-based configuration interface. Use arrow keys to navigate, Enter to select, Space to toggle options, and ? for help on any item. Key sections:</p>
<ul>
<li><strong>Component config → ESP32-specific → CPU frequency</strong> — 80, 160, or 240 MHz</li>
<li><strong>Component config → Wi-Fi → Wi-Fi Task Core ID</strong> — pin Wi-Fi to Core 0</li>
<li><strong>Partition Table</strong> — select a pre-defined partition table or custom CSV</li>
<li><strong>Component config → Log output → Default log verbosity</strong> — reduce to WARN for production builds</li>
</ul>

<p>Press S to save and Q to quit. Settings are written to <code>sdkconfig</code> and automatically included in the next build as preprocessor macros.</p>

<h2>Key IDF Differences from Arduino</h2>
<p>If you come from Arduino, a few IDF patterns are immediately different. There is no <code>setup()</code> and <code>loop()</code> — your program entry point is <code>app_main()</code> in C or C++. You create FreeRTOS tasks with <code>xTaskCreate()</code> or <code>xTaskCreatePinnedToCore()</code> rather than placing code in loop(). Memory allocation uses standard <code>malloc()</code>/<code>free()</code> (heap_caps_malloc for specific memory types). GPIO uses the gpio_set_direction/gpio_set_level API from <code>driver/gpio.h</code> instead of pinMode/digitalWrite.</p>

<pre><code>#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define LED_PIN GPIO_NUM_2

void blink_task(void *arg) {
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);
    while (1) {
        gpio_set_level(LED_PIN, 1);
        vTaskDelay(pdMS_TO_TICKS(500));
        gpio_set_level(LED_PIN, 0);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void app_main(void) {
    xTaskCreate(blink_task, "blink", 2048, NULL, 5, NULL);
}</code></pre>

<p>This IDF blink example creates a FreeRTOS task that toggles GPIO 2 every 500 ms. <code>vTaskDelay(pdMS_TO_TICKS(500))</code> suspends the task for 500 ms without burning CPU cycles — the scheduler runs other tasks during the delay.</p>

<h2>Updating ESP-IDF</h2>
<p>To update to a new version, navigate to your ESP-IDF directory, fetch the new tag, and re-run the install script:</p>
<pre><code>cd ~/esp/esp-idf
git fetch --all --tags
git checkout v5.3
git submodule update --init --recursive
./install.sh esp32</code></pre>

<p>Then run <code>idf.py set-target esp32</code> in your existing projects to regenerate sdkconfig for the new version. Some version upgrades require manual sdkconfig changes — check the migration guide in the IDF release notes.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'first-esp32-program',
'title'        => 'Your First ESP32 Program: From Blink to Wi-Fi in One Session',
'meta_desc'    => 'Write your first ESP32 programs step by step — LED blink, button input, Serial debugging, analog reading, and a Wi-Fi network scan — with full annotated code for each.',
'read_time'    => '17 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'Do I need to declare variables before void setup()?','answer'=>'Only if they need to be accessible in both setup() and loop(). Variables declared inside setup() are local to that function and cannot be read by loop(). Variables that track state across loop() iterations — like a counter, a timestamp, or a flag — must be declared globally, before setup(). Variables used only once inside a single function can be declared locally.'],
  ['question'=>'What does Serial.begin(115200) do?','answer'=>'It initialises the hardware UART0 at 115200 baud (bits per second). This sets the communication speed between the ESP32 and the Serial Monitor in your IDE. Both sides must use the same baud rate or output appears as garbled characters. 115200 is the standard for ESP32 development; 9600 was common on older Arduino boards but is unnecessarily slow for ESP32 diagnostics.'],
  ['question'=>'Why is my LED not blinking?','answer'=>'Check these in order: (1) Is the sketch uploaded? The IDE console should show "Hard resetting via RTS pin..." after a successful upload. (2) Is the LED connected to the same GPIO the sketch drives? The onboard LED on the DevKitC is GPIO 2. (3) If using an external LED, is there a current-limiting resistor (100–330 Ω) in series? Without it the LED may be too dim or the GPIO pin may be damaged. (4) Is the LED polarity correct? The longer leg (anode) connects to the GPIO pin through the resistor; the shorter leg (cathode) connects to GND.'],
  ['question'=>'What is the difference between digital and analog input on ESP32?','answer'=>'A digital input reads only two states: HIGH (logic 1, near 3.3 V) or LOW (logic 0, near 0 V). An analog input reads a voltage between 0 V and 3.3 V and returns a number from 0 to 4095 (12-bit resolution). Use digital input for buttons and switches; use analog input (analogRead()) for potentiometers, light sensors, temperature sensors with analog output, and any source that varies continuously.'],
  ['question'=>'How do I add a delay to my sketch without blocking other operations?','answer'=>'Use millis()-based timing instead of delay(). Store the time you last performed an action in a variable: unsigned long lastTime = 0; In loop(), check if (millis() - lastTime >= interval) { lastTime = millis(); doAction(); }. This approach lets the rest of loop() run continuously while waiting, enabling multiple independent timed operations to coexist without blocking each other.'],
  ['question'=>'Can I use pinMode INPUT_PULLUP on all ESP32 GPIO pins?','answer'=>'Most GPIO pins support internal pull-up resistors. GPIO 34, 35, 36, and 39 are input-only and do not have internal pull-up or pull-down resistors — for buttons on those pins you must add an external 10 kΩ pull-up. For all other output-capable GPIO pins, pinMode(pin, INPUT_PULLUP) enables an internal ~45 kΩ pull-up resistor to 3.3 V.'],
  ['question'=>'What happens if I forget a semicolon in my Arduino sketch?','answer'=>'The compiler stops at the first line following the missing semicolon and reports a cryptic error like "expected ; before X" — where X is the token on the next line, not the line with the actual problem. Always look one line above the reported error location when debugging syntax errors. Arduino IDE 2.x underlines syntax errors in red as you type, before compilation, which helps catch these early.'],
  ['question'=>'How do I read a button without getting bouncy readings?','answer'=>'Mechanical buttons "bounce" — they briefly make and break contact multiple times during a single press, causing multiple readings within a few milliseconds. Debounce in software: after detecting a state change, wait 20–50 ms before reading again. Use a flag to track whether you have already acted on the press: bool pressed = false; if (button is LOW && !pressed) { pressed = true; doAction(); } if (button is HIGH) { pressed = false; }'],
  ['question'=>'What does the void keyword mean in void setup()?','answer'=>'The void keyword indicates that the function does not return a value. In C and C++, every function must declare what type of data it returns. setup() and loop() do not return anything — they just run code — so their return type is void. If you write a helper function that calculates a number, you would declare it as int myFunction() to indicate it returns an integer.'],
  ['question'=>'Can the ESP32 run two programs at the same time?','answer'=>'Not two separate Arduino sketches, but two tasks within one sketch, yes. Using FreeRTOS (available in the ESP32 Arduino core), you can create tasks with xTaskCreatePinnedToCore() that run concurrently on either or both CPU cores. For example, one task reads sensors every second while another maintains a Wi-Fi connection and sends data when available.'],
],
'related' => [
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
  ['title'=>'Serial Monitor Guide','slug'=>'serial-monitor-guide'],
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
  ['title'=>'Safe GPIO Pins on ESP32','slug'=>'safe-gpio-pins-esp32'],
],
'body_html' => <<<'HTML'
<h2>The Learning Path in This Guide</h2>
<p>A great first session with a new microcontroller progresses through increasingly complex programs, with each one building on what you learned from the last. This guide takes you through five programs in order: an LED blink, button-controlled LED, serial debug output, analog sensor reading, and finally a Wi-Fi network scan. Each one introduces one or two new concepts so you are never overwhelmed, and each produces visible output so you know immediately whether your code works.</p>

<p>You need: Arduino IDE installed with ESP32 support, your ESP32 DevKitC plugged into USB, and optionally one LED with a 220 Ω resistor, one momentary push button, and a 10 kΩ potentiometer for the later examples. If you only have the bare ESP32 board, the onboard LED and the Serial Monitor provide enough feedback for all five programs.</p>

<h2>Program 1: LED Blink</h2>
<p>The blink program is the "Hello World" of microcontroller development. It proves that code compiles, uploads, and runs. Open Arduino IDE, create a new sketch (File → New), and replace all the contents with:</p>

<pre><code>const int LED_PIN = 2;   // Built-in LED on the DevKitC

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);   // LED on
  delay(500);                     // wait 500 ms
  digitalWrite(LED_PIN, LOW);    // LED off
  delay(500);                     // wait 500 ms
}</code></pre>

<p><strong>What each line does:</strong> <code>const int LED_PIN = 2</code> creates a named constant for the pin number — always name your pins rather than using raw numbers, because you will refer to them many times and a name is much easier to change later. <code>void setup()</code> runs once at power-on and after every reset. <code>pinMode(LED_PIN, OUTPUT)</code> tells the ESP32 that this pin will output a signal rather than read one. <code>void loop()</code> runs repeatedly forever after setup() completes. <code>digitalWrite(LED_PIN, HIGH)</code> drives the pin to 3.3 V, turning on the LED. <code>delay(500)</code> pauses the program for 500 milliseconds.</p>

<p>Upload the sketch. After the upload completes, the blue LED on the DevKitC should blink on for half a second and off for half a second, repeating indefinitely. If it does, move on to Program 2.</p>

<h2>Program 2: Button-Controlled LED</h2>
<p>This program reads a physical button and turns the LED on only while the button is pressed. Wire a momentary push button between GPIO 4 and GND. No pull-up resistor is needed because we will use the ESP32's internal pull-up in the code.</p>

<pre><code>const int LED_PIN    = 2;
const int BUTTON_PIN = 4;

void setup() {
  pinMode(LED_PIN,    OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // internal 45kΩ pull-up to 3.3V
}

void loop() {
  // Button reads LOW when pressed (it pulls to GND, overriding the pull-up)
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}</code></pre>

<p><strong>Key concepts:</strong> <code>INPUT_PULLUP</code> enables the internal resistor that holds the pin at 3.3 V when nothing drives it. When you press the button, it connects GPIO 4 to GND, overriding the pull-up and pulling the pin to 0 V. <code>digitalRead()</code> returns HIGH (1) when the pin is near 3.3 V and LOW (0) when near 0 V. Because the button grounds the pin when pressed, a LOW reading means the button is held down. This "active low" logic with pull-ups is the most common button wiring pattern in electronics.</p>

<p>Upload and test. The LED should light only while you hold the button. Release it and the LED turns off immediately.</p>

<h2>Program 3: Serial Debugging</h2>
<p>The Serial Monitor is your window into what the ESP32 is doing at runtime. This program uses it to print sensor readings, timing data, and state changes — an essential technique for debugging any project.</p>

<pre><code>const int LED_PIN    = 2;
const int BUTTON_PIN = 4;

int press_count = 0;
bool last_state = HIGH;   // tracks previous button state

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 started. Waiting for button press...");
  pinMode(LED_PIN,    OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  bool current_state = digitalRead(BUTTON_PIN);

  // Detect falling edge (HIGH → LOW = button just pressed)
  if (current_state == LOW && last_state == HIGH) {
    press_count++;
    Serial.print("Button pressed! Total presses: ");
    Serial.println(press_count);
    digitalWrite(LED_PIN, HIGH);
    delay(20);  // simple debounce
  }

  // Detect rising edge (LOW → HIGH = button just released)
  if (current_state == HIGH && last_state == LOW) {
    Serial.println("Button released.");
    digitalWrite(LED_PIN, LOW);
    delay(20);
  }

  last_state = current_state;
}</code></pre>

<p>Upload this sketch. Open the Serial Monitor (magnifying glass icon in IDE 2.x, or Ctrl+Shift+M) and set the baud rate to 115200. Press the button several times. Each press and release prints a message, and the press count increments. This edge-detection pattern — comparing current state to previous state — is fundamental to event-driven programming on microcontrollers.</p>

<p><code>Serial.print()</code> prints without a newline; <code>Serial.println()</code> adds a newline character at the end. <code>Serial.printf("Value: %d\n", variable)</code> works like C's printf for formatted output. Use <code>Serial.printf()</code> whenever you want to print a mix of text and numbers in a single call.</p>

<h2>Program 4: Analog Sensor Reading</h2>
<p>Connect a 10 kΩ potentiometer: outer pins to 3.3 V and GND, middle (wiper) pin to GPIO 32. GPIO 32 is on ADC1, which works correctly while Wi-Fi is active.</p>

<pre><code>const int POT_PIN = 32;
const int LED_PIN = 2;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  analogReadResolution(12);       // 12-bit: 0–4095
  analogSetAttenuation(ADC_11db); // full range: 0–3.3V
}

void loop() {
  int raw       = analogRead(POT_PIN);           // 0–4095
  float voltage = raw * (3.3f / 4095.0f);        // convert to volts
  int blink_ms  = map(raw, 0, 4095, 100, 2000);  // 100ms to 2s blink rate

  Serial.printf("Raw: %4d | Voltage: %.2f V | Blink: %dms\n",
                raw, voltage, blink_ms);

  digitalWrite(LED_PIN, HIGH);
  delay(blink_ms / 2);
  digitalWrite(LED_PIN, LOW);
  delay(blink_ms / 2);
}</code></pre>

<p><strong>Concepts introduced:</strong> <code>analogReadResolution(12)</code> sets the ADC to return values from 0 to 4095 (2¹² = 4096 steps). <code>analogSetAttenuation(ADC_11db)</code> extends the input range to approximately 3.3 V (without attenuation, the full-scale range is only ~1 V). <code>map(value, inMin, inMax, outMin, outMax)</code> rescales a number from one range to another — here, pot position (0–4095) becomes a blink delay (100–2000 ms). Turn the pot and watch the LED blink rate change; watch the Serial Monitor for live voltage readings.</p>

<h2>Program 5: Wi-Fi Network Scan</h2>
<p>This final program uses the ESP32's Wi-Fi radio to scan for nearby networks and print them to the Serial Monitor. No Wi-Fi credentials are needed — the scan works without connecting. This is an excellent test that the Wi-Fi hardware is working.</p>

<pre><code>#include &lt;WiFi.h&gt;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting Wi-Fi scan...");

  // Set Wi-Fi to station mode (not AP) — required before scanning
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();   // ensure we are not connected to anything
  delay(100);
}

void loop() {
  int network_count = WiFi.scanNetworks();

  if (network_count == 0) {
    Serial.println("No networks found.");
  } else {
    Serial.printf("\n%d networks found:\n", network_count);
    Serial.printf("%-5s %-32s %-6s %s\n", "No.", "SSID", "RSSI", "Security");
    Serial.println(String('-', 60));

    for (int i = 0; i < network_count; i++) {
      String security = (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? "Open" : "Secured";
      Serial.printf("%-5d %-32s %-6d %s\n",
                    i + 1,
                    WiFi.SSID(i).c_str(),
                    WiFi.RSSI(i),
                    security.c_str());
    }
  }

  WiFi.scanDelete();   // free scan results from heap
  Serial.println("\nScanning again in 10 seconds...");
  delay(10000);
}</code></pre>

<p>Upload and open the Serial Monitor at 115200. After a few seconds you will see a table of all Wi-Fi networks the ESP32 can detect, with their names (SSID), signal strength (RSSI in dBm — more negative means weaker), and security type. RSSI above -60 dBm is excellent; -70 to -80 dBm is usable; below -85 dBm is unreliable. The scan repeats every 10 seconds so you can watch signal strength change as you move the board around.</p>

<h2>Understanding the Compilation Process</h2>
<p>When you click Upload in Arduino IDE, three things happen. First, <strong>compilation</strong>: the IDE invokes the Xtensa GCC compiler to translate your C++ sketch into machine code. The output is an ELF file containing your program plus all library code. The IDE then runs esptool.py to compute flash memory regions and addresses from the ELF file. Second, <strong>flashing</strong>: esptool.py communicates with the ESP32 bootloader over UART at 921600 baud to erase the relevant flash sectors and write the new binary. Third, <strong>reset</strong>: esptool.py pulses the RTS line to trigger a hardware reset, causing the ESP32 to exit download mode and start running the new firmware.</p>

<p>The compilation output in the IDE console shows binary size and the percentage of flash used. A standard ESP32 DevKitC with the default 4 MB flash and "Default 4MB with spiffs" partition scheme gives you approximately 1.5 MB for your sketch. Complex sketches with BLE, TLS, and web servers can approach this limit; if they do, switch to the "Huge APP (3MB No OTA)" partition scheme, which gives your sketch 3 MB at the cost of OTA update capability.</p>

<h2>Next Steps After These Five Programs</h2>
<p>These five programs cover the fundamental input and output operations every ESP32 project relies on: output (LED control), input (button and analog), debugging (Serial), and connectivity (Wi-Fi scan). From here, the natural progression is connecting to a specific Wi-Fi network with a password, sending data to a server or cloud platform, reading a real sensor (DHT22 temperature, BMP280 pressure, or MPU6050 accelerometer), and storing data in NVS or SPIFFS. Each of those topics has its own guide in this series — follow the related guides below to continue.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'uploading-code-to-esp32',
'title'        => 'Uploading Code to ESP32: Methods, Troubleshooting, and OTA Updates',
'meta_desc'    => 'Master all methods for uploading code to ESP32 — USB serial, manual boot mode, OTA over Wi-Fi, esptool.py, and ESP Flash Download Tool — with complete troubleshooting for every upload failure.',
'read_time'    => '15 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'How do I upload code to ESP32 without pressing the BOOT button every time?','answer'=>'Quality development boards (DevKitC, NodeMCU-32S) handle this automatically through the USB-to-serial chip\'s DTR and RTS lines, which are wired to GPIO 0 and EN respectively. The IDE triggers the boot sequence via these signals. If you must manually press BOOT every time, your USB cable may be charge-only (no data lines), your USB-to-serial chip may be a low-quality clone, or the auto-reset capacitor on EN may be missing. Try a different USB cable first.'],
  ['question'=>'Can I program an ESP32 over Wi-Fi without a USB connection?','answer'=>'Yes, using OTA (Over-The-Air) updates. You must first upload a sketch that includes OTA code (using the ArduinoOTA library or a web server-based update). After that initial upload, subsequent firmware updates can be pushed over Wi-Fi from the Arduino IDE or a script. OTA is essential for deployed devices in hard-to-reach locations.'],
  ['question'=>'What does "esptool.py" do and when do I use it directly?','answer'=>'esptool.py is the open-source command-line tool that Arduino IDE, PlatformIO, and ESP-IDF all use internally to communicate with the ESP32 bootloader and flash firmware. You use it directly when you need to: flash a pre-built binary (.bin), erase all flash, read back firmware from a device, or flash multiple .bin files to specific addresses simultaneously. It is available as a standalone Python package: pip install esptool.'],
  ['question'=>'What is the difference between uploading and flashing?','answer'=>'In ESP32 context these terms are synonymous — both refer to writing new firmware to the flash chip. "Uploading" is the Arduino IDE term; "flashing" is the term used in ESP-IDF and by the broader embedded community. The underlying process is identical: esptool.py connects to the bootloader and writes .bin file(s) to flash memory.'],
  ['question'=>'My ESP32 shows "A fatal error occurred: Failed to connect to ESP32: Wrong boot mode detected. The chip needs to be in download mode."','answer'=>'The chip is not entering download mode when the upload starts. Hold the BOOT button on the board before clicking Upload, then release it after "Connecting..." appears. If this happens every upload, check that GPIO 0 is not pulled low by an external circuit (a sensor, transistor, or pull-down resistor connected to GPIO 0 causes this). For custom PCBs, verify the EN and GPIO 0 auto-reset circuit is correctly placed.'],
  ['question'=>'Can I upload to multiple ESP32 boards simultaneously?','answer'=>'Not from a single Arduino IDE instance, but you can open multiple IDE instances (each with a different COM port selected) and upload in sequence. For batch programming multiple boards from the same binary, use esptool.py in a script or Espressif\'s Flash Download Tool (a GUI application) which supports multiple simultaneous serial port connections.'],
  ['question'=>'What happens if I unplug the USB cable during an upload?','answer'=>'The partially written flash will likely contain a corrupted firmware image. On next power-on, the bootloader may fail to load the application and loop-reset, or print a "Guru Meditation Error". You can recover by putting the board in download mode (GPIO 0 low at reset) and flashing a known-good firmware from a computer. The bootloader itself (in a protected flash region) is not overwritten by normal uploads and remains intact for recovery.'],
  ['question'=>'How do I verify that my upload was successful without looking at the Serial Monitor?','answer'=>'The Arduino IDE console prints "Hash of data verified." immediately after writing the firmware, confirming the CRC of the written data matches the source binary. This verifies the data was correctly written to flash. If this line appears, the firmware was written correctly — any subsequent issue is a runtime problem in the sketch, not a flash write error.'],
  ['question'=>'Is it possible to upload ESP32 firmware from a smartphone or tablet?','answer'=>'Not via USB directly, but via OTA yes. If your ESP32 runs a web-based OTA update page (using the ElegantOTA library or a custom web server), you can navigate to its IP address from any browser — including mobile — and upload a new .bin file. Some ESP32 projects use BLE for OTA update as well, controlled via a mobile app.'],
  ['question'=>'What is the difference between Erase Flash and regular upload?','answer'=>'A regular upload only writes the application firmware to the app partition — it does not erase NVS settings, file system data, or other partitions. "Erase All Flash" (Tools → Erase All Flash Before Sketch Upload in Arduino IDE) erases the entire flash chip, clearing NVS, SPIFFS/LittleFS, and all user data before writing the new firmware. Use this when you need a clean slate — for example, when corrupted NVS data is causing crashes on startup.'],
],
'related' => [
  ['title'=>'Flashing ESP32 Firmware','slug'=>'flashing-esp32-firmware'],
  ['title'=>'Updating ESP32 Firmware','slug'=>'updating-esp32-firmware'],
  ['title'=>'Serial Monitor Guide','slug'=>'serial-monitor-guide'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
],
'body_html' => <<<'HTML'
<h2>The Upload Pipeline Explained</h2>
<p>Every time you click Upload in the Arduino IDE, a multi-step pipeline runs invisibly behind the progress bar. Understanding this pipeline transforms upload failures from mysterious black-box errors into diagnosable problems with specific fixes. The pipeline has four stages: compilation, binary packaging, bootloader negotiation, and flash writing.</p>

<p><strong>Stage 1 — Compilation:</strong> The Arduino IDE invokes the Xtensa GCC toolchain to compile your .ino sketch (converted to .cpp) plus all linked library source files into object files, then links them into an ELF (Executable and Linkable Format) binary. This is where syntax errors and missing library failures appear.</p>

<p><strong>Stage 2 — Binary packaging:</strong> The IDE runs esptool.py's merge_bin command to extract the application firmware from the ELF, create the bootloader and partition table binaries, and determine the correct flash addresses for each component.</p>

<p><strong>Stage 3 — Bootloader negotiation:</strong> esptool.py drives the RTS line on the USB-to-serial chip low (which connects to the EN/RST pin through a 0.1 µF capacitor), then drives DTR low (connected to GPIO 0). This sequence resets the ESP32 with GPIO 0 held low, putting it into UART download mode. The ESP32 ROM bootloader then starts responding at 115200 baud before synchronising to the upload speed.</p>

<p><strong>Stage 4 — Flash writing:</strong> esptool.py detects the connected chip, erases the relevant flash sectors, and writes the firmware at up to 921600 baud. A CRC check verifies each written block. When complete, RTS pulses again to reset the ESP32 into normal boot mode, starting your new sketch.</p>

<h2>Method 1: USB Serial Upload (Standard)</h2>
<p>This is the default and most used upload method. Requirements: a USB cable with data lines (charge-only cables have only two wires — power and ground — and cannot carry serial data), the correct USB-to-serial driver installed, and the correct COM port selected in the IDE.</p>

<p>Typical upload session in Arduino IDE 2.x:</p>
<ol>
<li>Select Tools → Board → your ESP32 board variant</li>
<li>Select Tools → Port → the COM port showing your board</li>
<li>Click the Upload button (→ arrow) or press Ctrl+U</li>
<li>Watch the output console — compilation messages appear first, then "Connecting...", then flash write progress</li>
<li>Upload complete when you see "Hard resetting via RTS pin..."</li>
</ol>

<p>The total time from clicking Upload to the sketch running is typically 10–30 seconds for small sketches and up to 60 seconds for large ones with many libraries. The compilation step is the slowest, but Arduino IDE caches compiled library objects — only changed code recompiles, making subsequent uploads faster.</p>

<h2>Method 2: Manual Boot Mode for Boards Without Auto-Reset</h2>
<p>Some ESP32 boards (particularly the ESP32-CAM and some custom hardware) lack the capacitor-resistor circuit that allows the IDE to automatically trigger download mode. For these boards:</p>
<ol>
<li>Press and hold the BOOT button (GPIO 0 to GND)</li>
<li>Press and release the EN (reset) button while holding BOOT</li>
<li>Release the BOOT button — the chip is now in download mode</li>
<li>Click Upload in the IDE — it should connect immediately</li>
</ol>

<p>You can confirm the board is in download mode by opening a serial terminal at 115200 baud — the ROM bootloader prints a brief message then waits silently. No LED activity occurs in download mode.</p>

<h2>Method 3: OTA — Over-the-Air Updates</h2>
<p>OTA allows uploading new firmware to an ESP32 over Wi-Fi — no USB cable required. You must first upload a sketch that includes OTA support. The ArduinoOTA library is the simplest approach:</p>

<pre><code>#include &lt;WiFi.h&gt;
#include &lt;ArduinoOTA.h&gt;

const char* ssid     = "YourNetwork";
const char* password = "YourPassword";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.print("IP: "); Serial.println(WiFi.localIP());

  ArduinoOTA.setPassword("admin");  // optional password protection
  ArduinoOTA.onStart([]()  { Serial.println("OTA start");   });
  ArduinoOTA.onEnd([]()    { Serial.println("OTA done");    });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\n", progress * 100 / total);
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA Error[%u]\n", error);
  });
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();  // must call this in every loop iteration
  // ... your application code ...
}</code></pre>

<p>After uploading this sketch via USB, the ESP32 appears as a network port in the Arduino IDE. Under Tools → Port, you will see an entry like "ESP32-XXXXXX at 192.168.1.x". Select it and upload subsequent sketches wirelessly. Each OTA sketch must also include ArduinoOTA.handle() in loop() to remain updateable over the air — forgetting this locks you out and requires the next update to be via USB again.</p>

<h2>Method 4: esptool.py Direct Flashing</h2>
<p>For advanced use cases — flashing pre-built binaries, batch programming, or automated CI/CD deployments — use esptool.py directly from the command line. Install it:</p>
<pre><code>pip install esptool</code></pre>

<p>Erase all flash:</p>
<pre><code>esptool.py --port COM3 erase_flash</code></pre>

<p>Flash a pre-built firmware (three files at their specific addresses):</p>
<pre><code>esptool.py --port COM3 --baud 921600 write_flash \
  0x1000  bootloader.bin \
  0x8000  partitions.bin \
  0x10000 firmware.bin</code></pre>

<p>The three addresses are standard for the ESP32: 0x1000 for the bootloader, 0x8000 for the partition table, and 0x10000 for the application. You can find the exact addresses by enabling verbose upload output in the Arduino IDE (File → Preferences → Show verbose output during upload) and reading the esptool.py command it runs.</p>

<h2>Method 5: Web Browser-Based OTA with ElegantOTA</h2>
<p>ElegantOTA is a library that adds a web-based update page to your ESP32. Navigate to the ESP32's IP address in any browser, select a .bin file, and upload — no IDE required, works from any device including smartphones. Install from the Arduino library manager. This approach is excellent for field firmware updates on deployed devices.</p>

<h2>Troubleshooting Upload Failures</h2>
<h3>"Connecting..." hangs indefinitely</h3>
<p>The IDE cannot reach the ESP32 bootloader. Check: USB cable (try a different one); driver installation (Device Manager on Windows); correct COM port selected; board not held in a crash loop by a malfunctioning sketch (hold BOOT before clicking Upload to override). If the board previously uploaded fine and now does not, the sketch may have disabled UART or used GPIO 0 as an output that holds it LOW.</p>

<h3>"A fatal error occurred: Invalid head of packet"</h3>
<p>Communication noise or baud rate mismatch during connection. The ESP32 started negotiating at one speed but the PC expects another. Fix: reduce upload speed to 115200 in Tools → Upload Speed. Also check for power supply instability causing glitches during the negotiation phase.</p>

<h3>"MD5 of file does not match data in flash"</h3>
<p>Data written to flash did not match the source binary — the flash write was corrupted. This suggests either a hardware problem (power instability during write, damaged flash chip) or USB communication errors (long cable, noisy USB hub). Try: shorter cable, direct laptop USB port (not hub), and lower upload speed.</p>

<h3>Upload succeeds but sketch does not run correctly</h3>
<p>If the IDE reports "Hash of data verified" but the sketch misbehaves, the firmware was written correctly — the problem is in the sketch logic itself. Open the Serial Monitor immediately after upload to catch any crash messages or panic outputs before they scroll away.</p>

<h2>OTA Best Practices for Deployed Devices</h2>
<p>For production devices that will receive OTA updates in the field, always use a dual-partition OTA layout (the default "OTA" partition scheme in the IDE). This allocates two equal app partitions: the currently running firmware and the update slot. The OTA process writes the new firmware to the unused slot, verifies it with a CRC check, then switches the boot partition pointer. If the new firmware fails to boot within a configured timeout, the device automatically rolls back to the previous working firmware. This rollback mechanism prevents a bad OTA update from permanently bricking a deployed device.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'serial-monitor-guide',
'title'        => 'ESP32 Serial Monitor Guide: Debug, Plot, and Monitor Your Projects',
'meta_desc'    => 'Master the Arduino Serial Monitor and Serial Plotter with ESP32. Learn Serial.print, printf, timestamps, debugging state machines, binary protocol decoding, and multiple UART ports.',
'read_time'    => '14 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What baud rate should I use for the ESP32 Serial Monitor?','answer'=>'Use 115200 baud for all ESP32 development. This is the rate the ESP32 ROM bootloader uses, the rate most library examples default to, and fast enough that printing does not add noticeable latency to your main loop. Avoid 9600 on ESP32 — at 9600 baud, printing one line of 60 characters takes 50 ms, which can interfere with timing-sensitive code. Match the Serial.begin() rate in your sketch to the baud dropdown in the Serial Monitor exactly.'],
  ['question'=>'Can I use Serial.print() on pins other than GPIO 1 and 3?','answer'=>'Yes. The ESP32 has three hardware UARTs. Serial (UART0) uses GPIO 1 (TX) and 3 (RX). Serial1 and Serial2 can be remapped to any GPIO. Use Serial2.begin(9600, SERIAL_8N1, rxPin, txPin) to initialise a second UART on chosen pins. In the Arduino IDE, Serial Monitor only shows UART0 (Serial). For other ports you need an external USB-to-serial adapter or a separate terminal emulator.'],
  ['question'=>'How do I receive data typed in the Serial Monitor back into my ESP32 sketch?','answer'=>'Use Serial.available() to check if bytes are waiting and Serial.read() or Serial.readString() to receive them. Type text in the Serial Monitor input box and press Enter (or Send) to transmit it to the ESP32. Example: if (Serial.available()) { String cmd = Serial.readStringUntil(\'\\n\'); cmd.trim(); if (cmd == "on") digitalWrite(LED, HIGH); }'],
  ['question'=>'Why do I see gibberish in the Serial Monitor?','answer'=>'The baud rate in the monitor does not match Serial.begin() in your sketch. They must be identical. Also, the ESP32 ROM boot messages print at 115200 baud before your sketch starts — these will appear as gibberish if you are monitoring at a different rate even if your sketch uses the correct rate. Set both to 115200 to see everything correctly.'],
  ['question'=>'What is the Serial Plotter and how do I use it?','answer'=>'The Serial Plotter (Tools → Serial Plotter in Arduino IDE, or the chart icon in IDE 2.x) reads comma-separated numbers from Serial output and plots them as scrolling lines. Print values separated by commas: Serial.printf("%d,%d\\n", sensor1, sensor2); The plotter shows each value as a separate coloured line. It is invaluable for visualising sensor noise, PID response curves, and signal patterns in real time.'],
  ['question'=>'Can I log Serial Monitor output to a file?','answer'=>'Arduino IDE does not have built-in Serial Monitor logging to file. Options: (1) Use PuTTY on Windows or screen/minicom on Linux with logging enabled. (2) Use a Python script with pyserial: import serial; ser = serial.Serial("COM3", 115200); open("log.txt","w").write(ser.readline()). (3) The Serial Monitor in VS Code with PlatformIO has a built-in log-to-file option.'],
  ['question'=>'How do I print floating-point numbers in ESP32 Arduino?','answer'=>'Use Serial.printf("%.2f", value) — this prints a float with 2 decimal places. Alternatively: Serial.println(value, 2) — the second argument specifies decimal places. Note: Serial.println(floatValue) works on ESP32 (unlike some AVR Arduinos where %f in printf requires special handling). For fixed-width columns, Serial.printf("%8.3f", value) pads to 8 characters total.'],
  ['question'=>'My Serial output is delayed or buffered. Why?','answer'=>'Serial output on ESP32 Arduino core is buffered by default — output is not transmitted until the buffer fills or you call Serial.flush(). If you need immediate transmission (e.g., for crash debugging), call Serial.flush() after critical messages, or enable immediate flushing with Serial.setDebugOutput(true) for internal debug messages. Also note that in deep sleep, any pending Serial output may not transmit before the chip powers down — always call Serial.flush() before esp_deep_sleep_start().'],
  ['question'=>'Can I send commands to my ESP32 over Serial to control it remotely?','answer'=>'Yes. Build a simple command parser in loop(): read Serial input line by line, split on spaces, and execute commands. For example, "led on", "led off", "read temp", "sleep 30" can each trigger different firmware behaviours. This is a quick way to add interactive control and diagnostic commands to any project without building a web interface.'],
  ['question'=>'Why does the Serial Monitor show the ESP32 boot log every time I press EN?','answer'=>'The ROM bootloader always prints to UART0 at 115200 baud on every reset. This is normal. You will see lines starting with "rst:0x1 (POWERON_RESET)" or similar, followed by "ets Jul 29 2019 12:21:46" and the boot sequence. These are from ROM code, not your sketch. They are useful for diagnosing boot failures but can be suppressed in production by pulling GPIO 15 low at boot.'],
],
'related' => [
  ['title'=>'First ESP32 Program','slug'=>'first-esp32-program'],
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
  ['title'=>'Common ESP32 Beginner Mistakes','slug'=>'esp32-beginner-mistakes'],
  ['title'=>'ESP32 Board Manager Setup','slug'=>'esp32-board-manager-setup'],
],
'body_html' => <<<'HTML'
<h2>The Serial Monitor: Your Most Valuable Debug Tool</h2>
<p>When an ESP32 project behaves unexpectedly — incorrect sensor readings, missed Wi-Fi connections, unexpected resets — the Serial Monitor is almost always the fastest path to the root cause. It provides a real-time text window into your running firmware at a cost of two GPIO pins and a USB cable. For the vast majority of ESP32 development, Serial output is the primary diagnostic technique, and investing time in learning to use it well returns dividends across every project you build.</p>

<p>This guide covers the complete Serial API, formatting techniques, receiving input, the Serial Plotter, multiple UART ports, debugging state machines, and how to structure Serial output for readability in complex projects.</p>

<h2>Basic Serial Output: print, println, printf</h2>
<p>The three core print functions serve different purposes:</p>

<pre><code>Serial.print("Hello");           // print without newline
Serial.println("Hello");         // print with newline
Serial.printf("x=%d y=%.2f\n", xVal, yVal);  // formatted print</code></pre>

<p><code>Serial.printf()</code> is the most versatile and the one you will use most often. It accepts the same format specifiers as C's printf: <code>%d</code> for int, <code>%u</code> for unsigned int, <code>%f</code> for float, <code>%s</code> for string (char*), <code>%c</code> for char, <code>%x</code> for hexadecimal. Width and precision modifiers work too: <code>%8d</code> right-justifies an integer in 8 characters, <code>%.3f</code> prints a float with 3 decimal places, <code>%08x</code> prints hex zero-padded to 8 digits.</p>

<pre><code>void setup() {
  Serial.begin(115200);
  float temperature = 23.45;
  int   raw_adc     = 2048;
  bool  wifi_up     = true;

  Serial.printf("Temperature: %.2f°C\n",   temperature);
  Serial.printf("ADC raw:     %4d (0x%03X)\n", raw_adc, raw_adc);
  Serial.printf("Wi-Fi:       %s\n",        wifi_up ? "connected" : "offline");
}</code></pre>

<p>The output:</p>
<pre><code>Temperature: 23.45°C
ADC raw:     2048 (0x800)
Wi-Fi:       connected</code></pre>

<p>Formatted, aligned output is far easier to read at a glance than unformatted strings — especially when values are scrolling quickly in the monitor during a live run.</p>

<h2>Adding Timestamps to Serial Output</h2>
<p>Raw print statements tell you what happened but not when. Adding timestamps transforms the Serial Monitor from a log viewer into a timing analyser:</p>

<pre><code>void logf(const char* format, ...) {
  char buf[256];
  va_list args;
  va_start(args, format);
  vsnprintf(buf, sizeof(buf), format, args);
  va_end(args);

  unsigned long ms = millis();
  Serial.printf("[%7lu.%03lu] %s\n",
                ms / 1000, ms % 1000, buf);
}

// Usage:
logf("Wi-Fi connected, IP: %s", WiFi.localIP().toString().c_str());
logf("Sensor reading: %.2f°C", temperature);</code></pre>

<p>Output:</p>
<pre><code>[      1.234] Wi-Fi connected, IP: 192.168.1.42
[      3.891] Sensor reading: 23.45°C</code></pre>

<p>The <code>[7lu.%03lu]</code> format prints seconds with 7 digits and milliseconds with 3 digits, giving you sub-second resolution. This is invaluable for diagnosing timing issues: if Wi-Fi connection takes 4 seconds but should take 1, the timestamps reveal exactly where the delay occurs.</p>

<h2>Receiving Serial Input</h2>
<p>The Serial Monitor is bidirectional. Type text in the input box at the top of the monitor and press Enter to send it to the ESP32. A basic command handler:</p>

<pre><code>void setup() {
  Serial.begin(115200);
  Serial.println("Commands: led_on, led_off, reboot, status");
  pinMode(2, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();  // remove trailing \r\n

    if      (cmd == "led_on")  { digitalWrite(2, HIGH); Serial.println("LED on"); }
    else if (cmd == "led_off") { digitalWrite(2, LOW);  Serial.println("LED off"); }
    else if (cmd == "reboot")  { Serial.println("Rebooting..."); delay(100); ESP.restart(); }
    else if (cmd == "status")  {
      Serial.printf("Heap: %d bytes free\n", ESP.getFreeHeap());
      Serial.printf("Uptime: %lu s\n",      millis() / 1000);
    }
    else { Serial.printf("Unknown command: '%s'\n", cmd.c_str()); }
  }
}</code></pre>

<p>Note: always call <code>cmd.trim()</code> — Serial Monitor on different operating systems sends different line endings (\n, \r\n, or \r). <code>trim()</code> removes all whitespace and line ending characters from both ends of the string, preventing "command not found" errors caused by invisible trailing characters.</p>

<h2>The Serial Plotter</h2>
<p>The Serial Plotter (Tools → Serial Plotter in the Arduino IDE menu, or the chart icon in IDE 2.x's top bar) reads comma-separated numeric values and plots them as scrolling lines. Separate multiple values with commas; each gets its own coloured line.</p>

<pre><code>void loop() {
  int raw   = analogRead(34);
  float volts = raw * 3.3f / 4095.0f;
  int smooth  = 0;

  // Simple moving average (not the right place for static, but illustrative)
  static int buffer[8] = {0};
  static int idx = 0;
  buffer[idx++ % 8] = raw;
  for (int i = 0; i < 8; i++) smooth += buffer[i];
  smooth /= 8;

  // Print values for plotter: label:value syntax gives named traces in IDE 2.x
  Serial.printf("Raw:%d,Smooth:%d,Volts:%.0f\n",
                 raw, smooth, volts * 100); // scale volts × 100 for same Y axis
  delay(50);
}</code></pre>

<p>In Arduino IDE 2.x, the plotter supports the <code>Label:Value</code> syntax — each trace gets a named legend. This makes it easy to identify which line is which when multiple sensors are plotted simultaneously. Use the plotter for: visualising sensor noise before and after filtering, tuning PID controllers, monitoring battery voltage over time, and debugging oscillating or unstable signal paths.</p>

<h2>Debugging State Machines</h2>
<p>Many ESP32 projects are state machines — code that transitions between states (IDLE, CONNECTING, READING, POSTING, SLEEPING) and must behave differently in each. Serial output combined with state names makes debugging dramatically easier:</p>

<pre><code>enum State { IDLE, CONNECTING, READING, POSTING, SLEEPING };
State state = IDLE;

const char* stateNames[] = {
  "IDLE", "CONNECTING", "READING", "POSTING", "SLEEPING"
};

void setState(State next) {
  if (next != state) {
    Serial.printf("[%lu] State: %s → %s\n",
                  millis()/1000, stateNames[state], stateNames[next]);
    state = next;
  }
}

void loop() {
  switch (state) {
    case IDLE:
      setState(CONNECTING);
      break;
    case CONNECTING:
      WiFi.begin(SSID, PASS);
      if (WiFi.status() == WL_CONNECTED) setState(READING);
      break;
    // ...
  }
}</code></pre>

<p>The output shows every state transition with a timestamp, making it easy to see where the system hangs, how long each state takes, and whether state transitions occur in the expected order.</p>

<h2>Using Multiple UARTs</h2>
<p>The ESP32 has three hardware UARTs. UART0 is the programming and Serial Monitor port. UART1 overlaps with flash SPI (avoid it). UART2 (GPIO 16 RX, GPIO 17 TX) is the safe general-purpose second UART for communicating with GPS modules, GSM modems, RS232 sensors, and other serial devices.</p>

<pre><code>void setup() {
  Serial.begin(115200);   // UART0 — for Serial Monitor / debugging
  Serial2.begin(9600, SERIAL_8N1, 16, 17);  // UART2 — for GPS module
}

void loop() {
  if (Serial2.available()) {
    String nmea = Serial2.readStringUntil('\n');
    Serial.println("GPS: " + nmea);  // echo GPS data to Serial Monitor
  }
}</code></pre>

<p>You can also remap UARTs to arbitrary pins. <code>Serial2.begin(9600, SERIAL_8N1, rxPin, txPin)</code> — where rxPin and txPin are any output-capable GPIOs — exploits the ESP32's GPIO matrix to route UART2 to whichever physical pins suit your board layout.</p>

<h2>Controlling Serial Output Verbosity</h2>
<p>For production builds you want minimal Serial output to avoid performance overhead. A common pattern is a global verbosity flag that controls which messages print:</p>

<pre><code>#define LOG_LEVEL 2  // 0=off, 1=error, 2=info, 3=debug

#define LOG_E(fmt, ...) if (LOG_LEVEL >= 1) Serial.printf("[ERR] " fmt "\n", ##__VA_ARGS__)
#define LOG_I(fmt, ...) if (LOG_LEVEL >= 2) Serial.printf("[INF] " fmt "\n", ##__VA_ARGS__)
#define LOG_D(fmt, ...) if (LOG_LEVEL >= 3) Serial.printf("[DBG] " fmt "\n", ##__VA_ARGS__)

// Usage:
LOG_E("Wi-Fi connection failed after %d attempts", retries);
LOG_I("Sensor reading: %.2f°C", temp);
LOG_D("ADC raw value: %d", raw);</code></pre>

<p>Change <code>LOG_LEVEL</code> to 0 before production deployment to silence all output, eliminating the CPU and timing overhead of Serial transmission. Because the condition is a compile-time constant, the compiler optimises away the unreachable branches entirely.</p>

<h2>Using Serial.flush() Before Deep Sleep</h2>
<p>Serial output is buffered — if your sketch calls <code>esp_deep_sleep_start()</code> while data is still in the UART transmit buffer, that data will never reach the Serial Monitor because the UART clock stops when the chip sleeps. Always call <code>Serial.flush()</code> before any sleep or restart command to ensure all pending output is transmitted:</p>

<pre><code>Serial.printf("Going to sleep for %d seconds. Uptime: %lu s\n",
              SLEEP_SECONDS, millis()/1000);
Serial.flush();
esp_sleep_enable_timer_wakeup(SLEEP_SECONDS * 1000000ULL);
esp_deep_sleep_start();</code></pre>
HTML,
],

]; // end return
