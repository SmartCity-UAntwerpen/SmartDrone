import math
import networkx as nx
import matplotlib.pyplot as plt
from networkx import NetworkXNoPath
from Marker import Marker

from Common.DBConnection import DBConnection


def distance(m1, m2):
    return math.sqrt(pow(m2.x - m1.x, 2) + pow(m2.y - m1.y, 2) + pow(m2.z - m2.z, 2))


class FlightPlanner:
    def __init__(self):
        """
        sets the maxflight time
        sets the markers
        makes a graph
        """
        self.db = DBConnection()
        self.maxFlightTime = 1.0
        self.markers = self.setMarkers()
        self.G = self.makeGraph()


    def makeGraph(self, verbose=False):
        """
        make a graph and fill the nodes with all the markers
        for every marker check al the other markers if the distance is smaller then a maxFlightTime
        add that marker as neighbour <=> there is a path between the markers with a weight equaling the distance
        this method could be improved if you make the path not bidirectional
        :param verbose: for debug prints the graph
        :return: the graph
        """
        # TODO replace this method to the backbone and let the FlightPlanner import the map from the backbone

        G = nx.Graph()
        G.add_nodes_from(self.markers)
        for currentMarker in self.markers:
            for index in self.markers:
                if index != currentMarker:
                    d = distance(currentMarker, index)
                    if d <= self.maxFlightTime:
                        G.add_edge(currentMarker, index, weight=d)

        # for debug purpuses you can print de graph
        if verbose:
            pos = nx.spring_layout(G)
            nx.draw(G, with_labels=True)
            plt.savefig("graph.png")
            plt.show()

        return G

    def findPath(self, id_marker1, id_marker2):
        """
        use dijkstra to find the path between marker m1 and m2
        if no path exist return an empty message
        otherwise cut the path into small instructions and return the instructions
        :param m1: marker 1 the startpoint
        :param m2: marker 2 the endpoint
        :return: json with instructions
        """
        m1 = self.getMarker(id_marker1)
        m2 = self.getMarker(id_marker2)
        flight_plan = {
            "commands": [],
        }

        try:
            path = nx.dijkstra_path(self.G, m1, m2)
        except NetworkXNoPath:
            print("no path to node")
            path = None

        if path is not None:
            fly_height = 1
            # takeoff
            takeoff = {
                "command": "takeoff",
                "velocity": 0.5,
                "height": fly_height
            }
            flight_plan["commands"].append(takeoff)

            # fly to target
            for index in range(0, len(path) - 1):
                delta_x = path[index + 1].x - path[index].x
                delta_y = path[index + 1].y - path[index].y
                delta_z = path[index + 1].z - path[index].z
                command = {
                    "command": "move",
                    "goal": (delta_x, delta_y, delta_z),
                    "velocity": 0.5
                }
                flight_plan["commands"].append(command)

            # land
            while fly_height >= 0.1:
                fly_height -= 0.1
                command = {
                    "command": "down",
                    "distance": 0.1,
                    "velocity": 0.2
                }
                flight_plan["commands"].append(command)
                command = {
                    "command": "center",
                    "id": m2.id
                }
                flight_plan["commands"].append(command)

            # get to ground and shutdown engine
            command = {
                "command": "land"
            }
            flight_plan["commands"].append(command)

        return flight_plan

    def setMarkers(self):
        """
        get the markers from the database and store them in an array
        :return: array with markers
        """

        # x,y,z,transitpoint
        markers = []
        for m in self.db.query("select * from point"):
            markers.append(Marker(m[1], m[2], m[3],m[0]))

        return markers

    def getMarker(self, index):
        """
        gets the marker from the array of markers
        just for testing
        :param index: index of array markers
        :return: marker
        """

        return self.markers[index]


if __name__ == "__main__":
    f = FlightPlanner()
    flightplan = f.findPath(1,2)
    print(flightplan)
