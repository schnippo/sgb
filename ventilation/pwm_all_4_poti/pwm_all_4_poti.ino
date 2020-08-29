#include <TimerOne.h>

int fan1 = 3;
int fan2 = 5;
int fan3 = 6;
int fan4 = 9;

int potiPin = A3;
int dutycycle = 512;

void setup(void)
{
  pinMode(fan1, OUTPUT);
  pinMode(fan2, OUTPUT);
  pinMode(fan3, OUTPUT);
  pinMode(fan4, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(fan1, 0);
  Timer1.pwm(fan2, 0);
  Timer1.pwm(fan3, 0);
  Timer1.pwm(fan4, 0);
  Serial.begin(9600);
  
}
void loop(void)
{
//  dutycycle = analogRead(potiPin); //get the poti value

  Timer1.setPwmDuty(fan1,dutycycle); // set the new poti value as dutycycle
  Timer1.setPwmDuty(fan2,dutycycle); // set the new poti value as dutycycle
  Timer1.setPwmDuty(fan3,dutycycle); // set the new poti value as dutycycle
  Timer1.setPwmDuty(fan4,dutycycle); // set the new poti value as dutycycle
  
  Serial.println(dutycycle / 10.23); //print dutycycle in percentages
}
