import pygame as pg
from texture_constants import EntityTextures
from rendering.sprites_holder import SpriteSheet
from rendering.shadow import Shadow
from entity.entity_brain import BasicBrain
from rendering.animator import Animator
from constants import GameUnits


class BaseEntity:
    """ ABSTRACT BASE CLASS """
    def __init__(self):
        self.type = "BaseEntity"
        self.position = None

        self.flipped = None
        self.ss_idle = None

        self.animator = None
        self.current_texture = None
        self.shadow = None

    def render(self, surface):
        """ Called every frame """
        self.animator.update()
        if self.animator.has_changed_texture:
            self.on_sprite_updated()
            self.animator.has_changed_texture = False

        # shadow
        self.shadow.draw(surface)

        # entity
        pos = pg.Vector2((self.position.x - self.get_sprite().get_width() / 2) + self.animator.offset.x,
                          (self.position.y - self.get_sprite().get_height() / 2) + self.animator.offset.y)
        surface.blit(self.get_sprite(), pg.Vector2(pos.x, pos.y + GameUnits.ENTITY_Y_OFFSET))
        pg.draw.rect(surface, (255, 0, 0), pg.rect.Rect(self.position.x, self.position.y, 3, 3), 2)

    def on_sprite_updated(self):
        """ Called when sprite updates its texture """
        self.current_texture = self.animator.texture_obj

        self.shadow.update_shadow(self.position, self.get_sprite(), self.animator.offset)

    def on_shadow_beat(self, shadow_beat_time):
        self.animator.on_shadow_beat(shadow_beat_time)

    def on_beat(self, beat_time):
        pass

    def on_bpm_change(self, new_bpm):
        self.animator.on_bpm_change(new_bpm)

    def get_sprite(self) -> pg.surface.Surface:
        """ Always use this to get the sprite. Just flips the sprite if it needs to """
        return pg.transform.flip(self.current_texture, True if self.flipped else False, False)

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

    def __repr__(self):
        return f"{self.type}({self.position})"


class PlaceholderEntity(BaseEntity):
    def __init__(self, game, spawn_pos: pg.Vector2):
        BaseEntity.__init__(self)
        self.type = "PlaceholderEntity"

        self.game = game
        self.position = spawn_pos

        # texture stuff
        self.flipped = False
        self.animator = Animator(SpriteSheet(EntityTextures.PLACEHOLDER, pg.Vector2(GameUnits.UNIT, GameUnits.UNIT), 4), pg.Vector2(0, 0))

        self.current_texture = self.animator.texture_obj
        self.shadow = Shadow(self.get_sprite(), self.position)

        # ai stuff
        self.brain = BasicBrain(self, self.game)

    def on_beat(self, beat_time):
        pass


ASCII_TO_ENTITY = {
    "pe": PlaceholderEntity
}
