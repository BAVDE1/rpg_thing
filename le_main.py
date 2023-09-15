from level_editor.file_displayer import FileDisplayer
from level_editor.le_editor import LevelEditor
from level_editor.le_state_handler import *
from level_editor.le_constants import *
from level_editor.buttons import Button, BTNOperation
from constants import GameUnits, EDITING_TAG
import os
import pygame as pg

LEVELS_DIR = "./assets/levels/"
KEYBOARD_NUMS = {pg.K_1: 1, pg.K_2: 2, pg.K_3: 3, pg.K_4: 4, pg.K_5: 5, pg.K_6: 6, pg.K_7: 7, pg.K_8: 8, pg.K_9: 9}


def render_class_items(items: list[FileDisplayer | Button]):
    """ Used to render a list of classes. Classes must contain 'render()' function """
    for item in items:
        item.render()


class LevelEditorMain:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 30
        self.running = True
        self.keys = pg.key.get_pressed()
        self.heading_text = ""

        self.selecting_area = False
        self.selected_area = get_json_data()[SELECTED_AREA]
        self.selecting_level = False
        self.selected_level = get_json_data()[SELECTED_LEVEL]
        self.editing_level = False
        self.editor_level = get_json_data()[EDITOR_LEVEL]

        self.seperators = []
        self.file_displays: list[FileDisplayer] = []
        self.buttons: list[Button] = []
        self.level_editor: LevelEditor | None = None

        self.switch_page()

    # ------->
    #  Loops
    # ------->

    def events(self):
        for event in pg.event.get():
            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.save_editor_state()
                self.running = False

            # update keys
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()

                # keyboard numbers
                if event.key in KEYBOARD_NUMS:
                    if self.editor_level and self.level_editor:
                        self.level_editor.keyboard_num_pressed(KEYBOARD_NUMS[event.key])
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            # button click  (if buttons overlap, both will click)
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_button = event.button

                # left click
                if mouse_button == 1:
                    # for level editors
                    if self.editor_level and self.level_editor:
                        self.level_editor.mouse_left_clicked()

                    for btn in self.buttons:
                        if btn.is_mouse_in_bounds():
                            self.button_left_clicked(btn.get_operation())
                    self.switch_page()

                # middle click
                if mouse_button == 2:
                    if self.editor_level and self.level_editor:
                        self.level_editor.mouse_middle_clicked()

                # right click
                if mouse_button == 3:
                    if self.editor_level and self.level_editor:
                        self.level_editor.mouse_right_clicked()

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
        if self.selected_area and self.selected_level:
            self.editor_level = f"{LEVELS_DIR}{self.selected_area}/{self.selected_level}"
        if not self.editing_level and self.editor_level:
            self.editing_level = True
            self.open_level_editor()

    def render(self):
        self.screen.fill([0, 0, 0])

        self.draw_seperators()
        render_class_items(self.file_displays)
        render_class_items(self.buttons)
        if self.level_editor:
            self.level_editor.render()

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
        areas = sorted(os.listdir(str(LEVELS_DIR)))
        for i in range(len(areas)):
            self.add_button(areas[i], pg.Vector2(0, 35 + (25 * i)), BTNOperation(BTN_AREA_SEL, areas[i]), size=20)

        self.add_seperator((0, 30), (self.screen.get_width(), 30))

    def open_level_select(self):
        self.heading_text = f"Level Select ({self.selected_area})"
        levels = sorted(os.listdir(str(LEVELS_DIR + self.selected_area)))  # list of files

        skipped = 0  # takes away from 'i'
        for i, level_file in enumerate(levels):
            # if it is an editor level, skip
            if level_file.split(" ")[-1] == EDITING_TAG.split(" ")[-1]:
                skipped += 1
                continue

            # list level
            if level_file.split(".")[0] == self.selected_area:
                self.add_file(f"{LEVELS_DIR}{self.selected_area}/{level_file}", pg.Vector2((self.screen.get_width() / 2) + 20, 40))
            else:
                self.add_button(level_file, pg.Vector2(0, 10 + (25 * (i - skipped))), BTNOperation(BTN_LEVEL_SEL, level_file), size=20)

        self.add_button("Back", pg.Vector2(0, self.screen.get_height() - 40), BTNOperation(BTN_BACK, self.open_area_select))
        self.add_seperator((self.screen.get_width() / 2, 30), (self.screen.get_width() / 2, self.screen.get_height()))
        self.add_seperator((0, 30), (self.screen.get_width(), 30))

    def open_level_editor(self):
        self.heading_text = f"Editing level - {self.selected_area}, {self.selected_level}"

        # seperators
        self.add_seperator((self.screen.get_width() / 2, 30), (self.screen.get_width() / 2, self.screen.get_height()))
        self.add_seperator((0, 30), (self.screen.get_width(), 30))

        # buttons
        self.add_button("Save", pg.Vector2(self.screen.get_width() - 300, 0), BTNOperation(BTN_SAVE, self.editor_level))
        self.add_button("Save&Close", pg.Vector2(self.screen.get_width() - 210, 0), BTNOperation(BTN_SAVE_CLOSE, self.editor_level))
        self.add_button("Close", pg.Vector2(self.screen.get_width() - 40, 8), BTNOperation(BTN_CLOSE, None), size=15)

        # files
        self.add_file(self.editor_level, pg.Vector2(10, 40), size=10)

        self.level_editor = LevelEditor(self.screen, self.editor_level, position=pg.Vector2(self.screen.get_width() / 2 + 30, 40), size=1.4)

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

    def add_seperator(self, start: tuple, end: tuple):
        self.seperators.append([self.screen, (255, 255, 255), start, end])

    def add_button(self, display_text: str, pos: pg.Vector2, operation: BTNOperation, size=30, image=None):
        self.buttons.append(Button(screen=self.screen, display_text=display_text, image=image, pos=pos, operation=operation, text_size=size))

    def add_file(self, file_dir: str, pos: pg.Vector2, size=20):
        self.file_displays.append(FileDisplayer(self.screen, file_dir, pos, size=size))

    def reload_files(self):
        for i, file in enumerate(self.file_displays):
            self.file_displays[i] = FileDisplayer(file.screen, file.file_dir, file.pos, file.size)

    def button_left_clicked(self, operation: BTNOperation):
        """ Called in 'events' every time a button is clicked """
        btn_type = operation.type
        btn_value = operation.value

        if btn_type == BTN_AREA_SEL:
            self.selected_area = btn_value
            self.reset_data()

        if btn_type == BTN_LEVEL_SEL:
            self.selected_level = btn_value
            self.reset_data()

        if btn_type == BTN_BACK:
            if btn_value == self.open_area_select:
                self.selected_area = ""
                self.selecting_level = False
                self.reset_data()

        if btn_type == BTN_SAVE:
            if self.level_editor:
                self.level_editor.save_editing_level()
                self.reload_files()

        if btn_type == BTN_SAVE_CLOSE:
            if self.level_editor:
                self.level_editor.save_editing_level()
            self.reset_data(complete=True)

        if btn_type == BTN_CLOSE:
            self.reset_data(complete=True)

    def reset_data(self, complete=False):
        self.selecting_area = False
        self.selecting_level = False
        self.editing_level = False

        self.seperators.clear()
        self.file_displays.clear()
        self.buttons.clear()
        self.level_editor = None
        if complete:
            self.selected_area = ""
            self.selected_level = ""
            self.editor_level = ""

    def save_editor_state(self):
        dic = {
            SELECTED_AREA: self.selected_area,
            SELECTED_LEVEL: self.selected_level,
            EDITOR_LEVEL: self.editor_level
        }
        save_json_data(dic)


def main():
    pg.init()
    pg.display.set_mode([GameUnits.RES_W * GameUnits.RES_MUL, GameUnits.RES_H * GameUnits.RES_MUL])
    pg.font.init()
    LevelEditorMain().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
