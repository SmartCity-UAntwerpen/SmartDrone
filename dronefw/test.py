import logging
import time
import sys
import signal

import signal
from functools import partial

def main_function():
    list = {'aborted':0}
    def signal_handler(signal, frame):
        if (list['aborted']==0):
            list['aborted'] = 1
            print('CTRL-C: auto land!')
            time.sleep(30)
            exit(0)
        if (list['aborted']==1):
            print('CTRL-C: abort abort abort!')
            time.sleep(1)
            exit(0)
    signal.signal(signal.SIGINT,signal_handler)

    for a in range(30):
        time.sleep(0.5)
        print ('sleep')


if __name__ == '__main__':
    main_function()