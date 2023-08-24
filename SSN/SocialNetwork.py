import numpy as np
import threading as thread
import time
import json as js
from matplotlib.collections import LineCollection


# Class for social networks.
# self.__users: a dictionary with key of user id with values of a list with latitude and longitude
# self.__userKeyList: a list of __users keys. Shares the same indexes as __userValueList
# self.__userValueList: a list of __user values. Shares the same indexes as __userKeyList
# self.__relations: a dictionary with key of start user id with values of a list of all end user ids
# self.__relationKeyList: a list of __relations keys. Shares the same indexes as __relationValueList
# self.__relationValueList: a list of __relations values. Shares the same indexes as __relationKeyList
class SocialNetwork:
    # locFile: File to read user locations from.
    # relFile: file to read user relations from.
    def __init__(self, name, locFile, relFile, keywordFile):
        readFiles = [thread.Thread(target=self.__readLocFile, args=(name, locFile,)),
                     thread.Thread(target=self.__readRelFile, args=(name, relFile,))]
        for x in readFiles:
            x.start()
        if keywordFile != '':
            readKeywords = thread.Thread(target=self.__readKeywordFile, args=(name, keywordFile,))
            readKeywords.start()
            readKeywords.join()
        for x in readFiles:
            x.join()

    def __readLocFile(self, name, locFile):
        print(f"{name}:  Reading social network location file ({locFile})...")
        f = open(locFile, "r")
        users = js.load(f)
        f.close()
        self.__users = users
        self.__userKeyList = list(users)
        self.__userValueList = list(users.values())
        print(f"{name}:  Done reading location file.")

    def __readRelFile(self, name, relFile):
        print(f"{name}:  Reading social network relation file ({relFile})...")
        f = open(relFile, "r")
        relations = js.load(f)
        f.close()
        self.__relations = relations
        self.__relationsKeyList = list(relations)
        self.__relationsValueList = list(relations.values())
        print(f"{name}:  Done reading relation file.")

    def __readKeywordFile(self, name, keywordFile):
        print(f"{name}: Reading keyword file ({keywordFile})...")
        file = open("dict.json", "r")
        self.__keywords = js.load(file)
        file.close()
        print(f"{name}: Done reading keyword file.")

    # Returns self.__relations
    def getRelations(self):
        return self.__relations

    # Returns self.__users
    def getUsers(self):
        return self.__users

    # Returns total number of users
    def getTotalUsers(self):
        return len(self.__users)

    # Returns total number of relations
    def getTotalRelations(self):
        return len(self.__relations)

    # Returns users at specific latitude and longitude
    def getUserByCoord(self, lat, long):
        i = 0
        for x in range(0, len(self.__userValueList)):
            for y in range(0, len(self.__userValueList[x])):
                if np.round((self.__userValueList[x])[y][1], 1) == np.round(float(lat), 1) and \
                        np.round((self.__userValueList[x])[y][0], 1) == np.round(float(long), 1):
                    return self.__userKeyList[i]
            i += 1

    # Returns edge at specific start and end
    #def getEdgeByRange(self, start, end):
    #    for x in range(0, self.getTotalEdges()):
    #        if (self.__edges[x][1] == start) & (self.__edges[x][2] == end):
    #            return [int(self.__edges[x][0]), int(self.__edges[x][1]), self.__edges[x][2],
    #                    self.__edges[x][3]]

    # Returns location of specific id
    def getLocByUserId(self, id):
        return self.__users[f"{float(id)}"][0]

    # Returns an array of latitudes
    def getLats(self):
        lats = []
        for x in self.__userValueList:
            for y in range(0, len(x)):
                lats.append(x[y][0])
        return lats

    # Returns an array of longitudes
    def getLongs(self):
        longs = []
        for x in self.__userValueList:
            for y in range(0, len(x)):
                longs.append(x[y][1])
        return longs

    # Returns a list of latitudes for plotting in form start, end, None, start1, end1, None...
    def getPlottableLats(self):
        lats = []
        for x in range(0, len(self.__relationsKeyList)):
            if ".weights" not in self.__relationsKeyList[x]:
                for y in range(0, len(self.__relationsValueList[x])):
                    lats.append(self.getLocByUserId(self.__relationsKeyList[x])[0])
                    lats.append(self.getLocByUserId(self.__relationsValueList[x][y])[0])
                    lats.append(None)
        return lats

    def getPlottableLongs(self):
        longs = []
        for x in range(0, len(self.__relationsKeyList)):
            if ".weights" not in self.__relationsKeyList[x]:
                for y in range(0, len(self.__relationsValueList[x])):
                    longs.append(self.getLocByUserId(self.__relationsKeyList[x])[1])
                    longs.append(self.getLocByUserId(self.__relationsValueList[x][y])[1])
                    longs.append(None)
        return longs

    def getPlottableWeights(self):
        weights = []
        for x in range(0, len(self.__relationsKeyList)):
            if ".weights" in self.__relationsKeyList[x]:
                for y in range(0, len(self.__relationsValueList[x])):
                    weights.append(self.__relations[f"{self.__relationsKeyList[x]}"][y])
                    weights.append(None)
                    weights.append(None)
        return weights

    # Returns a list of coordinates
    def getCoordList(self):
        coords = []
        for x in range(0, len(self.__userValueList)):
            coords.append(self.__userValueList[x][0])
        return np.array(coords)

    # Returns __keywords
    def getKeywords(self):
        return self.__keywords

    # Returns all relations from a user id
    def getAllRelations(self, id):
        if f"{id}" in self.__relations:
            return self.__relations[f"{id}"]
        return ["NONE"]
