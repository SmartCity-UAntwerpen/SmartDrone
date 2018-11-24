import math
import networkx as nx
import matplotlib.pyplot as plt
from networkx import NetworkXNoPath
from Marker import Marker


def distance(m1, m2):
    return math.sqrt(pow(m2.x - m1.x, 2) + pow(m2.y - m1.y, 2) + pow(m2.z - m2.z, 2))


class FlightPlanner:

    def __init__(self):
        self.markers = self.setMarkers()
        self.G = self.makeGraph()
        self.maxFlightTime = 1.0

    def makeGraph(self, verbose=0):
        # TODO replace this method to the backbone and let the FlightPlanner import the map from the backbone
        # make a graph and fill the nodes with all the markers
        # for every marker check al the other markers if the distance is smaller then a maxFlightTime
        # add that marker as neighbour <=> there is a path between the markers with a weight equaling the distance
        # this method could be improved if you make the path not bidirectional
        G = nx.Graph()
        G.add_nodes_from(self.markers)
        for currentMarker in self.markers:
            for index in self.markers:
                if index != currentMarker:
                    d = distance(currentMarker, index)
                    if d <= self.maxFlightTime:
                        G.add_edge(currentMarker, index, weight=d)

        # for debug purpuses you can print de graph
        if verbose == 1:
            pos = nx.spring_layout(G)
            nx.draw(G, with_labels=True)
            plt.savefig("graph.png")
            plt.show()

        return G

    def findPath(self, m1, m2):
        # use dijkstra to find the path between marker m1 and m2
        # if no path exist give a message
        # otherwise cut the path into small instructions
        try:
            path = nx.dijkstra_path(self.G, m1, m2)
        except NetworkXNoPath:
            # TODO replace by json and send to controller
            print("no path to node")
            path = None

        if path is not None:
            for index in range(0, len(path) - 1):
                delta_x = path[index + 1].x - path[index].x
                delta_y = path[index + 1].y - path[index].y
                delta_z = path[index + 1].z - path[index].z
                # TODO replace by json and send to controller
                print("move to id= ", path[index + 1].id, "(", delta_x, ";", delta_y, ";", delta_z, ")")

    def setMarkers(self):
        # get the markers from the database and store them in an array
        # TODO read markers from database
        m0 = Marker(1, 1, 0, 0)
        m1 = Marker(2, 1, 0, 1)
        m2 = Marker(1, 2, 0, 2)
        m3 = Marker(2, 2, 0, 3)
        m4 = Marker(1, 3, 0, 4)
        markers = [m0, m1, m2, m3, m4]
        return markers

    def getMarker(self,index):
        # just for testing
        return self.markers[index]

    if __name__ == '__main__':
        pass
