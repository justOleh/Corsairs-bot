import sys
import time
from pathlib import Path
import cv2 as cv
import numpy as np
import pandas as pd


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

        self.speeds = {"boat": 100, "cannonball": 6.32}
        # self.positions = {"boat": [], "cannonball": []}
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

        video_name = 'boat_angle.mp4'
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        video = cv.VideoWriter(video_name, fourcc, 5, (380, 690)) 

        cv.namedWindow("main")
        
        while True:

            try:
                image_vis = self.main_loop()
                video.write(image_vis)
            except:
                pass
    
            # end when seconds_to_play passed
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                # print(self.positions)
                # pd.DataFrame({"boat": self.positions["boat"]}).to_csv("boat_positions.csv")
                # pd.DataFrame({"cannonball": self.positions["cannonball"]}).to_csv("cannonball_positions.csv")
                video.release()
                self.exit("Bot has finished execution")

        
    def main_loop(self):
        screenshot = take_screenshot(self.window_coordinates)

        # TODO: check that only 1 exists
        boat_positions = self.get_position(screenshot, self.templates["boat"], self.template_thresholds["boat"])
        boat_position = self.non_maximum_suppression(boat_positions)
        boat_center = self.calc_center(boat_position[0])
                
        coins_position = self.get_position(screenshot, self.templates["coin"], self.template_thresholds["coin"])
        coin_position = self.non_maximum_suppression(coins_position)

        cannonballs_position = self.get_position(screenshot, self.templates["cannonball"], self.template_thresholds["cannonball"])
        cannonball_positions = self.non_maximum_suppression(cannonballs_position)
        cannonball_centers = [self.calc_center(cannonball_pos) for cannonball_pos in cannonball_positions]
        cannonball_centers_normalised = [self.normalize_point(boat_center) for cannonball_center in cannonball_centers]

        boat_center_normalised = self.normalize_point(boat_center)
        boat_angle = self.calc_angle(boat_center_normalised, self.raidus_vect)

        cannonball_angles = [self.calc_angle(cannonball_center, self.raidus_vect)
                             for cannonball_center in cannonball_centers_normalised]
        
        print(cannonball_angles)
        
        image_vis = screenshot.copy()
        image_vis = self.draw_angle(image_vis, boat_angle)
        # cv.imshow("main", image_vis)
        # cv.waitKey(30)

        return image_vis
        # return None

        # print(cannonball_centers)

        # self.positions["boat"].extend(boat_position)
        # self.positions["cannonball"].extend(cannonball_positions)

        # image_vis = self.draw_rectangles(screenshot, boat_position, color=(255, 0, 0))
        # image_vis = self.draw_rectangles(image_vis, coin_position, color=(0, 255, 0))
        # image_vis = self.draw_rectangles(image_vis, cannonball_positions, color=(0, 0, 255))

        # cv.imshow("main", image_vis)
        # cv.waitKey(30)

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
        folder_path = Path("src/image_processing/assets/templates")
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
    

    def calc_center(self, coordinates: tuple):
        return (coordinates[0] + coordinates[2])//2, (coordinates[1] + coordinates[3])//2

    def calc_angle(self, a, b):
        a = np.array(a)
        b = np.array(b)
        # common formula to calculate angle between two vectors
        angle_radians = np.arccos(np.sum(a*b)/(np.linalg.norm(a, ord=2)*np.linalg.norm(b, ord=2)))
        angle_degrees = angle_radians*(180/np.pi)
        return float(angle_degrees)
    
    def draw_angle(self, image, value):
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 255, 0)
        thickness = 2
        line_type = cv.LINE_AA
        
        text = f"{value:.2f}"
        
        text_size, _ = cv.getTextSize(text, font, font_scale, thickness)
        text_width, text_height = text_size

        position = (10, text_height + 10)
    
        cv.putText(image, text, position, font, font_scale, font_color, thickness, line_type)
        
        return image
    
    def normalize_point(self, coordiantes: tuple[int, int]):
        return (coordiantes[0]-self.center_of_game[0],
                coordiantes[1]-self.center_of_game[1])

    def exit(self, message):
        sys.exit(message)
