import pygame
import math
import json
import random
import paho.mqtt.client as paho

from Common.DBConnection import DBConnection

mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883
base_mqtt_topic = "smartcity/drones"


class Visualizer:

    def __init__(self, width, height):
        """
        This class is used to visualize the drone simulator
        At start a pygame window will open. After receiving a MQTT message from smartcity/drones/backend the markers
        will appear in a blue color and the drones will appear in a random color.
        Each drone is represented with a small dot on the window. The previous location of the drone is NOT saved, so
        in this version the user is not able to see the trajectory of the drone.
        :param width: width of the screen
        :param height: height of the screen
        """
        self.width = width
        self.height = height
        self.screen_offset = 10

        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

        self.drones = {}
        self.markers = self.init_markers()

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

        pygame.font.init()
        font = pygame.font.SysFont("monospace", 14)

        label = font.render("Waiting for mqtt message", 1, (255, 255, 0))
        self.screen.blit(label, (self.width / 3, self.height / 2))
        label2 = font.render("on " + base_mqtt_topic + "/backend", 1, (255, 255, 0))
        self.screen.blit(label2,(self.width/3, self.height/2+20))
        pygame.display.update()

    def mqtt_callback(self, mosq, obj, msg):
        """
        This method is called every time when a new mqtt message arrives
        It will set the drones location and update the screen
        :param msg: message
        """
        data = json.loads(msg.payload.decode())
        if data["action"] == "position_update":
            self.drones[int(data["id"])] = data["position"]

        self.update()

    def init_markers(self):
        """
        This method is used to init all the markers.
        First all the markers in the database are stored in a local variable.
        Then the maximum and minimum value for x and y are set. these variables will be used later to determent where to
        draw the markers on the screen
        :return: all the markers
        """
        db = DBConnection()
        # x,y,z,transitpoint
        markers = []
        for m in db.query("select * from point"):
            markers.append(Marker(m[1], m[2], m[3], m[0]))

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

        return markers

    def calculate_screen_location(self, marker):
        """
        This method calculated the location to draw a marker (or drone) on the screen
        first it calculated where (between 0 and 1) it position is relative to the min and max marker (in x and y direction)
        then this value is used to determent the place on the screen.
        afterward a screen_offset value is added or subtracted, thus all the markers will be nicely displayed on the screen
        :param marker: marker with x,y,z, id . only x and y are used
        :return: x and y position on the screen
        """
        distance_x = marker.x - self.min_x
        distance_y = marker.y - self.min_y

        total_distance_x = self.max_x - self.min_x
        total_distance_y = self.max_y - self.min_y

        delta_x = distance_x / total_distance_x
        delta_y = distance_y / total_distance_y

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

        return [pos_x, pos_y]

    def draw_markers(self, markers):
        """
        This function draws (as a blue circle) all the markers on to the screen
        :param markers: array of markers
        """
        for marker in markers:
            [pos_x, pos_y] = self.calculate_screen_location(marker)
            pygame.draw.circle(self.screen, (0, 0, 255), (pos_x, pos_y), 5)

    def quit_event(self):
        """
        This method insures that the game can be closed nicely
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def draw_drones(self):
        """"
        This method draws all the drones onto the screen.
        Each drone gets it own (random) color and is displayed with a circle
        """
        for i in self.drones:
            location = self.drones[i]
            # litte bit misuse of Marker :P
            drone = Marker(location[0], location[1], location[2], i)
            [pos_x, pos_y] = self.calculate_screen_location(drone)
            random.seed(i)
            pygame.draw.circle(self.screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                               (pos_x, pos_y), 5)

    def update(self):
        """
        This method is called from mqtt_callback. It clears the screen and draws the markers and drones.
        """
        self.screen.fill((0, 0, 0))
        self.draw_markers(self.markers)
        self.draw_drones()
        pygame.display.update()


if __name__ == "__main__":
    """
    makes a visualizer and keeps the program running
    """
    from Common.Marker import Marker

    screen = Visualizer(500, 500)

    running = True
    while running:
        # First check events
        running = not screen.quit_event()
