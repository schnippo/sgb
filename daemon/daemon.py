from time import sleep, time
import os, serial, relay, ard_auth
from file_handler import cache_properties, sync_properties, update_prop_or_relay
from pwm import update_auto_pwm, send_update_sig, get_sigs_to_send


LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/web/remote_properties"


def get_serial(flag):
	devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
	for device in devices:
		try:
			ser = serial.Serial(device)
			ser.write("9".encode())
			sleep(2)
			if ser.readline() == f"{flag}\r\n":
				print(f"{flag} at {device}")
				return ser
		except serial.SerialException:
			print("bad address: ", device)
			continue


last_modified = os.path.getmtime("remote_properties")
relay_ser = get_serial("relay_controller")
pwm_ser = get_serial("pwm_controller")
properties, relays = cache_properties() #this func returns two dictionaries





while True:
	sleep(1)
	#getting new properties in
	if last_modified != os.path.getmtime("remote_properties"):
		changed_pwm_sigs = get_pwm_changes(properties, REMOTE_PROPERTIES) #working with "properties" before it gets updated
		send_update_sig(pwm_ser, changed_pwm_sigs[0], changed_pwm_sigs[1])
		sync_properties() #saving remotely modified data locally
		properties, relays = cache_properties() #this func returns two dictionaries
		last_modified = os.path.getmtime("remote_properties")
	#doing relay tasks
	for relay in relays:
		print("updating relay", relay)
		update_rl_arr(relay)




