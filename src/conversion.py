# Conversion Module


import numpy as np
import data as data
import math as math


def conversion(mask_id, n_horizontal, m_vertical, datastruct):
    """Convert the Moire 3D array into the Crystal 2D array and store it in datastruct.
    The Moire 3D array is loaded from the data structure (datastruct) using the keyword (mask_id = string).
    The horizontal and vertical component of the Moire 3D array are separated and each component are converted using
    the integer n_horizontal and m_vertical and the pixel size (strictly positive real number loaded from datastuct)."""

    # Load the pixel size (p) from the data structure and check if p is strictly positive
    p = data.SMGData.load(datastruct, 'p')
    if p <= 0:
        raise Exception('Pixel size negative or zero, conversion cannot be performed')

    # Normalize the unstrained reference Moire 3D array (gMuns = 3D array -- 2D vector on each pixel of a
    # 2D image and separate components)
    g_m_uns = data.SMGData.load_g(datastruct, mask_id, 'gMuns')

    # Generate the correction 3D array to apply on the unstrained reference Moire 3D array on each component
    correction = np.ones(g_m_uns.shape)
    # Warning g[0] component along x (vertical axis pointing down)
    correction[0, :, :] = - m_vertical * correction[0, :, :]
    # Warning g[1] component along y (horizontal axis pointing right)
    correction[1, :, :] = n_horizontal * correction[1, :, :]

    # Apply correction to get the unstrained reference crystalline 3D array and store it in the data structure
    g_c_uns = g_m_uns + correction
    data.SMGData.store_g(datastruct, mask_id, 'gCuns', g_c_uns)

    # Inform user of the completion of the conversion and provide the norm of the crystalline wave vector
    norm = 1 / p * math.sqrt(g_c_uns[0, 0, 0] ** 2 + g_c_uns[1, 0, 0] ** 2)
    print('Conversion done !!')
    print('g norm = ', norm, ' nm-1')
