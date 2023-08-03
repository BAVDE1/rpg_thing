import time


class LinearTween:
    def __init__(self, value, goal, duration):
        self.current_time = time.time()
        self.start_time = self.current_time
        self.end_time = self.start_time + duration

        self.start_value = value
        self.end_value = goal - value

    def get_percent(self):
        return (self.current_time - self.start_time) / (self.end_time - self.start_time)

    def update(self, item):
        self.current_time = time.time()
        if not self.has_reached_goal():
            item = self.start_value + (self.end_value * self.get_percent())
        else:
            item = self.end_value
        return item

    def has_reached_goal(self):
        return self.end_time < self.current_time
