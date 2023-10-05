import pygame as pg
from rendering.split_sheet import split_sheet
from constants import GameUnits


class SpriteSheet:
    """ Holder for animation sprite sheets (ss) """
    def __init__(self, texture_path, size: pg.Vector2, columns: int):
        self.identifier = texture_path
        self.sprite_sheet = split_sheet(pg.image.load(texture_path).convert_alpha(), columns, split_size=size)
        self.length = len(self.sprite_sheet)

    def __eq__(self, other):
        return self.identifier == other.identifier


class BasicSprite(pg.sprite.Sprite):
    """ Sprite object to hold basic sprites """
    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        pg.sprite.Sprite.__init__(self)

        self.image = sprite_img
        self.pos = pos
        self.rect = pg.rect.Rect(pos.x + sprite_offset_pos.x, pos.y + sprite_offset_pos.y, self.image.get_width(), self.image.get_height())

    def __repr__(self):
        return f"BasicSprite({self.pos}, {self.rect})"


class TileSprite(BasicSprite):
    """ Sprite object to hold tile sprites information """
    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        BasicSprite.__init__(self, sprite_img, pos, sprite_offset_pos)

        self.relative_pos = pg.Vector2(((pos.x - GameUnits.LEVEL_X_OFFSET) - GameUnits.LEVEL_OFFSET) / GameUnits.UNIT,
                                       (pos.y - GameUnits.LEVEL_OFFSET) / GameUnits.UNIT)
