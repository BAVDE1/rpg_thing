from constants import *


class BTNOperation:
    def __init__(self, btn_type: str, value):
        self.type = btn_type
        self.value = value


class Button:
    def __init__(self, screen: pg.surface.Surface, display_text, image, pos: pg.Vector2, operation: BTNOperation, text_size: int = 30, override_size: tuple | None = None):
        self.screen = screen
        self.font = pg.font.SysFont('Times New Roman', text_size)

        self.pos = pos
        self.operation = operation

        self.display_text = self.font.render(display_text, True, (255, 255, 0))
        self.image = image

        # positional bounds [0][0]=x_left, [0][1]=x_right, [1][0]=y_top, [1][1]=y_bottom
        self.bounds = []
        if not override_size:
            self.bounds = [(self.pos.x, self.pos.x + self.display_text.get_width()),
                           (self.pos.y, self.pos.y + self.display_text.get_height() + (0 if not self.image else self.image.get_height()))]
        else:
            self.bounds = [(self.pos.x, self.pos.x + override_size[0]),
                           (self.pos.y, self.pos.y + override_size[1])]

    def render(self):
        self.mouse_hover()

        # render text and image
        self.screen.blit(self.display_text, self.pos)
        if self.image:
            self.screen.blit(self.image, (self.pos.x, self.pos.y + self.display_text.get_height()))

    def get_operation(self):
        if self.is_mouse_in_bounds():
            return self.operation

    def mouse_hover(self):
        if self.is_mouse_in_bounds():
            pg.draw.rect(self.screen, (50, 50, 50), pg.rect.Rect(self.bounds[0][0], self.bounds[1][0],
                                                                 self.bounds[0][1] - self.bounds[0][0],
                                                                 self.bounds[1][1] - self.bounds[1][0]))

    def is_mouse_in_bounds(self):
        m_x = pg.mouse.get_pos()[0]
        m_y = pg.mouse.get_pos()[1]
        return self.bounds[0][0] < m_x < self.bounds[0][1] and self.bounds[1][0] < m_y < self.bounds[1][1]


class ButtonOutlined(Button):
    def mouse_hover(self):
        if self.is_mouse_in_bounds():
            pg.draw.rect(self.screen, (50, 50, 50), pg.rect.Rect(self.bounds[0][0], self.bounds[1][0],
                                                                 self.bounds[0][1] - self.bounds[0][0],
                                                                 self.bounds[1][1] - self.bounds[1][0]), 2)
