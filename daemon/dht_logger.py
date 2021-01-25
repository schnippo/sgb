#this is an acustomed script, that only tries to log from the dht_sensor


import Adafruit_DHT
from time import sleep


#this script is inspired by dht_adafruit_test.py and aims to replace dht_logger_old.py

#dht_device = adafruit_dht.DHT22(board.D2)

PIN = 4 #GPIO4 on the board, see https://microcontrollerslab.com/wp-content/uploads/2019/12/Raspberry-Pi-pinout.png
SENSOR = Adafruit_DHT.DHT22


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
#humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)

def get_at():
    #return round(Adafruit_DHT.read_retry(SENSOR, PIN)[1], 2) # return the second value(temp) rounded to two digits
    return Adafruit_DHT.read_retry(SENSOR, PIN)[1]
def get_ah():
    #return round(Adafruit_DHT.read_retry(SENSOR, PIN)[0], 2) # return the first value(humidity) rounded to two digits
    return Adafruit_DHT.read_retry(SENSOR, PIN)[0]

if __name__ == "__main__":
    for i in range(5):
        print("temp: ", get_at())
        print("hum: ", get_ah())
