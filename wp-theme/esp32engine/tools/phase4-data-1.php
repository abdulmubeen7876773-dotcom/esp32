<?php
/* Phase 4: ESP32 Connectivity & Protocols — Guides 1–5
   wifi-basics-esp32, esp32-wifi-modes, http-client-esp32,
   esp32-web-server, mqtt-esp32
*/
return [

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'wifi-basics-esp32',
'title'     => 'Wi-Fi Basics on ESP32 — Connecting to a Network',
'meta_desc' => 'Learn how to connect your ESP32 to a Wi-Fi network using Arduino IDE. Covers SSID credentials, connection states, IP address retrieval, and reconnect logic.',
'read_time' => '12 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['esp32-wifi-modes','http-client-esp32','esp32-web-server','mqtt-esp32'],
'faqs'      => [
  ['q'=>'What Wi-Fi standards does ESP32 support?','a'=>'ESP32 supports 802.11 b/g/n at 2.4 GHz. It does not support 5 GHz networks. Maximum theoretical throughput is 150 Mbps but real-world speeds are closer to 20–30 Mbps for TCP traffic.'],
  ['q'=>'How do I store Wi-Fi credentials safely on ESP32?','a'=>'Use the Preferences library (NVS flash storage) to store SSID and password at runtime rather than hard-coding them. This lets you update credentials without reflashing and keeps them out of version control.'],
  ['q'=>'Why does ESP32 say WL_IDLE_STATUS then disconnect?','a'=>'This usually means the SSID is not found or the password is wrong. Double-check both, ensure the router broadcasts 2.4 GHz, and confirm the ESP32 is within range.'],
  ['q'=>'Can I connect ESP32 to a hidden SSID?','a'=>'Yes. Use WiFi.begin(ssid, password, channel, bssid, connect) with the exact BSSID (MAC address) of the access point, or call WiFi.scanNetworks(false, true) to include hidden networks in the scan.'],
  ['q'=>'What is the difference between WiFi.begin() and WiFi.reconnect()?','a'=>'WiFi.begin() starts a new connection attempt with the provided credentials. WiFi.reconnect() retries the last used credentials — useful in a reconnect loop without storing the password in a local variable again.'],
  ['q'=>'How long does ESP32 Wi-Fi connection take?','a'=>'Initial connection to a known network typically takes 1–3 seconds. If the router uses DHCP it may add another 500 ms for IP assignment. Static IP assignment skips this delay.'],
  ['q'=>'Does connecting to Wi-Fi affect ESP32 ADC readings?','a'=>'Yes. Wi-Fi and ADC2 share the RF subsystem. ADC2 pins (GPIO0, 2, 4, 12–15, 25–27) are unusable when Wi-Fi is active. Use ADC1 pins (GPIO32–39) for analog readings when Wi-Fi is on.'],
  ['q'=>'How do I set a static IP on ESP32?','a'=>'Call WiFi.config(IPAddress ip, IPAddress gateway, IPAddress subnet) before WiFi.begin(). For example: WiFi.config(IPAddress(192,168,1,100), IPAddress(192,168,1,1), IPAddress(255,255,255,0)).'],
  ['q'=>'Why does ESP32 Wi-Fi drop after a few minutes?','a'=>'Router power-saving or ARP timeout can disconnect idle clients. Call WiFi.setSleep(false) to disable ESP32 modem sleep, and implement a watchdog loop that calls WiFi.reconnect() when WiFi.status() != WL_CONNECTED.'],
  ['q'=>'Can multiple ESP32 boards connect to the same network?','a'=>'Yes. Each gets a unique IP and MAC. You can run up to 10 stations simultaneously in a typical home router. For larger deployments use a business-grade AP that supports more associations.'],
],
'body_html' => <<<'HTML'
<h2>Introduction to Wi-Fi on ESP32</h2>
<p>The ESP32's built-in Wi-Fi radio is one of its most powerful features. Unlike the Arduino Uno, which needs an external shield to reach the internet, the ESP32 connects natively to any 2.4 GHz 802.11 b/g/n network. This guide walks you through the complete connection sequence — from scanning for networks to reading your assigned IP address and handling dropped connections gracefully.</p>

<h2>Required Library</h2>
<p>The <code>WiFi.h</code> library is part of the official <strong>arduino-esp32</strong> board package and needs no separate installation. Add it to your sketch with a single include:</p>
<div class="code-block"><div class="code-bar"><span>includes</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;</pre></div>

<h2>Setting Your Credentials</h2>
<p>Hard-coding credentials is acceptable for personal experiments. For anything shared or version-controlled, use the <code>Preferences</code> library instead (covered later). For now:</p>
<div class="code-block"><div class="code-bar"><span>credentials.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>const char* ssid     = "YourNetworkName";   // case-sensitive
const char* password = "YourPassword";</pre></div>

<h2>The Minimal Connection Sketch</h2>
<div class="code-block"><div class="code-bar"><span>wifi_connect.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);          // station mode (client)
  WiFi.begin(ssid, password);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal (RSSI): ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
}

void loop() {
  // your application code here
}</pre></div>

<h2>Understanding WiFi.status()</h2>
<p>The <code>WiFi.status()</code> function returns one of these constants:</p>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
<thead><tr style="background:var(--surface-2)"><th style="padding:0.5rem;text-align:left">Constant</th><th style="padding:0.5rem;text-align:left">Value</th><th style="padding:0.5rem;text-align:left">Meaning</th></tr></thead>
<tbody>
<tr><td style="padding:0.5rem"><code>WL_CONNECTED</code></td><td style="padding:0.5rem">3</td><td style="padding:0.5rem">Successfully connected with IP assigned</td></tr>
<tr><td style="padding:0.5rem"><code>WL_NO_SSID_AVAIL</code></td><td style="padding:0.5rem">1</td><td style="padding:0.5rem">SSID not found in range</td></tr>
<tr><td style="padding:0.5rem"><code>WL_CONNECT_FAILED</code></td><td style="padding:0.5rem">4</td><td style="padding:0.5rem">Wrong password or authentication failed</td></tr>
<tr><td style="padding:0.5rem"><code>WL_IDLE_STATUS</code></td><td style="padding:0.5rem">0</td><td style="padding:0.5rem">Wi-Fi hardware idle or switching modes</td></tr>
<tr><td style="padding:0.5rem"><code>WL_DISCONNECTED</code></td><td style="padding:0.5rem">6</td><td style="padding:0.5rem">Not connected, but credentials are stored</td></tr>
</tbody></table>

