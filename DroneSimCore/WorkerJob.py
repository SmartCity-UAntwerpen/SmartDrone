from enum import Enum


class WorkerJob(Enum):
    CONNECTION = 0
    BOT = 1
    START = 2
    KILL = 3
    STOP = 4
    RESTART = 5
    SET = 6
