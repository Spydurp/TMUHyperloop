#include "Timer.h"

int sensor = 9;
double d = 0.1;
double circum = 3.14159265*d;
Timer timer(MILLIS);
unsigned int elapsedTime=0;
int counter;
double vel;
double RPM = 0;

void setup(){
  Serial.begin(9600);
  pinMode(9, INPUT);
  timer.start();
}

void loop(){
  unsigned int time = 0;
  

  if(!digitalRead(sensor)){
    counter++;
    Serial.println(counter);
    while(!digitalRead(sensor));
  }
  if(counter >= 24){
    counter = 0;
    time = timer.read() - elapsedTime;
    elapsedTime = timer.read();
    RPM = 1.0/(time/1000.0);
    vel = (double) circum*RPM;

    Serial.print("Velocity: ");
    Serial.println(vel);
    Serial.print("RPM: ");
    Serial.println(RPM);
    Serial.print("Time: ");
    Serial.println(time);
  }

}