<h2>Setting a Static IP Address</h2>
<p>DHCP adds a small delay and the IP can change between reboots. For servers and sensors that other devices need to find reliably, assign a static IP:</p>
<div class="code-block"><div class="code-bar"><span>static_ip.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

IPAddress local_IP(192, 168, 1, 120);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);    // optional

void setup() {
  Serial.begin(115200);

  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS)) {
    Serial.println("Static IP configuration failed");
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected with static IP: " + WiFi.localIP().toString());
}</pre></div>

<h2>Reconnection Watchdog</h2>
<p>Networks drop. Routers reboot. Implement a non-blocking reconnect loop so your device recovers automatically:</p>
<div class="code-block"><div class="code-bar"><span>wifi_watchdog.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

unsigned long lastReconnectAttempt = 0;
const unsigned long RECONNECT_INTERVAL = 10000; // 10 s

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  unsigned long t = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t &lt; 15000) {
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nFailed — will retry");
  }
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt &gt;= RECONNECT_INTERVAL) {
      lastReconnectAttempt = now;
      Serial.println("Wi-Fi lost — reconnecting...");
      WiFi.disconnect();
      connectWiFi();
    }
  }
  // application code here
}</pre></div>

<h2>Scanning for Networks</h2>
<p>Use <code>WiFi.scanNetworks()</code> to discover nearby SSIDs — useful for diagnostics or let users choose a network at runtime:</p>
<div class="code-block"><div class="code-bar"><span>wifi_scan.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  int n = WiFi.scanNetworks();
  if (n == 0) {
    Serial.println("No networks found");
  } else {
    Serial.printf("Found %d networks:\n", n);
    for (int i = 0; i &lt; n; i++) {
      Serial.printf("  %2d: %-30s RSSI:%4d CH:%2d %s\n",
        i + 1,
        WiFi.SSID(i).c_str(),
        WiFi.RSSI(i),
        WiFi.channel(i),
        WiFi.encryptionType(i) == WIFI_AUTH_OPEN ? "OPEN" : "SECURED");
    }
  }
  WiFi.scanDelete();
}

void loop() {}</pre></div>

<h2>Power and ADC Considerations</h2>
<p>When Wi-Fi is active the ESP32 radio draws up to 240 mA peak. Two side effects matter for hardware design:</p>
<ul>
<li><strong>ADC2 is unusable.</strong> Pins GPIO0, 2, 4, 12–15, 25–27 are shared with the RF subsystem. Use ADC1 (GPIO32–39) for any analog reads while Wi-Fi is on.</li>
<li><strong>Voltage rail noise.</strong> Add a 100 µF electrolytic and 100 nF ceramic capacitor between 3.3V and GND close to the ESP32 module to filter RF-induced supply spikes.</li>
</ul>

<h2>Disabling Modem Sleep</h2>
<p>By default the ESP32 enters modem sleep between beacons to save power. This can cause brief disconnections. For always-on applications:</p>
<div class="code-block"><div class="code-bar"><span>disable_sleep.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>WiFi.setSleep(false);   // call after WiFi.begin(), before connecting</pre></div>

<h2>Reading Network Information</h2>
<div class="code-block"><div class="code-bar"><span>network_info.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>Serial.println("=== Network Info ===");
Serial.println("SSID:    " + WiFi.SSID());
Serial.println("IP:      " + WiFi.localIP().toString());
Serial.println("Gateway: " + WiFi.gatewayIP().toString());
Serial.println("Subnet:  " + WiFi.subnetMask().toString());
Serial.println("DNS:     " + WiFi.dnsIP().toString());
Serial.println("MAC:     " + WiFi.macAddress());
Serial.printf( "RSSI:    %d dBm\n", WiFi.RSSI());</pre></div>

