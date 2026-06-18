<?php
/* Phase 2 guide data — guides 6-10 */
return [

/* ============================================================ */
[
'slug'         => 'esp32-board-manager-setup',
'title'        => 'ESP32 Board Manager Setup: Installing, Updating, and Switching Core Versions',
'meta_desc'    => 'How to install the ESP32 Arduino core via Board Manager, manage multiple core versions, switch between ESP32 chip variants, and resolve common Board Manager installation errors.',
'read_time'    => '12 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What is the Board Manager in Arduino IDE?','answer'=>'The Board Manager is the Arduino IDE\'s package manager for hardware support. Each board package ("core") contains the compiler toolchain, hardware abstraction libraries (WiFi, BLE, SPIFFS, etc.), pre-built firmware blobs, and board definitions for a family of microcontrollers. Without installing the ESP32 board package, the IDE only knows about AVR-based Arduino boards (Uno, Mega, etc.).'],
  ['question'=>'What is the difference between "Arduino ESP32" and "Arduino ESP32 S2/S3" board selections?','answer'=>'They are all part of the same ESP32 Arduino core package. The board list under Tools → Board → ESP32 Arduino contains entries for every chip variant: ESP32 Dev Module (original ESP32), ESP32-S2 Dev Module, ESP32-S3 Dev Module, ESP32-C3 Dev Module, and dozens more. Selecting the correct board from this list configures the compiler for the right CPU architecture (Xtensa vs RISC-V) and sets default flash and PSRAM sizes.'],
  ['question'=>'Can I have multiple ESP32 core versions installed simultaneously?','answer'=>'Yes. The Board Manager allows installing any number of versions side by side. In the Boards Manager, click the version dropdown next to "esp32 by Espressif Systems" and select "Install" for any additional version. Switch between them by selecting the desired version before compiling. This is useful when maintaining legacy projects on an older core while developing new projects on the latest version.'],
  ['question'=>'Why does my board not appear in the Boards Manager even after adding the URL?','answer'=>'Common causes: (1) The Additional Boards Manager URL has a typo — paste it fresh from the official documentation rather than retyping. (2) A proxy or firewall is blocking the download. (3) The IDE needs restarting after adding the URL. (4) File permission issues prevent writing to the Arduino packages directory. On Linux, check that ~/.arduino15 is writable by your user. On Windows, do not install Arduino to Program Files without administrator rights.'],
  ['question'=>'How do I find which core version a sketch was compiled with?','answer'=>'Check the IDE console during compilation. The verbose compiler output includes a path like C:/Users/name/AppData/Local/Arduino15/packages/esp32/hardware/esp32/2.0.17 — the last segment (2.0.17) is the core version. You can also print it from your sketch: Serial.printf("Core: %s\\n", ESP.getSdkVersion()); which prints the underlying IDF version the Arduino core was built on.'],
  ['question'=>'Should I always install the latest ESP32 Arduino core?','answer'=>'Not necessarily. The latest version has the newest features and bug fixes, but it may introduce breaking API changes or new bugs. For a new project, start with the latest stable version. For an ongoing project, only update when you need a specific bug fix or new feature, and test thoroughly after updating. Check the GitHub releases page for the core\'s changelog before updating.'],
  ['question'=>'What is the "esp32 by Arduino" package vs "esp32 by Espressif Systems"?','answer'=>'"esp32 by Espressif Systems" is the official Espressif-maintained Arduino core for all ESP32 variants. "esp32 by Arduino" (if you see it) refers to the Arduino Nano ESP32\'s core, maintained by Arduino LLC, which has different APIs and targets only the Arduino Nano ESP32 board. For DevKitC, NodeMCU, and most ESP32 boards, install "esp32 by Espressif Systems".'],
  ['question'=>'How much storage space does the ESP32 Arduino core use?','answer'=>'The installed ESP32 core occupies approximately 500 MB on disk, including the Xtensa and RISC-V GCC toolchains, the precompiled bootloader blobs, and all library source files. This is stored in the Arduino packages directory: C:\\Users\\name\\AppData\\Local\\Arduino15\\packages\\esp32 on Windows, ~/.arduino15/packages/esp32 on Linux/macOS.'],
  ['question'=>'I get "Board esp32:esp32:esp32 not found" when opening an old project. Why?','answer'=>'The old project\'s saved board selection references a board identifier string that is no longer valid in your installed core version. Open the project, go to Tools → Board, and manually select your board. The project will save the new board identifier. This sometimes happens when upgrading from ESP32 core v1.x to v2.x, which reorganised board identifiers.'],
  ['question'=>'How do I install a pre-release or beta version of the ESP32 core?','answer'=>'Add the development (unstable) index URL to Additional Boards Manager URLs: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json — this lists release candidates and beta versions. Search "esp32" in the Boards Manager and you will see both stable and development versions. Only use pre-release versions if you need a specific upcoming bug fix and understand you may encounter new issues.'],
],
'related' => [
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
  ['title'=>'First ESP32 Program','slug'=>'first-esp32-program'],
  ['title'=>'ESP32 Variants Explained','slug'=>'esp32-variants-explained'],
  ['title'=>'PlatformIO vs Arduino IDE','slug'=>'platformio-vs-arduino-ide'],
],
'body_html' => <<<'HTML'
<h2>What the Board Manager Actually Does</h2>
<p>The Arduino IDE's Board Manager is a package installer that downloads and installs hardware support packages — called "cores" — for microcontroller families. A core is a collection of files that teaches the Arduino build system how to compile code for a specific processor: the compiler toolchain binaries, the hardware abstraction library source code (WiFi.h, BLE.h, SPIFFS.h), pre-compiled bootloader blobs, a JSON board descriptor file listing available board variants, and upload tool scripts.</p>

<p>Before installing the ESP32 core, the Arduino IDE can only target AVR microcontrollers (Arduino Uno, Mega, Nano). After installing the ESP32 Espressif core, it gains the ability to compile for the ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6, and ESP32-H2 — and present all their board variants in the board selection menu.</p>

<h2>Adding the ESP32 Board Manager URL</h2>
<p>The first step is telling the Arduino IDE where to find the ESP32 core index. Open <strong>File → Preferences</strong> (macOS: Arduino IDE → Preferences). Find the "Additional boards manager URLs" field at the bottom of the dialog. Click the icon to the right of the field to open the multi-URL editor. Add this URL on its own line:</p>

<pre><code>https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json</code></pre>

<p>Click OK. This URL points to a JSON index file that the IDE downloads and parses to show you available core versions and their download locations. The URL itself is just a pointer — no large files are downloaded yet.</p>

<p>If you already have other URLs in this field (for SAM boards, STM32, etc.), add the ESP32 URL on a new line. Multiple URLs are separated by commas or newlines. The order does not matter.</p>

<h2>Installing the ESP32 Core</h2>
<p>Open the Boards Manager:</p>
<ul>
<li><strong>Arduino IDE 2.x:</strong> Click the board icon in the left sidebar (looks like a circuit board), or go to Tools → Board → Boards Manager</li>
<li><strong>Arduino IDE 1.8.x:</strong> Go to Tools → Board → Boards Manager</li>
</ul>

<p>Type <strong>esp32</strong> in the search box. You will see "esp32 by Espressif Systems". Click on it to expand the entry, then click <strong>Install</strong>. The latest stable version is selected by default — install it. The download is approximately 500 MB and includes the compiler toolchain, all library source files, and pre-compiled blobs. Depending on your internet connection, this takes 5–30 minutes.</p>

<p>Do not close the IDE during installation. A progress bar at the bottom of the IDE window shows download and extraction progress. When "INSTALLED" appears next to the version number, installation is complete.</p>

<h2>Verifying the Installation</h2>
<p>Go to Tools → Board. You should see a new submenu "ESP32 Arduino" with a long list of supported boards including "ESP32 Dev Module", "ESP32-S3 Dev Module", "ESP32-C3 Dev Module", "AI Thinker ESP32-CAM", and many more. If this submenu appears, the core is correctly installed.</p>

<p>As a functional verification, select Tools → Board → ESP32 Arduino → ESP32 Dev Module. Select your port (Tools → Port → your COM port). Open File → Examples → WiFi → WiFiScan. Click Upload. If the sketch compiles and uploads successfully, your Board Manager installation is fully operational.</p>

