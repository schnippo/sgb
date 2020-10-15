from time import sleep, time
import os, serial, relay, ard_auth
from file_handler import cache_properties, sync_properties, update_prop_or_relay

# import logger

last_modified = os.path.getmtime("remote_properties")


# devices = ["/dev/ttyACM0", "/dev/ttyACM1"]
# relay_ser = serial.Serial(scan_for_response("relay_controller", devices))
# pwm_ser = serial.Serial(scan_for_response("pwm_controller", devices))



# update_prop_or_relay("2", ["13", "10", "10", "on"], "local_properties")
update_prop_or_relay("pwm_turb", "50", "local_properties")


# while True:
# 	sleep(1)
# 	#getting new properties in
# 	if last_modified != os.path.getmtime("remote_properties"):
# 		sync_properties()
# 		properties, relays = cache_properties()
# 		last_modified = os.path.getmtime("remote_properties")
# 	#doing relay tasks
# 	for relay in relays:
# 		update_rl_arr(relay)



"""
TODO:
PWM UPDATE SIG, ONLY IF NECESSARY, DO IT THE SAME WAY WITH ALL 3 FANS, HAVE A PROPERTY,
CHECK IF IT HAS CHANGED, ONLY ACT IF IT CHANGED - EASY.



"""