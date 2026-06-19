<?php
/* Phase 4: ESP32 Connectivity & Protocols — Guides 6–10
   websockets-esp32, bluetooth-classic-esp32, ble-esp32,
   esp-now-protocol, ota-updates-esp32
*/
return [

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'websockets-esp32',
'title'     => 'WebSockets on ESP32 — Real-Time Bidirectional Communication',
'meta_desc' => 'Implement WebSockets on ESP32 for real-time bidirectional data between the board and a browser. Covers ESPAsyncWebServer, ws.textAll(), JSON events, and client reconnection.',
'read_time' => '13 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['esp32-web-server','mqtt-esp32','wifi-basics-esp32','ota-updates-esp32'],
'faqs'      => [
  ['q'=>'What is the difference between HTTP polling and WebSockets for ESP32?','a'=>'HTTP polling requires the browser to repeatedly request new data (every 1–2 seconds). WebSockets establish a persistent TCP connection so the ESP32 can push data to the browser the instant it changes, with no polling overhead.'],
  ['q'=>'Which library provides WebSocket support for ESP32?','a'=>'ESPAsyncWebServer (by me-no-dev) includes AsyncWebSocket built-in. Install it via the Library Manager along with its dependency AsyncTCP. Both are needed for WebSocket support.'],
  ['q'=>'How many WebSocket clients can ESP32 handle simultaneously?','a'=>'Practically 4–8 concurrent WebSocket clients on a typical ESP32 before heap pressure causes disconnects. The default ESPAsyncWebServer WebSocket limit is defined by WS_MAX_QUEUED_MESSAGES (50 by default).'],
  ['q'=>'How do I send sensor data to all connected WebSocket clients?','a'=>'Call ws.textAll("your data string") from anywhere in your sketch. This queues the message for transmission to every currently connected client in a single call.'],
  ['q'=>'Can I send binary data over WebSockets on ESP32?','a'=>'Yes. Use ws.binaryAll(uint8_t* data, size_t len) to broadcast binary frames to all clients, or ws.binary(client_id, data, len) for a specific client. This is useful for sending sensor arrays or image data.'],
  ['q'=>'How do I handle WebSocket client disconnections on ESP32?','a'=>'Listen for the WS_EVT_DISCONNECT event in your onEvent callback. Clean up any per-client state keyed by client->id() in that handler. ESPAsyncWebServer calls this event even on timeout-based disconnections.'],
  ['q'=>'Why do WebSocket messages arrive out of order on ESP32?','a'=>'Async delivery does not guarantee order when messages are queued faster than the TCP stack can send them. For ordered delivery, use a sequence number in each message and sort on the client side, or throttle the send rate.'],
  ['q'=>'Can I use WebSockets without a full web server on ESP32?','a'=>'The arduinoWebSockets library (by Links2004) provides a standalone WebSocket client and server without the full AsyncWebServer framework. It is lighter but has fewer features.'],
  ['q'=>'How do I reconnect a browser WebSocket if the ESP32 reboots?','a'=>'Add reconnect logic in the browser: on the WebSocket close event, wait 2–5 seconds then call new WebSocket(url) again. Repeat until connected.'],
  ['q'=>'What is the maximum WebSocket message size on ESP32?','a'=>'By default ESPAsyncWebServer limits WebSocket frames to 1436 bytes (one TCP segment). Larger messages are split into fragments. The server reassembles them transparently, but keep individual payloads under 4 KB to avoid heap issues.'],
],
'body_html' => <<<'HTML'
<h2>Why WebSockets?</h2>
<p>A web server on ESP32 is great for static pages, but once you need live sensor graphs, joystick controls, or real-time status indicators, HTTP polling becomes wasteful. WebSockets upgrade the HTTP handshake into a persistent bidirectional TCP pipe — the ESP32 pushes data the instant it changes, and the browser sends commands back on the same connection.</p>

<h2>Libraries Required</h2>
<p>Install both via Arduino Library Manager:</p>
<ol>
<li><strong>ESPAsyncWebServer</strong> (by lacamera or me-no-dev)</li>
<li><strong>AsyncTCP</strong> (dependency, for ESP32)</li>
</ol>

<h2>Complete WebSocket LED Controller</h2>
<div class="code-block"><div class="code-bar"><span>websocket_led.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;AsyncTCP.h&gt;
#include &lt;ESPAsyncWebServer.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

const int LED_PIN = 2;
bool ledState = false;

// HTML page served from PROGMEM
const char INDEX_HTML[] PROGMEM = R"rawliteral(
&lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;
&lt;meta charset='utf-8'&gt;&lt;title&gt;ESP32 WS&lt;/title&gt;
&lt;style&gt;body{font-family:sans-serif;max-width:400px;margin:2rem auto}
.btn{padding:.6rem 1.4rem;font-size:1rem;cursor:pointer;border-radius:6px;border:none;color:#fff}
.on{background:#16a34a}.off{background:#dc2626}&lt;/style&gt;&lt;/head&gt;&lt;body&gt;
&lt;h1&gt;LED Control&lt;/h1&gt;
&lt;p&gt;State: &lt;strong id='state'&gt;--&lt;/strong&gt;&lt;/p&gt;
&lt;button class='btn on' onclick='send("on")'&gt;Turn ON&lt;/button&gt;
&lt;button class='btn off' onclick='send("off")'&gt;Turn OFF&lt;/button&gt;
&lt;script&gt;
var ws = new WebSocket('ws://' + location.host + '/ws');
ws.onmessage = e =&gt; document.getElementById('state').textContent = e.data;
ws.onclose   = () =&gt; setTimeout(() =&gt; location.reload(), 3000);
function send(cmd) { ws.send(cmd); }
&lt;/script&gt;&lt;/body&gt;&lt;/html&gt;
)rawliteral";

void onWsEvent(AsyncWebSocket* server, AsyncWebSocketClient* client,
               AwsEventType type, void* arg, uint8_t* data, size_t len) {
  if (type == WS_EVT_CONNECT) {
    Serial.printf("WS client #%u connected\n", client->id());
    client->text(ledState ? "ON" : "OFF");   // send current state on connect
  }
  else if (type == WS_EVT_DISCONNECT) {
    Serial.printf("WS client #%u disconnected\n", client->id());
  }
  else if (type == WS_EVT_DATA) {
    AwsFrameInfo* info = (AwsFrameInfo*)arg;
    if (info->final && info->opcode == WS_TEXT) {
      String msg = "";
      for (size_t i = 0; i &lt; len; i++) msg += (char)data[i];
      if (msg == "on")  { ledState = true;  digitalWrite(LED_PIN, HIGH); }
      if (msg == "off") { ledState = false; digitalWrite(LED_PIN, LOW);  }
      ws.textAll(ledState ? "ON" : "OFF");   // broadcast to all clients
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nIP: " + WiFi.localIP().toString());

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
    req->send_P(200, "text/html", INDEX_HTML);
  });
  server.begin();
}

void loop() {
  ws.cleanupClients();   // free disconnected client memory
}</pre></div>

<h2>Broadcasting Sensor Data Periodically</h2>
<div class="code-block"><div class="code-bar"><span>ws_sensor_broadcast.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void loop() {
  ws.cleanupClients();

  static unsigned long last = 0;
  if (millis() - last &gt;= 1000) {
    last = millis();

    // Build JSON payload
    float temp = 20.0 + (analogRead(34) / 4095.0) * 20.0;
    char buf[64];
    snprintf(buf, sizeof(buf),
      "{\"temp\":%.1f,\"uptime\":%lu}", temp, millis() / 1000);

    if (ws.count() &gt; 0) {   // only send if anyone is listening
      ws.textAll(buf);
    }
  }
}</pre></div>

<h2>Ping/Pong and Connection Health</h2>
<p>WebSocket connections can silently die when a client's network changes. Configure pings to detect dead connections:</p>
<div class="code-block"><div class="code-bar"><span>ws_ping.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>// In onWsEvent, handle the pong:
else if (type == WS_EVT_PONG) {
  Serial.printf("Client #%u pong received\n", client->id());
}

// In loop(), ping all clients every 30 s:
static unsigned long lastPing = 0;
if (millis() - lastPing &gt; 30000) {
  lastPing = millis();
  ws.pingAll();
}</pre></div>

<h2>Client-Side Reconnect</h2>
<p>Add this JavaScript to any page to automatically reconnect when the ESP32 reboots:</p>
<div class="code-block"><div class="code-bar"><span>reconnect.js</span><button class="copy-btn" type="button">Copy</button></div>
<pre>function connectWS() {
  const ws = new WebSocket('ws://' + location.host + '/ws');
  ws.onopen    = () =&gt; console.log('WS connected');
  ws.onmessage = e =&gt; updateUI(JSON.parse(e.data));
  ws.onclose   = () =&gt; {
    console.log('WS closed — reconnecting in 3 s');
    setTimeout(connectWS, 3000);
  };
  ws.onerror   = () =&gt; ws.close();
  return ws;
}
const socket = connectWS();</pre></div>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'bluetooth-classic-esp32',
'title'     => 'Bluetooth Classic on ESP32 — Serial Over Bluetooth (SPP)',
'meta_desc' => 'Use ESP32 Bluetooth Classic Serial Port Profile (SPP) to send and receive data wirelessly from Android phones, Windows PCs, and other Bluetooth devices using Serial commands.',
'read_time' => '11 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['ble-esp32','wifi-basics-esp32','esp32-wifi-modes','digital-outputs-esp32'],
'faqs'      => [
  ['q'=>'What is the difference between Bluetooth Classic and BLE on ESP32?','a'=>'Bluetooth Classic (BR/EDR) supports the Serial Port Profile (SPP) for high-throughput streaming data — like connecting to Android apps via the Bluetooth Serial terminal. BLE (Bluetooth Low Energy) uses GATT profiles, consumes far less power, and is preferred for wearables, beacons, and iOS devices.'],
  ['q'=>'Can I use ESP32 Bluetooth Classic with an iPhone?','a'=>'No. Apple removed Bluetooth Classic SPP support from iOS. Use BLE with the NimBLE or ArduinoBLE library for iOS connectivity.'],
  ['q'=>'Do I need a Bluetooth module (HC-05/HC-06) with ESP32?','a'=>'No. The ESP32 has built-in Bluetooth hardware — both Classic and BLE. You do not need an external HC-05 or HC-06 module. The BluetoothSerial library accesses the built-in radio directly.'],
  ['q'=>'How do I pair an Android phone with ESP32 Bluetooth?','a'=>'Open Settings → Bluetooth on Android, scan for devices, and tap your ESP32 name (e.g. "ESP32-BT"). Accept the pairing request. Then use a terminal app like Serial Bluetooth Terminal to send and receive data.'],
  ['q'=>'Can ESP32 act as a Bluetooth master (connect to another device)?','a'=>'Yes. Call SerialBT.connect("HC-05") to initiate a master connection to another device by name, or SerialBT.connect(address) to connect by MAC address. This lets ESP32 talk to HC-05/HC-06 modules and Bluetooth keyboards.'],
  ['q'=>'What is the data rate of ESP32 Bluetooth Classic SPP?','a'=>'SPP theoretical throughput is around 1 Mbps, with real-world rates of 100–300 Kbps depending on Bluetooth version and interference. This is much higher than BLE (27 Kbps effective for BLE 4.2) making Classic better for audio or bulk data.'],
  ['q'=>'Can I use Bluetooth and Wi-Fi simultaneously on ESP32?','a'=>'Yes. The ESP32 has a co-existence system that time-multiplexes the 2.4 GHz radio between Wi-Fi and Bluetooth. Performance of both is reduced slightly when both are active.'],
  ['q'=>'How do I set a PIN for ESP32 Bluetooth pairing?','a'=>'Call SerialBT.setPin("1234") before SerialBT.begin() to set a 4-digit PIN. Without this call, most Android versions pair without a PIN confirmation.'],
  ['q'=>'Can multiple devices pair with the ESP32 Bluetooth at the same time?','a'=>'Bluetooth Classic supports only one active connection at a time. If a second device tries to connect while one is already connected, it will either be rejected or the first connection will be dropped.'],
  ['q'=>'Why does ESP32 Bluetooth not work on ESP32-S2?','a'=>'The ESP32-S2 chip does not include a Bluetooth radio — it is Wi-Fi only. Use an ESP32, ESP32-S3, or ESP32-C3 for Bluetooth. The S3 supports both Classic and BLE; the C3 supports only BLE.'],
],
'body_html' => <<<'HTML'
<h2>Bluetooth Serial on ESP32</h2>
<p>The <code>BluetoothSerial</code> library makes the ESP32's Bluetooth Classic radio behave like a serial port — the same <code>read()</code>, <code>print()</code>, and <code>println()</code> methods you already know from <code>Serial</code>. This is perfect for replacing an HC-05/HC-06 module, building a wireless serial monitor, or controlling an ESP32 from an Android app.</p>

<h2>Echo Server — Send What You Receive</h2>
<div class="code-block"><div class="code-bar"><span>bt_echo.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32-Device");   // Bluetooth device name
  Serial.println("Bluetooth started — pair with 'ESP32-Device'");
}

void loop() {
  // Forward USB Serial → Bluetooth
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  // Forward Bluetooth → USB Serial
  if (SerialBT.available()) {
    char c = SerialBT.read();
    Serial.write(c);
    SerialBT.write(c);   // echo back
  }
}</pre></div>

<h2>Command Parser</h2>
<p>A practical pattern: read a full line of text and parse it as a command:</p>
<div class="code-block"><div class="code-bar"><span>bt_commands.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include "BluetoothSerial.h"

BluetoothSerial SerialBT;
const int LED = 2;

void handleCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();

  if (cmd == "on")  {
    digitalWrite(LED, HIGH);
    SerialBT.println("LED turned ON");
  }
  else if (cmd == "off") {
    digitalWrite(LED, LOW);
    SerialBT.println("LED turned OFF");
  }
  else if (cmd == "status") {
    SerialBT.printf("LED: %s | Uptime: %lus\n",
      digitalRead(LED) ? "ON" : "OFF", millis() / 1000);
  }
  else {
    SerialBT.println("Unknown command. Try: on, off, status");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  SerialBT.begin("ESP32-Control");
  Serial.println("Bluetooth ready");
}

void loop() {
  if (SerialBT.available()) {
    String line = SerialBT.readStringUntil('\n');
    handleCommand(line);
  }
}</pre></div>

<h2>Setting a Pairing PIN</h2>
<div class="code-block"><div class="code-bar"><span>bt_pin.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.setPin("1234");   // set before begin()
  SerialBT.begin("SecureESP32");
  Serial.println("PIN: 1234");
}</pre></div>

