# Input Module
import tkinter as tk
from tkinter import filedialog
import dm3_lib as dm3_lib
import numpy as np


def load_files(datastruct):
    #root = tk.Tk()
    #root.withdraw()
    file_path_smh = filedialog.askopenfilename(title="Load the STEM Moire hologram")
    file_path_ic = filedialog.askopenfilename(title="Load the reference image")
    dm3_meta_smh = dm3_lib.DM3(file_path_smh)
    dm3_meta_ic = dm3_lib.DM3(file_path_ic)
    verify_i(dm3_meta_smh.imagedata, dm3_meta_ic.imagedata)
    pixel_smh = dm3_meta_smh.pxsize
    pixel_ic = dm3_meta_ic.pxsize
    verify_p(pixel_smh[0], pixel_ic[0])
    datastruct.store('ISMHexp', dm3_meta_smh.imagedata)
    datastruct.store('ICref', dm3_meta_ic.imagedata)
    datastruct.store('p', pixel_smh[0])
    datastruct.store('pref', pixel_ic[0])
    print('Files loaded')


def verify_i(ismh, ic):
    for value in np.nditer(np.isreal(ismh)):
        if value is False:
            raise Exception('The STEM Moire hologram is not composed of real numbers.')
    for value in np.nditer(np.isreal(ic)):
        if value is False:
            raise Exception('The Reference Image is not composed of real numbers.')

def verify_p(p, pref):
    if p < 0 or isinstance(p, float) == False:
        print(p)
        raise Exception('The pixel size of the STEM Moire hologram is not a real number strictly positive.')
    if pref < 0 or isinstance(pref, float) == False:
        raise Exception('The pixel size of the Reference image is not a real number strictly positive.')
    if p == pref:
        raise Warning('The pixel size is the same for the STEM Moire hologram and the Reference image. There is'
                      ' probably a mistake.')

def verify_p_unit(unit_p, unit_pref):
    if unit_p != 'nm':
        raise Exception('The pixel size of the STEM Moire hologram is not in nanometer.')
    if unit_pref != 'nm':
        raise Exception('The pixel size of the Reference image is not in nanometer.')
    if unit_p == unit_pref:
        raise Exception('The units used for the pixel size between the two images are different.')