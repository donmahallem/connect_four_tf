from player import Player
import numpy as np


class RandomPlayer(Player):
    def __init__(self, only_valid=True):
        super().__init__()
        self.only_valid = only_valid

    def take_turn(self, field):
        if self.only_valid:
            valid_turns = []
            for i in range(0, 7):
                if not field.isColumnFull(i):
                    valid_turns.append(i)
            return np.random.choice(valid_turns)
        else:
            return np.random.randint(0, 7)
