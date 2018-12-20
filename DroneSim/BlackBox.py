import logging

def create_black_box():
    black_box = logging.getLogger("Black Box")
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    formatter = logging.Formatter('%(asctime)s - [DRONE_SIM] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    black_box.addHandler(ch)
    black_box.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler("sim_log.txt")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    black_box.addHandler(fileHandler)
    return black_box
