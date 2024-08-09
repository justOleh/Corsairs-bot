import cv2 as cv
import numpy as np


class Visualizer:
    pass

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
    
    def draw_rectangles(self, image, rectangles, color=(0, 0, 255)):
        image_to_vis = image.copy()
                
        for rect in rectangles:
            # print(rect)
            top_left = (rect[0], rect[1])
            bottom_right = (rect[2], rect[3])
            cv.rectangle(image_to_vis, top_left, bottom_right, color, 1)

        return image_to_vis
    

    def do_something_with_video_stream():
        video_name = 'bot_playing_visualization.mp4'
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        video = cv.VideoWriter(video_name, fourcc, 10, (380, 492)) 