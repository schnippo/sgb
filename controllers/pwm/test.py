import os
port = "/dev/ttyACM0"

os.system("kill `fuser /dev/ttyACM0 2>/dev/null`")