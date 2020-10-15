import sys, glob, os, adafruit_dht, datetime, board
from time import sleep

# logfile_air_temp = "logs/at_log"
# logfile_air_hum = "logs/ah_log"
# logfile_water_temp = "logs/wt_log"

# int # tries = 0

## ONEWIRE SETUP

os.system('modprobe w1-gpio')                              # load one wire communication device kern$
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from $
device_file = device_folder + '/w1_slave' 

# def reset_file(file):
#    f = open(file, "w")
#    f.write("")
#    f.close
# store the details

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':                   # ignore first line
      sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')                        # find temperature in the details
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0                 # convert to Celsius
      return temp_c

## I2C Setup => temp and hum sensor
dht_device = adafruit_dht.DHT22(board.D2)

# reset_file(logfile_air_temp)
# reset_file(logfile_air_hum)
# reset_file(logfile_water_temp)


logat = open(logfile_air_temp, "a")
logah = open(logfile_air_hum, "a")
logwt = open(logfile_water_temp, "a")
# print("new logcycle")

def get_at():
  tries = 0
  while True: #TRYING TO GET AIR TEMP
      now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))    
      tries+= 1
      try:
          temp = dht_device.temperature
          return round(temp, 2)
          # logat.write(now + " "+str(dht_device.temperature)+"\n")
          # logat.close() #safe if done
          # print("air temp done")
          break
      except: #a potential jitter connection is handled here, just wait a second and try again
          print(sys.exc_info()[0] + "on air hum, trying again in 1s")
          sleep(1)
          if tries > 3:
            return "NA"
            # logat.write(now + " \n")
            break
          continue
def get_ah():
  tries = 0        
  while True: #TRYING TO GET AIR HUM
      now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))    
      tries += 1
      try:
          hum = dht_device.temperature
          return round(hum, 2)
          # logah.write(now + " "+str(dht_device.humidity)+"\n")
          # logah.close() #safe if done
          # print("air hum done")
          break
      except: #a potential jitter connection is handled here, just wait a second and try again
          print(sys.exc_info()[0] + "on air hum, trying again in 1s")
          sleep(1)
          if tries > 3: #escape the loop after the third try
              return None
              # logah.write(now + " \n")
              break
          continue
# def get_wt():
#   tries = 0
#   while True: #TRYING TO GET WATER TEMP
#       now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))    
#       tries += 1
#       try:
#           wtemp = read_temp()
#           return round(wtemp, 2)
#           # logwt.write(now + " "+str(read_temp)+"\n")
#           # logwt.close()
#           # print("water temp done")
#           break
#       except: #a potential jitter connection is handled here, just wait a second and try again
#           print(sys.exc_info()[0] + "on water temp, trying again in 1s")
#           sleep(1)
#           if tries > 3:
#               return None
#               # logwt.write(now + " \n")
#               break
#           continue

# print("DONE")