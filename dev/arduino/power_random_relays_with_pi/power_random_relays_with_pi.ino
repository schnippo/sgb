//Here I listen for a what the the random number the Pi gives me and power on a relay accordingly.



#define RL_1_PIN 9
#define RL_2_PIN 8
#define RL_3_PIN 7
#define RL_4_PIN 6

void ALL_OFF(){
  digitalWrite(RL_1_PIN, LOW);  
  digitalWrite(RL_2_PIN, LOW);
  digitalWrite(RL_3_PIN, LOW);
  digitalWrite(RL_4_PIN, LOW);
}




void setup() {
  Serial.begin(9600);
  pinMode(RL_1_PIN, OUTPUT);
  pinMode(RL_2_PIN, OUTPUT);
  pinMode(RL_3_PIN, OUTPUT);
  pinMode(RL_4_PIN, OUTPUT);

  ALL_OFF();
}

bool state;

void loop() {
  if (Serial.available() > 0) { //check if Pi has sent sth
    int ledNumber = Serial.read() - '0'; // this is a little trick to convert the received string into an integer.

//    ALL_OFF();
    switch (ledNumber) {
      case 1:
        state = digitalRead(RL_1_PIN);   
        state = !state;
        digitalWrite(RL_1_PIN, state);
        break;
      case 2:
        state = digitalRead(RL_2_PIN);   
        state = !state;
        digitalWrite(RL_2_PIN, state);
        break;
      case 3:
        state = digitalRead(RL_3_PIN);   
        state = !state;
        digitalWrite(RL_3_PIN, state);
        break;
      case 4:
        state = digitalRead(RL_4_PIN);
        state = !state;
        digitalWrite(RL_4_PIN, state);
        break;
      case 0:
      ALL_OFF();
      default:
        break;
    }
  
  }

}
