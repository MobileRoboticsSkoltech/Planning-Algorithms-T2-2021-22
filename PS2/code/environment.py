import numpy as np
import matplotlib.pyplot as plt


class State:

    def __init__(self, angles: np.ndarray):
        """
        Represents the state of the 4-link manipulator.

        :param angles: 4 angles for each link of the manipulator in degrees. Shape: (4,).
        """
        assert angles.shape == (4,)
        assert (np.abs(angles) >= 0.0).all() and (np.abs(angles) <= 180.0).all()
        self._angles = angles.copy()
        self._joints = State._calculate_joint_positions(angles)

    @property
    def angles(self) -> np.ndarray:
        """
        :return: 4 angles for each link of the manipulator in degrees
        """
        return self._angles

    @property
    def joints(self) -> np.ndarray:
        """
        :return: Positions of the 5 joints of the manipulator. Shape: (5, 2).
        """
        return self._joints

    @staticmethod
    def _calculate_joint_positions(angles: np.ndarray) -> np.ndarray:
        seg = np.zeros((5, 2))
        a1, a2, a3, a4 = np.deg2rad(angles)
        T1 = State._se2(np.array([0, 0, a1]))  # this is the first joint, a simple rotation
        T2 = State._se2(
            np.array([1, 0, a2]))  # the second joint, it is a bar of d =1, plus a rotation for the second joint
        T3 = State._se2(np.array([1, 0, a3]))
        T4 = State._se2(np.array([1, 0, a4]))
        T5 = State._se2(
            np.array([1, 0, 0]))  # this is simply to express the lenght of the second bar, no rotation required
        p = T1 @ T2 @ np.array([0, 0, 1])
        seg[1, :] = p[:2]
        p = T1 @ T2 @ T3 @ np.array([0, 0, 1])
        seg[2, :] = p[:2]
        p = T1 @ T2 @ T3 @ T4 @ np.array([0, 0, 1])
        seg[3, :] = p[:2]
        p = T1 @ T2 @ T3 @ T4 @ T5 @ np.array([0, 0, 1])
        seg[4, :] = p[:2]
        return seg

    @staticmethod
    def _se2(q):
        x, y, t = q
        T = np.array([
            [np.cos(t), -np.sin(t), x],
            [np.sin(t), np.cos(t), y],
            [0, 0, 1]])
        return T


class ManipulatorEnv:

    OBSTACLES_DIM = 3  # x, y, radius (assume all obstacles are circles)
    N_LINKS = 4

    def __init__(self,
                 obstacles: np.ndarray,
                 initial_state: State,
                 collision_threshold: float = 0.1):
        assert len(obstacles.shape) == 2 and obstacles.shape[1] == ManipulatorEnv.OBSTACLES_DIM
        self._obstacles = obstacles.copy()
        self._state = initial_state
        self._collision_threshold = collision_threshold

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        self._state = new_state

    def check_collision(self, state_to_check: State) -> bool:
        """
        Checks state (configuration) for the collisions.
        :return True if collision, False if no collisions
        """
        for obs in self._obstacles:
            for i in range(ManipulatorEnv.N_LINKS):
                segment = state_to_check.joints[[i, i+1], :]
                r = obs[2] + self._collision_threshold
                p0 = obs[:2]
                p1 = segment[0]
                p2 = segment[1]

                # Check if p1 or p2 in circle
                if np.linalg.norm(p0 - p1) <= r or np.linalg.norm(p0 - p2) <= r:
                    return True

                # Find projection
                t = np.sum((p0 - p1) * (p2 - p1)) / (np.linalg.norm(p2 - p1) ** 2)
                # Check if the projection is on the line
                # (in other words, if line is fully in the circle)
                if t < 0.0 or t > 1.0:
                    continue
                p4 = p1 + t * (p2 - p1)

                if np.linalg.norm(p0 - p4) <= r:
                    return True

                # distance = np.linalg.norm(np.cross(p2-p1, p1-p0)) / np.linalg.norm(p2-p1)
                # pro
                # distance = distance - r
                # if distance <= r:
                #     return False
        return False

    def render(self, plt_show=True) -> None:
        """
        Displays current configuration.
        :param plt_show: whether to call plt.show() or not
        """
        self._plot_segment(self._state.joints[[0, 1], :], np.array([1, 0, 0]),
                           is_start_link=True)
        self._plot_segment(self._state.joints[[1, 2], :], np.array([0, 1, 0]))
        self._plot_segment(self._state.joints[[2, 3], :], np.array([0, 0, 1]))
        self._plot_segment(self._state.joints[[3, 4], :], np.array([1, 0, 1]),
                           is_end_link=True)
        for obs in self._obstacles:
            plt.gca().add_patch(
                plt.Circle((obs[0], obs[1]), obs[2], fill=True))
        plt.axis('equal')
        if plt_show:
            plt.show()

    @staticmethod
    def _plot_segment(s, color_, is_start_link=False, is_end_link=False):
        plt.plot(s[:, 0], s[:, 1], linewidth=2, color=color_)
        if is_end_link:
            plt.plot(s[1, 0], s[1, 1], marker='>', color=color_)
        else:
            plt.plot(s[1, 0], s[1, 1], marker='o', color=color_)
        if is_start_link:
            plt.plot(s[0, 0], s[0, 1], marker='X', color=color_)
        else:
            plt.plot(s[0, 0], s[0, 1], marker='o', color=color_)
