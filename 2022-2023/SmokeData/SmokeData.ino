#include <SPI.h>
#include <SD.h>
#define MQ2pin 0

File myFile;
float sensorValue;

// change this to match your SD shield or module;
const int chipSelect = 10;

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }


  Serial.print("Initializing SD card...");

  if (!SD.begin()) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  myFile = SD.open("Smoke.txt", FILE_WRITE);

  

  // if the file opened okay, write to it:
  if (myFile) {
    for(int i = 0; i < 100; i++){
      sensorValue = analogRead(MQ2pin);
      Serial.println(sensorValue);
      myFile.println(sensorValue);
      delay(100);
    }
    
    // close the file:
    myFile.close();
    Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening SmokeData.txt");
  }


}

void loop()
{
  // nothing happens after setup
}
