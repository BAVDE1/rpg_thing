import time

import input_handler
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
                    if self.keys[pg.K_p]:
                        self.bpm = 60 if self.bpm == 120 else 120 if self.bpm > 120 else 180
                    if self.keys[pg.K_m]:
                        texture_idle = pg.image.load(PLAYER_IDLE_DEBUG).convert_alpha()
                        ss_idle = split_sheet(texture_idle, (BASE_UNIT, BASE_UNIT), 4)
                        self.player.animator.change_idle_anim(False, new_idle_ss=[PLAYER_IDLE_DEBUG, ss_idle], boomerang_idle=False)
                    if self.keys[pg.K_n]:
                        self.player.animator.change_idle_anim(set_to_default=True)
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

            pg.display.set_caption("{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps()))
