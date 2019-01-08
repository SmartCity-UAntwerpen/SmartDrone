import argparse, time
import subprocess
from Common.SocketCallback import SocketCallback
import signal,sys

drones = {}


def create(id):
    global drones
    print("Create drone.")
    # append id in list
    if id in drones:
        return b'NACK'
    else:
        # dictionary key (drone id_ value( marker, simProcess, controllerProcess)
        drones[id] = [-1, None, None]
        return b'ACK'


def run(id):
    global drones
    # start simulated.
    print("Run drone.")
    start_marker_id = drones[id][0]
    if start_marker_id == -1 or start_marker_id is None:
        drones[id][0] = 0
        start_marker_id = 0

    intID = int(id)
    simport = 5000 + intID * 2
    simProcess = subprocess.Popen(["python", "../DroneSim/DroneSimulator.py", str(simport)])
    drones[id][1] = simProcess
    controlProcess = subprocess.Popen(["python","../DroneCore/Controller.py",str(simport), str(start_marker_id), str(backendIP)])
    drones[id][2] = controlProcess


def stop(id):
    global drones
    print("Stop drone.")
    # stop simulated
    if id in drones:
        simprocess = drones[id][1]
        controlProcess = drones[id][2]
        if simprocess is None and controlProcess is None:
            print("no process to kill")
            return b'NACK'
        else:
            try:
                if sys.platform == 'win32':
                    # TODO fix windows
                    print("cannot stop this program when running on windows")
                else:
                    simprocess.send_signal(signal.SIGINT)
                    controlProcess.send_signal(signal.SIGINT)
            except:
                return b'NACK'
        return b'ACK'
    else:
        return b'NACK'


def kill(id):
    global drones
    print("Kill drone.")
    # remove id from list
    if id in drones:
        drones.pop(id)
        return b'ACK'
    else:
        return b'NACK'


def restart(id):
    answer = run(id)
    return answer


def set_startpoint(id, startpoint):
    global drones
    print("set_startpoint")
    if id in drones:
        drones[id][0] = startpoint if type(startpoint) is 'int' else 0
        return b'ACK'
    else:
        return b'NACK'


def handle_command(sock, data):
    try:
        data = data.decode()

        words = data.split()
        function_name = words[0]
        id = words[1]
        if id.isdigit():
            func = globals()[function_name]
            if len(words) == 2:
                answer = func(id)
            elif len(words) == 3:
                answer = func(id, words[2])
            else:
                answer = b'NACK'
        else:
            answer = b'NACK'
        sock.send(answer)
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--backend", help="backend ip")
    parser.add_argument("-p", "--port", help="Define port of connection with simulation backend.")
    parser.add_argument("-i", "--ip", help="Ip of connection with simulation backend.")

    args = parser.parse_args()

    global port
    port = 5000 if not args.port else int(args.port)
    global backendIP
    backendIP = "localhost" if not args.backend else args.backend
    global ip
    ip = "localhost" if not args.ip else args.ip

    print("simulationCore started. Send TCP/ip packet at ", ip, ":", port)
    print("create id: adds drone to the list")
    print("run id: starts simulated drone")
    print("stop id: stops simulated drone, works only on linux")
    print("kill id: removes drone from the list")
    print("set_startpoint id startpoint: change startpoint from drone")

    command_socket = SocketCallback(ip, port)
    command_socket.add_callback(handle_command)
    command_socket.start()
