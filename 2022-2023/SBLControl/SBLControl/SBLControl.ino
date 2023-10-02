#include <SoftwareSerial.h>
const byte rxPin = 8;
const byte txPin = 9;

SoftwareSerial mySerial = SoftwareSerial(rxPin, txPin);
String input = "";
String command = "";
String val = "";
String output = "";

void setup() {
  // put your setup code here, to run once:
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  mySerial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  mySerial.print(output);

  if(Serial.available() != 0){
    input = Serial.readString();
    int dump = sscanf(input.c_str(), "%s,%s", &command, &val);

  }
  if(command.equalsIgnoreCase("go")){
    output = "!G 1 " + val + "_";
    Serial.println(output);
  }
  mySerial.print(output);

}
