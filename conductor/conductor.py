from utility.logging import Logger


class Conductor:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.is_conducting = False

        self.bpm = "placeholder"

        self.combat_song = "placeholder"
        self.passive_song = "placeholder"

    def start_conducting(self):
        """ Call to start up the conductor, will fail if no music or bpm has been set """
        if not self.combat_song or not self.passive_song or not self.bpm:
            raise ValueError(f"Conductor not properly initialised:\nCombat song: {self.combat_song}\nPassive song: {self.passive_song}\nBPM: {self.bpm}")

        if not self.is_conducting:
            self.is_conducting = True
            self.logger.add_log(f"conductor started")
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
