#include <WiFi.h>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>

const char* SSID = "your wifi name";
const char* PASSWORD = "your wifi password";
constexpr uint32_t ATTEMPT_MS = 20000, RETRY_MS = 5000;
constexpr uint8_t MAX_ATTEMPTS = 3;
struct Event { WiFiEvent_t id; uint16_t reason; };
QueueHandle_t events;
bool ready = false, trying = false, paused = false, wasConnected = false;
uint8_t attempts = 0;
uint32_t started = 0, lastEnded = 0, lastStats = 0;

void onWiFi(WiFiEvent_t id, WiFiEventInfo_t info) {
  Event e{id, 0};
  if (id == ARDUINO_EVENT_WIFI_STA_DISCONNECTED)
    e.reason = info.wifi_sta_disconnected.reason;
  xQueueSend(events, &e, 0); // Callback task: copy only; never wait here.
}
void startAttempt() {
  ++attempts;
  started = millis(); trying = true;
  Serial.printf("Wi-Fi attempt %u/%u\n", attempts, MAX_ATTEMPTS);
  WiFi.begin(SSID, PASSWORD); // Starts connection; no waiting loop.
}
void setup() {
  Serial.begin(115200);
  events = xQueueCreate(12, sizeof(Event));
  if (!events || !WiFi.mode(WIFI_STA)) {
    Serial.println("Queue/Wi-Fi initialization failed; reset after checking board.");
    return;
  }
  WiFi.setAutoReconnect(false); // This sketch owns the bounded retry policy.
  WiFi.onEvent(onWiFi);
  ready = true;
  startAttempt();
}
void loop() {
  if (!ready) { delay(10); return; }
  const uint32_t now = millis();
  Event e;
  while (xQueueReceive(events, &e, 0) == pdTRUE) {
    if (e.id == ARDUINO_EVENT_WIFI_STA_CONNECTED)
      Serial.println("Associated with AP; still waiting for an IP address.");
    if (e.id == ARDUINO_EVENT_WIFI_STA_GOT_IP)
      Serial.println("GOT_IP: IP networking can start.");
    if (e.id == ARDUINO_EVENT_WIFI_STA_DISCONNECTED)
      Serial.printf("Disconnected: reason=%u (see version-matched Wi-Fi reference)\n", e.reason);
  }
  const bool connected = WiFi.status() == WL_CONNECTED;
  if (connected) {
    trying = false; attempts = 0; paused = false;
    if (!wasConnected || now - lastStats >= 10000) {
      lastStats = now;
      Serial.print("IP: "); Serial.println(WiFi.localIP());
      Serial.print("Gateway: "); Serial.println(WiFi.gatewayIP());
      Serial.print("DNS: "); Serial.println(WiFi.dnsIP());
      Serial.printf("Channel: %d, RSSI: %d dBm\n", WiFi.channel(), WiFi.RSSI());
    }
  } else {
    if (wasConnected) lastEnded = now;
    if (trying && now - started >= ATTEMPT_MS) {
      WiFi.disconnect(false); trying = false; lastEnded = now;
      Serial.println("20-second connection window ended.");
    }
    if (!trying && attempts < MAX_ATTEMPTS && now - lastEnded >= RETRY_MS)
      startAttempt();
    if (!trying && attempts >= MAX_ATTEMPTS && !paused) {
      paused = true;
      Serial.println("Retries paused. Correct network settings; send r to retry.");
    }
  }
  wasConnected = connected;
  if (Serial.available() && Serial.read() == 'r' && !connected) {
    WiFi.disconnect(false); attempts = 0; paused = false; trying = false;
    lastEnded = now - RETRY_MS;
  }
  delay(10); // Yield without an endless connection wait.
}