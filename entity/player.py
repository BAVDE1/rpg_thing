import copy
import time

import pygame as pg

from conductor.conductor import Conductor
from constants import GameUnits, DirectionalValues, PlayerValues
from level.area import Area
from rendering.animator import Animator
from rendering.shadow import Shadow
from rendering.split_sheet import split_sheet
from rendering.sprites_holder import SpriteSheet
from texture_constants import PlayerTextures
from utility.logging import Logger
from utility.text_object import TextObjectsHolder


class Player:
    def __init__(self, game, screen: pg.Surface, centre_screen):
        self.logger: Logger = game.logger
        self.conductor: Conductor = game.conductor
        self.txt_holder: TextObjectsHolder = game.text_objects_holder
        self.area: Area = game.area
        self.surface = screen

        # positional stuff
        self.direction = DirectionalValues.UP
        self.held_direction_keys = []
        self.position = pg.Vector2(centre_screen[0], centre_screen[1])

        self.miss_next_beat = False
        self.moving = False
        self.sprinting = False
        self.last_moved = time.time()

        # texture stuff
        self.texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE).convert_alpha()
        self.ss_idle = split_sheet(self.texture_idle, (GameUnits.UNIT, GameUnits.UNIT), 4)

        self.flipped = False
        self.shadow = None
        self.current_texture = None

        jump_horizontal_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_HORIZONTAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_HORIZONTAL).convert_alpha(), (GameUnits.UNIT * 2, GameUnits.UNIT * 2), 8))
        jump_vertical_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_VERTICAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_VERTICAL).convert_alpha(), (GameUnits.UNIT, GameUnits.UNIT * 3), 8))
        self.animator = Animator(self.logger, self.conductor, pg.Vector2(0, 0),
                                 SpriteSheet(PlayerTextures.PLAYER_IDLE, self.ss_idle),
                                 jump_horizontal_ss, jump_vertical_ss)

    def on_shadow_beat(self):
        """ Called on the perfect beat """
        self.animator.on_shadow_beat()

    def on_key_down(self, key):
        if key in DirectionalValues.DIRECTION_DICT:
            self.held_direction_keys.append(key)

            # action
            if self.can_do_action():
                self.direction = DirectionalValues.DIRECTION_DICT[self.held_direction_keys[0]]
                self.move()

    def on_key_up(self, key):
        if key in self.held_direction_keys:
            self.held_direction_keys.remove(key)

    def move(self):
        """ Moves player 1 tile in its current direction
            Sends the beat event to the conductor. """
        self.moving = True

        x = DirectionalValues.DIRECTION_MOV[self.direction][0]
        y = DirectionalValues.DIRECTION_MOV[self.direction][1]
        self.position = pg.Vector2(self.position.x + x, self.position.y + y)
        self.last_moved = time.time()

        self.flipped = True if self.direction == DirectionalValues.LEFT else False if self.direction == DirectionalValues.RIGHT else self.flipped

        # move animation
        if x:
            self.animator.do_animation(PlayerTextures.PLAYER_JUMP_HORIZONTAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED, offset=pg.Vector2(-x / 2, -GameUnits.UNIT / 2))  # jump anim horizontal
        else:
            self.animator.do_animation(PlayerTextures.PLAYER_JUMP_VERTICAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED, offset=pg.Vector2(0, 0 if y < 0 else -GameUnits.UNIT), reverse=y > 0)  # jump anim vertical
            self.shadow.add_offset_goal(len(self.animator.current_ot_anim_ss), pg.Vector2(GameUnits.UNIT / 2, -GameUnits.UNIT / 2), y > 0)

        self.moving = False

        # change level (changes, then assigns, then checks if)
        if level_change_dir := self.area.change_level_if_needed(self.get_relative_pos()):
            self.set_pos_on_lvl_change(level_change_dir)

        # beat the actual beat. After player movement
        self.conductor.beat()

    def sprint_manager(self):
        """ Used for holding movement keys when not in combat """
        if not self.conductor.is_in_combat:
            if len(self.held_direction_keys) > 0:
                if DirectionalValues.DIRECTION_DICT.get(self.held_direction_keys[0]) and self.can_do_action():
                    if not self.sprinting and time.time() - self.last_moved > PlayerValues.HOLD_TIME_TO_SPRINT:
                        self.sprinting = True  # start sprint
                    elif self.sprinting:
                        self.direction = DirectionalValues.DIRECTION_DICT[self.held_direction_keys[0]]
                        self.move()  # continue sprint
            elif len(self.held_direction_keys) == 0 and self.sprinting:
                self.sprinting = False  # stop sprint

    def render_player(self):
        # holds function until player is loaded
        while not self.is_player_loaded():
            self.load_player()

        # updates
        self.animator.update()
        if self.animator.has_changed_texture:
            self.on_sprite_updated()
            self.animator.has_changed_texture = False

        sprite = self.get_sprite()
        blit = ((self.position.x - sprite.get_width() / 2) + self.animator.offset.x,
                (self.position.y - sprite.get_height() / 2) + self.animator.offset.y)

        # shadow
        self.shadow.draw()

        # player
        self.surface.blit(sprite, blit)

    def on_sprite_updated(self):
        """ Called when sprite updates its texture """
        self.current_texture = self.animator.texture_obj

        self.shadow.update_shadow(self.position, self.get_sprite(), self.animator.offset)

    def get_sprite(self) -> pg.surface.Surface:
        """ Always use this to get the player sprite """
        flipped_sprite = pg.transform.flip(self.current_texture, True if self.flipped else False, False)
        return flipped_sprite

    def load_player(self):
        """ Used to initialise player textures, will continue to be called as long as the player is not yet loaded.
            Probably needs to be called twice before player is fully loaded? Maybe? """
        if not self.current_texture:
            self.animator.update()
            self.current_texture = self.animator.texture_obj
            return

        if not self.shadow and self.current_texture is not None:
            self.shadow = Shadow(self.surface, self.get_sprite(), self.position, self.logger)

    def set_pos(self, new_pos: pg.Vector2):
        """ Sets player position instantly """
        self.moving = True
        self.position = new_pos
        self.last_moved = time.time()
        self.moving = False

    def is_player_loaded(self) -> bool:
        """ Returns whether player has fully loaded in (add more checks later). Call player.Render() to load """
        return self.current_texture and self.shadow

    def can_do_action(self) -> bool:
        """ Returns true if the player is allowed to do an action, results will vary in and out of combat """
        # skip. This is reset in Games' on_beat(is_auto_beat = True)
        if self.miss_next_beat:
            return False

        # checks
        can_perform_action: bool = (not self.moving
                                    and not self.animator.current_ot_anim_ss
                                    and time.time() - PlayerValues.MOVEMENT_PAUSE > self.last_moved)

        # out of combat movement
        if not self.conductor.is_in_combat:
            return can_perform_action

        # in-combat movement
        if self.conductor.is_now_within_allowed_beat():
            return can_perform_action

        # missed an in-combat beat
        self.missed_beat()
        return False

    def missed_beat(self):
        self.txt_holder.add_text_object("Missed beat", pg.Vector2(self.position.x, self.position.y - 23))
        self.miss_next_beat = True

        self.logger.add_log(f"Missed beat", 2)

    def set_pos_on_lvl_change(self, direction):
        """ Sets the player's position based upon a level change direction """
        # deepcopy required here otherwise the updated rel_pos will be updating the vector2 in the constant dict
        rel_pos = copy.deepcopy(PlayerValues.LVL_CHANGE_DIR_TO_POS)[direction]

        # set the empty values
        rel_pos.y = self.get_relative_pos().y if not rel_pos.y else rel_pos.y
        rel_pos.x = self.get_relative_pos().x if not rel_pos.x else rel_pos.x

        self.set_pos(self.get_pos_from_relative(rel_pos))

    def get_relative_pos(self) -> pg.Vector2:
        """ Returns the smallest int of the players' current position """
        return pg.Vector2((self.position.x - GameUnits.LEVEL_OFFSET) / GameUnits.UNIT,
                          self.position.y / GameUnits.UNIT)

    def get_pos_from_relative(self, rel_pos: pg.Vector2 | None = None) -> pg.Vector2:
        """ Returns the players actual position from a relative """
        if not rel_pos:
            rel_pos = self.get_relative_pos()
        return pg.Vector2((rel_pos.x * GameUnits.UNIT) + GameUnits.LEVEL_OFFSET,
                          rel_pos.y * GameUnits.UNIT)
