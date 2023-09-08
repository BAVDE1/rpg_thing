import pygame as pg
from rendering.sprites_holder import BasicSprite


class Logger:
    """
    The logger is for displaying messages withing the frame to the screen like a one-way chat box
    Used for debugging
    """
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.font = pg.font.SysFont("", 14)
        self.logs_cap = 6

        self.logs_group = pg.sprite.Group()
        self.logs: list[str] = []

        self.update_log_group()

    def add_log(self, text: str):
        self.logs.insert(0, text)

        # remove last item from list
        if len(self.logs) > self.logs_cap:
            self.logs.pop()

        self.update_log_group()

    def update_log_group(self):
        self.logs_group.empty()
        for i, log in enumerate(self.logs):
            text_sprite = BasicSprite(self.font.render(log, True, (255, 255, 0)),
                                      pg.Vector2(0, self.screen.get_height() - (10 * (i + 1))))
            text_sprite.add(self.logs_group)

    def render_logs(self):
        self.logs_group.draw(self.screen)
