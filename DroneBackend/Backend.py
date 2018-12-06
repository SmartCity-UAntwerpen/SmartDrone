
import paho.mqtt.client as paho
import json, socket, asyncore
import BackendLogger
from json import JSONDecodeError
from flask import Flask
import sys, multiprocessing, signal

base_topic = "smartcity/drones"
mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883

app = Flask("DroneBackend")


class RestApi():

    api = multiprocessing.Process(target=app.run, args=("0.0.0.0",8082))

    def start(self):
        self.api.start()

    def join(self):
        self.api.terminate()
        self.api.join()


class Backend(asyncore.dispatcher):

    logger = BackendLogger.logger
    mqtt = None

    def __init__(self,ip,port,base_mqtt_topic):
        # Start tcp socket, drones connect to this socket to add themselves to the network
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(3)      # Allow 3 drones to be connected to the backend with tcp at the same time

        # Setup MQTT here
        self.base_mqtt_topic = base_mqtt_topic
        self.mqtt = paho.Client()
        self.mqtt.message_callback_add(base_mqtt_topic + "/backend", self.mqtt_callback)
        self.mqtt.connect(mqtt_broker, mqtt_port, 60)
        self.mqtt.subscribe(base_mqtt_topic + "/#")
        self.mqtt.loop_start()

        self.drones = {}
        self.ids = {}
        self.logger.info("Backend started.")

    def handle_accept(self):
        pair = self.accept()
        if pair is None: return
        sock, addr = pair

        data = sock.recv(2048).decode()
        try:
            data = json.loads(data)
            new_drone_id = self.ids[data["unique"]] if data["unique"] in self.ids.keys() else len(self.ids)
            reply = {
                "id": new_drone_id,
                "mqtt_topic": self.base_mqtt_topic,
                "mqtt_broker": mqtt_broker,
                "mqtt_port": mqtt_port
            }
            sock.send(json.dumps(reply).encode())
            self.ids[data["unique"]] = new_drone_id
            self.drones[new_drone_id] = (0, 0, 0)
            self.logger.info("Drone connected: [id] %d, [unique_msg] %s" % (new_drone_id, data["unique"]))
        except JSONDecodeError:
            self.logger.error("Received message (TCP) not json decodable.")

    def mqtt_callback(self, mosq, obj, msg):
        data = json.loads(msg.payload.decode())

        if data["action"] is None or data["id"] is None:
            self.logger.warn("Received uncomplete JSON message (no id or action field).")
            return

        if int(data["id"]) not in self.ids.values():
            self.logger.warn("Received message from unkown drone with id: %d" % int(data["id"]))
            return

        try:
            if data["action"] == "position_update":
                self.drones[int(data["id"])] = data["position"]
                self.logger.info("Position update. Drone id: %d, new position: (%.2f %.2f %.2f)"
                                 % (data["id"],data["position"][0],data["position"][1],data["position"][2]))
        except KeyError:
            self.logger.warn("Received message with action: %s, not enough data provided to perform action." % data["action"])

    def find_location(self, id):
        return self.drones[id]

    def set_location(self,id,location):
        if id in self.drones.keys():
            self.drones[id] = location

    def __del__(self):
        self.mqtt.disconnect()
        self.mqtt.loop_stop()
        self.close()


def exit(signal, frame):
    print("Terminating Backend...")
    global api
    api.join()
    global backend
    del backend
    sys.exit(0)


@app.route('/link')
def link_api():
    data = json.loads(open('carlinks.json').read())
    return json.dumps(data)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    backend = Backend("0.0.0.0", 5001, base_topic)
    api = RestApi()
    api.start()
    asyncore.loop()


    #TODO: add nodes from database
    #TODO: make use of flightplanner
    #TODO: accept a job from the maas