<h2>ESP32 as Bluetooth Master (Connect to HC-05)</h2>
<div class="code-block"><div class="code-bar"><span>bt_master.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

// Replace with your HC-05 MAC address (printed on module or found via scan)
uint8_t target_mac[6] = {0x00, 0x21, 0x09, 0x00, 0xBE, 0xEF};

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32-Master", true);   // true = master mode

  Serial.println("Connecting to HC-05...");
  bool connected = SerialBT.connect(target_mac);
  if (connected) {
    Serial.println("Connected!");
  } else {
    Serial.println("Failed — check MAC and pairing");
  }
}

void loop() {
  if (SerialBT.available()) Serial.write(SerialBT.read());
  if (Serial.available())   SerialBT.write(Serial.read());
}</pre></div>

<h2>Connection Event Callback</h2>
<div class="code-block"><div class="code-bar"><span>bt_events.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>void btCallback(esp_spp_cb_event_t event, esp_spp_cb_param_t* param) {
  if (event == ESP_SPP_SRV_OPEN_EVT) {
    Serial.println("Client connected");
    SerialBT.println("Welcome to ESP32!");
  }
  if (event == ESP_SPP_CLOSE_EVT) {
    Serial.println("Client disconnected");
  }
}

// In setup(), before SerialBT.begin():
SerialBT.register_callback(btCallback);</pre></div>

