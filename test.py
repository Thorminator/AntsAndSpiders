import time

import numpy as np

from game import Game

game = Game()
observations = []
while True:
    action = [[1, 0] for _ in range(10)]
    game.apply_action(np.array(action))
    observations.append(game.get_observation())
    time.sleep(0.02)
