import time

# import pyautogui
import AppKit



class Controller:
    def __init__(self, window_name = "Telegram") -> None:
        self.window = self.get_window(window_name)
        self.window.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        
        print(self.window)
        self.coins = []
        self.cannonballs = []
        self.boat = None

    def run(self, seconds_to_play=None):
        self.window.restore()
        self.window.activate()

        start = time.time()
        while True:
            # main logic


            # end when seconds_to_play passed
            end = time.time()
            seconds_played = end - start
            if (seconds_to_play is not None) and (seconds_played >= seconds_to_play):
                break


    def get_window(self, window_name):
        apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
        for app in apps:
            if window_name in app.localizedName():
                return app

    # def take_screenshot(self):
    #      screenshot = pyautogui.screenshot(region=(self.window.left, self.window.top,
    #                                                self.window.width, self.window.height))
    #      print(screenshot)