from qnet import QNet
from field import Field
import numpy as np
a = Field()

net = QNet()
net.getModel().summary()
for i in range(6*7+2):
    player = 1 if i % 2 == 0 else -1
    if player > 0:
        x = np.argmax(net.predict(a.getField().reshape((1, 6, 7)))[0])
    else:
        x = np.random.randint(0, 7)
    f1, action, done, reward = a.put(x, player)
    print(i)
    print(a.getField())
    if done:
        print("Player "+str(reward)+" won")
        break


class Game:
    def __init__(self):
        self.discount = 0.8
        self.qnet = QNet()

    def create_training_pair(self, old_state, action, reward, new_state):
        # Ask the model for the Q values of the old state (inference)
        states = np.zeros(
            (2, old_state.shape[0], old_state.shape[1], old_state.shape[2]))
        states[0] = old_state
        states[1] = new_state
        Q_values = self.qnet.predict(states)
        old_state_Q_values = Q_values[0]

        # Ask the model for the Q values of the new state (inference)
        new_state_Q_values = Q_values[1]

        # Real Q value for the action we took. This is what we will train towards.
        old_state_Q_values[action] = reward + \
            self.discount * np.amax(new_state_Q_values)

        return old_state, old_state_Q_values

    def minimax(self, field, player, depth=5):
        if depth == 0:
            return evaluate(position)
        bestScore = -100000000
        for i in range(0, 7):
            if field.isColumnFull(i):
                continue
            fieldClone = field.clone()
            fieldClone.put(i, player)
            subScore = - self.minimax(fieldClone, player*-1, depth - 1)
            if subScore > bestScore:
                bestScore = subScore
        return bestScore
