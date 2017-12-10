# Unstrain reference
import data as data
import numpy as np
from scipy.optimize import leastsq
from skimage.restoration import unwrap_phase

def update_zerostrain(mask_id, datastruct):

    '''def residuals(delta_g_model, delta_g_exp):
        delta_g_model_x, delta_g_model_y = delta_g_model
        d_g_x = delta_g_model_x * np.ones((delta_g_exp.shape[0], delta_g_exp.shape[1]))
        d_g_y = delta_g_model_y * np.ones((delta_g_exp.shape[1], delta_g_exp.shape[2]))
        d_g = np.array([d_g_x, d_g_y])
        err =  delta_g_exp - d_g
        print(err)
        print(err.shape)
        return err'''

    def residuals(delta_g_model, delta_g_exp):
        d_g = delta_g_model * np.ones((delta_g_exp.shape[0], delta_g_exp.shape[1]))
        err = delta_g_exp - d_g
        print('residual')
        print(err)
        print(err.shape)
        return err.flatten()

    # Load data needed
    u = data.SMGData.load(datastruct, 'Uref')
    print('Dand unstrainref')
    print(u)
    delta_g_m = data.SMGData.load_g(datastruct, mask_id, 'deltagM')
    g_uns = data.SMGData.load_g(datastruct, mask_id, 'gMuns')
    phase = data.SMGData.load_g(datastruct, mask_id, 'phasegM')

    # Build 3D array
    delta_g_m_exp = np.array([delta_g_m[0], delta_g_m[1]])
    g_uns_exp = np.array([g_uns[0], g_uns[1]])

    # Restrain on U
    delta_g_m_exp_u = delta_g_m_exp[:, u[0]:u[1], u[2]:u[3]]
    delta_g_model_u = np.array([0])

    # Calculate the delta_g_model_u using the least square fit method
    delta_g_model_u_x = leastsq(residuals, delta_g_model_u, args=delta_g_m_exp_u[0])
    delta_g_model_u_y = leastsq(residuals, delta_g_model_u, args=delta_g_m_exp_u[1])
    delta_g_model_u = [delta_g_model_u_x, delta_g_model_u_y]
    print('Resultat du calcul')
    print(delta_g_model_u)

    # Build 3D array of the delta g model on the entire image
    d_g_x = delta_g_model_u[0][0] * np.ones((delta_g_m[0].shape[0], delta_g_m[0].shape[1]))
    d_g_y = delta_g_model_u[1][0] * np.ones((delta_g_m[0].shape[0], delta_g_m[0].shape[1]))
    delta_g_model_u_3d = np.array([d_g_x, d_g_y])

    # Recalculate phase and g unstrain with updated reference on the entire image
    g_uns_update_3D = g_uns_exp + delta_g_model_u_3d
    delta_g_m_exp_update_3D = delta_g_m_exp - delta_g_model_u_3d

    # Rebuild 2D arrays to be stored
    g_uns_update = g_uns_update_3D[0, :, :], g_uns_update_3D[1, :, :]
    delta_g_m_exp_update = delta_g_m_exp_update_3D[0, :, :], delta_g_m_exp_update_3D[1, :, :]
    data.SMGData.store_g(datastruct, mask_id, 'gMuns', g_uns_update)
    data.SMGData.store_g(datastruct, mask_id, 'deltagM', delta_g_m_exp_update)

    # Recalculate and store phase
    mesh_x, mesh_y = np.meshgrid(np.arange(phase.shape[0]), np.arange(phase.shape[1]))
    unwrapped_phase_update = unwrap_phase(phase) - 2 * np.pi * (
        np.multiply(g_uns_update[1][0], mesh_x) + np.multiply(g_uns_update[0][0], mesh_y))
    phase_updated = unwrapped_phase_update - np.round(unwrapped_phase_update / (2 * np.pi) * 2 * np.pi)
    data.SMGData.store_g(datastruct, mask_id, 'phasegM', phase_updated)
