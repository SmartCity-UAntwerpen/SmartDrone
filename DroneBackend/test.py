import DroneSim.Drone as drone
from DroneBackend.Visualizer import Visualizer
from DroneCore.Marker import Marker

if __name__ == "__main__":

    m0 = Marker(1, 1, 0, 0)
    m1 = Marker(2, 1, 0, 1)
    m2 = Marker(1, 2, 0, 2)
    m3 = Marker(2, 2, 0, 3)
    m4 = Marker(4, 3, 0, 4)
    markers = [m0, m1, m2, m3, m4]

    screen = Visualizer(500, 500)
    screen.init_markers(markers)
    screen.draw_markers(markers)

    drone = drone.Drone()
    drone.arm()
    drone.takeOff()

    running = True
    while running:
        # First check events
        running = not screen.quit_event()
