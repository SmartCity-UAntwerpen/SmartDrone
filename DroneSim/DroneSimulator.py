
import Drone, socket, signal, sys, json, asyncore
from json import JSONDecodeError

markers = [
        (1,1,0),
        (2,1,0),
        (1,2,0),
        (2,2,0),
        (1,3,0)
    ]


def exit(signal, frame):
    print("Closing socket...")
    # emergency land drone?
    print("Simulator tured off.")
    sys.exit(0)


class DroneSimulator(asyncore.dispatcher):

    drone = Drone.Drone()

    def __init__(self,ip,port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(1)          # only allow one incomming connection
        self.running = True
        self.drone.black_box.info("Drone simulator started.")

    def handle_accept(self):
        pair = self.accept()  # wait for a connection
        if pair is None: return
        sock, addr = pair

        while self.running:
            data = sock.recv(2048)  # recieve data with buffer of size 2048
            if not data: exit(1, 1)
            try:
                data = json.loads(data.decode())
                if data["action"] == "execute_command":
                    self.perform_action(data, sock)
                elif data["action"] == "send_position":
                    self.send_drone_position(sock)
                elif data["action"] == "send_status":
                    self.send_drone_status(sock)
            except JSONDecodeError:
                self.drone.black_box.error("Recieved non json message, dropping message.")

    def send_drone_position(self, connection):
        #self.drone.black_box.info("Sending position update.")
        res = {
            "position": (float(self.drone.x), float(self.drone.y), float(self.drone.z)),
        }
        connection.send(json.dumps(res).encode())

    def send_drone_status(self, connection):
        #self.drone.black_box.info("Sending status update.")
        res = {
            "status": self.drone.status,
        }
        connection.send(json.dumps(res).encode())

    def perform_action(self, command, conn):
        #self.drone.black_box.info("Received a command.")
        try:
            message = command
            if self.drone.is_armed():
                if message["command"] == "takeoff":
                    self.drone.takeOff(message["height"], message["velocity"])
                    self.send_drone_position(conn)
                    return

            if self.drone.is_flying():
                if message["command"] == "land":
                    self.drone.land()
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "move":
                    goal = message["goal"]
                    self.drone.moveDistance(goal[0],goal[1],goal[2],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "forward":
                    self.drone.forward(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "backward":
                    self.drone.backward(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "left":
                    self.drone.left(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "right":
                    self.drone.right(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "up":
                    self.drone.up(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "down":
                    self.drone.down(message["distance"],message["velocity"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "turn_left":
                    self.drone.turnLeft(message["angle"],message["rate"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "turn_right":
                    self.drone.turnRight(message["angle"],message["rate"])
                    self.send_drone_position(conn)
                    return

                elif message["command"] == "center":
                    marker = markers[message["id"]]
                    self.drone.center(marker[0],marker[1])
                    self.send_drone_position(conn)
                    return

            # commands that can be berformed when not flying or armed
            if message["command"] == "arm":
                self.drone.arm()
                self.send_drone_position(conn)
                return

            elif message["command"] == "set":
                goal = message["goal"]
                self.drone.setCoordinates(goal[0], goal[1], goal[2])
                self.send_drone_position(conn)
                return

            conn.send(b'NOT_ARMED')
            return
        except JSONDecodeError: self.drone.black_box.error("Received wrong commands message (no JSON).")

    def __del__(self):
        self.close()
        self.running = False


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    backend = DroneSimulator("127.0.0.1", int(sys.argv[1]))
    asyncore.loop()
