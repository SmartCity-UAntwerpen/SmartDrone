
class Marker:

    def __init__(self, x, y, z, id):
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

