import os.path as osp
from field import Field


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


def take_turns(field, player, depth=None):
    if not depth == None and depth == 0:
        return 0
    scores = []
    for x in range(0, 7):
        if field.isColumnFull(x):
            continue
        field_copy = field.copy()
        _, _, done, x = field_copy.put(x, player)
        field_id = id(field_to_key(field_copy))
        score = 0
        if field_id in memory:
            score = memory[field_id]
        elif done:
            score = x
            memory[field_id] = score
        else:
            score = take_turns(field_copy, player*-1,
                               None if depth == None else depth-1)
            memory[field_id] = score
        scores.append(score)
    return sum(scores)/len(scores)


for p in range(0, 2):
    for t in range(0, 7):
        f = Field()
        f.put(t, 1 if p == 0 else -1)
        print(str(p)+" - "+str(t) + " res: " +
              str(take_turns(f, -1 if p == 0 else 1, 8)))
        print(len(memory.keys()))
