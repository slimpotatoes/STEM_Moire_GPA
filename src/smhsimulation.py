# STEM Moire hologram simulation module


import numpy as np
import data as data
import math as math
from scipy.ndimage.interpolation import shift


def smh_sim(datastruct):
    """Simulate the Fourier transform of the STEM Moire hologram based on the reference image"""

    # Make the Fourier transform of the STEM Moire hologram and store it.
    data.SMGData.store(datastruct, 'FTISMHexp', np.fft.fft2(data.SMGData.load(datastruct, 'ISMHexp')))

    # Load the intermediate variables from the reference image to make the simulation.
    ft_ic = np.fft.fftshift(np.abs(np.fft.fft2(data.SMGData.load(datastruct, 'ICref')) ** 2))
    p = data.SMGData.load(datastruct, 'p')
    pref = data.SMGData.load(datastruct, 'pref')
    n_lim = int(math.floor(p/pref))
    fov = ft_ic.shape[0]
    tile = int(pref / p * fov)
    ft_ismh_sim = np.ndarray(ft_ic.shape)

    # Simulation by calculating the STEM Moire hologram equation.
    counter = 0
    if n_lim % 2 != 0:
        initial_coordinate = (int(0.5 * (fov - n_lim * tile)), int(0.5 * (fov - n_lim * tile)))
        ft_ic_square = np.ndarray((len(range(0, n_lim)), len(range(0, n_lim)), tile, tile))

    else:
        n_lim -= 1
        initial_coordinate = (int(0.5 * (fov - n_lim * tile)), int(0.5 * (fov - n_lim * tile)))
        ft_ic_square = np.ndarray((len(range(0, n_lim)), len(range(0, n_lim)), tile, tile))

    # Print statement to inform user
    print('Shape in pixel of reference: ', ft_ismh_sim.shape)
    print('Shape in pixel of the tile: ', ft_ic_square.shape)
    print('Tile size (in pixel): ', tile)
    print('Number of tiles: ', n_lim ** 2)
    print('Please wait the calculation can take some time !!!')

    for i in range(0, n_lim):
        for j in range(0, n_lim):
            ft_ismh_sim += shift(ft_ic, [int(i - 0.5 * n_lim) * tile, int(j - 0.5 * n_lim) * tile],
                                 cval=0, order=0, prefilter=False)
            a = int(initial_coordinate[0] + i * tile)
            b = a + tile
            c = int(initial_coordinate[0] + j * tile)
            d = c + tile
            ft_ic_square[i][j] = ft_ic[a:b, c:d]
            counter += 1
            # print('Loop number: ', counter)

    print('Simulation done')

    # Storing data into data structure.
    data.SMGData.store(datastruct, 'FTISMHsim', ft_ismh_sim[
                        int(0.5*(ft_ismh_sim.shape[0] - tile)):int(0.5*(ft_ismh_sim.shape[0] + tile)),
                        int(0.5*(ft_ismh_sim.shape[0] - tile)):int(0.5*(ft_ismh_sim.shape[0] + tile))])
    data.SMGData.store(datastruct, 'FTISMHsimDisplay', ft_ic_square)
