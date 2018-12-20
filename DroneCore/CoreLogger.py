import logging

def create_logger():
    logger = logging.getLogger("Black Box")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [DRONE_CORE] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fileHandler = logging.FileHandler("core_log.txt")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = create_logger()
