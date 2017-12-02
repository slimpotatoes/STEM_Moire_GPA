import numpy as np
import data as data
import math as math
from scipy.ndimage.interpolation import shift


class SMHSim(object):

    def __init__(self):
        self.FTIc = None
        self.FTISMHsim = None

    def smh_sim(self, datastruct):
        data.SMGData.store(datastruct, 'FTISMHexp', np.fft.fft2(data.SMGData.load(datastruct, 'ISMHexp')))
        self.FTIc = np.fft.fftshift(np.abs(np.fft.fft2(data.SMGData.load(datastruct, 'ICref')) ** 2))
        p = data.SMGData.load(datastruct, 'p')
        pref = data.SMGData.load(datastruct, 'pref')
        n_lim = math.floor(p/(2*pref))
        tile = pref / p * self.FTIc.shape[0]
        self.FTISMHsim = np.ndarray(self.FTIc.shape)
        print('Please wait this step can take some time')
        for i in range(-n_lim, n_lim+1):
            for j in range(-n_lim, n_lim+1):
                self.FTISMHsim += shift(self.FTIc, [i*tile, j*tile], cval=0, order=0, prefilter=False)
        data.SMGData.store(datastruct, 'FTISMHsim', self.FTISMHsim[
                           int(0.5*(self.FTISMHsim.shape[0] - tile)):int(0.5*(self.FTISMHsim.shape[0] + tile)),
                           int(0.5*(self.FTISMHsim.shape[0] - tile)):int(0.5*(self.FTISMHsim.shape[0] + tile))])
        print('Simulation done')
