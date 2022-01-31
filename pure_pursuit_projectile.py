import numpy as np
import scipy.constants

import nans_lib
import pure_pursuit
from SAT import Polygon


class PlayerProjectile():
    def __init__(self, inital_point, max_engine=30, mass=1500, A=20, Cd=0.5):
        self._scale = 0.05
        self._A = A
        self._acceleration = 12
        self._velocity = 17
        self._point = inital_point
        self._polygon = Polygon(np.array([
            [self._point[0], self._point[1] + 850 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] + 820 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] - 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] - 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] + 820 * self._scale]], dtype="f"))
        self._Cd = Cd
        self._mass = mass
        self._weight = scipy.constants.g * mass
        self._angle1 = 0
        self._angle2 = 2.2
        self._previous_angle2 = 0
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
        self._angle1 = np.arctan((self._goal_point[1] - self._point[1]) / (self._goal_point[0] - self._point[0]))
        self._angle2, self._previous_angle2 = self._angle1, self._angle2
        drag = self._calculate_drag()
        push_int = self._max_engine - drag
        push = np.sqrt((push_int * np.sin(self._angle1) - self._weight) ** 2 + (push_int * np.cos(self._angle1)) ** 2)

        return push

    def calculate_distance(self, t, enemy):
        self._goal_point = pure_pursuit.find_goal_point(self._point, enemy.polygon.vertices)
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
        next_point = pure_pursuit.calculate_new_position(self._goal_point, self._point, distance)
        self._point = next_point
        print(self._goal_point)
        for i in self._polygon.vertices:
            temp_x = i[0] - self._point[0]
            temp_y = i[1] - self._point[1]
            # now apply rotatio
            angle_radians = self._angle2 - self._previous_angle2
            cos_angle = np.cos(angle_radians)
            sin_angle = np.sin(angle_radians)
            rotated_x = temp_x * cos_angle - temp_y * sin_angle
            rotated_y = temp_x * sin_angle + temp_y * cos_angle

            # translate back
            i[0] = rotated_x + next_point[0]
            i[1] = rotated_y + next_point[1]
        # print(self._polygon.vertices)
        self._point = next_point

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def angle1(self):
        return self._angle1

    @property
    def angle2(self):
        return self._angle2

    @property
    def previous_angle2(self):
        return self._previous_angle2

    @property
    def point(self):
        return self._point

    @property
    def polygon(self):
        return self._polygon

    @property
    def scale(self):
        return self._scale