<h2>Android Apps for Testing</h2>
<ul>
<li><strong>Serial Bluetooth Terminal</strong> (Google Play) — clean terminal, supports newline modes, timestamps</li>
<li><strong>Bluetooth Serial Monitor</strong> — shows raw bytes and ASCII side-by-side</li>
<li><strong>MIT App Inventor</strong> — build a custom app with buttons that send commands over BT Classic</li>
</ul>

<h2>Transitioning to BLE</h2>
<p>If you need iOS support, lower power consumption, or compatibility with modern wearables, migrate to the <a href="/guides/ble-esp32/">BLE guide</a> which uses GATT services instead of SPP.</p>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'ble-esp32',
'title'     => 'BLE on ESP32 — GATT Server, Characteristics, and Notifications',
'meta_desc' => 'Implement Bluetooth Low Energy on ESP32 as a GATT server. Create services and characteristics, send notifications to connected clients, and receive commands from iOS and Android.',
'read_time' => '14 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['bluetooth-classic-esp32','wifi-basics-esp32','esp-now-protocol','ota-updates-esp32'],
'faqs'      => [
  ['q'=>'What is the difference between a BLE service, characteristic, and descriptor?','a'=>'A service groups related data (e.g. "Heart Rate Service"). A characteristic is one data point within a service (e.g. "Heart Rate Measurement") — it has a UUID, a value, and properties (read/write/notify). A descriptor adds metadata to a characteristic (e.g. human-readable name, units, notify enable flag).'],
  ['q'=>'What BLE UUIDs should I use for custom ESP32 services?','a'=>'For standard profiles use official Bluetooth SIG UUIDs (16-bit, e.g. 0x180D for Heart Rate). For custom services use any valid 128-bit UUID (e.g. generated at uuidgenerator.net). Avoid reusing standard UUIDs for non-standard data.'],
  ['q'=>'How do I send data from ESP32 to a phone using BLE notifications?','a'=>'Set the characteristic property to BLECharacteristic::PROPERTY_NOTIFY, add a BLE2902 descriptor, then call characteristic->setValue(data) and characteristic->notify(). The phone receives the update without polling.'],
  ['q'=>'What is the maximum BLE packet size on ESP32?','a'=>'The default ATT MTU is 23 bytes (20 bytes of payload after 3 bytes overhead). After MTU negotiation, this can increase to 517 bytes (512 bytes payload) for BLE 4.2+ on ESP32. For larger data, split across multiple characteristic writes.'],
  ['q'=>'Can I connect multiple phones to one ESP32 BLE server?','a'=>'The default BLE stack allows one central (client) connection at a time. The ESP32 can technically support up to 3–4 simultaneous BLE connections but this requires lower-level SDK configuration and significantly increases RAM usage.'],
  ['q'=>'What is BLE advertising and when does it happen?','a'=>'Advertising is the periodic broadcast of the ESP32\'s identity (device name, service UUIDs) so nearby phones can discover it. It happens before a connection is established. Once connected, advertising typically stops. Restart it after disconnection with pServer->getAdvertising()->start().'],
  ['q'=>'How do I read data sent from a phone to ESP32 via BLE write?','a'=>'Set the characteristic property to PROPERTY_WRITE, attach a callback class that extends BLECharacteristicCallbacks, and override the onWrite() method. Inside it call pCharacteristic->getValue() to get the written bytes.'],
  ['q'=>'Does NimBLE-Arduino use less memory than the default ESP32 BLE stack?','a'=>'Yes, significantly. NimBLE-Arduino uses approximately 50% less heap and flash compared to the default Bluedroid stack. For RAM-constrained applications, switch to NimBLE by installing the library and changing include headers accordingly.'],
  ['q'=>'Can ESP32 BLE work simultaneously with Wi-Fi?','a'=>'Yes. Both share the 2.4 GHz radio via time-division co-existence. You will see slight throughput reduction on both interfaces. Call esp_coex_preference_set(ESP_COEX_PREFER_BALANCE) to balance performance between them.'],
  ['q'=>'How do I test ESP32 BLE without writing a mobile app?','a'=>'Use nRF Connect (iOS/Android) to discover services, read/write characteristics, and enable notifications. Use LightBlue (iOS/Android) for a friendlier UI. Both apps are free and invaluable for BLE debugging.'],
],
'body_html' => <<<'HTML'
<h2>BLE vs Bluetooth Classic</h2>
<p>Bluetooth Low Energy (BLE) is not a lower-speed version of Bluetooth Classic — it is a completely different protocol stack optimised for sending small bursts of data infrequently. A BLE temperature sensor can run on a coin cell for months. The tradeoff: BLE throughput is limited to ~27 Kbps effective (BLE 4.2) vs ~300 Kbps for Classic SPP. BLE is also the only option for iOS connectivity.</p>

