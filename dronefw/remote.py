#!/usr/bin/env python3

import sys, time

sys.path.append(sys.path[0] + "/..")

import drone as Drone
import socket, signal, json, asyncore, threading
import Common.Marker as Marker
import logger as dlogger
from Common.DBConnection import DBConnection


class ArmThread(threading.Thread):

    drone_connection = None

    def __init__(self, drone_connection):
        super().__init__()
        self.drone_connection = drone_connection

    def run(self):
        while self.drone_connection.running and self.drone_connection is not None:
            if self.drone_connection.drone.Gamepad.Start == 1:
                self.drone_connection.drone.Arm()
            time.sleep(0.01)

    def join(self, timeout=0):
        print("test1")
        super().join(timeout)
        print("test2")


class DroneConnector(asyncore.dispatcher):

    drone = Drone.DroneClass()
    logger = dlogger.create_logger()
    px = 0
    py = 0
    pz = 0

    def __init__(self, ip, port):
        LastStatusTime = 0
        StatusUpdateInterval = 3
        if time.time() - LastStatusTime > StatusUpdateInterval:
            print("Battery voltage:%s" % (self.drone.Vbat))
            print("Status:%s" % (self.drone.DroneStatus))
            print("")
            LastStatusTime = time.time()
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind((ip, port))
            self.listen(1)  # only allow one incomming connection
            self.running = True
            self.logger.info("Drone process started.")
            self.markers = self.get_markers()
            #self.arm_thread = ArmThread(self)
            #self.arm_thread.start()
        else:
            self.running = False

    def get_markers(self):
        db = DBConnection()
        # x,y,z,transitpoint
        markers = {}
        for m in db.query("select * from point"):
            marker = Marker.Marker(m[2], m[3], m[4], m[1])
            markers[m[1]] = marker
        if len(markers.keys()) == 0:
            self.logger.info("No markers loaded. Empty response from database.")
        return markers

    def handle_accept(self):
        pair = self.accept()  # wait for a connection
        if pair is None: return
        sock, addr = pair

        connected = True
        while connected:
            data = sock.recv(2048)  # receive data with buffer of size 2048
            try:
                data = data.decode()
                if not data: connected = False
                data = json.loads(data)
                if data["action"] == "execute_command":
                    self.perform_action(data, sock)
                elif data["action"] == "send_position":
                    self.send_drone_position(sock)
                elif data["action"] == "send_status":
                    self.send_drone_status(sock)
            except ValueError:
                self.logger.error("Received non json message, dropping message.")

    def send_drone_position(self, connection):
        res = {
            "position": (float(self.px), float(self.py), float(self.pz)),
        }
        connection.send(json.dumps(res).encode())

    def send_drone_status(self, connection):
        res = {"status": self.drone.DroneStatus.value}
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
                        self.px = marker.x
                        self.py = marker.y
                        self.pz = marker.z
                        conn.send(b'ACK')
                        return
                conn.send(b'ERROR')
                return

            if self.drone.DroneStatus == Drone.DroneStatusEnum.Idle:
                if command["command"] == "arm":
                    #self.drone.Arm()
                    conn.send(b'ACK')
                    return

                conn.send(b'NOT_ARMED')
                if self.wait_for_arm(10):
                    conn.send(b'ACK')
                else:
                    conn.send(b'NOT ARMED')
                return

            if self.drone.DroneStatus == Drone.DroneStatusEnum.Armed:
                if command["command"] == "takeoff":
                    if self.check_values(command, "height", "velocity"):
                        self.drone.mc.TakeOff(command["height"], command["velocity"])
                        conn.send(b'ACK')
                        return

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
                    if self.check_values(command, "angle", "rata"):
                        self.drone.mc.TurnLeft(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "turn_right":
                    if self.check_values(command, "angle", "rata"):
                        self.drone.mc.TurnRight(command["angle"], command["rate"])
                        conn.send(b'ACK')
                        return

                elif command["command"] == "center":
                    marker = self.drone.ArucoNav.Center()
                    if marker is None:
                        self.drone.mc.land()
                        conn.send(b'ABORT')
                    else:
                        marker = self.markers[marker.id]
                        self.px = marker.x
                        self.py = marker.y
                        self.pz = marker.z
                        conn.send(b'ACK')
                    return

                conn.send(b'ERROR')
                return

            conn.send(b'STATE_ERROR')
            return
        except Exception as e:
            if type(e) == ValueError:
                self.logger.error("Received wrong command message (no JSON).")
            else:
                self.logger.error("Command aborted.")
                conn.send(b'ABORT')

    def wait_for_arm(self,timeout):
        sleep_time = 0.1
        counter = 0
        self.logger.error("wait for arm")
        while self.running and counter <= timeout:
            if self.drone.Gamepad.Start == 1:
                self.drone.Arm()
                self.logger.error("drone armed")
                return True
            counter += sleep_time
            time.sleep(sleep_time)

        self.logger.error("timeout drone not armed")
        return False


    def close(self):
        self.running = False
        print("test0")
        #self.arm_thread.join()

def exit(signal, frame):
    print("Closing drone...")
    global drone_connection
    drone_connection.close()
    print("Drone tured off.")
    try:
        sys.exit(0)
    except Exception as e: print(e)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)

    drone_connection = DroneConnector("127.0.0.1", int(sys.argv[1]))

    if drone_connection.running:
        asyncore.loop()
    else:
        print("Error starting drone.")




