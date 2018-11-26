
from Mqtt import Mqtt

class Backend:
    """
    this class stores a dictionary with drone_id`s and there location
    a new drone subscribes to the backend and is added to the dictionary

    the backend is able to send a MQTT message to all drones (topic \drone)
    the backend is also able to send a MQTT message (job to drone) to a specific drone (topic \drone\id)
    all the drones send (on a regular base) a message with there new location

    the backend can also call Flightplanner to convert a job into instructions
    """

    def __init__(self):
        self.mqtt_backend = Mqtt("broker.mqttdashboard.com",1883,"smartcity/drone/backend")
        self.dictionary = {}
        self.start_listener_backend()
        self.mqtt_backend.send("backend online")

    # Connecteer met Mqtt Host
    def start_listener_backend(self):
        self.mqtt_backend.connect()
        self.mqtt_backend.add_listener_func(self.on_mqtt_message_backend)

    def on_mqtt_message_backend(self,msg):
        print(msg)

    def print_dictionary(self):
        print(self.dictionary.items())

    def add_drone(self, id, location):
        if id not in self.dictionary:
            self.dictionary[id] = location
        else:
            print("id already used")

    def remove_drone(self, id):
        if id in self.dictionary:
            del self.dictionary[id]
        else:
            print("id does not exist")

    def find_location(self, id):
        return self.dictionary[id]

    def set_location(self,id,location):
        if id in self.dictionary:
            self.dictionary[id] = location
        else:
            print("id does not exist")


if __name__ == "__main__":
    b = Backend()
    b.add_drone(1, (1, 1, 1))
    print(b.find_location(1))
    b.set_location(1,(2,2,2,))
    print(b.find_location(1))
    counter = 0
    while True:
        counter += 1


