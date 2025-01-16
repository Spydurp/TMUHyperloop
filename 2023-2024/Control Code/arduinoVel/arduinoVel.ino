#include <arduino-timer.h>

int sensor = 2;
double d = 0.1;
double circum = 3.14159265*d;
auto timer = timer_create_default();
double gapInterval = 15;
int counter = 0;
double vel;
double RPS = 0;

void setup(){
  Serial.begin(9600);
  pinMode(2, INPUT);
  timer.every(1000, velCalc);
}

void loop(){
  timer.tick();
  

  if(!digitalRead(sensor)){
    counter++;
    while(!digitalRead(sensor));
  }


}

bool velCalc(){
  RPS = (counter*15/360)/1;
  vel = (double) circum*RPS;
  counter = 0;
  Serial.print("Velocity: ");
  Serial.println(vel);
}