<h2>Understanding the Board List</h2>
<p>The ESP32 Arduino core includes board definitions for over 100 variants. Most beginners only need a handful:</p>

<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Board Selection</th><th>Use When</th></tr></thead>
<tbody>
<tr><td>ESP32 Dev Module</td><td>Generic ESP32 DevKitC, any WROOM-32 board, or unlisted ESP32 boards</td></tr>
<tr><td>NodeMCU-32S</td><td>NodeMCU-32S boards (CP2102 USB chip, 38 pins)</td></tr>
<tr><td>ESP32 Wrover Module</td><td>WROVER-based boards — enables PSRAM by default</td></tr>
<tr><td>AI Thinker ESP32-CAM</td><td>AI-Thinker ESP32-CAM camera boards</td></tr>
<tr><td>Adafruit ESP32 Feather</td><td>Adafruit HUZZAH32 Feather boards</td></tr>
<tr><td>ESP32-S3 Dev Module</td><td>ESP32-S3 DevKitC boards and S3-based custom boards</td></tr>
<tr><td>ESP32-C3 Dev Module</td><td>ESP32-C3 DevKitM and C3-based boards</td></tr>
<tr><td>WEMOS D1 MINI ESP32</td><td>LOLIN32 / WEMOS D32 boards</td></tr>
</tbody>
</table>
</div>

<p>If your specific board is not listed, use "ESP32 Dev Module" — it is the most generic setting and works for any standard ESP32 WROOM-32 board. The main difference between board definitions is the default flash size, partition scheme, and PSRAM settings. You can override all of these manually under the Tools menu after selecting a board.</p>

<h2>Important Tools Settings After Board Selection</h2>
<p>After selecting your board, review these settings under the Tools menu:</p>

<ul>
<li><strong>CPU Frequency:</strong> 240 MHz for maximum performance; 80 MHz for lower power consumption. Most projects use 240 MHz.</li>
<li><strong>Flash Frequency:</strong> 80 MHz is the standard and fastest. Some cheaper flash chips are only rated to 40 MHz — use 40 MHz if you experience random flash-read crashes.</li>
<li><strong>Flash Size:</strong> Must match your board's actual flash chip. Selecting 4 MB on a board with 2 MB flash will cause the partition table to reference addresses that do not exist, causing boot failures.</li>
<li><strong>Partition Scheme:</strong> "Default 4MB with spiffs" is the standard. "Huge APP (3MB No OTA)" gives more space for the sketch at the cost of OTA capability. "Minimal SPIFFS (1.9MB APP with OTA)" allocates more space to OTA and SPIFFS.</li>
<li><strong>PSRAM:</strong> Enable this if your board has a WROVER module with external PSRAM. Enabling it on a board without PSRAM does not crash the chip but ps_malloc() calls will fail.</li>
<li><strong>Upload Speed:</strong> 921600 for fast uploads. Reduce to 460800 or 115200 if uploads fail.</li>
</ul>

<h2>Managing Multiple Core Versions</h2>
<p>You can install multiple versions of the ESP32 core side by side. In the Boards Manager, click the version dropdown before clicking Install to choose a specific version. Old versions remain available even after installing a new one — click the dropdown again and select an older version to "Install" it alongside the newer one. Switch between versions by selecting the desired version in the Boards Manager dropdown. The currently active version for a sketch is whichever was selected when you last compiled it.</p>

<p>Common reason to keep multiple versions: a library you depend on has a known bug fix in v2.0.14 but a regression in v2.0.17. Keep both installed and use v2.0.14 for that specific project while using the latest for new projects.</p>

<h2>Troubleshooting Board Manager Issues</h2>
<h3>Download stalls or fails</h3>
<p>Check your internet connection and firewall. The download server is GitHub's CDN. If you are behind a corporate proxy, configure proxy settings in File → Preferences → Network. Alternatively, download the core ZIP manually from the GitHub releases page and install it using the offline install procedure (copy files to the Arduino15 packages directory).</p>

