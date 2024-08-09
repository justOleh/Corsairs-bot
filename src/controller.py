import sys
import time
from pathlib import Path

import cv2 as cv
import numpy as np
import pandas as pd
import pyautogui

from src.bots.random_bot import RandomBot
from src.bots.simple_bot import SimpleBot
from src.bots.memory_bot import MemoryBot
from src.visualizer import Visualizer
from src.screenshot_parser import ScreenshotParser
from src.window_manipulation import (activate_window, find_window_id,
                                     get_window_coordinates, take_screenshot)


class Controller:
    def __init__(self, window_name = "TelegramDesktop"):
        self.radius = 160 # in pixels
        self.raidus_vect = (self.radius, 0)
        self.center_of_game = (190, 265)

        self.screen_parser = ScreenshotParser(
            game_center = self.center_of_game,
            raidus_vect = self.raidus_vect)
        self.visualizer = Visualizer()
        # place to switch agents 
        # self.agent = SimpleBot()
        # self.agent = RandomBot()
        self.agent = MemoryBot()

        self.window_name = window_name
        self.window_id = find_window_id(window_name)

        self.speeds = {"boat": 100, "cannonball": 6.32}


    def run(self, seconds_to_play=None, visualize=False):
        if self.window_id is None:
            self.exit(f"Cannot find window: {self.window_name}")

        activate_window(self.window_id)
        self.window_coordinates = get_window_coordinates(self.window_id)

        start = time.time()
        self.start()

        if visualize:
            self.visualizer.open_video_capture()
        
        while True:
            
            try:
                screenshot, state = self.main_loop()
                if visualize:
                    screenshot_vis = self.visualizer.draw_state(screenshot, state)
                    self.visualizer.add_frame(screenshot_vis)
            except Exception as e:
                print(e) 

            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                if visualize:
                    self.visualizer.close_video_capture()
                self.exit("Bot has finished execution")
 
    def main_loop(self) -> tuple:
        screenshot = take_screenshot(self.window_coordinates)
        game_state = self.screen_parser.parse_to_state(screenshot)
        action = self.agent.action(game_state)
        if action == "change_direction":
            self.change_direction()
        return screenshot, game_state

    def start(self):
        activate_window(self.window_id)
        pyautogui.press("space")
 
    def change_direction(self):
        activate_window(self.window_id)
        pyautogui.press("space")

    def exit(self, message):
        sys.exit(message)
