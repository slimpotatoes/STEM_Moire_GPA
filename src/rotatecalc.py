import numpy as np
import math
import data


def angle_rotation(gui):
    first_position = [gui.line_rot.LineCoords[0][1], gui.line_rot.LineCoords[0][0]]
    second_position = [gui.line_rot.LineCoords[1][1], gui.line_rot.LineCoords[1][0]]

    print('first position = ', first_position)
    print('second position = ', second_position)

    first_point = [first_position[1], -first_position[0]]
    second_point = [second_position[1], -second_position[0]]

    print('first point = ', first_point)
    print('second point = ', second_point)

    # x1 = math.sqrt((second_point[0] - first_point[0]) ** 2)
    # x2 = math.sqrt((second_point[1] - first_point[1]) ** 2)

    norm = math.sqrt((second_point[0] - first_point[0]) ** 2 + (second_point[1] - first_point[1]) ** 2)

    horizontal_proj = (second_point[0] - first_point[0]) / norm
    vertical_proj = (second_point[1] - first_point[1]) / norm

    if vertical_proj >= 0:
        theta = np.arccos(horizontal_proj)
    else:
        theta = - np.arccos(horizontal_proj)

    print('theta = ', theta)
    return theta


def rotate_tensor(datastruct, gui):
    theta = angle_rotation(gui)

    exx = data.SMGData.load(datastruct, 'Exx')
    eyy = data.SMGData.load(datastruct, 'Eyy')
    exy = data.SMGData.load(datastruct, 'Exy')
    rxy = data.SMGData.load(datastruct, 'Rxy')

    epsilon = np.array([[exx, exy], [exy, eyy]])
    omega = np.array([[np.zeros(rxy.shape), rxy], [-rxy, np.zeros(rxy.shape)]])
    r = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])

    epsilon = np.transpose(epsilon, axes=[2, 3, 0, 1])
    omega = np.transpose(omega, axes=[2, 3, 0, 1])

    for i in range(0, epsilon[:, :, 0, 0].shape[0]):
        for j in range(0, epsilon[:, :, 0, 0].shape[1]):
            epsilon[i, j] = np.dot(np.transpose(r), np.dot(epsilon[i, j], r))
            omega[i, j] = np.dot(np.transpose(r), np.dot(omega[i, j], r))

    epsilon = np.transpose(epsilon, axes=[2, 3, 0, 1])
    omega = np.transpose(omega, axes=[2, 3, 0, 1])

    data.SMGData.store(datastruct, 'Exx', epsilon[0, 0])
    data.SMGData.store(datastruct, 'Eyy', epsilon[1, 1])
    data.SMGData.store(datastruct, 'Exy', epsilon[1, 0])
    data.SMGData.store(datastruct, 'Rxy', omega[1, 0])

