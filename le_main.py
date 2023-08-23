from constants import *
from os import listdir
from level_editor.button import Button

levels_dir = "assets/levels/"


class LevelEditor:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running = True
        self.keys = pg.key.get_pressed()
        self.heading_text = ""

        self.selecting_level = False
        self.selected_area = "overworld"  # changeable
        self.selected_level = None

        self.buttons = []

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False  # close game
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()  # update keys

    def main_loop(self):
        while self.running:
            pg.display.set_caption("Level Editor - FPS: {:.2f}".format(self.clock.get_fps()))
            self.events()
            self.render()
            self.clock.tick(self.fps)

    def render(self):
        self.screen.fill([0, 0, 0])
        self.display_text(self.heading_text)
        self.display_buttons()

        if not self.selected_level and not self.selecting_level:
            self.selecting_level = True
            self.init_level_select()

        if self.selected_level:
            pass

        pg.display.flip()

    def init_level_select(self):
        self.heading_text = "Level Select"
        lvls = sorted(listdir(str(levels_dir + self.selected_area)))
        for i in range(len(lvls)):
            if lvls[i].split(".")[0] != self.selected_area:
                self.add_button(lvls[i], (0, 10 + (25 * i)), display_text=lvls[i], size=20)

    def display_buttons(self):
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.render()

    def add_button(self, name, pos: tuple, display_text=None, size=30, image=None, operation=None):
        self.buttons.append(Button(self.screen, name, display_text, image, pos, size, operation))

    def display_text(self, text, size=30, position=(0, 0)):
        fnt = pg.font.SysFont('Times New Roman', size)
        text_surf = fnt.render(text, True, (255, 255, 0))
        self.screen.blit(text_surf, position)


def main():
    pg.init()
    pg.display.set_mode([RESOLUTION_X * 2, RESOLUTION_X])
    pg.font.init()
    LevelEditor().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