<h3>Boards Manager shows "Error downloading..."</h3>
<p>The index URL may be incorrect, or the file at that URL is temporarily unavailable. Verify the URL by opening it in a browser — it should return a JSON file. If the URL is correct, wait a few minutes and try again (GitHub's CDN occasionally has temporary outages).</p>

<h3>Core installed but no ESP32 boards appear in Tools → Board</h3>
<p>Restart the Arduino IDE completely. If the issue persists, the installation may be corrupt. Delete the ESP32 packages directory manually: on Windows at <code>%APPDATA%\Local\Arduino15\packages\esp32</code>, on Linux/macOS at <code>~/.arduino15/packages/esp32</code>. Then reinstall from the Boards Manager.</p>

<h3>Compilation error: "xtensa-esp32-elf-g++: not found"</h3>
<p>The toolchain binaries are not executable. This can happen if antivirus software quarantined them during download, or if the download was interrupted leaving a partial toolchain. Uninstall the core from Boards Manager and reinstall. On Windows, temporarily pause antivirus software during installation if this recurs.</p>

<h2>Keeping the Core Updated</h2>
<p>When a new ESP32 core version is released, the Boards Manager shows an "Update" button next to the installed version. Click it to download and install the new version. After updating, recompile and re-test your projects — API changes between versions occasionally require small code adjustments. Espressif documents breaking changes in the MIGRATION_GUIDES directory of the GitHub repository.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'platformio-vs-arduino-ide',
'title'        => 'PlatformIO vs Arduino IDE for ESP32: Feature Comparison and Migration Guide',
'meta_desc'    => 'Compare PlatformIO and Arduino IDE for ESP32 development. Covers project structure, library management, board configuration, debugging, CI/CD integration, and which to choose for your workflow.',
'read_time'    => '15 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'Should beginners start with Arduino IDE or PlatformIO?','answer'=>'Start with Arduino IDE. It has a simpler interface, the most tutorials target it, and the Board Manager installation is one step. Migrate to PlatformIO when you hit the limitations: poor multi-file project support, no dependency version pinning, or you want better integration with VS Code editing tools like IntelliSense and Git. Most experienced ESP32 developers eventually prefer PlatformIO for professional projects.'],
  ['question'=>'Can PlatformIO use Arduino libraries?','answer'=>'Yes, fully. PlatformIO\'s library registry (registry.platformio.org) mirrors the Arduino Library Manager catalog and adds thousands more libraries. PlatformIO.ini\'s lib_deps field lists libraries by name and version: lib_deps = bblanchon/ArduinoJson@^7.0.4. PlatformIO downloads and manages them automatically without you touching any files.'],
  ['question'=>'Does PlatformIO work with the same ESP32 code as Arduino IDE?','answer'=>'Yes for most code. The main difference is that PlatformIO requires a main .cpp file with a standard C++ main() or Arduino-style setup()/loop() declared explicitly. In Arduino IDE, the IDE wraps your .ino in a C++ class and provides main() automatically. In PlatformIO\'s Arduino framework, include <Arduino.h> and write setup()/loop() as usual — the framework provides main() for you.'],
  ['question'=>'How does PlatformIO manage dependencies differently from Arduino IDE?','answer'=>'Arduino IDE\'s library manager installs libraries globally — one version for all projects. PlatformIO installs libraries per-project and stores the exact version in platformio.ini. This means project A can use ArduinoJson v6 while project B uses v7, with no conflicts. PlatformIO also supports semantic version ranges (^7.0.4 = latest 7.x patch), enabling automatic minor-version updates while protecting against breaking major-version changes.'],
  ['question'=>'Can I import an existing Arduino .ino project into PlatformIO?','answer'=>'Yes. In VS Code with PlatformIO installed, use the "Import Arduino Project" option in the PlatformIO home tab. It reads the existing sketch, creates a platformio.ini with the correct framework and board, and copies your source files. You may need to add library dependencies manually to lib_deps since the .ino file does not track them.'],
  ['question'=>'Does PlatformIO support ESP32-S3, ESP32-C3, and other variants?','answer'=>'Yes. PlatformIO supports all ESP32 variants by specifying the board in platformio.ini. Common board IDs: esp32dev (original), esp32-s3-devkitc-1 (S3), esp32-c3-devkitm-1 (C3). The full list is at docs.platformio.org/boards. Each board entry specifies the correct framework, toolchain, and default settings automatically.'],
  ['question'=>'Does PlatformIO have a Serial Monitor?','answer'=>'Yes. Run "pio device monitor" in the terminal, or click the plug icon in the PlatformIO toolbar in VS Code. The baud rate is configured in platformio.ini: monitor_speed = 115200. The PlatformIO monitor supports ANSI colours, timestamps, filters (like a simple protocol decoder), and logging to file — features the Arduino IDE Serial Monitor lacks.'],
  ['question'=>'Can I use PlatformIO with ESP-IDF (not Arduino framework)?','answer'=>'Yes. Set framework = espidf in platformio.ini instead of arduino. PlatformIO downloads the configured ESP-IDF version and provides idf.py equivalent commands. You can also use a hybrid: framework = arduino, espidf — which enables using IDF APIs directly alongside the Arduino abstraction layer.'],
  ['question'=>'What is the PlatformIO home tab and do I need it?','answer'=>'The PlatformIO home tab is a graphical interface in VS Code that lets you create new projects, import existing ones, browse the library registry, and manage installed platforms. It is optional — everything it offers is also available via the command line (pio project init, pio lib install, pio run). Beginners may find the home tab easier; experienced developers often prefer the CLI.'],
  ['question'=>'Does PlatformIO support JTAG debugging for ESP32?','answer'=>'Yes, and this is one of PlatformIO\'s significant advantages over Arduino IDE. Configure debug_tool = esp-prog in platformio.ini, connect an ESP-Prog JTAG adapter, and use the VS Code debug sidebar to set breakpoints, inspect variables, step through code, and view the call stack. Arduino IDE has no comparable debugging capability for ESP32 (it requires a separate OpenOCD setup).'],
],
'related' => [
  ['title'=>'VS Code with ESP32','slug'=>'vscode-with-esp32'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
  ['title'=>'Installing ESP-IDF','slug'=>'installing-esp-idf'],
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
],
'body_html' => <<<'HTML'
<h2>Two Tools for the Same Chip</h2>
<p>The Arduino IDE and PlatformIO are both excellent ways to write, compile, and upload ESP32 firmware. They compile the same code, use the same ESP32 Arduino core, and produce identical binaries. The differences are in developer experience: project organisation, dependency management, editor capabilities, debugging, and fit with professional development workflows. Neither tool is objectively better — the right choice depends on your background, project complexity, and how much time you want to invest in tooling setup.</p>

<p>This guide compares every relevant dimension side by side and gives you a clear migration path if you decide to switch.</p>

<h2>Feature Comparison Table</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Feature</th><th>Arduino IDE 2.x</th><th>PlatformIO (VS Code)</th></tr></thead>
<tbody>
<tr><td>Installation complexity</td><td>Low — one installer</td><td>Medium — VS Code + PlatformIO extension</td></tr>
<tr><td>Code editor quality</td><td>Basic (improving in 2.x)</td><td>Excellent — full VS Code IntelliSense</td></tr>
<tr><td>Multi-file projects</td><td>Limited (.ino tabs only)</td><td>Full C++ project structure</td></tr>
<tr><td>Library management</td><td>Global install, no versioning</td><td>Per-project, version-pinned</td></tr>
<tr><td>Board configuration</td><td>GUI menus</td><td>platformio.ini text file</td></tr>
<tr><td>Hardware debugging</td><td>None (ESP32)</td><td>Full JTAG via OpenOCD</td></tr>
<tr><td>CI/CD integration</td><td>Difficult</td><td>Excellent (pio run in scripts)</td></tr>
<tr><td>Serial Monitor</td><td>Basic</td><td>Filters, colours, logging, timestamps</td></tr>
<tr><td>ESP-IDF support</td><td>Via Arduino core only</td><td>Native IDF or Arduino+IDF hybrid</td></tr>
<tr><td>Git integration</td><td>None</td><td>Full VS Code Git sidebar</td></tr>
<tr><td>Community tutorials</td><td>Vast — most tutorials target Arduino IDE</td><td>Good — growing rapidly</td></tr>
<tr><td>Learning curve</td><td>Very low</td><td>Moderate</td></tr>
</tbody>
</table>
</div>

<h2>Arduino IDE: Strengths and Limitations</h2>
<p>Arduino IDE's primary strength is simplicity. Install it, add the ESP32 URL, click Install in the Boards Manager, select your board, and write a sketch. The entire onboarding takes under 30 minutes. The IDE handles library downloads, port selection, and the upload process with minimal configuration. This makes it the fastest way to get to a working first project.</p>

<p>The limitations emerge as projects grow. Large projects with multiple source files become awkward — Arduino IDE forces all code into .ino files (which are actually .cpp files with a preprocessed wrapper), and navigation between many .ino tabs in one sketch folder is tedious. Library management installs globally to a shared folder, so upgrading a library for one project can break another that depends on the older version. There is no dependency file associated with a sketch, making it hard to reproduce the exact build environment on another computer. And hardware debugging requires an entirely separate OpenOCD setup outside the IDE.</p>

<h2>PlatformIO: Strengths and Limitations</h2>
<p>PlatformIO runs as a VS Code extension, giving you the world's most popular code editor with full IntelliSense, syntax highlighting, jump-to-definition, refactoring, Git integration, and a rich extension ecosystem — all for ESP32 development. Library dependencies are listed in platformio.ini with version constraints, making projects reproducible across machines. A new collaborator clones your repo, opens it in VS Code, and PlatformIO automatically downloads every dependency at the pinned version.</p>

<p>JTAG debugging is PlatformIO's most significant advantage for complex projects. Hardware breakpoints, variable inspection, and call stack visibility catch logic errors that Serial.print debugging misses. For production firmware development, this difference alone justifies the setup complexity.</p>

<p>The limitation is setup time. Installing VS Code, the PlatformIO extension, and letting it download the ESP32 toolchain takes 20–30 minutes on first run. Configuration is text-file-based rather than menu-driven, which is faster once learned but has a steeper initial curve. Most online tutorials show Arduino IDE code, which ports easily but may reference menu paths that do not exist in PlatformIO.</p>

<h2>PlatformIO Project Structure</h2>
<p>A PlatformIO project for ESP32 looks like this:</p>
<pre><code>my_project/
├── platformio.ini      ← project configuration
├── src/
│   └── main.cpp        ← your application code
├── include/            ← project-wide header files
├── lib/                ← project-local libraries
├── test/               ← unit tests
└── .pio/               ← build cache (git-ignore this)</code></pre>

<p>The <code>platformio.ini</code> file is the heart of a PlatformIO project:</p>
<pre><code>[env:esp32dev]
platform  = espressif32
board     = esp32dev
framework = arduino

monitor_speed   = 115200
upload_speed    = 921600

build_flags =
  -DDEBUG_LEVEL=2
  -DWIFI_SSID=\"MyNetwork\"
  -DWIFI_PASS=\"secret\"

lib_deps =
  bblanchon/ArduinoJson @ ^7.0.4
  knolleary/PubSubClient @ ^2.8.0
  adafruit/DHT sensor library @ ^1.4.6</code></pre>

<p>Every configuration option that requires navigating menus in Arduino IDE lives here as a readable, version-controllable text file. <code>build_flags</code> inject preprocessor definitions at compile time — useful for setting Wi-Fi credentials without hardcoding them in source code (instead they come from an environment-specific .ini file excluded from git). <code>lib_deps</code> lists all required libraries — PlatformIO downloads them automatically on the first build.</p>

<h2>Migrating from Arduino IDE to PlatformIO</h2>
<p>Migration is straightforward:</p>
<ol>
<li>Install VS Code from code.visualstudio.com</li>
<li>Open VS Code, go to the Extensions sidebar (Ctrl+Shift+X), search "PlatformIO IDE", click Install</li>
<li>After installation (it downloads toolchains in the background), open the PlatformIO home tab (the PlatformIO alien icon in the left sidebar)</li>
<li>Click "Import Arduino Project", select your Arduino sketch folder</li>
<li>PlatformIO creates platformio.ini with the detected board and framework</li>
<li>Add any missing library dependencies to lib_deps in platformio.ini</li>
<li>Click the checkmark (Build) or arrow (Upload) in the PlatformIO toolbar</li>
</ol>

<p>Your .ino file stays valid — Arduino's setup() and loop() structure works unchanged in PlatformIO's Arduino framework. The only required change is adding <code>#include &lt;Arduino.h&gt;</code> at the top of your main file if it is not already there.</p>

<h2>Running Both Tools in Parallel</h2>
<p>Many developers use both: Arduino IDE for quick experiments, small sketches, and projects following tutorials; PlatformIO for multi-file production projects where dependency management, debugging, and CI/CD matter. There is no conflict — the two tools share the same ESP32 hardware and can flash the same board. The toolchains are stored independently, so an update in one does not affect the other.</p>

<h2>PlatformIO for CI/CD</h2>
<p>PlatformIO's command-line interface makes it suitable for automated build pipelines. In a GitHub Actions workflow:</p>
<pre><code>name: Build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v3
        with:
          path: ~/.platformio
          key: ${{ runner.os }}-pio-${{ hashFiles('platformio.ini') }}
      - run: pip install platformio
      - run: pio run</code></pre>

<p>Every commit triggers a compilation check across all configured environments in platformio.ini. If the build breaks, the CI system reports it immediately — before you flash a broken binary to hardware. Arduino IDE has no equivalent automated build workflow without third-party tooling.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'vscode-with-esp32',
'title'        => 'VS Code with ESP32: PlatformIO and ESP-IDF Extension Setup Guide',
'meta_desc'    => 'Set up VS Code for ESP32 development using PlatformIO or the Espressif IDF extension. Covers IntelliSense configuration, JTAG debugging, CMake integration, and recommended extensions.',
'read_time'    => '14 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What is VS Code and why use it for ESP32?','answer'=>'VS Code (Visual Studio Code) is Microsoft\'s free, open-source code editor. For ESP32 development it offers IntelliSense (code completion, type checking, jump-to-definition), integrated Git, a built-in terminal, an extension ecosystem that adds ESP32-specific features, and a debugging interface that works with JTAG hardware debuggers. It is the most popular code editor among professional embedded developers and is free.'],
  ['question'=>'Is the PlatformIO extension or the Espressif IDF extension better for VS Code?','answer'=>'They serve different workflows. The PlatformIO extension is ideal if you use the Arduino framework — it manages board packages, libraries, and provides a familiar build/upload/monitor workflow with excellent library dependency management. The Espressif IDF extension is ideal if you use native ESP-IDF (FreeRTOS-based development) — it wraps idf.py commands in a GUI, integrates menuconfig, and provides component management. You can have both installed simultaneously.'],
  ['question'=>'Does VS Code work without internet after initial setup?','answer'=>'Yes. Once PlatformIO or ESP-IDF is installed and your project\'s dependencies are downloaded, you can build, upload, and debug entirely offline. The extensions only need internet to download new toolchain versions, library updates, or extension updates. For air-gapped environments, pre-download the toolchains and configure PlatformIO to use offline packages.'],
  ['question'=>'How do I fix IntelliSense showing "Cannot open source file WiFi.h" errors?','answer'=>'IntelliSense errors in PlatformIO projects resolve after a full build (Ctrl+Alt+B). The build generates a compile_commands.json file that tells the C++ IntelliSense engine where to find include paths. Without it, IntelliSense searches only standard system paths. If the error persists after building, click the "IntelliSense configuration provider: PlatformIO" in the VS Code bottom status bar and select "Rebuild IntelliSense Index".'],
  ['question'=>'Can I use VS Code to flash the ESP32 without PlatformIO?','answer'=>'Yes, using the Espressif IDF extension which wraps idf.py flash commands. Alternatively, install the esptool.py CLI and run it from VS Code\'s integrated terminal. You can also add a VS Code task (tasks.json) that runs your upload command with a keyboard shortcut, without needing any extension.'],
  ['question'=>'How do I add a launch configuration for debugging in VS Code?','answer'=>'PlatformIO automatically creates a launch.json for JTAG debugging when you add debug_tool = esp-prog to platformio.ini. Press F5 or click the Run and Debug sidebar (Ctrl+Shift+D) to start a debug session. For ESP-IDF, the IDF extension creates an OpenOCD-based launch configuration automatically. Connect the JTAG probe, set a breakpoint by clicking the gutter, and press F5 to debug.'],
  ['question'=>'What is c_cpp_properties.json and do I need to edit it?','answer'=>'c_cpp_properties.json configures the VS Code C/C++ IntelliSense engine — it lists include paths, defines, and the compiler to use for code analysis. In PlatformIO projects, this file is auto-generated and updated by the extension after each build. Do not edit it manually in PlatformIO projects — your changes will be overwritten. If IntelliSense does not work, delete the file and trigger a rebuild to regenerate it cleanly.'],
  ['question'=>'Can I develop for ESP32 on VS Code running on a Raspberry Pi?','answer'=>'Yes. Install the ARM64 version of VS Code and the PlatformIO extension. PlatformIO supports Linux ARM64 and downloads the correct toolchain binaries. Build times on a Pi 4 are slower than on x86 hardware but everything functions correctly. The ESP-IDF extension also works on ARM64 Linux. Serial monitor and upload work the same as on x86 — the ESP32 connects via USB and appears as /dev/ttyUSB0.'],
  ['question'=>'How do I use VS Code\'s integrated Git with ESP32 projects?','answer'=>'Create a .gitignore file in your project root to exclude build output and platform-specific caches: add .pio/, build/, and sdkconfig to it for PlatformIO and IDF projects respectively. Then use VS Code\'s Source Control sidebar (Ctrl+Shift+G) to stage, commit, and push changes. The integrated Git workflow is one of VS Code\'s major advantages over Arduino IDE, which has no source control integration.'],
  ['question'=>'Does VS Code\'s remote SSH feature work for ESP32 development?','answer'=>'Yes. VS Code Remote - SSH lets you connect to a Linux server or Raspberry Pi over SSH and develop as if the remote machine were local — including running PlatformIO builds on the remote, accessing its serial ports (with serial port forwarding via usbipd-win or socat), and even debugging. This allows developing on a powerful desktop while the ESP32 is physically connected to a Pi in another room.'],
],
'related' => [
  ['title'=>'PlatformIO vs Arduino IDE','slug'=>'platformio-vs-arduino-ide'],
  ['title'=>'Installing ESP-IDF','slug'=>'installing-esp-idf'],
  ['title'=>'Flashing ESP32 Firmware','slug'=>'flashing-esp32-firmware'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
],
'body_html' => <<<'HTML'
<h2>Why VS Code for ESP32?</h2>
<p>VS Code is the editor of choice for the majority of ESP32 developers who move beyond the Arduino IDE. Its combination of a first-class editing experience (IntelliSense, multi-cursor editing, split panes, integrated terminal), deep Git integration, and a rich extension marketplace makes it a significant productivity upgrade over the Arduino IDE's basic text editor. Two official extensions bring ESP32 development into VS Code: the PlatformIO IDE extension (for Arduino framework development) and the ESP-IDF VS Code Extension by Espressif (for native IDF development).</p>

<h2>Installing VS Code</h2>
<p>Download VS Code from <strong>code.visualstudio.com</strong>. It is available for Windows, macOS, and Linux. The installer is 100 MB and the app launches in under 5 seconds on modern hardware. VS Code is updated monthly — accept updates when prompted; updates never break existing projects because extensions and project settings are stored independently from the application binary.</p>

<p>After installation, install the C/C++ extension from Microsoft (search "C/C++" in the Extensions sidebar, Ctrl+Shift+X) — this provides IntelliSense for C and C++ code. You do not need to configure it separately; both PlatformIO and the IDF extension configure it automatically as part of their project setup.</p>

<h2>Option A: PlatformIO IDE Extension</h2>
<p>PlatformIO is the most popular extension for Arduino framework ESP32 development in VS Code. Install it from the Extensions sidebar: search "PlatformIO IDE" and click Install. After installation (it downloads toolchains in the background — this takes several minutes), the PlatformIO icon (a circular design) appears in the left activity bar.</p>

<h3>Creating Your First PlatformIO ESP32 Project</h3>
<ol>
<li>Click the PlatformIO icon → "New Project"</li>
<li>Name: My_ESP32_Project</li>
<li>Board: Search "ESP32 Dev Module" and select it</li>
<li>Framework: Arduino</li>
<li>Location: (choose a folder)</li>
<li>Click Finish</li>
</ol>

<p>PlatformIO creates the project structure and downloads the ESP32 platform (toolchain + framework) if not already installed. Open <code>src/main.cpp</code> — it contains a starter template with <code>#include &lt;Arduino.h&gt;</code>, <code>setup()</code>, and <code>loop()</code>. Write your code here exactly as you would in Arduino IDE.</p>

<p>The PlatformIO toolbar appears at the bottom status bar of VS Code:</p>
<ul>
<li>✓ (checkmark) — Build/Compile</li>
<li>→ (right arrow) — Upload</li>
<li>🔌 (plug) — Serial Monitor</li>
<li>⬆ (upload with monitor) — Upload + open monitor</li>
</ul>

<h3>Configuring platformio.ini</h3>
<p>All project configuration lives in <code>platformio.ini</code> at the project root. A full configuration for an ESP32 project:</p>

<pre><code>[env:esp32dev]
platform        = espressif32
board           = esp32dev
framework       = arduino
monitor_speed   = 115200
monitor_filters = esp32_exception_decoder  ; decode crash stack traces automatically
upload_speed    = 921600
build_flags     =
  -DCORE_DEBUG_LEVEL=2
  -DBOARD_HAS_PSRAM

lib_deps =
  bblanchon/ArduinoJson @ ^7.0.4
  knolleary/PubSubClient @ ^2.8.0
  adafruit/Adafruit_BME280_Library @ ^2.2.4</code></pre>

<p>The <code>esp32_exception_decoder</code> monitor filter is particularly valuable — when the ESP32 crashes and prints a stack trace (hex addresses), the filter automatically decodes it into function names and line numbers, showing you exactly where in your code the crash occurred.</p>

<h2>Option B: Espressif IDF Extension</h2>
<p>The ESP-IDF extension by Espressif is the official tool for native IDF development in VS Code. Install it from the Extensions sidebar: search "ESP-IDF" by Espressif Systems and install it.</p>

<p>On first use, run the command "ESP-IDF: Configure ESP-IDF extension" (Ctrl+Shift+P, type "ESP-IDF Configure"). The setup wizard asks you to:</p>
<ol>
<li>Choose express or advanced setup mode (express is fine for most users)</li>
<li>Select your Python executable</li>
<li>Choose the ESP-IDF version to download (or point to an existing installation)</li>
<li>Choose the tools download directory</li>
</ol>

<p>Express mode downloads ESP-IDF and all toolchains automatically — about 15–20 GB total. When complete, the IDF extension is fully configured.</p>

<h3>IDF Extension Key Commands</h3>
<p>All IDF extension commands are available through the VS Code command palette (Ctrl+Shift+P):</p>
<ul>
<li><strong>ESP-IDF: Build your Project</strong> — equivalent to idf.py build</li>
<li><strong>ESP-IDF: Flash your Project</strong> — equivalent to idf.py flash</li>
<li><strong>ESP-IDF: Monitor Device</strong> — equivalent to idf.py monitor</li>
<li><strong>ESP-IDF: Launch GUI Menuconfig Tool</strong> — opens menuconfig in a VS Code webview panel</li>
<li><strong>ESP-IDF: Set Espressif Device Target</strong> — sets the chip target (esp32, esp32s3, etc.)</li>
<li><strong>ESP-IDF: Create project from Extension Template</strong> — creates a new IDF project with CMakeLists.txt</li>
</ul>

<p>The IDF extension also adds a sidebar panel showing your project components, available examples, and a GUI menuconfig — a significant improvement over the terminal-based menuconfig for configuration-heavy projects.</p>

<h2>Setting Up JTAG Hardware Debugging</h2>
<p>JTAG debugging requires a hardware probe. Common options:</p>
<ul>
<li><strong>ESP-Prog</strong> — Espressif's official JTAG+UART programmer, ~$15, plug-and-play with both extensions</li>
<li><strong>J-Link EDU</strong> — Segger's popular debug probe, excellent software support, ~$60</li>
<li><strong>FTDI FT2232H breakout</strong> — budget option, requires manual OpenOCD configuration</li>
</ul>

<p>For PlatformIO, add to platformio.ini:</p>
<pre><code>debug_tool  = esp-prog
debug_init_break = tbreak app_main</code></pre>

<p>Press F5 to start debugging. VS Code enters debug mode: a debug toolbar appears at the top, the Variables panel shows current variable values, the Call Stack panel shows the function call chain, and you can set breakpoints by clicking the gutter (red dot) next to any line. Execution pauses at each breakpoint, letting you inspect state without any Serial.print statements.</p>

<h2>Recommended Extensions for ESP32 Development</h2>
<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Extension</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td>PlatformIO IDE</td><td>Full ESP32 Arduino framework build, upload, monitor</td></tr>
<tr><td>ESP-IDF (Espressif)</td><td>Native IDF development, menuconfig GUI, component management</td></tr>
<tr><td>C/C++ (Microsoft)</td><td>IntelliSense, syntax highlighting, error detection</td></tr>
<tr><td>GitLens</td><td>Enhanced Git — blame annotations, history browsing, comparison</td></tr>
<tr><td>Better Comments</td><td>Colour-coded comment types (TODO, FIXME, NOTE, WARN)</td></tr>
<tr><td>Hex Editor (Microsoft)</td><td>View and edit binary files, .bin firmware images</td></tr>
<tr><td>Remote - SSH</td><td>Develop on a remote Linux machine or Raspberry Pi</td></tr>
<tr><td>Error Lens</td><td>Shows compiler errors inline at the problematic line</td></tr>
</tbody>
</table>
</div>

<h2>Useful VS Code Settings for ESP32 Projects</h2>
<p>Add these to your VS Code settings.json (Ctrl+Shift+P → "Open User Settings JSON") for a more comfortable ESP32 development experience:</p>
<pre><code>{
  "editor.formatOnSave": false,         // don't auto-format; C++ style varies
  "editor.tabSize": 4,                  // 4-space indentation
  "files.trimTrailingWhitespace": true, // clean commits
  "terminal.integrated.shell.windows": "cmd.exe",  // for IDF CMD compatibility
  "C_Cpp.intelliSenseEngine": "default",
  "C_Cpp.default.cStandard": "c17",
  "C_Cpp.default.cppStandard": "c++17"
}</code></pre>

<p>These settings are personal preferences — adjust them to match your team's coding style. The C++ standard settings (c17, c++17) match the standard the ESP32 Arduino core uses, preventing false IntelliSense errors for C17/C++17 features.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'flashing-esp32-firmware',
'title'        => 'Flashing ESP32 Firmware: esptool.py, Flash Download Tool, and Recovery',
'meta_desc'    => 'Complete guide to flashing ESP32 firmware using esptool.py command line, Espressif Flash Download Tool GUI, and recovering a bricked ESP32 with a blank flash wipe.',
'read_time'    => '13 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What is "flashing" in ESP32 context?','answer'=>'Flashing means writing firmware to the ESP32\'s external SPI flash memory chip. The term comes from "flash memory" — the non-volatile storage that retains data without power. When you click Upload in Arduino IDE, the IDE invokes esptool.py to flash your compiled binary (.bin file) to the flash chip via the UART bootloader.'],
  ['question'=>'How do I find the correct flash address for my firmware?','answer'=>'The correct addresses are: 0x1000 for the bootloader, 0x8000 for the partition table, and 0x10000 for the application firmware. These are fixed for the standard ESP32 bootloader. When using esptool.py merge_bin or Arduino IDE verbose upload output, you can see all addresses being used. The application at 0x10000 is the standard address for the first app partition.'],
  ['question'=>'Can I flash the ESP32 over USB without any special software besides a web browser?','answer'=>'Yes. The Web Serial API allows flashing ESP32 directly from a Chrome/Edge browser using online tools. Navigate to esp.huhn.me or esptool.js (web-based esptool implementation) in Chrome, click Connect, select your ESP32\'s serial port, and flash a .bin file. No driver installation is required on modern Windows 11 or macOS. This is the easiest way to share firmware with non-technical users.'],
  ['question'=>'How do I recover an ESP32 that seems completely bricked?','answer'=>'A seemingly bricked ESP32 is almost always recoverable via a full flash erase and reflash. Put the board in download mode (GPIO 0 low at reset), run "esptool.py --port COM3 erase_flash" to wipe everything, then reflash your firmware from scratch. The bootloader in protected ROM cannot be overwritten by normal flash operations — the recovery path always exists.'],
  ['question'=>'What is the difference between esptool.py write_flash and flash_id?','answer'=>'flash_id reads and displays the flash chip\'s manufacturer ID, device ID, and total capacity — it does not write anything. Use it to verify esptool.py can communicate with the ESP32 and to confirm the actual flash size matches what you expect. write_flash writes binary data to specified addresses in flash. Always run flash_id first when diagnosing connection issues.'],
  ['question'=>'Can I flash over Wi-Fi without the ArduinoOTA library?','answer'=>'Yes. ESP-IDF includes the native OTA component (esp_https_ota) which supports pulling firmware from an HTTPS URL. There are also community tools like esp-web-tools which provide a browser-based OTA update page using Web Serial. For industrial deployments, custom OTA servers can serve firmware over HTTPS with signature verification and rollback support.'],
  ['question'=>'Does flashing erase all user data in NVS and SPIFFS?','answer'=>'A standard firmware upload (via Arduino IDE or esptool.py write_flash at 0x10000) only writes to the application partition — it leaves NVS, SPIFFS, and other partitions untouched. Only "Erase All Flash" (esptool.py erase_flash) wipes everything including user data. Use targeted partition writes to update firmware without losing configuration.'],
  ['question'=>'What baud rate does esptool.py use for flashing?','answer'=>'esptool.py starts negotiation at 115200 baud (the bootloader\'s default speed), then renegotiates to a higher speed (typically 921600 or 460800) for the actual flash write. You can force a specific speed with the --baud flag. Higher baud rates flash faster but may fail on long USB cables or noisy connections.'],
  ['question'=>'Is there a way to protect ESP32 firmware from being read back?','answer'=>'Yes. The ESP32 supports Flash Encryption, which encrypts the flash contents with a key burned into eFuse. Once encryption is enabled, the flash cannot be read in plaintext via esptool.py or JTAG. Additionally, Secure Boot verifies that only firmware signed with your private key is loaded. These features are documented in the ESP-IDF security guide and are intended for production devices containing proprietary firmware.'],
  ['question'=>'How can I see exactly what esptool.py command Arduino IDE uses?','answer'=>'Enable verbose upload output in Arduino IDE under File → Preferences → Show verbose output during upload. When you next upload, the console shows the complete esptool.py command line including all arguments, addresses, and binary file paths. You can copy this command and run it directly in a terminal for scripting or CI purposes.'],
],
'related' => [
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
  ['title'=>'Updating ESP32 Firmware','slug'=>'updating-esp32-firmware'],
  ['title'=>'Installing Arduino IDE for ESP32','slug'=>'installing-arduino-ide-esp32'],
  ['title'=>'ESP32 Boot Strapping Pins Explained','slug'=>'esp32-boot-strapping-pins'],
],
'body_html' => <<<'HTML'
<h2>What Happens When You Flash</h2>
<p>Flashing firmware to an ESP32 is a three-phase process. First, the host computer signals the ESP32 to enter download mode by asserting the DTR and RTS lines on the USB-to-serial chip in a specific sequence that grounds GPIO 0 while pulsing the EN (reset) pin. Second, esptool.py communicates with the ROM bootloader over UART, negotiating from the bootloader's fixed 115200 baud start to a higher transfer speed. Third, the binary data is written to the SPI flash chip in 4 KB sector-sized chunks with CRC verification after each write.</p>

