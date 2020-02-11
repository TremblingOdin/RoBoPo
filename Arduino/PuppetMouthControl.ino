/*
  Activating a servo based on the TX/RX signal
  by Kayvan Ehteshami (TremblingTitan/TremblingOdin)
  
  modified on 2/8/2020 (February 2nd)
*/

#include <Servo.h>

Servo mouth; //the puppet's mouth servo

int servoPin;
const int rxPin = 0;
const int txPin = 1;

int flap = 0; //Global mouth flap boolean
int posOpen = 50; //The location of an open flap
int posClosed = 0; //The location of a closed flap

void setup() {
  Serial.begin(9600); //The Baudrate for the serial
  
  servoPin = 6; //This number has to be a PWM pin  
  mouth.attach(servoPin); 
  mouth.write(posClosed);
}

void loop() {
  if(Serial.available()) {
    flap = Serial.read();
    
    if(flap) {
      mouth.write(posOpen);
    }
    else {
      mouth.write(posClosed);
    }
  }
}
