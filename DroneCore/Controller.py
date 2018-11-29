
import errno
import socket, time, json, sys, signal
import CoreLogger as clogger
import FlightPlanner as fp
import paho.mqtt.client as paho


class Controller:

    s_backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_execution = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger = clogger.logger

    id = -1         # id should be recieve from backend
    mqtt = None
    backend_topic = None

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

        if not connected:
            self.logger.error("No connection with backend established. Shutting down.")
            return False

        # connect with exection process
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.s_execution.connect((self.ip, self.port))
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

        # TODO: get current position somehow
        self.send_position_update((0,0,0))
        return True # controller successfully started

    def send_command(self, data):
        self.s_execution.send(bytearray(data, 'utf-8'))
        data = self.s_execution.recv(1024)

        if data == b'NOT_ARMED':
            return False               # Command failed

        data = json.loads(data.decode())
        self.send_position_update(data["position"])
        return True     # Command executed successfully

    def public_mqtt_callback(self, mosq, obj, msg):
        pass

    def unique_mqtt_callback(self, mosq, obj, msg):
        # jobs will come in here
        pass

    def send_position_update(self,position):
        data = {
            "id": self.id,
            "action": "position_update",
            "position": position
        }
        self.mqtt.publish(self.backend_topic, json.dumps(data),qos=2)

    def __del__(self):
        self.mqtt.disconnect()
        self.mqtt.loop_stop()
        self.s_backend.close()
        self.s_execution.close()


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
        "command": "set",
        "goal": (m1.x, m1.y, m1.z)
    }
    controller.send_command(json.dumps(initialze_command))

    for command in plan["commands"]:
        if not controller.send_command(json.dumps(command)):
            controller.logger.warn("Drone not armed yet!")
            arm_input = input("Type 'arm' to arm the drone: ")
            if arm_input.lower() == "arm":
                arm_command = {
                    "command": "arm"
                }
                controller.send_command(json.dumps(arm_command))
                controller.logger.info("Drone armed. Resuming flight path.")
                controller.send_command(json.dumps(command))