<p>Understanding this pipeline helps when diagnosing failures: if the process stalls at "Connecting...", the boot mode negotiation failed; if it fails partway through with a CRC error, the flash write is being corrupted; if the board does not run after a successful flash, the binary addresses are wrong.</p>

<h2>Method 1: esptool.py — The Universal Command-Line Tool</h2>
<p>esptool.py is the open-source Python tool that Arduino IDE, PlatformIO, and ESP-IDF all use internally. You can use it directly for tasks the IDEs do not expose through their GUIs. Install it with pip:</p>

<pre><code>pip install esptool</code></pre>

<p>Verify installation:</p>
<pre><code>esptool.py version</code></pre>

<h3>Detect Flash Information</h3>
<p>Always start with flash_id to confirm esptool can communicate with the device:</p>
<pre><code>esptool.py --port COM3 flash_id</code></pre>

<p>Expected output:</p>
<pre><code>Connecting...
Detecting chip type... ESP32
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse
Crystal is 40MHz
Detecting flash size... 4MB
Manufacturer: c8
Device: 4016</code></pre>

<p>The "Manufacturer: c8" and "Device: 4016" are the flash chip's ID codes. This output confirms: the chip type, flash size, and crystal frequency. If you see "Failed to connect" here, the issue is hardware (cable, driver, boot mode) not the flash itself.</p>

