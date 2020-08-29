int Pin1 = 3;
int Pin2 = 5;
int Pin3 = 6;

int dutycycle = 255;

void setup() {
  
  pinMode(Pin1, OUTPUT);
  pinMode(Pin2, OUTPUT);
  pinMode(Pin3, OUTPUT);
  


}

void loop() {
  analogWrite(Pin1, dutycycle);
  analogWrite(Pin2, dutycycle);
  analogWrite(Pin3, dutycycle);

}
