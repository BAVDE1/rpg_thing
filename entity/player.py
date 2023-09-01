import time
import pygame as pg
from constants import GameUnits, DirectionalValues, PlayerValues
from texture_constants import PlayerTextures
from rendering.split_sheet import split_sheet
from rendering.shadow import render_shadow
from utility.animator import Animator


class Player:
    def __init__(self, game, screen: pg.Surface, centre_screen):
        self.game = game
        self.surface = screen
        self.direction = DirectionalValues.UP
        self.position = pg.Vector2(centre_screen[0], centre_screen[1])
        self.sprite_pos = self.position
        self.flipped = False

        self.texture_idle = pg.image.load(PlayerTextures.PLAYER_IDLE).convert_alpha()
        self.ss_idle = split_sheet(self.texture_idle, (GameUnits.BASE_UNIT, GameUnits.BASE_UNIT), 4)

        self.current_texture = None
        self.animator = Animator(self.game, [PlayerTextures.PLAYER_IDLE, self.ss_idle], pg.Vector2(0, 0), False,
                                 [PlayerTextures.PLAYER_JUMP_HORIZONTAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_HORIZONTAL).convert_alpha(), (GameUnits.BASE_UNIT * 2, GameUnits.BASE_UNIT * 2), 8)],
                                 [PlayerTextures.PLAYER_JUMP_VERTICAL, split_sheet(pg.image.load(PlayerTextures.PLAYER_JUMP_VERTICAL).convert_alpha(), (GameUnits.BASE_UNIT, GameUnits.BASE_UNIT * 3), 8)])

        self.moving = False
        self.sprinting = False
        self.last_moved = time.time()

    def move(self):
        """ Moves player from user input """
        self.moving = True

        x = DirectionalValues.DIRECTION_MOV[self.direction][0]
        y = DirectionalValues.DIRECTION_MOV[self.direction][1]
        self.position = pg.Vector2(self.position.x + x, self.position.y + y)
        self.last_moved = time.time()

        self.flipped = True if self.direction == DirectionalValues.LEFT else False if self.direction == DirectionalValues.RIGHT else self.flipped
        self.sprite_pos = self.position  # will need to be changed based on animation

        # move animation
        if x:
            self.animator.do_animation(PlayerTextures.PLAYER_JUMP_HORIZONTAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED, offset=pg.Vector2(-x / 2, -GameUnits.UNIT / 2))  # jump anim
        else:
            self.animator.do_animation(PlayerTextures.PLAYER_JUMP_VERTICAL, PlayerValues.PLAYER_MOVE_ANIM_SPEED, offset=pg.Vector2(0, 0 if y < 0 else -GameUnits.UNIT), reverse=y > 0)

        # todo: send beat event (after player movement)

        self.moving = False

    def set_pos(self, x, y):
        """ Sets player position & sprite pos instantly """
        self.moving = True
        self.position.x = x
        self.position.y = y
        self.sprite_pos.x = x
        self.sprite_pos.y = y
        self.last_moved = time.time()
        self.moving = False

    def can_move(self):
        """ Returns true if the player is allowed to move """
        # TODO: replace animator.current_anim_ss with some other solution to the animation moving bug
        return not self.moving and not self.animator.current_anim_ss and time.time() - PlayerValues.MOVEMENT_PAUSE > self.last_moved

    def render_player(self):
        self.animator.update()
        self.current_texture = self.animator.texture_obj

        if self.is_player_loaded():
            sprite = pg.transform.scale(self.current_texture, (self.current_texture.get_width() * GameUnits.RES_MUL, self.current_texture.get_height() * GameUnits.RES_MUL))
            sprite = pg.transform.flip(sprite, True if self.flipped else False, False)

            blit = ((self.sprite_pos.x - sprite.get_width() // 2) + self.animator.offset.x,
                    (self.sprite_pos.y - sprite.get_height() // 2) + self.animator.offset.y)

            # render_shadow(self.surface, sprite, blit)
            self.surface.blit(sprite, blit)

    def is_player_loaded(self):
        """ Returns whether player has fully loaded in (add more checks later) """
        return self.current_texture
