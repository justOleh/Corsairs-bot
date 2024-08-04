import time
import sys
import pyautogui
# import pygetwindow as gw

from src.window_manipulation import find_window_id, activate_window, get_window_geometry


class Controller:
    def __init__(self, window_name = "TelegramDesktop") -> None:
        self.window_name = window_name
        self.window_id = find_window_id(window_name)
        self.coins = []
        self.cannonballs = []
        self.boat = None

    def run(self, seconds_to_play=None):
        if self.window_id is None:
            self.exit(f"Cannot find window: {self.window_name}")

        activate_window(self.window_id)
        start = time.time()
        while True:
            # main logic


            # end when seconds_to_play passed
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                break
    
    def exit(self, message):
        sys.exit(message)
