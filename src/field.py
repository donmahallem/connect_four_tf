import numpy as np


class Field:

    def __init__(self):
        self._field = np.zeros((6, 7))

    def put(self, x, player):
        for y in range(self._field.shape[0]):
            if self._field[y, x] == 0:
                self._field[y, x] = player
                return self._field, x, self.isDoneFast(y, x, player)
        raise Exception('column already full')

    def setCoords(self, coords):
        self.coords = coords

    def isDoneFast(self, y, x, player):
        min_x = max(0, x-3)
        max_x = min(self._field.shape[1]-3, x)
        min_y = max(0, y-3)
        max_y = min(self._field.shape[0]-3, y)
        for offset in range(-3, 1):
            offset_x = x+offset
            offset_y = y+offset
            if offset_x >= 0 and offset_x+4 <= self._field.shape[1]:
                # print(offset_x)
                if self._field[y, offset_x] == player and \
                        self._field[y, offset_x+1] == player and \
                        self._field[y, offset_x+2] == player and \
                        self._field[y, offset_x+3] == player:
                    return True
            if offset_y >= 0 and offset_y+4 <= self._field.shape[0]:
                # print(offset_y)
                if self._field[offset_y, x] == player and \
                        self._field[offset_y+1, x] == player and \
                        self._field[offset_y+2, x] == player and \
                        self._field[offset_y+3, x] == player:
                    return True
            if offset_x >= 0 and \
                    offset_y >= 0 and \
                    offset_y+4 <= self._field.shape[0] and \
                    offset_x+4 <= self._field.shape[1]:
                #print(str(offset_x)+" - "+str(offset_y))
                if self._field[offset_y, offset_x] == player and \
                        self._field[offset_y+1, offset_x+1] == player and \
                        self._field[offset_y+2, offset_x+2] == player and \
                        self._field[offset_y+3, offset_x+3] == player:
                    return True
        return False

    def getField(self):
        return self._field

    def isColumnFull(self, x):
        return self._field[self._field.shape[0]-1, x] != 0
