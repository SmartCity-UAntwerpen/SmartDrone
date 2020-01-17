class WorkerMessage(object):
    def __add__(self, workerID,workerType,status,botAmount):
        self.workerID = workerID
        self.workerType = workerType
        self.status = status
        self.botAmount = botAmount

    def readWorkerkMessage(self, msg):
        SimWorkerType = enumerate(["car", "f1", "Drone"])
        self.msg = msg
        sp = self.msg.split("\n")
        self.workerID = sp[1].split(":")[1]
        self.workerType = SimWorkerType(sp[2].split(":")[1])
        self.status = sp[3].split(":")[1]
        self.botAmount = sp[4].split(":")[1]

    def creatWorkerMessage(self, workerID,workerType,status,botAmount):
        self.workerID = workerID
        self.workerType = workerType
        self.status = status
        self.botAmount = botAmount