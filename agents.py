__author__ = 'Thurston Sexton'

import numpy as np

class Human:
    def __init__(self, name, playertype='human'):
        self.str = name
        self.playertype = playertype


class Rando:
    def __init__(self, name, playertype='random'):
        self.str = name
        self.playertype = playertype


class Perfect:
    def __init__(self, name, playertype='perfect'):
        self.str = name
        self.playertype = playertype


class Q_bot:
    def __init__(self, name, playertype='Q'):
        self.str = name
        self.playertype = playertype
        self.Q = {}

    def take_action(self, state, valids):
        eps = np.random.rand(1)
        if eps > 0.1:  # 90% chance
            # np.random.choice(np.where(a == a.max())[0]) #non-working

            # This chooses the action associated with the max Q value
            move = max(self.Q[state], key=self.Q[state].get)

            # move=np.max([self.Q[state][i] for i in self.Q[state]]) #selcts wrong thing
            return move
        else:  # 20% chance
            return np.random.choice(valids)

    def makeKey(self, state, valids):
        # print self.Q
        if state not in self.Q:
            self.Q[state] = {}
            for i in valids:
                # initialize with small random values
                self.Q[state][i] = np.random.uniform(low=-0.15, high=.15)

    def update_Q(self, state, move, valids, flipped=False):
        alpha = .45  # learning rate
        gamma = 1.  # memory
        reward = 0.

        if state == 1:
            self.makeKey(state, valids)
            reward = 10.
            self.Q[state + move][move] = (self.Q[state + move][move] +
                                          alpha * (reward -
                                                   self.Q[state + move][move]))
        if state == 0:
            self.makeKey(state + move, valids)
            reward = -10.
            # print state+move, move
            self.Q[state + move][move] = (self.Q[state + move][move] +
                                          alpha * (reward -
                                                   self.Q[state + move][move]))
        else:
            self.makeKey(state, valids)

            if flipped:
                self.Q[state + move][move] = (self.Q[state + move][move] +
                                              alpha * (reward -
                                                       gamma * self.Q[state][
                                                           max(self.Q[state], key=self.Q[state].get)] -
                                                       self.Q[state + move][move]))

            else:
                self.Q[state + move][move] = (self.Q[state + move][move] +
                                              alpha * (reward -
                                                       gamma * self.Q[state][
                                                           max(self.Q[state], key=self.Q[state].get)] -
                                                       self.Q[state + move][move]))
                # print self.Q[state+move][move]
