# https://github.com/websocket-client/websocket-client
import sys
import stomper
import websocket



try:
    import thread
except ImportError:
    import _thread as thread


sys.path.append(sys.path[0] + "/..")

import argparse, time
import subprocess
from Common.SocketCallback import SocketCallback
import signal, sys, json, requests, random
from DroneSimCore.ServerMessage import ServerMessage
from DroneSimCore.WorkerMessage import WorkerMessage
from DroneSimCore.WorkerJob import WorkerJob

drones = {}
marker_ids = []
logonMessage = '{"workerID" : "0","workerType" : "2","status" : "1","botamount" : "0"}'  # "workerID:0\nworkerType:2\nstatus:1\nbotamount:0"#
workerID = 0


def create(id):
    global drones
    print("Create drone.")
    # append id in list
    if id in drones:
        return b'NACK\n'
    else:
        # dictionary key (drone id_ value( marker, simProcess, controllerProcess)
        drones[id] = [-1, None, None]
        return b'ACK\n'


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
    try:
        #local:
        simProcess = subprocess.Popen(["python3", "../DroneSim/DroneSimulator.py", str(simport), "auto_arm"])
        #docker:
        #simProcess = subprocess.Popen(["python3", "./DroneSim/DroneSimulator.py", str(simport), "auto_arm"])
        drones[id][1] = simProcess
        #local:
        controlProcess = subprocess.Popen(
            ["python3", "../DroneCore/Controller.py", str(simport), str(start_marker_id), str(backendIP)])
        #drone:
        #controlProcess = subprocess.Popen(
         #       ["python3", "./DroneCore/Controller.py", str(simport), str(start_marker_id), str(backendIP)])
        drones[id][2] = controlProcess
        return b'ACK\n'
    except:
        return b'NACK\n'


def stop(id):
    global drones
    print("Stop drone.")
    # stop simulated
    if id in drones:
        simprocess = drones[id][1]
        controlProcess = drones[id][2]
        if simprocess is None and controlProcess is None:
            print("no process to kill")
            return b'NACK\n'
        else:
            try:
                if sys.platform == 'win32':
                    # TODO fix windows
                    print("cannot stop this program when running on windows")
                    return b'NACK\n'
                else:
                    simprocess.send_signal(signal.SIGINT)
                    controlProcess.send_signal(signal.SIGINT)
            except:
                return b'NACK\n'
        return b'ACK\n'
    else:
        return b'NACK\n'


def kill(id):
    global drones
    print("Kill drone.")
    # remove id from list
    if id in drones:
        drones.pop(id)
        return b'ACK\n'
    else:
        return b'NACK\n'


def restart(id):
    answer = run(id)
    return answer


def set_startpoint(id, startpoint):
    # set id startpoint value
    global drones
    print("set_startpoint")
    # check if startpoint is int
    try:
        startpoint = int(startpoint)
        # check if startpoint exist in markers
        if startpoint not in marker_ids:
            return b'NACK\n'
    except:
        # startpoint is auto, chose a random value
        startpoint = random.choice(marker_ids)

    if id in drones:
        drones[id][0] = startpoint
        return b'ACK\n'
    else:
        return b'NACK\n'


def ping():
    return b'PONG\n'


def set_markers():
    global marker_ids
    url = "http://" + backendIP + ":8082/getMarkers/"
    markers = json.loads(requests.get(url).text)['markers']
    for m in markers.values():
        marker_ids.append(m['id'])


def connecting(ID, arg):
    global workerID
    if (workerID == 0):
        print("received worker id %f" % ID)
        workerID = ID
    elif (arg == 'SHUTDOWN'):
        print("shutting down")
        exit()


