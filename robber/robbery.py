import numpy as np
__author__ = 'tbsexton'

class Robbery:

    def __init__(self, name, start, *players):
        self.str = name
        self.reset_val = tuple(start)
        self.state = tuple(start)
        self.playlist = players
        self.num_p = len(players)
        self.blocked = None  # being robbed
        # should have length 4
        for n,i in enumerate(players):
            setattr(self, 'p'+str(n), i)


    def loss(self, player_no):
        conds = [i >= 10 for i in self.state]
        del conds[player_no]
        if any(conds):
            return True
        else:
            return False

    def win(self, player_no):
        if self.state[player_no] >= 10:
            return True
        else:
            return False

    def civ_size(self):
        no_cities = np.array([np.ceil(2*np.cbrt(i-4)) for i in self.state])
        return np.maximum(no_cities, 2*np.ones(self.num_p))

    def harvest(self):
        # p = (np.array([1, 2, 3, 4, 5, 5, 4, 3, 2, 1]) / 36.).mean()
        p = 0.0834
        # har = np.array([np.random.binomial(i, .084) for i in self.civ_size()])
        har = np.random.binomial(3, .084, size=4)
        if self.blocked is not None:
            har[self.blocked] = 0
            # print 'thief is blocking Player {0}'.format(self.blocked)
        # print 'players received ', har
        return har

    def valid_moves(self, player_no):
        # a placeholder for now
        j = player_no
        n = self.num_p
        moves = [n*[0]]
        others = range(n)
        del others[j]
        for i in others:
            move = n*[0]
            move[j] = 1
            move[i] = -1
            moves += [move]
        return np.array(moves)

    def take_turn(self, player):

        if np.random.rand(1) >= 1./6.:  # not roll 7
            self.state = tuple(np.add(self.state, self.harvest()))
        else:  # roll 7
            valids = self.valid_moves(player.order)
            player.make_key(tuple(self.state), valids)

        # next, determine an action
            move = tuple(player.take_action(self.state, valids))
            # print 'player {0} made move '.format(player.str), move
            if np.min(move) == -1:  # being robbed...defector
                self.blocked = np.argmin(move)
            self.state = tuple(np.add(self.state, move))

            for agent in self.playlist:
                offset = agent.order - player.order
                rmove = tuple(np.roll(move, offset))
                rstate = tuple(np.roll(self.state, offset))
                rvalids = np.roll(valids, offset, axis=1)
                agent.update_Q(rstate, rmove, rvalids,
                               self.win(agent.order),
                               self.loss(agent.order))

    def one_round(self):
        for i in self.playlist:
            self.take_turn(i)

    def play(self):
        while not np.any([self.win(i) for i in range(self.num_p)]):
            self.one_round()
        # print 'hi'

    def reset(self):
        self.state = tuple(self.reset_val)
