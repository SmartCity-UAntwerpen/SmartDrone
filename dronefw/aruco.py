#!/usr/bin/env python3

from ctypes import *

class MarkerStruct(Structure):
   _fields_ = [("MarkerId", c_int),("TVecX", c_float),("TVecY",c_float),("TVecZ",c_float)]
                        

class aruco:
   def __init__(self,MarkerSize):
      self.MarkerSize=MarkerSize
      self.MaxNumMarkers=10
      self.MarkerList=(MarkerStruct*self.MaxNumMarkers)()
      self.detector=CDLL('./aruco.so')
      self.detector.ArucoInit(0, c_char_p("cam.yml".encode('UTF-8')), c_float(self.MarkerSize))
   def Detect(self):
      num = self.detector.ArucoDetect(self.MaxNumMarkers, byref(self.MarkerList))
      return num


if __name__=="__main__":
   Detector=aruco(0.087)
   while (True):
      num=Detector.Detect()
      if (num > 0):
         for a in range(0, num):
            print("Id:%s>(%s,%s,%s)" % (Detector.MarkerList[a].MarkerId, Detector.MarkerList[a].TVecX, Detector.MarkerList[a].TVecY, Detector.MarkerList[a].TVecZ))


   