<h2>Next Steps</h2>
<p>Now that your ESP32 is on the network, explore what you can do with it:</p>
<ul>
<li><a href="/guides/esp32-wifi-modes/">ESP32 Wi-Fi Modes</a> — Station, AP, and AP+STA explained</li>
<li><a href="/guides/http-client-esp32/">HTTP Client</a> — GET and POST requests to REST APIs</li>
<li><a href="/guides/esp32-web-server/">Web Server</a> — Serve a control page from the ESP32 itself</li>
<li><a href="/guides/mqtt-esp32/">MQTT</a> — Publish sensor data to a broker</li>
</ul>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'esp32-wifi-modes',
'title'     => 'ESP32 Wi-Fi Modes — Station, AP, and AP+STA',
'meta_desc' => 'Understand ESP32 Wi-Fi operating modes: Station (client), Access Point (hotspot), and the dual AP+STA mode. Includes code for each mode with configuration tips.',
'read_time' => '10 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','esp32-web-server','http-client-esp32','ota-updates-esp32'],
'faqs'      => [
  ['q'=>'What is the difference between WIFI_STA and WIFI_AP mode?','a'=>'WIFI_STA (Station) makes the ESP32 a client that joins an existing network. WIFI_AP (Access Point) makes the ESP32 itself a hotspot that other devices can connect to. WIFI_AP_STA enables both simultaneously.'],
  ['q'=>'How many clients can connect to an ESP32 Access Point?','a'=>'The ESP32 AP supports a maximum of 10 simultaneous clients (stations) by default. You can adjust this with WiFi.softAP(ssid, password, channel, hidden, max_connection) where max_connection is 1–10.'],
  ['q'=>'Can ESP32 AP and STA run on different channels?','a'=>'No. In AP+STA mode both interfaces must use the same channel. The STA channel is determined by the router it connects to, so the AP will also use that channel.'],
  ['q'=>'How do I hide the ESP32 AP SSID?','a'=>'Pass true as the fourth argument to softAP(): WiFi.softAP("MyNetwork", "password", 1, true). The network will not appear in scan results but devices that know the SSID can still connect.'],
  ['q'=>'What IP address do clients get from an ESP32 AP?','a'=>'By default the ESP32 AP uses DHCP and assigns addresses in the 192.168.4.x range. The ESP32 itself is at 192.168.4.1. You can change this with WiFi.softAPConfig(local_ip, gateway, subnet) before softAP().'],
  ['q'=>'Does the ESP32 AP mode support WPA2 security?','a'=>'Yes. WiFi.softAP(ssid, password) enables WPA2-PSK (AES) by default. Leave password empty ("") or omit it for an open network.'],
  ['q'=>'Can I run a web server in both AP and STA mode simultaneously?','a'=>'Yes. In WIFI_AP_STA mode one AsyncWebServer (or plain WebServer) instance serves requests on both interfaces using the respective IP addresses.'],
  ['q'=>'How do I get the connected client list in AP mode?','a'=>'Call WiFi.softAPgetStationNum() for the count. For individual client MAC addresses use the esp_wifi_ap_get_sta_list() function from the esp_wifi.h SDK header.'],
  ['q'=>'Why does my ESP32 AP disconnect clients after a few seconds?','a'=>'Check that your power supply can handle the load. Also ensure WiFi.softAP() is called in setup() not loop(). Calling softAP() repeatedly re-initialises the AP and kicks all clients.'],
  ['q'=>'What is the range of an ESP32 Wi-Fi AP?','a'=>'Typical indoor range is 20–50 metres. Using a whip antenna module instead of the PCB trace antenna, and keeping the line of sight clear, can extend this to 100 m outdoors.'],
],
'body_html' => <<<'HTML'
<h2>The Three Wi-Fi Modes</h2>
<p>Every ESP32 Wi-Fi session begins by choosing one of three operating modes. The mode tells the radio whether it should act as a client joining someone else's network, a host creating its own network, or both at once.</p>

<table style="width:100%;border-collapse:collapse;margin:1rem 0">
<thead><tr style="background:var(--surface-2)"><th style="padding:0.5rem;text-align:left">Mode Constant</th><th style="padding:0.5rem;text-align:left">Role</th><th style="padding:0.5rem;text-align:left">Typical Use Case</th></tr></thead>
<tbody>
<tr><td style="padding:0.5rem"><code>WIFI_STA</code></td><td style="padding:0.5rem">Station (client)</td><td style="padding:0.5rem">Joining your home/office network</td></tr>
<tr><td style="padding:0.5rem"><code>WIFI_AP</code></td><td style="padding:0.5rem">Access Point (hotspot)</td><td style="padding:0.5rem">Provisioning, local control without internet</td></tr>
<tr><td style="padding:0.5rem"><code>WIFI_AP_STA</code></td><td style="padding:0.5rem">Both simultaneously</td><td style="padding:0.5rem">OTA updates, bridging, captive portal</td></tr>
<tr><td style="padding:0.5rem"><code>WIFI_OFF</code></td><td style="padding:0.5rem">Radio disabled</td><td style="padding:0.5rem">Ultra-low power deep sleep</td></tr>
</tbody></table>

<h2>Station Mode (WIFI_STA)</h2>
<p>Station mode is the most common. The ESP32 connects to an existing router and receives an IP address via DHCP. This is what the <a href="/guides/wifi-basics-esp32/">Wi-Fi Basics guide</a> demonstrates. The key call is <code>WiFi.mode(WIFI_STA)</code> followed by <code>WiFi.begin(ssid, password)</code>.</p>

<h2>Access Point Mode (WIFI_AP)</h2>
<p>In AP mode the ESP32 becomes a Wi-Fi hotspot. Phones, laptops, or other ESP32 boards can connect directly to it — no external router required. This is ideal for local control panels, field devices with no existing infrastructure, and the Wi-Fi provisioning workflow.</p>
<div class="code-block"><div class="code-bar"><span>ap_mode.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

const char* ap_ssid     = "ESP32-Config";
const char* ap_password = "12345678";   // min 8 chars, or "" for open

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_AP);
  bool ok = WiFi.softAP(ap_ssid, ap_password);
  if (ok) {
    Serial.println("AP started");
    Serial.print("AP IP: ");
    Serial.println(WiFi.softAPIP());   // default: 192.168.4.1
  } else {
    Serial.println("AP failed — check credentials");
  }
}

void loop() {
  Serial.printf("Clients connected: %d\n", WiFi.softAPgetStationNum());
  delay(5000);
}</pre></div>

<h2>Customising the AP Address</h2>
<div class="code-block"><div class="code-bar"><span>ap_custom_ip.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>IPAddress ap_ip(10, 0, 0, 1);
IPAddress ap_gw(10, 0, 0, 1);
IPAddress ap_sub(255, 255, 255, 0);

WiFi.mode(WIFI_AP);
WiFi.softAPConfig(ap_ip, ap_gw, ap_sub);
WiFi.softAP("MyESP32", "password123");
Serial.println("AP IP: " + WiFi.softAPIP().toString());   // 10.0.0.1</pre></div>

<h2>AP + STA Dual Mode (WIFI_AP_STA)</h2>
<p>Dual mode lets the ESP32 stay connected to your home router as a client while simultaneously acting as its own hotspot. This is essential for OTA updates (download from the internet, serve the hotspot UI locally) and for bridging sensors that can only reach the ESP32 AP with a cloud backend reached via the STA interface.</p>
<div class="code-block"><div class="code-bar"><span>ap_sta_mode.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;

