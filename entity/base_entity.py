import pygame as pg
from texture_constants import EntityTextures
from rendering.sprites_holder import SpriteSheet
from rendering.shadow import Shadow
from rendering.split_sheet import split_sheet
from rendering.animator import Animator
from constants import GameUnits


class BaseEntity:
    """ ABSTRACT BASE CLASS """
    def __init__(self):
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
        surface.blit(self.get_sprite(), pg.Vector2(self.position.x, self.position.y + GameUnits.ENTITY_Y_OFFSET))

    def on_sprite_updated(self):
        """ Called when sprite updates its texture """
        self.current_texture = self.animator.texture_obj

        self.shadow.update_shadow(self.position, self.get_sprite(), self.animator.offset)

    def on_shadow_beat(self, prev_shadow_beat_time):
        self.animator.on_shadow_beat(prev_shadow_beat_time)

    def on_bpm_change(self, new_bpm):
        self.animator.on_bpm_change(new_bpm)

    def get_sprite(self) -> pg.surface.Surface:
        """ Always use this to get the player sprite. Just flips the sprite if it needs to """
        return pg.transform.flip(self.current_texture, True if self.flipped else False, False)


class PlaceholderEntity(BaseEntity):
    def __init__(self, spawn_pos: pg.Vector2):
        BaseEntity.__init__(self)

        self.position = spawn_pos

        # texture stuff
        self.flipped = False
        texture_idle = pg.image.load(EntityTextures.PLACEHOLDER).convert_alpha()
        self.ss_idle = split_sheet(texture_idle, (GameUnits.UNIT, GameUnits.UNIT), 4)

        self.animator = Animator(SpriteSheet(EntityTextures.PLACEHOLDER, self.ss_idle), pg.Vector2(0, 0))

        self.current_texture = self.animator.texture_obj
        self.shadow = Shadow(self.get_sprite(), self.position)

    def __repr__(self):
        return f"PlaceholderEntity({self.position})"


ASCII_TO_ENTITY = {
    "pe": PlaceholderEntity
}
