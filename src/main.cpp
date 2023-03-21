#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#ifdef __cplusplus
#include <atomic>
#include <ezButton.h>
using namespace std;
#else
#include <stdatomic.h>
#endif

LiquidCrystal_I2C lcd(0x27,20,4);

// custom char - delta 
byte customChar[] = {B00000,B00000,B00100,B01110,B11111,B11111,B11111,B00000};

// khai bao bien chua che do do
int mode = 0;
// khai bao chan cua sensor
const int start = 18; const int stop = 19; const int b1 = 23; const int d_start = 5;
int startstate; int stopstate; int b1state;
// tao instance cho sensor
ezButton startbtn(start);
ezButton stopbtn(stop);
ezButton b1btn(b1);
ezButton d_startbtn(d_start);

// che do do dong thoi a va b - dl 3 newton
// pointer den tien trinh chay khong dong bo
TaskHandle_t t1;
TaskHandle_t t2;
// bien dung thu vien atomic dung de cap nhat thong
// tin trong tien trinh khac tien trinh main loop
atomic<int> data1; 
atomic<int> data2; 

// ham do thoi gian vat chan cong
void tracker1(void * pvParameters) {
  long long int start, stop;
  while (true) {
    startbtn.loop();
    if (startbtn.isPressed()) {
      start = millis();
      while (true){
        startbtn.loop();
        if (startbtn.isReleased()) break;
      }
      stop = millis();
      break;
    }
  }
  long long int diff = stop - start;
  data1.store(diff);
  vTaskDelete(NULL);
}

void tracker2(void * pvParameters) {
  long long int start, stop;
  while (true) {
    stopbtn.loop();
    if (stopbtn.isPressed()) {
      start = millis();
      while (true){
        stopbtn.loop();
        if (stopbtn.isReleased()) break;
      }
      stop = millis();
      break;
    }
  }
  long long int diff = stop - start;
  data2.store(diff);
  vTaskDelete(NULL);
}

// ham in ki tu ra lcd
void printlcd(int row, int col, String string, bool clear = false) {
    if (clear) lcd.clear();
    lcd.setCursor(col, row);
    lcd.print(string);
}

// ham tao giao dien homescreen
void initHome(bool isClear = false) {
  printlcd(0, 0, "Cho tin hieu diem 1!", isClear);
  printlcd(2, 0, "Che do hien tai: ", false);
    switch (mode) {
      case 0:
        printlcd(3, 0, "A->B ", false);
        break;
      case 1:  
        printlcd(3, 0, "A & B", false);
        break;
      case 2:  
        printlcd(3, 0, "T    ", false);
        break;
      default:
        break;
    }
}

int a_b_timer() {
  printlcd(0, 0, "Bat dau nhan lenh!", true);
  printlcd(1, 0, "(A & B)", false);
  xTaskCreatePinnedToCore(tracker1, "t1", 10000, NULL, 1, &t1, 0);
  xTaskCreatePinnedToCore(tracker2, "t2", 10000, NULL, 1, &t2, 1);
  long long int prev1 = data1.load(), prev2 = data2.load();
  while (true) {
    if ((prev1 != data1.load()) && (prev2 != data2.load())) {
      printlcd(0, 0, "Ket thuc do!", true);
      printlcd(1, 0, "t1: "); printlcd(1, 4, String(data1.load()));
      printlcd(2, 0, "t2: "); printlcd(2, 4, String(data2.load()));
      Serial.print("0;"); 
      Serial.print(data1.load()); Serial.print(";");
      Serial.print(data2.load()); Serial.print(";");
      Serial.println("a&b;");
      break;
    }
  }
  // delay xem kq
  while (true) {
    b1btn.loop();
    if (b1btn.isPressed()) {
      delay(250);
      break;
    }
  }
  initHome(true);
  return 1;
}

