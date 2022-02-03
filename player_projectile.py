import numpy as np
import scipy.constants
import lead_collision
import nans_lib
from SAT import Polygon


class PlayerProjectile():
    def __init__(self, inital_point, max_engine=50, mass=1500, A=20, Cd=0.5):
        self._scale = 0.05
        self._A = A
        self._acceleration = 12
        self._velocity = 17
        self._point = inital_point
        self._polygon = Polygon(np.array([
            [self._point[0], self._point[1] + 850 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] + 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] + 820 * self._scale],
            [self._point[0] + 200 * self._scale, self._point[1] - 820 * self._scale],
            [self._point[0] - 200 * self._scale, self._point[1] - 820 * self._scale]], dtype="f"))
        self._Cd = Cd
        self._mass = mass
        self._weight = scipy.constants.g * mass
        self._angle1 = 0
        self._angle2 = 2.2
        self._previous_angle2 = 0
        self._s = 0
        self._max_engine = max_engine

    def _calculate_drag(self, ro=0.5):
        # CD coefficient of drag
        # ro air density
        # v velocity
        # A reference area
        D = self._Cd * ro * (self._velocity ** 2 * self._A) / 2
        return D

    def calculate_path_force(self, enemy):
        drag = self._calculate_drag()
        # drag_x = drag * np.cos(self._angle1)
        # drag_y = drag * np.sin(self._angle1)

        # we have length of vector for enemy direction
        norm, _ = enemy.calculate_path_force()
        # we have angle of vector
        theta = np.deg2rad(enemy.angle1)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # we form vector and rotate it
        vector_of_prediction = np.array([norm, 0])
        vector_of_prediction = np.dot(rot, vector_of_prediction)

        F = self._max_engine - drag
        angle = np.angle(vector_of_prediction)

        norm = np.sqrt(
            (F*np.sin(angle) - self._weight)**2 + (F*np.cos(angle))**2
        )

        # we have length of friendly vector
        # norm = 100
        # we have angle of friendly vector
        theta = np.deg2rad(self.angle1)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # we form vector and rotate it
        vector_of_movements = np.array([norm, 0])
        vector_of_movements = np.dot(rot, vector_of_movements)

        push = self._max_engine * lead_collision.lead_collision(vector_of_movements, self._point, vector_of_prediction,
                                                                enemy.point)
        # calculate new angle
        i = np.array([1, 0])
        cos = np.dot(push, i) / np.linalg.norm(push) / np.linalg.norm(i)
        self._angle1 = np.arccos(cos)

        # new angle points to enemy rocket
        self._previous_angle2 = self._angle2
        between = self.point - enemy.point
        i = np.array([1, 0])
        cos = np.dot(between, i) / np.linalg.norm(between) / np.linalg.norm(i)
        self._angle2 = np.arccos(cos)
        return 100

    def calculate_distance(self, t, enemy):
        F = self.calculate_path_force(enemy)
        dds = lambda *argv: F / self._mass
        tb = t + 1 / 60
        h = 1 / 1000

        fx_rk4 = nans_lib.rk4N(t, tb, h, np.array([self._s, self._velocity]), dds)
        self._s += fx_rk4[-1][-1][-1]
        self._velocity = nans_lib.rk4WithoutPlot(t, tb, h, self._velocity, dds)[-1]
        self._update_points(fx_rk4[-1][-1][-1])
        return fx_rk4[-1]

    def _update_points(self, distance):
        dist_arr = np.array([distance * np.cos(self._angle1), distance * np.sin(self._angle1)])
        self._point += dist_arr.astype(int)
        for i in self._polygon.vertices:
            i += dist_arr
            temp_x = i[0] - self._point[0]
            temp_y = i[1] - self._point[1]

            # now apply rotatio
            angle_radians = self._angle2 - self._previous_angle2
            cos_angle = np.cos(angle_radians)
            sin_angle = np.sin(angle_radians)
            rotated_x = temp_x * cos_angle - temp_y * sin_angle
            rotated_y = temp_x * sin_angle + temp_y * cos_angle

            # translate back
            i[0] = rotated_x + self._point[0]
            i[1] = rotated_y + self._point[1]
        print(self._polygon.vertices)

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
