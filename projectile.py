import numpy as np
import scipy.constants

import nans_lib


class Projectile(object):
    # _acceleration = 0
    # _velocity = 0
    # path = None
    # _polygon = None
    # _point = None
    # _sprite = None

    def __init__(self, polygon, max_engine=50000, mass=1500, path=None, A=20, Cd=0.5):
        self._A = A
        self._acceleration = 12
        self._velocity = 20
        self._polygon = polygon
        self._point = polygon[0]
        self._path = path
        self._Cd = Cd
        self._weight = scipy.constants.g * mass
        self._angle = 0

    def _calculate_drag(self, ro=0.5):
        # CD coefficient of drag
        # ro air density
        # v velocity
        # A reference area
        D = self._Cd * ro * (self._velocity ** 2 * self._A) / 2
        return D

    def calculate_path_force(self):
        path_prime = np.polyder(self._path)
        self._angle = np.arctan(path_prime(self._point[0]))
        drag = self._calculate_drag()
        drag_x = drag * np.cos(self._angle)
        drag_y = drag * np.sin(self._angle)
        push = lambda x: np.tan(self._angle) * (x - self._point[0]) + self._point[1]

        func = lambda x: np.polyval(self._path, x) \
                         - np.sqrt((push(x) * np.sin(self._angle) - drag_y - self._weight) ** 2 + (
                push(x) * np.cos(self._angle) - drag_x) ** 2)
        zero_x, zero_y, _ = nans_lib.zeroBisection(func, self._point[0], self._point[0] + 50)

        return lambda x: (zero_y - self._point[1]) / (zero_x - self._point[0]) * (x - self._point[0]) + self._point[1]

    def calculate_speed(self, t):
        self._point, _ = nans_lib.rk4N(t, t + 1 / 60, 1 / 1000, np.array([self._velocity, self._point]),
                                           self.calculate_path_force())

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def angle(self):
        return self._angle
