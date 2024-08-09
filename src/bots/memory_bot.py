import numpy as np

from src.bots.bot import Bot


class MemoryBot(Bot):
    def __init__(self):
        self.critical_distance = 40
        self.angle_threshold = 10

    def action(self, state):
        # TODO: implement logic here
        pass