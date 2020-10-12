import time, serial
    
def smallest_val_first(list): # a function to sort the values of a given array of numbers. it modifies it.
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp



class AuthUtils():
    devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
    
    def get_arduino_response(self, device, msg):
        ser = serial.Serial(device, 9600)
        ser.write(msg.encode())
        time.sleep(.5)
        while ser.in_waiting == 0:
            msg0 = ser.readline() #emptying the input buffer
        return str(ser.readline().decode())


    def scan_for_response(self, target, addresses = devices):
        # print("target ID: " + str(target))
        for addr in addresses:
            try:
                if (self.get_arduino_response(addr, "99") == str(target)+"\r\n"):
                    # print("success, address is " + addr)
                    return addr
            except serial.SerialException:
                # print("bad address: " + addr)
                continue



class Relay():
    
    serialbus = serial.Serial(AuthUtils().scan_for_response("relay_controller"))
    
    def __init__(self, relay_id, ontime, offtime, start_in = 0, active=True):
        self.id = relay_id
        self.ontime = ontime
        self.offtime = offtime
        self.start_in = start_in
        self.active = active
        if start_in > 0: # fire up the first timer, if it isn't on a first-time-delay (start_in)
            # print("Waiting " + str(self.start_in) + " second(s) for timer " + str(self.id) + " to start.")
            self.current_timer = self.start_in
            self.current_phase = 'waiting to start'
        else:
            self.current_timer = self.ontime
            self.current_phase = 'on'


    def toggle_relay(self):
        # print("toggling relay " + str(self.id))
        self.serialbus.write(str(self.id).encode)


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

# print(get_arduino_response(devices[2], "99"))

# print(scan_for_response(devices, "relay_controller"))


# ser.write(str(0).encode('utf-8')) # to reset all

# while True:

#     all_timers = [rl1.current_timer, rl2.current_timer]
#     smallest_val_first(all_timers) # sorting the currently ticking timers for the shortest
    
#     time_to_pass = all_timers[0] # the shortest ticking timer is the one that we now wait to elapse
    
#     time.sleep(time_to_pass) #wait for time to elapse
    
#     rl1.update_timers(time_to_pass)
#     rl2.update_timers(time_to_pass)