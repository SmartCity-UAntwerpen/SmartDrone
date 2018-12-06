import pygame
import math
import json
import paho.mqtt.client as paho

mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883
base_mqtt_topic = "smartcity/drones"


class Visualizer:

    def __init__(self, width, height):
        self.drones = {}

        self.width = width
        self.height = height
        self.screen_offset = 10

        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

        # Setup MQTT here
        self.base_mqtt_topic = base_mqtt_topic
        self.mqtt = paho.Client()
        self.mqtt.message_callback_add(base_mqtt_topic + "/backend", self.mqtt_callback)
        self.mqtt.connect(mqtt_broker, mqtt_port, 60)
        self.mqtt.subscribe(base_mqtt_topic + "/#")
        self.mqtt.loop_start()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Drone Simulator")
        pygame.display.flip()

    def mqtt_callback(self, mosq, obj, msg):
        print(msg)
        data = json.loads(msg.payload.decode())
        if data["action"] == "position_update":
            self.drones[int(data["id"])] = data["position"]

        self.update();

    def init_markers(self, markers):
        self.markers = markers
        for marker in markers:
            x = marker.x
            y = marker.y
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
            if x < self.min_x:
                self.min_x = x
            if y < self.min_y:
                self.min_y = y

    def get_delta(self, marker):
        distance_x = marker.x - self.min_x
        distance_y = marker.y - self.min_y

        total_distance_x = self.max_x - self.min_x
        total_distance_y = self.max_y - self.min_y

        delta_x = distance_x / total_distance_x
        delta_y = distance_y / total_distance_y

        return [delta_x, delta_y]

    def draw_markers(self, markers):
        for marker in markers:
            [delta_x, delta_y] = self.get_delta(marker)

            pos_x = int(self.width * delta_x)
            pos_y = int(self.height * delta_y)

            if pos_x < 250:
                pos_x += self.screen_offset
            if pos_y < 250:
                pos_y += self.screen_offset

            if pos_x > 250:
                pos_x -= self.screen_offset

            if pos_y > 250:
                pos_y -= self.screen_offset

            pygame.draw.circle(self.screen, (0, 0, 255), (pos_x, pos_y), 5)

    def quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def draw_drones(self):
        for i in self.drones:
            location = self.drones[i]
            x = location[0]
            y = location[1]
            z = location[2]
            m = Marker(x, y, z, i)
            [delta_x, delta_y] = self.get_delta(m)
            pos_x = int(self.width * delta_x)
            pos_y = int(self.height * delta_y)
            pygame.draw.circle(self.screen, (0, 255, 0), (pos_x, pos_y), 5)

    def update(self):
        self.draw_markers(self.markers)
        self.draw_drones()
        pygame.display.update()


if __name__ == "__main__":
    from Common.Marker import Marker

    m0 = Marker(1, 1, 0, 0)
    m1 = Marker(2, 1, 0, 1)
    m2 = Marker(1, 2, 0, 2)
    m3 = Marker(2, 2, 0, 3)
    m4 = Marker(4, 3, 0, 4)
    markers = [m0, m1, m2, m3, m4]

    screen = Visualizer(500, 500)
    screen.init_markers(markers)

    running = True
    while running:
        # First check events
        running = not screen.quit_event()
