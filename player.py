import numpy as np

from SAT import Polygon


class Player:
    def __init__(self, starting_point,speed):
        self._point = starting_point
        self._scale = 0.2
        self.angle = np.pi / 4
        self._sprite = None
        self._polygon = Polygon(np.array([
            [self._point[0], self._point[1] + 250 * self._scale],
            [self._point[0] + 250 * self._scale, self._point[1] + 250 * self._scale],
            [self._point[0] + 250 * self._scale, self._point[1] - 250 * self._scale],
            [self._point[0] - 250 * self._scale, self._point[1] - 250 * self._scale],
            [self._point[0] - 250 * self._scale, self._point[1] + 250 * self._scale]], dtype="i"))
        self._speed = speed

    def move(self,x_inc,y_inc):
        x_inc= int(x_inc)
        y_inc = int(y_inc)
        inc = np.array([x_inc,y_inc],dtype="i")

        self._point+= inc

        for i in self._polygon.vertices:
            i+= inc

    @property
    def scale(self):
        return self._scale

    @property
    def point(self):
        return self._point

    @property
    def polygon(self):
        return self._polygon

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self,sprite):
        self._sprite = sprite

    @property
    def speed(self):
        return self._speed
