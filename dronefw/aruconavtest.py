#!/usr/bin/env python3

from drone import *
from arucolib import *
from aruconav import *


Detector = ArucoClass(0.0792)

#Drone=DroneClass('radio://0/1/2M')
Drone=DroneClass('usb://0')
ArucoNav=ArucoNavClass(Drone,Detector)


# Main autonomous sequence
Drone.mc.TakeOff(0.3, 0.4);
print('Takeoff complete')
Drone.mc.Up(0.5, velocity=0.5)

ArucoNav.Center()
time.sleep(1)

print ('Move')

Drone.mc.Forward(2, velocity=0.5)
ArucoNav.Center()
Drone.mc.TurnLeft(180, 45)
Drone.mc.Forward(2, velocity=0.5)
Drone.mc.TurnLeft(180, 45)
ArucoNav.Center()

Drone.mc.Down(0.4, velocity=0.4)

ArucoNav.Center()

time.sleep(1)

Drone.mc.Down(1.0, velocity=0.2)

Drone.Close()


