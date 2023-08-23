from level_editor.le_constants import *
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

        self.selecting_area = False
        self.selected_area = ""
        self.selecting_level = False
        self.selected_level = ""

        self.buttons = []  # type: list[Button]

    # ------->
    #  Loops
    # ------->

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False  # close game
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()  # update keys

            # button click  (if buttons overlap, both will click)
            if event.type == pg.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn.is_mouse_in_bounds():
                        self.button_clicked(btn.mouse_down())

    def render(self):
        self.screen.fill([0, 0, 0])
        self.display_text(self.heading_text)
        self.display_buttons()

        if not self.selected_area and not self.selecting_area:
            self.selecting_area = True
            self.open_area_select()

        if self.selected_area and not self.selected_level and not self.selecting_level:
            self.selecting_level = True
            self.open_level_select()

        if self.selected_level:
            pass

        pg.display.flip()

    def main_loop(self):
        while self.running:
            pg.display.set_caption("Level Editor - FPS: {:.2f}".format(self.clock.get_fps()))
            self.events()
            self.render()
            self.clock.tick(self.fps)

    # --------->
    #  "PAGES"
    # --------->

    def open_area_select(self):
        print("area")
        self.heading_text = "Area Select"
        areas = listdir(str(levels_dir))
        for i in range(len(areas)):
            self.add_button(areas[i], (0, 35 + (25 * i)), areas[i], (BTN_AREA_SEL, areas[i]), size=20)

    def open_level_select(self):
        print("level")
        self.heading_text = f"Level Select ({self.selected_area})"
        levels = sorted(listdir(str(levels_dir + self.selected_area)))
        for i in range(len(levels)):
            if levels[i].split(".")[0] != self.selected_area:
                self.add_button(levels[i], (0, 10 + (25 * i)), levels[i], (BTN_LEVEL_SEL, levels[i]), size=20)
        self.add_button("back", (0, self.screen.get_height() - 40), "Back", (BTN_BACK, self.open_area_select))

    # ------------>
    #  Functions
    # ------------>

    def display_text(self, text, size=30, position=(0, 0)):
        """ Needs to be called every frame so text remains rendered """
        fnt = pg.font.SysFont('Times New Roman', size)
        text_surf = fnt.render(text, True, (255, 255, 0))
        self.screen.blit(text_surf, position)

    def display_buttons(self):
        for btn in self.buttons:
            btn.render()

    def add_button(self, name, pos: tuple, display_text: str, operation: tuple, size=30, image=None):
        self.buttons.append(Button(screen=self.screen, name=name, display_text=display_text, image=image, pos=pos, operation=operation, size=size))

    def button_clicked(self, operation: tuple):
        """ Called in 'events' """
        btn_op_type = operation[0]
        btn_op_value = operation[1]

        if btn_op_type == BTN_AREA_SEL:
            self.selected_area = btn_op_value
            self.selecting_area = False
        if btn_op_type == BTN_LEVEL_SEL:
            self.selected_level = btn_op_value
            self.selecting_level = False

        if btn_op_type == BTN_BACK:
            if btn_op_value == self.open_area_select:
                self.selected_area = None
                self.selecting_level = False

        self.buttons.clear()


def main():
    pg.init()
    pg.display.set_mode([RESOLUTION_X * 2, RESOLUTION_X])
    pg.font.init()
    LevelEditor().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
