#!/usr/bin/env python3

from ctypes import *
import cv2
import numpy
import math


class MarkerStruct(Structure):
   _fields_ = [("MarkerId", c_int),("TVecX", c_float),("TVecY",c_float),("TVecZ",c_float),("RVecX", c_float),("RVecY",c_float),("RVecZ",c_float)]
                        

class ArucoClass:
   def __init__(self,MarkerSize):
      self.MarkerSize=MarkerSize
      self.MaxNumMarkers=10
      self.MarkerList=(MarkerStruct*self.MaxNumMarkers)()
      self.detector=CDLL('./aruco.so')
      self.detector.ArucoInit(0, c_char_p("cam.yml".encode('UTF-8')), c_float(self.MarkerSize))
   def Detect(self):
      num = self.detector.ArucoDetect(self.MaxNumMarkers, byref(self.MarkerList))
      return num
   def GetMarkerYaw(self,MarkerIdx):
      rvec = numpy.array([self.MarkerList[0].RVecX, self.MarkerList[0].RVecY, self.MarkerList[0].RVecZ])[numpy.newaxis]
      tvec = numpy.array([self.MarkerList[0].TVecX, self.MarkerList[0].TVecY, self.MarkerList[0].TVecZ])[numpy.newaxis]
      rvec = numpy.transpose(rvec)
      tvec = numpy.transpose(tvec)
      rvec_matrix = cv2.Rodrigues(rvec)[0]
      proj_matrix = numpy.hstack((rvec_matrix, tvec))
      euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)[6]
      return euler_angles[2]


if __name__=="__main__":
   Detector=ArucoClass(0.087)
   while (True):
      num=Detector.Detect()
      if (num > 0):
         for a in range(0, num):
            rot=Detector.GetMarkerYaw(a)
            print("Id:%s>T(%s,%s,%s) R(%s)" % (Detector.MarkerList[a].MarkerId, Detector.MarkerList[a].TVecX, Detector.MarkerList[a].TVecY, Detector.MarkerList[a].TVecZ, rot))

            #print ("%s"%(Detector.MarkerList[0].RVecZ))

   
