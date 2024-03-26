#include <AM2302-Sensor.h>


AM2302::AM2302_Sensor am2302{2};


void setup() {
  Serial.begin(9600);
  am2302.begin();
}


void loop() {

  Serial.println(am2302.get_Temperature());


  delay(500); // Wait for 2 seconds before the next reading
}
