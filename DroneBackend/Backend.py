import paho.mqtt.client as paho
import json, enum, requests, threading, time, math
import DroneBackend.BackendLogger as BackendLogger
import DroneBackend.RestAPI as REST
import Common.DBConnection as db_connection
from Common.FlightPlanner import FlightPlanner

mqtt_broker = "smartcity.ddns.net"
#mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_username = "root"
mqtt_password = "smartcity"


class DroneStatusEnum(enum.Enum):
    Init=0
    Idle=1
    Armed=2
    Flying=3
    EmergencyLowBattery=4
    EmergencyGamepadLoss=5
    EmergencyGamepadLand=6
    EmergencyGamepadStop=7


class DroneAliveChecker(threading.Thread):

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.running = True

    def run(self):
        """ Check every 10 seconds if drones has at least once sent a status update,
        if not and last message was 20 seconds ago then we remove the drone from backend """
        counter = 0
        time_step = 0.1
        while self.running:
            if counter >= 10: # check if drones are alive every 10 seconds
                self.backend.logger.info("Checking if drones are alive...")
                for drone in list(self.backend.drones.keys()):
                    remove = False
                    if drone not in self.backend.alive_drones: remove = True
                    elif (time.time() - self.backend.alive_drones[drone]) > 20: remove = True   # 20 seconds because real drone can take some time to start sending messages
                    if remove:
                        self.backend.logger.info(
                            "Drone with id %d, did not send status update in time, removing drone." % drone)
                        self.backend.remove_drone(drone)
                        if drone in self.backend.alive_drones: del self.backend.alive_drones[drone]
                counter = 0
            counter += time_step
            time.sleep(time_step)

    def join(self, timeout=0):
        self.running = False
        super().join(timeout)


