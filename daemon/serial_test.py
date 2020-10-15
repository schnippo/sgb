import serial
from time import sleep

devices = ["/dev/ttyACM0", "/dev/ttyACM1"]

def try_devices():
	for device in devices:
		with serial.Serial(device) as ser:
			try:
				ser.write("9".encode())
				sleep(2)
				answer = ser.readline().decode()
				if answer == "pwm_controller" or answer == "relay_controller"
					print(device, ":", answer)
				ser.write("99".encode())
				sleep(2)
				answer = ser.readline().decode()
				if answer == "pwm_controller" or answer == "relay_controller"
					print(device, ":", answer)
			except:
				print("error at", device)
			

try_devices()