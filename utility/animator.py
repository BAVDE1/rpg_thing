import time

idle_error = "Error in loading '{}' idle sprite sheet.\n Something has gone wrong with creation of sprite sheet, or sheet was not added to list."
missing_anim_error = "The animation {} does not exist in animation dict: {}"
no_anim_error = "Cannot animate '{}' because there are no animations registered. Was the Animator, or the one_time_ss args initialised properly?"


class Animator:
    def __init__(self, game, idle_ss, boomerang_idle=False, *one_time_ss):
        """ ss - sprite sheets - must be lists of two objects - [0]: CONSTANT, [1]: sprite sheet """
        self.game = game
        self.texture_obj = None

        self.idling = True
        self.idle_ss = idle_ss
        self.default_idle_ss = idle_ss
        try:
            self.idle_len = len(idle_ss[1]) - 1
        except IndexError:
            raise IndexError(idle_error.format(idle_ss[0]))
        self.prev_idle_beat = game.song_start_time
        self.idle_prev_frame = 0
        self.idle_frame = 0
        self.bmrng_idle = boomerang_idle

        self.one_time_ss = None
        if one_time_ss:
            self.one_time_ss = {ss[0]: ss[1] for ss in one_time_ss if ss[0] and ss[1]}
        self.animation_queue = {}
        self.current_anim_ss = None
        self.current_anim_frame = None
        self.anim_frame_speed = None
        self.last_anim_frame_time = None

        self.update()  # init

    def change_idle_anim(self, set_to_default, new_idle_ss=None, boomerang_idle=False):
        """ Used to change the current idle animation to another animation. The default idle animation is saved and can be restored later. """
        if set_to_default and self.idle_ss[0] != self.default_idle_ss[0]:
            self.idle_ss = self.default_idle_ss
            self.restart_idle()
        elif new_idle_ss and self.idle_ss[0] != new_idle_ss[0]:
            self.bmrng_idle = boomerang_idle
            self.idle_ss = new_idle_ss
            self.restart_idle()

    def restart_idle(self):
        try:
            self.idle_len = len(self.idle_ss[1]) - 1
        except IndexError:
            raise IndexError(idle_error.format(self.idle_ss[0]))
        self.idle_prev_frame = 0
        self.idle_frame = 0

    def update(self):
        """ Should be called every frame """
        if self.idling:
            if time.time() > self.prev_idle_beat + ((60 / self.game.bpm) / self.idle_len):  # 60 secs
                self.advance_idle_animation_frame()
                self.texture_obj = self.idle_ss[1][self.idle_frame]  # set idle image
        elif self.current_anim_ss:
            if time.time() > self.last_anim_frame_time + self.anim_frame_speed:
                print(self.current_anim_frame)
                self.texture_obj = self.current_anim_ss[1][self.current_anim_frame]  # set one time anim image
                self.advance_one_time_anim_frame()

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

    def advance_one_time_anim_frame(self):
        self.current_anim_frame += 1
        if self.current_anim_frame < len(self.current_anim_ss[1]):
            self.last_anim_frame_time = time.time()
        else:
            self.finish_animating()

    def do_animation(self, anim, duration):
        """ Call to execute a registered animation (does not loop) """
        if self.one_time_ss:
            if anim not in self.one_time_ss:
                raise IndexError(missing_anim_error.format(anim, self.one_time_ss))

            if not self.current_anim_ss:
                self.idling = False
                self.current_anim_ss = [anim, self.one_time_ss[anim]]
                self.current_anim_frame = 0
                self.anim_frame_speed = duration / len(self.current_anim_ss[1])
                self.last_anim_frame_time = time.time()
            else:
                self.animation_queue[anim] = duration  # add item to queue
        else:
            raise IndexError(no_anim_error.format(anim))

    def finish_animating(self):
        if len(self.animation_queue) == 0:
            self.current_anim_ss = None
            self.current_anim_frame = None
            self.anim_frame_speed = None
            self.last_anim_frame_time = None
            self.idling = True
        else:
            self.current_anim_ss = None
            first_key = list(self.animation_queue.keys())[0]
            self.do_animation(first_key, self.animation_queue[first_key])  # play next animation in queue & remove
            self.animation_queue.pop(first_key)
