import time

from entity.player import Player
import rendering.render_handler as renderer
import input_handler
from constants import *


class Game(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running = True
        self.keys = pg.key.get_pressed()

        self.bpm = 120
        self.song_start_time = time.time()

        # set after requirements
        self.player = Player(self, self.screen_rect.center)

    def events(self):
        """ loops through all events in event queue """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False  # close game
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()  # update keys
                input_handler.player_key_down(self.player, event.key) if event.type == pg.KEYDOWN else\
                    input_handler.player_key_up(event.key)

    def functionality(self):
        input_handler.sprint_manager(self.player)

    def render(self):
        self.screen.fill("black")
        renderer.render(self.player, OVERWORLD_00, self.screen)

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)
