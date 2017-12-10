# Mask Module
import numpy as np


def mask_classic(center, r, shape):
    """Do not forget event coordinate (x,y) should be switched compared to array indexing"""
    g_0 = [(center[1] - 0.5 * shape[0]) / shape[0] * np.ones(shape),
           (center[0] - 0.5 * shape[1]) / shape[1] * np.ones(shape)]
    mask = np.ndarray(shape=shape)
    """Do not forget event coordinate (x,y) should be switched compared to array indexing"""
    for i in range(0, shape[1]):
        for j in range(0, shape[0]):
            if ((i - center[1]) ** 2 + (j - center[0]) ** 2) < (r ** 2):
                mask[i, j] = 1
            else:
                mask[i, j] = 0
    return mask, g_0


def mask_gaussian(center, r, shape):
    """Do not forget event coordinate (x,y) should be switched compared to array indexing"""
    g_0 = [(center[1] - 0.5 * shape[0]) / shape[0] * np.ones(shape),
           (center[0] - 0.5 * shape[1]) / shape[1] * np.ones(shape)]
    """Do not forget event coordinate (x,y) should be switched compared to array indexing"""
    const = 1 / (2 * (2 / 3 * r) ** 2)
    mesh_x, mesh_y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
    delta_x = (mesh_x - center[0]) ** 2
    delta_y = (mesh_y - center[1]) ** 2
    mask = np.exp(-(delta_x + delta_y) * const)
    return mask, g_0
