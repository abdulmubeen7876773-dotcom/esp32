#include <WiFi.h>
#include <ArduinoOTA.h>
const char* SSID = "change_with_your_wifi_SSID";
const char* PASSWORD = "change_with_your_wifi_password";
const char* OTA_PASSWORD = "change_password_ota";
const char* BUILD_ID = "usb-baseline-1"; // Change to ota-test-2 for the next upload.
constexpr uint32_t WINDOW_MS = 20000, RETRY_MS = 30000;
bool trying = false, otaReady = false;
uint32_t attemptAt = 0;
void startWiFi() {
  attemptAt = millis(); trying = true;
  WiFi.begin(SSID, PASSWORD);
  Serial.println("Starting bounded Wi-Fi window");
}
void setup() {
  Serial.begin(115200);
  Serial.print("Build: "); Serial.println(BUILD_ID);
  WiFi.mode(WIFI_STA); WiFi.setAutoReconnect(false);
  ArduinoOTA.setHostname("esp32-ota-lab"); // Use a different name per board.
  ArduinoOTA.setPassword(OTA_PASSWORD);
  ArduinoOTA.onStart([]() { Serial.println("OTA starting; keep power on"); });
  ArduinoOTA.onEnd([]() { Serial.println("OTA transfer finished"); });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA error code: %u\n", unsigned(error));
  });
  startWiFi();
}
void loop() {
  const uint32_t now = millis();
  if (WiFi.status() == WL_CONNECTED) {
    trying = false;
    if (!otaReady) {
      ArduinoOTA.begin(); otaReady = true;
      Serial.print("OTA host esp32-ota-lab, IP: "); Serial.println(WiFi.localIP());
    }
    ArduinoOTA.handle(); // Regular service; transfer processing can block.
  } else {
    if (otaReady) { ArduinoOTA.end(); otaReady = false; }
    if (trying && now - attemptAt >= WINDOW_MS) {
      WiFi.disconnect(false); trying = false;
      Serial.println("Wi-Fi window expired; USB recovery remains available");
    }
    if (!trying && now - attemptAt >= RETRY_MS) startWiFi();
  }
  delay(2);
}