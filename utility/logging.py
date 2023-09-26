import pygame as pg
from rendering.sprites_holder import BasicSprite


class LogItem:
    def __init__(self, text: str, colour: tuple):
        self.text = text
        self.colour = colour


class Logger:
    """
    The logger is for displaying messages withing the frame to the screen like a one-way chat box
    Used for debugging
    """
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.colour_tier_list = [(120, 120, 120), (255, 255, 0), (255, 0, 0)]

        self.font = pg.font.SysFont("consolas", 13)
        self.logs_cap = 16
        self.log_num = 0

        self.logs_group = pg.sprite.Group()
        self.logs: list[LogItem] = []

        self.update_log_group()

    def add_log(self, text: str, tier: int = 1):
        self.log_num += 1
        self.logs.insert(0, LogItem(f"{self.log_num} | {text}", self.colour_tier_list[tier]))

        # remove last item from list
        if len(self.logs) > self.logs_cap:
            self.logs.pop()

        self.update_log_group()

    def update_log_group(self):
        self.logs_group.empty()
        for i, log in enumerate(self.logs):
            text_sprite = BasicSprite(self.font.render(log.text, False, log.colour),
                                      pg.Vector2(5, self.screen.get_height() - (15 * (i + 2))))
            text_sprite.add(self.logs_group)

    def render_logs(self):
        self.logs_group.draw(self.screen)
