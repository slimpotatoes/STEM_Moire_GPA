# GPA Module
import mask as mask
import data as data
import numpy as np
from skimage.restoration import unwrap_phase


def gpa(mask_id, datastruct):
    center = data.SMGData.load_g(datastruct, mask_id, 'Mask')[0]
    r = data.SMGData.load_g(datastruct, mask_id, 'Mask')[1]
    ft_ismh_exp = data.SMGData.load(datastruct, 'FTISMHexp')
    m, g_uns = mask.mask_gaussian(center, r, ft_ismh_exp.shape)
    data.SMGData.store_g(datastruct, mask_id, 'gMuns', g_uns)
    masked_ft_ismh_exp = np.multiply(m, np.fft.fftshift(ft_ismh_exp))
    phase_g_m = np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_ismh_exp)))
    g_m = [1 / (2 * np.pi) * np.gradient(unwrap_phase(phase_g_m))[0],
           1 / (2 * np.pi) * np.gradient(unwrap_phase(phase_g_m))[1]]
    delta_g_m = np.subtract(g_m, g_uns)
    mesh_x, mesh_y = np.meshgrid(np.arange(phase_g_m.shape[0]), np.arange(phase_g_m.shape[1]))
    unwrapped_phase_delta_g_m = unwrap_phase(phase_g_m) - 2 * np.pi * (
        np.multiply(g_uns[1][0], mesh_x) + np.multiply(g_uns[0][0], mesh_y))
    phase_delta_g_m = unwrapped_phase_delta_g_m - np.round(unwrapped_phase_delta_g_m / (2 * np.pi) * 2 * np.pi)
    data.SMGData.store_g(datastruct, mask_id, 'deltagM', delta_g_m)
    data.SMGData.store_g(datastruct, mask_id, 'phasegM', phase_delta_g_m)
