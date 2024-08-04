import subprocess


def find_window_id(window_title):
    """Find the window ID of a window with a specific title."""
    output = subprocess.run(['wmctrl', '-l'], capture_output=True).stdout.decode()
    for line in output.splitlines():
        if window_title in line:
            return line.split()[0]
    return None


def get_window_geometry(window_id):
    """Get the geometry of a window by its ID."""
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
    return geometry


def activate_window(window_id):
    """Activate a window by its ID."""
    subprocess.run(['wmctrl', '-i', '-a', window_id])


def calculate_corners(geometry):
    """Calculate the positions of the four corners of the window."""
    x, y = geometry['x'], geometry['y']
    width, height = geometry['width'], geometry['height']
    return {
        'top_left': (x, y),
        'top_right': (x + width, y),
        'bottom_left': (x, y + height),
        'bottom_right': (x + width, y + height)
    }

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
