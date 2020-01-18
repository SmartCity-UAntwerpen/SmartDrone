import logging
import graypy


def create_logger():
    logger = logging.getLogger("DRONE BACKEND")
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - [DRONE_BACKEND] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fileHandler = logging.FileHandler("backend_log.txt")
    fileFormatter = logging.Formatter('%(asctime)s - [BACKEND] %(levelname)s - %(funcName)s - %(message)s')
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)

    #GrayLog logger
    graylogger = logging.getLogger("DRONE BACKEND")
    ch2 = logging.StreamHandler()
    ch2.setLevel(logging.WARN)
    formatter2 = logging.Formatter('%(asctime)s - [DRONE_BACKEND] %(levelname)s - %(message)s')
    ch2.setFormatter(formatter2)
    graylogger.addHandler(ch)
    grayloghandler = graypy.GELFUDPHandler('172.10.0.5', 12201)
    graylogger.addHandler(grayloghandler)

    return logger


logger = create_logger()
