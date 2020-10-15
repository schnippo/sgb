#include <TimerOne.h>

#define ArduinoID "fan_controller"

int Pin3 = 3; // is preset to be the small fogfan running on 35% PWM
int Pin9 = 9; // is preset for the in- and outtake fans. (it powers two transistors);
int Pin10 = 10; // is preset for the turbulence fan

char arg[10][10];
String data;
int arg_int[10];

void setup() {
  Serial.begin(9600);
  pinMode(Pin3, OUTPUT);
  pinMode(Pin9, OUTPUT);
  pinMode(Pin10, OUTPUT);  
  Timer1.initialize(25); // Set PWM Frequency to 40kH
//  Timer1.pwm(Pin3, 0);
  Timer1.pwm(Pin9, 0); // start the two pwm clocks
  Timer1.pwm(Pin10, 0);
}

void loop() {
  data = Serial.readStringUntil('\n');
  
  myParse(data);
//  data = '\0';
  arrStr2Int(); 
  
  
  updatePWM(arg_int);
}

void updatePWM(int args_int[10]){
    if (data != '\0'){
      switch (args_int[0])
      {
      case 3:
        analogWrite(Pin3, args_int[1]);
        Serial.println("P3");
        break;
      case 9:
        Timer1.setPwmDuty(Pin9, args_int[1]);
        Serial.println("P9");
        break;
      case 10:
        Timer1.setPwmDuty(Pin10, args_int[1]);
        Serial.println("P10");
        break;
      case 99: // in case the raspi wants to know which Arduino this is
        Serial.println(ArduinoID);
        break;
      default:
        Serial.println("Check your syntax: [id(3,9,10),[dutycycle(0-1023)]");
        break;
      }
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
//    Serial.println(arg_int[i]);
    i++;
  }
}
