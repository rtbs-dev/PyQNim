# PyQNim
A q-Learning Nim implementation in python

agents.py includes 4 different implementations of an agent to play a game. Though all are wrtten ambigously, the Q-learning agentcurrently only functions for the 1-D action/state environment (i.e. nim). 

nim.py contains the actual game, as well as if statements for the play strategies for each supported agent type. 

qIter.py contains helper functions for training the Q values over many trials, as well as visualizing. NB to see the Q-'brain' 
after training is complete, call the Brain_Show() function with an ax=None key after the player.Q dict. This will then instantiate a new pyplot frame, rather than the default subplot for viewing the animation while it learns. 

A note on visualization: For some reason, the iteration speed slows signifigantly after ~100 iterations when the plotting window is left open. Closing the window will allow >30k iterations to finish quickly (~20-30sec on the original machine). Since the previous axis draw is deleted on every iteration before a new one is drawn, the reason for this slow-down after a certain number of iterations is unknown. Please do not use inline plotting on IPython for the animation...it is not currently supported (use <%matplotlib qt> magic to remove the inline setting if needed, for the running cell).  
