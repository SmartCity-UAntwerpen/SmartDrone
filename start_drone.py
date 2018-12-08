
import time, argparse
from subprocess import Popen

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sim", help="Start a simulated drone.")
    parser.add_argument("--port", help="Define port for drone executing process.")
    parser.add_argument("--marker", help="Define the start position of the drone, by marker id.")

    args = parser.parse_args()

    port = 5000 if not args.port else args.port
    marker = 0 if not args.marker else args.marker

    if args.sim:
        # start a simulated drone
        executing_process = Popen(["python", "DroneSim/DroneSimulator.py", str(port)])
        communicating_process = Popen(["python", "DroneCore/Controller.py", str(port), str(marker)])

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

        executing_process.terminate()
        communicating_process.terminate()
