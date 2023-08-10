import time


class Animator:
    def __init__(self, game, current_texture_obj, idle_ss, boomerang_idle=True, *one_time_ss):
        """ ss - sprite sheets - must be lists of two objects - [0]: CONSTANT, [1]: sprite sheet """
        self.game = game
        self.prev_idle_beat = None

        self.texture_obj = current_texture_obj
        self.idle_ss = idle_ss
        if not idle_ss[1]:
            idle_ss[1] = [None, None, None]  # DEBUGGING PURPOSES
            #raise IndexError(f"Error in loading '{idle_ss[0]}' idle sprite sheet, something has gone wrong creation of sprite sheet")
        self.idle_len = len(self.idle_ss[1]) - 1
        self.idle_prev_frame = 0
        self.idle_frame = 0
        self.bmrng_idle = boomerang_idle

        if one_time_ss:
            self.one_time_ss = {ss[0]: ss[1] for ss in one_time_ss if ss[0] and ss[1]}

        self.idling = True
        self.currently_animating = None
        self.current_anim_frame = None

    def update(self):
        """ Should be called every frame """
        if not self.prev_idle_beat:
            self.prev_idle_beat = time.time()  # init

        if self.idling:
            if time.time() > self.prev_idle_beat + (60 / self.game.bpm):  # 60 secs in a min
                self.advance_idle_animation_frame()
                # set current sprite (based on idle_frame) here
        else:
            # one time animations here
            self.finish_animating()

    def advance_idle_animation_frame(self):
        immutable_frame = self.idle_frame

        if self.idle_prev_frame < self.idle_frame < self.idle_len or self.idle_frame == 0:
            self.idle_frame += 1
        elif self.idle_frame == self.idle_len:
            self.idle_frame = 0 if not self.bmrng_idle else self.idle_frame - 1
        elif self.idle_prev_frame > self.idle_frame != 0:
            self.idle_frame -= 1

        self.idle_prev_frame = immutable_frame
        self.prev_idle_beat = time.time()

    def do_animation(self, anim):
        if self.one_time_ss:
            if anim not in self.one_time_ss:
                raise IndexError(f"The animation {anim} does not exist in animation dict: {self.one_time_ss}")
            self.idling = False
            # do stuff here
        else:
            raise IndexError(f"Cannot animate {anim} because there are no animations registered. Was the Animator not initialised properly?")

    def finish_animating(self):
        self.currently_animating = None
        self.idling = True
