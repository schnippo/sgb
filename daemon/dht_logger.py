#this is an acustomed script, that only tries to log from the dht_sensor


import sys, adafruit_dht, board
from time import sleep

dht_device = adafruit_dht.DHT22(board.D2)

def get_at():
  tries = 0
  while True: #TRYING TO GET AIR TEMP
      tries+= 1
      try:
          temp = dht_device.temperature #CRITICAL
          return round(temp, 2)
          break
      except: #a potential jitter connection is handled here, just wait a second and try again
          print(str(sys.exc_info()[0]) + "on air temp, trying again in 1s")
          sleep(1)
          if tries > 3:
            return None
            break
          continue



def get_ah():
  tries = 0        
  while True: #TRYING TO GET AIR HUM
      tries += 1
      try:
          hum = dht_device.temperature #CRITICAL
          return round(hum, 2)
          break
      except: #a potential jitter connection is handled here, just wait a second and try again
          print(str(sys.exc_info()[0]) + "on air hum, trying again in 1s")
          sleep(1)
          if tries > 3: #escape the loop after the third try
              return None
              break
          continue



# Tryout

# while True:
# 	sleep(2)
# 	print(get_at())