#!/usr/bin/env python3

#code type val
#dpad left 16 3 -1
#dpad x center 16 3 0
#dpad right 16 3 1
#dpad up 17 3 -1
#dpad down 17 3 1
#dpad y center 17 3 0

#x 304 01 X
#b 306 01 X
#Y 307 01 X
#A 305 01 X

import evdev
import threading
import time

class GamepadClass:
    def ResetVars(self):
        self.ButtonX=0
        self.ButtonY=0
        self.ButtonA=0
        self.ButtonB=0
        self.DpadLeft=0
        self.DpadRight=0
        self.DpadUp=0
        self.DpadDown=0
        self.Start=0
        self.Back=0
        self.L1=0
        self.L2=0
        self.R1=0
        self.R2=0
        self.Connected=0



    def worker(self):
        while (True):
            #send callback if connection drops

            if (self.Connected==0):
                try:
                    self.dev = evdev.InputDevice("/dev/input/event0")
                    self.Connected=1
                except:
                    self.Connected=0
                    time.sleep(0.1)

            if (self.Connected==1):
                try:
                    for event in self.dev.read_loop():
                        #DPAD Left-right
                        #print ("Code:%s Type:%s Value:%s" % (event.code,event.type,event.value))
                        if (event.code==16 and event.type==3 and event.value==-1):
                            self.DpadLeft=1
                            self.DpadRight=0
                        if (event.code==16 and event.type==3 and event.value==0):
                            self.DpadLeft=0
                            self.DpadRight=0
                        if (event.code==16 and event.type==3 and event.value==1):
                            self.DpadLeft=0
                            self.DpadRight=1
                        #DPAD Up-down
                        if (event.code==17 and event.type==3 and event.value==-1):
                            self.DpadUp=1
                            self.DpadDown=0
                        if (event.code==17 and event.type==3 and event.value==0):
                            self.DpadUp=0
                            self.DpadDown=0
                        if (event.code==17 and event.type==3 and event.value==1):
                            self.DpadUp=0
                            self.DpadDown=1

                        #X
                        if (event.code==304 and event.type==1 and event.value==1):
                            self.ButtonX=1
                        if (event.code==304 and event.type==1 and event.value==0):
                            self.ButtonX=0
                        #Y
                        if (event.code==307 and event.type==1 and event.value==1):
                            self.ButtonY=1
                        if (event.code==307 and event.type==1 and event.value==0):
                            self.ButtonY=0
                        #A
                        if (event.code==305 and event.type==1 and event.value==1):
                            self.ButtonA=1
                        if (event.code==305 and event.type==1 and event.value==0):
                            self.ButtonA=0
                        #B
                        if (event.code==306 and event.type==1 and event.value==1):
                            self.ButtonB=1
                        if (event.code==306 and event.type==1 and event.value==0):
                            self.ButtonB=0

                        #Start
                        if (event.code==313 and event.type==1 and event.value==1):
                            self.Start=1
                        if (event.code==313 and event.type==1 and event.value==0):
                            self.Start=0

                        #Back
                        if (event.code==312 and event.type==1 and event.value==1):
                            self.Back=1
                        if (event.code==312 and event.type==1 and event.value==0):
                            self.Back=0

                        #L1
                        if (event.code==308 and event.type==1 and event.value==1):
                            self.L1=1
                        if (event.code==308 and event.type==1 and event.value==0):
                            self.L1=0

                        #L2
                        if (event.code==310 and event.type==1 and event.value==1):
                            self.L2=1
                        if (event.code==310 and event.type==1 and event.value==0):
                            self.L2=0

                        #R1
                        if (event.code==309 and event.type==1 and event.value==1):
                            self.R1=1
                        if (event.code==309 and event.type==1 and event.value==0):
                            self.R1=0

                        #R2
                        if (event.code==311 and event.type==1 and event.value==1):
                            self.R2=1
                        if (event.code==311 and event.type==1 and event.value==0):
                            self.R2=0

                        if (callable(self.Callback)):
                            self.Callback()

                except:
                        self.ResetVars()
                        self.Callback()


    def __init__(self):
        self.ResetVars()
        self.Callback = 0;
        threading.Thread(target=self.worker).start()

if __name__=="__main__":
    Gamepad=GamepadClass()
    while (True):
        print ("C:%s DPAD: %s %s %s %s XYAB: %s %s %s %s START-BACK: %s %s L12R12: %s %s %s %s" % \
               (Gamepad.Connected,Gamepad.DpadLeft,Gamepad.DpadRight,Gamepad.DpadUp,Gamepad.DpadDown, \
                Gamepad.ButtonX,Gamepad.ButtonY,Gamepad.ButtonA,Gamepad.ButtonB, \
                Gamepad.Start,Gamepad.Back,Gamepad.L1,Gamepad.L2,Gamepad.R1,Gamepad.R2))
        time.sleep(0.5)
