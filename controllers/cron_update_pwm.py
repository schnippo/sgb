import serial, time
from classes import *

ser = serial.Serial(AuthUtils().scan_for_response(addresses=AuthUtils().devices, target="fan_controller"), 9600)
def avg_lastNlines(file, N):
    f = open(file, "r")
    for line in len(f.readlines) [-N:]:
        try:
             s += line
        except TypeError as msg:
            print(msg)
            continue
    return s/N
     
def is_connected(): # sending code '7' and expecting to receive 'r'
        ser.write('7'.encode())
        if ser.read().decode() == 'r':
            return True 
        # print("arduino is responsive! :D")



opt_temp = open("at_threshold" ,"r").readline()
opt_hum = open("ah_threshold", "r").readline()
std_pwm = open("std_pwm", "r").readline()
max_delta_t = open("max_delta_t", "r").readline()
max_delta_h = open("max_delta_h", "r").readline()

curr_temp = avg_lastNlines(open("at_log"), 5) # get the last 5 minutes of temp values
curr_hum = avg_lastNlines(open("ah_log"), 5) # get the last 5 minutes of hum values

delta_t = curr_temp - opt_temp
delta_h = curr_hum - opt_hum






if delta_h > 0: #only act if necessary
    pwm_boost_t = (delta_t * (100 - std_pwm) / max_delta_t ) * 10.23 #multiplies delta_t with a factor, that is based on how far i assume i need to go
elif delta_h > 0:
    pwm_boost_h,pwm_boost_t = 0,0

#add the new pwm_boost to the std_pwm
new_pwm = std_pwm * 10.23 + ((max(pwm_boost_h, pwm_boost_t) - min(pwm_boost_h,pwm_boost_t)) * 2 / 3 * 10.23) # der obere wert wird um einen drittel des abstands zum unteren gekuerzt.
new_pwm = min(new_pwm, 1023) #takes the smaller value, to keep the script from sending  a value > 1023



##having a bit of rendunancy ain't bad. we send a new pwm sig to the fans on arduino port 9
##these are the in- and outtake fans.
while True:
    if is_connected and ser.isOpen():
        ser.write(("9,"+str(new_pwm).encode())) # sends the new pwm_sig 
        break
    else:
        print("can't reach arduino, trying again")
        time.wait(0.1)
