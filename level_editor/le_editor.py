from level.level import Level
from level_editor.buttons import ButtonOutlined, Button, BTNOperation
from level_editor.file_displayer import FileDisplayer
from constants import EDITING_TAG, GameUnits
from texture_constants import ASCII_TO_SPRITE
from level_editor.le_constants import *
import pygame as pg
import os


def get_file_contents_hash(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist, or could not be found.")

    with open(file_path) as file:
        return hash(file.read())


class TileOption:
    def __init__(self, screen: pg.surface.Surface, tile_chars: str, tile_sprite: pg.surface.Surface,
                 position: pg.Vector2, scale=1, text_index: str = ''):
        self.screen = screen
        self.pos = position

        self.tile_chars = tile_chars
        self.txt_size = 10 * scale
        self.tile_sprite = pg.transform.scale(tile_sprite,
                                              (tile_sprite.get_width() * scale, tile_sprite.get_height() * scale))

        if text_index:
            text_index += '-'
        self.button = Button(screen, f"{text_index}{tile_chars[:2]}", self.tile_sprite, position,
                             BTNOperation(BTN_TILE_OPTION, tile_chars), text_size=self.txt_size,
                             override_size=(self.tile_sprite.get_width(), self.tile_sprite.get_height() + self.txt_size))

    def get_rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x, self.pos.y, self.tile_sprite.get_width(),
                       self.tile_sprite.get_height() + self.txt_size)

    def __repr__(self):
        return f"TileOption({self.tile_chars}, {self.pos})"


class Hotbar:
    def __init__(self, screen, position: pg.Vector2, scale=1):
        self.screen = screen

        self.pos = position
        self.scale = scale

        self.max_size = 9
        self.tile_options: list[TileOption | None] = [None for _ in range(self.max_size)]  # generates a list of None

        self.selected_slot = 1

    def set_tile_option(self, slot_num: int, tile_char: str):
        """ Add a new tile to the hotbar, overrides existing tile in chosen slot """
        if tile_char in ASCII_TO_SPRITE:
            slot_num = max(1, min(self.max_size, slot_num))

            tile_sprite = ASCII_TO_SPRITE[tile_char]
            tile_option = TileOption(self.screen, tile_char, tile_sprite,
                                     pg.Vector2(self.pos.x + (50 * (slot_num - 1)), self.pos.y), scale=self.scale,
                                     text_index=str(slot_num))

            self.tile_options[slot_num - 1] = tile_option

    def get_selected_tile_chars(self) -> str:
        """ Returns the tile_chars (for ASCII_TO_SPRITE) or nothing if no tile in slot """
        slot = self.get_selected_slot()
        if slot:
            return slot.tile_chars
        return ""

    def render(self):
        for tile_option in self.tile_options:
            if tile_option:
                tile_option.button.render()

                # selected outline
                if slot := self.get_selected_slot():
                    pg.draw.rect(self.screen, (255, 255, 255), slot.get_rect(), 2)

    def switch_selected_slot(self, slot_num=None, addition=0):
        """ Used to switch the selected hotbar slot (clamped). Auto cycles through items """
        if addition:
            slot_num = max(0, min(self.max_size + 1, self.selected_slot + addition))

            if slot_num > self.max_size:
                slot_num = 1
            elif slot_num < 1:
                slot_num = self.max_size

            while self.tile_options[slot_num - 1] is None:
                slot_num += addition
                if slot_num > self.max_size:
                    slot_num = 1

        self.selected_slot = max(1, min(self.max_size, slot_num))  # clamps

    def get_selected_slot(self) -> TileOption | None:
        """ Returns TileOption (or None) of the slot selected """
        return self.tile_options[self.selected_slot - 1]


class TileInventory:
    def __init__(self, screen, hotbar: Hotbar, position):
        self.screen = screen
        self.hotbar = hotbar
        self.position = position

        self.spacing_x = (GameUnits.UNIT * 2) + 15
        self.spacing_y = (GameUnits.UNIT * 2) + 25

        self.rows = 7  # 7
        self.columns = 8  # 8

        self.inv_pages: dict = {}
        self.on_page = 0

        self.is_open = False
        self.create_inv()

    def create_inv(self):
        """ Creates the inventory """
        on_page = 0
        on_row = 0
        on_column = 0

        page = []
        for chars in ASCII_TO_SPRITE.keys():
            page.append(TileOption(self.screen, chars, ASCII_TO_SPRITE[chars],
                                  pg.Vector2(self.position.x + (self.spacing_x * on_column), self.position.y + (self.spacing_y * on_row)), scale=2))
            on_column += 1

            # restart column & add row
            if on_column == self.columns:
                on_column = 0
                on_row += 1

                # complete page & start a new page
                if on_row == self.rows:
                    self.inv_pages[on_page] = page
                    page = []
                    on_row = 0
                    on_page += 1

        # add if there was an incomplete page
        if len(page) > 0:
            self.inv_pages[on_page] = page

    def render(self):
        if self.is_open and len(self.inv_pages) > 0:
            # background
            bg_rect = pg.Rect(self.position.x - 10, self.position.y - 10, (self.spacing_x * self.columns) + 20, self.spacing_y * self.rows)
            pg.draw.rect(self.screen, (0, 0, 0), bg_rect)
            pg.draw.rect(self.screen, (255, 255, 255), bg_rect, 1)

            # tiles
            for tile_option in self.inv_pages[self.on_page]:
                tile_option.button.render()

            # page number
            self.screen.blit(pg.font.SysFont('Times New Roman', 20)
                             .render(f"{self.on_page + 1}/{len(self.inv_pages)}", False, (255, 255, 0)),
                             pg.Vector2(10, self.screen.get_height() - 20))

    def user_input(self, number=None):
        """ Called when the user left-clicks or presses a number on their keyboard """
        if self.is_open:
            for tile_option in self.inv_pages[self.on_page]:
                if tile_option.button.is_mouse_in_bounds():
                    if number:
                        self.hotbar.selected_slot = number
                    self.hotbar.set_tile_option(self.hotbar.selected_slot, tile_option.tile_chars)


