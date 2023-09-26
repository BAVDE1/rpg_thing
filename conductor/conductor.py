import time
from utility.logging import Logger
from constants import PlayerValues


class Conductor:
    def __init__(self, game, logger: Logger):
        self.game = game
        self.logger = logger

        self.is_conducting = False
        self.is_in_combat = True

        self.combat_song = ""
        self.passive_song = ""

        self.bpm = 300  # preset so not errors & fast when loading (in update()) animator, reset in on_level_fully_loaded() in Game
        self.song_started_time = time.time()
        self.next_shadow_beat_time = time.time()
        self.prev_shadow_beat_time = time.time()
        self.total_song_shadow_beats = 0

        self.has_performed_beat = False
        self.has_triggered_before_beat = False
        self.has_triggerd_after_beat = False
        self.prev_beat_time = time.time()
        self.total_song_beats = 0
        self.sec_per_beat = 0

    def update(self):
        """ Call every frame """
        if self.is_conducting:
            # start of allowed beat time
            if not self.has_triggered_before_beat and time.time() >= self.next_shadow_beat_time - PlayerValues.BEAT_GIVE_BEFORE:
                self.has_triggered_before_beat = True
                self.has_performed_beat = False

            # perfect on-time beat
            if time.time() >= self.next_shadow_beat_time:
                self.shadow_beat()

                self.has_triggerd_after_beat = False

            # end of allowed beat time
            if not self.has_triggerd_after_beat and time.time() >= self.prev_shadow_beat_time + PlayerValues.BEAT_GIVE_AFTER:
                self.has_triggerd_after_beat = True

                # auto beats if the player misses a beat
                if not self.has_performed_beat:
                    self.beat(is_auto_beat=True)

                self.has_triggered_before_beat = False

    def shadow_beat(self):
        """ Shadow beats, these are exactly on time """
        self.total_song_shadow_beats += 1

        self.prev_shadow_beat_time = self.next_shadow_beat_time
        self.next_shadow_beat_time = self.song_started_time + (self.sec_per_beat * self.total_song_shadow_beats)

        self.logger.add_log(f"{self.total_song_shadow_beats} sb", 0)

        self.game.on_shadow_beat()

    def beat(self, is_auto_beat=False):
        """ The actual beat, triggered by player or auto beat if the player missed the beat """
        if not self.has_performed_beat:
            self.has_performed_beat = True
            self.total_song_beats += 1
            self.prev_beat_time = time.time()

            self.logger.add_log(f"{self.total_song_beats} {'auto ' if is_auto_beat else ''}beat")

            self.game.on_beat(is_auto_beat)

    def start_conducting(self):
        """ Call to start up the conductor, will fail if no music or bpm has been set """
        if not self.combat_song or not self.passive_song or not self.bpm:
            raise ValueError(f"Conductor not properly initialised:\nCombat song: {self.combat_song}\nPassive song: {self.passive_song}\nBPM: {self.bpm}")

        if not self.is_conducting:
            self.song_started_time = time.time()
            self.next_shadow_beat_time = time.time()
            self.prev_shadow_beat_time = time.time()
            self.sec_per_beat = 60 / self.bpm

            self.is_conducting = True
            self.logger.add_log(f"conductor started ({self.sec_per_beat} / sec)")
        else:
            self.logger.add_log("cannot start: already conducting")

    def stop_conducting(self):
        """ Used to stop the conductor & its music """
        self.is_conducting = False

        self.combat_song = None
        self.passive_song = None
        self.bpm = None

    def set_music(self, combat_song_file, passive_song_file, new_bpm):
        """ Used to set the conductor's audio. Call self.start_conducting() to start """
        self.combat_song = combat_song_file
        self.passive_song = passive_song_file
        self.bpm = new_bpm

    def set_bpm(self, new_bpm):
        # TODO: not working as expected
        self.bpm = new_bpm
        self.sec_per_beat = 60 / self.bpm
