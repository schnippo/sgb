#include <TimerOne.h>

int pwmPin = ;

int potiPin = A3;
int dutycycle = 0;

void setup(void)
{
  pinMode(pwmPin, OUTPUT);
//  pinMode(7, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(pwmPin, 0);
 
  Serial.begin(9600);
  
}
void loop(void)
{
//  dutycycle = analogRead(potiPin); //get the poti value

    Timer1.setPwmDuty(pwmPin,512); // set the new poti value as dutycycle
    delay(3000);
//    Timer1.setPwmDuty(pwmPin,1023); // set the new poti value as dutycycle
//    delay(1000);

  Serial.println(dutycycle / 10.23); //print dutycycle in percentages
}
