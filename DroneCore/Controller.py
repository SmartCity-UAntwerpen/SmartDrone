
import errno
import socket, time, json, sys, signal
import CoreLogger as clogger


class Controller:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger = clogger.logger

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def start_controller(self):
        # subscribe to backend, recieve flightplan or not?
            # when no flightplan ==> create flightplanner
            # else parse flightplane
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.s.connect((self.ip, self.port))
                connected = True
                self.logger.info("Connection with exectution process established.")
            except socket.error as error:
                if error.errno == errno.ECONNREFUSED:
                    self.logger.warn("Connection to exectution process refused. Retrying...")
                    counter += 1
                    time.sleep(2)

        if not connected:
            self.logger.error("Connection with exectution process not established. Shutting down.")
            return False

        return True # controller succesfully started


    def send(self,data):
        self.s.send(bytearray(data, 'utf-8'))
        data = self.s.recv(1024) # wait for "ack" TODO: check result?

    def __del__(self):
        self.s.close()


def exit(signal, frame):
    print("Controller closed.")
    global controller
    del controller
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    controller = Controller("localhost", int(sys.argv[1]))
    if not controller.start_controller():
        exit(0,0)