class Backend():

    backbone_url = "http://smartcity.ddns.net:10000"
    base_mqtt_topic = "smartcity/drones"
    logger = BackendLogger.logger
    mqtt = None
    api = None
    db = None
    markers = []
    flightplanner = FlightPlanner()
    jobs = {}
    active_jobs = {}
    active_drones = []
    drones = []
    ids = []
    alive_drones = {}

    def __init__(self, ip, port, base_mqtt_topic=None, backbone_url=None):
        # Start tcp socket, drones connect to this socket to add themselves to the network
        self.ip = ip
        self.port = port

        if backbone_url: self.backbone_url = backbone_url
        if base_mqtt_topic: self.base_mqtt_topic = base_mqtt_topic

        # Connect to database
        self.db = db_connection.DBConnection("smartcity.ddns.net", "smartcity")
        self.markers = self.db.get_markers()

        self.flightplanner.update_markers(self.markers)

        # Setup MQTT
        self.mqtt = paho.Client()
        self.mqtt.message_callback_add(base_mqtt_topic + "/backend", self.mqtt_callback)
        self.mqtt.username_pw_set(mqtt_username, mqtt_password)
        self.mqtt.connect(mqtt_broker, mqtt_port, 60)
        self.mqtt.subscribe(base_mqtt_topic + "/#")
        self.mqtt.loop_start()

        self.drones, self.ids = self.db.load_drones()
        self.jobs, self.active_jobs, self.active_drones = self.db.load_jobs()
        
        #clean start
        self.hard_reset()

        self.drone_alive_checker = DroneAliveChecker(self)
        self.drone_alive_checker.start()
        self.logger.info("Backend started.")
        self.logger.info("Backbone url: %s" % self.backbone_url)
        self.logger.info("Base MQTT topic: %s" % self.base_mqtt_topic)

    def add_drone(self, unique_msg):
        """ Create an id for the drone by using the unique msg, which is mac + port from drone, reply with mqtt details"""
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
        self.alive_drones[new_drone_id] = time.time()
        reply = {
            "id": new_drone_id,
            "mqtt_topic": self.base_mqtt_topic,
            "mqtt_broker": mqtt_broker,
            "mqtt_port": mqtt_port,
            "mqtt_username": mqtt_username,
            "mqtt_password": mqtt_password
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
            # check if drone had active job, remove when true
            if drone_id in self.active_drones:
                self.job_failed(drone_id, "drone removed")
            # remove unique id from stored ids
            if drone_id in self.ids.values():
                unique = list(self.ids.keys())[list(self.ids.values()).index(drone_id)]
                del self.ids[unique]
                self.db.remove_drone(drone_id, str(unique))
                self.logger.info("Drone removed: [id] %d, [unique_msg] %s" % (drone_id, unique))
                return True
        return False

    def remove_job(self, drone_id):
        self.active_drones.remove(int(drone_id))
        # remove job from db
        self.db.remove_job(drone_id)
        del self.active_jobs[int(drone_id)]

    def mqtt_callback(self, mosq, obj, msg):
        """ Base MQTT callback for backend, here json messages with at least the fields id and action are expected."""
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
                self.alive_drones[int(data["id"])] = time.time()
                if int(data["status"]) == DroneStatusEnum.Idle.value:
                    self.assign_job_to_drone(int(data["id"]))
            elif data["action"] == "job_complete":
                self.job_complete(data["id"])
            elif data["action"] == "job_failed":
                #job_failed method redeploys job 3 times, if job is cancelled, it does not need to be redeployed, so it is directly removed.
                if data["reason"] != "Job cancelled":
                    self.job_failed(data["id"], data["reason"])
                else:
                    self.remove_job(data["id"])
                    
        except KeyError:
            self.logger.warn(
                "Received message with action: %s, not enough data provided to perform action." % data["action"])

    

    def assign_job_to_drone(self, drone_id):
        if len(self.jobs) != 0 and drone_id not in self.active_drones:
            job_id = list(self.jobs.keys()).pop(0)

            job = self.jobs[job_id]
            job["action"] = "no_plan_job"
            job["drone_id"]= drone_id
            job["job_id"] = job_id     
            self.mqtt.publish(self.base_mqtt_topic + "/" + str(drone_id), json.dumps(job), qos=2)
            self.logger.info("Deploying job to drone [id]: %d, [job_id] %d" % (drone_id, job_id))
            self.active_jobs[drone_id] = self.jobs[job_id]
            self.active_drones.append(drone_id)
            del self.jobs[job_id]
            self.db.set_job_active(job_id, drone_id)

    def job_complete(self, drone_id):
        if int(drone_id) in self.active_drones:
            self.logger.info("Drone with id: %d COMPLETED its job" % (int(drone_id)))
            job = self.active_jobs[int(drone_id)]
            self.remove_job(drone_id)
            # INFORM BACKBONE
            url = self.backbone_url + "/jobs/complete/" + str(job["job_id"])
            try:
                requests.post(url, timeout=2)
            except:
                self.logger.warn("Job status complete send to backbone failed")

    def job_failed(self, drone_id, reason):
        """ When job fails, job is redeployed 3 times. After 3 consecutive faillures, job gets removed and backend is informed."""
        if int(drone_id) in self.active_jobs:
            self.active_drones.remove(int(drone_id))
            job = self.active_jobs[int(drone_id)]
            job_id = job["job_id"]
            del self.active_jobs[int(drone_id)]

            try: fail_count = job["attempts"]
            except: fail_count = 0
            fail_count += 1
            self.logger.info("Drone with id: %d FAILED its job, attempt: %d" % (int(drone_id), fail_count))
            # Add job back in queue if less than 3 attempts are performed
            if fail_count >= 3:
                self.logger.info("Dropping job with id: %d because job exceeded attempt limit (3)." % int(job_id))
                self.db.remove_job(job["job_id"])
                #inform backbone if job has failed
                url = self.backbone_url + "/jobs/failed"
                content = {"jobId" : str(job["job_id"]),
                            "droneId": str(drone_id),
                            "reason": str(reason)
                            }
                try:
                    requests.post(url,json=content, timeout=2)
                except:
                    self.logger.warn("Job status failed send to backbone failed")
            else:
                #redeploy job: 
                job["attempts"] = fail_count
                self.jobs[int(job_id)] = job
                self.db.reset_job(int(job_id))

    def job_in_active_jobs(self, job_id):
        for job in self.active_jobs.values():
            if job["job_id"] == job_id: return True
        return False

    def cancel_job(self, job_id):
        """cancels the job, drone drone lands on next marker"""
        self.logger.info("Job cancel arrived at backend")
        if not self.active_jobs:
            self.logger.info("There are no active jobs to cancel")
            return "There are no active jobs"
        for key in self.active_jobs:
            job = self.active_jobs[int(key)]
            self.logger.info("active jobs: ID: %s, Drone_id: %s" % (job["job_id"], job["drone_id"]))
            if int(job["job_id"]) == int(job_id):
                drone_id = job["drone_id"]
                job["action"] = "cancel"
                job["drone_id"]= drone_id     
                self.mqtt.publish(self.base_mqtt_topic + "/" + str(drone_id), json.dumps(job), qos=2)
                self.logger.info("Drone %d warned to cancel job: %s" % (job["drone_id"],job["job_id"]))
                return "Job succesfully cancelled"
            return "job_id is not an active job"

    def completion_percentage(self, job_id):
        """returns the progress of a specific job (%), based upon path length and drone location"""
        for key in self.active_jobs:
            job = self.active_jobs[int(key)]
            if int(job["job_id"]) == int(job_id):
                drone_id = job["drone_id"]
                location_drone = self.drones[drone_id]
                point1= job["point1"]
                point2= job["point2"]
                markers = {}
                for marker in self.markers:
                    markers[marker] = self.markers[marker].get_dict()
                location1 = self.markers[point1]
                location2 = self.markers[point2]
                #total length of the flight path
                path_length = math.sqrt((location2.x-location1.x)**2 + (location2.y-location1.y)**2)
                #position of drone wrt point1
                drone_position = math.sqrt((location_drone[0]-location1.x)**2 + (location_drone[1]-location1.y)**2)
                completed = (drone_position / path_length)*100
                response = completed
                return response
        return "job_id is not an active job"



        
    
    def find_location(self, id):
        return self.drones[id]

    def set_location(self, id, location):
        if id in self.drones.keys():
            self.drones[id] = location

    def hard_reset(self):
        self.db.remove_all_jobs()
        self.logger.warn("Hard reset triggered!")
        #this will clean all lists that are locally stored
        self.jobs = {}
        self.active_jobs = {}
        self.active_drones = []


    def __del__(self):
        if self.drone_alive_checker:
            self.drone_alive_checker.join()
        self.mqtt.disconnect()
        self.mqtt.loop_stop()


def start_backend(ip, mqtt_topic, backbone_url):
    global backend
    backend = Backend(ip, 8082, mqtt_topic, backbone_url)
    REST.RestApi(backend)
