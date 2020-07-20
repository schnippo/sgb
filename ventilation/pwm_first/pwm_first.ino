#include <TimerOne.h>

int pwmPin = 10;
int potiPin = A3;
int dutycycle = 0;

void setup(void)
{
  pinMode(pwmPin, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(pwmPin, 0);
  Serial.begin(9600);
  
}
void loop(void)
{
  dutycycle = analogRead(potiPin); //get the poti value

  Timer1.setPwmDuty(pwmPin, dutycycle); // set the new poti value as dutycycle

  Serial.println(dutycycle / 10.23); //print dutycycle in percentages
}
