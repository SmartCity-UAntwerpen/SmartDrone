import logging
import graphy


def create_logger():
    logger = logging.getLogger("Black Box")
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - [DRONE_CORE] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fileHandler = logging.FileHandler("core_log.txt")
    fileFormatter = logging.Formatter('%(asctime)s - [DRONE_CORE] %(levelname)s - %(funcName)s - %(message)s')
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)

    #Graylog logger
    handler = graphy.GELFUDPHandler('172.10.0.5', 12201)
    logger.addHandler(handler)

    return logger


logger = create_logger()
