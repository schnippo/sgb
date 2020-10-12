import serial
import sys
from classes import scan_for_response

devices = ["/dev/ttyACM2", "/dev/ttyACM1", "/dev/ttyACM0", "/dev/ttyACM3"]

port = scan_for_response(devices, "fan_controller")
ser = serial.Serial(port, 9600, timeout=3)

while not (ser.isOpen) :
    print("trying to connect to fan-controller on " + port + ": pending")
print("connecting to fan-controller on " + port + ": done")

try:
    fan_nr = sys.argv[1]
    pwm_sig = int(sys.argv[2])
    pwm_sig = min(pwm_sig, 100)
except IndexError:
    print("please specify fan-nr[3(fogfan),9(in- & outtake), 10(turbulence)] and pwm[0-100%]")
    exit(1) 

    

ser.write((str(fan_nr) + "," + str(pwm_sig * 10.23)).encode())
ser.close()