<h3>Erase All Flash</h3>
<pre><code>esptool.py --port COM3 erase_flash</code></pre>

<p>This erases all 4 MB of flash, including the application, bootloader, partition table, NVS, and any file system. After this the ESP32 will not boot until you flash a new firmware. Use this when: resetting a corrupted device, clearing factory-burned firmware, or ensuring a completely clean starting point.</p>

<h3>Flash a Complete Firmware</h3>
<p>For a full firmware flash (bootloader + partition table + application):</p>
<pre><code>esptool.py --port COM3 --baud 921600 write_flash \
  0x1000  bootloader.bin \
  0x8000  partitions.bin \
  0xe000  ota_data_initial.bin \
  0x10000 firmware.bin</code></pre>

<p>The four binaries and their addresses are the standard layout for a default ESP32 OTA partition scheme. You can find these files in the Arduino build directory (enable verbose output to see the exact path) or in the ESP-IDF build/ subdirectory of your project.</p>

<h3>Flash Only the Application (Fast Update)</h3>
<pre><code>esptool.py --port COM3 --baud 921600 write_flash 0x10000 firmware.bin</code></pre>

<p>Writing only the application binary (at 0x10000) leaves the bootloader, partition table, NVS, and file system intact. This is the fastest way to update firmware without disturbing user data — the same operation Arduino IDE performs when you click Upload.</p>

