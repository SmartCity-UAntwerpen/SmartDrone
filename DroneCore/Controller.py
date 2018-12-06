
import errno
import socket, time, json, sys, signal
from json import JSONDecodeError
import CoreLogger as clogger
import FlightPlanner as fp
import paho.mqtt.client as paho
from uuid import getnode as get_mac
import threading
import SharedSocket


class Poller(threading.Thread):

    running = True

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        while self.running:
            controller.send_position_update()
            #controller.send_status_update()
            time.sleep(2)

    def join(self, timeout=0):
        self.running = False
        super().join(timeout)


class Controller:

    s_backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_execution = SharedSocket.SharedSocket()
    logger = clogger.logger

    id = -1         # id should be received from backend
    mqtt = None
    backend_topic = None
    socket_lock = threading.Lock()

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def start_controller(self):
        # subscribe to backend
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.s_backend.connect(("0.0.0.0", 5001))
                connected = True

                # send unique message to get id from the backend
                mac = get_mac()
                message = { "unique": mac + self.port }
                self.s_backend.send(json.dumps(message).encode())

                data = json.loads(self.s_backend.recv(1024).decode())
                self.id = data["id"]

                self.mqtt = paho.Client()
                self.mqtt.message_callback_add(data["mqtt_topic"] + "/" + str(self.id), self.unique_mqtt_callback)
                self.mqtt.message_callback_add(data["mqtt_topic"], self.public_mqtt_callback)
                self.mqtt.connect(data["mqtt_broker"], data["mqtt_port"], 60)
                self.mqtt.subscribe(data["mqtt_topic"] + "/#")
                self.mqtt.loop_start()
                self.backend_topic = data["mqtt_topic"] + "/backend"

                self.logger.info("Succesfully subscribed to the backend. Recieved id: %d" % self.id)
            except socket.error as error:
                if error.errno == errno.ECONNREFUSED:
                    self.logger.warn("Connection to backend refused. Retrying...")
                    counter += 1
                    time.sleep(2)
                else: break

        if not connected:
            self.logger.error("No connection with backend established. Shutting down.")
            return False

        # connect with exection process
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.s_execution.connect(self.ip, self.port)
                connected = True
                self.logger.info("Connection with exectution process established.")
            except socket.error as error:
                if error.errno == errno.ECONNREFUSED:
                    self.logger.warn("Connection to exectution process refused. Retrying...")
                    counter += 1
                    time.sleep(2)
                else: break

        if not connected:
            self.logger.error("Connection with exectution process not established. Shutting down.")
            return False

        self.poller = Poller(self)
        self.poller.start()
        return True # controller successfully started

    def send_command(self, data):
        data = self.s_execution.send_and_receive(data.encode())

        if data == b'NOT_ARMED':
            return False               # Command failed

        return True     # Command executed successfully

    def public_mqtt_callback(self, mosq, obj, msg):
        # possibility to recieve commands from the backend sent to all drones
        pass

    def unique_mqtt_callback(self, mosq, obj, msg):
        # jobs will come in here
        pass

    def send_position_update(self):
        message = { "action": "send_position" }
        data = self.s_execution.send_and_receive(json.dumps(message).encode())
        try:
            data = json.loads(data.decode())
            res = {
                "id": self.id,
                "action": "position_update",
                "position": data["position"]
            }
            self.mqtt.publish(self.backend_topic, json.dumps(res), qos=2)
        except JSONDecodeError: self.logger.error("Position result was not in the correct format (no JSON).")

    def send_status_update(self):
        message = {"action": "send_status"}
        data = self.s_execution.send_and_receive(json.dumps(message).encode())
        try:
            data = json.loads(data.decode())
            res = {
                "id": self.id,
                "action": "status_update",
                "position": data["status"]
            }
            self.mqtt.publish(self.backend_topic, json.dumps(res), qos=2)
        except JSONDecodeError:
            self.logger.error("Position result was not in the correct format (no JSON).")

    def __del__(self):
        self.mqtt.disconnect()
        self.mqtt.loop_stop()
        self.s_backend.close()
        self.s_execution.close()
        self.poller.join()


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

    flight_planner = fp.FlightPlanner()
    m1 = flight_planner.getMarker(0)
    m2 = flight_planner.getMarker(3)

    plan = flight_planner.findPath(m1,m2)

    initialze_command = {
        "action": "execute_command",
        "command": "set",
        "goal": (m1.x, m1.y, m1.z)
    }
    controller.send_command(json.dumps(initialze_command))

    for command in plan["commands"]:
        command["action"] = "execute_command"
        if not controller.send_command(json.dumps(command)):
            controller.logger.warn("Drone not armed yet!")
            arm_input = input("Type 'arm' to arm the drone: ")
            if arm_input.lower() == "arm":
                arm_command = {
                    "action": "execute_command",
                    "command": "arm"
                }
                controller.send_command(json.dumps(arm_command))
                controller.logger.info("Drone armed. Resuming flight path.")
                controller.send_command(json.dumps(command))
