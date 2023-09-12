from level.level import Level
from level_editor.buttons import ButtonOutlined
from constants import EDITING_TAG
import pygame as pg
import os


class LevelEditor:
    """ to handle rendering & buttons & stuff """
    def __init__(self, screen: pg.surface.Surface, level_file: str, position: pg.Vector2, size):
        self.screen = screen
        self.SOURCE_LEVEL_FILE = level_file
        self.EDITING_LEVEL_FILE = f"{level_file}{EDITING_TAG}"
        self.SOURCE_LEVEL_DIR = '/'.join(self.SOURCE_LEVEL_FILE.split('/')[:-1])  # removes ending file from path
        self.opened_level_file = self.SOURCE_LEVEL_FILE  # only change this
        self.update_opened_level_file()

        self.size = size
        self.position = position
        self.lvl_pos = pg.Vector2(position.x + 20, position.y + 80)

        self.font = pg.font.SysFont('Times New Roman', max(20, 3))
        self.display_text = None
        self.update_display_text()

        self.level = Level(screen, self.opened_level_file if not self.editing_file_exists() else self.EDITING_LEVEL_FILE, pos_offset=self.lvl_pos, size=size)
        self.buttons: list[ButtonOutlined] = []
        self.create_editing_buttons()

        self.selected_tile = '  '

    def render(self):
        # level text
        self.screen.blit(self.display_text, self.position)

        # level
        self.level.render_level()
        self.level.render_level_foreground()

        # editor
        for button in self.buttons:
            button.render()

    def create_editing_buttons(self):
        for tile_rect in self.level.generate_tile_rects():
            pos = pg.Vector2(tile_rect[0], tile_rect[1])
            size = (tile_rect[2], tile_rect[3])
            operation = (tile_rect[4], tile_rect[5])
            self.add_button('', pos, operation, override_size=size)

    def add_button(self, display_text: str, pos: pg.Vector2, operation: tuple, size=30, image=None, override_size=None):
        self.buttons.append(ButtonOutlined(screen=self.screen, display_text=display_text, image=image, pos=pos, operation=operation, size=size, override_size=override_size))

    def mouse_clicked(self):
        for btn in self.buttons:
            if btn.is_mouse_in_bounds():
                self.change_tile(btn.operation[1], btn.operation[0])

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

        self.update_opened_level_file()
        self.update_display_text()
        self.level.reload_or_load_level(self.opened_level_file)

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
        self.display_text = self.font.render(f"level: {self.opened_level_file.split('/')[-1:][0]}", True, (255, 255, 0))

    def update_opened_level_file(self):
        if self.editing_file_exists():
            if self.opened_level_file != self.EDITING_LEVEL_FILE:
                self.opened_level_file = self.EDITING_LEVEL_FILE
