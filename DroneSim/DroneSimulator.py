import sys

sys.path.append(sys.path[0] + "/..")

import DroneSim.Drone as Drone
import socket, signal, json, asyncore, threading, time
import Common.Marker as Marker
from json import JSONDecodeError

from Common.DBConnection import DBConnection


class ArmThread(threading.Thread):

    drone_connection = None

    def __init__(self, drone_connection):
        super().__init__()
        self.drone_connection = drone_connection

    def run(self):
        if self.drone_connection is not None:
            while self.drone_connection.running:
                if input("").lower() == "arm":
                    self.drone_connection.drone.arm()
                time.sleep(0.01)


def exit(signal, frame):
    print("Closing socket...")
    # emergency land drone?
    print("Simulator tured off.")
    sys.exit(0)


class DroneSimulator(asyncore.dispatcher):
    drone = Drone.Drone()

    def __init__(self, ip, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(1)  # only allow one incomming connection
        self.running = True
        self.drone.black_box.info("Drone simulator started.")
        self.markers = self.get_markers()
        self.arm_thread = ArmThread(self)
        self.arm_thread.start()

    def get_markers(self):
        db = DBConnection()
        # x,y,z,transitpoint
        markers = {}
        for m in db.query("select * from point"):
            marker = Marker.Marker(m[2], m[3], m[4], m[1])
            markers[m[1]] = marker
        if len(markers.keys()) == 0:
            self.drone.black_box.info("No markers loaded. Empty response from database.")
        return markers

    def handle_accept(self):
        pair = self.accept()  # wait for a connection
        if pair is None: return
        sock, addr = pair

        while self.running:
            data = sock.recv(2048)  # receive data with buffer of size 2048
            try:
                data = data.decode()
                if not data: continue
                data = json.loads(data)
                if data["action"] == "execute_command":
                    self.perform_action(data, sock)
                elif data["action"] == "send_position":
                    self.send_drone_position(sock)
                elif data["action"] == "send_status":
                    self.send_drone_status(sock)
            except JSONDecodeError:
                self.drone.black_box.error("Received non json message, dropping message.")

    def send_drone_position(self, connection):
        res = {
            "position": (float(self.drone.x), float(self.drone.y), float(self.drone.z)),
        }
        connection.send(json.dumps(res).encode())

    def send_drone_status(self, connection):
        res = {"status": self.drone.status.value}
        connection.send(json.dumps(res).encode())

    boundries = {
        "height": [0, 10],
        "velocity": [0, 0.5],
        "distance": [0, 5],
        "angle": [0, 360],
        "rate": [0, 5]
    }

    def check_values(self, command, *args):
        for to_check in args:
            try:
                if command[to_check] is None: return False
                values = self.boundries[to_check]
                if not (values[0] <= command[to_check] <= values[1]):
                    return False
            except KeyError: return False
        return True

    def perform_action(self, command, conn):
        try:
            if command["command"] == "set_position_marker":
                if command["id"] is not None:
                    if command["id"] in self.markers.keys():
                        marker = self.markers[command["id"]]
                        self.drone.setCoordinates(marker.x, marker.y, marker.z)
                        conn.send(b'ACK')
                        return
                conn.send(b'ERROR')
                return

            if self.drone.is_idle():
                # not armed return
                if command["command"] == "arm":
                    self.drone.arm()
                    conn.send(b'ACK')
                    return

                conn.send(b'NOT_ARMED')
                return

            if self.drone.is_armed():
                if command["command"] == "takeoff":
                    if self.check_values(command, "height", "velocity"):
                        self.drone.takeOff(command["height"], command["velocity"])
                        conn.send(b'ACK')
                        return

                if command["command"] == "disarm":
                    self.drone.disarm()
                    conn.send(b'ACK')
                    return

                conn.send(b'ERROR')
                return

            if self.drone.is_flying():
                if command["command"] == "land":
                    self.drone.land()
                    conn.send(b'ACK')
                    return

                elif command["command"] == "guided_land":
                    if self.check_values(command, "velocity"):
                        if command["id"] is not None:
                            if command["id"] in self.markers.keys():
                                marker = self.markers[command["id"]]
                                self.drone.guided_land(command["velocity"], marker.x, marker.y)
                                conn.send(b'ACK')
                                return

                elif command["command"] == "move":
                    if command["goal"] is not None:
                        goal = command["goal"]
                        if self.check_values(command, "velocity"):
                            self.drone.moveDistance(goal[0], goal[1], goal[2], command["velocity"])
                            conn.send(b'ACK')
                            return

                elif command["command"] == "forward":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.forward(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "backward":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.backward(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "left":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.left(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "right":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.right(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "up":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.up(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "down":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.down(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "turn_left":
                    if self.check_values(command, "angle", "rata"):
                        self.drone.turnLeft(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "turn_right":
                    if self.check_values(command, "angle", "rata"):
                        self.drone.turnRight(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "center":
                    if command["id"] is not None:
                        if command["id"] in self.markers.keys():
                            marker = self.markers[command["id"]]
                            self.drone.center(marker.x, marker.y)
                            conn.send(b'ACK')
                        return

                conn.send(b'ERROR')
                return

            conn.send(b'STATE_ERROR')
            return
        except Exception as e:
            if type(e) == JSONDecodeError:
                self.drone.black_box.error("Received wrong command message (no JSON).")
            else:
                self.drone.black_box.error("Command aborted.")

    def __del__(self):
        self.close()
        self.running = False
        self.arm_thread.join()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    backend = DroneSimulator("127.0.0.1", int(sys.argv[1]))
    asyncore.loop()
