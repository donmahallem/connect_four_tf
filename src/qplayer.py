from player import Player
import numpy as np
from qnet import QNet
from field import Field


class QPlayer(Player):
    def __init__(self):
        super().__init__()
        self.exploration_rate = 0.2
        self.qnet = QNet()

    def take_turn(self, field):
        if self.exploration_rate <= np.random.random():
            take = self.random_turn(field)
        else:
            take = self.greedy_turn(field)
        return take

    def random_turn(self, field):
        return np.random.randint(0, 7)

    def greedy_turn(self, field):
        return np.argmax(self.qnet.predict(field))


asdf = QPlayer()
f = Field()
print(asdf.take_turn(f))
