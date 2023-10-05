import pygame as pg


def split_sheet(image: pg.surface.Surface | str, columns, rows=1, split_size: pg.Vector2 = pg.Vector2(20, 20),):
    """ Returns list of sub-surfaces (really just surfaces) of image, for each rect """
    if isinstance(image, str):
        image = pg.image.load(image)
    sub_surfaces = []
    for y in range(rows):
        for x in range(columns):
            rect = pg.Rect((x * split_size.x, y * split_size.y), split_size)
            sub_surfaces.append(image.subsurface(rect))
    return sub_surfaces
