import matplotlib.pyplot as plt
import numpy as np
import scipy.constants

import nans_lib
import pathGenerator


class Projectile(object):
    # _acceleration = 0
    # _velocity = 0
    # path = None
    # _polygon = None
    # _point = None
    # _sprite = None

    def __init__(self, path=None, max_engine=50000, mass=1500, A=20, Cd=0.5):
        self._A = A
        self._acceleration = 12
        self._velocity = 20
        self._polygon = None
        self._point = np.array([0, np.polyval(path, 0)])
        self._path = path
        self._Cd = Cd
        self._mass = mass
        self._weight = scipy.constants.g * mass
        self._angle = 0
        self._s = 0

    def _calculate_drag(self, ro=0.5):
        # CD coefficient of drag
        # ro air density
        # v velocity
        # A reference area
        D = self._Cd * ro * (self._velocity ** 2 * self._A) / 2
        return D

    def calculate_path_force(self):
        path_prime = np.polyder(self._path)
        self._angle = np.arctan(np.polyval(path_prime, self._point[0]))
        drag = self._calculate_drag()
        drag_x = drag * np.cos(self._angle)
        drag_y = drag * np.sin(self._angle)
        push = lambda x: np.tan(self._angle) * (x - self._point[0]) + self._point[1]

        func = lambda x: np.polyval(self._path, x) \
                         - np.sqrt((push(x) * np.sin(self._angle) - drag_y - self._weight) ** 2 + (
                push(x) * np.cos(self._angle) - drag_x) ** 2)
        zero_x, it = nans_lib.zeroBisection(func, self._point[0], self._point[0] + 50)
        zero_y = np.polyval(self._path, zero_x)

        F = np.sqrt((self._point[0] - zero_x) ** 2 + (self._point[1] - zero_y) ** 2)

        self._angle = np.arctan((zero_y - self._point[1]) / (zero_x - self._point[0]))
        return F, lambda x: (zero_y - self._point[1]) / (zero_x - self._point[0]) * (x - self._point[0]) + self._point[
            1]

    def calculate_distance(self, t):
        F, func = self.calculate_path_force()
        dds = lambda *argv: F / self._mass
        tb = t + 1 / 60
        h = 1 / 1000

        fx_rk4 = nans_lib.rk4N(t, tb, h, np.array([self._s, self._velocity]), dds)
        self._s += fx_rk4[-1][-1][-1]
        self._velocity = nans_lib.rk4WithoutPlot(t, tb, h, self._velocity, dds)[-1]
        self._update_points(fx_rk4[-1][-1][-1])
        return fx_rk4[-1]

    def _update_points(self, distance):
        dist_arr = np.array([distance * np.cos(self._angle), distance * np.sin(self._angle)])
        self._point += dist_arr
        # for i in self._polygon:
        #     i += dist_arr

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def angle(self):
        return self._angle

    @property
    def point(self):
        return self._point


if __name__ == '__main__':
    pg = pathGenerator.PathGenerator()
    path = pg.generate_enemy_path(np.array([500, 500]))
    p1 = Projectile(path)
    print(path)
    pts = np.linspace(0, 1000, 200)
    f = lambda x: np.polyval(path, x)
    f_x = f(pts)
    plt.plot(pts, f_x)
    for i in range(100):
        F, func = p1.calculate_path_force()
        # print(F)
        plt.scatter(*p1.point, c="red")

        print(p1.calculate_distance(i / 60)[-1][-1])

    plt.show()
