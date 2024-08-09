import numpy as np

from src.bots.bot import Bot


class SimpleBot(Bot):
    def __init__(self):
        self.critical_distance = 40
        self.angle_threshold = 10

    def action(self, state):
        cannonball_centers_normalised = state["cannonball_centers"]
        boat_center_normalised = state["boat_center"]

        # Actions based on distances
        distances = np.linalg.norm(cannonball_centers_normalised-boat_center_normalised, ord=1, axis=1)

        if any(dist <= self.critical_distance for dist in distances):
            return "change_direction"