from level.level import Level
from level_editor.buttons import ButtonOutlined, Button, BTNOperation
from level_editor.file_displayer import FileDisplayer
from constants import EDITING_TAG
from texture_constants import ASCII_TO_SPRITE
from level_editor.le_constants import *
import pygame as pg
import os


class TileOption:
    def __init__(self, screen: pg.surface.Surface, tile_chars: str, tile_sprite: pg.surface.Surface, position: pg.Vector2, scale=1):
        self.screen = screen
        self.pos = position

        self.tile_chars = tile_chars
        self.txt_size = 20
        self.tile_sprite = pg.transform.scale(tile_sprite, (tile_sprite.get_width() * scale, tile_sprite.get_height() * scale))

        self.button = Button(screen, tile_chars, self.tile_sprite, position, BTNOperation(BTN_TILE_OPTION, tile_chars), text_size=self.txt_size,
                             override_size=(self.tile_sprite.get_width(), self.tile_sprite.get_height() + self.txt_size))


class Hotbar:
    def __init__(self):
        self.max_size = 6
        self.tile_options: list[TileOption] = []

    def add_tile_option(self, slot: int, tile_option: TileOption):
        slot = max(1, min(6, slot))
        self.tile_options.insert(slot, tile_option)

    def render(self):
        for tile_option in self.tile_options:
            tile_option.button.render()


class TileSelector:
    def __init__(self):

        self.is_open = False

    def render(self):
        if self.is_open:
            pass


class LevelEditor:
    """ to handle rendering & buttons & stuff """
    def __init__(self, screen: pg.surface.Surface, level_file: str, position: pg.Vector2, size):
        self.screen = screen

        self.SOURCE_LEVEL_FILE = level_file
        self.EDITING_LEVEL_FILE = f"{level_file}{EDITING_TAG}"
        self.SOURCE_LEVEL_DIR = '/'.join(self.SOURCE_LEVEL_FILE.split('/')[:-1])  # removes ending file from path
        self.opened_level_file = self.SOURCE_LEVEL_FILE  # only change this
        self.update_opened_level_file()

        self.font = pg.font.SysFont('Times New Roman', max(20, 3))
        self.display_text: pg.surface.Surface | None = None
        self.update_display_text()

        self.size = size
        self.position = position
        self.lvl_pos = pg.Vector2(position.x + 20, position.y + self.display_text.get_height() * 2)

        self.level = Level(screen, self.opened_level_file if not self.editing_file_exists() else self.EDITING_LEVEL_FILE, pos_offset=self.lvl_pos, size=size)
        self.editing_file: FileDisplayer | None = None
        self.buttons: list[ButtonOutlined | Button] = []
        self.create_editing_buttons()
        self.update_opened_level_file()

        self.selected_tile = '  '
        self.hotbar: Hotbar = Hotbar()
        self.hotbar.add_tile_option(1, TileOption(self.screen, 'Gr', ASCII_TO_SPRITE['Gr'], pg.Vector2(6, self.screen.get_height() - 70), scale=2))
        self.tile_selector: TileSelector = TileSelector()

    def render(self):
        # level text
        self.screen.blit(self.display_text, self.position)

        # editing file
        if self.editing_file:
            self.editing_file.render()

        # level
        self.level.render_level()
        self.level.render_level_foreground()

        # tile selection
        self.hotbar.render()
        self.tile_selector.render()

        # editor
        for button in self.buttons:
            button.render()

    def create_editing_buttons(self):
        for tile_rect in self.level.generate_tile_rects():
            pos = pg.Vector2(tile_rect[0], tile_rect[1])
            size = (tile_rect[2], tile_rect[3])
            operation = BTNOperation(BTN_TILE_CHANGE, (tile_rect[4], tile_rect[5]))
            self.buttons.append(ButtonOutlined(self.screen, '', None, pos, operation, override_size=size))

    def add_button(self, display_text: str, pos: pg.Vector2, operation: BTNOperation, size=30, image=None, override_size=None):
        self.buttons.append(Button(screen=self.screen, display_text=display_text, image=image, pos=pos, operation=operation, text_size=size, override_size=override_size))

    def mouse_clicked(self):
        for btn in self.buttons:
            if btn.is_mouse_in_bounds():
                btn_type = btn.operation.type
                btn_value = btn.operation.value

                if btn_type == BTN_TILE_CHANGE:
                    self.change_tile(btn_value[1], btn_value[0])

    def change_tile(self, row, column):
        """ Changes the tile to selected tile in the editing file """
        if not self.editing_file_exists():
            self.create_editing_file()

        # get lines
        lines = []
        with open(self.EDITING_LEVEL_FILE) as editing_file:
            for line in editing_file:
                lines.append(line.strip().replace("[", "").replace("]", "").split(","))

        # set tile
        lines[row][column] = self.selected_tile

        # update file
        with open(self.EDITING_LEVEL_FILE, 'w') as editing_file:
            contents = ""
            for line in lines:
                contents += f"[{','.join(line)}]\n"
            editing_file.write(contents)

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

        # reload file
        if self.editing_file:
            self.editing_file.create_display_file_lines()

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
            self.editing_file = FileDisplayer(self.screen, self.EDITING_LEVEL_FILE, pg.Vector2(10, 240), 10)
            if self.opened_level_file != self.EDITING_LEVEL_FILE:
                self.opened_level_file = self.EDITING_LEVEL_FILE
        else:
            self.opened_level_file = self.SOURCE_LEVEL_FILE
            self.editing_file = None