const char* sta_ssid = "HomeRouter";
const char* sta_pass = "routerPassword";
const char* ap_ssid  = "ESP32-Local";
const char* ap_pass  = "esp32pass";

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_AP_STA);

  // Start STA connection
  WiFi.begin(sta_ssid, sta_pass);

  // Start AP (runs immediately; STA connects in background)
  WiFi.softAP(ap_ssid, ap_pass);
  Serial.println("AP IP:  " + WiFi.softAPIP().toString());

  // Wait for STA to connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nSTA IP: " + WiFi.localIP().toString());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    delay(5000);
  }
}</pre></div>

<h2>Channel Constraint in Dual Mode</h2>
<p>A subtle but important limitation: in AP+STA mode both interfaces share the same radio and therefore must operate on the same Wi-Fi channel. The channel is set by the router the STA connects to. If your router uses channel 11, the ESP32 AP will also use channel 11 — you cannot override this.</p>

<h2>Wi-Fi Provisioning with AP Mode</h2>
<p>A common pattern for shipping consumer devices:</p>
<ol>
<li>Device boots, checks NVS flash for stored credentials</li>
<li>If no credentials found, starts AP mode ("DeviceName-Setup")</li>
<li>User connects phone to the AP, opens 192.168.4.1 in browser</li>
<li>Captive portal form collects SSID and password, stores to NVS</li>
<li>Device reboots, now connects to home router in STA mode</li>
</ol>

<h2>Turning Wi-Fi Off Completely</h2>
<p>For battery-powered sensors that send data periodically, turn off the radio between transmissions:</p>
<div class="code-block"><div class="code-bar"><span>wifi_off.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>WiFi.disconnect(true);    // disconnect and clear credentials
WiFi.mode(WIFI_OFF);      // power down the radio
esp_wifi_stop();          // full RF power cut (saves ~20 mA)</pre></div>
<p>Re-enable with <code>esp_wifi_start()</code> and <code>WiFi.begin(ssid, pass)</code> when you need to send the next reading.</p>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'http-client-esp32',
'title'     => 'ESP32 HTTP Client — GET and POST Requests',
'meta_desc' => 'Send HTTP GET and POST requests from ESP32 using the HTTPClient library. Includes JSON payloads, response parsing, HTTPS with certificate validation, and error handling.',
'read_time' => '14 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','mqtt-esp32','esp32-web-server','ota-updates-esp32'],
'faqs'      => [
  ['q'=>'Which library do I use for HTTP requests on ESP32?','a'=>'The built-in HTTPClient library (included with arduino-esp32) handles both HTTP and HTTPS. Include it with #include <HTTPClient.h>. No additional installation is needed.'],
  ['q'=>'How do I parse JSON responses on ESP32?','a'=>'Use the ArduinoJson library (install via Library Manager: search "ArduinoJson" by Benoit Blanchon). Deserialize the response string with deserializeJson(doc, payload) and access fields with doc["key"].as<type>().'],
  ['q'=>'Does ESP32 HTTPClient support HTTPS?','a'=>'Yes. Use WiFiClientSecure instead of WiFiClient. For full certificate validation call client.setCACert(root_ca_cert). For testing only you can call client.setInsecure() to skip validation (not safe for production).'],
  ['q'=>'What does HTTPClient return when the server is unreachable?','a'=>'http.GET() returns a negative error code. HTTPC_ERROR_CONNECTION_REFUSED is -1, HTTPC_ERROR_SEND_HEADER_FAILED is -2, HTTPC_ERROR_CONNECTION_LOST is -4. Always check for httpCode > 0 before reading the response.'],
  ['q'=>'How do I send form-encoded data with POST?','a'=>'Call http.addHeader("Content-Type", "application/x-www-form-urlencoded") then http.POST("key1=value1&key2=value2"). URL-encode special characters in the values.'],
  ['q'=>'Can I send binary data (images, firmware) with HTTPClient?','a'=>'Yes. Use http.POST(uint8_t* payload, size_t size) for binary payloads. Set Content-Type to application/octet-stream or the appropriate MIME type for your data.'],
  ['q'=>'Why does my ESP32 HTTPS request fail with certificate error?','a'=>'The root CA certificate for the server has likely changed or expired, or the ESP32 clock is not set (TLS requires a valid time). Call configTime() to sync NTP time before making HTTPS requests.'],
  ['q'=>'How do I set a timeout for HTTP requests on ESP32?','a'=>'Call http.setTimeout(milliseconds) before http.begin(). The default is 5000 ms (5 seconds). Set it to something like 10000 for slow APIs and 3000 for local network calls.'],
  ['q'=>'Can I add custom headers to ESP32 HTTP requests?','a'=>'Yes. Call http.addHeader("Header-Name", "value") as many times as needed before calling http.GET() or http.POST(). Common uses include Authorization, Accept, and User-Agent headers.'],
  ['q'=>'How do I stream a large HTTP response without running out of RAM?','a'=>'Use http.getStream() to get a Stream reference and read it in chunks: while (stream->available()) { uint8_t buf[128]; stream->readBytes(buf, sizeof(buf)); process(buf); }. This avoids loading the full response into a String.'],
],
'body_html' => <<<'HTML'
<h2>Why HTTP on ESP32?</h2>
<p>HTTP is the language of the web. With ESP32's built-in Wi-Fi and the <code>HTTPClient</code> library, your microcontroller can talk directly to REST APIs, IoT platforms, home automation hubs, and your own backend servers. This guide covers everything from a simple GET request to authenticated HTTPS POST with JSON.</p>

<h2>Prerequisites</h2>
<ul>
<li>ESP32 connected to Wi-Fi (<a href="/guides/wifi-basics-esp32/">Wi-Fi Basics guide</a>)</li>
<li><code>HTTPClient.h</code> — built into arduino-esp32, no install needed</li>
<li>Optional: <strong>ArduinoJson</strong> library for parsing responses</li>
</ul>

