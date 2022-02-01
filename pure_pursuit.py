import numpy as np
from matplotlib import pyplot as plt


def find_goal_point(my_point, enemy_points, look_ahead=0):
    min_x =1500
    max_x = 0
    min_y = 1500
    max_y = 0

    for i in enemy_points:
        if i[0] > max_x:
            max_x = i[0]
        if i[0] < min_x:
            min_x = i[0]
        if i[1] > max_y:
            max_y = i[1]
        if i[1] < min_y:
            min_y = i[1]

    generated_points = []

    for i in range(min_x,max_x):
        generated_points.append(np.array([i,min_y]))
        generated_points.append(np.array([i, max_y]))

    for i in range(min_y,max_y):
        generated_points.append(np.array([min_x,i]))
        generated_points.append(np.array([max_x, i]))

    potential_points = {}

    for i in generated_points:
        potential_points[abs(np.sqrt((i[0] - my_point[0]) ** 2 +
                                     (i[1] - my_point[1]) ** 2) - look_ahead)] = i

    value = potential_points[min(potential_points.keys())]
    return value


def calculate_angle(goal_point, current_point):
    leveled_current_point = np.array([current_point[0], 0])
    leveled_goal_point = np.array([goal_point[0], goal_point[1] - current_point[1]])

    if leveled_goal_point[1] == 0.0:
        # if leveled_goal_point[0] >= leveled_current_point[0]:
        #     new_x = np.array(current_point[0] + distance)
        # else:
        #     new_x = np.array(current_point[0] - distance)
        if current_point[0] - goal_point[0] > 0:
            return 3 * np.pi / 2
        else:
            return np.pi / 2


    if leveled_goal_point[0] == leveled_current_point[0]:
        # if leveled_goal_point[1] > 0:
        #     new_y = np.array(current_point[1] + distance)
        # else:
        #     new_y = np.array(current_point[1] - distance)
        if current_point[0] - goal_point[0] > 0:
            return np.pi
        else:
            return 0

    l_squared = (goal_point[0] - current_point[0]) ** 2 + (goal_point[1] - current_point[1]) ** 2
    r = l_squared / (2 * leveled_goal_point[1])

    # if leveled_goal_point[0] < leveled_current_point[0]:
    #     center_point = np.array([leveled_current_point[0] - r, 0])
    # else:
    #     center_point = np.array([leveled_current_point[0] + r, 0])
    angle = np.arctan(np.sqrt(l_squared) / r)
    if current_point[0] - goal_point[0] > 0:
        angle -= np.pi
        angle *= -1

    # distance_current = np.sqrt(r ** 2 + r ** 2 - 2 * r * r * np.cos(angle))
    #
    # # print(distance_current**2)
    # # print(r ** 2)
    # # print(leveled_current_point[0] ** 2)
    # # print(center_point[0] ** 2)
    # # print()
    #
    # new_x = (distance_current ** 2 - r ** 2 - leveled_current_point[0] ** 2 + center_point[0] ** 2) / \
    #         (2 * (center_point[0] - leveled_current_point[0]))
    #
    # if new_x < current_point[0]:
    #     a = 1
    #
    # if leveled_goal_point[1] < 0:
    #     new_y = -np.sqrt(distance_current ** 2 - (new_x - leveled_current_point[0]) ** 2) + current_point[1]
    # else:
    #     new_y = np.sqrt(distance_current ** 2 - (new_x - leveled_current_point[0]) ** 2) + current_point[1]
    # print(angle)
    return angle


def main_loop():
    func = lambda x: -(x + 1) ** 2
    current_point = np.array([0, 0])
    x = 0

    goal = find_goal_point(current_point, [np.array([np.inf, np.inf]), np.array([x, func(x)])])
    print(goal)
    print(current_point)
    for i in range(100):
        goal = find_goal_point(current_point, [np.array([np.inf, np.inf]), np.array([x, func(x)])])
        print("G:", end=" ")
        print(goal)
        # current_point = calculate_new_position(goal, current_point, 0.5)
        print(current_point)
        plt.scatter(current_point[0], current_point[1], c="blue")
        plt.scatter(goal[0], goal[1], c="red")
        x += 0.07

    plt.show()


if __name__ == '__main__':
    main_loop()
