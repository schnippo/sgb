from time import sleep, time
import os, serial, relay, ard_auth
from file_handler import cache_properties, sync_properties, update_prop_or_relay
from pwm import update_auto_pwm, send_update_sig


LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"


# def get_serial(flag):
# 	devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
# 	for device in devices:
# 		try:
# 			ser = serial.Serial(device)
# 			ser.write("9".encode())
# 			sleep(2)
# 			if ser.readline() == f"{flag}\r\n":
# 				print(f"{flag} at {device}")
# 				return ser
# 		except serial.SerialException:
# 			print("bad address: ", device)
# 			continue
def get_serial_devices():
	devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
	ser_relay, pwm_ser = None
	i = 0
	while ser_relay == None:
		for device in devices:
			try:
				ser_relay = serial.Serial(device, timeout=3)
				ser_relay.write("9".encode())
				sleep(2)
				if ser_relay.readline() == "relay_controller\r\n":
					break
				else:
					print(f"answer from {device} didn't mach 'relay_controller', try {i}")
					continue
			except serial.SerialException:
				print("bad address: ", device)
				continue

	while ser_pwm == None:
			for device in devices:
				try:
					ser_pwm = serial.Serial(device, timeout=3)
					ser_pwm.write("9".encode())
					sleep(2)
					if ser_pwm.readline() == "pwm_controller\r\n":
						break
					else:
						print(f"answer from {device} didn't mach 'relay_controller', try {i}")
						continue
				except serial.SerialException:
					print("bad address: ", device)
					continue
	return ser_relay, ser_pwm


print("tryna get serial connections in: ")
relay_ser, pwm_ser = get_serial_devices()
print("CHECK")

last_modified = os.path.getmtime(REMOTE_PROPERTIES)
# relay_ser = get_serial("relay_controller")
# pwm_ser = get_serial("pwm_controller")
properties, relays = cache_properties() #this func returns two dictionaries



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


