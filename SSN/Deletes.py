import numpy as np
import json as js

inFile = "gowalla_loc.json"
inFile2 = "gowalla_rel.json"
outFile = "gowalla_loc24.json"
outFile2 = "gowalla_rel24.json"

f = open(inFile, "r")
users = js.load(f)
f.close()
usersKey = list(users)
usersValue = list(users.values())

f = open(inFile2, "r")
relations = js.load(f)
f.close()
relKey = list(relations)
relValue = list(relations.values())

i, j = 0, 0
deleted = []
print(f"Size: {len(usersKey)}")
for x in range(0, len(usersValue)):
    i += 1
    #print(f"Main: {x}")
    # (usersValue[x])[0][0] is the long, (usersValue[x])[0][1] lat
    if 37.3 > float((usersValue[x])[0][0]) > 35.6 and -113.3 > float((usersValue[x])[0][1]) > -116.1:
        j += 1
        deleted.append(usersKey[x])
        del users[f"{usersKey[x]}"]
for y in range(0, len(deleted)):
    if f"{deleted[y]}" in relations:
        del relations[f"{deleted[y]}"]
        del relations[f"{deleted[y]}.weights"]
k = 0
#print(relValue[10][len(relValue[10])])
for z in range(0, len(relValue)):
    if ".weights" not in relKey[z]:
        for g in range(0, len(relValue[z]) - 1):
            print(f"{len(relValue[z])} HERE")
            for b in range(0, len(deleted)):
                print(g)
                if float(relValue[z][g]) == float(deleted[b]):
                    k += 1
                    relations[relKey[z]].remove(relValue[z][g])
print(f"{i} nodes scanned, {j} deleted {k}")

print(deleted)
'''
json1 = js.dumps(users)
f = open(outFile, "w")
f.write(json1)
f.close()
json2 = js.dumps(relations)
f = open(outFile2, "w")
f.write(json2)
f.close()
print(f"Done latlong")
'''