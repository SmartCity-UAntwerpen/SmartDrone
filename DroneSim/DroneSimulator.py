import sys, enum

sys.path.append(sys.path[0] + "/..")

import DroneSim.Drone as Drone
import signal, json, time, threading
from Common.SocketCallback import SocketCallback
from Common.Marker import Marker


class FlightCommanderState(enum.Enum):
    NoProblem = 0
    Aborted = 1


class DroneFlightCommander:
    drone = Drone.Drone()
    state = FlightCommanderState.NoProblem

    def __init__(self, port, auto_arm=False):
        ip = "127.0.0.1"
        self.command_socket = SocketCallback(ip, port)
        self.command_socket.add_callback(self.handle_command)
        self.command_socket.start()
        self.status_socket = SocketCallback(ip, port + 1)
        self.status_socket.add_callback(self.handle_status_update)
        self.status_socket.start()
        self.markers = None
        self.auto_arm = auto_arm
        self.drone.black_box.info("Drone simulator started.")
        if self.auto_arm: self.drone.black_box.info("Auto arm enabled.")

    def handle_status_update(self, sock, data):
        try:
            data = data.decode()
            data = json.loads(data)
            self.drone.black_box.log(15,data)
            if data["action"] == "send_position":
                self.send_drone_position(sock)
            elif data["action"] == "send_status":
                self.send_drone_status(sock)
            elif data["action"] == "marker_update":
                self.markers = {}
                for marker in data["markers"].keys():
                    m = Marker()  # create empty marker
                    m.load_dict(data["markers"][marker])
                    self.markers[int(marker)] = m
                self.drone.black_box.info("Received marker update.")
        except ValueError:
            self.drone.black_box.error("Received non json message, dropping message.")
        except KeyError:
            self.drone.black_box.error("Message does not contain enough information.")

    def send_drone_position(self, connection):
        res = {
            "position": (float(self.drone.x), float(self.drone.y), float(self.drone.z)),
        }
        connection.send(json.dumps(res).encode())

    def send_drone_status(self, connection):
        res = {"status": self.drone.status.value}
        connection.send(json.dumps(res).encode())

    def handle_command(self, sock, data):
        try:
            data = data.decode()
            data = json.loads(data)
            if data["action"] == "execute_command":
                self.perform_action(data, sock)
            if data["action"] == "shutdown":
                exit(0,0)
            elif data["action"] == "wait_for_idle":
                result = "true"
                if self.drone.status is not Drone.DroneStatusEnum.Idle or self.state is not FlightCommanderState.NoProblem:
                    self.drone.black_box.info("Type 'reset' to reset the drone status to idle")
                    if not self.wait_for_idle(): result = "false"
                sock.send(json.dumps({"result": result }).encode())
        except ValueError:
            self.drone.black_box.error("Received non json message, dropping message.")

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
                    self.drone.black_box.warn("Values not valid.")
                    return False
            except KeyError:
                return False
        return True

    def perform_action(self, command, conn):
        try:
            self.drone.black_box.log(15, command)
            if command["command"] == "set_position_marker":
                if command["id"] is not None and self.markers is not None:
                    if command["id"] in [int(k) for k in self.markers.keys()]:
                        marker = self.markers[int(command["id"])]
                        self.drone.setCoordinates(marker.x, marker.y, marker.z)
                        conn.send(b'ACK')
                        return
                self.drone.black_box.error("Not able to set position marker because id is None or markers are None.")
                conn.send(b'ERROR')
                return

            if self.drone.is_idle():
                # not armed return
                if command["command"] == "arm":
                    self.drone.black_box.info("Arm drone.")
                    self.drone.arm()
                    conn.send(b'ACK')
                    return

                self.drone.black_box.info("Drone not armed yet wait for arm.")
                conn.send(b'NOT_ARMED')
                if self.wait_for_arm():
                    self.drone.black_box.info("Drone armed.")
                    conn.send(b'ACK')
                else:
                    self.drone.black_box.error("Drone was not armed.")
                    self.state = FlightCommanderState.Aborted
                    conn.send(b'ABORT')
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

                self.drone.black_box.error("Status: armed. Input is not a valid command: %s." % command["command"])
                conn.send(b'ERROR')
                return

            if self.drone.is_flying():
                self.drone.black_box.log(15, "Status: flying. Command %s" % command["command"])
                if command["command"] == "land":
                    self.drone.land()
                    conn.send(b'ACK')
                    return

                elif command["command"] == "guided_land":
                    if self.check_values(command, "velocity"):
                        if command["id"] is not None and self.markers is not None:
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
                    if command["id"] is not None and self.markers is not None:
                        if command["id"] in self.markers.keys():
                            marker = self.markers[command["id"]]
                            self.drone.center(marker.x, marker.y)
                            conn.send(b'ACK')
                        else:
                            self.state = FlightCommanderState.Aborted
                            conn.send(b'ABORT')
                        return

                self.drone.black_box.error("Command not executed.")
                conn.send(b'ERROR')
                return

            self.drone.black_box.error("State error.")
            conn.send(b'STATE_ERROR')
            return
        except Exception as e:
            if type(e) == ValueError:
                self.drone.black_box.error("Received wrong command message (no JSON).")
            self.state = FlightCommanderState.Aborted
            self.drone.black_box.error("Command aborted.")

    def wait_for_idle(self):
        if input("").lower() == "reset":
            self.drone.status = Drone.DroneStatusEnum.Idle
            self.state = FlightCommanderState.NoProblem
            return True
        return False

    def wait_for_arm(self):
        if self.auto_arm:
            self.drone.arm()
            return True
        elif input("").lower() == "arm":
            self.drone.arm()
            return True
        self.drone.status = Drone.DroneStatusEnum.EmergencyGamepadStop      # for test, remove is not necessary
        return False

    def close(self):
        self.status_socket.close()
        self.command_socket.close()


def exit(signal, frame):
    print("Closing drone...")
    flight_commander.close()
    print("Simulator tured off.")
    global running
    running = False
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    try:
        flight_commander = DroneFlightCommander(int(sys.argv[1]), auto_arm=(sys.argv[2] == "auto_arm"))
    except IndexError:
        flight_commander = DroneFlightCommander(int(sys.argv[1]))

    running = True
    while running:
        time.sleep(1)
