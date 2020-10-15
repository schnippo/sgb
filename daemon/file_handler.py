import os, time

REMOTE_PROPERTIES_PATH = "/home/jonas/git/ssgb/daemon/local_properties"


def sync_properties():
	with open("local_properties", "w") as d:
			with open("remote_properties", "r") as s:
				d.write(s.read())


def cache_properties():
	properties = {}
	relays = {}
	with open("local_properties", "r") as f:
		data = f.readlines()
		for line in data:
			values = line.split()
			if values[0] == "relay":
				relays[values[1]] = [values[2], values[3], values[4], values[5]]
			else:
				properties[values[0]] = values[1]
		return [properties, relays]

PROPERTIES_PATH = '/home/jonas/git/ssgb/daemon/remote_properties'

def save_props_and_relays(relays_to_save, properties_to_save, path=REMOTE_PROPERTIES_PATH):
	with open(path, "w") as f:
		for key in relays_to_save:
			f.write(f"relay {key} {relays_to_save[key][0]} {relays_to_save[key][1]} {relays_to_save[key][2]} {relays_to_save[key][3]}\n")
		for key in properties_to_save:
			f.write(f"{key} {properties_to_save[key]}\n")

#key can be just a key for properties or the id for relays
def update_prop_or_relay(key, newvalue, path=PROPERTIES_PATH):
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

# def update_relay(_id, values, path=PROPERTIES_PATH):
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




def get_prop_value(prop):
	properties = {}
	lines = open("properties", "r").readlines()
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