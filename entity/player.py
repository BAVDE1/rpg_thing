import time
import pygame as pg
from constants import GameUnits, DirectionalValues, PlayerValues
from texture_constants import PlayerTextures
from rendering.split_sheet import split_sheet
from rendering.shadow import Shadow
from utility.animator import Animator


class Player:
    def __init__(self, game, screen: pg.Surface, centre_screen):
        self.game = game
        self.surface = screen

        # positional stuff
        self.direction = DirectionalValues.UP
        self.position = pg.Vector2(centre_screen[0], centre_screen[1])

        self.moving = False
        self.sprinting = False
        self.last_moved = time.time()

        # texture stuff
        self.texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE).convert_alpha()
        self.ss_idle = split_sheet(self.texture_idle, (GameUnits.BASE_UNIT, GameUnits.BASE_UNIT), 4)

        self.flipped = False
        self.shadow = None
        self.current_texture = None

        self.animator = Animator(self.game, [PlayerTextures.PLAYER_IDLE, self.ss_idle], pg.Vector2(0, 0), False,
                                 [PlayerTextures.PLAYER_JUMP_HORIZONTAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_HORIZONTAL).convert_alpha(), (GameUnits.BASE_UNIT * 2, GameUnits.BASE_UNIT * 2), 8)],
                                 [PlayerTextures.PLAYER_JUMP_VERTICAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_VERTICAL).convert_alpha(), (GameUnits.BASE_UNIT, GameUnits.BASE_UNIT * 3), 8)])

    def move(self):
        """ Moves player 1 tile in its current direction """
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

        # todo: send beat event (after player movement)

        self.moving = False

    def render_player(self):
        # holds function until player is loaded
        while not self.is_player_loaded():
            self.load_player()

        # updates
        self.animator.update()
        if self.animator.has_changed_texture:
            self.sprite_updated()
            self.animator.has_changed_texture = False

        sprite = self.get_sprite()
        blit = ((self.position.x - sprite.get_width() / 2) + self.animator.offset.x,
                (self.position.y - sprite.get_height() / 2) + self.animator.offset.y)

        # shadow
        self.shadow.draw()

        # player
        self.surface.blit(sprite, blit)

    def sprite_updated(self):
        """ Called when sprite updates its texture """
        self.current_texture = self.animator.texture_obj

        self.shadow.update_shadow(self.position, self.get_sprite(), self.animator.offset)

    def get_sprite(self) -> pg.surface.Surface:
        """ Always use this to get the player sprite """
        scaled_sprite = pg.transform.scale(self.current_texture, (self.current_texture.get_width() * GameUnits.RES_MUL, self.current_texture.get_height() * GameUnits.RES_MUL))
        flipped_sprite = pg.transform.flip(scaled_sprite, True if self.flipped else False, False)
        return flipped_sprite

    def is_player_loaded(self) -> bool:
        """ Returns whether player has fully loaded in (add more checks later) """
        return self.current_texture and self.shadow

    def can_move(self):
        """ Returns true if the player is allowed to move """
        return not self.moving and not self.animator.current_anim_ss and time.time() - PlayerValues.MOVEMENT_PAUSE > self.last_moved

    def set_pos(self, x, y):
        """ Sets player position & sprite pos instantly """
        self.moving = True
        self.position.x = x
        self.position.y = y
        self.last_moved = time.time()
        self.moving = False

    def load_player(self):
        """ Used to initialise player textures, will continue to be called as long as the player is not yet loaded """
        if not self.current_texture:
            self.animator.update()
            self.current_texture = self.animator.texture_obj
            return

        if not self.shadow and self.current_texture is not None:
            self.shadow = Shadow(self.surface, self.get_sprite(), self.position)
