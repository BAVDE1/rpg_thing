import pygame as pg
import time
import math


class SineShake:
    """ Used to shake the game screen using sine waves """
    def __init__(self):
        self.is_shaking = False

        self.shake_amp = 0
        self.shake_start = 0
        self.shake_end = 0

    def shake_screen(self, amp, secs):
        """ Set a shake.\n
            amp = amplitude """
        self.is_shaking = True
        self.shake_amp = amp

        self.shake_start = time.time()
        self.shake_end = time.time() + secs

    def get_value(self):
        """ Returns the current value that can be added to a variable """
        if self.is_shaking:
            percent = (time.time() - self.shake_start) / (self.shake_end - self.shake_start)
            if percent >= 1:
                self.is_shaking = False
                return 0

            return (self.shake_amp - self.shake_amp * percent) * math.sin((self.shake_amp * 2) * time.time())
        return 0


class ExponentialLerp:
    """ Used to exponentially lerp the screen to or from an addition.\n
        Can be set as a decay exponential (fast->slow rather than slow->fast). """
    def __init__(self):
        self.is_lerping = False
        self.is_lerping_from = False
        self.decay = False

        self.BASE = pg.Vector2(0, 0)
        self.lerp_to = pg.Vector2(0, 0)
        self.lerp_start = 0
        self.lerp_end = 0

    def lerp_screen(self, lerp_to: pg.Vector2, secs, lerping_from=False, decay=False):
        """ Set a lerp.\n
            Lerping_from takes away from the lerp_to over time.\n
            Decay makes exponential go from fast to slow. """
        self.is_lerping = True
        self.is_lerping_from = lerping_from
        self.decay = decay

        self.lerp_to = lerp_to
        self.lerp_start = time.time()
        self.lerp_end = time.time() + secs

    def get_value(self) -> pg.Vector2:
        """ Returns the current value that can be added to a variable """
        if self.is_lerping:
            percent = (time.time() - self.lerp_start) / (self.lerp_end - self.lerp_start)
            if percent >= 1:
                self.is_lerping = False
                return pg.Vector2(0, 0)

            if not self.is_lerping_from:
                amount = pg.Vector2(self.lerp_to.x - pow(self.lerp_to.x, 1-percent), self.lerp_to.y - pow(self.lerp_to.y, 1-percent))
            else:
                amount = pg.Vector2(pow(self.lerp_to.x, 1-percent), pow(self.lerp_to.y, 1-percent))
            return -amount if self.decay else amount
        return pg.Vector2(0, 0)

