from constants import GameUnits
from level.level import Level
import pygame as pg


class EditableLevel(Level):
    """ Editable level for the level editor cuh """


class LevelEditor:
    """ to handle rendering & stuff """
    def __init__(self, screen: pg.surface.Surface, level_dir, size):
        self.screen = screen
        self.level_dir = level_dir

        self.level = EditableLevel(screen, level_dir, pos_offset=pg.Vector2(200 * GameUnits.RES_MUL, 30 * GameUnits.RES_MUL), size=size)

    def render(self):
        self.level.render_level()
        self.level.render_level_foreground()
