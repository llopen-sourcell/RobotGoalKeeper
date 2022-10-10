#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(115200);
 Serial.setTimeout(1);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}


void loop() {
 while (!Serial.available());
 pos = Serial.readString().toInt();
 myservo.write(pos);
}
