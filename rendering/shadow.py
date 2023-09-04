from dataclasses import dataclass
import pygame as pg


@dataclass
class ToGoal:
    pass


class ShadowStripSprite(pg.sprite.Sprite):
    """ Sprite object to hold shadow sprites """
    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        pg.sprite.Sprite.__init__(self)

        self.image = sprite_img
        self.rect = pg.rect.Rect(pos.x + sprite_offset_pos.x, pos.y + sprite_offset_pos.y, self.image.get_width(), self.image.get_height())


class Shadow:
    def __init__(self, sprite: pg.surface.Surface, position: pg.Vector2, alpha: int = 100, slope=0.8, sign=-.5):
        self.sprite = sprite

        self.shadow_offset = pg.Vector2(0, 0)
        self.shadow_alpha = alpha

        self.shadow_strips = self.make_shadow_elements(position)
        self.shadow_strips_group = pg.sprite.Group()

        self.slope = slope
        self.sign = sign

    def make_shadow_elements(self, position: pg.Vector2):
        """ Split the image into horizontal strips.
        WARNING: updating this too often is heavy on performance
        """
        blank_col = (0, 0, 0, 0)

        color_key = self.sprite.get_colorkey()
        transparent = color_key if color_key else blank_col

        shadow_strips = []

        for y_row in range(self.sprite.get_height()):
            horizontal_strip = pg.Surface((self.sprite.get_width(), 1)).convert_alpha()
            horizontal_strip.fill(blank_col)

            for x_column in range(self.sprite.get_width()):
                pixel_colour = self.sprite.get_at((x_column, y_row))
                if pixel_colour != transparent:
                    horizontal_strip.set_at((x_column, 0), (10, 0, 10, self.shadow_alpha / 2))  # sets colour value

            shadow_strips.append(horizontal_strip)
        return shadow_strips[::-1]  # reverses list

    def draw(self, surface: pg.surface.Surface, position: pg.Vector2):
        """ Draw each strip of the shadow offsetting the x-axis accordingly. """
        for i, strip in enumerate(self.shadow_strips):
            angled = pg.Vector2((self.sprite.get_rect().x + i * self.slope * self.sign),
                                (self.sprite.get_rect().bottom - 1 + i * self.sign))

            pos = pg.Vector2((position.x - self.sprite.get_width() / 2 + angled.x) + self.shadow_offset.x,
                             (position.y - self.sprite.get_height() / 2 + angled.y) + self.shadow_offset.y)

            altered_pos = pg.Vector2(pos.x, pos.y)

            surface.blit(strip, altered_pos)

    def update_sprite(self, position: pg.Vector2, new_sprite: pg.surface.Surface, offset: pg.Vector2 = pg.Vector2(0, 0)):
        self.sprite = new_sprite
        self.shadow_offset = offset
        self.shadow_strips = self.make_shadow_elements(position)
