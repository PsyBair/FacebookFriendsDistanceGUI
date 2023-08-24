import numpy as np
import json as js

# Users
'''inFile = "tweets_loc.npy"
outFile = "tweets_loc_byPos.json"
outFile2 = "tweets_loc_byId.json"

sNetwork = np.load(inFile, allow_pickle=True)
latlong = {}
id = {}
i, j = 0, 0

print(f"Size: {len(sNetwork[:, 0])}, {len(sNetwork[0, :])}")
for x in range(0, len(sNetwork)):
    i += 1
    if 42 > sNetwork[x, 1] > 32 and -114 > sNetwork[x, 2] > -124.5:
        j += 1
        if f"{sNetwork[x, 0]}" not in id:
            id[f"{sNetwork[x, 0]}"] = []
        if f"{sNetwork[x, 1]}, {sNetwork[x, 2]}" not in latlong:
            latlong[f"{sNetwork[x, 1]}, {sNetwork[x, 2]}"] = []
        #make all of these arrays so you can append them
        id[f"{sNetwork[x, 0]}"].append([sNetwork[x, 1], sNetwork[x, 2]])
        latlong[f"{sNetwork[x, 1]}, {sNetwork[x, 2]}"].append(sNetwork[x, 0])

print(f"{i} nodes scanned, {j} added")
print(f"latlong: {len(latlong)}, id: {len(id)}")

json1 = js.dumps(latlong)
f = open(outFile, "w")
f.write(json1)
f.close()
print(f"Done latlong")

json2 = js.dumps(id)
f = open(outFile2, "w")
f.write(json2)
f.close()
print(f"Done id")'''

# Edges

inFile = "foursquare_loc_byId.json"
inFile2 = "foursquare_inf.npy"
outFile = "foursquare_rel.json"

f = open(inFile, "r")
users = js.load(f)
f.close()
ids = list(users)

edges = np.load(inFile2, allow_pickle=True)
starts = edges[:, 0]
ends = edges[:, 1]
weights = edges[:, 2]

iStarts = []
iEnds = []
iWeights = []

print("Started")
to = np.floor(len(starts)/100)
for x in range(int(to * 3), int(to * 4)):
    print(x)
    if f"{starts[x]}" in ids and f"{ends[x]}" in ids:
        iStarts.append(starts[x])
        iEnds.append(ends[x])
        iWeights.append(weights[x])
json1 = js.dumps(iStarts)
f = open("iStarts3.json", "w")
f.write(json1)
f.close()
json1 = js.dumps(iEnds)
f = open("iEnds3.json", "w")
f.write(json1)
f.close()
json1 = js.dumps(iWeights)
f = open("iWeights3.json", "w")
f.write(json1)
f.close()
print(f"Done latlong")
print("Done")
print("Done")
print("Done")
print("Done")
print("Done")
print("Done")
print("Done")
print("Done")
'''
f = open("iStarts.json", "r")
iStarts = js.load(f)
f.close()
f = open("iEnds.json", "r")
iEnds = js.load(f)
f.close()
f = open("iWeights.json", "r")
iWeights = js.load(f)
f.close()
edgesOut = {}
i, j = 0, 0

print(f"Size: {len(iStarts)}")
for x in range(0, len(iStarts)):
    i += 1
    print(f"Main: {x}")
    if f"{iStarts[x]}" not in edgesOut:
        edgesOut[f"{iStarts[x]}"] = []
        edgesOut[f"{iStarts[x]}.weights"] = []
for y in range(0, len(iEnds)):
    print(y)
    j += 1
    edgesOut[f"{iStarts[y]}"].append(iEnds[y])
    weight = iWeights[y]
    if weight < 0.01:
        weight = 0.01
    edgesOut[f"{iStarts[y]}.weights"].append(weight)

print(f"{i} nodes scanned, {j} added")

json1 = js.dumps(edgesOut)
f = open(outFile, "w")
f.write(json1)
f.close()
print(f"Done latlong")
'''