import threading, time, sys, serial


devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]

def get_arduino_response(device, msg):
    
    with serial.Serial(device, 9600) as ser:
        ser.write(msg.encode())
        time.sleep(.3)
        # while ser.in_waiting  0:
        #     msg0 = ser.readline() #emptying the input buffer
        return str(ser.read(200).decode())


def scan_for_response(target):
    # print("target ID: " + str(target))
    for addr in devices:
        try:
            if (get_arduino_response(addr, "9") == str(target)+"\r\n"):
                print("success, address is " + addr)
                return addr
        except serial.SerialException:
            print("bad address: " + addr)
            continue

print(get_arduino_response('/dev/ttyACM0', "9"))
# print(scan_for_response("fan_controller"))



def is_connected(): # sending code '7' and expecting to receive 'r'
    ser.write('7'.encode())
    if ser.read().decode() == 'r':
        return True 
    # print("arduino is responsive! :D")


class RelayTimer():
    
    # ser = serial.Serial(AuthUtils().scan_for_response(addresses=AuthUtils.devices, target="relay_controller"), timeout=2, baudrate=9600)
    
    
    def __init__(self, _id, ontime, offtime, switch="on"):
        self.id = _id
        self.ontime = ontime #if ontime > 0 else ontime * -1
        self.offtime = offtime #if offtime > 0 else offtime * -1
        self.switch = switch
        self.state = "off"
        self.timer = ontime #if ontime > 0 else ontime * -1
        self.value_check()

    def value_check(self):
        print("performing value check")
        if self.ontime == 0:
            print(f"switching off due to ontime being 0")
            self.switch = "off"
        elif self.offtime == 0:
            print(f"switching off due to offtime being 0")
       
    def is_connected(self): # sending code '7' and expecting to receive 'r'
        self.ser.write('7'.encode())
        if self.ser.read().decode() == 'r':
            return True 
        # print("arduino is responsive! :D")

    def swap_timer(self):
        while True:
            if self.is_connected and self.ser.isOpen(): # check if arduino is responsive
                self.ser.write(str(self.id).encode()) # here u actually send the signal, which only consists of the ID
                break 
            else:
                time.sleep(0.1)
                print("serial is still closed")
        self.timer = self.offtime if self.timer == self.ontime else self.ontime
        self.state = "off" if self.state == "on" else "on"
        print(f"swapping timer {self.id} in {self.timer} seconds")
        


    def wait_timer(self):
        time.sleep(self.timer) # actually wait
        self.swap_timer()


    def start(self):
        if self.switch == "off": #do not turn on if switch is off
            return
        else: 
            self.state = "on"
            self.clock = threading.Thread(target=self.wait_timer)
            self.clock.start()

    def stop(self):
        self.clock._stop()
        print("stopped timer")


def reactivate_inactive_timers(timer_list):
    for timer in timer_list:
        if timer.state == "off":
            timer.start()
            # print(f"reactivating timer {timer.id}")

def reinit_timers_via_extern(cmdfile, timers):
    with open(cmdfile, "r") as f:
        args = f.read().split()
        try:
            if args[0] != []:  
                if int(args[0]) == 0:
                    RelayTimer.ser.write("0".encode())
                    print("sending shut off signal")
                # print(args)
                for i in range(0, 3):
                    args[i] = int(args[i])
                #     args[i] = args[i] * -1 if args[i] < 0 else args[i] # values will be made positive if theyre negative
                #     print("making timers positive")
                #     if args[i] == 0:
                #         print("one timer is 0, flipping the switch off")
                #         args[3] = "off" #if one of them is 0, switch will be turned off
                # print("initializing new timer")
                timers[int(args[0]) - 1] = RelayTimer(args[0], args[1], args[2], args[3])
        except:
            # print("-")
            pass
    with open(cmdfile, "w") as f:
        f.write("")
        
    
def get_prop_value(prop):
    properties = {}
    lines = open("properties", "r").readlines()
    for line in lines:
        properties[line.split()[0]] = line.split()[1]
    return properties[prop]



def update_prop(prop, value):
    properties = {}
    lines = open("properties", "r").readlines()
    for line in lines:
        properties[line.split()[0]] = line.split()[1]
    properties[prop] = value
    with open("properties", "w") as f:
        for key in properties:
            f.write(key + " " + properties[key] +"\n")


def avg_lastNlines(file, N):
    total = 0
    with open(file, "r") as f:
        for line in (f.readlines() [-N:] ):
            try:
                # print(line)
                total += int(line)
            except TypeError as msg:
                print(msg)
                continue
        return round(total/N, 2)



#def get_arduino_response(device, msg):
#    ser = serial.Serial(device, 9600)
#    ser.write(msg.encode())
#    time.sleep(.5)
#    while ser.in_waiting == 0:
#        msg0 = ser.readline() #emptying the input buffer
#    return str(ser.readline().decode())
#
#
#def scan_for_response(addresses, target):
#    # print("target ID: " + str(target))
#    for addr in addresses:
#        try:
#            if (get_arduino_response(addr, "99") == str(target)+"\r\n"):
#                # print("success, address is " + addr)
#                return addr
#        except serial.SerialException:
#            # print("bad address: " + addr)
#            continue
#

# mytimer1 = RelayTimer(1,11,4)
# mytimer2 = RelayTimer(2,12,9)
# # mytimer3 = RelayTimer(3,4,5)
# timers = [mytimer1, mytimer2]



# while True:
#     time.sleep(0.5)
#     reinit_timers_via_extern()
#     # print("-")
#     reactivate_inactive_timers(timers)

# TODO: hook up the swap function with a signal call, so it works like the old class
# switch names, make it to the real class, dump the other one
# implement it, flash the relay-arduino with the relay_backend_script (with auth!)



# start = time.perf_counter()

# def do_sth():
#     print("boutta sleep fo 1 secc")
#     time.sleep(1)
#     print("dun sleepin fo 1 secc")

# threads = []

# for _ in range(5):
#     t = threading.Thread(target=do_sth)
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join() 

# end = time.perf_counter()


# print("finished in " + str(round(end - start, 3)) +" seconds")
