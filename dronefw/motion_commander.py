
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
The MotionCommander is used to make it easy to write scripts that moves the
Crazyflie around. Some sort of positioning support is required, for instance
the Flow deck.

The API contains a set of primitives that are easy to understand and use, such
as "go forward" or "turn around".

There are two flavors of primitives, one that is blocking and returns when
a motion is completed, while the other starts a motion and returns immediately.
In the second variation the user has to stop or change the motion when
appropriate by issuing new commands.

The MotionCommander can be used as context manager using the with keyword. In
this mode of operation takeoff and landing is executed when the context is
created/closed.
"""
import math
import sys
import time
from threading import Thread

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
import drone
import settings

if sys.version_info < (3,):
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty


class MotionCommander:
    """The motion commander"""
    VELOCITY = 0.2
    RATE = 360.0 / 5

    def __init__(self, crazyflie, Drone,default_height=0.3,MaxHeight=1.5):
        """
        Construct an instance of a MotionCommander

        :param crazyflie: a Crazyflie or SyncCrazyflie instance
        :param default_height: the default height to fly at
        """
        if isinstance(crazyflie, SyncCrazyflie):
            self._cf = crazyflie.cf
        else:
            self._cf = crazyflie

        self.default_height = default_height

        self._is_flying = False
        self._thread = None
        self.Drone=Drone
        self.DoNotInterrupt=0

    # Distance based primitives

    def TakeOff(self, height=None, velocity=VELOCITY):
        """
        Takes off, that is starts the motors, goes straigt up and hovers.
        Do not call this function if you use the with keyword. Take off is
        done automatically when the context is created.

        :param height: the height (meters) to hover at. None uses the default
                       height set when constructed.
        :param velocity: the velocity (meters/second) when taking off
        :return:
        """
        if self._is_flying:
            raise Exception('Already flying')
        if not self._cf.is_connected():
            raise Exception('Crazyflie is not connected')

        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        self.DoNotInterrupt = 0
        self._is_flying = True
        self._reset_position_estimator()

        if height is None:
            height = self.default_height

        self._cf.commander.send_setpoint(0, 0, 0, 0);

        #Spool up motors preflight
        for a in range(settings.SpoolUpTime):
            self._cf.commander.send_setpoint(0, 0, 0, 15000);
            time.sleep(0.1);

        self._thread = _SetPointThread(self._cf,height)

        for a in range(10):
            self._cf.commander.send_zdistance_setpoint(0,0,0,height)
            time.sleep(0.1)

        self._thread.start()

        self.stop()
        self.Drone.DroneStatus=drone.DroneStatusEnum.Flying

    def EmergencyStop(self):
        self.DoNotInterrupt = 1
        if (self._thread != None):
            self._thread.stop()
            self._thread = None
        self._cf.commander.send_setpoint(0, 0, 0, 0);
        self._cf.param.set_value('safety.estop', '1')
        self._is_flying=0

    def land(self, velocity=VELOCITY,DoNotExcept=False):
        if (self.DoNotInterrupt==1):
            if (DoNotExcept==False):
                raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return

        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        self.DoNotInterrupt=1
        if self._is_flying:
            self.Down(self._thread.get_height() + 0.4, velocity, priority=1)

            self._thread.stop()
            self._thread = None

            self._cf.commander.send_stop_setpoint()
            self._cf.param.set_value('safety.estop', '1')
            self._is_flying = False
            if (self.Drone.DroneStatus==drone.DroneStatusEnum.Flying):
                self.Drone.DroneStatus=drone.DroneStatusEnum.Idle

    def close(self):
        self._thread.stop()
        self._thread = None

        self._cf.commander.send_stop_setpoint()
        self._is_flying = False


    def Left(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go left

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """
        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(0.0, distance_m, 0.0, velocity)

    def Right(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go right

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """

        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(0.0, -distance_m, 0.0, velocity)

    def Forward(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go forward

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """

        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(distance_m, 0.0, 0.0, velocity)

    def Back(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go backwards

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """

        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(-distance_m, 0.0, 0.0, velocity)

    def Up(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go up

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """


        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(0.0, 0.0, distance_m, velocity)

    def Down(self, distance_m, velocity=VELOCITY, priority=0):
        """
        Go down

        :param distance_m: the distance to travel (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """
        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.MoveDistance(0.0, 0.0, -distance_m, velocity, priority=priority)

    def TurnLeft(self, angle_degrees, rate=RATE, priority=0):
        """
        Turn to the left, staying on the spot

        :param angle_degrees: How far to turn (degrees)
        :param rate: The trurning speed (degrees/second)
        :return:
        """
        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        flight_time = angle_degrees / rate

        self.start_turn_left(rate)
        time.sleep(flight_time)
        self.stop()

    def TurnRight(self, angle_degrees, rate=RATE, priority=0):
        """
        Turn to the right, staying on the spot

        :param angle_degrees: How far to turn (degrees)
        :param rate: The trurning speed (degrees/second)
        :return:
        """
        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        flight_time = angle_degrees / rate

        self.start_turn_right(rate)
        time.sleep(flight_time)
        self.stop()

    def circle_left(self, radius_m, velocity=VELOCITY, angle_degrees=360.0, priority=0):
        """
        Go in circle, counter clock wise

        :param radius_m: The radius of the circle (meters)
        :param velocity: The velocity along the circle (meters/second)
        :param angle_degrees: How far to go in the circle (degrees)
        :return:
        """

        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        distance = 2 * radius_m * math.pi * angle_degrees / 360.0
        flight_time = distance / velocity

        self.start_circle_left(radius_m, velocity)
        time.sleep(flight_time)
        self.stop()

    def circle_right(self, radius_m, velocity=VELOCITY, angle_degrees=360.0, priority=0):
        """
        Go in circle, clock wise

        :param radius_m: The radius of the circle (meters)
        :param velocity: The velocity along the circle (meters/second)
        :param angle_degrees: How far to go in the circle (degrees)
        :return:
        """

        #Clip velocity
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        distance = 2 * radius_m * math.pi * angle_degrees / 360.0
        flight_time = distance / velocity

        self.start_circle_right(radius_m, velocity)
        time.sleep(flight_time)
        self.stop()

    def MoveDistance(self, distance_x_m, distance_y_m, distance_z_m,
                     velocity=VELOCITY, priority=0):
        """
        Move in a straight line.
        positive X is forward
        positive Y is left
        positive Z is up

        :param distance_x_m: The distance to travel along the X-axis (meters)
        :param distance_y_m: The distance to travel along the Y-axis (meters)
        :param distance_z_m: The distance to travel along the Z-axis (meters)
        :param velocity: the velocity of the motion (meters/second)
        :return:
        """
        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        distance = math.sqrt(distance_x_m * distance_x_m +
                             distance_y_m * distance_y_m +
                             distance_z_m * distance_z_m)
        flight_time = distance / velocity* settings.TravelDistAdj

        velocity_x = velocity * distance_x_m / distance
        velocity_y = velocity * distance_y_m / distance
        velocity_z = velocity * distance_z_m / distance

        #Clip velocity
        if (velocity_z>settings.MaxZVel):
            velocity_z=settings.MaxZVel
        if (velocity_x>settings.MaxXYVel):
            velocity_x=settings.MaxXYVel
        if (velocity_y>settings.MaxXYVel):
            velocity_y=settings.MaxXYVel

        self.start_linear_motion(velocity_x, velocity_y, velocity_z,priority=priority)
        time.sleep(flight_time)
        self.stop(priority=priority)

    # Velocity based primitives

    def start_left(self, velocity=VELOCITY, priority=0):
        """
        Start moving left. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """

        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(0.0, velocity, 0.0)

    def start_right(self, velocity=VELOCITY, priority=0):
        """
        Start moving right. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """

        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(0.0, -velocity, 0.0)

    def start_forward(self, velocity=VELOCITY, priority=0):
        """
        Start moving forward. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """
        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(velocity, 0.0, 0.0)

    def start_back(self, velocity=VELOCITY, priority=0):
        """
        Start moving backwards. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """

        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(-velocity, 0.0, 0.0)

    def start_up(self, velocity=VELOCITY, priority=0):
        """
        Start moving up. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """
        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(0.0, 0.0, velocity)

    def start_down(self, velocity=VELOCITY, priority=0):
        """
        Start moving down. This function returns immediately.

        :param velocity: The velocity of the motion (meters/second)
        :return:
        """
        #Clip velocity
        if (velocity>settings.MaxZVel):
            velocity=settings.MaxZVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self.start_linear_motion(0.0, 0.0, -velocity)

    def stop(self, priority=0):
        """
        Stop any motion and hover.

        :return:
        """
        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self._set_vel_setpoint(0.0, 0.0, 0.0, 0.0)

    def start_turn_left(self, rate=RATE, priority=0):
        """
        Start turning left. This function returns immediately.

        :param rate: The angular rate (degrees/second)
        :return:
        """

        #Limit yaw rate
        if (rate>settings.MaxYawRate):
            rate=settings.MaxYawRate

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self._set_vel_setpoint(0.0, 0.0, 0.0, -rate)

    def start_turn_right(self, rate=RATE, priority=0):
        """
        Start turning right. This function returns immediately.

        :param rate: The angular rate (degrees/second)
        :return:
        """

        #Limit yaw rate
        if (rate>settings.MaxYawRate):
            rate=settings.MaxYawRate

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self._set_vel_setpoint(0.0, 0.0, 0.0, rate)

    def start_circle_left(self, radius_m, velocity=VELOCITY, priority=0):
        """
        Start a circular motion to the left. This function returns immediately.

        :param radius_m: The radius of the circle (meters)
        :param velocity: The velocity of the motion (meters/second)
        :return:
        """

        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        circumference = 2 * radius_m * math.pi
        rate = 360.0 * velocity / circumference

        self._set_vel_setpoint(velocity, 0.0, 0.0, -rate)

    def start_circle_right(self, radius_m, velocity=VELOCITY, priority=0):
        """
        Start a circular motion to the right. This function returns immediately

        :param radius_m: The radius of the circle (meters)
        :param velocity: The velocity of the motion (meters/second)
        :return:
        """

        if (velocity>settings.MaxXYVel):
            velocity=settings.MaxXYVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        circumference = 2 * radius_m * math.pi
        rate = 360.0 * velocity / circumference

        self._set_vel_setpoint(velocity, 0.0, 0.0, rate)

    def start_linear_motion(self, velocity_x_m, velocity_y_m, velocity_z_m, priority=0):
        """
        Start a linear motion. This function returns immediately.

        positive X is forward
        positive Y is left
        positive Z is up

        :param velocity_x_m: The velocity along the X-axis (meters/second)
        :param velocity_y_m: The velocity along the Y-axis (meters/second)
        :param velocity_z_m: The velocity along the Z-axis (meters/second)
        :return:
        """
        #Clip velocity
        if (velocity_x_m>settings.MaxXYVel):
            velocity_x_m=settings.MaxXYVel
        if (velocity_y_m>settings.MaxXYVel):
            velocity_y_m=settings.MaxXYVel
        if (velocity_z_m>settings.MaxZVel):
            velocity_z_m=settings.MaxZVel

        if (self.DoNotInterrupt==1 and priority==0):
            raise Exception ("Cannot execute motion; DoNotInterrupt override active.")
            return
        self._set_vel_setpoint(
            velocity_x_m, velocity_y_m, velocity_z_m, 0.0)

    def _set_vel_setpoint(self, velocity_x, velocity_y, velocity_z, rate_yaw):
        if not self._is_flying:
            raise Exception('Can not move on the ground. Take off first!')

        self._thread.set_vel_setpoint(
            velocity_x, velocity_y, velocity_z, rate_yaw)

    def _reset_position_estimator(self):
        self._cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        self._cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)


class _SetPointThread(Thread):
    TERMINATE_EVENT = 'terminate'
    UPDATE_PERIOD = 0.05
    ABS_Z_INDEX = 3

    def __init__(self, cf, startheight,update_period=UPDATE_PERIOD):
        Thread.__init__(self)
        self.update_period = update_period

        self._queue = Queue()
        self._cf = cf

        self._hover_setpoint = [0.0, 0.0, 0.0, startheight]

        self._z_base = startheight
        self._z_velocity = 0.0
        self._z_base_time = 0.0

    def stop(self):
        """
        Stop the thread and wait for it to terminate

        :return:
        """
        self._queue.put(self.TERMINATE_EVENT)
        self.join()

    def set_vel_setpoint(self, velocity_x, velocity_y, velocity_z, rate_yaw):
        """Set the velocity setpoint to use for the future motion"""
        self._queue.put((velocity_x, velocity_y, velocity_z, rate_yaw))

    def get_height(self):
        """
        Get the current height of the Crazyflie.

        :return: The height (meters)
        """
        return self._hover_setpoint[self.ABS_Z_INDEX]
    def set_height(self,height):

        self._hover_setpoint[self.ABS_Z_INDEX]=height

    def run(self):
        while True:
            try:
                event = self._queue.get(block=True, timeout=self.update_period)
                if event == self.TERMINATE_EVENT:
                    return

                self._new_setpoint(*event)
            except Empty:
                pass
            if (self.get_height()>settings.MaxHeight and self._z_velocity>0):
                self._new_setpoint(self._hover_setpoint[0],self._hover_setpoint[1],0,self._hover_setpoint[2]) #Height hold at max
            elif (self.get_height()<0.0 and self._z_velocity<0):
                self._new_setpoint(self._hover_setpoint[0],self._hover_setpoint[1],0,self._hover_setpoint[2]) #Height below 0 is invalid
            self._update_z_in_setpoint()
            self._cf.commander.send_hover_setpoint(*self._hover_setpoint)

    def _new_setpoint(self, velocity_x, velocity_y, velocity_z, rate_yaw):
        self._z_base = self._current_z()
        self._z_velocity = velocity_z
        self._z_base_time = time.time()

        self._hover_setpoint = [velocity_x, velocity_y, rate_yaw, self._z_base]

    def _update_z_in_setpoint(self):
        self._hover_setpoint[self.ABS_Z_INDEX] = self._current_z()


    def _current_z(self):
        now = time.time()
        return self._z_base + self._z_velocity * (now - self._z_base_time)
