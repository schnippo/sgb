def get_arduino_response(device, msg):
    with serial.Serial(device, 9600) as ser:
        ser.write(msg.encode())
        time.sleep(.3)
        # while ser.in_waiting  0:
        #     msg0 = ser.readline() #emptying the input buffer
        return str(ser.read(200).decode())


def scan_for_response(target, devices):
    # print("target ID: " + str(target))
    for addr in devices:
        try:
            if (get_arduino_response(addr, "9") == str(target)+"\r\n"):
                print("success, address is " + addr)
                return addr
        except serial.SerialException:
            print("bad address: " + addr)
            continue