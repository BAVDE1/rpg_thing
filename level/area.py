import pygame as pg
import os
from level.level import Level
from constants import GameUnits, DirectionalValues
from utility.screen_movers import ScreenLerper

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
        n, s, e, w = DirectionalValues.NORTH, DirectionalValues.SOUTH, DirectionalValues.EAST, DirectionalValues.WEST

        # incorrect direction value
        if directional_value not in (n, s, e, w):
            raise IndexError(f"Directional value '{directional_value}', is not allowed. Please only use 'NORTH', 'SOUTH', 'EAST' or 'WEST'")

        on_row = 0
        on_col = 0
        for r, row in enumerate(self.area_layout):
            for c, col in enumerate(row):
                if self.area_layout[r][c] == self.current_lvl_num:
                    on_row = r
                    on_col = c
                    break

        if directional_value in (n, s):
            on_row += AREA_LAYOUT_ADDITIONS[directional_value]
            lerp_vec = pg.Vector2(0, 10)
        else:
            on_col += AREA_LAYOUT_ADDITIONS[directional_value]
            lerp_vec = pg.Vector2(10, 0)
        new_lvl_num = self.area_layout[on_row][on_col]

        # lerp
        self.game.screen_lerper.lerp_screen(lerp_vec, 0.3, True, False if AREA_LAYOUT_ADDITIONS[directional_value] > 0 else True)

        self.current_lvl_num = new_lvl_num
        self.level = self.levels_dict[self.current_lvl_num]