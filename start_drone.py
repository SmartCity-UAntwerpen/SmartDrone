
import time, argparse, sys
from subprocess import Popen

running = False
executing_process = None
communicating_process = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sim", help="Start a simulated drone.", action="store_true")
    parser.add_argument("-p", "--port", help="Define port for drone executing process.")
    parser.add_argument("-m", "--marker", help="Define the start position of the drone, by marker id.")
    parser.add_argument("-b", "--backend", help="Set IP address of the backend to connect to.")
    parser.add_argument("-a", "--auto", help="Enable auto-arm functionality, works only for simulated drones.", action="store_true")

    args = parser.parse_args()

    port = 5000 if not args.port else args.port
    marker = 1 if not args.marker else args.marker
    ip = "localhost" if not args.backend else args.backend
    auto_arm = "" if not args.auto else "auto_arm"

    if args.sim:
        # start a simulated drone
        executing_process = Popen(["python3", "DroneSimulator.py", str(port), auto_arm], cwd=sys.path[0]+"/DroneSim")
        communicating_process = Popen(["python3", "Controller.py", str(port), str(marker), str(ip)],cwd=sys.path[0]+"/DroneCore")

        running = True
        try:
            while running:
                if executing_process.poll() is not None:
                    print("Executing process stopped.")
                    running = False
                if communicating_process.poll() is not None:
                    print("Communicating process stopped.")
                    running = False
                time.sleep(1)
        except KeyboardInterrupt:
            running = False

    else:
        # start a normal drone
        executing_process = Popen(["python3", "remote.py", str(port)],  cwd=sys.path[0]+"/dronefw")
        communicating_process = Popen(["python3", "DroneCore/Controller.py",  str(port), str(marker), str(ip)])

        running = True
        try:
            while running:
                if executing_process.poll() is not None:
                    print("Executing process stopped.")
                    running = False
                if communicating_process.poll() is not None:
                    print("Communicating process stopped.")
                    running = False
                time.sleep(1)
        except KeyboardInterrupt:
            running = False
