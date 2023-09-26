import time
import pygame as pg
import rendering.render_handler as renderer

from constants import GameUnits, LevelLocations
from rendering.split_sheet import split_sheet
from rendering.sprites_holder import SpriteSheet
from utility.text_object import TextObjectsHolder
from texture_constants import PlayerTextures
from conductor.conductor import Conductor
from utility.logging import Logger
from entity.player import Player
from level.level import Level


class GameStates:
    IN_LEVEL = "in_level"


class Game:
    def __init__(self):
        self.final_screen = pg.display.get_surface()
        self.screen_canvas = pg.surface.Surface((GameUnits.RES_W, GameUnits.RES_H))

        self.clock = pg.time.Clock()
        self.fps = 60  # 500 cap
        self.running = True
        self.logger = Logger(self.final_screen)

        self.keys = pg.key.get_pressed()

        self.song_start_time = time.time()

        self.game_state = GameStates.IN_LEVEL

        # set after requirements
        self.conductor = Conductor(self, self.logger)  # before entities
        self.text_objects_holder = TextObjectsHolder(self.screen_canvas)

        self.player = Player(self, self.screen_canvas, self.screen_canvas.get_rect().center)
        self.level = Level(self.screen_canvas, LevelLocations.OVERWORLD_00, pos_offset=pg.Vector2(GameUnits.LEVEL_OFFSET, 0))

    def events(self):
        """ For events in event queue """
        for event in pg.event.get():
            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

            # player inputs
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()  # update keys

                self.player.on_key_down(event.key)

                # dev thingos
                if self.keys[pg.K_t]:
                    self.text_objects_holder.add_text_object("abcdefghijklmnopqrstuvwxyz", pg.Vector2(self.player.position.x, self.player.position.y - 23))

                if self.keys[pg.K_c]:
                    self.conductor.is_in_combat = not self.conductor.is_in_combat
                    self.logger.add_log(f"Combat enabled: {self.conductor.is_in_combat}")

                if self.keys[pg.K_p]:
                    bpm = self.conductor.bpm
                    bpm = 60 if bpm == 120 else 120 if bpm > 120 else 180
                    self.conductor.set_bpm(bpm)
                    self.logger.add_log(f"bpm = {bpm}")

                if self.keys[pg.K_m]:  # set idle anim
                    texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE_DEBUG).convert_alpha()
                    ss_idle = split_sheet(texture_idle, (GameUnits.UNIT, GameUnits.UNIT), 4)
                    self.player.animator.change_idle_anim(set_to_default=False, new_idle_ss=SpriteSheet(PlayerTextures.PLAYER_IDLE_DEBUG, ss_idle))
                    self.logger.add_log("Debug idle: enabled")

                if self.keys[pg.K_n]:  # reset idle anim
                    self.player.animator.change_idle_anim(set_to_default=True)
                    self.logger.add_log("Debug idle: disabled")
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()  # update keys
                self.player.on_key_up(event.key)

    def functionality(self):
        self.player.sprint_manager()

        # conductor
        self.conductor.update()

    def on_level_fully_loaded(self):
        """ Called (on frame) once the level and entities are fully loaded """
        self.logger.add_log(f"level loaded")

        self.conductor.set_music("ph", "ph", 120)
        self.conductor.start_conducting()

    def on_shadow_beat(self):
        """ Called when the conductor sends a perfect beat """
        self.player.on_shadow_beat()

    def on_beat(self, is_auto_beat):
        """ Called on the actual beat """
        if is_auto_beat:
            self.player.miss_next_beat = False  # reset

    def render(self):
        fill_col = (0, 5, 5)
        self.final_screen.fill(fill_col)
        self.screen_canvas.fill(fill_col)

        if self.game_state == GameStates.IN_LEVEL:
            renderer.render_active_level(self, self.player, self.level, self.text_objects_holder)

        # scale to proper resolution
        self.final_screen.blit(pg.transform.scale(self.screen_canvas, (GameUnits.RES_W * GameUnits.RES_MUL, GameUnits.RES_H * GameUnits.RES_MUL)), (0, 0))

        # only for debugging
        self.logger.render_logs()

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("{} - FPS: {:.2f}".format(GameUnits.CAPTION, self.clock.get_fps()))
