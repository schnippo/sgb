import serial
from time import sleep

def get_address(flag):
	addresses = ["/dev/ttyACM0", "/dev/ttyACM1"]
	devices = [serial.Serial(addresses[0]), serial.Serial(addresses[1])]
	for device in devices:
		device.write("99".encode())
		sleep(2)
		answer = device.readline()
		# print(f"{device.port}: {answer.decode()}")
		if answer.decode() == f"{flag}\r\n":
			return device.port
		else:
			continue
			

# print(get_address("fan_controller"))