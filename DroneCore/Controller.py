import sys
sys.path.append(sys.path[0]+"/..")          # FIXME: working directory not always the parent directory of DroneCore. ==> modules not found

import errno
import socket, time, json, signal, enum ,requests
import DroneCore.CoreLogger as clogger
import Common.FlightPlanner as fp
import paho.mqtt.client as paho
from uuid import getnode as get_mac
import threading
from DroneCore.Exceptions import DroneNotArmedException, CommandNotExectuedException, StateException, AbortException, JustArmedException, NoPathFoundException

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
    cancel_received = False
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    poller = None
    logger = clogger.logger

    id = -1         # id should be received from backend
    mqtt = None
    backend_topic = None

    current_marker_id = 0
    flight_planner = fp.FlightPlanner()
    jobs = [] # job list
    drone_status = ""

    def __init__(self,ip,port):
        super().__init__()
        self.ip = ip
        self.port = port

    def start_controller(self):
        self.logger.info("Start controller.")
        # subscribe to backend
        try:
            mac = get_mac()
            url = "http://" + self.ip + ":8082/addDrone/" + str(mac + self.port)

            data = json.loads(requests.get(url).text)
            self.id = data["id"]
            self.mqtt = paho.Client()
            self.mqtt.message_callback_add(data["mqtt_topic"] + "/" + str(self.id), self.unique_mqtt_callback)
            self.mqtt.message_callback_add(data["mqtt_topic"], self.public_mqtt_callback)
            self.mqtt.username_pw_set(data["mqtt_username"], data["mqtt_password"])
            self.mqtt.connect(data["mqtt_broker"], data["mqtt_port"], 60)
            self.mqtt.subscribe(data["mqtt_topic"])
            self.mqtt.subscribe(data["mqtt_topic"] + "/" + str(self.id))
            self.mqtt.loop_start()
            self.backend_topic = data["mqtt_topic"] + "/backend"

            self.logger.info("Subscribed to %s MQTT topic." % (data["mqtt_topic"]))
            self.logger.info("Subscribed to %s MQTT topic." % (data["mqtt_topic"] + "/" + str(self.id)))
            self.logger.info("Succesfully subscribed to the backend. Recieved id: %d" % self.id)

            # succesfully subscribed to backend, update markers
            url = "http://" + self.ip + ":8082/getMarkers/"
            markers = json.loads(requests.get(url).text)
            self.flight_planner.update_markers(markers["markers"])
            self.logger.info("Received markers form %s" % url)
            self.logger.info("Markers updated.")
        except Exception as e:
            self.logger.error("Connection with backend failed.")
            return False

        # connect with execution process
        connected = False
        counter = 0
        while not connected and counter < 10:
            try:
                self.status_socket.connect(("127.0.0.1", self.port + 1))
                self.command_socket.connect(("127.0.0.1", self.port))
                connected = True

                markers["action"] = "marker_update"
                self.status_socket.send(json.dumps(markers).encode())

                self.logger.info("Connection with exectution process established.")
            except socket.error as error:
                if error.errno == errno.ECONNREFUSED:
                    self.logger.warn("Connection to exectution process refused. Retrying...")
                    counter += 1
                    time.sleep(2)
                else:
                    self.logger.exception(error)
                    break

        if not connected:
            self.logger.error("Connection with execution process not established. Shutting down.")
            return False

        self.poller = Poller(self)
        self.poller.start()

        initialze_command = {
            "action": "execute_command",
            "command": "set_position_marker",
            "id": self.current_marker_id
        }
        try: controller.send_command(json.dumps(initialze_command))
        except CommandNotExectuedException:
            self.logger.warn("Position not initialized correct, initialze command failed.")
        self.start()
        return True # controller successfully started

    def send_command(self, command):
        """ Send the command, which should be a json format (python dictionary) with the appropriate parameters. """
        self.logger.log(15,"send_command %s", command)
        self.command_socket.send(command.encode())
        data = self.command_socket.recv(2048)
        self.logger.log(15,"Received data %s", data.decode())

        if data == b'NOT_ARMED':
            self.logger.info("Drone not armed, waiting for arm...")
            data = self.command_socket.recv(2048)
            self.logger.log(15, "Received data %s", data.decode())
            if data == b'ACK':
                raise JustArmedException()              # Command failed
            else: raise AbortException()
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
        """ Unique mqtt callback (base_topic/id), msg should be json with at least the field action.
            Jobs are accepted here."""
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
                    self.logger.warn("Received incomplete job data.")

            if data["action"] == "cancel":
                self.logger.warn("job cancel arrived!")
                self.cancel_received = True



        except ValueError:
            self.logger.warn("Received new mqtt message on unique topic, message is not in JSON format.")

    def send_position_update(self):
        message = { "action": "send_position" }
        self.status_socket.send(json.dumps(message).encode())
        data = self.status_socket.recv(2048)
        try:
            data = json.loads(data.decode())
            res = {
                "id": self.id,
                "action": "position_update",
                "position": data["position"]
            }
            self.logger.log(15, "%s", res)
            self.mqtt.publish(self.backend_topic, json.dumps(res), qos=2)
        except ValueError: self.logger.error("Position result was not in the correct format (no JSON).")

    def get_drone_status(self):
        message = {"action": "send_status"}
        try:
            self.status_socket.send(json.dumps(message).encode())
            data = self.status_socket.recv(2048)
            data = json.loads(data.decode())
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
        while len(plan["commands"]) != 0 and self.executing_flight_plan and not self.cancel_received:
            command = plan["commands"].pop(0)
            command["action"] = "execute_command"

            counter = 0
            executed = False

            while not executed and counter < 10:
                try:
                    self.send_command(json.dumps(command))
                    executed = True
                except Exception as e:
                    counter += 1
                    if type(e) == AbortException:
                        self.logger.error("Drone aborted command. Stopping executing job.")
                        self.executing_flight_plan = False
                        raise AbortException()
                    if type(e) == DroneNotArmedException:
                        self.logger.error("Drone not armed. Retrying %d..." % counter)
                    if type(e) == CommandNotExectuedException:
                        self.logger.error("Command not executed. Retrying %d..." % counter)
                    if type(e) == StateException:
                        self.logger.error("Command not executed. Wrong state. Retrying %d..." % counter)
                    if type(e) == JustArmedException:
                        self.logger.info("Drone just armed.")

            if not executed:
                self.logger.error("Command not executed.")
                raise AbortException()
        self.executing_flight_plan = False
        if self.cancel_received:
            self.cancel_received = False
            self.logger.info("CANCEL HANDLED IN FLIGHT PLAN")
            command["action"] = "execute_command"
            command["command"] = "land"
            self.send_command(json.dumps(command))

    def fly_from_to(self, point1, point2):
        plan = self.flight_planner.find_path(point1, point2)
        if plan is None:
            self.logger.warn("No path from point %d to %d" % (point1, point2))
            raise NoPathFoundException()    

        self.logger.info("Flying from %d to %d." % (point1, point2))
        string = ""
        for command in plan["commands"]:
            string += "%s" % str(command) + "\n"
        self.logger.info("Flight plan:\n%s" % string)
        self.executing_flight_plan = True
        self.execute_flight_plan(plan)
        self.current_marker_id = point2

    def execute_job(self, job):
        try:
            if job["action"] == "no_plan_job":
                self.logger.info("Started job: %d to %d" % (job["point1"], job["point2"]))
                try:
                    if self.current_marker_id != job["point1"]:
                        # first go to point1
                        self.logger.info("Not on %d, flying to pick up location %d" % (job["point1"],job["point1"]))
                        self.fly_from_to(self.current_marker_id, job["point1"])

                    self.fly_from_to(job["point1"], job["point2"])
                except Exception as e:
                    if type(e) == AbortException:
                        message = {"action": "job_failed", "id": self.id, "reason": "abortException_during_execution"}
                        self.mqtt.publish(self.backend_topic, json.dumps(message), qos=2)
                        self.logger.info("Job was aborted, backend informed: abortException during execution.")

                        message = {"action": "wait_for_idle"}
                        self.command_socket.send(json.dumps(message).encode())          # use command socket, because status socket is used by thread
                        data = json.loads(self.command_socket.recv(2048).decode())
                        if data["result"] == "false":
                            message = {"action": "shutdown"}
                            self.command_socket.send(json.dumps(message).encode())
                            exit(0,0)
                        else:
                            # drone back in idle state, add job back in job queue
                            # IMPORTANT NOTE: when idle here, the drone should be placed back on its start marker
                            self.logger.info("Job was aborted, but drone is reset and back in idle.")
                        return False
                    elif type(e) == NoPathFoundException:
                        message = {"action": "job_failed", "id": self.id, "reason": "No_path_found"}
                        self.mqtt.publish(self.backend_topic, json.dumps(message), qos=2)
                        self.logger.info("Job was aborted, backend informed: NoPathFoundException.")

                        message = {"action": "wait_for_idle"}
                        self.command_socket.send(json.dumps(message).encode())          # use command socket, because status socket is used by thread
                        data = json.loads(self.command_socket.recv(2048).decode())
                        if data["result"] == "false":
                            message = {"action": "shutdown"}
                            self.command_socket.send(json.dumps(message).encode())
                            exit(0,0)
                        else:
                            # drone back in idle state, add job back in job queue
                            # IMPORTANT NOTE: when idle here, the drone should be placed back on its start marker
                            self.logger.info("Job was aborted, but drone is reset and back in idle.")
                        return False
                    else:
                        self.logger.warn("Job failed.")
                        self.logger.warn(e)
                        return False
                # plan job could be added here, instead of calling fly_from_to(), exectute_plan() could be used.
        except KeyError:
            self.logger.warn("Job failed, not engough information.")
            return False
        return True

    def run(self):
        try:
            # Polling loop, sleep 1 s each time
            while self.running:
                if len(self.jobs) is not 0:
                    # get the first job
                    job = self.jobs.pop(0)
                    if self.execute_job(job):
                        message = {
                            "action": "job_complete",
                            "id": self.id,
                        }
                        self.mqtt.publish(self.backend_topic, json.dumps(message), qos=2)
                time.sleep(0.1)
        except Exception as e:
            self.logger.exception(e)
            exit(0, 0)

    def close(self):
        url = "http://" + self.ip + ":8082/removeDrone/" + str(self.id)
        try:
            data = json.loads(requests.get(url).text)
            if data["result"] != "true": self.logger.warn("Drone not correctly removed from backend.")
        except: self.logger.warn("Drone lost connection with backend, not removed from backend.")
        self.logger.info("Closing controller.")
        self.running = False
        if self.mqtt:
            self.mqtt.disconnect()
            self.mqtt.loop_stop()
        self.command_socket.close()
        self.status_socket.close()
        if self.poller:
            if self.poller.isAlive():
                self.poller.join()


def exit(signal, frame):
    global controller
    controller.close()
    print("Controller closed.")
    if controller.isAlive():
        controller.join()
    try:
        sys.exit(0)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("STARTUP: Starting controller")
    signal.signal(signal.SIGINT, exit)
    controller = Controller(sys.argv[3], int(sys.argv[1]))
    controller.current_marker_id = int(sys.argv[2])
    if not controller.start_controller():
        exit(0,0)

    while controller.running:
        time.sleep(1)
