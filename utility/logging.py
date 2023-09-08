import pygame as pg
from rendering.sprites_holder import BasicSprite


class Logger:
    """
    The logger is for displaying messages withing the frame to the screen like a one-way chat box
    Used for debugging
    """
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.font = pg.font.SysFont("consolas", 15)
        self.logs_cap = 6
        self.log_num = 0

        self.logs_group = pg.sprite.Group()
        self.logs: list[str] = []

        self.update_log_group()

    def add_log(self, text: str):
        self.log_num += 1
        self.logs.insert(0, f"{self.log_num} | {text}")

        # remove last item from list
        if len(self.logs) > self.logs_cap:
            self.logs.pop()

        self.update_log_group()

    def update_log_group(self):
        self.logs_group.empty()
        for i, log_text in enumerate(self.logs):
            text_sprite = BasicSprite(self.font.render(log_text, True, (255, 255, 0)),
                                      pg.Vector2(5, self.screen.get_height() - (15 * (i + 2))))
            text_sprite.add(self.logs_group)

    def render_logs(self):
        self.logs_group.draw(self.screen)
