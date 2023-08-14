import time

import input_handler
import dev_mode
import rendering.render_handler as renderer
from constants import *
from entity.player import Player
from rendering.rendering_other import split_sheet


class Game:
    def __init__(self):
        self.dev_mode = False

        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running = True
        self.keys = pg.key.get_pressed()

        self.bpm = 180
        self.song_start_time = time.time()

        # set after requirements
        self.player = Player(self, self.screen, self.screen_rect.center)

    def events(self):
        """ For events in event queue """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False  # close game
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()  # update keys

                if event.type == pg.KEYDOWN:
                    input_handler.player_key_down(self.player, event.key)

                    # dev mode
                    if self.keys[pg.K_BACKSLASH]:
                        self.dev_mode = not self.dev_mode
                        if self.dev_mode:
                            dev_mode.activate_dev_mode(self.screen)
                        print("DEV MODE: " + str(self.dev_mode))
                    if self.dev_mode:
                        dev_mode.player_key_down(self, self.player, self.keys)
                elif event.type == pg.KEYUP:
                    input_handler.player_key_up(event.key)

    def functionality(self):
        input_handler.sprint_manager(self.player)

    def render(self):
        self.screen.fill([0, 5, 5])
        renderer.render(self, self.player, OVERWORLD_00, self.screen)

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.functionality()
            self.render()

            self.clock.tick(self.fps)

            if self.dev_mode:
                dev_mode.dev_mode_loop(self)
            else:
                pg.display.set_caption(CAPTION)
