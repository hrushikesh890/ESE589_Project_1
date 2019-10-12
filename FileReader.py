f = open("data/bezdekIris.data", "r")
fData = f.readlines()
lData = []

for sIter in fData:
	if (sIter[-1] == "\n"):
		sIter = sIter[:-1]
	lData.append(sIter.split(","))

print(lData)