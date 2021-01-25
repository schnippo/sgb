#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from serial_test import get_address
from time import sleep
ser = serial.Serial(get_address("fan_controller"))
print(ser)
input("go on? ")
ser.write("3,0".encode())
sleep(1)
ser.write("9,0".encode())
sleep(1)
ser.write("10,0".encode())
print("fans should be off now, exiting.")
