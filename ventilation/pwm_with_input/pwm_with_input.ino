#include <TimerOne.h>

int pwmPin = 3;

int dutycycle;
char arg[10][10];
String data;
int arg_int[10];


void setup(void)
{
  pinMode(pwmPin, OUTPUT);
//  pinMode(3, OUTPUT);
  Timer1.initialize(25);
  Timer1.pwm(pwmPin, 0);
 
  Serial.begin(9600);
  Serial.println("Ready");
}

void loop(void)
{
  data = Serial.readStringUntil('\n');
  myParse(data); //syntax is this: [fan-id],[pwm]
  arrStr2Int(); 
  dutycycle = arg_int[1]; //update the dutycycle for all timers
  Timer1.setPwmDuty(arg_int[0],dutycycle); // set the new poti value as dutycycle


  Serial.println(dutycycle); //print dutycycle in percentages
}


void updatePWM(int args_int){
  switch (args_int[0])
  {
  case 1:
    
    break;
  
  default:
    break;
  }

}

void myParse(String data) {
  char *token; // for storing the different, chopped up segments.
  int i = 0; //index

  token = strtok(data.c_str(), ",");
  while (token != NULL) { // keep running as long as there are tokens left
    strcpy(arg[i++], token); //get 
    //Serial.println(token);
    token = strtok(NULL, ",");
  }
  arg[i++][0] = 0;
}


void arrStr2Int() { // converts my string-based argument-array to a int-based argument-array
  int i = 0;

  while (arg[i][0] != 0) {
//    if (i == 0) { //skip the first token, since we expect a char anyway
//      i++;
//      continue;
//    }
    arg_int[i] = atoi(arg[i]); //assigning the old "char"  to a new "int"
    Serial.println(arg_int[i]);
    i++;
  }
}
