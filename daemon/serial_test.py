import serial, subprocess
from time import sleep


def get_address(flag, try_usb_reset=False):
    addresses, devices = [], []
    list_addresses_sp = subprocess.Popen("ls -d /dev/* | grep /dev/ttyACM",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True)
    addresses = list_addresses_sp.communicate()[0].split()
    print(f"available addresses after first try: {addresses}")
    if len(addresses) < 2:
        if try_usb_reset:
            print("addresses missing, trying to reset usb power...")
            reset_usb_ports_sp = subprocess.Popen("sudo uhubctl -a 2 -l 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
            rc = reset_usb_ports_sp.wait()
            sleep(2) # wait for the OS to detect the arduinos again, this takes up to 2s.
            list_addresses_sp = subprocess.Popen("ls -d /dev/* | grep /dev/ttyACM",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True)
            addresses = list_addresses_sp.communicate()[0].split()
            print(f"available addresses after usb_reset: {addresses}")
            if len(addresses) < 2:
                print("addresses are still missing, replug wires (might wanna try the relay power cord)\nexiting...")
                exit(1)
        print("missing addresses, check wiring or specify try_usb_reset=True.\nexiting...")
        exit(1)
    for address in addresses:
        try:
            devices.append(serial.Serial(address, timeout=3))
        except Exception as msg:
            print("encountered an error")
            print(msg)
            if flag == "relay_controller":
                reset_relays(address)
                get_address(flag)  #start new from the beginning.
            #print(devices)
    for device in devices:
        device.write("7".encode())
        sleep(1)
        answer = device.readline()
        #print(f"{device.port}: {answer.decode()}")
        if answer.decode() == f"{flag}\r\n":
            return device.port


def reset_relay(address):
    ser = serial.Serial(address)
    ser.write("9".encode())

if __name__ == "__main__":
    print("called as main file!")
    print(get_address("fan_controller"))
