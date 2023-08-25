from constants import *
from level.level import Level


class LevelEditor:
    def __init__(self, screen: pg.surface.Surface, level_dir):
        self.screen = screen
        self.level_dir = level_dir

        self.level = Level(screen, level_dir, pos_offset=pg.Vector2(220 * RES_MUL, 30 * RES_MUL), size=0.8)

    def render(self):
        self.level.render_level()
        self.level.render_level_foreground()
