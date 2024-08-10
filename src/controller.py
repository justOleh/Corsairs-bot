"""
    Current module contains class Controller responsible for controlling different parts of the program:
    Those parts are:
        window_manipulation, screen_parser, bot(agent), visualizer. 
"""

import sys
import time
from pathlib import Path

import cv2 as cv
import numpy as np
import pandas as pd
import pyautogui

from src.bots import get_bot
from src.screenshot_parser import ScreenshotParser
from src.visualizer import Visualizer
from src.window_manipulation import (activate_window, find_window_id,
                                     get_window_coordinates, take_screenshot)


class Controller:
    """
        Class Controller responsible for coordinating different parts of the program that
        they work proper and produce desirable outcome. 
    """
    def __init__(self, window_name = "TelegramDesktop", bot_name: str = "MemoryBot"):
        # setup variables for working with window
        self.radius = 160 # in pixels
        self.raidus_vect = (self.radius, 0)
        self.center_of_game = (190, 265)
        self.window_name = window_name
        self.window_id = find_window_id(window_name)

        self.screen_parser = ScreenshotParser(
            game_center = self.center_of_game,
            raidus_vect = self.raidus_vect)
        self.visualizer = Visualizer()
        # place to switch agents 
        self.agent = get_bot(bot_name)

    # still hard to follow the code, but looks prettier
    def run(self, seconds_to_play=None, visualize=False):
        """
            Entry method to start playing the game
        """
        self.ensure_window(self.window_id)
        activate_window(self.window_id)
        self.window_coordinates = get_window_coordinates(self.window_id)
        
        if visualize:
            self.visualizer.open_video_capture()
        self.start()
        # the main action, bot gets state, takes actions, also visualization happends
        self.run_seconds(self.main_loop, seconds_to_play=seconds_to_play, visualize=visualize)

    def run_seconds(self, main_loop, seconds_to_play, visualize=False):
        """
            Just take a look at method's name :)
        """
        def is_playing(start, finish, seconds_to_play):
            seconds_played = finish-start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                return False
            return True

        start = time.time()
        while is_playing(start, time.time(), seconds_to_play):
            try:
                main_loop(visualize=visualize)   
            except Exception as e:
                # TODO: redirect errors to error log 
                print(e) 
        self.exit("Bot has finished execution")


    def bot_loop(self) -> tuple:
        """
            Method responsible for taking screenshot
            parsing sreenshot to state, executing bots' actions
            based on passed state. 
        """
        screenshot = take_screenshot(self.window_coordinates)
        game_state = self.screen_parser.parse_to_state(screenshot)
        action = self.agent.action(game_state)
        if action == "change_direction":
            self.change_direction()
        return screenshot, game_state
    
    def main_loop(self, visualize):
        """
            Method responsible for executing bot actions, draw state
            and any additional steps required.
        """
        screenshot, state = self.bot_loop()
        if visualize:
            screenshot_vis = self.visualizer.draw_state(screenshot, state)
            self.visualizer.add_frame(screenshot_vis)

    def start(self):
        """
            Method for starting the game.
        """
        activate_window(self.window_id)
        pyautogui.press("space")
 
    def change_direction(self):
        """
            Method for manipulating bot dicrection.
        """
        activate_window(self.window_id)
        pyautogui.press("space")


    def ensure_window(self, window_id):
        """
        Exits execution if the window is not found.
        """
        if window_id is None:
            self.exit(f"Cannot find window: {self.window_name}")
        return True


    def exit(self, message):
        """
            Method for stoping bot execution.
            Could have some additional logic. 
        """
        if self.visualizer.video is not None:
            self.visualizer.close_video_capture()
        sys.exit(message)
