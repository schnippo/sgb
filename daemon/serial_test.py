import serial
from time import sleep

addresses = ["/dev/ttyACM0", "/dev/ttyACM1"]

devices = [serial.Serial(addresses[0]), serial.Serial(addresses[1])]


for device in devices:
	try:
		device.write("9".encode())
		sleep(2)
		answer = device.readline().decode()
		if answer == "pwm_controller" or answer == "relay_controller":
			print(device, ":", answer)
			continue
		else:
			device.write("99".encode())
			sleep(2)
			answer = device.readline().decode()
			if answer == "pwm_controller" or answer == "relay_controller":
				print(device, ":", answer)
	except:
		print("error at", device)
			

try_devices()