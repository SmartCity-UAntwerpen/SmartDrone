import logging
#import graypy

def create_logger():
    logger = logging.getLogger("Drone Process")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [DRONE_PROCESS] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler("drone_log.txt")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)


    #Graylog logger
    #handler = graypy.GELFUDPHandler('172.10.0.5', 12201)
    #logger.addHandler(handler)

    return logger
