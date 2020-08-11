#include <TimerOne.h>
#include <TFT.h>
#define RLP1 9
#define RLP2 8
#define RLP3 7
#define RLP4 6
bool flag;


void isr(){
  flag = true;
//  Timer1.detachInterrupt();
}


void setup() {
 
  Serial.begin(9600);
  pinMode(RLP1, OUTPUT);
  pinMode(RLP2, OUTPUT);
  pinMode(RLP3, OUTPUT);
  pinMode(RLP4, OUTPUT);
  
  Timer1.initialize(1000000);
  Timer1.attachInterrupt(isr, 5000000);


}



void loop() {
//   put your main code here, to run repeatedly:
  if (flag) {
    Serial.println("Yes");
    flag = false;
//    Timer1.detachInterrupt();
  }
}
