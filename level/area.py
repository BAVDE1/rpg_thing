import os

import pygame as pg

from constants import GameUnits, DirectionalValues
from level.level import Level

AREAS_DIR = "./assets/areas"

AREA_LAYOUT_ADDITIONS = {
    DirectionalValues.NORTH: -1,
    DirectionalValues.SOUTH: 1,
    DirectionalValues.EAST: 1,
    DirectionalValues.WEST: -1
}


def check_exists(path: str, not_found_msg: str) -> bool:
    if not os.path.exists(path):
        raise NotADirectoryError(not_found_msg)
    return True


def get_lvl_files(area: str, area_path_dir: str) -> dict:
    di = {}

    files_in_area = sorted(os.listdir(area_path_dir))
    for file in files_in_area:
        file = file.split(".")[0]
        if file != area:
            lvl_num = file.split("_")[1]
            if lvl_num in di:
                raise IndexError(f"The level number '{lvl_num}' already exists in the directory '{area_path_dir}'")
            di[lvl_num] = f"{file}.txt"

    return di


class Area:
    def __init__(self, game, area: str):
        self.game = game
        self.area_dir = f"{AREAS_DIR}/{area}"
        self.area_layout_file = f"{self.area_dir}/{area}.txt"

        check_exists(self.area_dir, f"Directory '{area}' does not exist in '{AREAS_DIR}'")
        check_exists(self.area_layout_file, f"Layout file '{area}.txt' does not exist in '{self.area_dir}'")

        self.area_layout = []
        with open(self.area_layout_file) as file:
            self.area_layout = [line.strip().strip("[").strip("]").split(",") for line in file]

        self.level_files_dict = get_lvl_files(area, self.area_dir)

        self.levels_dict = {}
        self.load_levels()

        self.current_lvl_num = "00"  # read from save or something
        self.level: Level = self.levels_dict[self.current_lvl_num]

    def load_levels(self):
        """ Stores levels in area dictionary """
        for level_num in self.level_files_dict:
            self.levels_dict[level_num] = Level(f"{self.area_dir}/{self.level_files_dict[level_num]}",
                                                pos_offset=pg.Vector2(GameUnits.LEVEL_OFFSET, 0))

    def change_level_by_direction(self, directional_value):
        """ Changes level by cardinal direction. Raises errors if the move is invalid. """
        if directional_value:
            n, s, e, w = DirectionalValues.NORTH, DirectionalValues.SOUTH, DirectionalValues.EAST, DirectionalValues.WEST

            # incorrect direction value
            if directional_value not in (n, s, e, w):
                raise IndexError(f"Directional value '{directional_value}', is not allowed. Please only use 'NORTH', 'SOUTH', 'EAST' or 'WEST'")

            # get current level position in layout file
            on_row = 0
            on_col = 0
            for r, row in enumerate(self.area_layout):
                for c, col in enumerate(row):
                    if self.area_layout[r][c] == self.current_lvl_num:
                        on_row = r
                        on_col = c
                        break

            # choose direction & lvl num
            if directional_value in (n, s):
                on_row += AREA_LAYOUT_ADDITIONS[directional_value]
                lerp_vec = pg.Vector2(0, (5 * GameUnits.RES_MUL))
            else:
                on_col += AREA_LAYOUT_ADDITIONS[directional_value]
                lerp_vec = pg.Vector2((5 * GameUnits.RES_MUL), 0)
            new_lvl_num = self.area_layout[on_row][on_col]

            # lerp
            self.game.screen_lerper.set_lerp(lerp_vec, 0.3, True, False if AREA_LAYOUT_ADDITIONS[directional_value] > 0 else True)

            # set new level
            self.current_lvl_num = new_lvl_num
            self.level = self.levels_dict[self.current_lvl_num]
            self.game.on_level_change(directional_value)

    def change_level_if_needed(self, player_relative_pos: pg.Vector2):
        """ Changes the level if it needs to.\n
            Returns the direction the level is changed after the level gets changed, or None.\n
            Should be called every time the player moves, or gets moved. """
        direction = None
        if player_relative_pos.y in DirectionalValues.LEVEL_EDGE_Y:
            direction = DirectionalValues.LEVEL_EDGE_Y[player_relative_pos.y]
        elif player_relative_pos.x in DirectionalValues.LEVEL_EDGE_X:
            direction = DirectionalValues.LEVEL_EDGE_X[player_relative_pos.x]
        self.change_level_by_direction(direction)
        return direction
