
import Drone, socket, signal, sys, json

drone = Drone.Drone()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def exit(signal, frame):
    print("Closing socket...")
    s.close()
    # land drone?
    print("Simulator tured off.")
    sys.exit(0)

def perform_action(command):
    """ Expecting a json message structered as followes:
        {
            "command": ex. "move" or "turn",
            "pos": (x,y,z),
            "velocity": velocity
            "angle": angle          # angle not always necessary, only if the command is turn
        }
    """
    message = json.loads(command.decode())
    if message["command"] == "move":
        goal = message["pos"]
        drone.moveDistance(goal[0],goal[1],goal[2],message["velocity"])
    elif message["command"] == "arm":
        drone.arm()
    elif message["command"] == "takeoff":
        drone.takeOff(0.4, message["velocity"])


if __name__ == "__main__":
     s.bind(("127.0.0.1", 9000))
     s.listen(1)

     signal.signal(signal.SIGINT, exit)
     conn, addr = s.accept()  # wait for a connection
     data = '123'
     while len(data):
         data = conn.recv(1024)     # recieve data with buffer of size 1024
         if not data:
             exit(1,1)
         perform_action(data)
