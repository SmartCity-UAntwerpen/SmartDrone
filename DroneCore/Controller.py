
import socket, time, json, sys, signal


class Controller:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        #self.s.connect((self.ip, self.port))

    def start_controller(self):
        pass
        # subscribe to backend, recieve flightplan or not?
            # when no flightplan ==> create flightplanner
            # else parse flightplane
        # wait for drone to connect with tcp

    def send(self,data):
        self.s.send(bytearray(data, 'utf-8'))
        data = self.s.recv(1024) # wait for "ack" TODO: check result?

    def __del__(self):
        self.s.close()

#time.sleep(1)   # wait 1 second for the drone to boot, so the tcp connection won't be refused #FIXME: catch the tcp connection refuse
controller = Controller("localhost", 5000)


def exit(signal, frame):
    print("Controller closed.")
    global controller
    del controller
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
