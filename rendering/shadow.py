from dataclasses import dataclass
from texture_constants import RenderValues
import pygame as pg

SHADOW_CLARITY = 10 - RenderValues.SHADOW_QUALITY
SHADOW_CLARITY = SHADOW_CLARITY if SHADOW_CLARITY % 2 == 0 else SHADOW_CLARITY + 1  # must always be even. If odd, add 1
SHADOW_CLARITY = max(2, min(10, SHADOW_CLARITY))  # clamps between 2 and 10

SUN_SLOPE = .8
SUN_SIGN = -.5


@dataclass
class ToGoal:
    pass


@dataclass
class FromGoal:
    pass


class ShadowStripSprite(pg.sprite.Sprite):
    """ Sprite object to hold shadow sprites """
    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        pg.sprite.Sprite.__init__(self)

        self.image = sprite_img
        self.rect = pg.rect.Rect(pos.x + sprite_offset_pos.x, pos.y + sprite_offset_pos.y, self.image.get_width(), self.image.get_height())


class Shadow:
    def __init__(self, surface: pg.surface.Surface, sprite: pg.surface.Surface, position: pg.Vector2, alpha: int = 100):
        self.surface = surface
        self.sprite = sprite

        self.shadow_offset = pg.Vector2(0, 0)
        self.shadow_alpha = alpha

        self.shadow_strips_group = pg.sprite.Group()
        self.make_shadow_elements(position)

    def make_shadow_elements(self, position: pg.Vector2):
        """ Split the image into horizontal strips.
        WARNING: updating this too often is heavy on performance
        """
        color_key = self.sprite.get_colorkey()
        blank_col = (0, 0, 0, 0)
        transparent = color_key if color_key else blank_col

        shadow_strips: list[ShadowStripSprite] = []
        for y_row in range(self.sprite.get_height()):
            if y_row % SHADOW_CLARITY == 0:
                horizontal_strip = pg.Surface((self.sprite.get_width(), 1)).convert_alpha()
                horizontal_strip.fill(blank_col)

                # set colour
                for x_column in range(self.sprite.get_width()):
                    pixel_colour = self.sprite.get_at((x_column, y_row))
                    if pixel_colour != transparent:
                        horizontal_strip.set_at((x_column, 0), (10, 0, 10, self.shadow_alpha))  # sets colour value

                horizontal_strip = pg.transform.scale(horizontal_strip, (
                    horizontal_strip.get_width(),
                    horizontal_strip.get_height() * (SHADOW_CLARITY / 2)))  # scale horizontal strips' height

                # create position
                angled = pg.Vector2((self.sprite.get_rect().x + (self.sprite.get_height() - y_row) * SUN_SLOPE * SUN_SIGN),
                                    (self.sprite.get_rect().bottom - 1 + (self.sprite.get_height() - y_row) * SUN_SIGN))

                pos = pg.Vector2((position.x - self.sprite.get_width() / 2 + angled.x) + self.shadow_offset.x,
                                 (position.y - self.sprite.get_height() / 2 + angled.y) + self.shadow_offset.y)

                shadow_strips.append(ShadowStripSprite(horizontal_strip, pos))
        self.shadow_strips_group.empty()
        self.shadow_strips_group.add(*shadow_strips)

    def draw(self):
        """ Draw each strip of the shadow offsetting the x-axis accordingly. """
        self.shadow_strips_group.draw(self.surface)

    def update_shadow(self, position: pg.Vector2, new_sprite: pg.surface.Surface = None, offset: pg.Vector2 = pg.Vector2(0, 0)):
        """ Updates the shadow with a new position and a new sprite """
        if not new_sprite:
            new_sprite = self.sprite
        self.sprite = new_sprite
        self.shadow_offset = offset
        self.make_shadow_elements(position)