<h3>Merge All Binaries into One File</h3>
<p>For distributing firmware to end users or for web-based flashing:</p>
<pre><code>esptool.py merge_bin \
  --flash_size 4MB \
  -o merged-firmware.bin \
  0x1000  bootloader.bin \
  0x8000  partitions.bin \
  0xe000  ota_data_initial.bin \
  0x10000 firmware.bin</code></pre>

<p>The merged file contains padding to maintain correct addresses, so it can be flashed with a single command at address 0x0 using the web-based ESP Tool or Flash Download Tool without specifying individual files.</p>

<h2>Method 2: Espressif Flash Download Tool (Windows GUI)</h2>
<p>The Flash Download Tool is Espressif's official GUI application for Windows. Download it from the Espressif website. It is useful for: batch programming multiple boards simultaneously, flashing pre-built binary packages without command-line knowledge, and production programming environments.</p>

<p>Launch the tool and select "ESP32" in the chip dropdown. You will see a grid of file/address pairs. For a standard firmware:</p>
<ol>
<li>Check the first row, click "..." to browse to bootloader.bin, enter 0x1000 in the address field</li>
<li>Check the second row for partitions.bin at 0x8000</li>
<li>Check the third row for ota_data_initial.bin at 0xe000</li>
<li>Check the fourth row for firmware.bin at 0x10000</li>
<li>Set COM port (dropdown on right) and baud rate (921600)</li>
<li>Click START</li>
</ol>

<p>The tool supports up to eight simultaneous serial port connections — useful for programming assembly lines where multiple boards are flashed in parallel.</p>

<h2>Method 3: Web Serial (Browser-Based Flashing)</h2>
<p>Tools built on the Web Serial API allow flashing directly from a web browser on Chrome or Edge without installing any software. Navigate to <strong>esp.huhn.me</strong> or a similar tool, connect your ESP32 via USB, and select the merged .bin file. The browser handles all communication through the Web Serial API.</p>

