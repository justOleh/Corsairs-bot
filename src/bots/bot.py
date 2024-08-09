from abc import ABC


class Bot(ABC):
    def __init__(self, state = None):
        self.prev_state = None
        self.state = state
        
    def action(self, state: None):
        pass

