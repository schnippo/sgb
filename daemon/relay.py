from daemon import relays

def update_rl_arr(ID):
	timer = 0
	ontime = 1
	offtime = 2
	state = 3
	#expecting a list as input with the following format: [timer, ontime, offtime, state]
	relays[str(ID)][timer] -= 1	
	if relays[str(ID)][timer] < 1:
		relays[str(ID)][timer] = relays[str(ID)][ontime] if relays[str(ID)][state]	== "off" else relay[str(ID)][offtime] # set timer to ontime if the old state was off
		relays[str(ID)][3] = "off" if relays[str(ID)][3] == "on" else "on" #set state to off if 
		send_flip_token(ID)

def send_flip_token(serial_object,ID):
	serial_object.write(ID.encode())