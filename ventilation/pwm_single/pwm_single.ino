#include <TimerOne.h>

int pwmPin = 10;


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


    Timer1.setPwmDuty(pwmPin,512); // set the new poti value as dutycycle
    


    Serial.println(dutycycle / 10.23); //print dutycycle in percentages
}
