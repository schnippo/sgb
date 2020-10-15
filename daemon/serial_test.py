import serial
from time import sleep

addresses = ["/dev/ttyACM0", "/dev/ttyACM1"]

devices = [serial.Serial(addresses[0]), serial.Serial(addresses[1])]

print("hello")
print(devices)

for device in devices:
	try:
		device.write("9".encode())
		sleep(2)
		answer = device.readline()
		print(device, answer)
		if answer.decode() == "pwm_controller\r\n" or answer == "relay_controller\r\n":
			print(device, ":", answer)
			continue
		else:
			device.write("99".encode())
			sleep(2)
			answer = device.readline()
			print(device, answer)
			if answer.decode() == "pwm_controller\r\n" or answer == "relay_controller\r\n":
				print(device, ":", answer)
	except:
		print("error at", device)
			

