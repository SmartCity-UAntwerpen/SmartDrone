import paho.mqtt.client as paho
import json
import DroneBackend.BackendLogger as BackendLogger
import DroneBackend.RestAPI as REST
import Common.DBConnection as db_connection
from Common.Marker import Marker

base_topic = "smartcity/drones/test"
mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883


temp_markers = {
    0: Marker(0,0,0,0),
    1: Marker(1,1,0,1),
    2: Marker(2,1,0,2),
}


class Backend():

    logger = BackendLogger.logger
    mqtt = None
    api = None
    db = None
    markers = []

    def __init__(self, ip, port, base_mqtt_topic):
        # Start tcp socket, drones connect to this socket to add themselves to the network
        self.ip = ip
        self.port = port

        # Connect to database
        #db = db_connection.DBConnection()
        #self.markers = db.get_markers()

        self.markers = temp_markers

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

    def add_drone(self, unique_msg):
        new_drone_id = self.ids[unique_msg] if unique_msg in self.ids.keys() else self.get_new_drone_id()
        reply = {
            "id": new_drone_id,
            "mqtt_topic": self.base_mqtt_topic,
            "mqtt_broker": mqtt_broker,
            "mqtt_port": mqtt_port
        }
        self.ids[unique_msg] = new_drone_id
        self.drones[new_drone_id] = (0, 0, 0)
        self.logger.info("Drone connected: [id] %d, [unique_msg] %s" % (new_drone_id, unique_msg))
        return reply

    def get_new_drone_id(self):
        for i in range(len(self.ids)):
            if i not in self.ids.values():
                return i
        return len(self.ids)

    def remove_drone(self, drone_id):
        drone_id = int(drone_id)
        if drone_id in self.drones.keys():
            del self.drones[drone_id]
            if drone_id in self.ids.values():
                unique = list(self.ids.keys())[list(self.ids.values()).index(drone_id)]
                del self.ids[unique]
                self.logger.info("Drone removed: [id] %d, [unique_msg] %s" % (drone_id, unique))
                return {"result": "succes"}
        return {"result": "failed"}

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
                                 % (data["id"], data["position"][0], data["position"][1], data["position"][2]))
            elif data["action"] == "status_update":
                self.logger.info("Status update. Drone id: %d, status: %s" % (data["id"], data["status"]))
        except KeyError:
            self.logger.warn(
                "Received message with action: %s, not enough data provided to perform action." % data["action"])

    def find_location(self, id):
        return self.drones[id]

    def set_location(self, id, location):
        if id in self.drones.keys():
            self.drones[id] = location

    def __del__(self):
        self.mqtt.disconnect()
        self.mqtt.loop_stop()


def start_backend():
    global backend
    backend = Backend("127.0.0.1", 8082, base_topic)
    REST.RestApi(backend)

    # TODO: add nodes from database
    # TODO: make use of flightplanner
    # TODO: accept a job from the maas


