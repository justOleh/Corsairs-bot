import sys
import time
from pathlib import Path

import cv2 as cv
import numpy as np
import pandas as pd
import pyautogui

from src.bots.simple_bot import SimpleBot
from src.visualizer import Visualizer
from src.screenshot_parser import ScreenshotParser
from src.window_manipulation import (activate_window, find_window_id,
                                     get_window_coordinates, take_screenshot)


class Controller:
    def __init__(self, window_name = "TelegramDesktop") -> None:
        self.screen_parser = ScreenshotParser()
        self.visualizer = Visualizer()
        self.agent = SimpleBot()

        self.window_name = window_name
        self.window_id = find_window_id(window_name)

        self.speeds = {"boat": 100, "cannonball": 6.32}
        self.radius = 160 # in pixels
        self.raidus_vect = (self.radius, 0)
        self.center_of_game = (190, 265)

    def run(self, seconds_to_play=None):
        if self.window_id is None:
            self.exit(f"Cannot find window: {self.window_name}")

        activate_window(self.window_id)
        self.window_coordinates = get_window_coordinates(self.window_id)

        start = time.time()
        self.start()
        
        while True:
            try:
                self.main_loop()
            except Exception as e:
                print(e) 
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                self.exit("Bot has finished execution")
 
    def main_loop(self):
        screenshot = take_screenshot(self.window_coordinates)
        game_state = self.screen_parser.parse_to_state(screenshot)
        action = self.agent.action(game_state)
        if action == "change_direction":
            self.change_direction()


        # image_vis = screenshot.copy()
        # image_vis = self.draw_angle(image_vis, boat_angle)

        # image_vis = self.draw_rectangles(image_vis, boat_position, color=(255, 0, 0))
        # image_vis = self.draw_rectangles(image_vis, coin_positions, color=(0, 255, 0))
        # image_vis = self.draw_rectangles(image_vis, cannonball_positions, color=(0, 0, 255))

        # cv.imshow("main", image_vis)
        # cv.waitKey(30)
        # return image_vis

    def start(self):
        activate_window(self.window_id)
        pyautogui.press("space")
 
    def change_direction(self):
        activate_window(self.window_id)
        pyautogui.press("space")

    def exit(self, message):
        sys.exit(message)
