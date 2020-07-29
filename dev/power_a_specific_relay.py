import serial
import random
from time import sleep
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
    led_number = '0'
    while True:
        if led_number == '1' or led_number == '2' or led_number == '3' or led_number == '4':
             print("Sending number " + str(led_number) + " to Arduino")
             ser.write(str(led_number).encode('utf-8'))    
             led_number = 0        
        else:
            led_number = input("enter a number from 1 to 4: ")
        