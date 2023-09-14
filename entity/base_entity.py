

# abstract base class?
class BaseEntity:
    def __init__(self):
        self.health = None

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def kill(self):
        pass
