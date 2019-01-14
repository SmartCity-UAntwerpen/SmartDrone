#!/usr/bin/env python3

import sys, time, enum

sys.path.append(sys.path[0] + "/..")

import drone as Drone
import signal, json
import Common.Marker as Marker
import logger as dlogger
from Common.Marker import Marker
from Common.SocketCallback import SocketCallback


class FlightCommanderState(enum.Enum):
    NoProblem = 0
    Aborted = 1     # more states can be added to better define the problem

class DroneFlightCommander:

    drone = Drone.DroneClass()
    logger = dlogger.create_logger()
    px = 0
    py = 0
    pz = 0
    state = FlightCommanderState.NoProblem

    def __init__(self, port):
        LastStatusTime = 0
        StatusUpdateInterval = 3
        if time.time() - LastStatusTime > StatusUpdateInterval:
            self.logger.info("Battery voltage:%s" % (self.drone.Vbat))
            self.logger.info("Status:%s" % (self.drone.DroneStatus))
            LastStatusTime = time.time()
            ip = "127.0.0.1"
            self.command_socket = SocketCallback(ip, port)
            self.command_socket.add_callback(self.handle_command)
            self.command_socket.start()
            self.status_socket = SocketCallback(ip, port + 1)
            self.status_socket.add_callback(self.handle_status_update)
            self.status_socket.start()
            self.markers = None
            self.logger.info("Drone started.")
            self.running = True
        else:
            self.running = False

    def handle_status_update(self, sock, data):
        try:
            data = data.decode()
            data = json.loads(data)
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
                self.logger.info("Received marker update.")
        except ValueError:
            self.logger.exception(ValueError)
            self.logger.error("Received non json message, dropping message.")
        except KeyError:
            self.logger.exception(KeyError)
            self.logger.error("Message does not contain enough information.")

    def send_drone_position(self, connection):
        res = {
            "position": (float(self.px), float(self.py), float(self.pz)),
        }
        connection.send(json.dumps(res).encode())

    def send_drone_status(self, connection):
        if self.state != FlightCommanderState.NoProblem and self.drone.DroneStatus == Drone.DroneStatusEnum.Idle:
            # when state != noproblem and drone state is idle, jobs will be send to drone, to avoid this we send another state
            res = {"status": Drone.DroneStatusEnum.EmergencyGamepadLand.value }
        else:
            res = {"status": self.drone.DroneStatus.value}
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
                if self.drone.DroneStatus is not Drone.DroneStatusEnum.Idle or self.state is not FlightCommanderState.NoProblem:
                    if not self.wait_for_idle(120): result = "false"
                sock.send(json.dumps({"result": result }).encode())
        except ValueError:
            self.logger.exception(ValueError)
            self.logger.error("Received non json message, dropping message.")

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
                    self.logger.error("Values not in boundaries")
                    return False
            except KeyError:
                self.logger.exception(KeyError)
                return False
        return True

    def perform_action(self, command, conn):
        try:
            self.logger.log(15, command["command"])
            if command["command"] == "set_position_marker":
                if command["id"] is not None and self.markers is not None:
                    if command["id"] in [int(k) for k in self.markers.keys()]:
                        marker = self.markers[int(command["id"])]
                        self.px = marker.x
                        self.py = marker.y
                        self.pz = marker.z
                        conn.send(b'ACK')
                        return
                self.logger.error("Command id was None or self.markers were none.")
                conn.send(b'ERROR')
                return

            if self.drone.DroneStatus == Drone.DroneStatusEnum.Idle:
                self.logger.info("Arming drone.")
                if command["command"] == "arm":
                    #self.drone.Arm()
                    conn.send(b'ACK')
                    return

                self.logger.info("Drone not armed yet wait for arm.")
                conn.send(b'NOT_ARMED')
                if self.wait_for_arm(120):
                    self.logger.info("Drone armed.")
                    conn.send(b'ACK')
                else:
                    self.logger.info("Drone not armed abort.")
                    self.state = FlightCommanderState.Aborted
                    conn.send(b'ABORT')
                return

            if self.drone.DroneStatus == Drone.DroneStatusEnum.Armed:
                if command["command"] == "takeoff":
                    if self.check_values(command, "height", "velocity"):
                        self.drone.mc.TakeOff(command["height"], command["velocity"])
                        conn.send(b'ACK')
                        return

                self.logger.error("Status armed, command invalid.")
                conn.send(b'ERROR')
                return

            if self.drone.DroneStatus == Drone.DroneStatusEnum.Flying:
                if command["command"] == "land":
                    self.drone.mc.land()
                    conn.send(b'ACK')
                    return

                elif command["command"] == "guided_land":
                    self.drone.ArucoNav.GuidedLand()
                    conn.send(b'ACK')
                    return

                elif command["command"] == "move":
                    if command["goal"] is not None:
                        goal = command["goal"]
                        if self.check_values(command, "velocity"):
                            self.drone.mc.MoveDistance(goal[0], goal[1], goal[2], command["velocity"])
                            conn.send(b'ACK')
                            return

                elif command["command"] == "forward":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Forward(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "backward":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Backward(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "left":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Left(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "right":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Right(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "up":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Up(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "down":
                    if self.check_values(command, "distance", "velocity"):
                        self.drone.mc.Down(command["distance"], command["velocity"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "turn_left":
                    if self.check_values(command, "angle", "rate"):
                        self.drone.mc.TurnLeft(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "turn_right":
                    if self.check_values(command, "angle", "rate"):
                        self.drone.mc.TurnRight(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "center":
                    marker = self.drone.ArucoNav.Center()
                    self.logger.info(marker)
                    if marker is None:
                        self.drone.ArucoNav.GuidedLand()
                        self.logger.error("No marker detected")
                        self.state = FlightCommanderState.Aborted
                        conn.send(b'ABORT')
                        return
                    else:
                        if marker.Id is not int(command["id"]):
                            self.drone.ArucoNav.GuidedLand()
                            self.logger.error("Wrong marker detected, abort execution!")
                            self.state = FlightCommanderState.Aborted
                            conn.send(b'ABORT')
                            return
                        if self.markers is not None:
                            marker = self.markers[marker.Id]
                            self.px = marker.x
                            self.py = marker.y
                            self.pz = marker.z
                        conn.send(b'ACK')
                    return

                self.logger.error("Command not executed.")
                conn.send(b'ERROR')
                return

            self.logger.error("State Exception.")
            conn.send(b'STATE_ERROR')
            return
        except Exception as e:
            self.logger.exception(e)
            self.logger.info("Exception occured, drone state: %d" % self.drone.DroneStatus.value)
            if type(e) == ValueError:
                self.logger.error("Received wrong command message (no JSON).")
            if self.drone.DroneStatus is Drone.DroneStatusEnum.Flying:
                self.drone.ArucoNav.GuidedLand()
            self.state = FlightCommanderState.Aborted
            self.logger.error("Command aborted.")
            conn.send(b'ABORT')

    def wait_for_idle(self,timeout):
        sleep_time = 0.1
        counter = 0
        self.logger.info("Wait for idle.")
        while self.running and counter <= timeout:
            if self.drone.Gamepad.L2 == 1:
                self.drone.ClearEmergency()
                self.state = FlightCommanderState.NoProblem
                self.logger.info("Drone state set to idle.")
                return True
            counter += sleep_time
            time.sleep(sleep_time)

        self.logger.error("Timeout drone not set in idle state.")
        return False

    def wait_for_arm(self,timeout):
        sleep_time = 0.1
        counter = 0
        self.logger.info("Wait for arm.")
        while self.running and counter <= timeout:
            if self.drone.Gamepad.Start == 1:
                self.drone.Arm()
                self.logger.info("Drone armed.")
                return True
            counter += sleep_time
            time.sleep(sleep_time)

        self.logger.error("Timeout drone not armed.")
        return False

    def close(self):
        self.status_socket.close()
        self.command_socket.close()

def exit(signal, frame):
    print("Closing drone...")
    flight_commander.close()
    print("Drone tured off.")
    global running
    running = False
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    flight_commander = DroneFlightCommander(int(sys.argv[1]))

    running = True
    while running:
        time.sleep(1)
