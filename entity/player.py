import copy
import time

import pygame as pg

from conductor.conductor import Conductor
from constants import GameUnits, DirectionalValues, PlayerValues
from rendering.animator import Animator
from rendering.shadow import Shadow
from rendering.split_sheet import split_sheet
from rendering.sprites_holder import SpriteSheet
from texture_constants import PlayerTextures
from utility.logging import Logger
from utility.text_object import TextObjectsHolder
from level.area import Area


class Player:
    def __init__(self, game):
        self.logger: Logger = game.logger
        self.conductor: Conductor = game.conductor
        self.txt_holder: TextObjectsHolder = game.text_objects_holder
        self.area: Area = game.area

        # positional stuff
        self.direction = DirectionalValues.UP
        self.held_direction_keys = []
        self.position = pg.Vector2(game.screen_canvas.get_rect().center)

        self.miss_next_beat = False
        self.is_performing_action = False
        self.sprinting = False
        self.last_action_time = time.time()

        # texture stuff
        self.flipped = False

        jump_horizontal_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_HORIZONTAL, (GameUnits.UNIT * 2, GameUnits.UNIT * 2), 8)
        jump_horizontal_stunted_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_HORIZONTAL_STUNTED, (GameUnits.UNIT * 2, GameUnits.UNIT * 2), 8)
        jump_vertical_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_VERTICAL, (GameUnits.UNIT, GameUnits.UNIT * 3), 8)
        jump_vertical_stunted_ss = SpriteSheet(PlayerTextures.PLAYER_JUMP_VERTICAL_STUNTED, (GameUnits.UNIT, GameUnits.UNIT * 3), 8)

        self.animator = Animator(SpriteSheet(PlayerTextures.PLAYER_IDLE, (GameUnits.UNIT, GameUnits.UNIT), 4), pg.Vector2(0, 0),
                                 jump_horizontal_ss, jump_horizontal_stunted_ss, jump_vertical_ss, jump_vertical_stunted_ss)

        self.current_texture = self.animator.texture_obj
        self.shadow = Shadow(self.get_sprite(), self.position)

    def on_shadow_beat(self, prev_shadow_beat_time):
        """ Called on the perfect beat """
        self.animator.on_shadow_beat(prev_shadow_beat_time)

    def on_bpm_change(self, new_bpm):
        self.animator.on_bpm_change(new_bpm)

    def on_key_down(self, key):
        if key in DirectionalValues.DIRECTION_DICT:
            self.held_direction_keys.append(key)

            # action
            if self.can_do_action():
                self.direction = DirectionalValues.DIRECTION_DICT[self.held_direction_keys[0]]
                self.do_action()

    def on_key_up(self, key):
        if key in self.held_direction_keys:
            self.held_direction_keys.remove(key)

    def do_action(self):
        """ Performs players action based on stuff.
            Sends the beat event to the conductor. """
        self.is_performing_action = True
        x = DirectionalValues.DIRECTION_MOV[self.direction][0]
        y = DirectionalValues.DIRECTION_MOV[self.direction][1]

        # PERFORM ACTIONS HERE
        self.move_or_collide(x, y)

        # after action
        self.last_action_time = time.time()
        self.flipped = True if self.direction == DirectionalValues.LEFT else False if self.direction == DirectionalValues.RIGHT else self.flipped
        self.is_performing_action = False

        # change level (if: changes, then assigns, then checks)
        if level_change_dir := self.area.change_level_if_needed(self.get_relative_pos()):
            self.set_pos_on_lvl_change(level_change_dir)

        # beat the actual beat. After player movement
        self.conductor.beat()

    def move_or_collide(self, x, y):
        """ Move to tile facing, or collide """
        new_pos = pg.Vector2(self.position.x + x, self.position.y + y)
        if self.get_relative_pos(new_pos) not in self.area.level.relative_wall_positions:
            self.position = new_pos
            # move animation
            if x:
                self.animator.do_animation(PlayerTextures.PLAYER_JUMP_HORIZONTAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED,
                                           offset=pg.Vector2(-x / 2, -GameUnits.UNIT / 2))  # jump anim horizontal
            else:
                self.animator.do_animation(PlayerTextures.PLAYER_JUMP_VERTICAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED,
                                           offset=pg.Vector2(0, 0 if y < 0 else -GameUnits.UNIT),
                                           reverse=y > 0)  # jump anim vertical
                self.shadow.add_offset_goal(len(self.animator.current_ot_anim_ss),
                                            pg.Vector2(GameUnits.UNIT / 2, -GameUnits.UNIT / 2), y > 0)
        else:
            # collision animation
            if x:
                self.animator.do_animation(PlayerTextures.PLAYER_JUMP_HORIZONTAL_STUNTED,
                                           PlayerValues.PLAYER_MOVE_ANIM_SPEED,
                                           offset=pg.Vector2(x / 2, -GameUnits.UNIT / 2))
            else:
                self.animator.do_animation(PlayerTextures.PLAYER_JUMP_VERTICAL_STUNTED,
                                           PlayerValues.PLAYER_MOVE_ANIM_SPEED, offset=pg.Vector2(0, -GameUnits.UNIT))

    def sprint_manager(self):
        """ Used for holding movement keys when not in combat """
        if not self.conductor.is_in_combat:
            if len(self.held_direction_keys) > 0:
                if DirectionalValues.DIRECTION_DICT.get(self.held_direction_keys[0]) and self.can_do_action():
                    if not self.sprinting and time.time() - self.last_action_time > PlayerValues.HOLD_TIME_TO_SPRINT:
                        self.sprinting = True  # start sprint
                    elif self.sprinting:
                        self.direction = DirectionalValues.DIRECTION_DICT[self.held_direction_keys[0]]
                        self.do_action()  # continue sprint
            elif len(self.held_direction_keys) == 0 and self.sprinting:
                self.sprinting = False  # stop sprint

    def render_player(self, surface):
        self.animator.update()
        if self.animator.has_changed_texture:
            self.on_sprite_updated()
            self.animator.has_changed_texture = False

        # shadow
        self.shadow.draw(surface)

        # player
        pos = pg.Vector2((self.position.x - self.get_sprite().get_width() / 2) + self.animator.offset.x,
                          (self.position.y - self.get_sprite().get_height() / 2) + self.animator.offset.y)
        surface.blit(self.get_sprite(), pg.Vector2(pos.x, pos.y + GameUnits.ENTITY_Y_OFFSET))
        pg.draw.rect(surface, (255, 0, 0), pg.rect.Rect(self.position.x, self.position.y, 3, 3), 2)

    def on_sprite_updated(self):
        """ Called when sprite updates its texture """
        self.current_texture = self.animator.texture_obj

        self.shadow.update_shadow(self.position, self.get_sprite(), self.animator.offset)

    def get_sprite(self) -> pg.surface.Surface:
        """ Always use this to get the player sprite. Just flips the sprite if it needs to """
        return pg.transform.flip(self.current_texture, True if self.flipped else False, False)

    def set_pos(self, new_pos: pg.Vector2):
        """ Sets player position instantly """
        self.is_performing_action = True
        self.position = new_pos
        self.last_action_time = time.time()
        self.is_performing_action = False

    def can_do_action(self) -> bool:
        """ Returns true if the player is allowed to do an action, results will vary in and out of combat """
        # skip. This is reset in Games' on_beat(is_auto_beat = True)
        if self.miss_next_beat:
            return False

        # checks
        can_perform_action: bool = (not self.is_performing_action
                                    and not self.animator.current_ot_anim_ss
                                    and time.time() - PlayerValues.MOVEMENT_PAUSE > self.last_action_time)

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

    def get_relative_pos(self, pos=None) -> pg.Vector2:
        """ Returns the smallest int of the players' current position """
        if not pos:
            pos = self.position
        return pg.Vector2((pos.x - GameUnits.LEVEL_X_OFFSET) / GameUnits.UNIT,
                          pos.y / GameUnits.UNIT)

    def get_pos_from_relative(self, rel_pos: pg.Vector2 | None = None) -> pg.Vector2:
        """ Returns the players actual position from a relative """
        if not rel_pos:
            rel_pos = self.get_relative_pos()
        return pg.Vector2((rel_pos.x * GameUnits.UNIT) + GameUnits.LEVEL_X_OFFSET,
                          rel_pos.y * GameUnits.UNIT)