<p>This method is ideal for: sharing pre-built firmware with end users who should not need to install development tools; flashing firmware for IoT projects where the end user configures the device via a browser after flashing; and development environments where installing desktop software is restricted.</p>

<h2>Recovery: Unbricking an ESP32</h2>
<p>An ESP32 that does not boot (crash loop, blank serial output, or completely silent) is almost never truly bricked. The ROM bootloader is stored in the chip's internal ROM, which cannot be overwritten — it is always available to accept a new firmware download.</p>

<p>Recovery procedure:</p>
<ol>
<li>Put the board in download mode: hold BOOT, press EN, release EN, release BOOT</li>
<li>Verify connection: <code>esptool.py --port COM3 flash_id</code> — you should see chip information</li>
<li>Erase all flash: <code>esptool.py --port COM3 erase_flash</code></li>
<li>Reflash firmware: <code>esptool.py --port COM3 write_flash 0x1000 bootloader.bin 0x8000 partitions.bin 0x10000 firmware.bin</code></li>
</ol>

<p>If step 2 fails ("Failed to connect"), the board is not entering download mode. Check: GPIO 0 is grounded (BOOT button), EN is pulsing (RST button), the USB cable has data lines, and the driver is installed. An oscilloscope on the TX pin can confirm whether the ROM bootloader is outputting any serial data at all.</p>

<h2>Flash Read-Back (Backup)</h2>
<p>You can read the existing firmware from an ESP32 flash chip before overwriting it — useful for creating backups or extracting firmware from a working device:</p>

<pre><code>esptool.py --port COM3 read_flash 0x0 0x400000 flash_backup.bin</code></pre>

<p>This reads the full 4 MB of flash (0x400000 bytes) into flash_backup.bin. The resulting file is a raw image of the flash at the time of reading. You can restore it with <code>write_flash 0x0 flash_backup.bin</code> to return the device to exactly the state it was in when backed up. Note: if Flash Encryption is enabled on the device, the read-back data is encrypted and cannot be easily interpreted or transferred to another device.</p>
HTML,
],

