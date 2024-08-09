import subprocess

import cv2 as cv
import numpy as np
import pyautogui


def find_window_id(window_title):
    """Find the window ID of a window with a specific title."""
    output = subprocess.run(['wmctrl', '-l'], capture_output=True).stdout.decode()
    for line in output.splitlines():
        if window_title in line:
            return line.split()[0]
    return None


def get_window_coordinates(window_id):
    """Get the positions of the top-left and bottom-right coordinates of a window by its ID."""
    output = subprocess.run(['xwininfo', '-id', window_id], capture_output=True).stdout.decode()
    geometry = {}
    for line in output.splitlines():
        if 'Absolute upper-left X:' in line:
            geometry['x'] = int(line.split()[-1])
        if 'Absolute upper-left Y:' in line:
            geometry['y'] = int(line.split()[-1])
        if 'Width:' in line:
            geometry['width'] = int(line.split()[-1])
        if 'Height:' in line:
            geometry['height'] = int(line.split()[-1])
    
    x1, y1 = geometry['x']+11, geometry['y']+11
    width, height = geometry['width']-22, geometry['height']-220
    return x1, y1, width, height 


def activate_window(window_id):
    """Activate a window by its ID."""
    subprocess.run(['wmctrl', '-i', '-a', window_id])


def take_screenshot(window_coordinates):
     pil_image = pyautogui.screenshot(region=window_coordinates)
     open_cv_image = np.array(pil_image)
     open_cv_image = cv.cvtColor(open_cv_image, cv.COLOR_RGB2BGR)
     return open_cv_image


if __name__ == "__main__":
    window_title = 'TelegramDesktop'  # Replace with your window's title

    window_id = find_window_id(window_title)
    if window_id:
        geometry = get_window_geometry(window_id)
        activate_window(window_id)
        corners = calculate_corners(geometry)
        print(f"Window corners: {corners}")
    else:
        print(f'Window with title "{window_title}" not found.')
