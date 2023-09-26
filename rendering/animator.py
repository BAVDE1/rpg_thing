from constants import *
from conductor.conductor import Conductor
from rendering.sprites_holder import SpriteSheet
import time

idle_error = "Error in loading '{}' idle sprite sheet.\n Something has gone wrong with creation of sprite sheet, or sheet was not added to list."
missing_anim_error = "The animation {} does not exist in animation dict: {}"
no_anim_error = "Cannot animate '{}' because there are no animations registered. Was the Animator, or the one_time_ss args initialised properly?"


class Animator:
    def __init__(self, logger, conductor: Conductor, idle_offset: pg.Vector2, idle_ss: SpriteSheet, *one_time_ss: SpriteSheet):
        self.logger = logger
        self.conductor = conductor
        self.texture_obj = None
        self.has_changed_texture = False  # updates to true on texture change (and should be back to false within the frame)

        self.idling = True
        self.idle_ss = idle_ss
        self.default_idle_ss = idle_ss
        try:
            self.idle_len = idle_ss.length - 1
        except IndexError:
            raise IndexError(idle_error.format(idle_ss.identifier))
        self.prev_idle_start = time.time()
        self.idle_frame_prev = -1
        self.idle_frame = 0

        self.one_time_ss = {}
        if one_time_ss:
            self.one_time_ss = {ss.identifier: ss.sprite_sheet for ss in one_time_ss}

        self.current_one_time_anim = ""
        self.current_ot_anim_ss = None
        self.ot_current_anim_frame = None
        self.ot_anim_frame_speed = None
        self.last_ot_anim_frame_time = None

        self.idle_offset = idle_offset
        self.offset = idle_offset

        self.update()  # init

    def on_shadow_beat(self):
        """ Called on the perfect beat """
        self.restart_idle()
        self.prev_idle_start = self.conductor.prev_shadow_beat_time

    def change_idle_anim(self, set_to_default, new_idle_ss: SpriteSheet | None = None):
        """ Used to change the current idle animation to another animation. The default idle animation is saved and can be restored later. """
        if set_to_default and self.idle_ss != self.default_idle_ss:
            self.idle_ss = self.default_idle_ss
            self.restart_idle()
        elif new_idle_ss and self.idle_ss != new_idle_ss:
            self.idle_ss = new_idle_ss
            self.restart_idle()

    def restart_idle(self):
        try:
            self.idle_len = self.idle_ss.length - 1
        except IndexError:
            raise IndexError(idle_error.format(self.idle_ss.identifier))
        self.idle_frame_prev = -1
        self.idle_frame = 0

    def update(self):
        """ Should be called every frame """
        if self.idling:  # idle
            next_idle_frame_time = self.prev_idle_start + self.conductor.sec_per_beat * (self.idle_frame / (self.idle_len + 1))
            if time.time() >= next_idle_frame_time and self.idle_frame != self.idle_frame_prev:  # time more than when next idle frame should tick
                # reset offset (changed because of a one time anim)
                if self.offset != self.idle_offset:
                    self.offset = self.idle_offset

                self.texture_obj = self.idle_ss.sprite_sheet[self.idle_frame]  # set image
                self.advance_idle_animation_frame()
                # self.logger.add_log(f"{self.idle_frame_prev}, (next: {self.idle_frame})")

                self.has_changed_texture = True

        elif self.current_ot_anim_ss:  # one time anim
            next_ot_frame_time = self.last_ot_anim_frame_time + self.ot_anim_frame_speed
            if time.time() > next_ot_frame_time:
                self.advance_one_time_anim_frame()
                if self.current_ot_anim_ss:  # check incase animation finished in the advance
                    self.texture_obj = self.current_ot_anim_ss[self.ot_current_anim_frame]  # set image

                    self.has_changed_texture = True

    def advance_idle_animation_frame(self):
        self.idle_frame_prev = self.idle_frame
        self.idle_frame += 1 if self.idle_frame < self.idle_len else 0

    def advance_one_time_anim_frame(self):
        self.ot_current_anim_frame += 1
        if self.ot_current_anim_frame == len(self.current_ot_anim_ss):
            self.finish_animating()
        else:
            self.last_ot_anim_frame_time = time.time()

    def do_animation(self, anim, duration, offset: pg.Vector2 = pg.Vector2(0, 0), reverse=False):
        """ Call to execute a registered animation (does not loop) """
        if self.one_time_ss:
            if anim not in self.one_time_ss:
                raise IndexError(missing_anim_error.format(anim, self.one_time_ss))

            # do animation
            if not self.current_one_time_anim:
                anim_ss = self.one_time_ss[anim]

                # flip animation
                if reverse:
                    anim_ss = anim_ss[::-1]

                self.current_one_time_anim = anim
                self.idling = False
                self.current_ot_anim_ss = anim_ss
                self.ot_current_anim_frame = 0
                self.ot_anim_frame_speed = duration / len(self.current_ot_anim_ss)
                self.last_ot_anim_frame_time = time.time()
                self.texture_obj = self.current_ot_anim_ss[self.ot_current_anim_frame]  # set one time anim image

                self.offset = offset

                self.has_changed_texture = True
        else:
            raise IndexError(no_anim_error.format(anim))

    def finish_animating(self):
        self.current_one_time_anim = ""
        self.current_ot_anim_ss = None
        self.ot_current_anim_frame = None
        self.ot_anim_frame_speed = None
        self.last_ot_anim_frame_time = None
        self.idling = True
