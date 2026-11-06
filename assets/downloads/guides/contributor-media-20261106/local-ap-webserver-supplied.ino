#include <WiFi.h>
#include <WebServer.h>

const char* AP_SSID = "ESP32-Lab";
const char* AP_PASSWORD = "12345678"; // Replace with your own 8-63 character passphrase.
WebServer server(80);
bool ready = false;

void setup() {
  Serial.begin(115200);
  if (!WiFi.mode(WIFI_AP) || !WiFi.softAP(AP_SSID, AP_PASSWORD, 6)) {
    Serial.println("AP start failed; check board and passphrase length, then reset.");
    return;
  }
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html; charset=utf-8",
      "<!DOCTYPE html><html lang='en'><meta name='viewport' content='width=device-width,initial-scale=1'>"
      "<title>ESP32 Lab</title><h1>ESP32 local server</h1>"
      "<p>This page came from the board.</p><p><a href='/uptime'>Read uptime</a></p></html>");
  });
  server.on("/uptime", HTTP_GET, []() {
    server.send(200, "text/plain", String(millis()) + " ms since reset\n");
  });
  server.onNotFound([]() { server.send(404, "text/plain", "No such route\n"); });
  server.begin(); ready = true;
  Serial.print("Join "); Serial.println(AP_SSID);
  Serial.print("Open http://"); Serial.println(WiFi.softAPIP());
}
void loop() {
  if (ready) server.handleClient();
  delay(2);
}