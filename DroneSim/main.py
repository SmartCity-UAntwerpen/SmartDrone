
from Drone import Drone

if __name__ == "__main__":
    drone = Drone()
    drone.arm()
    drone.takeOff()
    drone.forward(1)
    drone.back(1)
    drone.printInfo()
