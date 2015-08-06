
import operator

preferences = {}
locations = {}
infile = open("Preference.json", "r")

lastdish = ""
for line in infile.readlines():
	if "dishName" in line:
		newline = line.replace("dishName", "").replace("\"", "").replace("   ", "").replace(",", "").replace(":", "").replace("   ", "").replace("\n", "")
		if newline not in preferences:
			preferences[newline] = 1
		else:
			preferences[newline] += 1
		lastdish = newline
	elif "location" in line:
		loc = line.replace("location", "").replace("\"", "").replace("   ", "").replace(",", "").replace(":", "").replace("   ", "").replace("\n", "")
		if preferences[lastdish] < 2:
			locations[lastdish] = loc

sorted_x = sorted(preferences.items(), key=operator.itemgetter(1))

ranked = []
for thing in sorted_x:
	ranked.append(thing[0])
for i in xrange(6):
	if i != 0:
		print ranked[-i], locations[ranked[-i]]
