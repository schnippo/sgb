#include <TimerOne.h>

int pwmPin = 9;

//int potiPin = A3;
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
    dutycycle = 512;
    Timer1.setPwmDuty(pwmPin,dutycycle); // set the new poti value as dutycycle
    Serial.println(dutycycle / 10.23); //print dutycycle in percentages
    delay(3000);
    
    dutycycle = 1023;
    Timer1.setPwmDuty(pwmPin,dutycycle); // set the new poti value as dutycycle
    Serial.println(dutycycle / 10.23); //print dutycycle in percentages
    delay(1000);
    
}
