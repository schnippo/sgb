import time, serial
from ard_auth import *
    
def smallest_val_first(list): # a function to sort the values of a given array of numbers. it modifies it.
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp

devices = ard_auth.devices
port = scan_for_response(devices, "relay_controller")
ser = serial.Serial('port', 9600)



if __name__ == "__main__":
    class Relay():
        def __init__(self, relay_id, ontime, offtime, start_in = 0):
            self.id = relay_id
            self.ontime = ontime
            self.offtime = offtime
            self.start_in = start_in
            
            if start_in > 0: # fire up the first timer, if it isn't on a first-time-delay (start_in)
                # print("Waiting " + str(self.start_in) + " second(s) for timer " + str(self.id) + " to start.")
                self.current_timer = self.start_in
                self.current_phase = 'waiting to start'
            else:
                self.current_timer = self.ontime
                self.current_phase = 'on'


        def toggle_relay(self):
            # print("toggling relay " + str(self.id))
            ser.write(str(self.id).encode)


        def subtract_time_passed(self, time_passed):
            self.current_timer -= time_passed

        def update_timers(self, time_passed): # to be called everytime a timer-cycle has been completed
            self.subtract_time_passed(time_passed)
            if self.current_timer == 0:
                
                if self.current_phase == 'on': # the ontimer has expired, we switch to the offtimer
                    # print("Relay " +  str(self.id) + ": Ontimer has expired, starting offtimer now")
                    self.current_timer = self.offtime
                    self.current_phase = 'off' 
                    self.toggle_relay()         # toggling the relay
                elif self.current_phase == 'off': #if the offtimer has expired, we switch to the ontimer
                    # print("Relay " + str(self.id) + ": Offtimer has expired, starting ontimer now")
                    self.current_timer = self.ontime
                    self.current_phase = 'on'  
                    self.toggle_relay()         # toggling the relay
                elif self.current_phase == 'waiting to start':
                    self.start_in = 0
                    self.current_timer = self.ontime
                    self.current_phase = 'on'
                    self.toggle_relay()



ser.write(str(0).encode('utf-8')) # to reset all

# while True:

#     all_timers = [rl1.current_timer, rl2.current_timer]
#     smallest_val_first(all_timers) # sorting the currently ticking timers for the shortest
    
#     time_to_pass = all_timers[0] # the shortest ticking timer is the one that we now wait to elapse
    
#     time.sleep(time_to_pass) #wait for time to elapse
    
#     rl1.update_timers(time_to_pass)
#     rl2.update_timers(time_to_pass)