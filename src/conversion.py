import numpy as np
import data as data
import math as math


def conversion(mask_id, n, m, datastruct):
    p = data.SMGData.load(datastruct, 'p')
    g_m_uns = data.SMGData.load_g(datastruct, mask_id, 'gMuns')
    print('g M ref avant calib')
    print(g_m_uns)
    g_m_uns[0, :, :] = 1 / p * g_m_uns[0, :, :]
    g_m_uns[1, :, :] = 1 / p * g_m_uns[1, :, :]
    print('g M ref apres calib')
    print(g_m_uns)
    correction = np.ones(g_m_uns.shape)
    correction[0, :, :] = - m / p * correction[0, :, :]
    correction[1, :, :] = n / p * correction[1, :, :]
    print('correction')
    print(correction)
    g_c_uns = g_m_uns + correction
    data.SMGData.store_g(datastruct, mask_id, 'gCuns', g_c_uns)
    norm = math.sqrt(g_c_uns[0, 0, 0] ** 2 + g_c_uns[1, 0, 0] ** 2)
    print('Conversion done !!')
    print('g norm = ', norm, ' nm-1')
