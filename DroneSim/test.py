
import DroneSim.Drone as drone
from DroneSim.Visualizer import Visualizer

markers = [
    (0,0,0),
    (1,1,0)
    ]

if __name__ == "__main__":

    screen = Visualizer(500, 500)
    if screen.initialze_coordinate_system(markers):
        screen.draw_markers(markers)

        drone = drone.Drone()
        drone.arm()
        drone.takeOff()

        running = True
        while running:
            # First check events
            running = not screen.quit_event()
