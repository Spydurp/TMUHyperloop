#include "Timer.h"

int sensor = 9;
double d = 0.1;
double circum = PI*d;
Timer timer(MILLIS);
unsigned int elapsedTime=0;
int counter = 0;
int front = 0;
int back = 23;
double vel;
double RPM;
double time = 0;

void setup(){
  Serial.begin(9600);
  pinMode(9, INPUT);
  timer.start();
}

void loop(){

  if(!digitalRead(sensor)){
    counter++;
    while(!digitalRead(sensor));
  }

  // Count seconds since last vel update
  // Calculate Velocity
  // time = time since last vel update
  time = timer.read() - elapsedTime; // elapsedTime = time of last vel update
  if(time >= 500){
    RPM = (double)(15.0*counter/360)/(time/1000.0);
    vel = (double) circum*RPM;
    elapsedTime = timer.read();   // Update time of last velocity reading
    counter = 0;
  }

  Serial.print(vel);
  Serial.print(",");
  Serial.print(RPM);
  Serial.println("");
  // Add delay if necessary
}
