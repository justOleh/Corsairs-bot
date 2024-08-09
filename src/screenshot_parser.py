import cv2 as cv
import numpy as np

from pathlib import Path


class ScreenshotParser():
    def __init__(self, game_center: tuple, raidus_vect: tuple) -> None:
        self.game_center = game_center
        self.raidus_vect = raidus_vect
        self.templates = self.load_templates()
        self.template_thresholds = {"boat": 0.55, "coin": 0.8, "cannonball": 0.6}

    def parse_to_state(self, screenshot: np.ndarray) -> dict:
        boat_positions = self.get_position(screenshot, self.templates["boat"], self.template_thresholds["boat"])
        boat_position = self.non_maximum_suppression(boat_positions)
        boat_center = self.calc_center(boat_position[0])
                
        coin_positions = self.get_position(screenshot, self.templates["coin"], self.template_thresholds["coin"])
        coin_positions = self.non_maximum_suppression(coin_positions)

        cannonballs_position = self.get_position(screenshot, self.templates["cannonball"], self.template_thresholds["cannonball"])
        cannonball_positions = self.non_maximum_suppression(cannonballs_position)
        cannonball_centers = [self.calc_center(cannonball_pos) for cannonball_pos in cannonball_positions]
        cannonball_centers_normalised = np.array([self.normalize_point(cannonball_center) for cannonball_center in cannonball_centers])

        boat_center_normalised = self.normalize_point(boat_center)

        # Calculated angles
        boat_angle = self.calc_angle(boat_center_normalised, self.raidus_vect)


        cannonball_angles = [self.calc_angle(cannonball_center, self.raidus_vect)
                             for cannonball_center in cannonball_centers_normalised]

        return {"boat_center": boat_center_normalised,
                "boat_angle": boat_angle,
                "cannonball_centers": cannonball_centers_normalised,
                "cannonbal_angles": cannonball_angles,
                "coin_positions": coin_positions}


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
        return np.array([(coordinates[0] + coordinates[2])//2, (coordinates[1] + coordinates[3])//2])

    def calc_angle(self, a, b):
        a = np.array(a)
        b = np.array(b)
        # common formula to calculate angle between two vectors
        angle_radians = np.arccos(np.sum(a*b)/(np.linalg.norm(a, ord=2)*np.linalg.norm(b, ord=2)))
        angle_degrees = angle_radians*(180/np.pi)
        return float(angle_degrees)


    def normalize_point(self, coordiantes: tuple[int, int]):
        return np.array([coordiantes[0]-self.game_center[0],
                coordiantes[1]-self.game_center[1]])
    
        
    def imshow(self, image, pause=0):
        cv.namedWindow("main")
        cv.imshow("main", image)
        cv.waitKey(pause)
        cv.destroyWindow("main")


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