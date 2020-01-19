import logging
import graypy

class logFilter(logging.Filter):
        def __init__(self):
                self.origin = 'Drone Backend'
                self.vehicleType = 'Drone'
        
        def filter(self, record):
            record.origin = self.origin
            record.vehicleType = self.vehicleType
            return True

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
    grayHandler = graypy.GELFUDPHandler('172.10.0.5', 12201)
    grayFormatter = logging.Formatter('%(message)s')
    grayHandler.setFormatter(grayFormatter)
    grayHandler.setLevel(logging.WARN)
    logger.addHandler(grayHandler)
    logger.addFilter(logFilter())
    
    return logger


logger = create_logger()
