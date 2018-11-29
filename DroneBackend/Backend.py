
import paho.mqtt.client as paho
import json, socket, asyncore
import BackendLogger

mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883

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
        self.logger.info("Backend started.")

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        sock, addr = pair
        new_drone_id = len(self.drones.keys())
        reply = {
            "id": new_drone_id,
            "mqtt_topic": self.base_mqtt_topic,
            "mqtt_broker": mqtt_broker,
            "mqtt_port": mqtt_port
        }
        sock.send(json.dumps(reply).encode())
        self.drones[new_drone_id] = (0,0,0)
        self.logger.info("New drone connected: [id] %d, [ip_addr] %s" % (new_drone_id, str(addr)))

    def mqtt_callback(self, mosq, obj, msg):
        data = json.loads(msg.payload.decode())

        if data["action"] == "position_update":
            self.drones[int(data["id"])] = data["position"]
            self.logger.info("Position update. Drone id: %d, new position: (%.2f %.2f %.2f)"
                             % (data["id"],data["position"][0],data["position"][1],data["position"][2]))

    def find_location(self, id):
        return self.drones[id]

    def set_location(self,id,location):
        if id in self.drones.keys():
            self.drones[id] = location

    def __del__(self):
        self.mqtt.disconnect()
        self.mqtt.loop_stop()
        self.close()


if __name__ == "__main__":
    backend = Backend("0.0.0.0", 5001,"smartcity/drones")
    asyncore.loop()


    #TODO: add nodes from database
    #TODO: make use of flightplanner
    #TODO: accept a job from the maas
