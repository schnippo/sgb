LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"

from file_handler import cache_properties, sync_properties, update_prop_or_relay, get_new_pwm
from pwm import get_auto_pwm, send_update_sig
from time import sleep
import os, serial
from serial_test import get_address
from dht_logger import get_at

last_modified = os.path.getmtime(REMOTE_PROPERTIES)
relay_ser = serial.Serial(get_address("relay_controller", try_usb_reset=True))
pwm_ser = serial.Serial(get_address("fan_controller", try_usb_reset=True))
if relay_ser.port == None:
    print("relay port isn't plugged in, pls replug")
    exit()
elif pwm_ser.port == None:
    print("pwm port isn't plugged in, pls replug")
    exit()
print("* relay on", relay_ser.port)
print("* pwm on", pwm_ser.port)


print("* serial connections established")
sync_properties() # overrides local_props with remote_props
print("* synced properties for the first time")

properties, relays = cache_properties() #this func returns two dictionaries

vent_counter, tries = 0,0

pwm_sigs_now = { # last Value is if it needs to change stills
        "pwm_fog": [3, 40, True],
        #"pwm_turb": [10, 0, True], #removed due to the turb-fan being too weak, see toboy notes
        "pwm_vent": [9, 0, True]
        }

print("* started the fans, should be running now")
print("checking temp sensor...(max 15s)")
temp_check = get_at()
if temp_check is not None:
    print("temp sensor check: successful, continuing..")
else:
    print(f"temp rn: {temp_check}\ntemp sensor check: fatal, check wiring or W1 Modules. Aborting.")
    exit(1)




def update_rl_arr(serial_object, ID):
    #expecting a key for a list as input that has the following format: [timer, ontime, offtime, state]
    timer, ontime, offtime, state = 0, 1, 2, 3 # these are the indexes
    # relays[ID][state] = str(relays[ID][state]) 
    if relays[ID][timer] == "inactive" :
        #print(f"relay {ID} is currently inactive, skipping...")
        return
    relays[ID][timer] = int(relays[ID][timer])
    relays[ID][timer] -= 1        
    if relays[ID][timer] < 1:
        print(f"relay {ID} has reached 0, swapping timers..")
        relays[ID][timer] = relays[ID][ontime] if relays[ID][state] == "off" else relays[ID][offtime] # set timer to ontime if the old state was off
        relays[ID][state] = "off" if relays[ID][state] == "on" else "on" #set state to off if 
        send_flip_token(serial_object, ID)

def send_flip_token(serial_object,ID):
    serial_object.write(ID.encode())
    

def update_fans():
    for fan in pwm_sigs_now:
        if pwm_sigs_now[fan][2]: # check if it needs to be changed
            pwm_sigs_now[fan][2] = False
            if send_update_sig(pwm_ser, pwm_sigs_now[fan][0], pwm_sigs_now[fan][1]):
                print(f"- success on {fan} with {pwm_sigs_now[fan][1]}%")



while True:
    sleep(1)
    print(".")
    vent_counter += 1
    # print(vent_counter)
    for fan in pwm_sigs_now:
        if pwm_sigs_now[fan][2]: # check if it still needs to change sth
            pwm_sigs_now[fan][2] = False
            response = send_update_sig(pwm_ser, pwm_sigs_now[fan][0], pwm_sigs_now[fan][1])
            if response:
                print(f"- success on {fan} with {pwm_sigs_now[fan][1]}%")
            else:
                print(response)


    if vent_counter >= 10:
        #also print all active timers:
#        for relay in relays:
        for relay in relays:
            print(relay, " ", relays[relay])
#            print(f"relay{relay[0]} timer: {relay[1]}")
        vent_counter = 0 # reset it to start a new auto_pwm loop
        result = get_auto_pwm()
        if result != pwm_sigs_now["pwm_vent"][1]: # if it's different from before
            pwm_sigs_now["pwm_vent"] = [9, result, True] # then update it pls.

    if last_modified != os.path.getmtime(REMOTE_PROPERTIES):
        last_modified = os.path.getmtime(REMOTE_PROPERTIES)
        print("$$$$$$$$$$$$  props have changed, sync process starting")
        pwm_sigs_now = get_new_pwm(pwm_sigs_now) #working with "properties" before it gets updated
        # print(f"changed_pwm_sigs: {pwm_sigs_now}")
        sync_properties() #saving remotely modified data locally
        properties, relays = cache_properties(relays) #this func returns two dictionaries
        print("SYNC DONE")

    update_fans()

    # doing relay tasks
    for relay in relays:
        # print("updating relay", relay)
        update_rl_arr(relay_ser, relay)

