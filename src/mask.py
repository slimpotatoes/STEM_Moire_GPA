# Mask Module


import numpy as np


def mask_classic(center, r, shape):
    """Return the mask function in the image space I defined by shape (see MIS). The classic mask takes the center of a
    circle center = (xc,yc) and its radius r and put 1 if the image space is inside the circle and 0 outside. In
    addition, the center of the mask is used to return g_0 that correspond to a first estimation of the unstrained
    reference."""
    """Do not forget event coordinate (x,y) from matplotlib should be switched compared to numpy array indexing"""
    g_0 = np.array([(center[1] - 0.5 * shape[0]) / shape[0] * np.ones(shape),
                    (center[0] - 0.5 * shape[1]) / shape[1] * np.ones(shape)])
    mask = np.ndarray(shape=shape)
    """Do not forget event coordinate (x,y) from matplotlib  should be switched compared to numpy array indexing"""
    for i in range(0, shape[1]):
        for j in range(0, shape[0]):
            if ((i - center[1]) ** 2 + (j - center[0]) ** 2) < (r ** 2):
                mask[i, j] = 1
            else:
                mask[i, j] = 0
    return mask, g_0


def mask_gaussian(center, r, shape):
    """Return the mask function in the image space I defined by shape (see MIS). The Gaussian mask takes the center of a
        circle center = (xc,yc) and its radius r to generate a 2D gaussian function centered around the circle. In
        addition, the center of the mask is used to return g_0 that correspond to the unstrained reference."""
    """Do not forget event coordinate (x,y) from matplotlib  should be switched compared to numpy array indexing"""
    g_0 = np.array([(center[1] - 0.5 * shape[0]) / shape[0] * np.ones(shape),
                    (center[0] - 0.5 * shape[1]) / shape[1] * np.ones(shape)])
    """Do not forget event coordinate (x,y) from matplotlib  should be switched compared to numpy array indexing"""
    const = 1 / (2 * (2 / 3 * r) ** 2)
    mesh_x, mesh_y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
    delta_x = (mesh_x - center[0]) ** 2
    delta_y = (mesh_y - center[1]) ** 2
    mask = np.exp(-(delta_x + delta_y) * const)
    return mask, g_0
