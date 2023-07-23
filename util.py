from constants import *


def is_direction_opposite(dir_a, dir_b):
    """ Returns whether directions given are opposites of each other """
    return True if OPP_DIR[dir_a] == dir_b else False
