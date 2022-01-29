import numpy as np
import nans_lib


class PathGenerator:
    _enemy_start = None
    _enemy_target = None
    _my_start = None
    _enemy_path_order = None
    _file_path = None

    def __init__(self):
        self._enemy_start = np.array([0, 0])
        self._enemy_target = np.array([1000, 0])
        self._my_start = np.array([500, 1000])
        self._enemy_path_order = 2
        # order = 2 is natural due to curvature of Earth, and taking shortest possible path, and gravity being weaker away from surface

        self._file_path = "enemy_middle_points"

    def generate_enemy_path(self, middle_point):
        x =np.array([self._enemy_start[0], middle_point[0], self._enemy_target[0]])
        f_x = np.array([self._enemy_start[1], middle_point[1], self._enemy_target[1]])

        p = nans_lib.lagrange_interpolation(x, f_x)

        return p

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

    def get_enemy_point_from_file(self, line_index):
        enemy_point_file = open(self._file_path, "r")
        lines = enemy_point_file.readlines()
        if len(lines) <= line_index:
            x = float(lines[-1].split("|")[0])
            y = float(lines[-1].split("|")[1])
        else:
            x = float(lines[line_index].split("|")[0])
            y = float(lines[line_index].split("|")[1])

        return self.generate_enemy_path(np.array([x, y]))
