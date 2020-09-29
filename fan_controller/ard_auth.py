import serial
from time import sleep

devices = ["/dev/ttyACM2", "/dev/ttyACM1", "/dev/ttyACM0"]

def get_arduino_response(device, msg):
    ser = serial.Serial(device, 9600)
    ser.write(msg.encode())
    sleep(.5)
    while ser.in_waiting == 0:
        msg0 = ser.readline() #emptying the input buffer
    return str(ser.readline().decode())


def scan_for_response(addresses, target):
    print("target ID: " + str(target))
    for addr in addresses:
        try:
            if (get_arduino_response(addr, "99") == str(target)):
                # print("success, address is " + addr)
                return addr
        except serial.SerialException:
            print("bad address: " + addr)
            continue