import time


class Animator:
    def __init__(self, game, current_texture_obj, idle_ss, boomerang_idle=True, *one_time_ss):
        """ ss - sprite sheets - must be lists of two objects - [0]: CONSTANT, [1]: sprite sheet """
        self.game = game
        self.texture_obj = current_texture_obj

        self.idling = True
        self.idle_ss = idle_ss
        if not idle_ss[1]:
            idle_ss[1] = [None, None, None]  # DEBUGGING EXAMPLE until actual is ss working
            #raise IndexError(f"Error in loading '{idle_ss[0]}', idle sprite sheet '{idle_ss[1]}', something has gone wrong with creation of sprite sheet")
        self.idle_len = len(idle_ss[1]) - 1
        self.prev_idle_beat = game.song_start_time
        self.idle_prev_frame = 0
        self.idle_frame = 0
        self.bmrng_idle = boomerang_idle

        if one_time_ss:
            self.one_time_ss = {ss[0]: ss[1] for ss in one_time_ss if ss[0] and ss[1]}
        self.animation_queue = []
        self.currently_animating = None
        self.current_anim_frame = None

    def update(self):
        """ Should be called every frame """
        if self.idling:
            if time.time() > self.prev_idle_beat + ((60 / self.game.bpm) / self.idle_len):  # 60 secs in a min
                self.advance_idle_animation_frame()
                # set current sprite (based on idle_frame) here
        else:
            # one time animations here
            self.finish_animating()

    def advance_idle_animation_frame(self):
        im_frame = self.idle_frame

        if self.idle_prev_frame < self.idle_frame < self.idle_len or self.idle_frame == 0:
            self.idle_frame += 1
        elif self.idle_frame == self.idle_len:
            self.idle_frame = 0 if not self.bmrng_idle else self.idle_frame - 1
        elif self.idle_prev_frame > self.idle_frame != 0:
            self.idle_frame -= 1

        self.idle_prev_frame = im_frame
        self.prev_idle_beat = time.time()

    def do_animation(self, anim):
        if self.one_time_ss:
            if anim not in self.one_time_ss:
                raise IndexError(f"The animation {anim} does not exist in animation dict: {self.one_time_ss}")

            if self.currently_animating:
                self.animation_queue.append(anim)
            else:
                self.idling = False
                # do stuff here
        else:
            raise IndexError(f"Cannot animate {anim} because there are no animations registered. Was the Animator, and the one_time_ss args initialised properly?")

    def finish_animating(self):
        if len(self.animation_queue) == 0:
            self.currently_animating = None
            self.idling = True
        else:
            self.currently_animating = None
            self.do_animation(self.animation_queue[0])
            self.animation_queue.pop(0)
