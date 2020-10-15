from file_handler import cache_properties, sync_properties, update_prop_or_relay
from pwm import update_auto_pwm, send_update_sig
from time import sleep
import os, serial

LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"




last_modified = os.path.getmtime(REMOTE_PROPERTIES)
relay_ser = serial.Serial("/dev/ttyACM1")
pwm_ser = serial.Serial("/dev/ttyACM0")
properties, relays = cache_properties() #this func returns two dictionaries
from relay import update_rl_arr
vent_counter, tries = 0,0




while True:
	sleep(1)
	vent_counter += 1
	if vent_counter >= 10:
		if update_auto_pwm() == True:
			print("automatically updated vent pwm")
			tries, vent_counter = 0,0
		elif update_auto_pwm() == "auto-mode is off":
			tries, vent_counter = 0,0
		else:
			tries += 1
			print(f"dht-error, couldn't get temp, trying again next cycle, tries: {tries}")

	#getting new properties in
	if last_modified != os.path.getmtime(REMOTE_PROPERTIES):
		changed_pwm_sigs = get_pwm_changes(properties, REMOTE_PROPERTIES) #working with "properties" before it gets updated
		send_update_sig(pwm_ser, changed_pwm_sigs[0], changed_pwm_sigs[1])
		sync_properties() #saving remotely modified data locally
		properties, relays = cache_properties() #this func returns two dictionaries
		last_modified = os.path.getmtime(REMOTE_PROPERTIES)
	#doing relay tasks
	for relay in relays:
		print("updating relay", relay)
		update_rl_arr(relay)


