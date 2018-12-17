
import time, argparse, sys
from subprocess import Popen
from signal import SIGINT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sim", help="Start a simulated drone.", action="store_true")
    parser.add_argument("-p", "--port", help="Define port for drone executing process.")
    parser.add_argument("-m", "--marker", help="Define the start position of the drone, by marker id.")
    parser.add_argument("-b", "--backend", help="Set IP address of the backend to connect to.")

    args = parser.parse_args()

    port = 5000 if not args.port else args.port
    marker = 1 if not args.marker else args.marker
    ip = "localhost" if not args.backend else args.backend

    if args.sim:
        # start a simulated drone
        executing_process = Popen(["python3", "DroneSim/DroneSimulator.py", str(port)])
        communicating_process = Popen(["python3", "DroneCore/Controller.py", str(port), str(marker), str(ip)])

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

        if executing_process.poll() is not None:
            executing_process.send_signal(SIGINT)
        if communicating_process.poll() is not None:
            communicating_process.send_signal(SIGINT)
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

        if executing_process.poll() is not None:
            executing_process.send_signal(SIGINT)
        if communicating_process.poll() is not None:
            communicating_process.send_signal(SIGINT)
