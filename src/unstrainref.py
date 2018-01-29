# Unstrained reference Module


import data as data
import numpy as np
from scipy.optimize import leastsq
from skimage.restoration import unwrap_phase


def update_zerostrain(mask_id, datastruct):

    def residuals(delta_g_model, delta_g_exp):
        delta_g_model_x = delta_g_model[0]
        delta_g_model_y = delta_g_model[1]
        d_g_x = delta_g_model_x * np.ones((delta_g_exp.shape[1], delta_g_exp.shape[2]))
        d_g_y = delta_g_model_y * np.ones((delta_g_exp.shape[1], delta_g_exp.shape[2]))
        d_g = np.array([d_g_x, d_g_y])
        err =  delta_g_exp - d_g
        print('Iteration dans residual')
        return err.flatten()

    """def residuals(delta_g_model, delta_g_exp):
        d_g = delta_g_model * np.ones((delta_g_exp.shape[0], delta_g_exp.shape[1]))
        err = np.absolute(delta_g_exp - d_g)
        print('residual')
        print(err.shape)
        return err.flatten()"""

    # Load data needed
    u = data.SMGData.load(datastruct, 'Uref')
    print('Dand unstrainref', u)
    delta_g_m = data.SMGData.load_g(datastruct, mask_id, 'deltagM')
    g_uns = data.SMGData.load_g(datastruct, mask_id, 'gMuns')
    phase = data.SMGData.load_g(datastruct, mask_id, 'phaseraw')
    # print('deltagM', delta_g_m.shape)
    # print('gMuns', g_uns.shape, g_uns)
    # print('phasegM', phase.shape)

    # Restrain on U
    phase_u = phase[u[1]:u[3], u[0]:u[2]]
    delta_g_m_u = delta_g_m[:, u[1]:u[3], u[0]:u[2]]
    delta_g_model_u = np.array([0, 0])
    # print('Restriction on u')
    # print('deltag', delta_g_m_u.shape)

    """fig = plt.figure()
    fig.add_subplot(1, 3, 1).imshow(delta_g_m_u[0, :, :])
    fig.add_subplot(1, 3, 2).imshow(delta_g_m_u[1, :, :])
    fig.add_subplot(1, 3, 3).imshow(phase_u)
    plt.show()"""

    # Calculate the delta_g_model_u using the least square fit method
    delta_g_model_u= leastsq(residuals, delta_g_model_u, args=delta_g_m_u, ftol=1.49012e-60, xtol=1.49012e-15)
    print('Resultat du calcul')
    print(delta_g_model_u)

    # Build 3D array of the delta g model on the entire image
    d_g_x = delta_g_model_u[0][0] * np.ones(phase.shape)
    d_g_y = delta_g_model_u[0][1] * np.ones(phase.shape)
    delta_g_model_3d = np.array([d_g_x, d_g_y])
    print('deltag Model', delta_g_model_3d)

    # Recalculate phase and g unstrain with updated reference on the entire image
    g_uns_update = g_uns + delta_g_model_3d
    delta_g_m_update = delta_g_m - delta_g_model_3d
    # print('guns_updated', g_uns_update.shape, g_uns_update)
    # print('deltag_updated', delta_g_m_update.shape, delta_g_m_update)

    # Store the updated data
    data.SMGData.store_g(datastruct, mask_id, 'gMuns', g_uns_update)
    data.SMGData.store_g(datastruct, mask_id, 'deltagM', delta_g_m_update)

    # Recalculate and store phase
    mesh_x, mesh_y = np.meshgrid(np.arange(phase.shape[0]), np.arange(phase.shape[1]))
    unwrapped_phase_update = np.array(unwrap_phase(phase)) - 2 * np.pi * (
        np.multiply(g_uns_update[1], mesh_x) + np.multiply(g_uns_update[0], mesh_y))
    phase_updated = unwrapped_phase_update - np.round(unwrapped_phase_update / (2 * np.pi)) * 2 * np.pi
    data.SMGData.store_g(datastruct, mask_id, 'phasegM', phase_updated)

    '''
    phase_updated_u = phase_updated[u[1]:u[3], u[0]:u[2]]
    fig = plt.figure()
    fig.add_subplot(2, 4, 1).imshow(phase)
    fig.add_subplot(2, 4, 2).imshow(phase_u)
    fig.add_subplot(2, 4, 3).imshow(delta_g_m[0, :, :], vmin=-0.01, vmax=0.01, cmap='bwr')
    fig.add_subplot(2, 4, 4).imshow(delta_g_m[1, :, :], vmin=-0.01, vmax=0.01, cmap='bwr')
    fig.add_subplot(2, 4, 5).imshow(phase_updated)
    fig.add_subplot(2, 4, 6).imshow(phase_updated_u)
    fig.add_subplot(2, 4, 7).imshow(delta_g_m_update[0, :, :], vmin=-0.01, vmax=0.01, cmap='bwr')
    fig.add_subplot(2, 4, 8).imshow(delta_g_m_update[1, :, :], vmin=-0.01 , vmax=0.01, cmap='bwr')
    plt.show()

    '''
