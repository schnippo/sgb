LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"

import os, time




def sync_properties():
	with open(LOCAL_PROPERTIES, "w") as d:
			with open(REMOTE_PROPERTIES, "r") as s:
				d.write(s.read())


def cache_properties(existing_relays=None):
	myproperties = {}
	myrelays = {}
	with open(LOCAL_PROPERTIES, "r") as f:
		data = f.readlines()
		for line in data:
			values = line.split()
			#print(f"splitted line: {values}")
			if values[0] == "relay":
                                #print("existing relays: ", existing_relays) 
                                if existing_relays is None: #get some default values
                                        values[2] = 0  if values[2] == "persist" else values[2] #if there is no prior data, give the values 0s
                                        values[3] = 10 if values[3] == "persist" else values[3]# 10s ontime
                                        values[4] = 20 if values[4] == "persist" else values[4]# 10s offtime
                                elif existing_relays is not None: #get already existing values
                                        print(f"old timer {values[1]} persists: {existing_relays[values[1]][1]}")
                                        values[2] = existing_relays[values[1]][0] if values[2] == "persist" else values[2]
                                        values[3] = existing_relays[values[1]][1] if values[3] == "persist" else values[3]
                                        values[4] = existing_relays[values[1]][2] if values[4] == "persist" else values[4]
                                elif values[2] == "inactive":#or be inactive
                                    print(f"relay {values[1]} now inactive")
                                #print("values: ",values)
                                myrelays[values[1]] = [values[2], int(values[3]), int(values[4]), values[5]]
			else:
				myproperties[values[0]] = values[1]
		return [myproperties, myrelays]

def get_new_pwm(current_pwm_sigs, remote_properties=REMOTE_PROPERTIES): #checks if the remote_properties have sth new for the static fans (turb and fogfan)
	new_pwm_sigs = current_pwm_sigs
	for fan in current_pwm_sigs:
		# print(fan)
		local_val, remote_val = current_pwm_sigs[fan][1], get_prop_value(fan, remote_properties)
		print(f"{fan} old value: {local_val}, remoteval: {remote_val}")
		if local_val != remote_val:
                        new_pwm_sigs[fan][1], new_pwm_sigs[fan][2] = remote_val, True # update the value and the NTC (Needs To Change) 
		else:
                    print(f"nothing changed in {fan}, moving on")
	return new_pwm_sigs


def save_props_and_relays(relays_to_save, properties_to_save, path=REMOTE_PROPERTIES):
	with open(path, "w") as f:
		for key in relays_to_save:
			f.write(f"relay {key} {relays_to_save[key][0]} {relays_to_save[key][1]} {relays_to_save[key][2]} {relays_to_save[key][3]}\n")
		for key in properties_to_save:
			f.write(f"{key} {properties_to_save[key]}\n")

#key can be just a key for properties or the id for relays
def update_prop_or_relay(key, newvalue, path=REMOTE_PROPERTIES):
	properties = {}
	relays = {}
	with open(path, "r") as f:
		for line in f.readlines():
			values = line.split()
			if values[0] == "relay":
				if values[1] == key: #check if i can already overwrite the old stuff
					relays[key] = newvalue #as we expect to change a relay, "newvalue" should be a list.
				else:
					relays[values[1]] = [values[2], values[3], values[4], values[5]] # if it didn't match, write the normal values instead
			elif values[0] == key:
				properties[key] = newvalue #and if it wasn't a relay, just save it as a property. Here it doesn't need to be a list.
			else:
				properties[values[0]] = values[1]
	save_props_and_relays(relays, properties, path)	#save them all

# def update_relay(_id, values, path=LOCAL_PROPERTIES):
# 	relays = {}
# 	properties = {}
# 	with open(path, "r") as f.
# 		for line in f.readlines():
# 			values = line.split()
# 			if values[0] == "relay":
# 				relays[values[1]] = [values[2], values[3], values[4], values[5]]
# 			else:
# 				properties[values[0]] = values[1]
# 		for key in relays:
# 			if key == _id:
# 				relays[key] = values # update the values




def get_prop_value(prop, path=REMOTE_PROPERTIES):
	properties = {}
	lines = open(path, "r").readlines()
	for line in lines:
		properties[line.split()[0]] = line.split()[1]
	return properties[prop]

def get_prop_value(prop, path=REMOTE_PROPERTIES):
	properties = {}
	with open(path, "r") as f:
		for line in f.readlines():
			properties[line.split()[0]] = line.split()[1]
	return properties[prop]



def avg_lastNlines(file, N):
	total = 0
	with open(file, "r") as f:
		for line in (f.readlines() [-N:] ):
			try:
				# print(line)
				total += int(line)
			except TypeError as msg:
				print(msg)
				continue
		return round(total/N, 2)
