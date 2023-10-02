#include <Adafruit_MPU6050.h>
#include <Wire.h>
#include <Vector.h>
#include <KalmanFilter.h>
#include <SPI.h>
#include <SD.h>

// ______CONSTANTS______________________________________________________________________________
//_________Accelerometer declarations____________
MPU6050 mpu;

KalmanFilter kalmanX(0.001, 0.003, 0.03);
KalmanFilter kalmanY(0.001, 0.003, 0.03);

float accPitch = 0;
float accRoll = 0;

float kalPitch = 0;
float kalRoll = 0;

//__________Voltmeter declarations___________
int volt1pin = 0;
int volt2pin = 1;
int volt3pin = 2;

volatile float volt1;
volatile float volt2;
volatile float volt3;

//_________Current meter declarations___________
int cur1pin = 3;
int cur2pin = 4;
int cur3pin = 5;

//__________Tachometer IR Sensor Declarations________________
// I2C Slave Address of the Slave Arduino
#define PI 3.1415926535897932384626433832795
const int slaveAddress = 9;
const float wheelRad = 0.13; // Meters
const float deg = 15; 
const float arc = 15*(PI/180) * wheelRad;

// __________Relay declarations____________________
int relayPin = 7;

//_________________Nominal values________________________
const float nominal_min_voltage = 8;
const float nominal_max_voltage = 11;

const float trackDistance = 100; // Meters
const float safeStoppingDistance;

const float maxCurrent = 20; // Amps

const float track_maxTemp = 70; //Degrees celcius

const float maxAccel = 50; // m/s2
const float targetVelocity;


//________SDWrite declarations______________
File dataFile;

//_______Control Signal Declarations________
bool startSignal;


// ______FUNCTIONS______________________________________________________________________________________

//_______State_________
// Returns true if all values are nominal.
// Returns false otherwise
bool checkState(float volts[], float currents[], float temp, Vector<float> acc){
  if(temp > track_maxTemp || acc.XAxis > maxAccel || acc.YAxis > maxAccel || acc.ZAxis > maxAccel){
    return false;
  }
  for(int i = 0; i < 4; i++){
    if(volts[i] < nominal_min_voltage || volts[i] > nominal_max_voltage || currents[i] > maxCurrent){
      return false;
    }
  }
  return true;
}

//________Relay functions_________
void setRelay(bool x){
  
  if (x==true){ //Close relay
    analogWrite(relayPin, HIGH);
  }
  else{ //Open relay
    analogWrite(relayPin, LOW);
  }
}
//void closeRelay(float volt1){
//  
//}


//________Accelerometer function_________
Vector<float> getAccel(){
  Vector<float> acc = mpu.readNormalizeAccel();
  Vector<float> gyr = mpu.readNormalizeGyro();

  // Calculate Pitch & Roll from accelerometer (deg)
  accPitch = -(atan2(acc.XAxis, sqrt(acc.YAxis*acc.YAxis + acc.ZAxis*acc.ZAxis))*180.0)/M_PI;
  accRoll  = (atan2(acc.YAxis, acc.ZAxis)*180.0)/M_PI;

  // Kalman filter
  kalPitch = kalmanY.update(accPitch, gyr.YAxis);
  kalRoll = kalmanX.update(accRoll, gyr.XAxis);

  Serial.print("acc.XAxis: ");
  Serial.println(acc.XAxis);
  Serial.print("acc.YAxis: ");
  Serial.println(acc.YAxis);
  Serial.print("acc.ZAxis: ");
  Serial.println(acc.ZAxis);

  return acc;
}


//________Voltage function_________
float* getVolt(){
  volt1 = (analogRead(volt1pin) - 512) * 0.073170;
  float volt2 = (analogRead(volt2pin) - 512) * 0.073170;
  float volt3 = (analogRead(volt3pin) - 512) * 0.073170;

  Serial.print("Battery Voltage: ");
  Serial.print(volt1);
  Serial.println(" V");
  //Serial.println(volt2);
  //Serial.println(volt3);
  //Serial.println(volt4);
  
  //temp values
  float volts[3] = {volt1, 0.0, 0.0};
  return volts;
}

