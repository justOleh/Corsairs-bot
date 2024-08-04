import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from src.controller import Controller

import numpy as np

ct = Controller()


def test_normalize():
    boat_position = (210, 110)
    boat_normalized_position = ct.normalize_point(boat_position)

    assert np.allclose(boat_normalized_position, [20, -155])