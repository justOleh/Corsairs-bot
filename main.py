from src.controller import Controller

# TODO: add argument parsing
if __name__ == "__main__":
    controller = Controller(window_name="TelegramDesktop")
    controller.run(seconds_to_play=10, visualize=True)
