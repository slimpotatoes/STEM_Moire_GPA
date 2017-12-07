# STEM Moire hologram simulation module
import numpy as np
import data as data
import math as math
from scipy.ndimage.interpolation import shift


def smh_sim(datastruct):
    """Simulate the Fourier transform of the STEM Moire hologram based on the reference image"""
    """Make the Fourier transform of the STEM Moire hologram and store it"""
    data.SMGData.store(datastruct, 'FTISMHexp', np.fft.fft2(data.SMGData.load(datastruct, 'ISMHexp')))
    """Load the intermediate variables from the reference image to make the simulation"""
    ft_ic = np.fft.fftshift(np.abs(np.fft.fft2(data.SMGData.load(datastruct, 'ICref')) ** 2))
    p = data.SMGData.load(datastruct, 'p')
    pref = data.SMGData.load(datastruct, 'pref')
    n_lim = math.floor(p/(2*pref))
    fov = ft_ic.shape[0]
    tile = int(pref / p * fov)
    ft_ismh_sim = np.ndarray(ft_ic.shape)
    ft_ic_square = np.ndarray((len(range(-n_lim, n_lim+1)), len(range(-n_lim, n_lim+1)), int(tile), int(tile)))
    """Simulation by calculating the STEM Moire hologram equation"""
    print('Please wait the calculation can take some time !!!')
    for i in range(-n_lim, n_lim+1):
        for j in range(-n_lim, n_lim+1):
            ft_ismh_sim += shift(ft_ic, [i*tile, j*tile], cval=0, order=0, prefilter=False)
            a = int(0.5 * (fov - tile) + i * tile)
            b = int(0.5 * (fov + tile) + i * tile)
            c = int(0.5 * (fov - tile) + j * tile)
            d = int(0.5 * (fov + tile) + j * tile)
            ft_ic_square[i+n_lim][j+n_lim] = ft_ic[a:b, c:d]
    print('Simulation done')
    '''Storing data into data structure'''
    data.SMGData.store(datastruct, 'FTISMHsim', ft_ismh_sim[
                        int(0.5*(ft_ismh_sim.shape[0] - tile)):int(0.5*(ft_ismh_sim.shape[0] + tile)),
                        int(0.5*(ft_ismh_sim.shape[0] - tile)):int(0.5*(ft_ismh_sim.shape[0] + tile))])
    data.SMGData.store(datastruct, 'FTISMHsimDisplay', ft_ic_square)

