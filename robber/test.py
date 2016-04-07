import numpy as np
import q_learn as ql
import robbery as rb
import pickle as pkl
from tqdm import tqdm


q1 = ql.Agent('p1')
q2 = ql.Agent('p2')
q3 = ql.Agent('p3')
q4 = ql.Agent('p4')

game = rb.Robbery('test', [2,2,2,2], *ql.Agent.get_agents())

for i in tqdm(range(100000)):
    game.reset()
    game.play()

# for i in ql.Agent.get_agents():
#     with open(i.str+'_table.txt', 'w') as f:
#         pkl.dump(i.Q, f)
# print game.state