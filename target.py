import arcade
import numpy as np

import SAT


class Target:

    def __init__(self, target_point):
        self._scale = 0.5
        self._sprite = None
        self._point = np.array([target_point[0], target_point[1] + 50 * self._scale])

        self._polygon = SAT.Polygon(np.array([
            [self._point[0] + 100 * self._scale, self._point[1] + 50 * self._scale],
            [self._point[0] + 100 * self._scale, self._point[1] - 50 * self._scale],
            [self._point[0] - 100 * self._scale, self._point[1] - 50 * self._scale],
            [self._point[0] - 100 * self._scale, self._point[1] + 50 * self._scale]], dtype="f"))

    @property
    def polygon(self):
        return self._polygon

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite
        self._sprite.set_position(self._point[0], self._point[1])

    @property
    def scale(self):
        return self._scale
