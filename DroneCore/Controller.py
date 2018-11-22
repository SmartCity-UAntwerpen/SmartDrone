
import socket, time, json

class Controller:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.s.connect((self.ip, self.port))

    def send(self,data):

        self.s.send(bytearray(data, 'utf-8'))

    def __del__(self):
        self.s.close()


if __name__ == '__main__':
    """
        Send the flight commands to the executing process using tcp sockets
    """
    controller = Controller("localhost",9000)

    message = {
        "command": "arm",
    }
    controller.send(json.dumps(message))
    time.sleep(2)
    message = {
        "command": "takeoff",
        "velocity": .5
    }
    controller.send(json.dumps(message))
    time.sleep(2)
    message = {
        "command": "move",
        "pos": (1,1,0),
        "velocity":  0.5
    }
    controller.send(json.dumps(message))
