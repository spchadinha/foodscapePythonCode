

import json

###########################################
## Necessary data storage and conversion
###########################################
eco = ["cob", "cbf", "cls", "ifo", "dcb", "euo", "fac", "msc", "mba", "phc", "rac", "usda"]
fair = ["eft", "ffs", "fl", "f", "fw", "fjc", "sps"]
humane = ["aga", "ahc", "awa", "chr", "gap"]
categories = {"eco" : eco, "fair" : fair, "humane" : humane}

days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


convert_eco = {"scratch": "FS","compost":"C", "recycle":"R", "local":"L", "energy":"ES", "beer":"LA", "wine":"LA"}
eco_icon = ["scratch", "compost", "recycle", "local", "energy", "beer", "wine"]
convert_social = {"donatefood":"FD", "donatemoney":"MD", "allergy":"AI", "volunteer":"VO", "cater":"CA"}
social_icon = ["donatefood", "donatemoney", "allergy", "volunteer", "cater"]

convert_att = {"address":"address", "website":"website", "score":"healthScore", "rest_name":"name", "description":"restDescription"}

#####################################
## Open and process restaurant info
#####################################
a = open("Restaurant.json", "r")
s = ""
master = ""
groups = []
count = 0
firstline = a.readline()
for line in a.readlines():
	if "\"name\":" in line:
		master += line
	if "{" in line:
		count += 1
	elif "}" in line:
		count -= 1
	if count == 0:
		groups.append(s)
		s = ""
	else:
		s += line

y = []
for g in groups:
	y.append(json.loads(g+"\n        }"))
template = y[0]

#####################################
## Open and process webportal info
#####################################
x = open("alphatest.txt", "r").readlines()
lst = []
count = 0
for t in x[0].split("}"):
	lst.append([])
	for b in t.replace(", ", "-").split(","):
		if "\"" in b:
			lst[count].append(b.replace("\"", "").replace("{", "").replace("[", ""))
	count += 1

wp_lst = filter(None, lst)


################################################################################
## create a dictionary of name to dictionary of attributes for each restaurant
################################################################################

rest_dict = {}
for rest in wp_lst:
	dct = {}
	for attribute in rest:
		pair = attribute.split(":")
		if pair[0] in days:
			if 'hours' not in dct:
				dct['hours'] = [[],[],[],[],[],[],[]]
			dct['hours'][days.index(pair[0])].append(pair[1])

		elif pair[0] in eco:
			if 'eco' not in dct:
				dct['eco'] = []
				if pair[1] == 'true':
					dct['eco'].append(pair[0].upper())
			else:
				if pair[1] == 'true':
					dct['eco'].append(pair[0].upper())

		elif pair[0] in fair:
			if 'fair' not in dct:
				dct['fair'] = []
				if pair[1] == 'true':
					dct['fair'].append(pair[0].upper())
			else:
				if pair[1] == 'true':
					dct['fair'].append(pair[0].upper())

		elif pair[0] in humane:
			if 'humane' not in dct:
				dct['humane'] = []
				if pair[1] == 'true':
					dct['humane'].append(pair[0].upper())
			else:
				if pair[1] == 'true':
					dct['humane'].append(pair[0].upper())

		elif pair[0] in eco_icon or pair[0] in social_icon:
			if 'labelDescription' not in dct:
				dct['labelDescription'] = [[],[],[]]
				if pair[0] in eco_icon:
					if pair[1] == 'true':
						dct['labelDescription'][0].append(convert_eco[pair[0]])
					else:
						dct['labelDescription'][0].append("\"\"")
				elif pair[0] in social_icon:
					if pair[1] == 'true':
						dct['labelDescription'][1].append(convert_eco[pair[0]])
					else:
						dct['labelDescription'][1].append("\"\"")

		elif pair[0] in convert_att:
			if pair[0] == 'score':
				dct[convert_att[pair[0]]] = int(pair[1])
			else:
				dct[convert_att[pair[0]]] = pair[1]
		elif pair[0] == 'categories':
			dct['dynamic'] = pair[1].split("-")

		else:
			pass
			# if pair[0] not in template:
			# 	print pair[0]
			# 	dct[pair[0]] = pair[1]

	rest_dict[dct['name']] = dct


for rest in y:
	for att in rest:
		try:
			if att in rest_dict[rest['name']]:
				rest[att] = rest_dict[rest['name']][att]
		except KeyError:
			pass

for thing in y:
	if thing['name'] == "Fork!":
		for att in thing:
			pass

for rest in rest_dict:
	for field in template:
		if field not in rest_dict[rest]:
			rest_dict[rest][field] = None

made = []
for thing in y:
	made.append(thing['name'])
for nombre in rest_dict:
	if nombre not in made:
		y.append(rest_dict[nombre])


with open("boots_with_the_furr.json", "w") as outfile:
	outfile.write("{ \"results\": [")
	for i in xrange(len(y)-1):
		json.dump(y[i], outfile)
		outfile.write(",")
	json.dump(y[-1], outfile)
	outfile.write("] }")

