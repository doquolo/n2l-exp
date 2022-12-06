#include <Arduino.h>
#include <ezButton.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);

// custom char - delta 
byte customChar[] = {B00000,B00000,B00100,B01110,B11111,B11111,B11111,B00000};

// khai bao chan cua sensor
const int start = 18; const int stop = 19;
int startstate; int stopstate;
// tao instance cho sensor
ezButton startbtn(18);
ezButton stopbtn(19);

void printlcd(int row, int col, String string, bool clear = false) {
    if (clear) lcd.clear();
    lcd.setCursor(col, row);
    lcd.print(string);
}

int timer() {
  // lay thoi gian dau theo ms
  long int starttime = millis();
  printlcd(0, 0, "Bat dau dem!", true);
  Serial.print("Timer started! ");
  // cho diem ket thuc duoc kich hoat
  while (true) {
    stopbtn.loop();
    if (stopbtn.isPressed()) break;
  }
  // ket thuc
  printlcd(0, 0, "Ket thuc dem!", true);
  Serial.println("Timer ended!");
  // lay thoi gian ket thuc theo ms
  long int stoptime = millis();
  // tinh chenh lech thoi gian
  long int difftime = stoptime - starttime;
  // in thong tin ra serial + lcd
  String start = "t1 = " + String(starttime) + "(ms)"; printlcd(1, 0, start, false);
  Serial.print("Start time: "); Serial.print(starttime); Serial.print("(ms) ");
  String stop = "t2 = " + String(stoptime) + "(ms)"; printlcd(2, 0, stop, false);
  Serial.print("Stop time: "); Serial.print(stoptime); Serial.print("(ms) ");
  String diff = "t = " + String(difftime) + "(ms)"; 
  lcd.createChar(0, customChar); lcd.setCursor(0, 3); lcd.write(0);
  printlcd(3, 1, diff, false);
  Serial.print("Time difference: "); Serial.print(difftime);Serial.println("(ms)");
  delay(5000);
  printlcd(0, 0, "Cho tin hieu diem 1!", true);
  return 1;
}

void setup() {
  // put your setup code here, to run once:
  // setup giao thuc serial
  Serial.begin(115200);
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
