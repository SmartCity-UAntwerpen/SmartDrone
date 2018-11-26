
import Drone, socket, signal, sys, json

markers = [
        (1,1,0),
        (2,1,0),
        (1,2,0),
        (2,2,0),
        (1,3,0)
    ]

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
    if drone.is_armed():
        if message["command"] == "takeoff":
            drone.takeOff(message["height"], message["velocity"])
            conn.send(b'ACK')
            return

    if drone.is_flying():
        if message["command"] == "land":
            drone.land()
            conn.send(b'ACK')
            return

        elif message["command"] == "move":
            goal = message["goal"]
            drone.moveDistance(goal[0],goal[1],goal[2],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "forward":
            drone.forward(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "backward":
            drone.backward(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "left":
            drone.left(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "right":
            drone.right(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "up":
            drone.up(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "down":
            drone.down(message["distance"],message["velocity"])
            conn.send(b'ACK')
            return

        elif message["command"] == "turn_left":
            drone.turnLeft(message["angle"],message["rate"])
            conn.send(b'ACK')
            return

        elif message["command"] == "turn_right":
            drone.turnRight(message["angle"],message["rate"])
            conn.send(b'ACK')
            return

        elif message["command"] == "center":
            marker = markers[message["id"]]
            drone.center(marker[0],marker[1])
            conn.send(b'ACK')
            return

    # commands that can be berformed when not flying or armed
    if message["command"] == "arm":
        drone.arm()
        conn.send(b'ACK')
        return

    elif message["command"] == "set":
        goal = message["goal"]
        drone.setCoordinates(goal[0], goal[1], goal[2])
        conn.send(b'ACK')
        return

    conn.send(b'NOT ARMED')
    return


if __name__ == "__main__":
    s.bind(("127.0.0.1", int(sys.argv[1])))
    s.listen(1)

    # initialze markers

    signal.signal(signal.SIGINT, exit)
    drone.black_box.info("Drone simulator started.")

    conn, addr = s.accept()  # wait for a connection
    while 1:
        data = conn.recv(1024)     # recieve data with buffer of size 1024
        if not data:
            exit(1,1)
        perform_action(data, conn)
