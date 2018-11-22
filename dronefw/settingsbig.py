#Global drone settings


#URI='radio://0/1/2M'
URI='usb://0' #Drone connection URI
VbatMult = 8.4 #Scale factor to V
VbatLimit = 3.3  # Low battery limit; autoland below this limit (V)
VbatWarning = 3.6 # Low battery warning limit (V)
ArucoEnabled=False
ArucoMarkerSize=0.0792 #Aruco marker size in m
TravelDistAdj=10/9 #Travel distance correction parameter
SpoolUpTime=10 #Preflight motor spool up time (100 ms units)
MaxHeight=1.0 #Maximum altitude (m)
MaxZVel=0.5 #Maximum vertical velocity (m/s)
MaxXYVel=0.5 #Maximum horizontal velocity (m/s)
MaxYawRate=180 #Maximum yaw rate (deg/s)

GamepadRequired=False #Flag: gamepad connection required to start?

ParamList=[ ['velCtlPid.vzKp', '22'],['velCtlPid.vzKi', '22'],
            ['posCtlPid.thrustMin','20000'],
            ['velCtlPid.vxKp', '22'],['velCtlPid.vyKp', '22'],
            ['pid_attitude.pitch_kd', '0.01'],['pid_attitude.pitch_ki', '3.00'],['pid_attitude.pitch_kp', '6.00'],
            ['pid_attitude.roll_kd', '0.01'],['pid_attitude.roll_ki', '3.00'],['pid_attitude.roll_kp', '6.00'],
            ['pid_rate.pitch_kp', '200.00'],
            ['pid_rate.roll_kp', '200.00']]