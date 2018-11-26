
import Drone, socket, signal, sys, json

drone = Drone.Drone()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def exit(signal, frame):
    print("Closing socket...")
    s.close()
    # land drone?
    print("Simulator tured off.")
    sys.exit(0)


def perform_action(command, conn):
    message = json.loads(command.decode())
    if drone.is_armed() or drone.is_Flying():
        if message["command"] == "move":
            goal = message["goal"]
            drone.moveDistance(goal[0],goal[1],goal[2],message["velocity"])
            conn.send(b'ACK')
        elif message["command"] == "takeoff":
            drone.takeOff(message["height"], message["velocity"])
            conn.send(b'ACK')
        else:
            conn.send(b'WHAT?')
    else:
        if message["command"] == "arm":
            drone.arm()
            conn.send(b'ACK')
        else:
            conn.send(b'NOT ARMED')


if __name__ == "__main__":
    s.bind(("127.0.0.1", int(sys.argv[1])))
    s.listen(1)

    signal.signal(signal.SIGINT, exit)
    drone.black_box.info("Drone simulator started.")

    conn, addr = s.accept()  # wait for a connection
    while 1:
        data = conn.recv(1024)     # recieve data with buffer of size 1024
        if not data:
            exit(1,1)
        perform_action(data, conn)
