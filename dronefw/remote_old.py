#!/usr/bin/env python3


from drone import *

Drone=DroneClass()

LastStatusTime=0
StatusUpdateInterval=3


while (True):
    try:
        #Print status
        if (time.time()-LastStatusTime>StatusUpdateInterval):
            print ("Battery voltage:%s" % (Drone.Vbat))
            print ("Status:%s" % (Drone.DroneStatus))
            print ("")
            LastStatusTime=time.time()


        #Flight commands
        if (Drone.DroneStatus != DroneStatusEnum.Flying):
            if (Drone.Gamepad.Start==1 and Drone.DroneStatus==DroneStatusEnum.Idle):
                print ("Arm")
                Drone.Arm()
                Drone.mc.TakeOff(0.3, 0.4)
            elif (Drone.Gamepad.Start==1 and (Drone.DroneStatus==DroneStatusEnum.EmergencyLowBattery or
                  Drone.DroneStatus==DroneStatusEnum.EmergencyGamepadLoss or
                  Drone.DroneStatus==DroneStatusEnum.EmergencyGamepadStop or
                  Drone.DroneStatus==DroneStatusEnum.EmergencyGamepadLand)):
                Drone.ClearEmergency()

        if (Drone.DroneStatus == DroneStatusEnum.Flying):
            if (Drone.Gamepad.DpadUp==1):
                Drone.mc.Forward(0.2, velocity=0.5)
            if (Drone.Gamepad.DpadDown==1):
                Drone.mc.Back(0.2, velocity=0.5)
            if (Drone.Gamepad.DpadRight==1):
                Drone.mc.Right(0.2, velocity=0.5)
            if (Drone.Gamepad.DpadLeft==1):
                Drone.mc.Left(0.2, velocity=0.5)
            if (Drone.Gamepad.ButtonY==1):
                Drone.mc.Up(0.2, velocity=0.5)
            if (Drone.Gamepad.ButtonA==1):
                Drone.mc.Down(0.2, velocity=0.5)
            if (Drone.Gamepad.ButtonX==1):
                Drone.mc.TurnLeft(30, 90)
            if (Drone.Gamepad.ButtonB==1):
                Drone.mc.TurnRight(30, 90)
            if (Drone.Gamepad.R1==1):
                Drone.ArucoNav.Center()
            if (Drone.Gamepad.R2==1):
                #Drone.mc.MoveDistance(1.0, 0, 0, 0.5)
                Drone.ArucoNav.GuidedLand()
            if (Drone.Gamepad.L2==1):
                # Main autonomous sequence


                Drone.ArucoNav.Center()
                time.sleep(1)

                print('Move')

                Drone.mc.Forward(2.0, velocity=0.5)
                Drone.ArucoNav.Center()

                Drone.mc.Forward(2.0, velocity=0.5)
                Drone.ArucoNav.Center()

                Drone.mc.Forward(2.0, velocity=0.5)
                Drone.ArucoNav.Center()

                Drone.mc.Forward(2.0, velocity=0.5)
                Drone.ArucoNav.Center()
                Drone.ArucoNav.Center()

                Drone.mc.Down(0.4, velocity=0.4)

                Drone.ArucoNav.Center()

                time.sleep (1)

                Drone.mc.Down(1.0, velocity=0.4)
                Drone.mc.land()
    except Exception as e:
        print ("exception:%s" % e)

