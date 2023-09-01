from constants import GameUnits
from level.level import Level
import pygame as pg


class LevelEditor:
    def __init__(self, screen: pg.surface.Surface, level_dir, size):
        self.screen = screen
        self.level_dir = level_dir

        self.level = Level(screen, level_dir, pos_offset=pg.Vector2(220 * GameUnits.RES_MUL, 30 * GameUnits.RES_MUL), size=size)

    def render(self):
        self.level.render_level()
        self.level.render_level_foreground()
