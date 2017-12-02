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
        fov = self.FTIc.shape[0]
        tile = int(pref / p * fov)
        self.FTISMHsim = np.ndarray(self.FTIc.shape)
        FTIc_square = np.ndarray((len(range(-n_lim, n_lim+1)),len(range(-n_lim, n_lim+1)),int(tile),int(tile)))
        print(FTIc_square.shape)
        print('Please wait this step can take some time')
        for i in range(-n_lim, n_lim+1):
            for j in range(-n_lim, n_lim+1):
                self.FTISMHsim += shift(self.FTIc, [i*tile, j*tile], cval=0, order=0, prefilter=False)
                a = int(0.5 * (fov - tile) + i * tile)
                b = int(0.5 * (fov + tile) + i * tile)
                c = int(0.5 * (fov - tile) + j * tile)
                d = int(0.5 * (fov + tile) + j * tile)
                print(a,b)
                print(c,d)
                FTIc_square[i+n_lim][j+n_lim] = self.FTIc[a : b , c : d]
        data.SMGData.store(datastruct, 'FTISMHsim', self.FTISMHsim[
                           int(0.5*(self.FTISMHsim.shape[0] - tile)):int(0.5*(self.FTISMHsim.shape[0] + tile)),
                           int(0.5*(self.FTISMHsim.shape[0] - tile)):int(0.5*(self.FTISMHsim.shape[0] + tile))])
        data.SMGData.store(datastruct, 'FTISMHsimDisplay', FTIc_square)
        print('Simulation done')
