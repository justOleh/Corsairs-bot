import sys
import time

import cv2 as cv

from src.window_manipulation import (activate_window, find_window_id,
                                     get_window_coordinates, take_screenshot)
import pyautogui


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
        self.window_coordinates = get_window_coordinates(self.window_id)

        start = time.time()
        self.start()

        while True:

            self.main_loop()
    
            # end when seconds_to_play passed
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                self.exit("Bot has finished execution")

    def main_loop(self):
        screenshot = take_screenshot(self.window_coordinates)

    def start(self):
        pyautogui.press("space")

    
    def exit(self, message):
        sys.exit(message)