// do thoi gian di tu a->b
int ab_timer() {
  // lay thoi gian dau theo ms
  unsigned long int starttime = millis();
  printlcd(0, 0, "Bat dau do!", true);
  // cho diem ket thuc duoc kich hoat
  while (true) {
    b1btn.loop();
    stopbtn.loop();
    if (stopbtn.isPressed()) break;
    else if (b1btn.isPressed()) return 0;
  }
  // lay thoi gian ket thuc theo ms
  unsigned long int stoptime = millis();
  // ket thuc
  printlcd(0, 0, "Ket thuc do (A->B)", true);
  // tinh chenh lech thoi gian
  unsigned long int difftime = stoptime - starttime;
  // in thong tin ra serial + lcd
  // String start = "t1 = " + String(starttime) + "(ms)"; printlcd(1, 0, start, false);
  Serial.print(starttime); Serial.print(";");
  // String stop = "t2 = " + String(stoptime) + "(ms)"; printlcd(2, 0, stop, false);
  Serial.print(stoptime); Serial.print(";");
  String diff = "t = " + String(difftime) + "(ms)"; 
  lcd.createChar(0, customChar); lcd.setCursor(0, 1); lcd.write(0);
  printlcd(1, 1, diff, false);
  Serial.print(difftime);Serial.print(";");
  Serial.println("ab;");
  // delay xem kq
  while (true) {
    b1btn.loop();
    if (b1btn.isPressed()) {
      delay(250);
      break;
    }
  }
  initHome(true);
  return 1;
}

// do thoi gian mot vat di tu cong quang va thoat khoi cong quang
int t_timer() {
  // lay thoi gian dau theo ms
  unsigned long int starttime = millis();
  printlcd(0, 0, "Bat dau do (T)", true);
  while (true) {
    b1btn.loop();
    startbtn.loop();
    if (startbtn.isReleased()) break;
    else if (b1btn.isPressed()) return 0;
  }
  // lay thoi gian ket thuc theo ms
  unsigned long int stoptime = millis();
  // ket thuc
  printlcd(0, 0, "Ket thuc do (T)", true);
  // tinh chenh lech thoi gian
  unsigned long int difftime = stoptime - starttime;
  // in thong tin ra serial + lcd
  // String start = "t1 = " + String(starttime) + "(ms)"; printlcd(1, 0, start, false);
  Serial.print(starttime); Serial.print(";");
  // String stop = "t2 = " + String(stoptime) + "(ms)"; printlcd(2, 0, stop, false);
  Serial.print(stoptime); Serial.print(";");
  String diff = "t = " + String(difftime) + "(ms)"; 
  lcd.createChar(0, customChar); lcd.setCursor(0, 1); lcd.write(0);
  printlcd(1, 1, diff, false);
  Serial.print(difftime);Serial.print(";");
  Serial.println("t;");
  // delay xem kq
  while (true) {
    b1btn.loop();
    if (b1btn.isPressed()) {
      delay(250);
      break;
    }
  }
  initHome(true);
  return 1;
}

void setup() {
  // put your setup code here, to run once:
  // setup giao thuc serial
  Serial.begin(9600);
  // init man hinh + bat den nen
  lcd.init();
  lcd.backlight();
  printlcd(0, 0, "Cho tin hieu diem 1!", true);
  printlcd(2, 0, "Che do hien tai: ", false);
  printlcd(3, 0, "A->B", false);
}

void loop() {
  // loop
  startbtn.loop();
  b1btn.loop();
  d_startbtn.loop();
  if (b1btn.isPressed()) {
    mode = (mode + 1 == 3) ? 0 : mode+1;
    delay(250);
    // in ra man hinh che do hien tai
    initHome();
  }
  // kich hoat che do do tuong ung khi startbtn duoc kich hoat
  if (startbtn.isPressed()) {
    switch (mode) {
      case 0:
        ab_timer();
        break;
      case 2:
        t_timer();
        break;
      default:
        break;
    }
  } else if (d_startbtn.isPressed() && mode == 1) a_b_timer();
  delay(10); // this speeds up the simulation
}
