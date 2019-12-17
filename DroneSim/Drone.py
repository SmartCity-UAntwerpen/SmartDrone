import enum, math, time
import numpy as np
import BlackBox

MAX_VELOCITY = 0.5
VELOCITY = 0.5
DEFAULT_HEIGHT = 0.5
RATE = 360.0 / 5


class DroneStatusEnum(enum.Enum):
    Init = 0
    Idle = 1
    Armed = 2
    Flying = 3
    EmergencyLowBattery = 4
    EmergencyGamepadLoss = 5
    EmergencyGamepadLand = 6
    EmergencyGamepadStop = 7


class Drone:
    """
    Simulated drone class, simulates the drone actions
    :ivar x, y, z: position of the drone, updated after each command (see moveDistance function)
    :ivar pitch, yaw, roll: rotations of the drone
    :ivar flying, bool: True means the drone flying
    :ivar status, drone status enum (see DroneStatusEnum class for possible statusses)
    :ivar black_box: 'black box' of the aircraft, logs every action of the drone
    """
    x, y, z = 0, 0, 0
    pitch, yaw, roll = 0, 0, 0
    deviation= [0,0,0,0]
    flying = False
    status = DroneStatusEnum.Idle  # or init? no real initialization in simulation
    black_box = BlackBox.create_black_box()

    def is_armed(self):
        return self.status == DroneStatusEnum.Armed

    def is_flying(self):
        return self.status == DroneStatusEnum.Flying

    def is_idle(self):
        return self.status == DroneStatusEnum.Idle

    def arm(self):
        self.status = DroneStatusEnum.Armed
        self.black_box.info("Drone armed.")

    def disarm(self):
        self.status = DroneStatusEnum.Idle
        self.black_box.info("Drone disarmed.")

    def takeOff(self, height=DEFAULT_HEIGHT, velocity=VELOCITY):
        if self.status == DroneStatusEnum.Armed:
            self.status = DroneStatusEnum.Flying
            self.black_box.info("Taking off to %0.2f m" % height)
            self.moveDistance(0, 0, height, velocity)
        else:
            self.black_box.warn("Drone not armed! Arm drone before takeoff.")

    def land(self):
        self.black_box.info("Drone landing.")
        self.moveDistance(0, 0, -self.z, velocity=0.2, deviation_sigma=0.02)
        self.black_box.info("Drone landed at: (%.2f %.2f %.2f)." % (self.x, self.y, self.z))
        self.status = DroneStatusEnum.Idle

    def guided_land(self, velocity, x, y):
        self.black_box.info("Drone landing (guided).")
        self.center(x, y)
        self.moveDistance(0, 0, -self.z, velocity=velocity, deviation_sigma=0)
        self.black_box.info("Drone landed at: (%.2f %.2f %.2f)." % (self.x, self.y, self.z))
        self.status = DroneStatusEnum.Idle

    def forward(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving forwards by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(distance, 0, 0, velocity)
        

    def backward(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving backwards by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(-distance, 0, 0, velocity)
        


    def left(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving left by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(0, distance, 0, velocity)

    def right(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving right by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(0, -distance, 0, velocity)

    def up(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving up by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(0, 0, distance, velocity)

    def down(self, distance=None, velocity=VELOCITY):
        if distance is None or distance < 0:
            self.black_box.warn("Specify the (positive) distance to move.")
            return

        self.black_box.info("Moving down by %0.2f m." % distance)
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY

        self.moveDistance(0, 0, -distance, velocity)

    def turnLeft(self, angle_degrees=None, rate=RATE):
        if angle_degrees is None:
            self.black_box.warn("Specify the angle to turn.")
            return

        self.black_box.info("Turning left by %0.2f degree." % angle_degrees)
        flight_time = angle_degrees / rate
        self.black_box.info("ALERT: YAW voor rotation: %f" %self.yaw)
        self.yaw += angle_degrees * math.pi / 180
        # move the drone, turning the drone is not perfect and moves the drone
        self.x += np.random.normal(0, 0.2)
        self.y += np.random.normal(0, 0.2)
        self.black_box.info("ALERT: YAW na rotation: %f" %self.yaw)
        time.sleep(flight_time)

    def turnRight(self, angle_degrees=None, rate=RATE):
        if angle_degrees is None:
            self.black_box.warn("Specify the angle to turn.")
            return

        self.black_box.info("Turning right by %0.2f degree." % angle_degrees)
        flight_time = angle_degrees / rate
        self.yaw -= angle_degrees * math.pi / 180
        # move the drone, turning the drone is not perfect and moves the drone
        self.x += np.random.normal(0, 0.2)
        self.y += np.random.normal(0, 0.2)
        time.sleep(flight_time)

    def DetectArray(self, MarkerId, x,y ):
        """Detects the deviation and returns it as an array
            :param marker id: id of the marker
            :param goal: the coordinates of the marker to which you want to calculate the deviation
        """
        self.black_box.info("Detecting deviation to marker %d" % MarkerId)
        self.black_box.info("DEBUG: deviating position")
        self.x -= 0.05
        self.y += 0.05

        
        fov = 60
        self.deviation[0] = MarkerId
        view_distance = 2 * self.z * math.tan(math.radians(fov / 2))
        if x - view_distance / 2 <= self.x <= x + view_distance / 2 and y - view_distance / 2 <= self.y <= y + view_distance / 2:
            x_dev = float(x - self.x)
            y_dev = float(y - self.y)

            self.black_box.info("--DEBUG-- Flight correction ! NO ! YAW, x: %f, y: %f, yaw: %f" % (x_dev, y_dev, self.yaw))

            self.yaw = 0.1
            #calculate detected path according to rotation. 
            #Note: Drone first rotates back to desired angle before continuing flight.
            x_corr = x_dev*math.cos(self.yaw) + y_dev*math.sin(self.yaw)
            y_corr = x_dev*math.sin(self.yaw) + y_dev*math.cos(self.yaw)
            self.black_box.info("--DEBUG-- Flight correction ! WITH ! YAW, x: %f, y: %f, yaw: %f" % (x_corr, y_corr, self.yaw))
            self.deviation[1] = x_dev  # x deviation
            self.deviation[2] = y_dev # y deviation
            self.deviation[3]= self.yaw 
        else:
            self.black_box.info("Detection failed, no marker found.")
            #return MarkerID value 99: this is error value.
            self.deviation= [99,0,0,0]
   
        return self.deviation
        

    def center(self, x, y):
        # different from the real center function, the dronesimulator will tranlate the marker id to the correct coordinates
        fov = 60
        view_distance = 2 * self.z * math.tan(math.radians(fov / 2))
        if x - view_distance / 2 <= self.x <= x + view_distance / 2 and y - view_distance / 2 <= self.y <= y + view_distance / 2:
            dx = float(x - self.x)
            dy = float(y - self.y)
            self.black_box.info("Centering drone to x: %.2f y: %0.2f" % (x, y))
            self.moveDistance(dx, dy, 0, velocity=0.5, deviation_mean=0,
                              deviation_sigma=0)  # move to the position with 0 randomness
            self.yaw = 0
        else:
            self.black_box.info("Centering failed, no marker found.")

    def moveDistance(self, distance_x_m, distance_y_m, distance_z_m, velocity=0.5, deviation_mean=0,
                     deviation_sigma=0.05):
        """
        Move distance specified by the distance x,y,z parameters [m], the deviation_mean and deviation_simgma control
        the randomness of the movement
        :param distance_x_m: distance to move on x axis in m
        :param distance_y_m: distance to move on y axis in m
        :param distance_z_m: distance to move on z axis in m
        :param velocity: velocity to move with in m/s
        :param deviation_mean: control the randomness of the movement
        :param deviation_sigma: control the randomness of the movement
        :return:
        """
        distance_x_m += np.random.normal(deviation_mean, deviation_sigma)
        distance_y_m += np.random.normal(deviation_mean, deviation_sigma)
        
        distance = math.sqrt(distance_x_m * distance_x_m +
                             distance_y_m * distance_y_m +
                             distance_z_m * distance_z_m)

        if not self.check_before_flight(distance, velocity):
            return

        # velocity += np.random.normal(0,0.1)

        flight_time = distance / velocity

        # rotation
        roll = np.mat(
            [[1, 0, 0], [0, math.cos(self.roll), -math.sin(self.roll)], [0, math.sin(self.roll), math.cos(self.roll)]])
        pitch = np.mat(
            [[math.cos(self.pitch), 0, -math.sin(self.pitch)], [0, 1, 0],
             [math.sin(self.pitch), 0, math.cos(self.pitch)]])
        yaw = np.mat(
            [[math.cos(self.yaw), -math.sin(self.yaw), 0], [math.sin(self.yaw), math.cos(self.yaw), 0], [0, 0, 1]])

        move_vector = np.mat([[distance_x_m], [distance_y_m], [distance_z_m]])
        move_vector = (roll * pitch * yaw) * move_vector

        self.x += move_vector[0]
        self.y += move_vector[1]
        self.z += move_vector[2]
        self.black_box.info("New position: (%.2f, %.2f, %.2f) duration: %.2f s velocity: %.2f m/s"
                             % (self.x, self.y, self.z, flight_time, velocity))
        time.sleep(flight_time)

    def printInfo(self):
        print("Drone: \nPos: (%.2f, %.2f, %.2f) \nAngles: \n\t- pitch: %.2f \n\t- yaw: %.2f \n\t- roll: %.2f"
              % (self.x, self.y, self.z, self.pitch, self.yaw, self.roll))

    def check_before_flight(self, distance, velocity):
        if distance < 0 or velocity < 0:
            self.black_box.error("Distance or velocity is not valid (< 0).")
            return False
        if self.status is not DroneStatusEnum.Flying:
            self.black_box.error("Drone has not taken off yet!")
            return False
        return True

    def setCoordinates(self, x, y, z):
        # set the coordinates of the drone, use this function only when starting
        self.x = x
        self.y = y
        self.z = z
