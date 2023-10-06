from constants import GameUnits, DirectionalValues, LevelLocations
from texture_constants import get_outline_tileset_dict, TileTextures, ASCII_TO_SPRITE
from rendering.sprites_holder import TileSprite
from entity.base_entity import ASCII_TO_ENTITY, BaseEntity
import os
import pygame as pg


def parse_level_file(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError(
            f"level file {level_source} could not be found. Was there a typo; was the directory not properly declared?")

    seperator_count = 0
    layers_dict: dict[int:list] = {}

    with open(level_source) as file:
        for line in file:
            line = line.strip().strip("[").strip("]")

            # seperator
            if line == LevelLocations.LEVEL_LAYER_SEPERATOR:
                seperator_count += 1
                continue

            # add line to dict
            if seperator_count in layers_dict:
                layers_dict[seperator_count].append(line)
            else:
                layers_dict[seperator_count] = [line]
    return layers_dict


def outline_decider(dic: dict):
    """ Returns suitable outline for tiles' position depending upon its surrounding tiles.
        Returns None if no suitable outline is found """
    outlines = get_outline_tileset_dict(TileTextures.LEAVES_TILESET_IMAGES)

    sprite_to_add = None
    for sprite in outlines.keys():
        found_suitable_sprite = True
        for requirement in outlines[sprite]:  # if even one requirement is not met, 'found_suitable_sprite' will be false
            found_suitable_sprite = False if bool(dic[requirement]) != outlines[sprite][requirement] else found_suitable_sprite

        if found_suitable_sprite:
            sprite_to_add = sprite
            break  # stop loop once it finds a suitable tile

    return sprite_to_add


def store_layer(layer: list, layer_lines):
    """ Generates a list of split lines of the level file given
     eg: [[  ,Gr,Gr,  ], [Gr,Gr,Gr,  ]]
     """
    for line in layer_lines:
        row = [ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None for chars in line.split(',')]
        layer.append(row)


class Level:
    def __init__(self, game, level_source, pos_offset: pg.Vector2 = pg.Vector2(0, 0), size=1):
        self.is_initialised = False
        self.game = game
        self.pos_offset = pos_offset
        self.size = size

        self.level_source = level_source

        self.whole_level = parse_level_file(self.level_source)
        self.top_layer_lines = self.whole_level[0]
        self.entity_layer_lines = self.whole_level[1]
        self.ground_layer_lines = self.whole_level[2]

        self.top_layer_group = pg.sprite.Group()
        self.ground_layer_group = pg.sprite.Group()
        self.ground_grid_group = pg.sprite.Group()
        self.outline_layer_group = pg.sprite.Group()

        # collide-able positions
        self.relative_wall_positions = []

        self.entities: list[BaseEntity] = []

        # initializes level
        self.initialise_level()

    def load_or_reload_level(self, new_level_source=None):
        """ Reloads level with the option of using a different level file """
        if new_level_source:
            self.level_source = new_level_source

        self.is_initialised = False

        self.whole_level = parse_level_file(self.level_source)
        self.top_layer_lines = self.whole_level[0]
        self.entity_layer_lines = self.whole_level[1]
        self.ground_layer_lines = self.whole_level[2]

        self.top_layer_group.empty()
        self.ground_layer_group.empty()
        self.outline_layer_group.empty()

        self.relative_wall_positions = []
        self.entities: list[BaseEntity] = []

        self.initialise_level()

    def initialise_level(self):
        if not self.is_initialised:
            # create tiles & fill groups
            self.store_group(self.ground_layer_group, self.ground_layer_lines, store_empty_as_walls=True)
            self.store_group(self.top_layer_group, self.top_layer_lines, store_tiles_as_walls=True)
            self.store_grid()
            self.store_entities()
            self.store_outline(True)

            # finish
            self.is_initialised = True

    def render_level(self, surface):
        """ Called every frame """
        if self.is_initialised:
            self.ground_layer_group.draw(surface)
            self.top_layer_group.draw(surface)

    def render_entities(self, surface):
        for entity in self.entities:
            entity.render(surface)

    def render_level_foreground(self, surface):
        """ Called every frame (after other things have been rendered) """
        if self.is_initialised:
            self.outline_layer_group.draw(surface)

    def store_group(self, group: pg.sprite.Group, layer_lines, store_empty_as_walls=False, store_tiles_as_walls=False):
        """ Converts ascii chars from layer_lines into valid TileSprites and stores them into the given group """
        for row_n, line in enumerate(layer_lines):
            for column_n, chars in enumerate(line.split(",")):
                if raw_sprite := ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None:
                    raw_sprite = self.create_scaled_tile_sprite(raw_sprite)
                    t_pos = self.create_tile_pos(row_n, column_n)

                    tile_sprite = TileSprite(raw_sprite, t_pos)

                    if store_tiles_as_walls:
                        self.relative_wall_positions.append(tile_sprite.relative_pos)

                    tile_sprite.add(group)
                elif store_empty_as_walls:
                    self.relative_wall_positions.append(TileSprite(TileTextures.GRASS_IMAGE, self.create_tile_pos(row_n, column_n)).relative_pos)

    def store_grid(self):
        for r in range(GameUnits.LVL_HEIGHT):
            for c in range(GameUnits.LVL_WIDTH):
                if c % 2 == 0:
                    if (r + 1) % 2 == 0:
                        self.ground_grid_group.add(pg.sprite.)
                        print(r, c)
                else:
                    if r % 2 == 0:
                        print(r, c)

    def store_entities(self):
        for row_n, line in enumerate(self.entity_layer_lines):
            for column_n, chars in enumerate(line.split(",")):
                if raw_entity := ASCII_TO_ENTITY[chars] if chars in ASCII_TO_ENTITY else None:
                    pos = self.create_entity_pos(row_n, column_n)

                    self.entities.append(raw_entity(self.game, pos))

    def store_outline(self, store_fade=False):
        """ Used to determine and put sprites into the outline group """
        ground_layer_bools = []
        for line in self.ground_layer_lines:
            row = [1 if chars in ASCII_TO_SPRITE else 0 for chars in line.split(',')]
            ground_layer_bools.append(row)

        for row_n, line in enumerate(ground_layer_bools):
            for column_n, chars in enumerate(line):
                north_t = max(0, row_n - 1)
                south_t = min(len(ground_layer_bools) - 1, row_n + 1)
                east_t = min(len(line) - 1, column_n + 1)
                west_t = max(0, column_n - 1)

                cardinal_dic = {
                    DirectionalValues.TILE: chars,
                    DirectionalValues.NORTH: ground_layer_bools[north_t][column_n],
                    DirectionalValues.SOUTH: ground_layer_bools[south_t][column_n],
                    DirectionalValues.EAST: ground_layer_bools[row_n][east_t],
                    DirectionalValues.WEST: ground_layer_bools[row_n][west_t],
                    DirectionalValues.NORTH_EAST: ground_layer_bools[north_t][east_t],
                    DirectionalValues.NORTH_WEST: ground_layer_bools[north_t][west_t],
                    DirectionalValues.SOUTH_EAST: ground_layer_bools[south_t][east_t],
                    DirectionalValues.SOUTH_WEST: ground_layer_bools[south_t][west_t]
                }

                if raw_sprite := outline_decider(cardinal_dic):
                    raw_sprite = self.create_scaled_tile_sprite(raw_sprite)
                    t_pos = self.create_tile_pos(row_n, column_n)

                    tile_sprite = TileSprite(raw_sprite, t_pos)
                    tile_sprite.add(self.outline_layer_group)

                # store fade tiles after other tiles, so it renders on top
                if store_fade and (column_n == 0 or column_n == len(line) - 1):  # only on the level sides atm
                    f_raw_sprite = pg.transform.flip(TileTextures.FADE_IMAGE, 1, 0) if column_n == 0 else TileTextures.FADE_IMAGE
                    f_raw_sprite = self.create_scaled_tile_sprite(f_raw_sprite)
                    f_pos = self.create_tile_pos(row_n, column_n)

                    f_tile_sprite = TileSprite(f_raw_sprite, f_pos)
                    f_tile_sprite.add(self.outline_layer_group)

    def create_scaled_tile_sprite(self, sprite) -> pg.surface.Surface:
        """ Returns given sprite scaled to areas' size """
        return pg.transform.scale(sprite, (sprite.get_width() * self.size, sprite.get_height() * self.size))

    def create_tile_pos(self, row: int, column: int) -> pg.Vector2:
        """ Returns Vector2 of a given sprites position depending upon row, column and level size """
        return pg.Vector2(
            (((column * GameUnits.UNIT) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.x,
            (((row * GameUnits.UNIT) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.y)

    def create_entity_pos(self, row: int, column: int) -> pg.Vector2:
        """ Returns Vector2 of a given sprites position depending upon row, column and level size """
        return pg.Vector2(
            ((((column * GameUnits.UNIT) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.x) + GameUnits.UNIT / 2,
            ((((row * GameUnits.UNIT) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.y) + GameUnits.UNIT / 2)

    def generate_tile_rects(self) -> list[tuple]:
        """ Generates and returns a list of tile rects: 0=x, 1=y, 2=width, 3=height, 4=row, 5=column (used in level editor) """
        li: list[tuple] = []
        for row_n in range(GameUnits.LVL_HEIGHT + 1):
            for column_n in range(GameUnits.LVL_WIDTH + 1):
                tile_pos = self.create_tile_pos(row_n, column_n)
                li.append((tile_pos.x, tile_pos.y, GameUnits.UNIT * self.size, GameUnits.UNIT * self.size, column_n, row_n))
        return li

    def __repr__(self):
        return f"Level({self.level_source}, entities_alive:{len(self.entities)})"
