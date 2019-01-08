import argparse, time
import subprocess
from Common.SocketCallback import SocketCallback

drones = {}


def create(id):
    print("Create drone.")
    # append id in list
    if id in drones:
        return b'NACK'
    else:
        # dictionary key (drone id_ value( marker, process)
        drones[id] = [-1, None]
        return b'ACK'


def run(id):
    # start simulated.
    print("Run drone.")
    start_marker_id = drones[id][0]
    if start_marker_id == -1 or start_marker_id is None:
        drones[id][0] = 0
    intID = int(id)
    simport = 5000 + intID * 2
    process = subprocess.Popen(
        ["python", "../start_drone.py", "-s", "-p", str(simport), "-m", str(start_marker_id), "-b", backendIP])
    drones[id][1] = process


def stop(id):
    print("Stop drone.")
    # stop simulated
    if id in drones:
        process = drones[id][1]
        if process is None:
            print("no process to kill")
            return b'NACK'
        else:
            try:
                # TODO process does not kill
                process.kill()
            except:
                return b'NACK'
        return b'ACK'
    else:
        return b'NACK'


def kill(id):
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
        func = globals()[function_name]

        answer = func(id)
        sock.send(answer)
    except:
        pass


def test(data):
    words = data.split()
    function_name = words[0]
    id = words[1]
    func = globals()[function_name]

    answer = func(id)
    print(answer)


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

    command_socket = SocketCallback(ip, port)
    command_socket.add_callback(handle_command)
    command_socket.start()

    # for testing without socket
    print("simulationCore started")
    test("create 3")
    test("run 3")
    time.sleep(10)
    test("stop 3")
    print("program done")
