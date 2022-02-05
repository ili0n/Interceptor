import numpy as np
import scipy.constants

import nans_lib
import pure_pursuit
import SAT


class PlayerProjectile():
    def __init__(self, inital_point, max_engine=20, mass=1500, A=20, Cd=0.5):
        self._scale = 0.05
        self._A = A
        self._acceleration = 12
        self._velocity = 7
        self._point = inital_point
        self._polygon = SAT.Polygon(np.array([
            [self._point[0], self._point[1] + 850 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] + 820 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] - 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] - 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] + 820 * self._scale]], dtype="i"))
        self._Cd = Cd
        self._mass = mass
        self._weight = scipy.constants.g * mass
        self._angle = np.pi * 0.5
        self._previous_angle = np.pi * 0.5
        self._s = 0
        self._max_engine = max_engine
        self._goal_point = None

    def _calculate_drag(self, ro=0.5):
        # CD coefficient of drag
        # ro air density
        # v velocity
        # A reference area
        D = self._Cd * ro * (self._velocity ** 2 * self._A) / 2
        return D

    def calculate_force(self):
        self._previous_angle, self._angle = self._angle, pure_pursuit.calculate_angle(self._goal_point, self._point)
        drag = self._calculate_drag()
        push_int = self._max_engine - drag
        push = np.sqrt((push_int * np.sin(self._angle) - self._weight) ** 2 + (push_int * np.cos(self._angle)) ** 2)

        return push

    def calculate_distance(self, t, enemy):
        # self._goal_point = pure_pursuit.find_goal_point(self._point, enemy.polygon.vertices)
        F = self.calculate_force()
        dds = lambda *argv: F / self._mass
        tb = t + 1 / 60
        h = 1 / 1000

        fx_rk4 = nans_lib.rk4N(t, tb, h, np.array([self._s, self._velocity]), dds)
        self._s += fx_rk4[-1][-1][-1]
        self._velocity = nans_lib.rk4WithoutPlot(t, tb, h, self._velocity, dds)[-1]

        self._update_points(fx_rk4[-1][-1][-1])
        return fx_rk4[-1]

    def _update_points(self, distance):
        translation = np.array([
            np.cos(self._angle) * distance,
            np.sin(self._angle) * distance
        ])
        self._point += translation.astype(int)
        rows, _ = np.shape(self.polygon.vertices)
        self.polygon.vertices = SAT.rotate(self.polygon.vertices, np.sum(self.polygon.vertices, axis=0) / rows,
                                           self.angle - self._previous_angle)
        self.polygon.vertices += translation.astype(int)
        print(self._polygon.vertices)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    # @property
    # def angle1(self):
    #     return self._angle1

    @property
    def angle(self):
        return self._angle

    @property
    def previous_angle(self):
        return self._previous_angle

    @property
    def point(self):
        return self._point

    @property
    def polygon(self):
        return self._polygon

    @property
    def scale(self):
        return self._scale

    @property
    def goal_point(self):
        return  self._goal_point

    @goal_point.setter
    def goal_point(self,goal):
        self._goal_point = goal
