import numpy as np
import weakref

__author__ = 'tbsexton'

class Agent:

    agent_list = {}

    def __init__(self, name, params=(1., .5)):
        self.order = len(Agent.agent_list.values())
        self.str = name
        self.Q = {}
        self.games_played = 0
        self.wins = 0.
        self.alpha, self.gamma = params  # learning rate, memory
        Agent.agent_list[name] = self

        self.static = False

    @classmethod
    def get_agents(cls):
        return Agent.agent_list.values()

    def summary_actions(self):  # all state:action pairs w/ non-zero Q
        kist = [{k: v for k, v in self.Q[key].iteritems() if v != 0} for key in self.Q.keys()]
        return {k: v for k, v in dict(zip(self.Q.keys(), kist)).iteritems() if bool(v)}

    def take_action(self, state, valid_acts):
        # SOFT-MAX #
        # -------- #
        tau = 100.
        self.make_key(state, valid_acts)
        try:
            ex = np.exp(np.array([self.Q[state][tuple(i)] for i in valid_acts])/tau)
        except KeyError:
            print 'WHAT!!?'
            raise
        pmf = ex/np.sum(ex)

        # move = np.random.choice(valid_acts, size=1, p=pmf)
        move = valid_acts[np.random.choice(valid_acts.shape[0], p=pmf)]
        return move

        # EPSILON-GREEDY #
        # -------------- #
        # eps = np.random.rand(1)
        # if eps > 0.1:  # 90% chance
        #     # np.random.choice(np.where(a == a.max())[0]) #non-working
        #
        #     # This chooses the action associated with the max Q value
        #     move = max(self.Q[state], key=self.Q[state].get)
        #
        #     # move=np.max([self.Q[state][i] for i in self.Q[state]]) #selcts wrong thing
        #     return move
        # else:  # 20% chance
        #     return valid_acts[np.random.choice(valid_acts.shape[0])]

    def make_key(self, state, valid_acts):
        # print self.Q
        # print type(state)
        if state not in self.Q:
            self.Q[state] = {}
        for i in valid_acts:
            # initialize with small random values
            # self.Q[state][tuple(i)] = np.random.uniform(low=-0.15, high=.15)
            self.Q[state][tuple(i)] = 0.

    def update_Q(self, state, move, valids, *conds):
        win_check, lose_check = conds

        old_state = tuple(np.subtract(state, move))

        # reward = 0.
        self.make_key(state, valids)
        self.make_key(old_state, valids)

        if self.static:
            return

        if win_check:
            # print 'Player {} wins!'.format(self.str)
            # print self.Q[old_state][move]
            self.games_played +=1
            self.wins += 1
            reward = 6. / np.where(np.array(state) == np.max(state))[0].size  # split btw. winners
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                          self.alpha * (reward +
                                                   self.Q[old_state][move]))
            # print self.Q[old_state][move]
        elif lose_check:
            self.games_played += 1
            reward = -6.
            # print state+move, move
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                       self.alpha * (reward -
                                                     self.Q[old_state][move]))
        else:
            self.Q[old_state][move] = (self.Q[old_state][move] +
                                       self.alpha * (
                                                     self.gamma * self.Q[state][max(self.Q[state],
                                                                                    key=self.Q[state].get)] -
                                                     self.Q[old_state][move]))
        return
