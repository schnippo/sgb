//Here I try to create a specific workflow for the Arduino:
// I want it to handle the relay timers and in a later version i want to be able to
// change the parameters of every timer via a serial connection with the Pi
#include <TimerOne.h>

volatile bool time_running = false;
volatile bool sec_over;
unsigned long t1, time_passed_until_reinit;
int all_timers[2], arg_long[10], sec_count,new_time;
char arg[10][10];
String data;


#define RLP1 9
#define RLP2 8
#define RLP3 7
#define RLP4 6

class Relay {
  public:
    int id;
    int port;
    int ontime;
    int offtime;
    int start_delay;
    int timer;
    char phase;
    Relay(int _id, int _port, int _ontime, int _offtime, int _start_delay) { //constructor
      id = _id;
      port = _port;
      ontime = _ontime;
      offtime = _offtime;
      start_delay = _start_delay;

      if (start_delay != 0) {
        timer = start_delay;
        phase = 'w';
      } else {
        timer = ontime;
        phase = 'y';
      }
    }
    void subtract_time_passed(int time_passed) {
      timer -= time_passed;
    }
//##################################

    void update_timers(int time_passed) { 
      subtract_time_passed(time_passed);

      if (timer <= 0) { //IMPORTATNT
        if (start_delay != 0){ // START DELAY IF it hasn't been done yet.
          timer = start_delay;
          start_delay = 0; //set it to 0, so it doesnt run in the next cycle
          phase = 'w';
          digitalWrite(port, LOW);
          Serial.print("______________________Delay detected on RL ");
          Serial.println(id);
        } else if (phase == 'y') { // TOGGLE OFF
          timer = offtime;
          phase = 'n';
          toggle_relay();
          Serial.print("Relay OFF: ");
          Serial.println(id);
        } else if (phase == 'n' or phase == 'w') { //TOGGLE ON
          timer = ontime;
          phase = 'y';
          toggle_relay(); 
          Serial.print("Relay ON:  ");
          Serial.println(id);
        
        }
      }
    }
//    ##########################################################3
    void toggle_relay() { //toggle the current relay state
      bool state = digitalRead(port);
      state = !state;
      Serial.print("Relay "); Serial.print(id); Serial.print("- State: "); Serial.println(state);
      digitalWrite(port, state);
      
    }

    void switch_to_startdelay(){
      
      if (start_delay != 0){
        timer = start_delay;
        start_delay = 0;
        phase = 'w';
        Serial.println("#### A NEW STARTDELAY HAS BEEN DETECTED, SWITCHING NOW $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
      }
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
//    if (i == 0) { //skip the first token, since we expect a char anyway
//      i++;
//      continue;
//    }
    arg_long[i] = atof(arg[i]); //assigning the old "char"  to a new "long int"
    Serial.println(arg_long[i]);
    i++;
  }
}


//######################################33


Relay rl1(1,RLP1, 50, 10, 0);
//Relay rl2(2,RLP2, 2, 2, 2);


//#######################3##########333

void reinit_rl(int _id, int _ontime, int _offtime, int _start_delay){
  Serial.println("###Reinit started###");
  Timer1.detachInterrupt();
  Serial.println("###Detached Timer###");
  time_passed_until_reinit = (millis() - t1);
  
  Serial.print((int)time_passed_until_reinit / 1000); Serial.println(" seconds passed since timer first started");
  switch (_id) {
    case 1:
      Serial.println("### CHANGING RL1 SETTINGS ###");
      rl1.ontime = _ontime;
      rl1.offtime = _offtime;
      rl1.start_delay = _start_delay;
      break;

    case 2:
      Serial.println("### CHANGING //rl2 SETTINGS ###");
      //rl2.ontime = _ontime;
      //rl2.offtime = _offtime;
      //rl2.start_delay = _start_delay;
      break;
//    case 3:
//      Serial.println("### CHANGING RL3 SETTINGS ###");
//      rl3.ontime = _ontime;
//      rl3.offtime = _offtime;
//      rl3.start_delay = _start_delay; 
//      break;
//    
//    case 4:
//      Serial.println("### CHANGING RL4 SETTINGS ###");
//      rl4.ontime = _ontime;
//      rl4.offtime = _offtime;
//      rl4.start_delay = _start_delay;
//      break;
      default:
        Serial.println("###Check your syntax!###");
        break;
  }
  Serial.println("###########Updating TIMERS");
  rl1.switch_to_startdelay(); 
  //rl2.switch_to_startdelay(); 
//  rl3.switch_to_startdelay(); 
//  rl4.switch_to_startdelay(); 
//  rl1.update_timers((int)time_passed_until_reinit / 1000);  
//  //rl2.update_timers(time_passed_until_reinit);
//  r3.update_timers(time_passed_until_reinit);
//  r4.update_timers(time_passed_until_reinit);
  
  time_running = false; // so that it starts the new timer
}


void setup() {
  Serial.begin(9600);
  pinMode(RLP1, OUTPUT);
  pinMode(RLP2, OUTPUT);
  pinMode(RLP3, OUTPUT);
  pinMode(RLP4, OUTPUT);
  Timer1.initialize(1000000); //start the timer, the value has no meaning.
}

void isr(){ //interrupt service routine
  sec_count++;
  sec_over = true;
}



void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
//    dump = Serial.read();
    myParse(data);
    arrStr2Int();
    reinit_rl(arg_long[0], arg_long[1], arg_long[2], arg_long[3]);
  }

  
  
  if (time_running == false) { // check if i should start a timer
    all_timers[0] = rl1.timer;
//    all_timers[1] = rl2.timer;
    selectionSort(all_timers, 1);
    new_time = all_timers[0];
    Serial.print("+ Starting timer: ");
    Serial.print(new_time);
    Serial.print(" seconds\n");
    t1 = millis(); //Timestamp of when the timer has been started
    time_running = true;
  }



  if (sec_count == new_time) { // timer is over
    sec_count = 0;
    Serial.println("+ Time is over");
    Timer1.detachInterrupt();
    rl1.update_timers(all_timers[0]);
    //rl2.update_timers(all_timers[0]);
    time_running = false;
  } else {
    Timer1.attachInterrupt(isr, 1000000); // wait another second
    sec_over = false;
//    Serial.println(sec_count);
  }
  
}
