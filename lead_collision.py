import numpy as np
import matplotlib.pyplot as plt

"""
    vector of position is described with equation
    r = a + tb
    a is dot, b is vector of direction
    circle equation in vector shape
    (r - c)(r - c) = radius**2
    c is vector of position of center
"""


def find_vector_circle_intersection(a, b, c, radius):
    # we form quadratic equation coefficients
    aq = np.linalg.norm(b) ** 2
    bq = np.dot(2 * (a - c), b)
    cq = np.linalg.norm(a - c) ** 2 - radius**2

    t1 = (-bq - np.sqrt(bq**2 - 4 * aq * cq)) / (2 * aq)
    t2 = (-bq + np.sqrt(bq**2 - 4 * aq * cq)) / (2 * aq)

    r1 = a + b * t1
    r2 = a + b * t2
    return r1, r2


""" 
    vl is leading projectile velocity
    rl is leading projectile position
    vt is target projectile velocity
    rt is target projectile position
"""


def lead_collision(vl, rl, vt, rt):
    # we find closer intersection
    r1, r2 = find_vector_circle_intersection(rl, rt - rl, rt + vt, np.dot(vt, vt))
    dist1 = np.linalg.norm(r1)
    dist2 = np.linalg.norm(r2)
    if dist1 > dist2:
        intersection = dist2
    else:
        intersection = dist1
    # lead direction is from intersection to center of circle
    lead_direction = (rt + vt) - intersection
    # with Thales theorem we find how long the vector should be
    ratio = np.linalg.norm(rt - rl) / (intersection - rl)
    result_vector = ratio * lead_direction
    return result_vector


def line(dot1, dot2):
    x = np.linspace(dot1[0], dot2[0])
    y = (dot2[1] - dot1[1]) / (dot2[0] - dot1[0]) * (x - dot1[0]) + dot1[1]
    return x, y


if __name__ == '__main__':
    rl = np.array([1, 1])
    vl = np.array([2, 2])
    rt = np.array([5, 6])
    vt = np.array([2, -1])
    plt.scatter(rl[0], rl[1])
    plt.scatter(vl[0], vl[1], c="black")
    plt.scatter(rt[0], rt[1])
    plt.scatter(vt[0], vt[1], c="black")
    plt.scatter((rt + vt)[0], (rt + vt)[1], c="yellow")
    x, y = line(rl, rt)
    plt.plot(x, y)

    x, y = line(rt, rt + vt)
    plt.plot(x, y)

    circle1 = plt.Circle(rt + vt, np.linalg.norm(vl), color='r', fill=False)
    plt.gca().add_patch(circle1)

    r1, r2 = find_vector_circle_intersection(rl, rt - rl, rt + vt, np.linalg.norm(vl))
    plt.scatter(r1[0], r1[1], c="green")
    plt.scatter(r2[0], r2[1], c="green")

    result = lead_collision(vl, rl, vt, rt)
    x, y = line(rl, rl + result)
    plt.plot(x, y)
    plt.show()


