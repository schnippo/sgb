#include <stdio.h>
#include <string.h>
char arg[10][10];
int toggle = 0;
void setup() {
  pinMode(6,OUTPUT); 
  Serial.begin(9600);
  
}
void loop() {
//  Serial.println("Hello World");
//  delay(3000);
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    myParse(data);
    execCommand();
    
  }
}

void execCommand(){
  int i = 0;
  
  while(arg[i][0] != 0) {
   switch(arg[0][0]){
    case 'r':
        Serial.println("received 'r'");
//      digitalWrite(13, toggle);
//      toggle = !toggle;
      break;
   }
  }
 }



void myParse(String data){
  char *token;
  int i = 0;
  
  token = strtok(data.c_str(), ",");
  while(token != NULL){
    strcpy(arg[i++],token);
    //Serial.println(token);
    token = strtok(NULL, ",");
  }
  arg[i++][0] = 0;  
}
