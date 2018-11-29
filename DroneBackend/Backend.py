
from Mqtt import Mqtt
import json


class Backend:
    """
    this class stores a dictionary with drone_id`s and there location
    a new drone subscribes to the backend and is added to the dictionary

    the backend is able to send a MQTT message to all drones (topic /drones)
    the backend is also able to send (publish) a MQTT message (job to drone) to a specific drone (topic /drone/id)
    all the drones send (on a regular base) a message with there new location

    the backend can also call Flightplanner to convert a job into instructions
    """

    def __init__(self):
        self.mqtt_backend = Mqtt("broker.mqttdashboard.com",1883,"smartcity/drone/backend")
        self.dictionary = {}

        self.mqtt = Mqtt("broker.mqttdashboard.com", 1883, "smartcity/drones")
        self.start_listener_backend()
        self.mqtt.send("backend online")

    def start_listener_backend(self):
        self.mqtt.connect()
        self.mqtt.add_listener_func(self.on_mqtt_message_backend)

    def on_mqtt_message_backend(self,msg):
        """
        recive message from drone, message is a json message
        example
        {"id": 1, "action": add, "location": [1,1,1]}
        :param msg:
        """
        msg = msg.decode("utf-8")
        in_message = json.loads(msg)
        id = in_message['id']
        location = in_message['location']
        action = in_message['action']

        if action == "add":
            self.add_drone(id, location)
        elif action == "remove":
            self.remove_drone(id)
        elif action == "update":
            self.set_location(id,location)
        else:
            message = {
                "id": id,
                "action": "undefined"
            }
            self.mqtt.send_to_drone(id,json.dumps(message))

    def print_dictionary(self):
        print(self.dictionary.items())

    def add_drone(self, id, location):
        """
        check if id exist, if not add to dictionary and send ack message to drone
        else send nack
        :param id: id from drone
        :param location: location from drone
        """
        if id not in self.dictionary:
            self.dictionary[id] = location
            message = {
                "id": id,
                "action": "ack"
            }
            self.mqtt.send_to_drone(id, json.dumps(message))
        else:
            message = {
                "id": id,
                "action": "nack"
            }
            self.mqtt.send_to_drone(id, json.dumps(message))

    def remove_drone(self, id):
        """
        check if id exist, if remove from dictionary and send ack message to drone
        else send nack
        :param id:
        """
        if id in self.dictionary:
            del self.dictionary[id]
            message = {
                "id": id,
                "action": "ack"
            }
            self.mqtt.send_to_drone(id, json.dumps(message))
        else:
            message = {
                "id": id,
                "action": "nack"
            }
            self.mqtt.send_to_drone(id, json.dumps(message))

    def find_location(self, id):
        return self.dictionary[id]

    def set_location(self,id,location):
        if id in self.dictionary:
            self.dictionary[id] = location


if __name__ == "__main__":
    b = Backend()
    b.add_drone(1, (1, 1, 1))
    print(b.find_location(1))
    b.set_location(1,(2,2,2,))
    print(b.find_location(1))

    #TODO replace this
    while True:
        pass


    #TODO add nodes from database
    #TODO make use of flightplanner
    #TODO accept a job from the maas
