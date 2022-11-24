
 #include <LiquidCrystal_I2C.h>
// //define I2C address......
LiquidCrystal_I2C lcd(0x27,16,2);
String incomingByte ;    
int i;
void setup() {
  i = 0;
   Serial.begin(9600);
  //pinMode(LED_BUILTIN, OUTPUT);

   // initialize the LCD
   lcd.init();

  // Turn on the blacklight and print a message.
   lcd.backlight();
  //lcd.print("Hello, world!");
}

void loop() {

  if (Serial.available() > 0) {

  incomingByte = Serial.readString(); //read incoming data
  lcd.clear();
   
  while(incomingByte[i] != NULL){
    lcd.print(incomingByte[i]); //printing character by character by cahracter
    i = i + 1;
  }
i = 0;
   
 // lcd.setCursor(0, 0);
  //lcd.print(incomingByte);
  delay(1000);
  lcd.clear();
  lcd.print("x"); //print a value to check transission
  delay(1000);

  //Serial.write(incomingByte);

   
  }

}
