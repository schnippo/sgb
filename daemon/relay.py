from daemon import relays

def update_rl_arr(_id):
	#expecting a list as input with the following format: [timer, ontime, offtime, state]
	relays[str(_id)][0] -= 1	
	if relays[str(_id)][0] < 1:
		relays[str(_id)][0] = relays[str(_id)][1] if relays[str(_id)][3]	== "off" else relay[str(_id)][2] # set timer to ontime if the old state was off
		relays[str(_id)][3] = "off" if relays[str(_id)][3] == "on" else "on" #set state to off if 
		send_flip_token(_id)

def send_flip_token(serial_object,_id):
	serial_object.write(_id.encode())