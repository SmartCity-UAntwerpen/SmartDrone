import json

from DroneSimCore.WorkerJob import WorkerJob


class ServerMessage(object):

    def __init__(self, msg):
        # jobs = {
        #     "CONNECTION": 0,
        #     "BOT": 1,
        #     "START": 2,
        #     "KILL": 3,
        #     "STOP": 4,
        #     "RESTART": 5,
        #     "SET": 6
        # }
        self.msg = msg
        fullMessage = self.msg.split("\n")
        bodyplace = len(fullMessage)-1
        #temp = fullMessage[bodyplace]
        body = json.loads(fullMessage[bodyplace].rstrip('\x00'))
        self.workerID = body["workerID"]
        self.job = WorkerJob[body["job"]] #jobs[body["job"]]
        self.botID = body["botID"]
        self.arguments = body["arguments"]
