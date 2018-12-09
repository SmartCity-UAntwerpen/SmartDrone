
class Marker:

    def __init__(self, x, y, z, id):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def print(self):
        print("marker id= ", self.id, "[", self.x, ",", self.y, ",", self.z, "]")

    def __str__(self):
        return str(self.id)