/* ============================================================ */
[
'slug'         => 'updating-esp32-firmware',
'title'        => 'Updating ESP32 Firmware: OTA Updates, Version Control, and Rollback',
'meta_desc'    => 'How to safely update ESP32 firmware using OTA updates, HTTPS secure delivery, dual-partition rollback, ElegantOTA, and version tracking for deployed IoT devices.',
'read_time'    => '16 min read',
'phase'        => 'Phase 2: Setup & Development',
'faqs'         => [
  ['question'=>'What is OTA and why is it important for IoT devices?','answer'=>'OTA (Over-The-Air) update is the ability to deliver new firmware to a deployed device without physical access. For IoT devices installed in hard-to-reach locations — weather stations on rooftops, soil sensors in fields, smart switches inside walls — OTA is the only practical way to push bug fixes, security patches, and new features. Without OTA, every update requires physically connecting a USB cable to each device.'],
  ['question'=>'How does the dual-partition OTA scheme work?','answer'=>'The ESP32 divides flash into two equal-sized application partitions (OTA_0 and OTA_1) and a small OTA data partition that tracks which one is currently active. During an OTA update, the new firmware is written to the inactive partition. Only after the new firmware is verified does the OTA data partition update to point to the new one. On next reboot, the new firmware runs. If it fails to boot successfully within the rollback timeout, the device automatically reverts to the previous partition.'],
  ['question'=>'Is OTA update secure?','answer'=>'ArduinoOTA (the basic library) sends firmware without encryption or authentication — anyone on the same network could push a rogue firmware. For production security, use: HTTPS for firmware delivery (esp_https_ota in IDF), firmware signing verification (Secure Boot in conjunction with Signed OTA), a password on ArduinoOTA.setPassword(), or a custom HMAC-signed update protocol. Minimum viable security for hobbyist projects: ArduinoOTA with password + WPA2 network.'],
  ['question'=>'How much flash do I need for OTA updates?','answer'=>'The OTA partition scheme requires two equal app partitions. On a 4 MB flash device, each partition is typically 1.9 MB (default) or up to 1.4 MB (with a larger SPIFFS partition). Your compiled firmware must fit in one partition. If your sketch exceeds 1.9 MB when compiled, switch to a partition scheme with larger app partitions or reduce code size.'],
  ['question'=>'Can I do OTA update while the ESP32 is performing other tasks?','answer'=>'Yes. ArduinoOTA.handle() runs in the main loop alongside your application code. The OTA process runs as a background operation — your sensors continue reading, MQTT messages are processed, and actuators respond while firmware is being received. The only interruption is the final reboot after the update completes. For time-critical applications, you can postpone the reboot to a maintenance window.'],
  ['question'=>'What happens if the internet connection drops during an OTA update?','answer'=>'If the connection drops before the update is complete, the partial firmware in the inactive partition is simply ignored on reboot — the OTA data partition still points to the old (working) firmware. The device recovers automatically. Only when a complete, CRC-verified firmware is written does the OTA data partition switch to the new partition. Partial updates cannot brick the device.'],
  ['question'=>'How do I know what firmware version is running on a deployed device?','answer'=>'Define a version constant in your firmware and report it over MQTT, HTTP, or Serial: #define FW_VERSION "1.2.3". On boot, publish a heartbeat message: {"device":"esp32-sensor-01","version":"1.2.3","uptime":0}. Your backend can then track which version each device is running and trigger OTA updates for devices running outdated firmware.'],
  ['question'=>'What is ElegantOTA and when should I use it?','answer'=>'ElegantOTA is an Arduino library that adds a polished web-based firmware update page to your ESP32. Navigate to the device\'s IP address in any browser, select a .bin file, and upload. No IDE needed. It is ideal for end-user deployments where the person updating the firmware is not a developer, or for firmware updates from a mobile device.'],
  ['question'=>'Can I schedule OTA updates to happen at a specific time?','answer'=>'Yes. Your firmware can check for updates periodically and apply them during a maintenance window. Store the last-check timestamp in RTC memory or NVS, check an update server URL every hour, and if a new version is available, apply it immediately or queue it for a 3 AM update window. The esp_https_ota function handles the download and write; your application logic controls when to call it.'],
  ['question'=>'How do I test OTA before deploying to production devices?','answer'=>'Test OTA on a development board before deploying: (1) Flash firmware v1.0 that includes OTA support. (2) Trigger an OTA update with v1.1. (3) Verify v1.1 runs correctly. (4) Test the rollback path: flash a deliberately broken v1.2 that never calls esp_ota_mark_app_valid() — the device should revert to v1.1 after the watchdog timeout. (5) Test network failure mid-update by pulling the cable during upload — device should recover on reboot.'],
],
'related' => [
  ['title'=>'Flashing ESP32 Firmware','slug'=>'flashing-esp32-firmware'],
  ['title'=>'Uploading Code to ESP32','slug'=>'uploading-code-to-esp32'],
  ['title'=>'ESP32 Memory Architecture','slug'=>'esp32-memory-architecture'],
  ['title'=>'ESP32 Power Consumption Guide','slug'=>'esp32-power-consumption'],
],
'body_html' => <<<'HTML'
<h2>Why Firmware Updates Matter</h2>
<p>Every firmware has bugs. Every project evolves. Every security vulnerability eventually needs a patch. For an ESP32 sitting on a desk connected by USB cable, firmware updates are trivial — click Upload. For an ESP32 installed in a weather-proof enclosure on a rooftop, inside a wall, at a remote agricultural site, or distributed across hundreds of customer devices, physically connecting a USB cable for each update is impractical or impossible.</p>

<p>Firmware update capability — OTA (Over-The-Air) updates — should be designed into every ESP32 project that will leave your desk. This guide covers how ESP32 OTA works, the standard ArduinoOTA library for development use, the ElegantOTA web interface for end-user updates, and the more robust esp_https_ota approach for production firmware with rollback protection.</p>

<h2>Understanding the Dual-Partition OTA Architecture</h2>
<p>The ESP32's OTA system depends on having two separate application partitions in flash. The standard OTA partition scheme on a 4 MB device allocates:</p>

<div class="table-wrap">
<table class="wiring-table">
<thead><tr><th>Name</th><th>Type</th><th>Offset</th><th>Size</th></tr></thead>
<tbody>
<tr><td>nvs</td><td>data/nvs</td><td>0x9000</td><td>20 KB</td></tr>
<tr><td>otadata</td><td>data/ota</td><td>0xe000</td><td>8 KB</td></tr>
<tr><td>app0 (OTA_0)</td><td>app/ota_0</td><td>0x10000</td><td>1.9 MB</td></tr>
<tr><td>app1 (OTA_1)</td><td>app/ota_1</td><td>0x1F0000</td><td>1.9 MB</td></tr>
<tr><td>spiffs</td><td>data/spiffs</td><td>0x3D0000</td><td>192 KB</td></tr>
</tbody>
</table>
</div>

<p>The otadata partition is 8 KB and contains a small record indicating which app partition (app0 or app1) is currently active and whether it has been verified. During OTA: the currently running firmware writes incoming bytes to the inactive partition; when the download completes and the CRC verifies correctly, it updates the otadata to mark the new partition as boot target; the device reboots; the new firmware runs and must call <code>esp_ota_mark_app_valid_cancel_rollback()</code> to confirm it is working — if it does not (because it crashed), the watchdog timer eventually triggers and the bootloader reverts to the previous partition.</p>

<h2>Method 1: ArduinoOTA — Development Use</h2>
<p>ArduinoOTA is the simplest OTA implementation, included with the ESP32 Arduino core. After the initial USB flash, subsequent updates come from the Arduino IDE over Wi-Fi. Include OTA support in your sketch:</p>

<pre><code>#include &lt;WiFi.h&gt;
#include &lt;ArduinoOTA.h&gt;

const char* SSID = "YourSSID";
const char* PASS = "YourPassword";
const char* OTA_PASS = "your-ota-password"; // use a strong password

void setup() {
  Serial.begin(115200);

  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.printf("\nConnected: %s\n", WiFi.localIP().toString().c_str());

  ArduinoOTA.setHostname("esp32-sensor-01"); // identifies board in IDE port list
  ArduinoOTA.setPassword(OTA_PASS);

  ArduinoOTA.onStart([]() {
    String type = ArduinoOTA.getCommand() == U_FLASH ? "sketch" : "filesystem";
    Serial.println("OTA start: updating " + type);
  });
  ArduinoOTA.onEnd([]()   { Serial.println("\nOTA complete. Rebooting..."); });
  ArduinoOTA.onProgress([](unsigned int done, unsigned int total) {
    Serial.printf("Progress: %u%%\r", done * 100 / total);
  });
  ArduinoOTA.onError([](ota_error_t err) {
    Serial.printf("OTA Error[%u]: ", err);
    if      (err == OTA_AUTH_ERROR)    Serial.println("Auth Failed");
    else if (err == OTA_BEGIN_ERROR)   Serial.println("Begin Failed");
    else if (err == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (err == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (err == OTA_END_ERROR)     Serial.println("End Failed");
  });

  ArduinoOTA.begin();
  Serial.println("OTA ready");
}

void loop() {
  ArduinoOTA.handle(); // must call every loop iteration
  // ... your application code ...
}</code></pre>

<p>After uploading this via USB, the board appears under Tools → Port in Arduino IDE as a network device (e.g., "esp32-sensor-01 at 192.168.1.x"). Select it and upload subsequent sketches wirelessly. Ensure every future sketch also includes <code>ArduinoOTA.handle()</code> in loop() — without it, the next OTA will fail and you must revert to USB.</p>

<h2>Method 2: ElegantOTA — Browser-Based Updates</h2>
<p>ElegantOTA adds a web page at <code>/update</code> on your ESP32's IP address. Any browser on the same network can open it, select a .bin file, and upload. Install via the Arduino Library Manager: search "ElegantOTA" by Ayush Sharma.</p>

<pre><code>#include &lt;WiFi.h&gt;
#include &lt;WebServer.h&gt;
#include &lt;ElegantOTA.h&gt;

WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin("SSID", "Password");
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("IP: " + WiFi.localIP().toString());

  server.on("/", []() {
    server.send(200, "text/plain", "ESP32 Sensor Node v1.0");
  });

  ElegantOTA.begin(&server, "admin", "strongpassword");
  server.begin();
}

void loop() {
  server.handleClient();
  ElegantOTA.loop();
}</code></pre>

<p>Open <code>http://192.168.1.x/update</code> in any browser. A clean upload page accepts a .bin file. This is the recommended approach for end-user firmware updates — your users do not need Arduino IDE, PlatformIO, or any developer tools.</p>

<h2>Method 3: esp_https_ota — Production-Grade OTA</h2>
<p>For production firmware, OTA updates should come from your own server over HTTPS with SSL certificate validation. The ESP-IDF <code>esp_https_ota</code> component handles this:</p>

<pre><code>#include "esp_https_ota.h"
#include "esp_ota_ops.h"

#define FIRMWARE_URL "https://updates.yourserver.com/firmware/esp32-v1.2.0.bin"

// Your server's root CA certificate (embed as a C string)
extern const uint8_t server_cert_pem_start[] asm("_binary_server_cert_pem_start");
extern const uint8_t server_cert_pem_end[]   asm("_binary_server_cert_pem_end");

void perform_ota_update(void) {
  esp_http_client_config_t config = {
    .url            = FIRMWARE_URL,
    .cert_pem       = (char*)server_cert_pem_start,
    .timeout_ms     = 10000,
    .keep_alive_enable = true,
  };

  esp_https_ota_config_t ota_config = { .http_config = &config };
  esp_err_t ret = esp_https_ota(&ota_config);

  if (ret == ESP_OK) {
    ESP_LOGI("OTA", "OTA complete — rebooting");
    esp_restart();
  } else {
    ESP_LOGE("OTA", "OTA failed: %s", esp_err_to_name(ret));
  }
}</code></pre>

<p>The certificate validation ensures only your server can deliver firmware — a compromised network cannot inject rogue updates. Combined with Secure Boot and Signed OTA, this creates a trust chain from the chip's ROM all the way to your build server.</p>

<h2>Implementing Rollback Protection</h2>
<p>Automatic rollback prevents a bad OTA update from permanently bricking a device. After a firmware update and reboot, the new firmware has a window (defined by the watchdog timeout) to call <code>esp_ota_mark_app_valid_cancel_rollback()</code>. If it does not — because it crashed, hung, or failed to connect — the bootloader reverts to the previous firmware on the next reset.</p>

<pre><code>#include "esp_ota_ops.h"

void setup() {
  // ... initialise everything ...

  // Connect to Wi-Fi
  WiFi.begin(SSID, PASS);
  if (WiFi.waitForConnectResult(10000) == WL_CONNECTED) {
    // Everything critical works — mark this firmware as valid
    esp_ota_mark_app_valid_cancel_rollback();
    Serial.println("Firmware validated — rollback cancelled");
  } else {
    // Failed — do NOT mark valid; rollback will occur on next reset
    Serial.println("Wi-Fi failed — NOT marking firmware valid");
    delay(5000);
    ESP.restart();  // trigger rollback to previous firmware
  }
}</code></pre>

<h2>Tracking Firmware Versions</h2>
<p>Every deployed firmware should identify itself with a version string. Define it at compile time and report it on boot and in any status messages:</p>

<pre><code>#define FW_VERSION   "2.1.4"
#define FW_BUILD     __DATE__ " " __TIME__

void setup() {
  Serial.printf("Firmware: v%s (built %s)\n", FW_VERSION, FW_BUILD);

  // Report version via MQTT
  char payload[128];
  snprintf(payload, sizeof(payload),
    "{\"version\":\"%s\",\"build\":\"%s\",\"ip\":\"%s\"}",
    FW_VERSION, FW_BUILD, WiFi.localIP().toString().c_str());
  mqttClient.publish("devices/esp32-01/status", payload, true); // retained
}</code></pre>

<p>Your backend can subscribe to the status topic and maintain a registry of device-version pairs. When a new firmware is released, query the registry to find all devices still on older versions and trigger OTA updates programmatically — scaling from one device to thousands with no manual intervention.</p>
HTML,
],

]; // end return