class LevelEditor:
    """ to handle rendering & buttons & stuff """

    def __init__(self, screen: pg.surface.Surface, level_file: str, position: pg.Vector2, size):
        self.screen = screen

        self.SOURCE_LEVEL_FILE = level_file
        self.EDITING_LEVEL_FILE = f"{level_file}{EDITING_TAG}"
        self.SOURCE_LEVEL_DIR = '/'.join(self.SOURCE_LEVEL_FILE.split('/')[:-1])  # removes ending file from path
        self.opened_level_file = self.SOURCE_LEVEL_FILE  # only change this
        self.update_opened_level_file()

        self.selected_layer = 2

        self.font = pg.font.SysFont('Times New Roman', max(20, 3))
        self.display_text: pg.surface.Surface | None = None
        self.update_display_text()

        self.size = size
        self.position = position
        self.lvl_pos = self.load_lvl_pos()

        self.level = self.load_lvl()
        self.editing_file: FileDisplayer | None = None
        self.buttons: list[ButtonOutlined | Button] = []
        self.create_editor_buttons()
        self.update_opened_level_file()

        self.max_saved_changes = 50
        self.saved_changes: list[tuple[int, int, str]] = []  # row, column, tile chars

        self.hotbar: Hotbar = Hotbar(self.screen, pg.Vector2((self.screen.get_width() / 2) + 10, self.screen.get_height() - 70), scale=2)
        self.hotbar.set_tile_option(1, 'Gr')
        self.hotbar.set_tile_option(2, 'Pt')
        self.hotbar.set_tile_option(3, 'Dt*0')

        self.tile_inv: TileInventory = TileInventory(self.screen, self.hotbar, pg.Vector2(10, 40))

    def load_lvl_pos(self) -> pg.Vector2:
        return pg.Vector2(self.position.x + 22 * self.size,
                          self.position.y + self.display_text.get_height() * (self.size * 2))

    def load_lvl(self) -> Level:
        return Level(self, self.opened_level_file if not self.editing_file_exists() else self.EDITING_LEVEL_FILE,
                     pos_offset=self.lvl_pos, size=self.size)

    def render(self):
        # level text
        self.screen.blit(self.display_text, self.position)

        # editing file
        if self.editing_file:
            self.editing_file.render()

        # level
        self.level.render_level(self.screen)
        self.level.render_entities(self.screen)
        self.level.render_level_foreground(self.screen)

        # tile selection
        self.hotbar.render()
        self.tile_inv.render()

        # buttons
        for button in self.buttons:
            button.render()

        # layer selection
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect((self.screen.get_width() / 2) - 30, (self.screen.get_height() - 30) - (20 * (2 - self.selected_layer)), 20, 22), 1)

    def create_editor_buttons(self):
        """ Creates (or updates) the buttons for editing the level """
        self.buttons = []
        for tile_rect in self.level.generate_tile_rects():
            pos = pg.Vector2(tile_rect[0], tile_rect[1])
            size = (tile_rect[2], tile_rect[3])
            operation = BTNOperation(BTN_TILE_CHANGE, (tile_rect[4], tile_rect[5]))
            self.buttons.append(ButtonOutlined(self.screen, '', None, pos, operation, override_size=size))

        # layer switch buttons
        self.add_button(" t ", pg.Vector2((self.screen.get_width() / 2) - 30, self.screen.get_height() - 70), BTNOperation(BTN_LAYER_OPTION, 0), size=20)
        self.add_button(" e ", pg.Vector2((self.screen.get_width() / 2) - 30, self.screen.get_height() - 50), BTNOperation(BTN_LAYER_OPTION, 1), size=20)
        self.add_button(" g ", pg.Vector2((self.screen.get_width() / 2) - 30, self.screen.get_height() - 30), BTNOperation(BTN_LAYER_OPTION, 2), size=20)

    def add_button(self, display_text: str, pos: pg.Vector2, operation: BTNOperation, size=30, image=None, override_size=None):
        self.buttons.append(
            Button(screen=self.screen, display_text=display_text, image=image, pos=pos,
                   operation=operation, text_size=size, override_size=override_size))

    def keyboard_num_pressed(self, number):
        self.tile_inv.user_input(number)
        self.hotbar.switch_selected_slot(slot_num=number)

    def keyboard_ctrl_z_pressed(self):
        if len(self.saved_changes) != 0:
            self.change_tile(*self.saved_changes.pop(0), save_change=False)

    def mouse_left_clicked(self):
        self.tile_inv.user_input()
        self.mouse_clicked_on_editor_level()

    def mouse_right_clicked(self):
        self.mouse_clicked_on_editor_level(override_value='  ')

    def mouse_middle_clicked(self):
        print("middle")

    def mouse_clicked_on_editor_level(self, override_value=None):
        """ Used for button click detection & functionality when the mouse is clicked """
        for btn in self.buttons:
            if btn.is_mouse_in_bounds():
                btn_type = btn.operation.type
                btn_value = btn.operation.value

                if btn_type == BTN_TILE_CHANGE:
                    self.change_tile(btn_value[1], btn_value[0], override_value)

                if btn_type == BTN_LAYER_OPTION:
                    self.change_selected_layer(btn_value)

    def change_tile(self, row, column, override_value=None, save_change=True):
        """ Changes the tile to selected tile in the editing file """
        if not self.editing_file_exists():
            self.create_editing_file()

        # get lines
        lines = []
        with open(self.EDITING_LEVEL_FILE) as editing_file:
            for line in editing_file:
                lines.append(line.strip().replace("[", "").replace("]", "").split(","))

        # save change
        if save_change:
            # offset row to the layer selected
            row += (GameUnits.LVL_HEIGHT * self.selected_layer) + self.selected_layer * 2

            # save
            self.saved_changes.insert(0, (row, column, lines[row][column]))
            if len(self.saved_changes) > self.max_saved_changes:
                self.saved_changes.pop()

        # set tile
        lines[row][column] = self.hotbar.get_selected_tile_chars() if override_value is None else override_value

        # update file
        with open(self.EDITING_LEVEL_FILE, 'w') as editing_file:
            contents = ""
            for line in lines:
                contents += f"[{','.join(line)}]\n"
            editing_file.write(contents)

        # if editor is identical to source, save (aka, remove the editing file)
        if get_file_contents_hash(self.EDITING_LEVEL_FILE) == get_file_contents_hash(self.SOURCE_LEVEL_FILE):
            self.save_editing_level()
        self.update_all_items()

    def save_editing_level(self):
        """ Used to save the editor level to the source level """
        if self.editing_file_exists():
            with open(self.SOURCE_LEVEL_FILE, 'w+') as level_file:
                with open(self.EDITING_LEVEL_FILE) as editing_file:
                    contents = editing_file.read()
                level_file.write(contents)
            os.remove(self.EDITING_LEVEL_FILE)

            self.update_all_items()

    def update_all_items(self):
        """ Used to update all necessary items in the editor """
        self.update_opened_level_file()
        self.update_display_text()
        self.level.load_or_reload_level(self.opened_level_file)

        self.lvl_pos = self.load_lvl_pos()
        self.level = self.load_lvl()
        self.create_editor_buttons()

        # reload file
        if self.editing_file:
            self.editing_file.create_display_file_lines()

    def zoom_size(self, amount):
        """ Rounds to 1 decimal place """
        self.size = max(0.5, min(1.3 if GameUnits.RES_MUL == 2 else 2.2, round(self.size + amount, 1)))
        self.update_all_items()

    def change_selected_layer(self, layer):
        """ Clamps layer between reachable values """
        self.selected_layer = max(0, min(2, layer))

    def create_editing_file(self):
        """ If it doesn't exist, creates new file in level directory for editing, on creation it is an exact copy of it level """
        with open(self.EDITING_LEVEL_FILE, 'w+') as editing_file:
            with open(self.SOURCE_LEVEL_FILE) as source_file:
                contents = source_file.read()
            editing_file.write(contents)

    def editing_file_exists(self) -> bool:
        """ Returns whether an editing file for the selected level exists """
        return os.path.exists(self.EDITING_LEVEL_FILE)

    def update_display_text(self):
        """ Updates the display text to match that of the opened file """
        self.display_text = self.font.render(f"level: {self.opened_level_file.split('/')[-1:][0]}", True, (255, 255, 0))

    def update_opened_level_file(self):
        """ Used to update the opened file, if an editor exists set to that, else set to the source file """
        if self.editing_file_exists():
            self.editing_file = FileDisplayer(self.screen, self.EDITING_LEVEL_FILE, pg.Vector2(225, 40), size=7)
            if self.opened_level_file != self.EDITING_LEVEL_FILE:
                self.opened_level_file = self.EDITING_LEVEL_FILE
        else:
            self.opened_level_file = self.SOURCE_LEVEL_FILE
            self.editing_file = None