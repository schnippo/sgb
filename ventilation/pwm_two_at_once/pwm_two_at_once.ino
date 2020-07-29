#include <TimerOne.h>

int pwmPin1 = 10;
int pwmPin2= 9;
int pwmCopy1 = 5;
int pwmCopy2 = 4;
int potiPin = A3;
int dutycycle = 0;
int toggle = 0;
void setup(void)
{
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmCopy1, OUTPUT);
  pinMode(pwmCopy2, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(pwmPin1, 0);
  Timer1.pwm(pwmPin2, 0);
  Serial.begin(9600);
  
}
void loop(void)
{
  dutycycle = analogRead(potiPin); //get the poti value

  Timer1.setPwmDuty(pwmPin1, 512); // set the new poti value as dutycycle
  Timer1.setPwmDuty(pwmPin2, dutycycle); // set the new poti value as dutycycle

  //Serial.println(dutycycle / 10.23); //print dutycycle in percentages

  toggle = !toggle;
  digitalWrite(pwmCopy1, toggle);
  digitalWrite(pwmCopy2, digitalRead(pwmCopy1));
}
