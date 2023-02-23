#ifdef __cplusplus
#include <atomic>
#include <ezButton.h>
using namespace std;
#else
#include <stdatomic.h>
#endif


TaskHandle_t t1;
TaskHandle_t t2;

atomic<int> data1; 
atomic<int> data2; 

ezButton bstart(21);
ezButton b1(23);
ezButton b2(22);


void setup() {
  Serial.begin(9600);
  delay(500);
}

void tracker1(void * pvParameters) {
  long long int start, stop;
  while (true) {
    b1.loop();
    if (b1.isPressed()) {
      start = millis();
      Serial.println(start);
      while (true){
        b1.loop();
        if (b1.isReleased()) break;
      }
      stop = millis();
      Serial.println(stop);
      break;
    }
  }
  long long int diff = stop - start;
  Serial.print("time 1 stopped: ");
  Serial.println(diff);
  data1.store(diff);
  vTaskDelete(NULL);
}

void tracker2(void * pvParameters) {
  long long int start, stop;
  while (true) {
    b2.loop();
    if (b2.isPressed()) {
      start = millis();
      Serial.println(start);
      while (true){
        b2.loop();
        if (b2.isReleased()) break;
      }
      stop = millis();
      Serial.println(stop);
      break;
    }
  }
  long long int diff = stop - start;
  Serial.print("time 2 stopped: ");
  Serial.println(diff);
  data2.store(diff);
  vTaskDelete(NULL);
}

void loop() {
  bstart.loop();
  if (bstart.isPressed()) {
    Serial.println("Measuring started!");
    xTaskCreatePinnedToCore(tracker1, "t1", 10000, NULL, 1, &t1, 0);
    xTaskCreatePinnedToCore(tracker2, "t2", 10000, NULL, 1, &t2, 1);
    long long int prev1 = data1.load(), prev2 = data2.load();
    while (true) {
      if ((prev1 != data1.load()) && (prev2 != data2.load())) {
        Serial.println("Measuring finished!");
        Serial.print("Sensor 1: "); Serial.println(data1.load());
        Serial.print("Sensor 2: "); Serial.println(data2.load());
        break;
      }
    }
  }
  delay(10);
}