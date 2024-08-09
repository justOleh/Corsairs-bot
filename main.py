from src.controller import Controller

if __name__ == "__main__":
    controller = Controller(window_name="TelegramDesktop")
    controller.run(seconds_to_play=10, visualize=False)