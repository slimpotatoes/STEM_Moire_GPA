# Strain calculation Module
import numpy as np
import data as data

def strain_calculation(mask_id_1, mask_id_2, datastruct):
    p = data.SMGData.load(datastruct, 'p')
    g_c_uns_1 = data.SMGData.load_g(datastruct, mask_id_1, 'gCuns')
    delta_g_1 = data.SMGData.load_g(datastruct, mask_id_1, 'deltagM')
    g_c_uns_2 = data.SMGData.load_g(datastruct, mask_id_2, 'gCuns')
    delta_g_2 = data.SMGData.load_g(datastruct, mask_id_2, 'deltagM')

    delta_g_1[0, :, :] = 1 / p * delta_g_1[0, :, :]
    delta_g_1[1, :, :] = 1 / p * delta_g_1[1, :, :]

    delta_g_2[0, :, :] = 1 / p * delta_g_2[0, :, :]
    delta_g_2[1, :, :] = 1 / p * delta_g_2[1, :, :]

    identity = np.ones(delta_g_1.shape)
    identity_image = np.array([[identity, np.zeros(identity.shape)], [np.zeros(identity.shape), identity]])

    # Raw data
    '''g_ref = np.array([[g_c_uns_1[0, :, :], g_c_uns_2[0, :, :]],
                      [g_c_uns_1[1, :, :], g_c_uns_2[1, :, :]]])
    delta_g = np.array([[delta_g_1[0, :, :], delta_g_2[0, :, :]],
                        [delta_g_1[0, :, :], delta_g_2[0, :, :]]])'''

    # Data rotated by 90 degrees R = ([0, -1],[1. 0])
    g_ref = np.array([[g_c_uns_2[0, :, :], (-1) * g_c_uns_1[0, :, :]],
                      [g_c_uns_2[1, :, :], (-1) * g_c_uns_1[1, :, :]]])
    delta_g = np.array([[delta_g_2[0, :, :], (-1) * delta_g_1[0, :, :]],
                        [delta_g_2[1, :, :], (-1) * delta_g_1[1, :, :]]])


    print(g_ref.shape)
    print(delta_g.shape)

    g = np.add(g_ref, delta_g)

    g_ref_pixel = np.transpose(g_ref, axes=[2, 3, 1, 0])
    g_pixel = np.transpose(g, axes=[2, 3, 1, 0])
    identity_pixel = np.transpose(identity_image, axes=[2, 3, 1, 0])

    print(g_ref_pixel.shape)
    print(g.shape)
    print(g_ref[0, 0])
    print(g[0, 0])

    # Calculate gradient deformation tensor nabla(u)
    D = np.subtract(np.dot(np.linalg.inv(np.transpose(g_pixel, axes=[0, 1, 3, 2])), np.transpose(g_ref_pixel, axes=[0, 1, 3, 2])), identity_pixel)

    # Calculate strain tensor
    epsilon = 0.5 * np.add(D, np.transpose(D, axes=[0, 1, 3, 2]))
    omega = np.array([0.5 * np.subtract(D, np.transpose(D, axes=[0, 1, 3, 2]))])

    # Put them in image format and store
    epsilon_image = np.transpose(epsilon, axes=[2, 3, 0, 1])
    omega_image = np.transpose(omega, axes=[2, 3, 0, 1])
    data.SMGData.store(datastruct, 'Exx', epsilon_image[0, 0])
    data.SMGData.store(datastruct, 'Eyy', epsilon_image[1, 1])
    data.SMGData.store(datastruct, 'Exy', epsilon_image[1, 0])
    data.SMGData.store(datastruct, 'Rxy', omega_image[1, 0])
