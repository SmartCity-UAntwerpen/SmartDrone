import argparse, time
import _thread as thread
from subprocess import Popen
from Common.SocketCallback import SocketCallback

drones = {}


def create(id):
    print("Create drone.")
    # append id in list
    if id in drones:
        return b'NACK'
    else:
        # dictionary key (drone id_ value( marker, running)
        drones[id] = (-1, True)
        return b'ACK'


def start_drone(id):
    if id in drones:
        start_marker_id = drones[id][0]
        if start_marker_id == -1 or start_marker_id is None:
            start_marker_id = 0
        id = int(id)
        simport = 5000 + id * 2
        process = Popen(
            ["python", "../start_drone.py", "-s", "-p", str(simport), "-m", str(start_marker_id), "-b", backendIP])
        running = True
        try:
            while running:
                running = drones[str(id)][1]
                print(running)
                if process.poll() is not None:
                    running = False
                time.sleep(1)
        except KeyboardInterrupt:
            running = False
        print("process stopped.")
        process.terminate()
        # TODO process stops but threads keep running

def run(id):
    # start simulated.
    print("Run drone.")
    try:
        thread.start_new_thread(start_drone, (id,))
        return b'ACK'
    except Exception as e:
        print(e)
        return b'NACK'


def stop(id):
    print("Stop drone.")
    # stop simulated
    if id in drones:
        marker_id = drones[id][0]
        drones[id] = (marker_id, False)
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
    if id in drones:
        drones[id] = (startpoint, True)
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
    print(drones)
