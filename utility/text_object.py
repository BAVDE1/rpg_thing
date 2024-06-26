import time
import math
import pygame as pg


class TextObjectsHolder:
    def __init__(self, surface: pg.surface.Surface):
        self.surface = surface

        self.text_objects_group = pg.sprite.Group()

    def add_text_object(self, text: str, pos: pg.Vector2,
                        colour: tuple = (255, 255, 255), lifetime=1, move_by: pg.Vector2 = pg.Vector2(0, -10), fade=True, sin_amp=3):
        """ Creates a new text object """
        txt_obj = TextObject(text, colour, pos, lifetime, move_by, fade, sin_amp)
        txt_obj.add(self.text_objects_group)

    def render(self):
        self.text_objects_group.update()
        self.text_objects_group.draw(self.surface)


class TextObject(pg.sprite.Sprite):
    def __init__(self, text: str, colour: tuple, pos: pg.Vector2, lifetime, move_by: pg.Vector2, fade: bool, sin_amp):
        pg.sprite.Sprite.__init__(self)

        self.font = pg.font.SysFont("consolas", 9)

        self.created_time = time.time()
        self.die_time = self.created_time + lifetime

        self.move_by = move_by
        self.sin_amp = sin_amp
        self.fade = fade

        self.image = self.font.render(text, False, colour).convert_alpha()

        self.og_pos = pg.Vector2(pos.x - self.image.get_width() / 2, pos.y)
        self.rect = pg.rect.Rect(self.og_pos.x, self.og_pos.y, 0, 0)

    def update(self):
        """ Update this before rendering """
        # delete
        if time.time() >= self.die_time:
            self.kill()

        # update pos
        percent = (time.time() - self.created_time) / (self.die_time - self.created_time)
        self.rect.x = self.og_pos.x + ((self.move_by.x * percent) +
                                       ((self.sin_amp - self.sin_amp * percent) * math.sin((self.sin_amp * 2) * time.time())))
        self.rect.y = self.og_pos.y + (self.move_by.y * percent)

        if self.fade:
            self.image.set_alpha(255 - (255 * percent))
