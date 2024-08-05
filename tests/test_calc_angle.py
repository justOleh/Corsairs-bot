import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from src.controller import Controller

import pytest

import numpy as np

ct = Controller()


@pytest.mark.parametrize("boat_vector, horizon_vector, expected_angle",
                         [((160, 0), (160, 0), 0),
                          ((0, 160), (160, 0), 90),
                          ((113, 113), (160, 0), (45)),
                          ((-113, 113), (160, 0), 135),
                          ((-113, -113), (160, 0), 135)])
def test_calc_angle(boat_vector, horizon_vector, expected_angle):

    calculated_angle = ct.calc_angle(boat_vector, horizon_vector)

    assert np.allclose(calculated_angle, expected_angle)