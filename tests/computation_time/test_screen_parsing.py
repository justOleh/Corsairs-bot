import time
import os
import sys

import cv2 as cv
import numpy as np


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname((os.path.dirname(script_dir)))
sys.path.append(parent_dir)

from src.screenshot_parser import ScreenshotParser

screen_parser = ScreenshotParser((160, 0), (190, 265))


def test_state_parsing_time():
    img = cv.imread("tests/computation_time/files/field.png")
    durations = []
    for _ in range(30):
        start = time.time()
        state = screen_parser.parse_to_state(img)
        end = time.time()
        duration = end-start
        durations.append(duration)

    print(f"mean parsing duration {np.mean(durations):.3f}")
    print(f"std parsing duration {np.std(durations):.3f}")

    assert np.mean(durations) < 0.05
    assert np.std(durations) < 0.1