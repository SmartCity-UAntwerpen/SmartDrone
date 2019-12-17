from arucolib import *
from drone import *
import math


class MarkerVectorClass:
    """
    Aruco marker class. Contains a detected marker ID and relative vector to the marker.

    :ivar Id: Marked ID
    :ivar X: X offset (m)
    :ivar Y: Y offset (m)
    :ivar Rot: Relative yaw rotation to marker (-180° to +180°)
    """
    Id=0   
    X=0
    Y=0
    Rot=0


class ArucoNavClass:
    """
    Aruco navigation class. Enables detection and automatic flight relative to a detected aruco marker

    :ivar RotRate: Yaw rotation rate when centering above a marker
    """
    def __init__(self,Drone,Detector):
        """
        Constructs an instance of an aruco navigation class

        :param Drone: initialized DroneClass instance of drone to be controlled
        :param Detector: initialized ArucoClass instance of aruco detector
        """
        self._Drone=Drone
        self._Detector=Detector
        self.RotRate=20
        self._DebugPrint = True

    def DetectArray(self,MarkerId=-1,PipelineFlush=True,NumTries=40,CalcYaw=True):
        """
        Try to detect aruco markers under the drone

        :param MarkerId: -1 if any marker ID should be detected, otherwise an ID value (NOT IMPLEMENTED)

        :returns:
        None if no valid marker has been detected. Otherwise returns an array [id, x, y, MarkerYaw]
        containing the relative vector to the detected marker.

        :note:
        x and Y are calculated taking into account the yaw rotation of the drone to the marker 

        """
        print("Detecting deviation to marker.")
        self.MarkerVectorArray=None

        if (PipelineFlush==True):
            for a in range(0, 15):
                num = self._Detector.Detect()
        for a in range(0, NumTries):
            num = self._Detector.Detect()
            if (num > 0):
                break;

        if (num > 0):
            self.MarkerVectorArray[0]=self._Detector.MarkerList[0].MarkerId
            x_dev= self._Detector.MarkerList[0].TVecX #x deviation
            y_dev = self._Detector.MarkerList[0].TVecY #y deviation
            self.MarkerVectorArray[3]=self._Detector.GetMarkerYaw(0)       
            #calculate detected path according to rotation to marker (MarkerYaw). 
             #Note: Drone first rotates back to desired angle before continuing flight.
            #x_corr = x_dev*math.cos(self.MarkerVectorArray[3]) + y_dev*math.sin(self.MarkerVectorArray[3])
            #y_corr = x_dev*math.sin(self.MarkerVectorArray[3]) + y_dev*math.cos(self.MarkerVectorArray[3])
            self.MarkerVectorArray[1] = x_dev
            self.MarkerVectorArray[2] = y_dev
            return self.MarkerVectorArray
        else:
            if (self._DebugPrint == True):
                print("Detection failed, no marker found.")
            return [99,0,0,0]

    def Detect(self,MarkerId=-1,PipelineFlush=True,NumTries=40,CalcYaw=True):
        """
        Try to detect aruco markers under the drone

        :param MarkerId: -1 if any marker ID should be detected, otherwise an ID value (NOT IMPLEMENTED)

        :returns:
        None if no valid marker has been detected. Otherwise returns an instance of MarkerVectorClass
        containing the relative vector to the detected marker.
        """
        self.MarkerVector=MarkerVectorClass

        if (PipelineFlush==True):
            for a in range(0, 15):
                num = self._Detector.Detect()
        for a in range(0, NumTries):
            num = self._Detector.Detect()
            if (num > 0):
                break;

        if (num > 0):
            self.MarkerVector.Id=self._Detector.MarkerList[0].MarkerId
            self.MarkerVector.Y = -self._Detector.MarkerList[0].TVecX
            self.MarkerVector.X = -self._Detector.MarkerList[0].TVecY
            if (CalcYaw==True):
                self.MarkerVector.Rot=self._Detector.GetMarkerYaw(0)
            if (self._DebugPrint == True):
                print ('Marker:(%s,%s,%s)' % (self.MarkerVector.X,self.MarkerVector.Y,self.MarkerVector.Rot))
            return self.MarkerVector
        else:
            if (self._DebugPrint == True):
                print("None detected")
            return None
    

    def Center(self,MarkerId=-1,Velocity=0.5):
        """
        Try to detect aruco markers under the drone, flies and aligns itself to the marker. If marker is not detected,
        does nothing.

        :param MarkerId: -1 if any marker ID should be detected, otherwise an ID value (NOT IMPLEMENTED)
        :param Velocity: Speed (m/s) of the drone while centering
        :returns:
        None if no valid marker has been detected. Otherwise returns an instance of MarkerVectorClass
        containing the relative vector to the detected marker before the centering operation.
        """
        MarkerVector=self.Detect(MarkerId)

        if (MarkerVector is not None):
            self._Drone.mc.MoveDistance(MarkerVector.X, MarkerVector.Y, 0, Velocity)
            if (MarkerVector.Rot>0):
                self._Drone.mc.TurnRight(MarkerVector.Rot, self.RotRate)
            else:
                self._Drone.mc.TurnLeft(-MarkerVector.Rot, self.RotRate)
        return MarkerVector

    def GuidedLand(self,XYVelocitySlow=0.05,XYVelocityFast=0.4,ZVelocitySlow=0.1,ZVelocityFast=0.4,MinGuidedHeight=0.3):
        """
        Try to land on an aruco marker in the viewport of the drone. If no marker is detected, an unguided landing is performed.
        If a marker is detected, the drone will first perform a centering operation on the marker and then perform a slow descent
        while tracking the marker. When descending under a specified height, the rest of the descent is performed unguided.
        Currently guidance velocity is limited by the latency of the Aruco detector.

        :param XYVelocitySlow: XY speed (m/s) while performing guided operations
        :param XYVelocityFast: XY speed (m/s) while performing unguided operations
        :param ZVelocitySlow: Z speed (m/s) while performing guided operations
        :param ZVelocityFast: Z speed (m/s) while performing unguided operations
        :param MinGuidedHeight: underneath this height the rest of the descent will be performed unguided
        :param Velocity: Speed (m/s) of the drone while centerin
        :returns:
        None if no valid marker has been detected. Otherwise returns an instance of MarkerVectorClass
        containing the relative vector to the detected marker before the centering operation.
        """


        #First center command, flush camera pipeline
        MarkerVector=self.Center(-1,XYVelocityFast)
        self.Center(-1,XYVelocityFast)

        if (MarkerVector is None):
            #No marker detected --> perform normal unguided fast land
            self._Drone.mc.land(ZVelocityFast)
            return MarkerVector

        #Continuous descent
        while (self._Drone.pz>MinGuidedHeight):
            if (self._DebugPrint == True):
                print ("pz:%s" %(self._Drone.pz))
            MarkerVector = self.Detect(PipelineFlush=False,NumTries=1,CalcYaw=False)
            if (MarkerVector is not None):
                vl=math.sqrt (MarkerVector.X**2 + MarkerVector.Y**2)
                vx=MarkerVector.X/vl*XYVelocitySlow
                vy=MarkerVector.Y/vl*XYVelocitySlow
                self._Drone.mc.start_linear_motion(vx, vy, -ZVelocitySlow)
            else:
                self._Drone.mc.start_linear_motion(0, 0, -ZVelocitySlow)
        print ("Fast land!")
        self._Drone.mc.land(ZVelocityFast)
        return MarkerVector
