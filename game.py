import math
import random
import time

import pygame as pg

import rendering.render_handler as renderer
from conductor.conductor import Conductor
from constants import GameUnits, DirectionalValues
from entity.player import Player
from level.area import Area
from rendering.split_sheet import split_sheet
from rendering.sprites_holder import SpriteSheet
from texture_constants import PlayerTextures
from utility.interpolators import SineShake, ExponentialLerp
from utility.logging import Logger
from utility.text_object import TextObjectsHolder


class GameStates:
    IN_MAIN_MENU = "in_menu"

    IN_LEVEL = "in_level"
    IN_INVENTORY = "in_inventory"
    IS_PAUSED = "is_paused"


class Game:
    def __init__(self):
        self.final_screen = pg.display.get_surface()
        self.screen_canvas = pg.surface.Surface((GameUnits.RES_W, GameUnits.RES_H))

        self.clock = pg.time.Clock()
        self.fps = 60  # 500 cap
        self.running = True
        self.dev_mode = True

        self.keys = pg.key.get_pressed()

        self.game_state = GameStates.IN_LEVEL  # for now

        # set after requirements
        self.logger = Logger(self, self.final_screen)
        self.text_objects_holder = TextObjectsHolder(self.screen_canvas)

        self.conductor = Conductor(self, self.logger)  # before entities
        self.area = Area(self, "overworld")

        self.player = Player(self)

        # screen movers
        self.screen_shaker = SineShake()
        self.screen_lerper = ExponentialLerp()

    def events(self):
        """ For events in event queue """
        for event in pg.event.get():
            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

            # keydown input
            if event.type == pg.KEYDOWN:
                # update keys first
                self.keys = pg.key.get_pressed()

                self.player.on_key_down(event.key)

                if self.dev_mode:
                    self.developer_hotkeys()

            # keyup input
            if event.type == pg.KEYUP:
                # update keys first
                self.keys = pg.key.get_pressed()

                self.player.on_key_up(event.key)

    def developer_hotkeys(self):
        """ Called when dev_mode is active and a key is pressed / released """
        # zx: screen movement
        if self.keys[pg.K_z]:
            self.screen_shaker.set_shake((5 * GameUnits.RES_MUL), 0.3)
            self.logger.add_log(f"Shake screen, amp: {self.screen_shaker.shake_amp}", 2)
        if self.keys[pg.K_x]:
            self.screen_lerper.set_lerp(pg.Vector2((5 * GameUnits.RES_MUL), 0), 0.3, True)
            self.logger.add_log(f"Lerp screen, amp: {self.screen_lerper.lerp_to}", 2)

        # 1234: switch level (n, s, e, w)
        if self.keys[pg.K_1]:
            self.area.change_level_by_direction(DirectionalValues.NORTH)
        if self.keys[pg.K_2]:
            self.area.change_level_by_direction(DirectionalValues.SOUTH)
        if self.keys[pg.K_3]:
            self.area.change_level_by_direction(DirectionalValues.EAST)
        if self.keys[pg.K_4]:
            self.area.change_level_by_direction(DirectionalValues.WEST)

        # v: text object
        if self.keys[pg.K_v]:
            self.text_objects_holder.add_text_object("abcdefghijklmnopqrstuvwxyz 1234567890",
                                                     pg.Vector2(self.player.position.x, self.player.position.y - 23))

        # c: toggle combat
        if self.keys[pg.K_c]:
            self.conductor.is_in_combat = not self.conductor.is_in_combat
            self.logger.add_log(f"Combat enabled: {self.conductor.is_in_combat}")

        # b: change bpm
        if self.keys[pg.K_b]:
            bpm = self.conductor.bpm
            bpm = 60 if bpm == 120 else 120 if bpm > 120 else 180
            # self.conductor.set_bpm(bpm)  todo: broken atm
            self.logger.add_log(f"bpm = {self.conductor.bpm}")

        # mn: set & reset idle animation
        if self.keys[pg.K_m]:
            texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE_DEBUG).convert_alpha()
            ss_idle = split_sheet(texture_idle, (GameUnits.UNIT, GameUnits.UNIT), 4)
            self.player.animator.change_idle_anim(set_to_default=False,
                                                  new_idle_ss=SpriteSheet(PlayerTextures.PLAYER_IDLE_DEBUG, ss_idle))
            self.logger.add_log("Debug idle: enabled")
        if self.keys[pg.K_n]:  # reset
            self.player.animator.change_idle_anim(set_to_default=True)
            self.logger.add_log("Debug idle: disabled")

    def functionality(self):
        self.player.sprint_manager()

        # conductor
        self.conductor.update()

    def on_level_fully_loaded(self):
        """ Called once the level and entities are fully loaded """
        self.logger.add_log(f"level loaded")

        self.conductor.set_music("placeholder", "placeholder", 120)
        self.conductor.start_conducting()

    def on_shadow_beat(self):
        """ Called when the conductor sends a perfect beat """
        self.player.on_shadow_beat()

    def on_beat(self, is_auto_beat):
        """ Called on the actual beat """
        if is_auto_beat:
            self.player.miss_next_beat = False  # reset

    def on_level_change(self, direction):
        """ Called right after the level gets changed. \n
            Direction is the where the switched level was before it was changed to; 'NORTH', 'EAST', etc. """

    def render(self):
        fill_col = (0, 5, 5)
        self.final_screen.fill(fill_col)
        self.screen_canvas.fill(fill_col)

        if self.game_state == GameStates.IN_LEVEL:
            renderer.render_active_level(self, self.screen_canvas, self.player, self.area, self.text_objects_holder)

        # scale to proper resolution
        pos = pg.Vector2(0, 0 + self.screen_shaker.get_value()) + self.screen_lerper.get_value()
        scaled = pg.transform.scale(self.screen_canvas, (GameUnits.RES_W * GameUnits.RES_MUL, GameUnits.RES_H * GameUnits.RES_MUL))
        self.final_screen.blit(scaled, pos)

        # only works in dev_mode
        self.logger.render_logs()

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("{} - FPS: {:.2f}".format(GameUnits.CAPTION, self.clock.get_fps()))
