from qnet import QNet
import os.path as osp
from field import Field
import pickle
import numpy as np


class StateManager:

    def __init__(self, root_dir):
        self.root = root_dir

    def exists(self, id):
        return osp.exists(osp.join(self.root, id))


def bit_array_to_int(arr):
    i = 0
    for bit in arr:
        k = 0
        if bit != 0:
            k = 1 if bit == 1 else 2
        i = (i << 2) | k
    return i


def field_to_key(field):
    ret = ""
    np_field = field.getField()
    for y in range(6):
        for x in range(7):
            ret += str(np_field[y, x]+1)
    return ret


class Memory:
    def __init__(self, limit=100000):
        self.memory = []
        self.limit = limit

    def add(self, data):
        self.memory.append(data)
        overhead = len(self.memory)-self.limit
        if overhead > 0:
            self.memory = self.memory[overhead:]

    def count(self):
        return len(self.memory)


mem = Memory()

exploration_rate = 0.2
net = QNet()


def take_turns(field, player, max_depth=None):
    if not max_depth == None and max_depth == 0:
        return 0
    old_field = np.copy(field.getField())
    if np.random.random() < exploration_rate:
        take_turn = np.random.randint(0, 7)
    else:
        np_field = old_field.reshape((1, 6, 7))
        if player == -1:
            np_field *= -1
        predictions = net.predict(np_field)[0]
        take_turn = np.argmax(predictions)
    _, _, done, reward = field.put(take_turn, player)
    mem.add((old_field, take_turn, reward, field.getField()))
    if done == True:
        return player
    else:
        return take_turns(field, player*-1)


for p in range(0, 2):
    f = Field()
    print(take_turns(f, 1))


print(mem.count())
