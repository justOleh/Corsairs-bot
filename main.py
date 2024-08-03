from src.controller import Controller


if __name__ == "__main__":
    window_name = "Telegram"

    controller = Controller(window_name)
    controller.run(5)