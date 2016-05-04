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
        conds = np.array([i >= 5 for i in self.state])
        some_winner = sum(conds) > 0.

        # lead = np.where(np.array(self.state) == np.max(self.state))[0]
        # not_best = player_no not in lead and lead.size == 1
        # del conds[player_no]
        if (not conds[player_no]) and some_winner:
            return True
        else:
            return False

    def win(self, player_no):
        conds = [i >= 5 for i in self.state]
        if conds[player_no]:
            return True
        else:
            return False
        # at_least = self.state[player_no] >= 3
        # lead = np.where(np.array(self.state) == np.max(self.state))[0]
        # best = player_no in lead and lead.size == 1
        # if at_least and best:
        #     return True
        # else:
        #     return False

    # def civ_size(self):
    #     no_cities = np.array([np.ceil(2*np.cbrt(i-4)) for i in self.state])
    #     return np.maximum(no_cities, 2*np.ones(self.num_p))

    # def harvest(self):
    #     # Increasing w/ wealth
    #     # p = (np.array([1, 2, 3, 4, 5, 5, 4, 3, 2, 1]) / 36.).mean()
    #     # har = np.array([np.random.binomial(i, .084) for i in self.civ_size()])
    #
    #     # Flat chance
    #     # p = 0.0834
    #     # har = np.random.binomial(2, .084, size=self.num_p)
    #
    #     # Uniform deterministic income
    #     har = np.ones(self.num_p)
    #
    #     if self.blocked is not None:
    #         har[self.blocked] = 0
    #         # print 'thief is blocking Player {0}'.format(self.blocked)
    #     # print 'players received ', har
    #     return har

    def valid_moves(self, player_no):
        # a placeholder for now
        j = player_no
        n = self.num_p
        moves = [n*[1]]
        others = range(n)
        del others[j]
        for i in others:
            move = n*[1]
            if self.state[i] == 0:  # has something to steal?
                move[i] = 0  # no...
            else:
                move[j] = 2  # yes...
                move[i] = -1
            moves += [move]
        # mask = np.logical_or(np.array(self.state) != 0, np.array(moves)[:, j] == 1)
        # mask[j] = True
        # print np.min()
        # print player_no
        # print np.array(moves), self.state, mask
        return np.array(moves)

    # def take_turn(self, player):
    #     no_cities = np.array([np.ceil(2*np.cbrt(i-4)) for i in self.state])
    #     return np.maximum(no_cities, 2*np.ones(n))

    # '''Like Catan, robber only able to be moved once a 7 is rolled.
    # '''
    #     if np.random.rand(1) >= 1./6.:  # not roll 7
    #         self.state = tuple(np.add(self.state, self.harvest()))
    #     else:  # roll 7
    #         valids = self.valid_moves(player.order)
    #         player.make_key(tuple(self.state), valids)
    #
    #     # next, determine an action
    #         move = tuple(player.take_action(self.state, valids))
    #         # print 'player {0} made move '.format(player.str), move
    #         if np.min(move) == -1:  # being robbed...defector
    #             self.blocked = np.argmin(move)
    #         self.state = np.add(self.state, move)
    #         self.state[self.state < 0] = 0
    #         self.state = tuple(self.state)
    #
    #         # player.update_Q(self.state, move, valids,
    #         #                 self.win(player.order),
    #         #                 self.loss(player.order))
    #         for agent in self.playlist:
    #             offset = agent.order - player.order
    #             rmove = tuple(np.roll(move, offset))
    #             rstate = tuple(np.roll(self.state, offset))
    #             rvalids = np.roll(valids, offset, axis=1)
    #             agent.update_Q(rstate, rmove, rvalids,
    #                            self.win(player.order),
    #                            self.loss(player.order))
    def take_turn(self, player):
        """
        Players always receive 1 if not blocked. Players can always rob. (deterministic)
        """

        # self.state = tuple(np.add(self.state, self.harvest()))

        valids = self.valid_moves(player.order)
        player.make_key(tuple(self.state), valids)

        # next, determine an action
        move = tuple(player.take_action(self.state, valids))
        # print 'player {0} made move '.format(player.str), move
        if np.min(move) == -1:  # being robbed...defector
            self.blocked = np.argmin(move)
        self.state = np.add(self.state, move)
        self.state[self.state < 0] = 0
        self.state = tuple(self.state)

        # player.update_Q(self.state, move, valids,
        #                 self.win(player.order),
        #                 self.loss(player.order))
        for agent in self.playlist:
            offset = agent.order - player.order
            rmove = tuple(np.roll(move, offset))
            rstate = tuple(np.roll(self.state, offset))
            rvalids = np.roll(valids, offset, axis=1)
            agent.update_Q(rstate, rmove, rvalids,
                           self.win(player.order),
                           self.loss(player.order))

    def one_round(self):
        for i in self.playlist:
            if np.any([self.win(j) for j in range(self.num_p)]):
                break
            self.take_turn(i)

    def play(self):
        while not np.any([self.win(i) for i in range(self.num_p)]):
            self.one_round()
        # print 'hi'

    def reset(self):
        self.state = tuple(self.reset_val)
