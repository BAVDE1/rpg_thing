import pygame as pg


def split_sheet(image: pg.surface.Surface, size: tuple, columns, rows=1):
    """ Returns list of sub-surfaces (really just surfaces) of image, for each rect """
    sub_surfaces = []
    for y in range(rows):
        for x in range(columns):
            rect = pg.Rect((x * size[0], y * size[1]), size)
            sub_surfaces.append(image.subsurface(rect))
    return sub_surfaces
