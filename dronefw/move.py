#!/usr/bin/env python3

from drone import *

#Drone=DroneClass('radio://0/1/2M')
Drone=DroneClass('usb://0')


# Main autonomous sequence
Drone.mc.TakeOff(0.3, 0.4);
print('Takeoff complete')

time.sleep(3)
Drone.mc.Up(0.5, velocity=0.5)
time.sleep(1)
print('Move!')
# for y in range (2):
#     mc.forward(0.5,velocity=0.5)
#     #mc.turn_right(360,90)
#     mc.right(0.5,velocity=0.5)
#     mc.back(0.5,velocity=0.5)
#     mc.left(0.5,velocity=0.5)
#     time.sleep(1)

Drone.mc.Forward(3.0 / 0.8, velocity=0.5)
Drone.mc.TurnLeft(90, 90)
Drone.mc.Forward(1.5 / 0.8, velocity=0.5)

Drone.mc.TurnLeft(180, 90)

Drone.mc.Forward(1.5 / 0.8, velocity=0.5)
Drone.mc.TurnRight(90, 90)
Drone.mc.Forward(3.0 / 0.8, velocity=0.5)

# mc.circle_left(0.5,0.5,360)
# mc.circle_right(0.5,0.5,360)

Drone.mc.TurnLeft(180, 90)

Drone.mc.Down(2.0, velocity=0.4)
Drone.mc.close()

Drone.Close()


