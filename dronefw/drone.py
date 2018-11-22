#!/usr/bin/env python3

import logging
import time
import sys
import os
import signal
import enum


import cflib.crtp
import threading
import settings
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from motion_commander import MotionCommander
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.log import LogConfig
from threading import Thread
from gamepad import *
from aruconav import *


class DroneStatusEnum(enum.Enum):
    Init=0
    Idle=1
    Armed=2
    Flying=3
    EmergencyLowBattery=4
    EmergencyGamepadLoss=5
    EmergencyGamepadLand=6
    EmergencyGamepadStop=7


class DroneClass:
    """
    Drone class. Base class controlling all interaction with the drone

    :ivar Vbat: Battery voltage (V)
    :ivar NumCells: The number of LiIon cells autodetected
    :ivar DroneStatus: Actual status of the drone
    :ivar Gamepad: Gamepad class instance
    :ivar ArucoNav: Aruco marker navigation class instance
    :ivar mc: Motion commander class instance. Used to control drone movement
    :ivar px: Drone X position
    :ivar py: Drone Y position
    :ivar pz: Drone Z position
    :ivar roll: Drone roll angle
    :ivar pitch: Drone pitch angle
    :ivar yaw: Drone yaw angle
    """
    def __init__(self):
        """
        Constructs an instance of a drone class
        """

        self.Vbat=-1
        self.NumCells=0
        self.DroneStatus=DroneStatusEnum.Init
        self.px=0.0
        self.py=0.0
        self.pz=0.0
        self.roll=0.0
        self.pitch=0.0
        self.yaw=0.0

        #Gamepad init
        self.Gamepad = GamepadClass()
        self.Gamepad.Callback=self._GamepadCallback

        #Aruco tag detector init
        if (settings.ArucoEnabled):
            self._Detector = ArucoClass(settings.ArucoMarkerSize)
            self.ArucoNav = ArucoNavClass(self, self._Detector)

        self.logger_thread_stop=threading.Event()



        # Only output errors from the logging framework
        logging.basicConfig(level=logging.ERROR)
        #logging.basicConfig(level=logging.DEBUG)

        # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)
        print ('Driver init complete')

        #Initialize logging framework
        self.lg_stab=LogConfig(name='Position', period_in_ms=100)
        self.lg_stab.add_variable('kalman.stateX', 'float')
        self.lg_stab.add_variable('kalman.stateY', 'float')
        self.lg_stab.add_variable('kalman.stateZ', 'float')
        self.lg_stab.add_variable('controller.roll', 'float')
        self.lg_stab.add_variable('controller.pitch', 'float')
        self.lg_stab.add_variable('controller.yaw', 'float')

        self.lg_diag = LogConfig(name='Diag', period_in_ms=100)
        self.lg_diag.add_variable('pm.vbat', 'float')
        self.lg_diag.add_variable('kalman.varPX', 'float')

        #Try and retry to connect
        while True:
            try:
                self.cf = Crazyflie(ro_cache='ro', rw_cache='rw')
                self.scf = SyncCrazyflie(settings.URI, cf=self.cf)
                self.scf.open_link()
                if (self.cf.link_established):
                    break;
            except:
                print ('Connection failed. Retry.')
                self.cf.close_link()


        time.sleep(1)
        print ('connect complete')

        #Set drone parameters
        for param in settings.ParamList:
            self.cf.param.set_value(param[0],param[1])
        print ('Parameters set')


        #Initialize motion commander
        self.mc=MotionCommander(self.scf,self)


        # Start logging thread
        self.logger_stab=SyncLogger(self.scf, self.lg_stab)
        self.logger_stab.connect()
        self.logger_diag=SyncLogger(self.scf, self.lg_diag)
        self.logger_diag.connect()
        self.logger_thread = Thread(target=self._logger_thread_worker, args=([self.logger_stab, self.logger_diag]))
        self.logger_thread.start()


        #CTRL-C handler.
        aborted_list = {'aborted': 0}
        def _signal_handler(signal, frame):
            if (aborted_list['aborted']==0): #One press: autoland
                aborted_list['aborted'] = 1
                print('CTRL-C: auto land!')
                self.mc.land(0.4,True)
                time.sleep(4)
                self.scf.close_link()
                self.cf.close_link()
                os._exit(0)
            if (aborted_list['aborted']==1): #Two presses: immediate shutdown
                aborted_list['aborted'] = 2
                print('CTRL-C: hard abort!')
                self.mc.EmergencyStop()
                time.sleep(1)
                self.scf.close_link()
                self.cf.close_link()
                time.sleep(1)
                os._exit(0)
            if (aborted_list['aborted'] == 2):
                print ("Already shutting down.")
        signal.signal(signal.SIGINT, _signal_handler)

        self.DroneStatus=DroneStatusEnum.Idle
        print('Init complete')

    def _logger_thread_worker(self, logger_stab, logger_diag):
        posfile=open("posfile","w")
        while (not self.logger_thread_stop.is_set()):
            for log_entry in logger_stab:
                timestamp = log_entry[0]
                data = log_entry[1]

                self.px = data.get('kalman.stateX')
                self.py = data.get('kalman.stateY')
                self.pz = data.get('kalman.stateZ')
                self.roll = data.get('controller.roll')
                self.pitch = data.get('controller.pitch')
                self.yaw = data.get('controller.yaw')

                posfile.write("%s,%s,%s,%s,%s,%s\n" % (self.px, self.py, self.pz, self.yaw, self.roll, self.pitch))
                #print('px:[%s] py:[%s] pz:[%s] roll:[%s] pitch:[%s] yaw:[%s]' % (self.px,self.py,self.pz,self.roll,self.pitch,self.yaw))

                break
            for log_entry in logger_diag:
                timestamp = log_entry[0]
                data = log_entry[1]

                self.varX = data.get('kalman.varPX')
                self.Vbat=data.get('pm.vbat')*settings.VbatMult

                #Battery handling
                #Battery cell count autodetect
                if (self.NumCells==0):
                    if (self.Vbat<8.6):
                        self.NumCells=2
                        print ("Number of battery cells: 2")
                    else:
                        self.NumCells=3
                        print("Number of battery cells: 3")

                #Low battery autoland
                if (self.Vbat<(settings.VbatLimit*self.NumCells)):
                    self.mc.land()
                if (self.Vbat<(settings.VbatLimit*self.NumCells)):
                    print ("Battery low. %s V" % (self.Vbat))
                #print ('m1:[%s] m2:[%s] m3:[%s] m4:[%s]'% (self.m1,self.m2,self.m3,self.m4))
                #print ('vbat:%s' % (self.Vbat))
                #if (self.varX>4.8E-5):
                #    print('varx:%s' % (self.varX))
                break

        posfile.close()


    def Arm(self):
        """
        Puts drone in armed mode. Can takeoff afterwards
        """
        #Prearm checklist
        if (self.Vbat<(settings.VbatWarning*self.NumCells)):
            raise Exception("Battery too low to fly; %s V per cell" % str(self.Vbat /self.NumCells))
        if (self.Gamepad.Connected == 0 and settings.GamepadRequired == True):
            raise Exception("Arming without gamepad connection is not permitted!")
        self.mc.EmergencyStop()
        self.cf.param.set_value('safety.estop', '0')
        self.DroneStatus=DroneStatusEnum.Armed

    def _GamepadCallback(self):
        #Left button 1: autoland
        if (self.Gamepad.L1):
            threading.Thread(target=self.mc.land,args=([0.4,True])).start() #Asynch call, so emergency stop can still be performed
            self.DroneStatus=DroneStatusEnum.EmergencyGamepadLand

        #Back button: emergency stop
        if (self.Gamepad.Back == 1):
            try:
                self.mc.EmergencyStop()
                self.DroneStatus=DroneStatusEnum.EmergencyGamepadStop
            except:
                pass

        #Connection loss: autoland
        if (self.Gamepad.Connected == 0 and settings.GamepadRequired==True):
            self.DroneStatus=DroneStatusEnum.EmergencyGamepadLoss
            self.mc.land(0.4)


    def Close(self):
        """
        Terminates drone connection, disarms drone
        """
        #Terminate and perform safing of drone
        print ('Terminating')
        time.sleep(3)
        self.cf.param.set_value('safety.estop', '1')
        self.mc.close()
        self.scf.close_link()
        self.logger_thread_stop.set()
        self.logger_thread.join()




    



