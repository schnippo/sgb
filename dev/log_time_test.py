import datetime, random
from time import sleep

def reset_file(file):
    f = open(file, "w")
    f.write("")
    f.close

reset_file("test_log.txt")


while True:
    log = open("test_log.txt", "a")

    for i in range(3):

        sleep(1)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log.write(str(now + "\n"))
    log.close

log = open("test_log.txt", "r")
for line in log.readlines():
    print(line)