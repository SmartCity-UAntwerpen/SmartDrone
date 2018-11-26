import logging

def create_black_box():
    black_box = logging.getLogger("Black Box")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [DRONE_SIM] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    black_box.addHandler(ch)
    black_box.setLevel(logging.DEBUG)
    return black_box