<h2>Simple HTTP GET Request</h2>
<div class="code-block"><div class="code-bar"><span>http_get.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;HTTPClient.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nConnected: " + WiFi.localIP().toString());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin("http://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.1&current_weather=true");
    http.setTimeout(10000);

    int httpCode = http.GET();

    if (httpCode > 0) {
      Serial.printf("HTTP %d\n", httpCode);
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        Serial.println(payload.substring(0, 200)); // first 200 chars
      }
    } else {
      Serial.printf("GET failed: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
  delay(30000);
}</pre></div>

<h2>Parsing a JSON Response with ArduinoJson</h2>
<div class="code-block"><div class="code-bar"><span>http_get_json.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;HTTPClient.h&gt;
#include &lt;ArduinoJson.h&gt;

// ... WiFi setup ...

void fetchWeather() {
  HTTPClient http;
  http.begin("http://api.open-meteo.com/v1/forecast"
             "?latitude=51.5&longitude=-0.1&current_weather=true");

  if (http.GET() == HTTP_CODE_OK) {
    String body = http.getString();

    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, body);

    if (!err) {
      float temp      = doc["current_weather"]["temperature"];
      int   windspeed = doc["current_weather"]["windspeed"];
      Serial.printf("Temp: %.1f°C  Wind: %d km/h\n", temp, windspeed);
    } else {
      Serial.println("JSON parse error: " + String(err.c_str()));
    }
  }
  http.end();
}</pre></div>

<h2>HTTP POST — JSON Body</h2>
<div class="code-block"><div class="code-bar"><span>http_post_json.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;HTTPClient.h&gt;
#include &lt;ArduinoJson.h&gt;

void postSensorData(float temperature, float humidity) {
  HTTPClient http;
  http.begin("https://your-api.example.com/sensors");
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer YOUR_API_TOKEN");

  JsonDocument doc;
  doc["device_id"]   = "esp32-living-room";
  doc["temperature"] = temperature;
  doc["humidity"]    = humidity;
  doc["timestamp"]   = millis();

  String body;
  serializeJson(doc, body);

  int httpCode = http.POST(body);
  Serial.printf("POST status: %d\n", httpCode);

  if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED) {
    Serial.println("Data sent: " + http.getString());
  }
  http.end();
}</pre></div>

<h2>HTTP POST — Form-Encoded Data</h2>
<div class="code-block"><div class="code-bar"><span>http_post_form.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>HTTPClient http;
http.begin("http://192.168.1.100/api/control");
http.addHeader("Content-Type", "application/x-www-form-urlencoded");

String payload = "relay=on&duration=5000&device=esp32";
int code = http.POST(payload);
Serial.printf("Response: %d — %s\n", code, http.getString().c_str());
http.end();</pre></div>

<h2>HTTPS with Certificate Validation</h2>
<p>For production code, always validate the server's TLS certificate. You need the root CA certificate of the server (download it from your browser's certificate inspector or use <code>openssl s_client -connect host:443 -showcerts</code>).</p>
<div class="code-block"><div class="code-bar"><span>https_secure.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;HTTPClient.h&gt;
#include &lt;WiFiClientSecure.h&gt;

// Root CA for your server (get from browser or openssl)
const char* root_ca = R"(
-----BEGIN CERTIFICATE-----
MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
...
-----END CERTIFICATE-----
)";

void setup() {
  // ... WiFi connect ...

  WiFiClientSecure client;
  client.setCACert(root_ca);         // validates server cert
  // client.setInsecure();           // TESTING ONLY — skip validation

  HTTPClient https;
  https.begin(client, "https://api.example.com/data");
  int code = https.GET();
  Serial.printf("HTTPS %d: %s\n", code, https.getString().c_str());
  https.end();
}</pre></div>

<h2>Syncing Time for HTTPS</h2>
<p>TLS handshakes require the ESP32 clock to be within a few minutes of real time. Sync via NTP before any HTTPS call:</p>
<div class="code-block"><div class="code-bar"><span>ntp_sync.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;time.h&gt;

