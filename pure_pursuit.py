import numpy as np
from matplotlib import pyplot as plt


def find_goal_point(my_point,enemy_points):
    potential_points = {}
    for i in range(len(my_point)):
        potential_points[abs(np.sqrt((enemy_points[i][0] - my_point[0]) ** 2 +
                                     (enemy_points[i][1] - my_point[1]) ** 2))] = enemy_points[i]

    value = potential_points[min(potential_points.keys())]
    return value


def calculate_new_position(goal_point, current_point, distance):
    leveled_current_point = np.array([current_point[0], 0])
    leveled_goal_point = np.array([goal_point[0], goal_point[1] - current_point[1]])

    if leveled_goal_point[1] == 0:
        if leveled_goal_point[0] >= leveled_current_point[0]:
            new_x = np.array(current_point[0] + distance)
        else:
            new_x = np.array(current_point[0] - distance)

        return np.array([new_x, current_point[1]])

    if leveled_goal_point[0] == leveled_current_point[0]:
        if leveled_goal_point[1] > 0:
            new_y = np.array(current_point[1] + distance)
        else:
            new_y = np.array(current_point[1] - distance)

        return np.array([current_point[0], new_y])

    l_squared = (goal_point[0] - current_point[0]) ** 2 + (goal_point[1] - current_point[1]) ** 2
    r = abs(l_squared / (2 * leveled_goal_point[1]))

    if leveled_goal_point[0] < leveled_current_point[0]:
        center_point = np.array([leveled_current_point[0] - r, 0])
    else:
        center_point = np.array([leveled_current_point[0] + r, 0])

    arch = distance
    angle = arch / r

    distance_current = np.sqrt(r ** 2 + r ** 2 - 2 * r * r * np.cos(angle))

    # print(distance_current**2)
    # print(r ** 2)
    # print(leveled_current_point[0] ** 2)
    # print(center_point[0] ** 2)
    # print()

    new_x = (distance_current ** 2 - r ** 2 - leveled_current_point[0] ** 2 + center_point[0] ** 2) \
            / (2 * (center_point[0] - leveled_current_point[0]))

    if new_x < current_point[0]:
        a = 1

    if leveled_goal_point[1] < 0:
        new_y = -np.sqrt(distance_current ** 2 - (new_x - leveled_current_point[0]) ** 2) + current_point[1]
    else:
        new_y = np.sqrt(distance_current ** 2 - (new_x - leveled_current_point[0]) ** 2) + current_point[1]

    return np.array([new_x, new_y])


def main_loop():
    func = lambda x: -(x + 1) ** 2
    current_point = np.array([0, 0])
    x = 0

    goal = find_goal_point(current_point, [np.array([np.inf,np.inf]), np.array([x,func(x)])])
    print(goal)
    print(current_point)
    for i in range(100):
        goal = find_goal_point(current_point, [np.array([np.inf,np.inf]), np.array([x,func(x)])])
        print("G:", end=" ")
        print(goal)
        current_point = calculate_new_position(goal, current_point, 0.5)
        print(current_point)
        plt.scatter(current_point[0], current_point[1], c="blue")
        plt.scatter(goal[0], goal[1], c="red")
        x += 0.07

    plt.show()



if __name__ == '__main__':
    main_loop()
