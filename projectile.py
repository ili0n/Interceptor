import numpy as np
import scipy.constants


class Projectile(object):
    _acceleration = 0
    _velocity = 0
    path = None
    _polygon = None
    _point = None

    def __init__(self, polygon, path=None):
        self._acceleration = 12
        self._initial_velocity = 20
        self._polygon = polygon
        self._set_point()
        self._path = path

    def _set_point(self):
        pass
        # TODO nemanja dodaj sta treba

    def _calculate_drag(self):
        return 0  # TODO calculate drag

    def _calculate_current_velocity(self):
        path_prime = np.polyder(self._path)
        angle = np.arctan(path_prime(self._point[0]))

        distance = self._move_points(angle)

        velocity_x = self._velocity * np.cos(angle)
        velocity_y = self._velocity * np.sin(angle) - scipy.constants.g

        self._velocity = np.sqrt(velocity_y ** 2 + velocity_x ** 2) + self._acceleration - self._calculate_drag()

        return distance

    def _move_points(self, angle):
        distance_x = self._velocity * np.cos(angle) + 1 / 2 * np.cos(angle) * self._acceleration
        distance_y = self._velocity * np.sin(angle) + 1 / 2 * (-scipy.constants.g + np.sin(angle) * self._acceleration)

        self._point[0] += distance_x
        self._point[1] += distance_y

        for i in range(len(self._polygon)):
            self._polygon[i][0] += distance_x
            self._polygon[i][1] += distance_y

        return np.sqrt(distance_y ** 2 + distance_x ** 2)

    def gat_traveled_distance(self):
        distance = self._calculate_current_velocity()
        return distance
