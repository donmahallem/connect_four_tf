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


memory = dict()
last_pickle = 0

if osp.exists("filename.pickle"):
    with open('filename.pickle', 'rb') as handle:
        memory = pickle.load(handle)


def take_turns(field, player, max_depth=None):
    global last_pickle
    if not max_depth == None and max_depth == 0:
        return 0
    scores = []
    for x in range(0, 7):
        if field.isColumnFull(x):
            continue
        field_copy = field.copy()
        _, _, done, x = field_copy.put(x, player)
        field_id = field_to_key(field_copy)
        field_id2 = field_to_key(np.flip(field_copy, 1))
        score = 0
        if field_id in memory:
            score = memory[field_id]
        elif field_id2 in memory:
            score = memory[field_id2]
        elif done:
            score = x
            memory[field_id] = score
        else:
            score = take_turns(field_copy, player*-1,
                               None if max_depth == None else max_depth-1)
            memory[field_id] = score
        scores.append(score)
    if field.getTurns() % 10 == 0 and last_pickle+10000 < len(memory.keys()):
        print("Done with depth: "+str(field.getTurns()))
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(memory, handle, protocol=pickle.HIGHEST_PROTOCOL)
        last_pickle = len(memory.keys())
    return 0.8*sum(scores)/len(scores)


for p in range(0, 2):
    for t in range(0, 7):
        f = Field()
        f.put(t, 1 if p == 0 else -1)
        print(str(p)+" - "+str(t) + " res: " +
              str(take_turns(f, -1 if p == 0 else 1, None)))
        print(len(memory.keys()))
