
import json
import string
import operator

preferences = {}
locations = {}
#infile = open("preference_counter.txt", "r")

dl = open("Disliked.json", "r")
fstln = dl.readline()
dislikes = []
keep = ""
follow = 0
for line in dl.readlines():
	if "{" in line:
		follow += 1
	elif "}" in line:
		follow -= 1
	if follow == 0:
		dislikes.append(keep)
		keep = ""
	else:
		keep += line

fnl = []
for d in dislikes:
	#print g
	fnl.append(json.loads(d+"\n        }"))
template = fnl[0]

dl.close()

dholder = []
dchecker = []
for g in fnl:
	#print g['dishName']
	if g['dishName'] not in dchecker:
		g['dislike'] = 1
		dholder.append(g)
		dchecker.append(g['dishName'])
		#print g['count']
	else:
		dholder[dchecker.index(g['dishName'])]['dislike'] += 1

hates = {}
for thing in dholder:
	if thing['location'] not in hates:
		hates[thing['location']] = []
		hates[thing['location']].append(thing)
	else:
		hates[thing['location']].append(thing)


###############################################
#Likes


a = open("Preference.json", "r")
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
	#print g
	y.append(json.loads(g+"\n        }"))
template = y[0]

a.close()

lholder = []
lchecker = []
for g in y:
	#print g['dishName']
	if g['dishName'] not in lchecker:
		g['count'] = 1
		lholder.append(g)
		lchecker.append(g['dishName'])
		#print g['count']
	else:
		lholder[lchecker.index(g['dishName'])]['count'] += 1
		#print lholder[lchecker.index(g['dishName'])]['count']
	# for att in g:
	# 	print att
	# break

loxs = {}
for thing in lholder:
	if thing['location'] not in loxs:
		loxs[thing['location']] = []
		loxs[thing['location']].append(thing)
	else:
		loxs[thing['location']].append(thing)




for thing in loxs:
	sortlike = sorted(loxs[thing], key=lambda k: k['count'], reverse=True)

	newfile = open(str(thing.replace(" ", ""))+"_stats.txt", "w")
	newfile.write('Preference Data For ' + thing + ':\n')
	for meal in sortlike:
		name = filter(lambda x: x in string.printable, meal['dishName'])
		
		count =  meal['count']
		# print name + ": " + str(count)
		newfile.write(name + ": " + str(count) + "\n")
	newfile.write("\n")

	if thing in hates:
		sorthate = sorted(hates[thing], key=lambda k: k['dislike'], reverse=True)
		newfile.write('Dislike Data For ' + thing + ':\n')
		for meal in sorthate:
			name = filter(lambda x: x in string.printable, meal['dishName'])
		
			count =  meal['dislike']
			# print name + ": " + str(count)
			newfile.write(name + ": " + str(count) + "\n")

	newfile.close()

