import numpy as np
import q_learn as ql
import robbery as rb
import pickle as pkl
from tqdm import tqdm


q1 = ql.Agent('p1')
q2 = ql.Agent('p2')
q3 = ql.Agent('p3')
q4 = ql.Agent('p4')

# game = rb.Robbery('test', [0, 0, 0, 0], *ql.Agent.get_agents())
game = rb.Robbery('test', [1,1,1,1], *ql.Agent.get_agents())

for i in tqdm(range(100000)):
    game.reset()
    game.play()



for i in ql.Agent.get_agents():
    with open('./deterministic/'+i.str+'_table_1M_FOURS(1111)_alpha1.txt', 'wb-') as f:
        pkl.dump({'Q': i.Q, 'games_played': i.games_played, 'games_won': i.wins}, f)
