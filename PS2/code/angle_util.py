from typing import Union
import numpy as np


def angle_difference(angle1: Union[float, np.ndarray],
                     angle2: Union[float, np.ndarray],
                     directional=False) -> Union[float, np.ndarray]:
    """
    :param angle1: first angle in degrees
    :param angle2: second angle in degrees
    :param return: signed diff between angles (from 0 to 180)
    """
    if type(angle1) is np.ndarray:
        assert type(angle1) == type(angle2)
        assert angle1.shape == angle2.shape
        return np.array([angle_difference(a1, a2) for (a1, a2) in zip(angle1, angle2)])
    delta_angle = angle1 - angle2
    delta_angle = (delta_angle + 180) % 360 - 180
    return delta_angle


def angle_linspace(start_angle: Union[float, np.ndarray],
                   end_angle: Union[float, np.ndarray],
                   n: int):
    """
    :param start_angle: start angle (or whole configuration) in degrees
    :param end_angle: end angle (or whole configuration) in degrees
    :param n: number of steps
    """
    if type(start_angle) is np.ndarray:
        assert type(start_angle) == type(end_angle)
        assert start_angle.shape == end_angle.shape
        return np.array([angle_linspace(a1, a2, n) for (a1, a2) in zip(start_angle, end_angle)]).T

    step = angle_difference(end_angle, start_angle) / n
    result = [start_angle]
    for _ in range(n):
        new_item = result[-1] + step
        if np.abs(new_item) > 180.0:
            if new_item > 0.0:
                new_item = new_item - 360.0
            else:
                new_item = new_item + 360.0
        result.append(new_item)
    return np.array(result)
