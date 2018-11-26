
import DroneSim.Drone as drone


if __name__ == "__main__":
    drone = drone.Drone()
    drone.arm()
    drone.takeOff()
    drone.down(0.05,0.2)
    drone.center(1,1)
