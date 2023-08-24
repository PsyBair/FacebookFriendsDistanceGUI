import numpy as np


# Class for road networks.
# self.__nodes: a numpy array with 3 columns (id, latitude, longitude), and n (number of nodes) rows.
# self.__edges: a numpy array with 4 columns (id, start, end, distance), and n (number of edges) rows.
# self.__plottableLats: a numpy array of latitudes formatted for plotting. [startLat1, endLat1, startLat2, endLat2...]
# self.__plottableLongs: a numpy array of longitudes formatted for plotting. [startLong1, endLong1...]
class RoadNetwork:
    def __init__(self, name, nodeFile, edgeFile, plotLatFile, plotLongFile):
        print(f"{name}: Reading node file ({nodeFile})...")
        self.__nodes = np.load(nodeFile, allow_pickle=True)
        print(f"{name}: Done reading node file.")
        print(f"{name}: Reading roadmap edge file ({edgeFile})...")
        self.__edges = np.load(edgeFile, allow_pickle=True)
        print(f"{name}: Done reading edge file.")
        print(f"{name}: Reading plottable latitude list file ({plotLatFile})...")
        self.__plottableLats = np.load(plotLatFile, allow_pickle=True)
        print(f"{name}: Done reading plottable latitude list file.")
        print(f"{name}: Reading plottable longitude list file ({plotLongFile})...")
        self.__plottableLongs = np.load(plotLongFile, allow_pickle=True)
        print(f"{name}: Done reading plottable longitude list file.")

    # Returns self.__nodes
    def getNodes(self):
        return self.__nodes

    # Returns self.__edges
    def getEdges(self):
        return self.__edges

    # Returns self.__plottableLats
    def getPlottableLats(self):
        return self.__plottableLats

    # Returns self.__plottableLongs
    def getPlottableLongs(self):
        return self.__plottableLongs

    # Returns total number of nodes
    def getTotalNodes(self):
        return self.__nodes.shape[0]

    # Returns total number of edges
    def getTotalEdges(self):
        return self.__edges.shape[0]

    # Returns node from specific index i in __nodes
    def getNodeByIndex(self, i):
        return [int(self.__nodes[i][0]), self.__nodes[i][1], self.__nodes[i][2]]

    # Returns edge from specific index i in __edges
    def getEdgeByIndex(self, i):
        return [int(self.__edges[i][0]), int(self.__edges[i][1]), int(self.__edges[i][2]), self.__edges[i][3]]

    # Returns node at specific latitude lat and longitude long HERE
    def getNodeByCoord(self, lat, long):
        for x in range(0, self.getTotalNodes()):
            if (self.__nodes[x][1] == lat) & (self.__nodes[x][2] == long):
                return [int(self.__nodes[x][0]), self.__nodes[x][1], self.__nodes[x][2]]

    # Returns edge at specific start and end
    def getEdgeByRange(self, start, end):
        for x in range(0, self.getTotalEdges()):
            if (self.__edges[x][1] == start) & (self.__edges[x][2] == end):
                return [int(self.__edges[x][0]), int(self.__edges[x][1]), int(self.__edges[x][2]), self.__edges[x][3]]

    # Returns node of specific id
    def getNodeById(self, id):
        for x in range(0, self.getTotalNodes()):
            if self.__nodes[x][0] == id:
                return [int(self.__nodes[x][0]), self.__nodes[x][1], self.__nodes[x][2]]

    # Returns edge of specific id
    def getEdgeById(self, id):
        for x in range(0, self.getTotalEdges()):
            if self.__edges[x][0] == id:
                return [int(self.__edges[x][0]), int(self.__edges[x][1]), int(self.__edges[x][2]), self.__edges[x][3]]

    # Returns an array of latitudes
    def getLats(self):
        return self.__nodes[:, 1]

    # Returns an array of longitudes
    def getLongs(self):
        return self.__nodes[:, 2]
