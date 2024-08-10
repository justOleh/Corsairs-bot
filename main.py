"""
    Current module serves as an entry point to bot playing the game.

    Arguments:
        window_name - Name of the window to control. 
        seconds_to_play - Number of seconds for bot to play.
        visualize - Whether to visualize the controller's actions. The result will be .mp4 file.
        bot_name - Select bot name of the available options: ['MemoryBot', 'RandomBot', 'SimpleBot']
"""


import argparse

from src.controller import Controller


def main(window_name, bot_name, seconds_to_play, visualize):
    controller = Controller(window_name=window_name, bot_name=bot_name)
    controller.run(seconds_to_play=seconds_to_play, visualize=visualize)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Controller for a specified window.")
    
    parser.add_argument("--window_name", type=str, default="TelegramDesktop", help="Name of the window to control.")
    parser.add_argument("--seconds_to_play", type=int, default=5, help="Number of seconds for bot to play.")
    parser.add_argument("--visualize", action="store_true", default=False, help="Whether to visualize the controller's actions.")
    parser.add_argument("--bot_name", type=str, default="MemoryBot", choices=['MemoryBot', 'RandomBot', 'SimpleBot'],
                        help="Select bot name of the available options")
    
    args = parser.parse_args()
    
    main(window_name=args.window_name,
         bot_name=args.bot_name, 
         seconds_to_play=args.seconds_to_play, 
         visualize=args.visualize)
