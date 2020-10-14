import serial
ser = serial.Serial()


def update_rl_arr(_id):
	#expecting a list as input with the following format: [timer, ontime, offtime, state]
	int(relay[str(_id)][0]) -= 1	
	if relay[str(_id)][0] < 1:
		relay[str(_id)][0] = relay[str(_id)][1] if relay[str(_id)][3]	== "off" else relay[str(_id)][2] # set timer to ontime if the old state was off
		relay[str(_id)][3] = "off" if relay[str(_id)][3] == "on" else "on" #set state to off if 
		send_flip_token(_id)

def send_flip_token(_id):
	ser.write(_id.encode())