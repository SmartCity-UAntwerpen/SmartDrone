import math
import networkx as nx
from networkx import NetworkXNoPath
from Common.Marker import Marker


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
        It sets a maxFlightDistance
        """
        self.maxFlightDistance = 1
        self.markers = {}
        self.G = None

    def update_markers(self, markers):
        self.markers = {}
        for marker in markers.keys():
            if type(markers[marker]) != Marker:
                m = Marker() # create empty marker
                m.load_dict(markers[marker])
            else: m = markers[int(marker)]
            self.markers[int(marker)] = m
        self.G = self.makeGraph()

    def makeGraph(self):
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

        try:
            path = nx.dijkstra_path(self.G, m1, m2)
        except NetworkXNoPath:
            path = None

        if path is None: return None

        flight_plan = {
            "commands": [],
        }

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

            command = {
                "command": "center",
                "id": path[index+1].id,     #for simulator
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

    def calculate_cost(self, id_marker1, id_marker2):
        m1 = self.markers[id_marker1]
        m2 = self.markers[id_marker2]
        return nx.shortest_path_length(self.G, m1,m2, weight='weight')
