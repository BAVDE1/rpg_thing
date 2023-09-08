import pygame as pg


class BasicSprite(pg.sprite.Sprite):
    """ Sprite object to hold basic sprites """

    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        pg.sprite.Sprite.__init__(self)

        self.image = sprite_img
        self.rect = pg.rect.Rect(pos.x + sprite_offset_pos.x, pos.y + sprite_offset_pos.y, self.image.get_width(), self.image.get_height())


class TileSprite(BasicSprite):
    """ Sprite object to hold tile sprites information """
