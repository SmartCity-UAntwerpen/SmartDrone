import math
import networkx as nx
import matplotlib.pyplot as plt
from networkx import NetworkXNoPath
from Common.Marker import Marker

from Common.DBConnection import DBConnection


def distance(m1, m2):
    """
    :param m1: marker 1 (with location x,y,z)
    :param m2: marker 2 (with location x,y,z)
    :return: The Euclidean distance between m1 and m2
    """
    return math.sqrt(pow(m2.x - m1.x, 2) + pow(m2.y - m1.y, 2) + pow(m2.z - m2.z, 2))


class FlightPlanner:
    def __init__(self):
        """
        This class makes a graph of all the markers.
        With the use of this graph it is possible to find the most optimal route between two markers
        It uses the database to find all the markers in the world.
        It sets a maxFlightDistance
        """
        self.db = DBConnection()
        self.maxFlightDistance = 1.6
        self.markers = self.setMarkers()
        self.G = self.makeGraph()


    def makeGraph(self, verbose=False):
        """
        make a graph and fill the nodes with all the markers
        for every marker check al the other markers, if the distance is smaller then a maxFlightTime
        add that marker as neighbour <=> there is a path between the markers with a weight equaling the distance
        this method could be improved if you make the path not bidirectional
        :param verbose: for debug prints the graph
        :return: the graph
        """
        # TODO replace this method to the backbone and let the FlightPlanner import the map from the backbone

        G = nx.Graph()
        G.add_nodes_from(self.markers.values())
        for currentMarker in self.markers.values():
            for index in self.markers.values():
                if index != currentMarker:
                    d = distance(currentMarker, index)
                    if d <= self.maxFlightDistance:
                        G.add_edge(currentMarker, index, weight=d)

        # for debug purpuses you can print de graph
        if verbose:
            pos = nx.spring_layout(G)
            nx.draw(G, with_labels=True)
            plt.savefig("graph.png")
            plt.show()

        return G

    def find_path(self, id_marker1, id_marker2):
        """
        use dijkstra to find the path between marker m1 and m2
        if no path exist return an empty message
        otherwise cut the path into small instructions and return the instructions
        :param m1: marker 1 the startpoint
        :param m2: marker 2 the endpoint
        :return: json with instructions
        """
        m1 = self.markers[id_marker1]
        m2 = self.markers[id_marker2]
        flight_plan = {
            "commands": [],
        }

        try:
            path = nx.dijkstra_path(self.G, m1, m2)
        except NetworkXNoPath:
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
            command = {
                "command": "guided_land",
                "velocity": 0.2,
                "id": m2.id
            }
            flight_plan["commands"].append(command)

        return flight_plan

    def setMarkers(self):
        """
        get the markers from the database and store them in an array
        :return: array with markers
        """

        # x,y,z,transitpoint
        markers = {}
        for m in self.db.query("select * from point"):
            markers[m[0]] = Marker(m[1], m[2], m[3],m[0])

        return markers


if __name__ == "__main__":
    """
    Small test
    """
    f = FlightPlanner()
    flightplan = f.find_path(1, 2)
    print(flightplan)