<h2>GATT Concepts</h2>
<ul>
<li><strong>Server</strong> — the ESP32; holds the data (services and characteristics)</li>
<li><strong>Client</strong> — the phone; connects to read/write characteristics and subscribe to notifications</li>
<li><strong>Service UUID</strong> — identifies a group of related data (e.g. <code>4fafc201-1fb5-459e-8fcc-c5c9c3319000</code>)</li>
<li><strong>Characteristic UUID</strong> — identifies one value within a service (e.g. <code>beb5483e-36e1-4688-b7f5-ea07361b26a8</code>)</li>
</ul>

<h2>Temperature Notification Server</h2>
<div class="code-block"><div class="code-bar"><span>ble_temperature.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;BLEDevice.h&gt;
#include &lt;BLEUtils.h&gt;
#include &lt;BLEServer.h&gt;
#include &lt;BLE2902.h&gt;

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c3319000"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic* pChar;
bool deviceConnected = false;

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer)    { deviceConnected = true;  Serial.println("BLE: client connected"); }
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    Serial.println("BLE: client disconnected — restarting advertising");
    pServer->getAdvertising()->start();
  }
};

void setup() {
  Serial.begin(115200);

  BLEDevice::init("ESP32-Temp");
  BLEServer* pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  BLEService* pService = pServer->createService(SERVICE_UUID);

  pChar = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  pChar->addDescriptor(new BLE2902());   // enables notify subscription

  pService->start();

  BLEAdvertising* pAdv = BLEDevice::getAdvertising();
  pAdv->addServiceUUID(SERVICE_UUID);
  pAdv->setScanResponse(true);
  BLEDevice::startAdvertising();
  Serial.println("BLE advertising as 'ESP32-Temp'");
}

void loop() {
  if (deviceConnected) {
    float temp = 22.5 + (random(-5, 5) / 10.0);   // replace with real sensor
    char buf[8];
    dtostrf(temp, 4, 1, buf);
    pChar->setValue(buf);
    pChar->notify();
    Serial.printf("Notified: %s°C\n", buf);
  }
  delay(2000);
}</pre></div>

<h2>Receiving Write Commands from a Phone</h2>
<div class="code-block"><div class="code-bar"><span>ble_write.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#define CMD_UUID "a1234567-0000-1000-8000-00805f9b34fb"

const int LED = 2;

class CmdCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* pC) {
    String val = pC->getValue().c_str();
    val.trim();
    if (val == "ON")  { digitalWrite(LED, HIGH); Serial.println("LED ON"); }
    if (val == "OFF") { digitalWrite(LED, LOW);  Serial.println("LED OFF"); }
  }
};

// In setup(), after createService():
BLECharacteristic* pCmd = pService->createCharacteristic(
  CMD_UUID,
  BLECharacteristic::PROPERTY_WRITE
);
pCmd->setCallbacks(new CmdCallbacks());</pre></div>

<h2>Read-Only Characteristic</h2>
<div class="code-block"><div class="code-bar"><span>ble_read.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#define UPTIME_UUID "b2345678-0001-1000-8000-00805f9b34fb"

BLECharacteristic* pUptime = pService->createCharacteristic(
  UPTIME_UUID,
  BLECharacteristic::PROPERTY_READ
);

// Update before each read (use a callback to stay current):
class UptimeCallbacks : public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic* pC) {
    unsigned long s = millis() / 1000;
    char buf[16];
    snprintf(buf, sizeof(buf), "%lus", s);
    pC->setValue(buf);
  }
};
pUptime->setCallbacks(new UptimeCallbacks());</pre></div>

<h2>Using nRF Connect to Test</h2>
<ol>
<li>Install <strong>nRF Connect for Mobile</strong> (Android/iOS) — free from Nordic Semiconductor</li>
<li>Open the app → Scan → find "ESP32-Temp"</li>
<li>Connect → expand the Unknown Service</li>
<li>Tap the notification icon (three arrows down) to subscribe to notifications</li>
<li>Watch temperature values arrive every 2 seconds</li>
<li>Tap the write icon on the command characteristic → type "ON" → send</li>
</ol>

<h2>NimBLE for Lower Memory Usage</h2>
<p>The default Bluedroid BLE stack uses ~100 KB of heap. For projects that also use Wi-Fi, switch to NimBLE-Arduino which uses ~50 KB:</p>
<div class="code-block"><div class="code-bar"><span>nimble_switch.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>// Replace all BLEDevice.h imports with:
#include &lt;NimBLEDevice.h&gt;

// API is nearly identical — NimBLEServer, NimBLEService, NimBLECharacteristic
// No BLE2902 descriptor needed — NimBLE handles notifications automatically
// Connections: up to 9 simultaneous clients (vs 3 with Bluedroid)</pre></div>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'esp-now-protocol',
'title'     => 'ESP-NOW — Low-Latency Peer-to-Peer Wireless Between ESP32 Boards',
'meta_desc' => 'Use ESP-NOW to send data between ESP32 boards without a Wi-Fi router. Covers point-to-point, broadcast, and multi-peer communication with send/receive callbacks and error handling.',
'read_time' => '13 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','ble-esp32','bluetooth-classic-esp32','mqtt-esp32'],
'faqs'      => [
  ['q'=>'What is ESP-NOW and when should I use it instead of Wi-Fi?','a'=>'ESP-NOW is a proprietary Espressif protocol that lets ESP8266/ESP32 devices communicate directly at the MAC layer, bypassing TCP/IP entirely. Use it when you need ultra-low latency (< 2 ms), want to avoid a router, need to wake from deep sleep and send quickly, or want a wireless sensor network without internet.'],
  ['q'=>'What is the maximum ESP-NOW packet size?','a'=>'ESP-NOW payloads are limited to 250 bytes per packet. For larger data, split into multiple packets and reassemble with a sequence counter on the receiver side.'],
  ['q'=>'Does ESP-NOW work at the same time as Wi-Fi?','a'=>'Yes, but both must use the same Wi-Fi channel. Call WiFi.begin() first (STA mode) to get the router channel, then initialise ESP-NOW. The channel is determined by the router and both protocols share it.'],
  ['q'=>'How do I find the MAC address of my ESP32 for ESP-NOW?','a'=>'Call WiFi.macAddress() after WiFi.mode(WIFI_STA) and before WiFi.begin(). Print it to Serial. Alternatively use esp_read_mac() from esp_wifi.h for the base MAC without initialising Wi-Fi.'],
  ['q'=>'What is ESP-NOW broadcast address?','a'=>'The broadcast MAC address is {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}. Sending to this address delivers the packet to ALL ESP-NOW-listening devices in range, regardless of whether they are registered as peers.'],
  ['q'=>'Can I send from multiple senders to one ESP-NOW receiver?','a'=>'Yes. The receiver must register each sender as a peer using esp_now_add_peer(). In practice you can register up to 20 peers. All their messages arrive at the same onDataRecv callback where you use the sender MAC to route them.'],
  ['q'=>'How far does ESP-NOW reach?','a'=>'Typically 200–500 m line-of-sight outdoors with PCB antenna. With an external omnidirectional antenna (IPEX connector or U.FL on some modules) range can exceed 1 km.'],
  ['q'=>'Is ESP-NOW encrypted?','a'=>'Encryption is optional per-peer. Enable it with esp_now_peer_info_t.encrypt = true and supply a 16-byte Local Master Key (LMK). Without encryption, packets are transmitted in plain text.'],
  ['q'=>'What happens to ESP-NOW if the receiver is out of range?','a'=>'The sender\'s onDataSent callback receives ESP_NOW_SEND_FAIL status. The packet is dropped — ESP-NOW does not retry or queue. Implement application-level acknowledgement if delivery confirmation is critical.'],
  ['q'=>'Can ESP-NOW work during deep sleep?','a'=>'Not directly — the radio is off during deep sleep. The typical pattern is: wake, call WiFi.mode(WIFI_STA) + esp_now_init(), send one packet, wait for the onDataSent callback, then go back to deep sleep. Total awake time is 50–150 ms.'],
],
'body_html' => <<<'HTML'
<h2>Why ESP-NOW?</h2>
<p>ESP-NOW operates at the 802.11 MAC layer — there is no TCP handshake, no IP address, no DHCP, no router. One ESP32 sends a 250-byte packet directly to another ESP32's MAC address and it arrives in under 2 milliseconds. For remote sensors, wireless remotes, and mesh networks where a router is impractical, ESP-NOW is the right tool.</p>

