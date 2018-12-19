
class Marker:

    def __init__(self, x=0, y=0, z=0, id=0):
        """
        This class holds the information of a specific marker
        :param x: x location
        :param y: y location
        :param z: z location
        :param id: id
        """
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def print(self):
        """
        print all the info of a marker in a nice format
        """
        print("marker id= ", self.id, "[", self.x, ",", self.y, ",", self.z, "]")

    def get_dict(self):
        res = {
            "x":self.x,
            "y":self.y,
            "z":self.z,
            "id":self.id
        }
        return res

    def load_dict(self, dict):
        try:
            self.x = dict["x"]
            self.y = dict["y"]
            self.z = dict["z"]
            self.id = dict["id"]
        except: print("Error loading dictionary!")


