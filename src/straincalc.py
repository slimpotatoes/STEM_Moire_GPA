# Strain calculation Module


import numpy as np
import data as data
import rotatecalc


def strain_calculation(mask_id_1, mask_id_2, datastruct):
    p = data.SMGData.load(datastruct, 'p')
    if p <= 0:
        raise Exception('Pixel size negative or zero, strain calculation cannot be performed')

    # Load the crystalline 3D arrays and their corresponding delta G 3D arrays and calibrate them with the pixel size p
    g_c_uns_1 = 1 / p * data.SMGData.load_g(datastruct, mask_id_1, 'gCuns')
    g_c_uns_2 = 1 / p * data.SMGData.load_g(datastruct, mask_id_2, 'gCuns')
    delta_g_1 = 1 / p * data.SMGData.load_g(datastruct, mask_id_1, 'deltagM')
    delta_g_2 = 1 / p * data.SMGData.load_g(datastruct, mask_id_2, 'deltagM')

    identity = np.ones(delta_g_1[0, :, :].shape)
    identity_image = np.array([[identity, np.zeros(identity.shape)], [np.zeros(identity.shape), identity]])

    # Raw data
    '''g_ref = np.array([[g_c_uns_1[0, :, :], g_c_uns_2[0, :, :]],
                      [g_c_uns_1[1, :, :], g_c_uns_2[1, :, :]]])
    delta_g = np.array([[delta_g_1[0, :, :], delta_g_2[0, :, :]],
                        [delta_g_1[1, :, :], delta_g_2[1, :, :]]])'''

    # Data rotated by 90 degrees R = ([0, -1],[1. 0])
    '''g_ref = np.array([[g_c_uns_2[0, :, :], (-1) * g_c_uns_1[0, :, :]],
                      [g_c_uns_2[1, :, :], (-1) * g_c_uns_1[1, :, :]]])
    delta_g = np.array([[delta_g_2[0, :, :], (-1) * delta_g_1[0, :, :]],
                        [delta_g_2[1, :, :], (-1) * delta_g_1[1, :, :]]])'''

    # Data rotated by 90 degrees R = ([0, 1],[-1. 0]) --- Base rotation not vector rotation
    '''g_ref = np.array([[(-1) * g_c_uns_2[0, :, :], g_c_uns_1[0, :, :]],
                      [(-1) * g_c_uns_2[1, :, :], g_c_uns_1[1, :, :]]])
    delta_g = np.array([[(-1) * delta_g_2[0, :, :], delta_g_1[0, :, :]],
                        [(-1) * delta_g_2[1, :, :], delta_g_1[1, :, :]]])'''

    # Raw data adapted to base rotation (90 degree CCW)
    g_ref = np.array([[(-1) * g_c_uns_1[1, :, :], (-1) * g_c_uns_2[1, :, :]],
                      [g_c_uns_1[0, :, :], g_c_uns_2[0, :, :]]])
    delta_g = np.array([[(-1) * delta_g_1[1, :, :], (-1) * delta_g_2[1, :, :]],
                        [delta_g_1[0, :, :], delta_g_2[0, :, :]]])

    g = np.add(g_ref, delta_g)

    t_g_ref_pixel = np.transpose(np.transpose(g_ref, axes=[2, 3, 0, 1]), axes=[0, 1, 3, 2])
    t_g_pixel = np.transpose(np.transpose(g, axes=[2, 3, 0, 1]), axes=[0, 1, 3, 2])
    identity_pixel = np.transpose(identity_image, axes=[2, 3, 0, 1])

    # Store intermediate values because of memory ?? LOL
    inv_t_g_pixel = np.linalg.inv(t_g_pixel)
    displacement = np.zeros(t_g_pixel.shape)

    for i in range(0, t_g_ref_pixel[:, :, 0, 0].shape[0]):
        for j in range(0, t_g_ref_pixel[:, :, 0, 0].shape[1]):
            displacement[i, j] = np.dot(inv_t_g_pixel[i, j], t_g_ref_pixel[i, j])

    # Calculate gradient deformation tensor nabla(u)
    d = np.subtract(displacement, identity_pixel)

    # Calculate strain tensor
    epsilon = 0.5 * np.array(np.add(d, np.transpose(d, axes=[0, 1, 3, 2])))
    omega = 0.5 * np.array(np.subtract(d, np.transpose(d, axes=[0, 1, 3, 2])))

    # Put them in image format and store
    epsilon_image = np.transpose(epsilon, axes=[2, 3, 0, 1])
    omega_image = np.transpose(omega, axes=[2, 3, 0, 1])
    data.SMGData.store(datastruct, 'Exx', epsilon_image[0, 0])
    data.SMGData.store(datastruct, 'Eyy', epsilon_image[1, 1])
    data.SMGData.store(datastruct, 'Exy', epsilon_image[1, 0])
    data.SMGData.store(datastruct, 'Rxy', omega_image[1, 0])
    print('2D strain calculation done !')
