from field import Field
from randomplayer import RandomPlayer
import numpy as np


class Game:
    def __init__(self, p1, p2):
        self.discount = 0.8
        self.field = Field()
        self.player1 = p1
        self.player2 = p2

    def play(self):
        self.field.reset()
        first_player = np.random.randint(2)
        for turn in range(6*7+7):
            current_player = 1 if (turn+first_player) % 2 else -1
            if current_player == -1:
                take_turn = self.player1.take_turn(self.field)
            else:
                take_turn = self.player2.take_turn(self.field)
            _field, x, done, player = self.field.put(take_turn, current_player)
            if done:
                print("Turns "+str(turn))
                print(x)
                print(player)
                return self.field


g = Game(RandomPlayer(), RandomPlayer())
print(g.play().getField())
