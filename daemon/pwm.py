#README: This script updates the ventilation pwm(pin 9) automatically based on the temp and hum
#values of the last N minutes -> specify this number of minutes in the properties file, after "auto_update_reference"


from file_handler import get_prop_value, update_prop, avg_lastNlines
import logger


def update_auto_pwm():
	if get_prop_value("pwm_mode") == "manual":
	    print("pwm_mode is on manual, exiting..")
	    exit()

	opt_temp = int(get_prop_value("at_threshold"))
	# opt_hum = get_prop_value("ah_threshold")
	std_pwm = int(get_prop_value("std_pwm"))
	max_delta_t = int(get_prop_value("max_delta_t"))
	# max_delta_h = get_prop_value("max_delta_h")
	pwm_boost_t = 0

	curr_temp = get_at()

	delta_t = curr_temp - opt_temp #subtract the smaller from the greater (supposing that we need to cool down, the current temp is above the threshold)

	# print(f"delta t is {delta_t}")
	# delta_h = curr_hum - opt_hum # here we also suppose that we need to vent, cuz it's too humid

	if delta_t > 0: #only act if necessary
	    pwm_boost_t = (delta_t * (100 - std_pwm) / max_delta_t ) #multiplies delta_t with a factor, that is based on how far i assume i need to go
	    # print(f"pwm boost is {pwm_boost_t}")
	# elif delta_h > 0: #           ca. 60%      geteilt durch 3°  -> delta_t wird also mit diesen 20%/° multipliziert.
	#     pwm_boost_h,pwm_boost_t = 0,0
	else:
	    pwm_boost_t = 0
	    # print(f"pwm_boost is 0, staying on {std_pwm}% pwm and exiting...")
	    exit()

	new_pwm = min(100, round(std_pwm + pwm_boost_t, 2)) #dont go over 100%
	# print(f"new pwm value is {new_pwm}%, writing to properties")

	update_prop("pwm_dutycycle", str(new_pwm), "remote_properties") # write it to properties.


	""" HERLEITUNG DER FORMEL:
	Ich gehe von 40% std_pwm aus, es bleiben also noch 60% welche ich auf die von mir angenommen moeglichen Temperaturschwankungen
	aufteile. BSP: Wir nehmen an, dass der Maximalwert der Temp auf max 3° ueber dem Normalwert liegt, ganz naiv angenommen:
	Dann teile ich also die dynamischen 60% auf diese 3° Auf und erhoehe somit um 20% PWM leistung pro ein Grad.

	Ich lasse den LF Teil vorerst raus, der Einfachheit halber und weil sie einen geringeren Einfluss auf die Pflanzen hat, als die Temp.

	"""