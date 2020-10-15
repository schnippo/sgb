#README: This script updates the ventilation pwm(pin 9) automatically based on the temp and hum
#values of the last N minutes -> specify this number of minutes in the properties file, after "auto_update_reference"
LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"


from file_handler import get_prop_value, update_prop_or_relay, avg_lastNlines
from dht_logger import get_at



def update_auto_pwm():
	if get_prop_value("pwm_mode") == "manual":
	    print("pwm_mode is on manual, exiting..")
	    return "auto-mode is off"

	opt_temp = int(get_prop_value("opt_temp"))
	# opt_hum = get_prop_value("ah_threshold")
	std_pwm = int(get_prop_value("std_pwm"))
	max_delta_t = int(get_prop_value("max_delta_t"))
	# max_delta_h = get_prop_value("max_delta_h")
	pwm_boost_t = 0

	curr_temp = get_at()
	# curr_temp = 23
	if not curr_temp:
		return False

	delta_t = curr_temp - opt_temp #subtract the smaller from the greater (supposing that we need to cool down, the current temp is above the threshold)

	if delta_t > 0: #only act if necessary
	    pwm_boost_t = (delta_t * (100 - std_pwm) / max_delta_t ) #multiplies delta_t with a factor, that is based on how far i assume i need to go
	    # print(f"pwm boost is {pwm_boost_t}")
	else:
	    pwm_boost_t = 0
	    # print(f"pwm_boost is 0, staying on {std_pwm}% pwm and exiting...")
	    return True

	new_pwm = min(100, round(std_pwm + pwm_boost_t, 2)) #dont go over 100%
	# print(f"new pwm value is {new_pwm}%, writing to properties")

	update_prop_or_relay("pwm_dutycycle", str(new_pwm), REMOTE_PROPERTIES) # write it to properties.
	return True


def send_update_sig(serial_object, _id, dutycycle):
	serial_object.write(f"{_id},{int(dutycycle * 10.23)}".encode())















# def get_sigs_to_send(old_sigs, updated_file=REMOTE_PROPERTIES): #old_sigs are expected to be a dictionary
# # also: old_sigs can just be properties, logic, right?
# 	sigs_to_send = {}
# 	for key in old_sigs:
# 		if old_sigs[key] == get_prop_value(key, REMOTE_PROPERTIES):
# 			continue
# 		else:
# 			sigs_to_send[key] = get_prop_value(key, REMOTE_PROPERTIES)
# 	return sigs_to_send


# old_sigs = {}

# def update_in_old_sig(signals): #signal needs to be in dictionary format
# 	for key in signals:
# 		old_sigs[key] = signals[key]

	""" HERLEITUNG DER FORMEL:
	Ich gehe von 40% std_pwm aus, es bleiben also noch 60% welche ich auf die von mir angenommen moeglichen Temperaturschwankungen
	aufteile. BSP: Wir nehmen an, dass der Maximalwert der Temp auf max 3° ueber dem Normalwert liegt, ganz naiv angenommen:
	Dann teile ich also die dynamischen 60% auf diese 3° Auf und erhoehe somit um 20% PWM leistung pro ein Grad.

	Ich lasse den LF Teil vorerst raus, der Einfachheit halber und weil sie einen geringeren Einfluss auf die Pflanzen hat, als die Temp.

	"""