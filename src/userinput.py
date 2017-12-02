# Input Module
from tkinter import filedialog
import dm3_lib as dm3_lib
import numpy as np
import data as data


class UserInput(object):

    def __init__(self):
        pass

    def load_files(self, datastruct):
        file_path_smh = filedialog.askopenfilename(title="Load the STEM Moire hologram")
        file_path_ic = filedialog.askopenfilename(title="Load the reference image")
        dm3_meta_smh = dm3_lib.DM3(file_path_smh)
        dm3_meta_ic = dm3_lib.DM3(file_path_ic)
        self.verify_i(dm3_meta_smh.imagedata, dm3_meta_ic.imagedata)
        pixel_smh = dm3_meta_smh.pxsize
        pixel_ic = dm3_meta_ic.pxsize
        self.verify_p(pixel_smh[0], pixel_ic[0])
        self.verify_p_unit(pixel_smh[1].decode("ascii"), pixel_ic[1].decode("ascii"))
        data.SMGData.store(datastruct, 'ISMHexp', dm3_meta_smh.imagedata)
        data.SMGData.store(datastruct, 'p', pixel_smh[0])
        data.SMGData.store(datastruct, 'ICref', dm3_meta_ic.imagedata)
        data.SMGData.store(datastruct, 'pref', pixel_ic[0])
        print('Files loaded')

    @staticmethod
    def verify_i(ismh, ic):
        for value in np.nditer(np.isreal(ismh)):
            if value is False:
                raise Exception('The STEM Moire hologram is not composed of real numbers.')
        for value in np.nditer(np.isreal(ic)):
            if value is False:
                raise Exception('The Reference Image is not composed of real numbers.')

    @staticmethod
    def verify_p(p, pref):
        if p < 0 or isinstance(p, float) is False:
            print(p)
            raise Exception('The pixel size of the STEM Moire hologram is not a real number strictly positive.')
        if pref < 0 or isinstance(pref, float) is False:
            raise Exception('The pixel size of the Reference image is not a real number strictly positive.')
        if p == pref:
            raise Warning('The pixel size is the same for the STEM Moire hologram and the Reference image. There is'
                          ' probably a mistake.')

    @staticmethod
    def verify_p_unit(unit_p, unit_pref):
        if unit_p != 'nm':
            raise Exception('The pixel size of the STEM Moire hologram is not in nanometer.')
        if unit_pref != 'nm':
            raise Exception('The pixel size of the Reference image is not in nanometer.')
        if unit_p != unit_pref:
            raise Exception('The units used for the pixel size between the two images are different.')
