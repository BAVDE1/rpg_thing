from constants import *
import os


def parse_file(file):
    """ Returns list of lines in file """
    if not os.path.exists(file):
        raise FileNotFoundError(
            f"level file {file} could not be found. Was there a typo; was the directory not properly declared?")

    level_lines = []
    with open(file) as f:
        for line in f:
            level_lines.append(line.strip().replace("[", "").replace("]", ""))
    return level_lines


class FileDisplayer:
    def __init__(self, screen: pg.surface.Surface, file_dir: str, pos: pg.Vector2, size: int = 20):
        self.screen = screen
        self.file_dir = file_dir

        self.pos = pos

        self.size = size
        self.font = pg.font.SysFont('Times New Roman', max(20, size))
        self.file_font = pg.font.SysFont('Consolas', size)
        self.display_text = self.font.render(f"file_display: {file_dir.split('/')[-1:][0]}", True, (255, 255, 0))

        self.file_lines = parse_file(file_dir)
        self.display_file_lines = self.create_display_file_lines()

    def create_display_file_lines(self):
        """ Creates (or updates) the opened file's display """
        return [self.file_font.render(str("[{}]".format(line)), True, (255, 255, 255)) for line in self.file_lines]

    def render(self):
        self.screen.blit(self.display_text, self.pos)
        for i in range(len(self.display_file_lines)):
            self.screen.blit(self.display_file_lines[i], (self.pos[0], self.pos[1] + max(25, self.size) + (self.size * i)))
