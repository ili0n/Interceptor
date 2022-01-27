import numpy as np


class Polygon(object):
    def __init__(self, vertices):
        self._vertices = vertices

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, val):
        self._vertices = val

    def perpendicular(self, i):
        i1 = i
        i2 = (i + 1) % len(self.vertices)
        dx = self.vertices[i2][0] - self.vertices[i1][0]
        dy = self.vertices[i2][1] - self.vertices[i1][1]
        return np.array([-dy, dx]), self.vertices[i]


# a, b - two polygons
def min_separation(a, b):
    separation = -np.inf
    for i in range(len(a.vertices)):
        normal, va = a.perpendicular(i)
        min_sep = np.inf
        for vb in b.vertices:
            projection = np.dot(vb - va, normal)
            min_sep = min(min_sep, projection)
        if min_sep > separation:
            separation = min_sep
    return separation


def is_colliding(a, b):
    return min_separation(a, b) <= 0


if __name__ == '__main__':
    a = Polygon(np.array([[1, 1], [1, 2], [2, 2], [2, 1]], dtype="f"))
    b = Polygon(np.array([[2, 1.5], [2, 1.75], [2.5, 1.75], [2.5, 1.5]], dtype="f"))
    print(is_colliding(a, b))

    a = Polygon(np.array([[1, 1], [1, 2], [2, 2], [2, 1]], dtype="f"))
    b = Polygon(np.array([[1, 1.5], [1, 1.75], [2.5, 1.75], [2.5, 1.5]], dtype="f"))
    print(is_colliding(a, b))