void syncTime() {
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Syncing NTP");
  time_t now = time(nullptr);
  while (now &lt; 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println(" done");
}</pre></div>

<h2>Error Handling Reference</h2>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
<thead><tr style="background:var(--surface-2)"><th style="padding:0.5rem">Code</th><th style="padding:0.5rem">Constant</th><th style="padding:0.5rem">Meaning</th></tr></thead>
<tbody>
<tr><td style="padding:0.5rem">-1</td><td style="padding:0.5rem"><code>HTTPC_ERROR_CONNECTION_REFUSED</code></td><td style="padding:0.5rem">Server port closed or firewall blocked</td></tr>
<tr><td style="padding:0.5rem">-4</td><td style="padding:0.5rem"><code>HTTPC_ERROR_CONNECTION_LOST</code></td><td style="padding:0.5rem">TCP connection dropped mid-transfer</td></tr>
<tr><td style="padding:0.5rem">-11</td><td style="padding:0.5rem"><code>HTTPC_ERROR_READ_TIMEOUT</code></td><td style="padding:0.5rem">Server did not respond within timeout</td></tr>
<tr><td style="padding:0.5rem">401</td><td style="padding:0.5rem">HTTP_CODE_UNAUTHORIZED</td><td style="padding:0.5rem">Missing or wrong Authorization header</td></tr>
<tr><td style="padding:0.5rem">429</td><td style="padding:0.5rem">Too Many Requests</td><td style="padding:0.5rem">Rate limit — add exponential backoff</td></tr>
</tbody></table>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'esp32-web-server',
'title'     => 'ESP32 Web Server — Serve an HTML Control Page',
'meta_desc' => 'Build a local web server on ESP32 to control GPIO pins from a browser. Covers the WebServer library, route handlers, HTML forms, JSON API endpoints, and mDNS hostname setup.',
'read_time' => '16 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','esp32-wifi-modes','mqtt-esp32','ota-updates-esp32'],
'faqs'      => [
  ['q'=>'What library do I use to create a web server on ESP32?','a'=>'The built-in WebServer library (for synchronous use) is included with arduino-esp32. For better performance under multiple simultaneous clients, use the ESPAsyncWebServer library available through the Library Manager.'],
  ['q'=>'How do I access my ESP32 web server by name instead of IP?','a'=>'Use mDNS (Multicast DNS). Call MDNS.begin("esp32") and your device will be reachable at http://esp32.local/ from any device on the same network that supports mDNS (all modern operating systems do).'],
  ['q'=>'Can the ESP32 web server handle multiple clients at the same time?','a'=>'The basic WebServer library is synchronous — it handles one request at a time. ESPAsyncWebServer handles concurrent connections asynchronously. For most home-automation use cases the basic server is sufficient.'],
  ['q'=>'How do I serve CSS and JavaScript files from ESP32 flash?','a'=>'Store them in SPIFFS or LittleFS. Use the LittleFS library and ESP32 Sketch Data Upload tool to upload files from a /data folder in your sketch. Serve them with server.serveStatic("/style.css", LittleFS, "/style.css").'],
  ['q'=>'How do I receive form data submitted by a browser on ESP32?','a'=>'Use server.arg("fieldName") inside your route handler. For GET requests the field comes from the URL query string. For POST requests with application/x-www-form-urlencoded it comes from the body.'],
  ['q'=>'Can I use WebSockets with the ESP32 web server?','a'=>'Yes. The ESPAsyncWebServer library includes AsyncWebSocket support. Create an AsyncWebSocket object, attach it to the server, and push messages with ws.textAll("message") to broadcast to all clients.'],
  ['q'=>'How do I password-protect my ESP32 web server?','a'=>'Add a basic auth check in your route handler: if (!server.authenticate("admin", "password")) { server.requestAuthentication(); return; }. Use HTTPS for any real security since basic auth sends credentials in clear text.'],
  ['q'=>'Why does my ESP32 web server stop responding after a while?','a'=>'The most common cause is not calling server.handleClient() frequently enough in loop(). Also check for blocking code (long delays, blocking I/O) that prevents the server from processing incoming requests.'],
  ['q'=>'How large can the HTML page served from ESP32 be?','a'=>'The ESP32 has 520 KB of SRAM. Strings larger than a few KB should be stored in PROGMEM or served from LittleFS rather than held in RAM. For complex UIs, serve the HTML from flash and load data via AJAX/fetch calls.'],
  ['q'=>'Can I update the web page content without refreshing the browser?','a'=>'Yes. Add a /status JSON endpoint and use JavaScript fetch() in the browser to poll it every few seconds. Alternatively use WebSockets or Server-Sent Events for true real-time push updates.'],
],
'body_html' => <<<'HTML'
<h2>What You Will Build</h2>
<p>A local web page hosted on the ESP32 itself that lets you control an LED from any browser on your network. By the end of this guide you will have a working URL like <code>http://192.168.1.120/</code> that shows LED state, toggles it on/off, and returns live status as JSON.</p>

<h2>Hardware Setup</h2>
<ul>
<li>LED + 220 Ω resistor connected to GPIO2 (built-in LED on most DevKit boards)</li>
<li>ESP32 DevKit connected via USB</li>
</ul>

<h2>Minimal Web Server</h2>
<div class="code-block"><div class="code-bar"><span>web_server_basic.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;WebServer.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";
const int   LED_PIN  = 2;

WebServer server(80);
bool ledState = false;

String buildPage() {
  String html = "<!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;";
  html += "&lt;meta charset='utf-8'&gt;&lt;meta name='viewport' content='width=device-width,initial-scale=1'&gt;";
  html += "&lt;title&gt;ESP32 Control&lt;/title&gt;";
  html += "&lt;style&gt;body{font-family:sans-serif;max-width:480px;margin:2rem auto;padding:1rem}";
  html += ".btn{display:inline-block;padding:.6rem 1.4rem;border-radius:6px;color:#fff;text-decoration:none;font-size:1rem}";
  html += ".on{background:#16a34a}.off{background:#dc2626}&lt;/style&gt;&lt;/head&gt;&lt;body&gt;";
  html += "&lt;h1&gt;ESP32 Control Panel&lt;/h1&gt;";
  html += "&lt;p&gt;LED is &lt;strong&gt;" + String(ledState ? "ON" : "OFF") + "&lt;/strong&gt;&lt;/p&gt;";
  html += "&lt;a class='btn " + String(ledState ? "off" : "on") + "' href='/toggle'&gt;";
  html += (ledState ? "Turn Off" : "Turn On") + String("&lt;/a&gt;");
  html += "&lt;p style='margin-top:2rem;color:#666'&gt;IP: " + WiFi.localIP().toString() + "&lt;/p&gt;";
  html += "&lt;/body&gt;&lt;/html&gt;";
  return html;
}

void handleRoot() {
  server.send(200, "text/html", buildPage());
}

void handleToggle() {
  ledState = !ledState;
  digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  server.sendHeader("Location", "/");
  server.send(303);   // redirect back to home page
}

void handleStatus() {
  String json = "{\"led\":" + String(ledState ? "true" : "false") + ",";
  json += "\"uptime\":" + String(millis() / 1000) + "}";
  server.send(200, "application/json", json);
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nIP: " + WiFi.localIP().toString());

  server.on("/",        handleRoot);
  server.on("/toggle",  handleToggle);
  server.on("/status",  handleStatus);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}</pre></div>

<h2>Setting Up mDNS (Access by Name)</h2>
<p>Instead of remembering an IP address, configure mDNS so the device is reachable at a friendly hostname:</p>
<div class="code-block"><div class="code-bar"><span>mdns_setup.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;ESPmDNS.h&gt;

// In setup(), after WiFi connects:
if (MDNS.begin("esp32-control")) {
  MDNS.addService("http", "tcp", 80);
  Serial.println("mDNS: http://esp32-control.local/");
}</pre></div>
<p>Now any device on the same LAN can browse to <code>http://esp32-control.local/</code> without knowing the IP.</p>

