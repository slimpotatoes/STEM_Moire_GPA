# GPA Module
import mask as mask
import data as data
import numpy as np
from skimage.restoration import unwrap_phase


def gpa(mask_id, datastruct):
    """Pefrom GPA on the GUI id, mask_id using the data in datastructure:
            1. Load elements of GUI (center, radius) to create the mask
            2. Load the Fourier transform of the ISMHexp (element to mask)
            3. Create the mask in the image space
            4. Store the approximation of the unstrain reference as the center of the circle g_uns
            5. Mask the Fourier transform of ISMHexp
            6. Calculate the phase of the masked section of ISMHexp
            7. Calculate the g_M vector by taking the gradient of the phase
            8. Calculate the variation of the g_M vector as the difference of g_M and g_uns
            9. Calculate the phase corrected by removing the contribution of g_uns to be only related to delta_g
            10. Store delta_g and the phase related to delta_g"""

    # Load the elements
    center = data.SMGData.load_g(datastruct, mask_id, 'Mask')[0]
    r = data.SMGData.load_g(datastruct, mask_id, 'Mask')[1]
    ft_ismh_exp = data.SMGData.load(datastruct, 'FTISMHexp')

    # Generate the mask in the image space
    m, g_uns = mask.mask_gaussian(center, r, ft_ismh_exp.shape)
    #print('gpa, g_uns', g_uns.shape, g_uns)

    # Store the unstrain reference in the datastructure
    data.SMGData.store_g(datastruct, mask_id, 'gMuns', g_uns)

    # Mask and calculate the phase component
    masked_ft_ismh_exp = np.multiply(m, np.fft.fftshift(ft_ismh_exp))
    phase_g_m = np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_ismh_exp)))
    data.SMGData.store_g(datastruct, mask_id,'phaseraw', phase_g_m)

    # Calculate g_m and the variation of g_M
    g_m = np.array([1 / (2 * np.pi) * np.gradient(unwrap_phase(phase_g_m))[0],
                    1 / (2 * np.pi) * np.gradient(unwrap_phase(phase_g_m))[1]])
    #print('gpa, g_m', g_m.shape, g_m)
    delta_g_m = np.subtract(g_m, g_uns)

    # Calculate phase corrected by removing the contribution of g_uns to be only related to delta_g
    mesh_x, mesh_y = np.meshgrid(np.arange(phase_g_m.shape[0]), np.arange(phase_g_m.shape[1]))
    unwrapped_phase_delta_g_m = np.array(unwrap_phase(phase_g_m)) - 2 * np.pi * (
        np.multiply(g_uns[1], mesh_x) + np.multiply(g_uns[0], mesh_y))
    #print('gpa, unwrap_phase', unwrapped_phase_delta_g_m.shape, unwrapped_phase_delta_g_m)
    phase_delta_g_m = unwrapped_phase_delta_g_m - np.round(unwrapped_phase_delta_g_m / (2 * np.pi) * 2 * np.pi)
    #print('gpa, deltag', delta_g_m.shape, delta_g_m)
    #print('gpa, phaseg', phase_delta_g_m.shape, phase_delta_g_m)

    # Store the final data
    data.SMGData.store_g(datastruct, mask_id, 'deltagM', delta_g_m)
    data.SMGData.store_g(datastruct, mask_id, 'phasegM', phase_delta_g_m)
