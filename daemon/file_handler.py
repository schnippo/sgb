LOCAL_PROPERTIES = "/home/pi/git/ssgb/daemon/local_properties"
REMOTE_PROPERTIES = "/home/pi/git/ssgb/web/remote_properties"

import os, time




def sync_properties():
	with open(LOCAL_PROPERTIES, "w") as d:
			with open(REMOTE_PROPERTIES, "r") as s:
				d.write(s.read())


def cache_properties():
	myproperties = {}
	myrelays = {}
	with open(LOCAL_PROPERTIES, "r") as f:
		data = f.readlines()
		for line in data:
			values = line.split()
			if values[0] == "relay":
				myrelays[values[1]] = [values[2], values[3], values[4], values[5]]
			else:
				myproperties[values[0]] = values[1]
		return [myproperties, myrelays]


def get_pwm_changes(properties, remote_properties=REMOTE_PROPERTIES):
	changes = {}
	pin = 0
	for key in properties:
		if key == "pwm_vent" or key == "pwm_fog" or key == "pwm_turb": # find one of the three keys.
			local_val, remote_val = properties[key], get_prop_value(key, remote_properties)
			if local_val != remote_val:
				if key == "pwm_vent":
					pin = 9
				elif key == "pwm_turb":
					pin = 3
				elif key == "pwm_fog":
					pin = 1
				changes[key] = [pin, remote_val]
		return changes


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
	lines = open(LOCAL_PROPERTIES, "r").readlines()
	for line in lines:
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