LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"

from file_handler import cache_properties, sync_properties, update_prop_or_relay, get_pwm_changes
from pwm import update_auto_pwm, send_update_sig
from time import sleep
import os, serial







last_modified = os.path.getmtime(REMOTE_PROPERTIES)
relay_ser = serial.Serial("/dev/ttyACM0")
pwm_ser = serial.Serial("/dev/ttyACM1")
print("serial connections established")
sync_properties()
print("synced properties for the first time")
properties, relays = cache_properties() #this func returns two dictionaries
vent_counter, tries = 0,0

pwm_start_sigs = {"3": 35, "10": 40, "9": 40}

for ID in pwm_start_sigs:
	print(send_update_sig(pwm_ser, ID, pwm_start_sigs[ID]))
# print("started the fans, should be running now")

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




while True:
	sleep(1)
	# vent_counter += 1
	# print(vent_counter)
	# if vent_counter >= 10:
	# 	if update_auto_pwm() == True:
	# 		print("automatically updated vent pwm")
	# 		tries, vent_counter = 0,0
	# 	elif update_auto_pwm() == "auto-mode is off":
	# 		print("auto-mode is off, turn it on via web interface")
	# 		tries, vent_counter = 0,0
	# 	else:
	# 		tries += 1
	# 		print(f"dht-error, couldn't get temp, trying again next cycle, tries: {tries}")

	#getting new properties in
	
	if last_modified != os.path.getmtime(REMOTE_PROPERTIES):
		print("props have changed, SYNC PROCESS STARTING")
		changed_pwm_sigs = get_pwm_changes(properties, REMOTE_PROPERTIES) #working with "properties" before it gets updated
		print(f"changed_pwm_sigs: {changed_pwm_sigs}")
		
		if changed_pwm_sigs:
			for fan in changed_pwm_sigs:				
				sent_successfully = send_update_sig(pwm_ser, changed_pwm_sigs[0], changed_pwm_sigs[1])
				print(f"sent update sig to {fan}(Pin {changed_pwm_sigs[0]}), with value {changed_pwm_sigs[1]}%")
				print(f"Answer Code Code: {sent_successfully}")			
		else:
			print("not sending any sigs, nothing changed")		
		sync_properties() #saving remotely modified data locally
		properties, relays = cache_properties() #this func returns two dictionaries
		print("SYNC DONE")
		last_modified = os.path.getmtime(REMOTE_PROPERTIES)
	
	#doing relay tasks
	# for relay in relays:
	# 	print("updating relay", relay)
	# 	update_rl_arr(relay_ser, relay)

