import time

from utility.logging import Logger


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
        self.next_beat_time = time.time()
        self.prev_beat_time = time.time()
        self.total_song_beats = 0
        self.sec_per_beat = 0

    def update(self):
        if self.is_conducting:
            if time.time() >= self.next_beat_time:
                self.beat()

    def beat(self):
        """ Shadow beats, exactly on time """
        self.total_song_beats += 1

        self.prev_beat_time = self.next_beat_time
        self.next_beat_time = self.song_started_time + (self.sec_per_beat * self.total_song_beats)

        # self.logger.add_log(f"{self.total_song_beats}: {self.prev_beat_time}")
        self.logger.add_log(f"sb {self.total_song_beats}", 0)

        self.game.on_conductor_beat()

    def player_beat(self):
        """ Beats when player does action """

    def auto_beat(self):
        """ Auto beats if the player misses it """

    def start_conducting(self):
        """ Call to start up the conductor, will fail if no music or bpm has been set """
        if not self.combat_song or not self.passive_song or not self.bpm:
            raise ValueError(f"Conductor not properly initialised:\nCombat song: {self.combat_song}\nPassive song: {self.passive_song}\nBPM: {self.bpm}")

        if not self.is_conducting:
            self.song_started_time = time.time()
            self.next_beat_time = time.time()
            self.prev_beat_time = time.time()
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
