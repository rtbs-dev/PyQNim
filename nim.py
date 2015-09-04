__author__ = 'Thurston'

import numpy as np
from agents import *


class Nim:

    def __init__(self, name, start, p1, p2):
        import numpy as np
        self.str=name
        self.reset_val=start
        self.state=start
        self.p1=p1
        self.p2=p2

    def valid_moves(self,state):
        # a placeholder for now
        return [i for i in [1, 2, 3] if (i<=state)]

    def play(self):
        player=self.p1
        # print 'There are ', self.state, 'sticks to pick up'
        self.p1.games_played+=1
        self.p2.games_played+=1
        while True:

            if self.state==1:
                move=1
                self.state = self.state-move

                #print "player ", player.str, 'loses.'

                if player.playertype=='Q':
                    player.update_Q(self.state, move, self.valid_moves(self.state+move))
                break

            #print 'Player ', player.str

            if player.playertype=='human':
                while True:
                    move = input("What is your move? ")
                    if move in self.valid_moves(self.state):
                        break
                    print "Invalid Move"
            elif player.playertype=='Q':
                # first, make this state's table
                player.makeKey(self.state, self.valid_moves(self.state))

                # next, determine an action
                move = player.take_action(self.state, self.valid_moves(self.state))
                #print "He picks up", move, " sticks."

            elif player.playertype=='perfect':
                if self.state==self.reset_val:
                    move = self.state%(3+1)
                elif self.state<=4:
                    move = self.state - 1
                else:
                    move = (3+1) - move

                #print "He picks up", move, " sticks."
            else:
                move = np.random.choice(self.valid_moves(self.state))
                #print "He picks up", move, " sticks."
            #print self.state, move

            self.state = self.state-move
            #print self.state
            # now, update Q
            if player.playertype=='Q':
                player.update_Q(self.state, move, self.valid_moves(self.state))

            #print '# of objects: ', self.state

            #if self.state==1:
            #    print "player ", player.str, 'wins.'

            if self.state==0:
                #print "player ", player.str, 'loses.'
                if player.playertype=='Q':
                    player.update_Q(self.state, move, self.valid_moves(self.state+move))
                break

            if player==self.p1:
                player=self.p2
            else:
                player=self.p1

            # learn from the other guy
            if player.playertype=='Q':
                player.makeKey(self.state+move, self.valid_moves(self.state+move))
                player.update_Q(self.state, move, self.valid_moves(self.state), flipped=True)

        #print 'Game Over'
    def reset(self):
        self.state = self.reset_val