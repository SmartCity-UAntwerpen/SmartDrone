#Global drone settings


#URI='radio://0/1/2M'
URI='usb://0' #Drone connection URI
VbatMult = 2.6 #Scale factor to V
VbatLimit = 3.3  # Low battery limit; autoland below this limit (V)
VbatWarning = 3.6 # Low battery warning limit (V)
ArucoEnabled=True
ArucoMarkerSize=0.0792 #Aruco marker size in m
TravelDistAdj=1.0 #Travel distance correction parameter
SpoolUpTime=10 #Preflight motor spool up time (100 ms units)
MaxHeight=1.0 #Maximum altitude (m)
MaxZVel=0.5 #Maximum vertical velocity (m/s)
MaxXYVel=0.5 #Maximum horizontal velocity (m/s)
MaxYawRate=180 #Maximum yaw rate (deg/s)

GamepadRequired=True #Flag: gamepad connection required to start?

ParamList=[ #Rate loop PID parameters
            ['pid_rate.pitch_kp', '200.00'],['pid_rate.pitch_ki', '300.00'],['pid_rate.pitch_kd', '2.5'],
            ['pid_rate.roll_kp', '200.00'],['pid_rate.roll_ki', '300.00'],['pid_rate.roll_kd', '2.5'],
            ['pid_rate.yaw_kp', '120.00'],['pid_rate.yaw_ki', '16.70'],['pid_rate.yaw_kd', '0.00'],

            #Attitude loop PID parameters
            ['pid_attitude.pitch_kp', '6.00'],['pid_attitude.pitch_ki', '3.00'],['pid_attitude.pitch_kd', '0.01'],
            ['pid_attitude.roll_kp', '6.00'],['pid_attitude.roll_ki', '3.00'],['pid_attitude.roll_kd', '0.01'],
            ['pid_attitude.yaw_kp', '6.00'],['pid_attitude.yaw_ki', '1.00'],['pid_attitude.yaw_kd', '0.35'],

            #Velocity loop PID parameters
            ['velCtlPid.vxKp', '22'],['velCtlPid.vxKi', '1.0'],['velCtlPid.vxKd', '0.0'],
            ['velCtlPid.vyKp', '22'],['velCtlPid.vyKi', '1.0'],['velCtlPid.vyKd', '0.0'],
            ['velCtlPid.vzKp', '22'],['velCtlPid.vzKi', '22'],['velCtlPid.vzKd', '0.0'],

            #Other parameters
            ['posCtlPid.thrustMin','20000']
            ]