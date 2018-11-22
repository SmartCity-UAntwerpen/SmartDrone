from drone import *
from arucolib import *

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

    def Detect(self,MarkerId=-1):
        """
        Try to detect aruco markers under the drone

        :param MarkerId: -1 if any marker ID should be detected, otherwise an ID value (NOT IMPLEMENTED)

        :returns:
        None if no valid marker has been detected. Otherwise returns an instance of MarkerVectorClass
        containing the relative vector to the detected marker.
        """
        self.MarkerVector=MarkerVectorClass

        print('Scan')
        for a in range(0, 15):
            num = self._Detector.Detect()
            print('Num:%s' % (num))
        for a in range(0, 40):
            num = self._Detector.Detect()
            print('Num:%s' % (num))
            if (num > 0):
                break;

        if (num > 0):
            self.MarkerVector.Id=self._Detector.MarkerList[0].MarkerId
            self.MarkerVector.Y = -self._Detector.MarkerList[0].TVecX
            self.MarkerVector.X = -self._Detector.MarkerList[0].TVecY
            self.MarkerVector.Rot=self._Detector.GetMarkerYaw(0)
            print ('Marker:(%s,%s,%s)' % (self.MarkerVector.X,self.MarkerVector.Y,self.MarkerVector.Rot))
            return self.MarkerVector
        else:
            print("None detected")
            return None

    def Center(self,MarkerId=-1,Velocity=0.5):
        """
        Try to detect aruco markers under the drone, flies and aligns itself to the marker. If marker is not detected,
        does nothing.

        :param MarkerId: -1 if any marker ID should be detected, otherwise an ID value (NOT IMPLEMENTED)
        :param Velocity: Speed (m/s) of the drone while centering
        """
        MarkerVector=self.Detect(MarkerId)

        if (MarkerVector is not None):
            self._Drone.mc.MoveDistance(MarkerVector.X, MarkerVector.Y, 0, Velocity)
            if (MarkerVector.Rot>0):
                self._Drone.mc.TurnRight(MarkerVector.Rot, self.RotRate)
            else:
                self._Drone.mc.TurnLeft(-MarkerVector.Rot, self.RotRate)

