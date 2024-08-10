from src.bots.memory_bot import MemoryBot
from src.bots.random_bot import RandomBot
from src.bots.simple_bot import SimpleBot


def get_bot(bot_name):
    name_class_dict = {"MemoryBot": MemoryBot,
                       "RandomBot": RandomBot,
                       "SimpleBot": SimpleBot}
    # check proper class and create instance 
    return name_class_dict[bot_name]()
