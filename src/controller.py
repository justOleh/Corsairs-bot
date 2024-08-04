import sys
import time
from pathlib import Path
import cv2 as cv
import numpy as np


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

        self.templates = self.load_templates()
        self.template_thresholds = {"boat": 0.55, "coin": 0.8, "cannonball": 0.6}

    def run(self, seconds_to_play=None):
        if self.window_id is None:
            self.exit(f"Cannot find window: {self.window_name}")

        activate_window(self.window_id)
        self.window_coordinates = get_window_coordinates(self.window_id)

        start = time.time()
        self.start()

        while True:

            cv.namedWindow("main")
            self.main_loop()
    
            # end when seconds_to_play passed
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                self.exit("Bot has finished execution")

    def main_loop(self):
        screenshot = take_screenshot(self.window_coordinates)
        # TODO: check that only 1 exists
        boat_positions = self.get_position(screenshot, self.templates["boat"], self.template_thresholds["boat"])
        boat_position = self.non_maximum_suppression(boat_positions)
                
        coins_position = self.get_position(screenshot, self.templates["coin"], self.template_thresholds["coin"])
        coin_position = self.non_maximum_suppression(coins_position)

        cannonballs_position = self.get_position(screenshot, self.templates["cannonball"], self.template_thresholds["cannonball"])
        cannonball_position = self.non_maximum_suppression(cannonballs_position)

        image_vis = self.draw_rectangles(screenshot, boat_position, color=(255, 0, 0))
        image_vis = self.draw_rectangles(image_vis, coin_position, color=(0, 255, 0))
        image_vis = self.draw_rectangles(image_vis, cannonball_position, color=(0, 0, 255))

        cv.imshow("main", image_vis)
        cv.waitKey(30)

    def start(self):
        pyautogui.press("space")

    def get_position(self, screenshot, template, threshold) -> tuple:
        """
        Finds and draws bounding boxes around template matches in a screenshot.

        Parameters:
        - screenshot: The image where template matching will be performed.
        - template: The template image to match in the screenshot.
        - threshold: The matching threshold for considering a region as a match.

        Returns:
        - A tuple containing:
        - The image with drawn bounding boxes.
        - A list of tuples where each tuple represents (x1, y1, x2, y2) coordinates of the bounding boxes.
        """
        # Perform template matching
        result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        coordinates = []

        for pt in zip(*loc[::-1]):  # Switch x and y coordinates
            top_left = pt
            bottom_right = (pt[0] + template.shape[1], pt[1] + template.shape[0])

            coordinates.append((int(top_left[0]), int(top_left[1]), int(bottom_right[0]), int(bottom_right[1])))

        return coordinates


    def load_templates(self):
        # TODO: move to config
        folder_path = Path("src/image_processing/templates")
        templates = {}
        templates["boat"] = cv.imread(folder_path/"boat.png")
        templates["coin"] = cv.imread(folder_path/"coin.png")
        templates["cannonball"] = cv.imread(folder_path/"cannonball.png")
        
        return templates
    
    def imshow(self, image, pause=0):
        cv.namedWindow("main")
        cv.imshow("main", image)
        cv.waitKey(pause)
        cv.destroyWindow("main")

    def draw_rectangles(self, image, rectangles, color=(0, 0, 255)):
        image_to_vis = image.copy()
                
        for rect in rectangles:
            print(rect)
            top_left = (rect[0], rect[1])
            bottom_right = (rect[2], rect[3])
            cv.rectangle(image_to_vis, top_left, bottom_right, color, 1)

        return image_to_vis
    

    def non_maximum_suppression(self, rectangles, threshold=0.1):
        def intersection_over_union(boxA, boxB):
            xA = max(boxA[0], boxB[0])
            yA = max(boxA[1], boxB[1])
            xB = min(boxA[2], boxB[2])
            yB = min(boxA[3], boxB[3])
            
            interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
            boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
            boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
            
            iou = interArea / float(boxAArea + boxBArea - interArea)
            return iou
        
        # Sort rectangles by their x2 coordinate (right edge)
        rectangles = sorted(rectangles, key=lambda x: x[2])
        selected_boxes = []
        
        while rectangles:
            current = rectangles.pop(0)
            selected_boxes.append(current)
            rectangles = [box for box in rectangles if intersection_over_union(current, box) < threshold]
        
        return selected_boxes



    
    def exit(self, message):
        sys.exit(message)
