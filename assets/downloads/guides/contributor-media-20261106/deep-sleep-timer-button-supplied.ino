#include <Arduino.h>
#include <esp_sleep.h>
#include <driver/rtc_io.h>

constexpr gpio_num_t WAKE_PIN = GPIO_NUM_33;
RTC_DATA_ATTR uint32_t bootCount = 0;

void setup() {
  Serial.begin(115200);
  ++bootCount;
  const esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();
  Serial.printf("RTC boot count: %lu, wake cause: %d\n",
                (unsigned long)bootCount, int(cause));
  // EXT0 leaves this pad in RTC mode. Restore digital GPIO before reading.
  rtc_gpio_deinit(WAKE_PIN);
  pinMode(int(WAKE_PIN), INPUT); // External 10 kOhm pull-up, not INPUT_PULLUP.
  delay(100); // Short, bounded awake window for Serial output.
  if (esp_sleep_enable_timer_wakeup(10ULL * 1000000ULL) != ESP_OK) {
    Serial.println("Timer setup failed; remain awake."); return;
  }
  if (digitalRead(int(WAKE_PIN)) == HIGH) {
    if (esp_sleep_enable_ext0_wakeup(WAKE_PIN, 0) != ESP_OK) {
      Serial.println("EXT0 setup failed; remain awake."); return;
    }
    Serial.println("Timer or button LOW can wake this classic ESP32.");
  } else {
    Serial.println("Button held LOW: timer only this cycle; release it.");
  }
  Serial.println("Entering deep sleep; setup runs again after wake.");
  Serial.flush();
  esp_deep_sleep_start();
}
void loop() { delay(100); } // Reached only if setup returned on an error.