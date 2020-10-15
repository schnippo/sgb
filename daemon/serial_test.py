import serial
from time import sleep

devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]

def try_devices():
	for device in devices:
		with serial.Serial(device) as ser:
			try:
				ser.write("9".encode())
				sleep(2)
				print(ser.readline().decode())
			except:
				print("error at", device)
			

try_devices()