import numpy as np
import weakref

__author__ = 'tbsexton'

class Agent:

    agent_list = {}

    def __init__(self, name, params=(.45, .9)):
        self.order = len(Agent.agent_list.values())
        self.str = name
        self.Q = {}
        self.games_played = 0
        self.wins = 0.
        self.alpha, self.gamma = params  # learning rate, memory
        Agent.agent_list[name] = self

    @classmethod
    def get_agents(cls):
        return Agent.agent_list.values()

    def take_action(self, state, valid_acts):
        eps = np.random.rand(1)
        if eps > 0.1:  # 90% chance
            # np.random.choice(np.where(a == a.max())[0]) #non-working

            # This chooses the action associated with the max Q value
            move = max(self.Q[state], key=self.Q[state].get)

            # move=np.max([self.Q[state][i] for i in self.Q[state]]) #selcts wrong thing
            return move
        else:  # 20% chance
            return valid_acts[np.random.choice(valid_acts.shape[0])]

    def make_key(self, state, valid_acts):
        # print self.Q
        # print type(state)
        if state not in self.Q:
            self.Q[state] = {}
            for i in valid_acts:
                # initialize with small random values
                self.Q[state][tuple(i)] = np.random.uniform(low=-0.15, high=.15)

    def update_Q(self, state, move, valids, *conds):
        win_check, lose_check = conds

        old_state = tuple(np.subtract(state, move))
        reward = 0.
        self.make_key(state, valids)
        self.make_key(old_state, valids)

        if win_check:
            self.games_played +=1
            self.wins += 1
            reward = 10.
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                          self.alpha * (reward -
                                                   self.Q[old_state][move]))
        elif lose_check:
            self.games_played += 1
            reward = -10.
            # print state+move, move
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                          self.alpha * (reward -
                                                   self.Q[old_state][move]))
        else:
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                          self.alpha * (reward -
                                                   self.gamma * self.Q[state][
                                                       max(self.Q[state], key=self.Q[state].get)] -
                                                   self.Q[old_state][move]))
