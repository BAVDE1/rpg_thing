

# Base entity class to be inherited by entities
class BaseEntity:
    def __init__(self):
        self.health = None

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def kill(self):
        pass
