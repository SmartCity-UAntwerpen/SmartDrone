
import threading, socket


class SharedSocket(threading.Thread):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    queues = {}
    running = True
    lock = threading.Lock()

    def connect(self,ip,port):
        self.s.connect((ip, port))

    def send_and_receive(self,data):
        self.lock.acquire()
        self.s.send(data)
        data = self.s.recv(2048)
        self.lock.release()
        return data

    def close(self):
        self.s.close()
