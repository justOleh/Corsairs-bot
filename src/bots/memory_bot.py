import numpy as np

from src.bots.bot import Bot


class MemoryBot(Bot):
    def __init__(self):
        self.critical_distance = 50

        self.action_count_rotate = 3
        self.action_count_pass = 0
        self.is_start_count = False

    def action(self, state):
        if self.is_start_count:
            self.action_count_pass += 1

        cannonball_centers_normalised = state["cannonball_centers"]
        boat_center_normalised = state["boat_center"]

        # Actions based on distances
        distances = np.linalg.norm(cannonball_centers_normalised-boat_center_normalised, ord=1, axis=1)

        if self.action_count_pass >= self.action_count_rotate:
            print(self.action_count_pass)
            self.is_start_count = False
            self.action_count_pass = 0
            print("change dir oposite")
            return "change_direction"

        if any(dist <= self.critical_distance for dist in distances):
            self.is_start_count = True
            return "change_direction"