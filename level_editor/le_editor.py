from constants import GameUnits
from level.level import Level
import pygame as pg


class EditableLevel(Level):
    """ Editable level for the level editor cuh """
    def __init__(self, surface, level_source, pos_offset: pg.Vector2 = pg.Vector2(0, 0), size=1):
        super().__init__(surface, level_source, pos_offset, size)

    def change_tile_sprite(self):
        pass


class LevelEditor:
    """ to handle rendering & buttons & stuff """
    def __init__(self, screen: pg.surface.Surface, level_dir, pos_offset: pg.Vector2, size):
        self.screen = screen
        self.level_dir = level_dir
        self.pos_offset = pg.Vector2(pos_offset.x, pos_offset.y + 30)

        self.font = pg.font.SysFont('Times New Roman', max(20, 3))
        self.display_text = self.font.render(f"level: {level_dir.split('/')[-1:][0]}", True, (255, 255, 0))

        self.level = EditableLevel(screen, level_dir, pos_offset=self.pos_offset, size=size)

    def render(self):
        # level text
        self.screen.blit(self.display_text, (GameUnits.LEVEL_OFFSET + self.pos_offset.x, self.pos_offset.y - 50))

        # level editor
        self.level.render_level()
        self.level.render_level_foreground()
