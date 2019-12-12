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


def map(value, leftMin, leftMax, rightMin, rightMax):
    """
    Map a value located between [leftMin, leftMax] to a value between [rightMin, righMax]
    """
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


class FlightPlanner:
    def __init__(self):
        """
        This class makes a graph of all the markers.
        With the use of this graph it is possible to find the most optimal route between two markers
        It sets a maxFlightDistance
        """
        self.maxFlightDistance = 1
        self.markers = {}
        self.links = {}
        self.G = None
        self.longest_path_cost = None  # used to map cost to [0, 100], this value should be the longest path in the graph

    def update_markers(self, markers):
        for marker in markers.keys():
            if type(markers[marker]) != Marker:
                m = Marker() # create empty marker
                m.load_dict(markers[marker])
            else: m = markers[int(marker)]
            self.markers[int(marker)] = m
        self.G = self.makeGraph()
        self.longest_path_cost = self.find_longest_path()

    def find_longest_path(self):
        """
        go trough all nodes and check all paths. Save the longest_path_cost
        :return: longest_path_cost
        """
        longest_path_cost = 0
        for m1 in self.markers.values():
            for m2 in self.markers.values():
                try:
                    cost = nx.shortest_path_length(self.G, m1, m2, weight='weight')
                    if cost > longest_path_cost:
                        longest_path_cost = cost
                except:
                    pass
        return longest_path_cost

    def makeGraph(self):
        """
        make a graph and fill the nodes with all the markers
        for every marker check al the other markers, if the distance is smaller then a maxFlightTime
        add that marker as neighbour <=> there is a path between the markers with a weight equaling the distance
        this method could be improved if you make the path not bidirectional
        :param verbose: for debug prints the graph
        :return: the graph
        """

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
        direction = ""

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

        command = {
            "command": "center",
            "id": m1.id,  # for simulator
        }
        flight_plan["commands"].append(command)

        # fly to target
        #see if path has endend, only on end recenter. In middle detect deviation.
        for index in range(0, len(path) - 1):
            delta_x = path[index + 1].x - path[index].x
            delta_y = path[index + 1].y - path[index].y
            delta_z = path[index + 1].z - path[index].z

            x_dir = path[len(path)-1].x-path[0].x
            y_dir = path[len(path)-1].y-path[0].y
            if x_dir > 0:
                direction = "RaisingX"

            command = {
                "command": "move",
                "goal": (delta_x, delta_y, delta_z),
                "velocity": 0.5,
                "direction" : direction ,     #needed for path recalculation after deviation

            }
            flight_plan["commands"].append(command)

            if (index+1) == (len(path)-1):
                command = {
                "command": "center",
                "id": path[index+1].id,     #for simulator
                }
            #if not on end of path, do not center on marker, but detect deviation and correct for it whilst continuing flight    
            else:
                command = {
                "command": "detect",
                "goal":(path[index+1].x,path[index+1].y, path[index+1].z ), #for simulator
                "id": path[index+1].id, #for simulator
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
        if self.G is not None:
            m1 = self.markers[id_marker1]
            m2 = self.markers[id_marker2]
            try:
                cost = nx.shortest_path_length(self.G, m1, m2, weight='weight')
            except:
                cost = 100000
            if self.longest_path_cost is None:
                self.longest_path_cost = self.find_longest_path() # graph should exist
            return int(map(cost, 0, self.longest_path_cost, 0, 100))
        else:
            return 100000
