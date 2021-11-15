from typing import List, Callable

import numpy as np

from environment import State, ManipulatorEnv


class RRTPlanner:

    def __init__(self,
                 env: ManipulatorEnv,
                 distance_fn: Callable,
                 max_angle_step: float = 10.0):
        """
        :param env: manipulator environment
        :param distance_fn: function distance_fn(state1, state2) -> float
        :param max_angle_step: max allowed step for each joint in degrees
        """
        self._env = env
        self._distance_fn = distance_fn
        self._max_angle_step = max_angle_step

    def plan(self,
             start_state: State,
             goal_state: State) -> List[State]:
        # TODO: Implement
        pass
