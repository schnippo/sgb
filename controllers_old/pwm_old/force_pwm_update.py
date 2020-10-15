import serial, sys, os
from classes import scan_for_response, get_prop_value



# devices = ["/dev/ttyACM2", "/dev/ttyACM1", "/dev/ttyACM0", "/dev/ttyACM3"]

os.system("kill `fuser /dev/ttyACM0 2>/dev/null`")
with serial.Serial("/dev/ttyACM0") as ser:
	print(ser.isOpen)

	while not (ser.isOpen) :
	    print("trying to connect to fan-controller on " + port + ": pending")
	print("connecting to fan-controller on " + port + ": done")

	try:
	    fan_nr = sys.argv[1]
	    pwm_sig = int(sys.argv[2])
	    pwm_sig = min(pwm_sig, 100)
	except IndexError:
	    print("Assuming that there is no direct input, this must be a automatic systemcall\nCan specify fan-nr[3(fogfan),9(in- & outtake), 10(turbulence)] and pwm[0-100%] directly if needed")
	    fan_nr = 9
	    pwm_sig = get_prop_value("pwm_dutycyle")
	    

	ser.write((str(fan_nr) + "," + str(pwm_sig * 10.23)).encode())
