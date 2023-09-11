from constants import *
import time

idle_error = "Error in loading '{}' idle sprite sheet.\n Something has gone wrong with creation of sprite sheet, or sheet was not added to list."
missing_anim_error = "The animation {} does not exist in animation dict: {}"
no_anim_error = "Cannot animate '{}' because there are no animations registered. Was the Animator, or the one_time_ss args initialised properly?"


class Animator:
    def __init__(self, game, idle_ss, idle_offset: pg.Vector2, boomerang_idle=False, *one_time_ss):
        """ ss - sprite sheets - must be lists of two objects - [0]: CONSTANT, [1]: sprite sheet """
        self.game = game
        self.texture_obj = None
        self.has_changed_texture = False  # updates to true on texture change (and should be back to false within the frame)

        self.idling = True
        self.idle_ss = idle_ss
        self.default_idle_ss = idle_ss
        try:
            self.idle_len = len(idle_ss[1]) - 1
        except IndexError:
            raise IndexError(idle_error.format(idle_ss[0]))
        self.prev_idle_beat = time.time()
        self.idle_prev_frame = 0
        self.idle_frame = 0
        self.bmrng_idle = boomerang_idle

        self.one_time_ss = None
        if one_time_ss:
            self.one_time_ss = {ss[0]: ss[1] for ss in one_time_ss if ss[0] and ss[1]}

        self.current_one_time_anim = ""
        self.current_anim_ss = None
        self.current_anim_frame = None
        self.anim_frame_speed = None
        self.last_anim_frame_time = None

        self.idle_offset = idle_offset
        self.offset = idle_offset

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
        if self.idling:  # idle
            if time.time() > self.prev_idle_beat + ((60 / self.game.bpm) / self.idle_len):  # 60 secs
                if self.offset != self.idle_offset:
                    self.offset = self.idle_offset

                self.advance_idle_animation_frame()
                self.texture_obj = self.idle_ss[1][self.idle_frame]  # set image

                self.has_changed_texture = True

        elif self.current_anim_ss:  # one time anim
            if time.time() > self.last_anim_frame_time + self.anim_frame_speed:
                self.advance_one_time_anim_frame()
                if self.current_anim_ss:  # check incase animation finished in the advance
                    self.texture_obj = self.current_anim_ss[self.current_anim_frame]  # set image

                    self.has_changed_texture = True

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
        if self.current_anim_frame == len(self.current_anim_ss):
            self.finish_animating()
        else:
            self.last_anim_frame_time = time.time()

    def do_animation(self, anim, duration, offset: pg.Vector2 = pg.Vector2(0, 0), reverse=False):
        """ Call to execute a registered animation (does not loop) """
        if self.one_time_ss:
            if anim not in self.one_time_ss:
                raise IndexError(missing_anim_error.format(anim, self.one_time_ss))

            # do animation
            if not self.current_one_time_anim:
                anim_list = list(self.one_time_ss[anim])

                # flip animation
                if reverse:
                    anim_list = anim_list[::-1]

                self.current_one_time_anim = anim
                self.idling = False
                self.current_anim_ss = anim_list
                self.current_anim_frame = 0
                self.anim_frame_speed = duration / len(self.current_anim_ss)
                self.last_anim_frame_time = time.time()
                self.texture_obj = self.current_anim_ss[self.current_anim_frame]  # set one time anim image

                self.offset = offset

                self.has_changed_texture = True
        else:
            raise IndexError(no_anim_error.format(anim))

    def finish_animating(self):
        self.current_one_time_anim = ""
        self.current_anim_ss = None
        self.current_anim_frame = None
        self.anim_frame_speed = None
        self.last_anim_frame_time = None
        self.idling = True
