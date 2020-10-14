def get_prop_value(prop):
	properties = {}
	lines = open("properties", "r").readlines()
	for line in lines:
		properties[line.split()[0]] = line.split()[1]
	return properties[prop]



def update_prop(prop, value):
	properties = {}
	lines = open(PROPERTIES_PATH, "r").readlines()
	for line in lines:
		properties[line.split()[0]] = line.split()[1]
	properties[prop] = value
	with open("properties", "w") as f:
		for key in properties:
			f.write(key + " " + properties[key] +"\n")


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
