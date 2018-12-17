import sys
sys.path.append(sys.path[0]+"/..")          # FIXME: working directory not always the parent directory of DroneCore. ==> modules not found

import errno
import socket, time, json, signal, enum
import DroneCore.CoreLogger as clogger
import Common.FlightPlanner as fp
import paho.mqtt.client as paho
from uuid import getnode as get_mac
import threading
from DroneCore.SharedSocket import SharedSocket
from DroneCore.Exceptions import DroneNotArmedException, CommandNotExectuedException, StateException, AbortException


class DroneStatusEnum(enum.Enum):
    Init=0
    Idle=1
    Armed=2
    Flying=3
    EmergencyLowBattery=4
    EmergencyGamepadLoss=5
    EmergencyGamepadLand=6
    EmergencyGamepadStop=7


class Poller(threading.Thread):

    running = True

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        while self.running:
            controller.send_position_update()
            controller.send_status_update()
            time.sleep(2)

    def join(self, timeout=0):
        self.running = False
        super().join(timeout)


class Controller(threading.Thread):

    running = True
    executing_flight_plan = False
    s_backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_execution = SharedSocket()
    poller = None
    logger = clogger.logger

    id = -1         # id should be received from backend
    mqtt = None
    backend_topic = None
    socket_lock = threading.Lock()

    current_marker_id = 0
    flight_planner = fp.FlightPlanner()
    jobs = [] # job list
    drone_status = ""

    def __init__(self,ip,port):
        super().__init__()
        self.ip = ip
        self.port = port

    def start_controller(self):
        # subscribe to backend
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.s_backend.connect((self.ip, 5001))
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
                self.mqtt.subscribe(data["mqtt_topic"])
                self.mqtt.subscribe(data["mqtt_topic"] + "/" + str(self.id))
                self.mqtt.loop_start()
                self.backend_topic = data["mqtt_topic"] + "/backend"

                self.logger.info("Subscribed to %s MQTT topic." % (data["mqtt_topic"]))
                self.logger.info("Subscribed to %s MQTT topic." % (data["mqtt_topic"] + "/" + str(self.id)))

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
                self.s_execution.connect("127.0.0.1", self.port)
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

        initialze_command = {
            "action": "execute_command",
            "command": "set_position_marker",
            "id": self.current_marker_id
        }
        try: controller.send_command(json.dumps(initialze_command))
        except CommandNotExectuedException: self.logger.warn("Position not initialized correct, initialze command failed.")
        return True # controller successfully started

    def send_command(self, data):
        data = self.s_execution.send_and_receive(data.encode())

        if data == b'NOT_ARMED':
            raise DroneNotArmedException()              # Command failed
        if data == b'ERROR':
            raise CommandNotExectuedException()         # Command failed
        if data == b'STATE_ERROR':
            raise StateException()                      # Command failed
        if data == b'ABORT':
            raise AbortException()                      # Command failed
        # Command executed successfully

    def public_mqtt_callback(self, mosq, obj, msg):
        # possibility to recieve commands from the backend sent to all drones
        pass

    def unique_mqtt_callback(self, mosq, obj, msg):
        try:
            data = json.loads(msg.payload.decode())
            if data["action"] is None:
                self.logger.warn("Received new mqtt message on unique topic, message does not contain an action.")

            if data["action"] == "no_plan_job":
                # add job to the queue
                try:
                    self.logger.info("Received job from marker %d to %d." % (data["point1"], data["point2"]))
                    self.jobs.append(data)
                except KeyError:
                    self.logger.warn("Recieved incomplete job data.")

        except ValueError:
            self.logger.warn("Received new mqtt message on unique topic, message is not in JSON format.")

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
        except ValueError: self.logger.error("Position result was not in the correct format (no JSON).")

    def get_drone_status(self):
        message = {"action": "send_status"}
        try:
            data = json.loads(self.s_execution.send_and_receive(json.dumps(message).encode()).decode())
            return data["status"]
        except: self.logger.warn("Status update failed.")

    def send_status_update(self):
        status = self.get_drone_status()
        res = {
            "id": self.id,
            "action": "status_update",
            "status": status
        }
        self.mqtt.publish(self.backend_topic, json.dumps(res), qos=2)

    def execute_flight_plan(self,plan):
        while len(plan["commands"]) != 0 and self.executing_flight_plan:
            command = plan["commands"].pop(0)
            command["action"] = "execute_command"

            counter = 0
            executed = False

            while not executed and counter < 10:
                try:
                    self.send_command(json.dumps(command))
                    executed = True
                except Exception as e:
                    if type(e) == DroneNotArmedException:
                        self.logger.warn("Drone not armed yet!")
                        counter += 1
                        time.sleep(2)
                    if type(e) == AbortException:
                        self.logger.error("Drone aborted command. Stopping executing job.")
                        self.executing_flight_plan = False
                        raise AbortException()

            if not executed: raise AbortException()
        self.executing_flight_plan = False

    def execute_job(self,job):
        try:
            status = DroneStatusEnum(self.get_drone_status())
            if status == DroneStatusEnum.Flying.value or status == DroneStatusEnum.Armed or status == DroneStatusEnum.Idle:
                if job["action"] == "no_plan_job":
                    self.logger.info("Started job: %d to %d" % (job["point1"], job["point2"]))
                    if self.current_marker_id != job["point2"]:
                        try:
                            if self.current_marker_id != job["point1"]:
                                # first go to point1
                                self.logger.info("Not on point1, flying to point1")
                                plan = self.flight_planner.find_path(self.current_marker_id, job["point1"])
                                string = ""
                                for command in plan["commands"]:
                                    string += "%s" % str(command) + "\n"
                                self.logger.info("Flight plan:\n %s" % string)
                                self.executing_flight_plan = True
                                self.execute_flight_plan(plan)
                                self.current_marker_id = job["point1"]

                            self.logger.info("Flying to point2.")
                            plan = self.flight_planner.find_path(job["point1"], job["point2"])
                            string = ""
                            for command in plan["commands"]:
                                string += "%s" % str(command) + "\n"
                            self.logger.info("Flight plan:\n %s" % string)
                            self.executing_flight_plan = True
                            self.execute_flight_plan(plan)
                            self.current_marker_id = job["point2"]
                        except:
                            self.logger.error("Job execution aborted.")
                            self.jobs.append(job)
                    else:
                        self.logger.info("Already at point2.")
                else:
                    self.logger.info("Drone not able to perform job at this time (status).")
                    self.jobs.append(job)
        except KeyError:
            self.logger.warn("Job failed, not engough information.")

    def run(self):
        try:
            # Polling loop, sleep 1 s each time
            while self.running:
                if len(self.jobs) is not 0:
                    # get the first job
                    job = self.jobs.pop(0)
                    self.execute_job(job)
                time.sleep(0.1)
        except Exception:
            exit(0, 0)

    def close(self):
        self.running = False
        if self.mqtt:
            self.mqtt.disconnect()
            self.mqtt.loop_stop()
        self.s_backend.close()
        self.s_execution.close()
        if self.poller:
            if self.poller.isAlive():
                self.poller.join()


def exit(signal, frame):
    print("Controller closed.")
    global controller
    controller.close()
    controller.join()
    try:
        sys.exit(0)
    except: pass


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    controller = Controller(sys.argv[3], int(sys.argv[1]))
    controller.current_marker_id = int(sys.argv[2])
    if not controller.start_controller():
        exit(0,0)

    controller.start()
