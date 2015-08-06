
import json

eco = ["cob", "cbf", "cls", "ifo", "dcb", "euo", "fac", "msc", "mba", "phc", "rac", "usda"]
fair = ["eft", "ffs", "fl", "f", "fw", "fjc", "sps"]
humane = ["aga", "ahc", "awa", "chr", "gap"]
labels = {'scratch':'FSD', 'local':'LD', 'season':'SE'}
approved = ['name', 'price']

a = open("dishInfo.json", "r")
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



x = open("alpham.txt", "r").readlines()
lst = []
count = 0
for t in x[0].split("}"):
	lst.append([])
	for b in t.replace(", ", "-").split(","):
		if "\"" in b:
			lst[count].append(b.replace("\"", "").replace("{", "").replace("[", ""))
	count += 1
wp_lst = filter(None, lst)


dishes = {}
for dish in wp_lst:
	dct = {}
	for att in dish:
		pair = att.split(":")
		if pair[0] in approved:
			dct[pair[0]] = pair[1]
			#print pair[0], pair[1]
		elif pair[0] == 'ingredient':
			dct['ingredient'] = pair[1].split("-")
			#print dct['ingredient']
		elif pair[0] == 'category':
			dct['type'] = pair[1]
			#print dct['type']
		elif pair[0] in labels:
			if 'susLabels' not in dct:
				dct['susLabels'] = []
			if pair[1] == 'true':
				dct['susLabels'].append(labels[pair[0]])

		elif pair[0] in eco:
			if 'eco' not in dct:
				dct['eco'] = []
				if pair[1] == 'true':
					dct['eco'].append(pair[0].upper()+"D")
			else:
				if pair[1] == 'true':
					dct['eco'].append(pair[0].upper()+"D")

		elif pair[0] in fair:
			if 'fair' not in dct:
				dct['fair'] = []
				if pair[1] == 'true':
					dct['fair'].append(pair[0].upper()+"D")
			else:
				if pair[1] == 'true':
					dct['fair'].append(pair[0].upper()+"D")

		elif pair[0] in humane:
			if 'humane' not in dct:
				dct['humane'] = []
				if pair[1] == 'true':
					dct['humane'].append(pair[0].upper()+"D")
			else:
				if pair[1] == 'true':
					dct['humane'].append(pair[0].upper()+"D")
	

	dishes[dct['name']] = dct

for meal in y:
	for d in dishes:
		if meal['name'] == d:
			for att in dishes[d]:
				meal[att] = dishes[d][att]

for dish in dishes:
	for field in template:
		if field not in dishes[dish]:
			if field == "ACL":
				dishes[dish][field] = template[field]
			else:
				dishes[dish][field] = None

made = []
for thing in y:
	made.append(thing['name'])
for nombre in dishes:
	if nombre not in made:
		y.append(dishes[nombre])

# for it in y:
# 	print it
# 	print
# 	print 

with open("apple_bottom_jeans.json", "w") as outfile:
	outfile.write("{ \"results\": [")
	for i in xrange(len(y)-1):
		json.dump(y[i], outfile)
		outfile.write(",")
	json.dump(y[-1], outfile)
	outfile.write("] }")



