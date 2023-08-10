from constants import *


def split_sheet(image, size: tuple, columns, rows=1):
    """ Returns list of rectangles for each frame """
    sub_surfaces = []
    for y in range(rows):
        for x in range(columns):
            rect = pg.Rect((x * size[0], y * size[1]), size)
            sub_surfaces.append(image.subsurface(rect))
    return sub_surfaces


def render_shadow(sprite, player_blit_xy, surface: pg.Surface):
    width = sprite.get_width() * SHADOW_WIDTH
    height = sprite.get_height() * SHADOW_HEIGHT
    pos_x = player_blit_xy[0] + sprite.get_width() * ((1 - SHADOW_WIDTH) / 2)
    pos_y = player_blit_xy[1] + (sprite.get_height() - (height / 2))

    rect = pg.Rect(pos_x, pos_y, width, height)

    shadow_surf = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.rect(shadow_surf, [0, 0, 0, SHADOW_ALPHA], shadow_surf.get_rect())

    surface.blit(shadow_surf, rect)
