

class Logger:
    def __init__(self, screen):
        self.screen = screen

        self.messages_cap = 6

        self.messages: list[str] = []