//____________Current Function___________
float* getCurrent(){
  float sensor1 = analogRead(cur1pin) * 5.0/1023;
  float sensor2 = analogRead(cur2pin) * 5.0/1023;
  float sensor3 = analogRead(cur3pin) * 5.0/1023;

  float current1 = (sensor1-2.5)/0.066;
  float current2 = (sensor2-2.5)/0.066;
  float current3 = (sensor3-2.5)/0.066;

  Serial.print("Battery Current: ");
  Serial.print(current1);  
  Serial.print(" A, ");
  Serial.print(current2);
  Serial.print(" A, ");
  Serial.print(current3);
  Serial.print(" A\n");

  float currents[3] = {current1, current2, current3};
  return currents;
}

float * getTach() {
  byte dataBytes[sizeof(float) + sizeof(unsigned long)];

  Wire.requestFrom(slaveAddress, sizeof(float) + sizeof(unsigned long));

  if (Wire.available() >= sizeof(float) + sizeof(unsigned long)) {
    for (int i = 0; i < sizeof(float) + sizeof(unsigned long); i++) {
      dataBytes[i] = Wire.read();
    }
  }

  float rpm;
  unsigned long stripeCount;

  // Extract the RPM value from the byte array
  byte* rpmBytes = (byte*)&rpm;
  for (int i = 0; i < sizeof(float); i++) {
    rpmBytes[i] = dataBytes[i];
  }

  // Extract the stripe count value from the byte array
  byte* countBytes = (byte*)&stripeCount;
  for (int i = 0; i < sizeof(unsigned long); i++) {
    countBytes[i] = dataBytes[sizeof(float) + i];
  }
  float distance = stripeCount*arc;
  float vel = rpm*2*PI*wheelRad/60;
  // Print the received RPM and stripe count values
  Serial.print("Speed: ");
  Serial.println(vel, 2);
  Serial.print("Distance: ");
  Serial.println(distance);
  float data[2] = {vel, distance};
  return data;
}

// Writes data to sd card
// Format: [accX,accY,accZ,volt1,volt2,volt3,volt4,speed(m/s),distance(m)]
void write(Vector<float> acc, float volts[], float currents[], float speed, float distance){
  if(SD.begin()){
    dataFile = SD.open("dOut.txt", FILE_WRITE);
    dataFile.print(String(acc.XAxis) + "," + String(acc.YAxis) + "," + String(acc.ZAxis) + ",");
    
    for(int i = 0; i < sizeof(volts)/sizeof(float); i++){
      dataFile.print(String(volts[i]) + ",");
    }
    dataFile.print(String(speed) + "," + String(distance) + "\n");
    dataFile.close();
  }else{
    Serial.println("Write Error");
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //________MPU6050 Accelerometer declaration_____________
  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    delay(500);
    Serial.println("Trying to connect");
  }
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  //________Voltage reading____________
  pinMode(volt1pin, INPUT);
  pinMode(volt2pin, INPUT);
  pinMode(volt3pin, INPUT);

  //________Current Reading__________
  pinMode(cur1pin, INPUT);
  pinMode(cur2pin, INPUT);
  pinMode(cur3pin, INPUT);

  //_________Tachometer____________
  //Wire.begin();

  //________Relay__________
  pinMode(relayPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Vector acc = getAccel();
  delay(500);
  float* volts = getVolt();
  float voltVal[4] = {*(volts+0), *(volts+1), *(volts+2)};
  //getTemp()
  //getCurrents()
  float temp = 0;

  float* current = getCurrents();
  float currents[3] = {*(current+0),*(current+1),*(current+2)};
  delay(500);
  float* SpdDis = getTach();
  float speed = *(SpdDis+0);
  float distance = *(SpdDis+1);
  write(acc, voltVal, currents, speed, distance);
  delay(1000);

  // Control statements
  // If outside nominal range, close relay
//
  bool nominal = checkState(voltVal, currents, temp, acc);
  if(startSignal == true && nominal == true){
    if(distance >= safeStoppingDistance){
    //begin braking
    }
    if(speed <= targetVelocity && distance < safeStoppingDistance){
      //accelerate
    }
    if(speed >= targetVelocity && distance < safeStoppingDistance){
      //maintain velocity
      //
    }
    if(speed == 0 && started == true){
      //start shutdown
      //maintain brakes
      //turn off power
    }
  }
  if(nominal == false){
    //close relays
    //brake
    //turn off all power
    //panic
  }
  

//  if (volt1<nominal_min_voltage || volt1>nominal_max_voltage){
//    bool closeRelay = true;
//    setRelay(closeRelay);
//  }
//  else{
//    bool closeRelay = false;
//    setRelay(closeRelay);
//  }
}
