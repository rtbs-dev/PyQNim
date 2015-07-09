__author__ = 'Thurston'

from agents import *
from nim import *
import matplotlib.pyplot as plt

def Brain_Show(Q, dim, ax):

    qplot=np.zeros(dim)


    for state in Q.keys():
        for action in Q[state].keys():
            qplot[action-1, state-1] = Q[state][action]
    sct=None
    if ax is None:
        fig = plt.figure()
        ax=fig.add_subplot(111)
    plt.ion()
    plt.show

    if sct is not None:
        del ax.lines[0]
    sct=ax.matshow(qplot, cmap='hot', extent=[.5,dim[1]+.5,3.5,0.5], vmin=0, vmax=1)
    ax.set_xticks(range(1,dim[1]+1))
    ax.set_xlabel('state')
    ax.set_ylabel('action')
    ax.set_title('Evolution of Q-table')
    ax.xaxis.set_ticks_position('bottom')
    #ax.tight_layout()
    plt.pause(.001)

    #print qplot


def run_Q(game, trials, anim=True):

    if anim:

        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

    for i in range(trials):
        game.reset()
        game.play()
        if anim:
            if game.p1.playertype == 'Q':
                Brain_Show(game.p1.Q, (3, game.reset_val), ax1)
            if game.p2.playertype == 'Q':
                Brain_Show(game.p2.Q, (3, game.reset_val), ax2)