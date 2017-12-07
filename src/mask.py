# Mask Module
import numpy as np
'''To test
from tkinter import filedialog
import matplotlib.pyplot as plt
import dm3_lib as dm3_lib'''


def mask_classic(center, r, shape):
    g_0 = [(shape[0] / 2 - center[0]) * np.ones(shape), (shape[1] / 2 - center[1]) * np.ones(shape)]
    mask = np.ndarray(shape=shape)
    '''Do not forget event coordinate (x,y) should be switched compared to array indexing'''
    for i in range(0, shape[1]):
        for j in range(0, shape[0]):
            if ((i - center[1]) ** 2 + (j - center[0]) ** 2) < (r ** 2):
                mask[i, j] = 1
            else:
                mask[i, j] = 0
    return mask, g_0


def mask_gaussian(center, r, shape):
    g_0 = [(shape[0] / 2 - center[0]) * np.ones(shape), (shape[1] / 2 - center[1]) * np.ones(shape)]
    const = 1 / (2 * (2 / 3 * r) ** 2)
    mesh_x, mesh_y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
    delta_x = (mesh_x - center[0]) ** 2
    delta_y = (mesh_y - center[1]) ** 2
    mask = np.exp(-(delta_x + delta_y) * const)
    return mask, g_0

'''Quick test

file_path_smh = filedialog.askopenfilename(title="Load the STEM Moire hologram")
dm3_meta_smh = dm3_lib.DM3(file_path_smh)
image = dm3_meta_smh.imagedata

mask_classic = mask_classic((100,0),50,(512,512))
image_mask_classic = np.multiply(image, mask_classic[0])

mask_gaussian = mask_gaussian((100,0),50,(512,512))
image_mask_gaussian = np.multiply(image, mask_gaussian[0])

fig = plt.figure()
fig_ax1 = fig.add_subplot(1,2,1)
fig_ax2 = fig.add_subplot(1,2,2)
fig_ax1.imshow(image_mask_classic)
fig_ax2.imshow(image_mask_gaussian)
print(mask_classic[1])
print(mask_gaussian[1])

plt.show()'''
