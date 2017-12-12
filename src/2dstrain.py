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

    g_ref = np.array([[g_c_uns_1[1, :, :], g_c_uns_2[1, :, :]],
                      [(-1) * g_c_uns_1[0, :, :], (-1) * g_c_uns_2[0, :, :]]])
    delta_g = np.array([[delta_g_1[1, :, :], delta_g_2[1, :, :]],
                        [(-1) *delta_g_1[0, :, :], (-1) * delta_g_2[0, :, :]]])

    print(g_ref.shape)
    print(delta_g.shape)

    g = np.add(g_ref, delta_g)