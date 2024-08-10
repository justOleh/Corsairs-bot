import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

import numpy as np

# TODO: use it from config in future
from src.screenshot_parser import ScreenshotParser
sp = ScreenshotParser((190, 265), (160, 0))


def test_normalize():
    boat_position = (210, 110)
    boat_normalized_position = sp.normalize_point(boat_position)

    assert np.allclose(boat_normalized_position, [20, -155])