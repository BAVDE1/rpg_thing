from level_editor.le_constants import *
from constants import *
import os
from level_editor.button import Button
from level_editor.file_displayer import FileDisplayer

levels_dir = "assets/levels/"


class LevelEditor:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 30
        self.running = True
        self.keys = pg.key.get_pressed()
        self.heading_text = ""

        self.selecting_area = False
        self.selected_area = ""
        self.selecting_level = False
        self.selected_level = ""
        self.editing_level = ""

        self.seperators = []
        self.file_displays = []  # type: list[FileDisplayer]
        self.buttons = []  # type: list[Button]

        self.switch_page()

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
                self.switch_page()

    def switch_page(self):
        """ Switch page if needed. If already on page, do nothing """

        # select area
        if not self.selected_area and not self.selecting_area:
            self.selecting_area = True
            self.open_area_select()

        # select level
        if self.selected_area and not self.selected_level and not self.selecting_level:
            self.selecting_level = True
            self.open_level_select()

        # level editor
        if not self.editing_level and self.selected_area and self.selected_level:
            self.editing_level = str(levels_dir + self.selected_area + "/" + self.selected_level)
            self.open_level_editor()

    def render(self):
        self.screen.fill([0, 0, 0])

        self.draw_seperators()
        self.display_files()
        self.display_buttons()
        self.display_text(self.heading_text)

        pg.display.flip()

    def main_loop(self):
        while self.running:
            pg.display.set_caption("Level Editor - FPS: {:.2f}".format(self.clock.get_fps()))
            self.events()
            self.render()
            self.clock.tick(self.fps)

    # --------->
    #  PAGES
    # --------->

    def open_area_select(self):
        self.heading_text = "Area Select"
        areas = sorted(os.listdir(str(levels_dir)))
        for i in range(len(areas)):
            self.add_button(areas[i], (0, 35 + (25 * i)), (BTN_AREA_SEL, areas[i]), size=20)
        self.add_seperator((0, 30), (self.screen.get_width(), 30))

    def open_level_select(self):
        self.heading_text = f"Level Select ({self.selected_area})"
        levels = sorted(os.listdir(str(levels_dir + self.selected_area)))

        for i in range(len(levels)):
            if levels[i].split(".")[0] == self.selected_area:
                self.add_file(str(levels_dir + self.selected_area + "/" + levels[i]), ((self.screen.get_width() / 2) + 20, 40))
            else:
                self.add_button(levels[i], (0, 10 + (25 * i)), (BTN_LEVEL_SEL, levels[i]), size=20)

        self.add_button("Back", (0, self.screen.get_height() - 40), (BTN_BACK, self.open_area_select))
        self.add_seperator((self.screen.get_width() / 2, 30), (self.screen.get_width() / 2, self.screen.get_height()))
        self.add_seperator((0, 30), (self.screen.get_width(), 30))

    def open_level_editor(self):
        self.heading_text = f"Editing level - {self.selected_area}, {self.selected_level}"

        # seperators
        self.add_seperator((self.screen.get_width() / 2, 30), (self.screen.get_width() / 2, self.screen.get_height()))
        self.add_seperator((0, 30), (self.screen.get_width(), 30))

        # buttons
        self.add_button("Save", (self.screen.get_width() - 300, 0), (BTN_SAVE, str(levels_dir + self.selected_area + "/" + self.selected_level)))
        self.add_button("Save&Close", (self.screen.get_width() - 210, 0), (BTN_SAVE_CLOSE, str(levels_dir + self.selected_area + "/" + self.selected_level)))
        self.add_button("Close", (self.screen.get_width() - 40, 8), (BTN_CLOSE, None), size=15)

        # files
        self.add_file(self.editing_level, (10, 40), size=10)

    # ------------>
    #  Functions
    # ------------>

    def display_text(self, text, size=25, position=(0, 0)):
        """ Needs to be called every frame so text remains rendered """
        fnt = pg.font.SysFont('Times New Roman', size)
        text_surf = fnt.render(text, True, (255, 255, 0))
        self.screen.blit(text_surf, position)

    def draw_seperators(self):
        for sep in self.seperators:
            pg.draw.line(*sep)

    def display_buttons(self):
        for btn in self.buttons:
            btn.render()

    def display_files(self):
        for file in self.file_displays:
            file.render()

    def add_seperator(self, start: tuple, end: tuple):
        self.seperators.append([self.screen, (255, 255, 255), start, end])

    def add_button(self, display_text: str, pos: tuple, operation: tuple, size=30, image=None):
        self.buttons.append(Button(screen=self.screen, display_text=display_text, image=image, pos=pos, operation=operation, size=size))

    def add_file(self, file_dir:str, pos: tuple, size=20):
        self.file_displays.append(FileDisplayer(self.screen, file_dir, pos, size=size))

    def button_clicked(self, operation: tuple):
        """ Called in 'events' """
        btn_op_type = operation[0]
        btn_op_value = operation[1]

        if btn_op_type == BTN_AREA_SEL:
            self.selected_area = btn_op_value
            self.selecting_area = False
            self.reset_data()
        if btn_op_type == BTN_LEVEL_SEL:
            self.selected_level = btn_op_value
            self.selecting_level = False
            self.reset_data()

        if btn_op_type == BTN_BACK:
            if btn_op_value == self.open_area_select:
                self.selected_area = None
                self.selecting_level = False
                self.reset_data()

        if btn_op_type == BTN_SAVE:
            print("SAVE")

        if btn_op_type == BTN_SAVE_CLOSE:
            print("SAVE")
            self.reset_data(complete=True)

        if btn_op_type == BTN_CLOSE:
            self.reset_data(complete=True)

    def reset_data(self, complete=False):
        self.seperators.clear()
        self.file_displays.clear()
        self.buttons.clear()
        if complete:
            self.selected_area = ""
            self.selected_level = ""
            self.editing_level = ""


def main():
    pg.init()
    pg.display.set_mode([RESOLUTION_X * 2, RESOLUTION_X])
    pg.font.init()
    LevelEditor().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
