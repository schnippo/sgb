#https://github.com/adafruit/Adafruit_CircuitPython_DHT

import adafruit_dht
#import RPi.GPIO as GPIO
from time import sleep

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(4, GPIO.IN)

dht_device = adafruit_dht.DHT22(2)

while True:
	print(dht_device.temperature)
	print(dht_device.humidity)
	print("____")
	sleep(2)
