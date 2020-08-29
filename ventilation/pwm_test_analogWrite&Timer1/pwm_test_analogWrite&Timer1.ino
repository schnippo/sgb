#include <TimerOne.h>


int Pin3 = 3;
int Pin9 = 5;

int dutycycle = 255;

void setup() {
  
  pinMode(Pin3, OUTPUT);
  pinMode(Pin9, OUTPUT);
    Timer1.initialize(25);
    Timer1.pwm(Pin9, dutycycle);
}

void loop() {
  analogWrite(Pin3, dutycycle / 4);
  Timer1.setPwmDuty(Pin9, dutycycle);

}
