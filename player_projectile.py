import matplotlib.patches
import numpy as np
import scipy.constants
import lead_collision
import nans_lib
from SAT import Polygon
import matplotlib.pyplot as plt

class PlayerProjectile():
    def __init__(self, inital_point, max_engine=1000, mass=500, A=20, Cd=0.5):
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
            [self._point[0] - 200 * self._scale, self._point[1] - 820 * self._scale]]))
        self._Cd = Cd
        self._mass = mass
        self._weight = scipy.constants.g * mass
        self._angle1 = 0.5 * np.pi
        self._previous_angle1 = 0.5 * np.pi
        self._angle2 = 0.5 * np.pi
        self._previous_angle2 = 0.5 * np.pi
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

        F = np.abs(self._max_engine - drag)
        i = np.array([1, 0])

        norm = np.sqrt(
            (F * np.sin(self.angle1) - self._weight) ** 2 + (F * np.cos(self.angle1)) ** 2
        )

        # we have length of friendly vector
        # norm = 100
        # we have angle of friendly vector
        theta = np.deg2rad(self.angle1)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # we form vector and rotate it
        vector_of_movements = np.array([norm, 0])
        vector_of_movements = np.dot(rot, vector_of_movements)

        direction, length = lead_collision.lead_collision(vector_of_movements, self._point, vector_of_prediction,
                                                          enemy.point)
        if length < norm and length != 0:
            engine_power = length
        else:
            engine_power = norm
        push = engine_power * direction
        # calculate new angle
        i = np.array([1, 0])
        cos = np.dot(push, i) / np.linalg.norm(push) / np.linalg.norm(i)
        self._previous_angle1 = self._angle1
        self._angle1 = np.arccos(cos)
        # diskutabilno
        if direction[0] < 0:
            self._angle1 *= -1

        # new angle points to enemy rocket
        between = - self.point + enemy.point
        i = np.array([1, 0])
        cos = np.dot(between, i) / np.linalg.norm(between) / np.linalg.norm(i)
        self._previous_angle2, self._angle2 = self.angle2, np.arccos(cos)
        if between[0] < 0:
            self._angle2 *= -1
        return F

    def calculate_distance(self, t, enemy):
        # lose racunanje sile, treba sopstvene a ne protivnicke
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
        translation = np.array([
            np.cos(self._angle1) * distance,
            np.sin(self._angle1) * distance
        ])
        self._point += translation.astype(int)
        rows, _ = np.shape(self.polygon.vertices)
        self.polygon.vertices = Rotate2D(self.polygon.vertices, np.sum(self.polygon.vertices, axis=0) / rows, self.angle1 - self._previous_angle1)
        self.polygon.vertices += translation.astype(int)
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
    def previous_angle1(self):
        return self._previous_angle1

    @property
    def point(self):
        return self._point

    @property
    def polygon(self):
        return self._polygon


def Rotate2D(points, center, angle):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return np.dot(points - center, np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])) + center


if __name__ == '__main__':
    pts = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    print(np.sum(pts, axis=0))
    rotated = Rotate2D(pts, np.array([0.5, 0.5]), np.pi/4)
    p = matplotlib.patches.Polygon(pts)
    p.fill = False

    r = matplotlib.patches.Polygon(rotated)
    r.fill = False

    fig, ax = plt.subplots()

    ax.add_patch(p)
    ax.add_patch(r)
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    # plt.plot(rotated)
    plt.show()
