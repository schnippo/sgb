#returns both 1W and I2C sensor values - only one I2C device


import glob
import os
import adafruit_dht
from time import sleep
## ONEWIRE SETUP
os.system('modprobe w1-gpio')                              # load one wire communication device kern$
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from $
device_file = device_folder + '/w1_slave'                  # store the details
def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':                   # ignore first line
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')                        # find temperature in the details
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0                 # convert to Celsius
      return temp_c



## I2C Setup
dht_device = adafruit_dht.DHT22(2)

while True:
        print("I2C-Temp: " + str(dht_device.temperature))
        print("I2C-Hum: " + str(dht_device.humidity))
        print("1W-Temp: " + str(read_temp()))
        sleep(2)