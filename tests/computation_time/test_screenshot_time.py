import time
import numpy as np

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname((os.path.dirname(script_dir)))
sys.path.append(parent_dir)


from src.window_manipulation import (activate_window, find_window_id,
                                     get_window_coordinates, take_screenshot)

window_name = "TelegramDesktop"
def test_screenshot_time():
    times = []
    for _ in range(30):
        start = time.time()
        window_id = find_window_id(window_name)
        window_coordinates = get_window_coordinates(window_id)
        activate_window(window_id)
        screenshot = take_screenshot(window_coordinates)
        end = time.time()
        times.append(end-start)

    # less than 100 ms
    assert np.mean(times) < 0.1
    assert np.std(times) <= 0.05