from field import Field
import numpy as np
a = Field()
for i in range(6*7+2):
    player = 1 if i % 2 == 0 else -1
    while True:
        x = np.random.randint(0, 7)
        if not a.isColumnFull(x):
            break
    f1, action, done = a.put(x, player)
    print("Turn "+str(i))
    print(a.getField())
    if done:
        break