<h2>Comparison: ESP-NOW vs Wi-Fi MQTT vs BLE</h2>
<table style="width:100%;border-collapse:collapse;margin:1rem 0">
<thead><tr style="background:var(--surface-2)"><th style="padding:0.5rem">Feature</th><th style="padding:0.5rem">ESP-NOW</th><th style="padding:0.5rem">Wi-Fi + MQTT</th><th style="padding:0.5rem">BLE</th></tr></thead>
<tbody>
<tr><td style="padding:0.5rem">Latency</td><td style="padding:0.5rem">&lt; 2 ms</td><td style="padding:0.5rem">50–300 ms</td><td style="padding:0.5rem">10–50 ms</td></tr>
<tr><td style="padding:0.5rem">Router needed</td><td style="padding:0.5rem">No</td><td style="padding:0.5rem">Yes</td><td style="padding:0.5rem">No</td></tr>
<tr><td style="padding:0.5rem">Max payload</td><td style="padding:0.5rem">250 bytes</td><td style="padding:0.5rem">256 MB</td><td style="padding:0.5rem">512 bytes (MTU)</td></tr>
<tr><td style="padding:0.5rem">Peer limit</td><td style="padding:0.5rem">20 encrypted</td><td style="padding:0.5rem">Unlimited</td><td style="padding:0.5rem">9 (NimBLE)</td></tr>
<tr><td style="padding:0.5rem">Wake from sleep</td><td style="padding:0.5rem">~50 ms</td><td style="padding:0.5rem">~2000 ms</td><td style="padding:0.5rem">~500 ms</td></tr>
</tbody></table>

<h2>Point-to-Point Sender</h2>
<div class="code-block"><div class="code-bar"><span>espnow_sender.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;esp_now.h&gt;

// Replace with the MAC address printed by the RECEIVER sketch
uint8_t receiverMAC[] = {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF};

typedef struct {
  float    temperature;
  float    humidity;
  uint32_t counter;
} SensorPacket;

SensorPacket packet;

void onDataSent(const uint8_t* mac, esp_now_send_status_t status) {
  Serial.printf("Send to %02X:%02X:%02X:%02X:%02X:%02X — %s\n",
    mac[0], mac[1], mac[2], mac[3], mac[4], mac[5],
    status == ESP_NOW_SEND_SUCCESS ? "OK" : "FAIL");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }
  esp_now_register_send_cb(onDataSent);

  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, receiverMAC, 6);
  peer.channel = 0;     // 0 = current channel
  peer.encrypt = false;
  esp_now_add_peer(&peer);

  Serial.println("Sender ready. My MAC: " + WiFi.macAddress());
}

void loop() {
  packet.temperature = 22.5 + (random(-20, 20) / 10.0);
  packet.humidity    = 55.0 + (random(-50, 50) / 10.0);
  packet.counter++;

  esp_err_t result = esp_now_send(receiverMAC,
    (uint8_t*)&packet, sizeof(packet));

  Serial.printf("Sent #%lu: %.1f°C %.1f%% — %s\n",
    packet.counter, packet.temperature, packet.humidity,
    result == ESP_OK ? "queued" : "error");

  delay(2000);
}</pre></div>

<h2>Receiver</h2>
<div class="code-block"><div class="code-bar"><span>espnow_receiver.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;esp_now.h&gt;

typedef struct {
  float    temperature;
  float    humidity;
  uint32_t counter;
} SensorPacket;

void onDataRecv(const esp_now_recv_info_t* info,
                const uint8_t* data, int len) {
  SensorPacket* p = (SensorPacket*)data;
  Serial.printf("From %02X:%02X:%02X:%02X:%02X:%02X — ",
    info->src_addr[0], info->src_addr[1], info->src_addr[2],
    info->src_addr[3], info->src_addr[4], info->src_addr[5]);
  Serial.printf("#%lu  %.1f°C  %.1f%%\n",
    p->counter, p->temperature, p->humidity);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }
  esp_now_register_recv_cb(onDataRecv);

  Serial.println("Receiver ready. My MAC: " + WiFi.macAddress());
  Serial.println("Give this MAC to the sender sketch.");
}

void loop() {}</pre></div>

<h2>Broadcast to All Devices</h2>
<div class="code-block"><div class="code-bar"><span>espnow_broadcast.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>uint8_t broadcastMAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

esp_now_peer_info_t bcastPeer = {};
memcpy(bcastPeer.peer_addr, broadcastMAC, 6);
bcastPeer.channel = 0;
bcastPeer.encrypt = false;
esp_now_add_peer(&bcastPeer);

// Send:
esp_now_send(broadcastMAC, (uint8_t*)&packet, sizeof(packet));</pre></div>

<h2>Deep Sleep Sender (Battery Sensor Node)</h2>
<div class="code-block"><div class="code-bar"><span>espnow_deepsleep.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;esp_now.h&gt;
#include &lt;esp_sleep.h&gt;

#define SLEEP_SECONDS 60

uint8_t receiverMAC[] = {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF};
volatile bool sent = false;

typedef struct { float temp; uint32_t bootCount; } Pkt;

RTC_DATA_ATTR uint32_t bootCount = 0;

void onSent(const uint8_t* mac, esp_now_send_status_t s) {
  Serial.printf("Sent: %s\n", s == ESP_NOW_SEND_SUCCESS ? "OK" : "FAIL");
  sent = true;
}

