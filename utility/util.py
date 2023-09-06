from constants import DirectionalValues
import time


def is_direction_opposite(dir_a, dir_b):
    """ Returns whether directions given are opposites of each other """
    return True if DirectionalValues.OPP_DIR[dir_a] == dir_b else False


def time_it(f):
    """ Decorator that times how long its function takes """
    def new_func(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()

        diff = end - start
        print(f"Function '{f.__name__}' took '{diff:.16f}' to run")
        return diff

    return new_func
