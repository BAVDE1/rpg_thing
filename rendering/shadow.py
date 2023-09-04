import pygame as pg


class Shadow:
    def __init__(self, sprite: pg.surface.Surface, alpha: int = 150, slope=0.8, sign=-.5):
        self.sprite = sprite

        self.shadow_offset = pg.Vector2(0, 0)
        self.shadow_alpha = alpha

        self.shadow_strips = self.make_shadow_elements()

        self.slope = slope
        self.sign = sign

    def make_shadow_elements(self):
        """ Split the image into horizontal strips. """
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

            pos = (((position.x - self.sprite.get_width() / 2 + angled.x) + self.shadow_offset.x),
                   (position.y - self.sprite.get_height() / 2 + angled.y) + self.shadow_offset.y)
            print(pos)
            surface.blit(strip, pos)
        print("----")

    def update_sprite(self, new_sprite: pg.surface.Surface, offset: pg.Vector2):
        self.sprite = new_sprite
        self.shadow_offset = offset
        self.shadow_strips = self.make_shadow_elements()


# def render_shadow(surface: pg.Surface, sprite, player_blit_xy):
#     width = sprite.get_width() * SHADOW_WIDTH
#     height = sprite.get_height() * SHADOW_HEIGHT
#     pos_x = player_blit_xy[0] + sprite.get_width() * ((1 - SHADOW_WIDTH) / 2)
#     pos_y = player_blit_xy[1] + (sprite.get_height() - (height / 2))
#
#     rect = pg.Rect(pos_x, pos_y, width, height)
#
#     shadow_surf = pg.Surface(rect.size, pg.SRCALPHA)
#     pg.draw.rect(shadow_surf, [0, 0, 0, SHADOW_ALPHA], shadow_surf.get_rect())
#
#     surface.blit(shadow_surf, rect)
