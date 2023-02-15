#include <Arduino.h>
#include <ezButton.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);

// custom char - delta 
byte customChar[] = {B00000,B00000,B00100,B01110,B11111,B11111,B11111,B00000};

// khai bao bien chua che do do
int mode = 0;
// khai bao chan cua sensor
const int start = 18; const int stop = 19; const int b1 = 23;
int startstate; int stopstate; int b1state;
// tao instance cho sensor
ezButton startbtn(start);
ezButton stopbtn(stop);
ezButton b1btn(b1);

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
        printlcd(3, 0, "A->B", false);
        break;
      case 1:  
        printlcd(3, 0, "T   ", false);
        break;
      default:
        break;
    }
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
  if (b1btn.isPressed()) {
    mode = !(mode);
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
      case 1:
        t_timer();
        break;
      default:
        break;
    }
  }
  // delay(10); // this speeds up the simulation
}