<h2>Real-Time Updates with AJAX Polling</h2>
<p>Refresh sensor data without a full page reload by adding a small JavaScript fetch loop to your HTML:</p>
<div class="code-block"><div class="code-bar"><span>ajax_poll.html (inside the String)</span><button class="copy-btn" type="button">Copy</button></div>
<pre>&lt;div id="status"&gt;Loading…&lt;/div&gt;
&lt;script&gt;
setInterval(async () => {
  const r = await fetch('/status');
  const d = await r.json();
  document.getElementById('status').textContent =
    'LED: ' + (d.led ? 'ON' : 'OFF') + ' | Uptime: ' + d.uptime + 's';
}, 2000);
&lt;/script&gt;</pre></div>

<h2>Serving Multiple GPIO Pins</h2>
<div class="code-block"><div class="code-bar"><span>multi_gpio.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void handlePin() {
  if (server.hasArg("pin") && server.hasArg("state")) {
    int  pin   = server.arg("pin").toInt();
    bool state = server.arg("state") == "1";
    if (pin >= 0 && pin <= 39) {
      pinMode(pin, OUTPUT);
      digitalWrite(pin, state ? HIGH : LOW);
      server.send(200, "application/json", "{\"ok\":true}");
    } else {
      server.send(400, "application/json", "{\"error\":\"invalid pin\"}");
    }
  }
}
// Register: server.on("/pin", HTTP_GET, handlePin);
// Call: GET /pin?pin=4&state=1</pre></div>

<h2>Receiving POST Data from a Form</h2>
<div class="code-block"><div class="code-bar"><span>post_handler.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void handleForm() {
  if (server.method() == HTTP_POST) {
    String name  = server.arg("name");
    String value = server.arg("value");
    Serial.printf("Received: %s = %s\n", name.c_str(), value.c_str());
    server.send(200, "text/plain", "Saved: " + name + " = " + value);
  } else {
    server.send(405, "text/plain", "Method not allowed");
  }
}</pre></div>

<h2>Performance Tips</h2>
<ul>
<li><strong>Call <code>server.handleClient()</code> every loop iteration</strong> — never put long blocking code in <code>loop()</code> when a web server is running.</li>
<li><strong>Use <code>PROGMEM</code> for large HTML</strong> — store the page template in flash, not SRAM, with <code>const char html[] PROGMEM = "..."</code>.</li>
<li><strong>Compress static files</strong> — serve pre-gzipped CSS/JS and set the <code>Content-Encoding: gzip</code> header for up to 70% size reduction.</li>
<li><strong>For concurrent clients</strong> — switch to <code>ESPAsyncWebServer</code> which handles multiple connections without blocking.</li>
</ul>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'mqtt-esp32',
'title'     => 'MQTT on ESP32 — Publish Sensor Data to a Broker',
'meta_desc' => 'Use MQTT with ESP32 to publish sensor readings and subscribe to commands. Covers PubSubClient library, broker setup, QoS levels, retained messages, and last-will topics.',
'read_time' => '15 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','http-client-esp32','esp32-web-server','websockets-esp32'],
'faqs'      => [
  ['q'=>'What is MQTT and why use it with ESP32?','a'=>'MQTT (Message Queuing Telemetry Transport) is a lightweight publish-subscribe protocol designed for low-bandwidth, unreliable networks. It is ideal for IoT because a 50-byte sensor reading costs far less bandwidth than an equivalent HTTP request.'],
  ['q'=>'Which MQTT library works best for ESP32?','a'=>'PubSubClient by Nick O\'Leary is the most widely used library for Arduino/ESP32. Install it via Library Manager (search "PubSubClient"). For more advanced features like QoS 2 and MQTT 5 support, use the MQTT library by Joel Gaehwiler.'],
  ['q'=>'What is a retained MQTT message?','a'=>'A retained message is stored by the broker and immediately sent to any new subscriber when they first subscribe to that topic. This is useful for state topics — a new dashboard that subscribes to sensor/temperature gets the last known value right away.'],
  ['q'=>'What MQTT QoS level should I use on ESP32?','a'=>'QoS 0 (at most once, fire-and-forget) is fastest and uses least RAM — good for high-frequency sensor data where losing a reading is acceptable. QoS 1 (at least once) guarantees delivery but uses more RAM. QoS 2 is rarely needed on embedded devices.'],
  ['q'=>'What is an MQTT last will and testament (LWT)?','a'=>'An LWT is a message the broker sends automatically if the ESP32 disconnects unexpectedly (TCP timeout or power loss). Set it with client.setWill("device/status", "offline", true, 1) to let subscribers know the device went offline.'],
  ['q'=>'Can I use MQTT over TLS (MQTTS) on ESP32?','a'=>'Yes. Use WiFiClientSecure with the broker\'s root CA certificate, then pass the secure client to PubSubClient instead of a plain WiFiClient. Use port 8883 instead of 1883.'],
  ['q'=>'What free MQTT brokers can I use for testing?','a'=>'broker.hivemq.com and test.mosquitto.org are public test brokers with no authentication required. For production, use Mosquitto on a VPS, HiveMQ Cloud free tier, or AWS IoT Core.'],
  ['q'=>'How many topics can ESP32 subscribe to simultaneously?','a'=>'PubSubClient can subscribe to as many topics as memory allows, but there is a practical limit of 10–20 active subscriptions before performance degrades on the 520 KB heap. Use wildcard subscriptions (sensor/+/temperature) to reduce the count.'],
  ['q'=>'Why does my ESP32 MQTT connection keep dropping?','a'=>'Check three things: (1) the keepalive interval — call client.setKeepAlive(60) and ensure your broker keepalive matches; (2) the broker might have a maximum connection time; (3) implement a reconnect loop that re-subscribes after reconnecting, since subscriptions are lost on disconnect.'],
  ['q'=>'Can I publish JSON payloads with MQTT on ESP32?','a'=>'Yes. Serialize your data to a JSON string using ArduinoJson and publish it: char buf[200]; serializeJson(doc, buf); client.publish("sensor/data", buf). Many brokers and dashboards like Node-RED and Grafana accept JSON payloads natively.'],
],
'body_html' => <<<'HTML'
<h2>Why MQTT for ESP32?</h2>
<p>When a DHT22 reads 23.4°C, you have two options: send an HTTP POST (adds ~300 bytes of headers to your 8 bytes of data) or publish an MQTT message (8 bytes, no headers). For devices publishing every 5 seconds, that bandwidth difference compounds fast. MQTT also gives you a central broker that routes messages to any number of subscribers — dashboards, databases, automation rules — without the sensor needing to know they exist.</p>

