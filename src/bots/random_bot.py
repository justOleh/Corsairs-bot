import numpy as np

from src.bots.bot import Bot


class RandomBot(Bot):
    def __init__(self):
        self.action_count = 0
        self.each_action = 10
        self.chance_change_direction = 0.5

    def action(self, state):
        self.action_count += 1
        if self.action_count % self.each_action == 0:
            if np.random.rand() <= self.chance_change_direction:
                return "change_direction"