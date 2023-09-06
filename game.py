import time
import pygame as pg
import input_handler
import rendering.render_handler as renderer

from constants import GameUnits, LevelLocations
from rendering.split_sheet import split_sheet
from texture_constants import PlayerTextures
from utility.logging import Logger
from entity.player import Player


class Game:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_canvas = pg.surface.Surface((GameUnits.RES_W, GameUnits.RES_H))

        self.clock = pg.time.Clock()
        self.fps = 60  # 500 cap
        self.running = True
        self.logger = Logger(self.screen_canvas)

        self.keys = pg.key.get_pressed()

        self.bpm = 180
        self.song_start_time = time.time()

        # set after requirements
        self.player = Player(self, self.screen_canvas, self.screen_canvas.get_rect().center)
        print(self.screen_canvas.get_rect(), self.screen_canvas.get_rect().center)

    def events(self):
        """ For events in event queue """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False  # close game
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()  # update keys

                if event.type == pg.KEYDOWN:
                    input_handler.player_key_down(self.player, event.key)

                    # dev thingos
                    if self.keys[pg.K_p]:
                        self.bpm = 60 if self.bpm == 120 else 120 if self.bpm > 120 else 180
                    if self.keys[pg.K_m]:  # set idle anim
                        texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE_DEBUG).convert_alpha()
                        ss_idle = split_sheet(texture_idle, (GameUnits.UNIT, GameUnits.UNIT), 4)
                        self.player.animator.change_idle_anim(False, new_idle_ss=[PlayerTextures.PLAYER_IDLE_DEBUG, ss_idle], boomerang_idle=False)
                    if self.keys[pg.K_n]:  # reset idle anim
                        self.player.animator.change_idle_anim(set_to_default=True)
                elif event.type == pg.KEYUP:
                    input_handler.player_key_up(event.key)

    def functionality(self):
        input_handler.sprint_manager(self.player)

    def render(self):
        fill_col = (0, 5, 5)
        self.screen.fill(fill_col)
        self.screen_canvas.fill(fill_col)

        renderer.render(self.screen_canvas, self.player, LevelLocations.OVERWORLD_00)

        self.screen.blit(pg.transform.scale(self.screen_canvas, (GameUnits.RES_W * GameUnits.RES_MUL, GameUnits.RES_H * GameUnits.RES_MUL)), (0, 0))
        # self.screen.blit(self.screen_canvas, (0, 0))

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("{} - FPS: {:.2f}".format(GameUnits.CAPTION, self.clock.get_fps()))
