LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"

from file_handler import cache_properties, sync_properties, update_prop_or_relay, get_pwm_changes
from pwm import get_auto_pwm, send_update_sig
from time import sleep
import os, serial
from serial_test import get_address






last_modified = os.path.getmtime(REMOTE_PROPERTIES)
relay_ser = serial.Serial(get_address("relay_controller"))
pwm_ser = serial.Serial(get_address("fan_controller"))
print("* relay on", relay_ser.port)
print("* pwm on", pwm_ser.port)


print("* serial connections established")
sync_properties()
print("* synced properties for the first time")
properties, relays = cache_properties() #this func returns two dictionaries
vent_counter, tries = 0,0

pwm_sigs_now = { # last Value is if it needs to change still
	"pwm_fog": [3, 0, True],
	"pwm_turb": [10, 0, True], 
	"pwm_vent": [9, 0, True]
	}

for fan in pwm_sigs_now:
	if pwm_sigs_now[fan][2]:
		pwm_sigs_now[fan][2] = False
		response = send_update_sig(pwm_ser, pwm_sigs_now[fan][0], pwm_sigs_now[fan][1])
		if response:
			print(f"- success on {fan} with {pwm_sigs_now[fan][1]}%")
		else:
			print(response)

print("* started the fans, should be running now")

def update_rl_arr(serial_object, ID):
	#expecting a key for a list as input that has the following format: [timer, ontime, offtime, state]

	timer, ontime, offtime, state = 0, 1, 2, 3
	# relays[ID][state] = str(relays[ID][state]) 
	relays[ID][timer] -= 1	
	if relays[ID][timer] < 1:
		print(f"relay {ID} has reached 0, swapping timers..")
		relays[ID][timer] = relays[ID][ontime] if relays[ID][state]	== "off" else relays[ID][offtime] # set timer to ontime if the old state was off
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
	vent_counter += 1
	# print(vent_counter)
	if vent_counter >= 10:
		result = get_auto_pwm()
		if result != pwm_sigs_now["pwm_vent"][1] and result != False:
			pwm_sigs_now["pwm_vent"] = [9, result, True]

	if last_modified != os.path.getmtime(REMOTE_PROPERTIES):
		last_modified = os.path.getmtime(REMOTE_PROPERTIES)
		print("props have changed, sync process starting")
		pwm_sigs_now = get_pwm_changes(pwm_sigs_now) #working with "properties" before it gets updated
		# print(f"changed_pwm_sigs: {pwm_sigs_now}")
		sync_properties() #saving remotely modified data locally
		properties, relays = cache_properties() #this func returns two dictionaries
		print("SYNC DONE")
	
	update_fans()		

	# doing relay tasks
	for relay in relays:
		# print("updating relay", relay)
		update_rl_arr(relay_ser, relay)

