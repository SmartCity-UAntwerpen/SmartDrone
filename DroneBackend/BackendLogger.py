import logging

def create_logger():
    logger = logging.getLogger("DRONE BACKEND")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [DRONE_BACKEND] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    return logger


logger = create_logger()