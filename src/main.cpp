#include <Arduino.h>
#include <ezButton.h>

// khai bao chan cua sensor
const int start = 18; const int stop = 19;
int startstate; int stopstate;
// tao instance cho sensor
ezButton startbtn(18);
ezButton stopbtn(19);

int timer() {
  // lay thoi gian dau theo ms
  int64_t starttime = millis();
  Serial.print("Timer started! ");
  // cho diem ket thuc duoc kich hoat
  while (true) {
    stopbtn.loop();
    if (stopbtn.isPressed()) break;
  }
  // ket thuc
  Serial.println("Timer ended!");
  // lay thoi gian ket thuc theo ms
  int64_t stoptime = millis();
  // tinh chenh lech thoi gian
  int64_t difftime = stoptime - starttime;
  // in thong tin ra serial
  Serial.print("Start time: "); Serial.print(starttime); Serial.print("(ms) ");
  Serial.print("Stop time: "); Serial.print(stoptime); Serial.print("(ms) ");
  Serial.print("Time difference: "); Serial.print(difftime);Serial.println("(ms)");
  return 1;
}

void setup() {
  // put your setup code here, to run once:
  // setup giao thuc serial
  Serial.begin(115200);
}

void loop() {
  // loop
  startbtn.loop();
  // chay ham timer khi diem 1 duoc kich hoat
  if (startbtn.isPressed()) timer();
  delay(10); // this speeds up the simulation
}
