#include <SD.h>
#include <SPI.h>
#include <string.h>
//#include <SoftwareSerial.h>

File dataFile;
String id = "M";

//SoftwareSerial Test (15,14);
const int chipSelect = 10;

void write(int data[]){
    if(SD.begin()){
      dataFile = SD.open("dOut.txt", FILE_WRITE);
      for(int i = 0; i < sizeof(data)/sizeof(int); i++){
        dataFile.print(String(data[i]) + ",");
      }
      dataFile.close(); 
      Serial.println("Success");
    }else{
      Serial.println("Error");
    }
    
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Test.begin(9600);
  int data[1] = {73357};  
  for(int i = 0; i < 100; i++){
    write(data);
  }
 
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
}