import numpy as np

import nans_lib


class PathGenerator:
    _enemy_start = None
    _enemy_target = None
    _my_start = None
    _enemy_path_order = None

    def __init__(self):
        self._enemy_start = np.array([0, 1000])
        self._enemy_target = np.array([1000, 1000])
        self._my_start = np.array([500, 1000])
        self._enemy_path_order = 2
        # order = 2 is natural due to curvature of Earth, and taking shortest possible path, and gravity being weaker away from surface

    def generate_enemy_path(self, middle_point):
        x = [self._enemy_start[0], middle_point[0], self._enemy_target[0]]
        f_x = [self._enemy_start[1], middle_point[1], self._enemy_target[1]]

        p = nans_lib.lagrange_interpolation(x, f_x)

        return lambda v: np.polyval(p, v)

    def approximate_enemy_path(self, points):
        x = []
        y = []

        for i in range(len(points)):
            x.append(points[i][0])
            y.append(points[i][1])

        p = nans_lib.least_squares_regression(x, y, self._enemy_path_order)

        return lambda v: np.polyval(p, v)

    def generate_lead_path(self, enemy_evaluated):
        x = [self._my_start[0], enemy_evaluated[0]]
        y = [self._my_start[1], enemy_evaluated[1]]
        order = 1  # lead calculates line(order = 1) for intercepting
        p = nans_lib.least_squares_regression(x, y, order)

        return lambda v: np.polyval(p, v)
