#!/usr/bin/env python3

from drone import *

Drone=DroneClass('radio://0/1/2M')
#Drone=DroneClass('usb://0')


# Main autonomous sequence
Drone.mc.take_off(0.3, 0.4);
print('Takeoff complete')

time.sleep(3)
Drone.mc.up(0.3, velocity=0.5)
time.sleep(1)
print('Move!')


Drone.mc.forward(1.0 / 0.8, velocity=0.5)
print ('turn')
Drone.mc.turn_left(180, 90)
Drone.mc.forward(1.0 / 0.8, velocity=0.5)

Drone.mc.down(2.0, velocity=0.4)
Drone.mc.close()

Drone.Close()