<h2>Architecture Overview</h2>
<ul>
<li><strong>Broker</strong> — the central hub (Mosquitto, HiveMQ, AWS IoT Core). Routes messages between publishers and subscribers.</li>
<li><strong>Publisher</strong> — your ESP32, sending sensor readings to topics like <code>home/bedroom/temperature</code>.</li>
<li><strong>Subscriber</strong> — a Node-RED flow, Grafana panel, or another ESP32 receiving the messages.</li>
<li><strong>Topic</strong> — a UTF-8 string path like <code>home/bedroom/temperature</code>. Use <code>/</code> as a separator, <code>+</code> as a single-level wildcard, <code>#</code> as a multi-level wildcard.</li>
</ul>

<h2>Install PubSubClient</h2>
<p>Open Arduino IDE → Sketch → Include Library → Manage Libraries. Search for <strong>PubSubClient</strong> (by Nick O'Leary) and install the latest version.</p>

<h2>Connect and Publish</h2>
<div class="code-block"><div class="code-bar"><span>mqtt_publish.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;PubSubClient.h&gt;

const char* ssid        = "YourSSID";
const char* password    = "YourPassword";
const char* mqtt_server = "broker.hivemq.com";
const int   mqtt_port   = 1883;
const char* client_id   = "ESP32Sensor001";   // must be unique per broker

WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT... ");
    if (mqtt.connect(client_id)) {
      Serial.println("connected");
    } else {
      Serial.printf("failed (rc=%d) — retry in 5 s\n", mqtt.state());
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWi-Fi connected");

  mqtt.setServer(mqtt_server, mqtt_port);
  mqtt.setKeepAlive(60);
  connectMQTT();
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();   // processes incoming messages and keepalives

  // Publish a fake temperature reading every 10 s
  static unsigned long last = 0;
  if (millis() - last &gt;= 10000) {
    last = millis();
    float temp = 22.5 + (random(-10, 10) / 10.0);
    char buf[16];
    dtostrf(temp, 4, 1, buf);
    bool ok = mqtt.publish("home/bedroom/temperature", buf, true); // retained
    Serial.printf("Published: %s (%s)\n", buf, ok ? "OK" : "FAIL");
  }
}</pre></div>

<h2>Subscribing to Topics</h2>
<div class="code-block"><div class="code-bar"><span>mqtt_subscribe.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i &lt; length; i++) msg += (char)payload[i];
  Serial.printf("[%s] %s\n", topic, msg.c_str());

  // Control LED via command topic
  if (String(topic) == "home/bedroom/led/set") {
    digitalWrite(2, msg == "ON" ? HIGH : LOW);
  }
}

// In setup():
mqtt.setCallback(callback);

// In connectMQTT(), after mqtt.connect():
mqtt.subscribe("home/bedroom/led/set");
mqtt.subscribe("home/+/command");   // wildcard — all rooms</pre></div>

<h2>Last Will and Testament (LWT)</h2>
<p>LWT lets the broker announce on your behalf when your device goes offline unexpectedly:</p>
<div class="code-block"><div class="code-bar"><span>mqtt_lwt.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>// In setup(), before connectMQTT():
mqtt.setWill(
  "home/bedroom/status",  // topic
  "offline",              // message
  true,                   // retained
  1                       // QoS 1
);

// In connectMQTT(), after mqtt.connect():
mqtt.publish("home/bedroom/status", "online", true);</pre></div>

<h2>Publishing JSON with ArduinoJson</h2>
<div class="code-block"><div class="code-bar"><span>mqtt_json.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;ArduinoJson.h&gt;

void publishSensorData(float temp, float hum) {
  JsonDocument doc;
  doc["device"]      = client_id;
  doc["temperature"] = serialized(String(temp, 1));
  doc["humidity"]    = serialized(String(hum, 1));
  doc["uptime"]      = millis() / 1000;

  char buf[256];
  serializeJson(doc, buf, sizeof(buf));
  mqtt.publish("home/bedroom/sensors", buf, true);
}</pre></div>

<h2>MQTT over TLS (Port 8883)</h2>
<div class="code-block"><div class="code-bar"><span>mqtt_tls.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFiClientSecure.h&gt;

const char* root_ca = R"(-----BEGIN CERTIFICATE-----
... broker root CA certificate here ...
-----END CERTIFICATE-----
)";

WiFiClientSecure secureClient;
PubSubClient     mqtt(secureClient);

// In setup():
secureClient.setCACert(root_ca);
mqtt.setServer("your-broker.com", 8883);</pre></div>

<h2>Reconnect Pattern</h2>
<p>The connection can drop. Subscriptions are lost when it does. Always re-subscribe inside the reconnect function:</p>
<div class="code-block"><div class="code-bar"><span>mqtt_reconnect.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void connectMQTT() {
  int retries = 0;
  while (!mqtt.connected() && retries &lt; 5) {
    if (mqtt.connect(client_id, "username", "password")) {
      Serial.println("MQTT connected");
      // Re-subscribe every reconnect
      mqtt.subscribe("home/bedroom/led/set");
      mqtt.publish("home/bedroom/status", "online", true);
      return;
    }
    retries++;
    delay(5000);
  }
  if (!mqtt.connected()) ESP.restart(); // hard reset after 5 fails
}</pre></div>

<h2>Testing with MQTT Explorer</h2>
<p>Install <strong>MQTT Explorer</strong> (free, cross-platform) to visualise topics, publish test messages, and inspect payloads while developing. Connect to your broker, subscribe to <code>#</code> (all topics), and watch your ESP32 messages arrive in real time.</p>
HTML
],

];
