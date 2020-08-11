//Here I try to create a specific workflow for the Arduino:
// I want it to handle the relay timers and in a later version i want to be able to
// change the parameters of every timer via a serial connection with the Pi

class Relay {
  public:
    int id;
    int ontime;
    int offtime;
    int start_in;
    //int relay_pin;
    int timer;
    char phase;
    Relay(int _id, int _ontime, int _offtime, int _start_in = 0) { //constructor
     // Serial.println("initializing object");
      id = _id;
      ontime = _ontime;
      offtime = _offtime;
      start_in = _start_in;

      if (start_in == 0) {
        timer = start_in;
        phase = 'w';
        //Serial.println("Waiting");
      } else {
        timer = ontime;
        phase = 'y';
        //Serial.println("Ontime");
      }
    }
    void subtract_time_passed(int time_passed) {
      timer -= time_passed;
      //Serial.print(id);
      //Serial.println(":  Subtracting time");
    }

    void update_timers(int time_passed) {
      
      subtract_time_passed(time_passed);
      if (timer == 0) {
        //Serial.println("A timer is on 0");
        if (phase == 'y') { // ontimer has expired
          timer = offtime;
          phase = 'n';
         //Serial.println("About to toggle the relay!!\n\n\n\n");
          toggle_relay(); // toggling the relay
          Serial.print("Relay OFF: ");
          Serial.println(id);
        } else if (phase == 'n' || phase == 'w') { //incase the offtimer or the waiting timer has expired
          timer = ontime;
          phase = 'y';
          toggle_relay(); // toggling the relay
          Serial.print("Relay ON:  ");
          Serial.println(id);
        }
      }
    }
    void toggle_relay() { //toggle the current relay state
      bool state = digitalRead(id);
      state = !state;
     // Serial.print("Relay state: ");
     // Serial.println(state);
      digitalWrite(id, state);
      
    }
};


void selectionSort(int a[], int n) {
   int i, j, min, temp;
   for (i = 0; i < n - 1; i++) {
      min = i;
      for (j = i + 1; j < n; j++)
      if (a[j] < a[min])
      min = j;
      temp = a[i];
      a[i] = a[min];
      a[min] = temp;
   }
}


int all_timers[2];

char arg[10][10];
long int arg_long[10];
String data;

#define RLP1 9
#define RLP2 8
#define RLP3 7
#define RLP4 6

void ALL_OFF() {
  digitalWrite(RLP1, LOW);
  digitalWrite(RLP2, LOW);
  digitalWrite(RLP3, LOW);
  digitalWrite(RLP4, LOW);
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

void arrStr2Int() {
  int i = 0;

  while (arg[i][0] != 0) {
    if (i == 0) { //skip the first token, since we expect a char anyway
      i++;
      continue;
    }
    arg_long[i] = atol(arg[i]); //assigning the old "char"  to a new "long int"
    Serial.println(arg_long[i]);
    i++;
    //    if (i > 4){
    //      break;
    //    }
  }
}

Relay rl1(RLP1, 5, 10, 0);
Relay rl2(RLP2, 2, 2, 0);


void setup() {
  Serial.begin(9600);
  pinMode(RLP1, OUTPUT);
  pinMode(RLP2, OUTPUT);
  pinMode(RLP3, OUTPUT);
  pinMode(RLP4, OUTPUT);

}

void loop() {
//  if (Serial.available() > 0) {
//    data = Serial.readStringUntil('\n');
//
//    myParse(data);
//    arrStr2Int();
//  }
  all_timers[0] = rl1.timer;
  all_timers[1] = rl2.timer;
  selectionSort(all_timers, 2);
  delay(all_timers[0] * 1000);
  Serial.println("_____________");
  Serial.print("Timer on:  ");
  Serial.println(all_timers[0]);
  rl1.update_timers(all_timers[0]);
  rl2.update_timers(all_timers[0]);

  
  delay(3000);
  
}
