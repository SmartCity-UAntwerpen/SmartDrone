
import paho.mqtt.client as mqttclient


class Mqtt:
    listeners = []

    def __init__(self, host, port,topic="smartcity/drone", client_id="iotSmartCityDrone"):
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqttclient.Client(client_id)

    def add_listener_func(self, func):
        self.listeners.append(func)

    def notify_listeners(self, message):
        for func in self.listeners:
            func(message)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
        print("Connected with " + self.host)

    def on_message(self, client, userdata, msg):
        self.notify_listeners(msg.payload)

    def publish(self, topic, message, callback=None):
        if callback != None:
            self.on_publish = callback
        self.client.publish(topic, message)

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def send(self,message):
        self.publish(self.topic, message)

    def send_to_drone(self,id,message):
        topic = "smartcity/drones/" + str(id)
        self.publish(topic, message)

