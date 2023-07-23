import pygame as pg
import entity.player
import input_handler
import rendering.render_handler as renderer
from constants import *


class Game(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 30
        self.running = True
        self.keys = pg.key.get_pressed()
        self.player = entity.player.Player(self.screen_rect.center)

    def events(self):
        """ loops through all events in event queue """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                # close game
                self.running = False
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                # update keys
                self.keys = pg.key.get_pressed()
                input_handler.player_key_down(self.player, event.key) if event.type == pg.KEYDOWN else\
                    input_handler.player_key_up(self.player, event.key)

    def functionality(self):
        input_handler.sprint_manager(self.player)

    def render(self):
        self.screen.fill("black")
        renderer.render(self.player, OVERWORLD_LEVEL_DIR, self.screen)

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)