def handle_webCommand(message, ws):
    try:
        ID = message.botID
        switcher = {
            WorkerJob.CONNECTION: lambda: connecting(message.workerID, message.arguments),
            WorkerJob.BOT: lambda: create(ID),
            WorkerJob.START: lambda: run(ID),
            WorkerJob.STOP: lambda: stop(ID),
            WorkerJob.KILL: lambda: kill(ID),
            WorkerJob.RESTART: lambda: restart(ID),
            WorkerJob.SET: lambda: set_startpoint(ID, message.arguments)
        }
        if (workerID == message.workerID or message.job == WorkerJob.CONNECTION):
            func = switcher.get(message.job, lambda: "Invalid Command")
            func()
            ackMessage = '{"workerID": "%d","job": "%d","botID":"%d","arguments":"OK"}' % (
            workerID, message.job.value, message.botID)
            if (message.job != WorkerJob.CONNECTION):
                ws.send(stomper.send("/SimCity/Robot/topic/answers", ackMessage, transactionid=None,
                                     content_type='application/json;charset=UTF-8'))
                print("Reply ack sent")
    except:
        nackMessage = '{"workerID": "%d","job":"%d","botID":"%d","arguments":"NOK"}' % (
        workerID, message.job.value, message.botID)
        if (workerID == message.workerID):
            if (message.job != WorkerJob.CONNECTION):
                ws.send(stomper.send("/SimCity/Robot/topic/answers", nackMessage, transactionid=None,
                                     content_type='application/json;charset=UTF-8'))
                print("Reply nack sent")

#depricated (TCP => now  uses websockets see handle_webCommand)
def handle_command(sock, data):
    try:
        data = data.decode()
        words = data.split()
        if len(words) == 1:
            # case that data = ping
            function_name = words[0]
            func = globals()[function_name]
            answer = func()
        elif len(words) == 2 and words[1].isdigit():
            # case data is create, run, stop, kill , restart with id
            function_name = words[0]
            func = globals()[function_name]
            answer = func(words[1])
        elif len(words) == 4 and words[1].isdigit():
            # case data is set id startpoint value
            answer = set_startpoint(words[1], words[3])
        else:
            answer = b'NACK\n'

        sock.send(answer)
    except:
        answer = b'NACK\n'
        sock.send(answer)

    print(answer)


def exit():
    global running, command_socket
    running = False
    #command_socket.close()
    #command_socket.join()


# Possible usage for callback instead of while loop for websockets
# def on_message(ws, message):
#      print("job %f" %message.job)
# def on_error(ws, error):
#     print(error)
#
# def on_close(ws):
#     print("### closed ###")
#
#def on_open(ws):
#    print("connected")

    def run(*args):
        ws.send(stomper.send("/SimCity/worker/Robot", logonMessage))
        time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
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

    set_markers()

    print("simulationCore started. Send TCP/ip packet at ", ip, ":", port)
    print("create id: adds drone to the list")
    print("run id: starts simulated drone")
    print("stop id: stops simulated drone, works only on linux")
    print("kill id: removes drone from the list")
    print("set_startpoint id startpoint: change startpoint from drone")
    websocket.enableTrace(True)
    # Possible callback system instead of while loop?
    # See for more info: https://pypi.org/project/websocket_client/
    # ws = websocket.WebSocketApp("ws://localhost:1394/droneworker/",
    #                             on_message=on_message,
    #                             on_error=on_error,
    #                             on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever()
    # local:
    ws = websocket.create_connection("ws://localhost:1394/droneworker")
    # docker:
    #ws = websocket.create_connection("ws://172.10.0.4:8080/droneworker")
    v = str(random.randint(0, 1000))
    sub1 = stomper.subscribe("/user/queue/worker", v, ack='auto')
    sub2 = stomper.subscribe("/topic/messages", v, ack='auto')
    sub3 = stomper.subscribe("/topic/shutdown", v, ack='auto')
    logon = stomper.send("/SimCity/worker/Robot", logonMessage, transactionid=None,
                         content_type='application/json;charset=UTF-8')
    ws.send(sub1)
    ws.send(sub2)
    ws.send(sub3)
    p = WorkerMessage().creatWorkerMessage(0, 2, 1, 0)
    ws.send(logon)
    running = True
    while running:
        d = ws.recv()
        m = ServerMessage(d)
        if(m.workerID == workerID or m.job == WorkerJob.CONNECTION):
            if(workerID == 0 or m.workerID == workerID):
                print("job = " + m.job.name + " workerID = %f" %m.workerID)
                handle_webCommand(m, ws)
    # TCP CODE
    # command_socket = SocketCallback(ip, port)
    # command_socket.add_callback(handle_command)
    # command_socket.start()
    #
    # running = True
    # while running: time.sleep(1)