void setup() {
  Serial.begin(115200);
  bootCount++;

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  esp_now_init();
  esp_now_register_send_cb(onSent);

  esp_now_peer_info_t p = {};
  memcpy(p.peer_addr, receiverMAC, 6);
  esp_now_add_peer(&p);

  Pkt pkt = { 23.5, bootCount };
  esp_now_send(receiverMAC, (uint8_t*)&pkt, sizeof(pkt));

  // Wait for send callback (max 200 ms)
  unsigned long t = millis();
  while (!sent && millis() - t &lt; 200) delay(10);

  Serial.printf("Sleeping %d s (boot #%lu)\n", SLEEP_SECONDS, bootCount);
  esp_deep_sleep(SLEEP_SECONDS * 1000000ULL);
}

void loop() {}</pre></div>
HTML
],

/* ─────────────────────────────────────────────────────────────────── */
[
'slug'      => 'ota-updates-esp32',
'title'     => 'OTA Updates on ESP32 — Update Firmware Over Wi-Fi',
'meta_desc' => 'Flash new firmware to ESP32 over Wi-Fi without a USB cable. Covers ArduinoOTA (Arduino IDE), web browser OTA with ESPAsyncWebServer, and secure HTTPS OTA from a server.',
'read_time' => '14 min',
'phase'     => 'Phase 4: Connectivity',
'related'   => ['wifi-basics-esp32','esp32-web-server','http-client-esp32','esp32-wifi-modes'],
'faqs'      => [
  ['q'=>'What is OTA (Over-the-Air) update on ESP32?','a'=>'OTA lets you upload new firmware to ESP32 over Wi-Fi without connecting a USB cable. The ESP32 runs the new firmware from a second flash partition (OTA partition 0 and OTA partition 1) and switches to it on reboot, leaving the old firmware as a rollback option.'],
  ['q'=>'How much flash space does OTA require?','a'=>'OTA needs two firmware partitions plus one OTA data partition. By default each firmware partition is about half the available flash minus overhead. On a 4 MB flash chip, each OTA slot is about 1.9 MB, leaving ~1.8 MB for SPIFFS/LittleFS.'],
  ['q'=>'What is the difference between ArduinoOTA and web-browser OTA?','a'=>'ArduinoOTA uses the Arduino IDE\'s built-in upload mechanism over mDNS and UDP — you select the network port in the IDE exactly like a USB port. Web-browser OTA uses an HTTP endpoint where you upload the .bin file through a web form without the Arduino IDE.'],
  ['q'=>'Is ArduinoOTA secure?','a'=>'By default ArduinoOTA has optional MD5 hash verification and password protection, but it sends the firmware unencrypted over the local network. For production devices, use HTTPS OTA (Update library with WiFiClientSecure) to encrypt the firmware in transit.'],
  ['q'=>'Can I rollback to the previous firmware after an OTA update?','a'=>'Yes. The esp_ota_ops.h API includes esp_ota_mark_app_invalid_rollback_and_reboot() to return to the previous firmware partition. Implement a "healthy boot" check in your app_main and only mark the update as valid after verifying the new firmware works correctly.'],
  ['q'=>'How do I trigger an OTA update automatically from a server?','a'=>'Use the Update library with HTTPClient: periodically check a version endpoint, compare with your current version (defined as a build flag), and if a newer version is available call Update.begin() followed by Update.writeStream(httpStream) to download and apply the update.'],
  ['q'=>'Can I update SPIFFS/LittleFS content via OTA?','a'=>'Yes. Arduino IDE OTA supports a separate filesystem upload. Build with Sketch → Export Compiled Binary, then use the filesystem image OTA slot. Alternatively upload files individually via HTTP PUT endpoints served by the ESP32.'],
  ['q'=>'What happens if the Wi-Fi drops during an OTA update?','a'=>'If the write to flash fails mid-way, the OTA data partition still points to the old firmware and the ESP32 boots normally after a timeout or power cycle. The incomplete new firmware partition is simply overwritten on the next update attempt.'],
  ['q'=>'How do I password-protect ArduinoOTA updates?','a'=>'Call ArduinoOTA.setPassword("yourpassword") before ArduinoOTA.begin(). The Arduino IDE will prompt for the password when uploading via the network port. Use a strong password — the credentials are sent as an MD5 hash, not plain text.'],
  ['q'=>'Can I do OTA updates without Arduino IDE using HTTP?','a'=>'Yes. The Update library\'s Update.begin() / Update.write() / Update.end() functions work independently of ArduinoOTA. Build your firmware binary in Arduino IDE (Sketch → Export Compiled Binary) and upload it via any HTTP server endpoint you create.'],
],
'body_html' => <<<'HTML'
<h2>Why OTA Matters</h2>
<p>Once an ESP32 sensor is mounted behind a wall, embedded in a product enclosure, or deployed to a remote location, reprogramming it by USB cable is impractical. OTA lets you push bug fixes and new features wirelessly from your laptop — or even automate firmware updates from a cloud server.</p>

<h2>Method 1 — ArduinoOTA (Arduino IDE Upload via Network)</h2>
<p>The simplest approach: the ESP32 appears as a network port in the Arduino IDE. Select it, click Upload, and the IDE sends the firmware over Wi-Fi.</p>
<div class="code-block"><div class="code-bar"><span>ota_arduino.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;ArduinoOTA.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nIP: " + WiFi.localIP().toString());

  ArduinoOTA.setHostname("esp32-sensor");    // appears as this in IDE
  ArduinoOTA.setPassword("ota-password");    // optional but recommended

  ArduinoOTA.onStart([]() {
    String type = (ArduinoOTA.getCommand() == U_FLASH) ? "firmware" : "filesystem";
    Serial.println("OTA start: " + type);
  });
  ArduinoOTA.onEnd([]()   { Serial.println("\nOTA done — rebooting"); });
  ArduinoOTA.onError([](ota_error_t e) {
    Serial.printf("OTA error[%u]: ", e);
    if      (e == OTA_AUTH_ERROR)    Serial.println("Auth failed");
    else if (e == OTA_BEGIN_ERROR)   Serial.println("Begin failed");
    else if (e == OTA_CONNECT_ERROR) Serial.println("Connect failed");
    else if (e == OTA_RECEIVE_ERROR) Serial.println("Receive failed");
    else if (e == OTA_END_ERROR)     Serial.println("End failed");
  });
  ArduinoOTA.onProgress([](unsigned int prog, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (prog / (total / 100)));
  });

  ArduinoOTA.begin();
  Serial.println("ArduinoOTA ready — select 'esp32-sensor' in IDE > Tools > Port");
}

