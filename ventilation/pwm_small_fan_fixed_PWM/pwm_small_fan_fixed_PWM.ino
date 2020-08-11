#include <TimerOne.h>
int pwmPin = 10;
int dutycycle = 360; // this is 20% dutycycle, the perfect amount for creating a light breeze in the tank
void setup(void)
{
  pinMode(pwmPin, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(pwmPin, dutycycle);
}
void loop(void){
Timer1.setPwmDuty(pwmPin, 1023); //this kicks the fan in the ass, so it starts
delay(100); // this is necessary, since it doesnt always start on 35% dutycycle, if it somehow stops
Timer1.setPwmDuty(pwmPin, dutycycle);
delay(10000);

}
