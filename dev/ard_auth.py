#until now hopeless tries to advance the serial authentication, i think it works fine if i 
#just tell the daemon which ports to use
import serial, time


def get_arduino_response(device, msg):
    with serial.Serial(device, 9600) as ser:
        ser.write(msg.encode())
        time.sleep(.3)
        # while ser.in_waiting  0:
        #     msg0 = ser.readline() #emptying the input buffer
        return str(ser.readline().decode())


def scan_for_response(target, devices):
    # print("target ID: " + str(target))
    for addr in devices:
        try:
            if (get_arduino_response(addr, "9") == str(target)):
                print("success, address is " + addr)
                return addr
        except serial.SerialException:
            print("bad address: " + addr)
            continue

# def get_serial(flag):
#   devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
#   for device in devices:
#       try:
#           ser = serial.Serial(device)
#           ser.write("9".encode())
#           sleep(2)
#           if ser.readline() == f"{flag}\r\n":
#               print(f"{flag} at {device}")
#               return ser
#       except serial.SerialException:
#           print("bad address: ", device)
#           continue
def get_serial_devices():
    devices = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]
    ser_relay, ser_pwm = None, None
    i = 0
    while ser_relay == None:
        for device in devices:
            try:
                ser_relay = serial.Serial(device, timeout=3)
                ser_relay.write("9".encode())
                time.sleep(2)
                if ser_relay.readline() == "relay_controller\r\n":
                    break
                else:
                    print(f"answer from {device} didn't match 'relay_controller', try {i}")
                    continue
            except serial.SerialException:
                print("bad address: ", device)
                continue

    while ser_pwm == None:
            for device in devices:
                try:
                    ser_pwm = serial.Serial(device, timeout=3)
                    ser_pwm.write("9".encode())
                    time.sleep(2)
                    if ser_pwm.readline() == "pwm_controller\r\n":
                        break
                    else:
                        print(f"answer from {device} didn't match 'pwm_controller', try {i}")
                        continue
                except serial.SerialException:
                    print("bad address: ", device)
                    continue
    return ser_relay, ser_pwm




if __name__ == "__main__": 
    #get_arduino_response("/dev/ttyACM0", "9")
    devices1 = ["/dev/ttyACM0", "/dev/ttyACM1"]
    scan_for_response("relay_controller", devices1)