void loop() {
  ArduinoOTA.handle();   // must call every loop — checks for incoming update
  // your application code here
}</pre></div>

<h2>Method 2 — Web Browser OTA (Upload .bin via HTML Form)</h2>
<p>No Arduino IDE required — upload firmware from any web browser by browsing to the ESP32's IP and selecting the .bin file.</p>
<div class="code-block"><div class="code-bar"><span>ota_web.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;AsyncTCP.h&gt;
#include &lt;ESPAsyncWebServer.h&gt;
#include &lt;Update.h&gt;

const char* ssid     = "YourSSID";
const char* password = "YourPassword";
AsyncWebServer server(80);

const char OTA_PAGE[] PROGMEM = R"(
&lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;&lt;title&gt;OTA Update&lt;/title&gt;&lt;/head&gt;&lt;body&gt;
&lt;h1&gt;OTA Firmware Update&lt;/h1&gt;
&lt;form method='POST' action='/update' enctype='multipart/form-data'&gt;
  &lt;input type='file' name='firmware' accept='.bin'&gt;
  &lt;input type='submit' value='Update'&gt;
&lt;/form&gt;
&lt;/body&gt;&lt;/html&gt;
)";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nIP: " + WiFi.localIP().toString());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
    req->send_P(200, "text/html", OTA_PAGE);
  });

  server.on("/update", HTTP_POST,
    [](AsyncWebServerRequest* req) {
      bool ok = !Update.hasError();
      AsyncWebServerResponse* response = req->beginResponse(
        200, "text/plain", ok ? "Update OK — rebooting" : "Update FAILED");
      response->addHeader("Connection", "close");
      req->send(response);
      if (ok) ESP.restart();
    },
    [](AsyncWebServerRequest* req, String filename, size_t index,
       uint8_t* data, size_t len, bool final) {
      if (!index) {
        Serial.printf("OTA start: %s\n", filename.c_str());
        if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
          Update.printError(Serial);
        }
      }
      if (Update.write(data, len) != len) Update.printError(Serial);
      if (final) {
        if (Update.end(true)) {
          Serial.printf("OTA complete: %u bytes\n", index + len);
        } else {
          Update.printError(Serial);
        }
      }
    }
  );

  server.begin();
  Serial.println("Web OTA server ready at http://" + WiFi.localIP().toString());
}

void loop() {}</pre></div>

<h2>Method 3 — Automatic OTA from HTTP Server</h2>
<p>The ESP32 periodically checks a version file on your server and downloads the firmware binary if a newer version is available:</p>
<div class="code-block"><div class="code-bar"><span>ota_auto.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;WiFi.h&gt;
#include &lt;HTTPClient.h&gt;
#include &lt;Update.h&gt;

#define CURRENT_VERSION "1.0.2"
#define VERSION_URL     "http://your-server.com/esp32/version.txt"
#define FIRMWARE_URL    "http://your-server.com/esp32/firmware.bin"

void checkForUpdate() {
  HTTPClient http;
  http.begin(VERSION_URL);
  if (http.GET() == HTTP_CODE_OK) {
    String latest = http.getString();
    latest.trim();
    if (latest != CURRENT_VERSION) {
      Serial.printf("New version %s available (have %s) — downloading\n",
        latest.c_str(), CURRENT_VERSION);
      downloadAndApply();
    } else {
      Serial.println("Firmware up to date: " + String(CURRENT_VERSION));
    }
  }
  http.end();
}

void downloadAndApply() {
  HTTPClient http;
  http.begin(FIRMWARE_URL);
  int code = http.GET();
  if (code == HTTP_CODE_OK) {
    int total = http.getSize();
    if (!Update.begin(total &gt; 0 ? total : UPDATE_SIZE_UNKNOWN)) {
      Update.printError(Serial); return;
    }
    WiFiClient* stream = http.getStreamPtr();
    size_t written = Update.writeStream(*stream);
    if (Update.end()) {
      Serial.printf("Updated: %u bytes — rebooting\n", written);
      ESP.restart();
    } else {
      Update.printError(Serial);
    }
  }
  http.end();
}

void loop() {
  static unsigned long last = 0;
  if (millis() - last &gt;= 3600000) {   // check every hour
    last = millis();
    checkForUpdate();
  }
  // your application code
}</pre></div>

<h2>Partition Scheme for OTA</h2>
<p>OTA requires the correct partition scheme. In Arduino IDE: Tools → Partition Scheme → select one with "OTA" in the name (e.g. "Default with OTA (1.3 MB APP / 1.5 MB SPIFFS)").</p>

<h2>Rollback Safety Pattern</h2>
<div class="code-block"><div class="code-bar"><span>ota_rollback.ino</span><button class="copy-btn" type="button">Copy</button></div>
<pre>#include &lt;esp_ota_ops.h&gt;

// In setup(), after all hardware initialised successfully:
esp_ota_img_states_t state;
const esp_partition_t* running = esp_ota_get_running_partition();
if (esp_ota_get_state_partition(running, &state) == ESP_OK) {
  if (state == ESP_OTA_IMG_PENDING_VERIFY) {
    // Mark this boot as valid — do NOT call this if something is wrong
    esp_ota_mark_app_valid_cancel_rollback();
    Serial.println("OTA: firmware marked as valid");
  }
}
// If setup() crashes before reaching this line, the watchdog timer
// triggers a reboot and the bootloader rolls back to the previous image.</pre></div>
HTML
],

];
