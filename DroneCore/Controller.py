
import socket, time, json, sys, signal

class Controller:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.s.connect((self.ip, self.port))

    def send(self,data):
        self.s.send(bytearray(data, 'utf-8'))
        data = self.s.recv(1024) # wait for "ack" TODO: check result?

    def __del__(self):
        self.s.close()

time.sleep(1)   # wait 1 second for the drone to boot, so the tcp connection won't be refused #FIXME: catch the tcp connection refuse
controller = Controller("localhost", int(sys.argv[1]))

def exit(signal, frame):
    print("Controller closed.")
    global controller
    del controller
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)

    message = {
        "command": "arm",
    }
    controller.send(json.dumps(message))
    time.sleep(2)

    message = {
        "command": "takeoff",
        "velocity": .5,
        "height": 5
    }
    controller.send(json.dumps(message))
    time.sleep(2)

    message = {
        "command": "move",
        "goal": (1,1,0),
        "velocity":  0.5
    }
    controller.send(json.dumps(message))
    controller.send(json.dumps(message))
