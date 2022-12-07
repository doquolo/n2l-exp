#include <Arduino.h>
#include <ezButton.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);

// custom char - delta 
byte customChar[] = {B00000,B00000,B00100,B01110,B11111,B11111,B11111,B00000};

// khai bao chan cua sensor
const int start = 18; const int stop = 19; const int b1 = 23;
int startstate; int stopstate; int b1state;
// tao instance cho sensor
ezButton startbtn(start);
ezButton stopbtn(stop);
ezButton b1btn(b1);

void printlcd(int row, int col, String string, bool clear = false) {
    if (clear) lcd.clear();
    lcd.setCursor(col, row);
    lcd.print(string);
}

int timer() {
  // lay thoi gian dau theo ms
  unsigned long int starttime = millis();
  printlcd(0, 0, "Bat dau do!", true);
  Serial.print("Timer started! ");
  // cho diem ket thuc duoc kich hoat
  while (true) {
    stopbtn.loop();
    if (stopbtn.isPressed()) break;
  }
  // ket thuc
  printlcd(0, 0, "Ket thuc do!", true);
  Serial.println("Timer ended!");
  // lay thoi gian ket thuc theo ms
  unsigned long int stoptime = millis();
  // tinh chenh lech thoi gian
  unsigned long int difftime = stoptime - starttime;
  // in thong tin ra serial + lcd
  String start = "t1 = " + String(starttime) + "(ms)"; printlcd(1, 0, start, false);
  Serial.print("Start time: "); Serial.print(starttime); Serial.print("(ms) ");
  String stop = "t2 = " + String(stoptime) + "(ms)"; printlcd(2, 0, stop, false);
  Serial.print("Stop time: "); Serial.print(stoptime); Serial.print("(ms) ");
  String diff = "t = " + String(difftime) + "(ms)"; 
  lcd.createChar(0, customChar); lcd.setCursor(0, 3); lcd.write(0);
  printlcd(3, 1, diff, false);
  Serial.print("Time difference: "); Serial.print(difftime);Serial.println("(ms)");
  Serial.println("Bam nut bat ki de ket thuc phien do!");
  // delay xem kq
  while (true) {
    b1btn.loop();
    if (b1btn.isPressed()) break;
  }
  printlcd(0, 0, "Cho tin hieu diem 1!", true);
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
}

void loop() {
  // loop
  startbtn.loop();
  // in ra man hinh
  // chay ham timer khi diem 1 duoc kich hoat
  if (startbtn.isPressed()) timer();
  delay(10); // this speeds up the simulation
}
