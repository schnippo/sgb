# import time, serial, sys
from classes import *

print(RelayTimer.ser)

rl1 = RelayTimer(1, 0, 0, "off")
rl2 = RelayTimer(2, 0, 0, "off")
rl3 = RelayTimer(3, 0, 0, "off")
rl4 = RelayTimer(4, 0, 0, "off")

relays = [rl1, rl2, rl3, rl4]

file = "./rl_update_args"

while True:
    # time.sleep(0.5)
    reinit_timers_via_extern(file, relays)
    reactivate_inactive_timers(relays)
