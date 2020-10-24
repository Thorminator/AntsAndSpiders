from typing import Any

import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.typing import types

from game import Game


class RLGameEnvironment(py_environment.PyEnvironment):
    def __init__(self, simulate=True):
        super().__init__()
        self.game = Game(target_fps=0, simulate=simulate)
        self._action_spec = array_spec.BoundedArraySpec(shape=(10, 2), dtype=np.float32, minimum=0,
                                                        maximum=1, name="action")
        self._observation_spec = array_spec.BoundedArraySpec(shape=(17, 3), dtype=np.float32, minimum=0,
                                                             maximum=1, name="observation")

    def observation_spec(self) -> types.NestedArraySpec:
        return self._observation_spec

    def action_spec(self) -> types.NestedArraySpec:
        return self._action_spec

    def get_info(self) -> Any:
        return None

    def get_state(self) -> Any:
        return self.game.get_state()

    def set_state(self, state: Any) -> None:
        self.game.set_state(state)

    def _step(self, action: types.NestedArray) -> ts.TimeStep:
        action_caused_reset = self.game.apply_action(action)
        if self.game.game_over:
            return ts.termination(observation=self.game.get_observation(), reward=self.game.get_reward())
        return self.__get_current_time_step(first=action_caused_reset)

    def __get_current_time_step(self, first=False):
        observation = self.game.get_observation()
        if first:
            return ts.restart(observation=observation)
        else:
            return ts.transition(observation=observation, reward=self.game.get_reward(), discount=0.99)

    def _reset(self) -> ts.TimeStep:
        self.game.reset()
        return self.__get_current_time_step(first=True)
