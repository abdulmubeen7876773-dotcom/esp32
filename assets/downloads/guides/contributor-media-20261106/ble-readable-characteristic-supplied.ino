#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <atomic>

const char* SERVICE_UUID = "63c80f8e-71b1-4ee8-973e-68e9182b8721";
const char* VALUE_UUID = "88c78480-46d5-4a48-a57c-cb7fc0ea59e1";
BLECharacteristic* value;
std::atomic<bool> disconnected{false};
class Callbacks : public BLEServerCallbacks {
  void onDisconnect(BLEServer*) override { disconnected.store(true); }
};
Callbacks callbacks;

void setup() {
  Serial.begin(115200);
  BLEDevice::init("ESP32-Read-Demo");
  BLEServer* server = BLEDevice::createServer();
  server->setCallbacks(&callbacks);
  BLEService* service = server->createService(SERVICE_UUID);
  value = service->createCharacteristic(VALUE_UUID, BLECharacteristic::PROPERTY_READ);
  value->setValue("uptime_ms=0");
  service->start();
  BLEAdvertising* advertising = BLEDevice::getAdvertising();
  advertising->addServiceUUID(SERVICE_UUID);
  advertising->setScanResponse(true);
  BLEDevice::startAdvertising();
  Serial.println("Scan for ESP32-Read-Demo; connect and read the custom characteristic.");
}
void loop() {
  static uint32_t updated = 0, restartAt = 0;
  static bool restartPending = false;
  const uint32_t now = millis();
  if (disconnected.exchange(false)) { restartAt = now; restartPending = true; }
  if (restartPending && now - restartAt >= 200) {
    BLEDevice::startAdvertising(); restartPending = false;
    Serial.println("Advertising restarted after disconnect.");
  }
  if (now - updated >= 2000) {
    updated = now;
    value->setValue(String("uptime_ms=") + String(now));
  }
  delay(10);
}