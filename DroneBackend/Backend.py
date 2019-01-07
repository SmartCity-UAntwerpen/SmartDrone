import paho.mqtt.client as paho
import json, enum, requests
import DroneBackend.BackendLogger as BackendLogger
import DroneBackend.RestAPI as REST
import Common.DBConnection as db_connection
from Common.Marker import Marker
from Common.FlightPlanner import FlightPlanner

backbone_url = "http://172.16.0.139"
base_topic = "smartcity/drones"
mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883


temp_markers = {
    0: Marker(0,0,0,0),
    1: Marker(1,0,0,1),
    2: Marker(2,0,0,2),
}


class DroneStatusEnum(enum.Enum):
    Init=0
    Idle=1
    Armed=2
    Flying=3
    EmergencyLowBattery=4
    EmergencyGamepadLoss=5
    EmergencyGamepadLand=6
    EmergencyGamepadStop=7


class Backend():

    logger = BackendLogger.logger
    mqtt = None
    api = None
    db = None
    markers = []
    flightplanner = FlightPlanner()
    jobs = {}
    active_jobs = {}
    active_drones = []          # simple solution, maybe a better solution is to add a  new state to the drones

    def __init__(self, ip, port, base_mqtt_topic):
        # Start tcp socket, drones connect to this socket to add themselves to the network
        self.ip = ip
        self.port = port

        # Connect to database
        self.db = db_connection.DBConnection()
        self.markers = self.db.get_markers()

        #self.markers = temp_markers

        self.flightplanner.update_markers(self.markers)

        # Setup MQTT here
        self.base_mqtt_topic = base_mqtt_topic
        self.mqtt = paho.Client()
        self.mqtt.message_callback_add(base_mqtt_topic + "/backend", self.mqtt_callback)
        self.mqtt.connect(mqtt_broker, mqtt_port, 60)
        self.mqtt.subscribe(base_mqtt_topic + "/#")
        self.mqtt.loop_start()

        self.drones, self.ids = self.db.load_drones()
        self.logger.info("Backend started.")

    def add_drone(self, unique_msg):
        self.logger.info("Add_drone %s." % unique_msg)
        if unique_msg in self.ids.keys():
            new_drone_id = self.ids[unique_msg]
            location = self.db.get_location(new_drone_id)
            self.drones[new_drone_id] = location
            self.logger.info("Drone reconnected: [id] %d, [unique_msg] %s, [location] (%0.2f, %0.2f, %0.2f)"
                             % (new_drone_id, unique_msg, location[0], location[1], location[2]))
        else:
            new_drone_id = self.get_new_drone_id()
            self.ids[unique_msg] = new_drone_id
            self.drones[new_drone_id] = (0, 0, 0)
            self.db.add_drone(new_drone_id, str(unique_msg), (0, 0, 0))  # save unique_msg as string
            self.logger.info("New Drone connected: [id] %d, [unique_msg] %s" % (new_drone_id, unique_msg))
        reply = {
            "id": new_drone_id,
            "mqtt_topic": self.base_mqtt_topic,
            "mqtt_broker": mqtt_broker,
            "mqtt_port": mqtt_port
        }
        return reply

    def get_new_drone_id(self):
        for i in range(len(self.ids)):
            if i not in self.ids.values():
                return i
        return len(self.ids)

    def remove_drone(self, drone_id):
        self.logger.info("Remove drone %s." %drone_id)
        drone_id = int(drone_id)
        if drone_id in self.drones.keys():
            del self.drones[drone_id]
            if drone_id in self.ids.values():
                unique = list(self.ids.keys())[list(self.ids.values()).index(drone_id)]
                del self.ids[unique]
                self.db.remove_drone(drone_id, str(unique))
                self.logger.info("Drone removed: [id] %d, [unique_msg] %s" % (drone_id, unique))
                return {"result": "true"}
        return {"result": "false"}

    def mqtt_callback(self, mosq, obj, msg):
        data = json.loads(msg.payload.decode())
        self.logger.log(15, data)
        if data["action"] is None or data["id"] is None:
            self.logger.warn("Received uncomplete JSON message (no id or action field).")
            return

        if int(data["id"]) not in self.ids.values():
            self.logger.warn("Received message from unkown drone with id: %d" % int(data["id"]))
            return

        try:
            if data["action"] == "position_update":
                self.drones[int(data["id"])] = data["position"]
                self.db.update_drone(int(data["id"]), (data["position"][0], data["position"][1], data["position"][2]))
                self.logger.info("Position update. Drone id: %d, new position: (%.2f %.2f %.2f)"
                                 % (data["id"], data["position"][0], data["position"][1], data["position"][2]))
            elif data["action"] == "status_update":
                self.logger.info("Status update. Drone id: %d, status: %s" % (data["id"], data["status"]))
                if int(data["status"]) == DroneStatusEnum.Idle.value:
                    self.assign_job_to_drone(int(data["id"]))
            elif data["action"] == "job_complete":
                drone_id = data["id"]
                if int(drone_id) in self.active_drones:
                    self.logger.info("Drone with id: %d completed its job: with status: %s", (int(drone_id), data["status"]))
                    self.active_drones.remove(int(drone_id))
                    job = self.active_jobs[int(drone_id)]
                    del self.active_jobs[int(drone_id)]
                    # INFORM BACKBONE
                    url = backbone_url + "/job/complete/" + str(job["job_id"])
                    try: requests.post(url)
                    except: self.logger.warn("Job status complete send to backbone failed")
        except KeyError:
            self.logger.warn(
                "Received message with action: %s, not enough data provided to perform action." % data["action"])

    def assign_job_to_drone(self, drone_id):
        if len(self.jobs) != 0 and drone_id not in self.active_drones:
            job_id = list(self.jobs.keys()).pop(0)

            job = self.jobs[job_id]
            job["action"] = "no_plan_job"       # backend now does not make the flightplan, in the future the flight plan could be created here
            self.mqtt.publish(base_topic + "/" + str(drone_id), json.dumps(job), qos=2)
            self.logger.info("Deploying job to drone [id]: %d, [job_id] %d" % (drone_id, job_id))

            self.active_jobs[drone_id] = self.jobs[job_id]
            self.active_drones.append(drone_id)
            del self.jobs[job_id]

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
    backend = Backend("0.0.0.0", 8082, base_topic)
    REST.RestApi(backend)
