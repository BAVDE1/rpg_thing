import pygame as pg


class BrainStates:
    PASSIVE = "state_passive"
    TARGET_PLAYER = "state_target_player"
    AVOID_PLAYER = "state_avoid_player"
    SPECIAL = "state_special"


class BasicBrain:
    def __init__(self, entity, game):
        self.entity = entity
        self.game = game

        self.state = BrainStates.TARGET_PLAYER
