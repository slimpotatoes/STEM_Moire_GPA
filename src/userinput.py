# Input Module


import dm3_lib as dm3_lib
import numpy as np
import data as data


def load_files(file_path_smh, file_path_ic, datastruct):
    """Load the files by asking the controller the filepaths smh and ic provided by the user and store the appropriate
    data in the data structure object (dictionary). Before storing, the data are verified"""
    dm3_meta_smh = dm3_lib.DM3(file_path_smh)
    dm3_meta_ic = dm3_lib.DM3(file_path_ic)
    verify_i(dm3_meta_smh.imagedata, dm3_meta_ic.imagedata)
    pixel_smh = dm3_meta_smh.pxsize
    pixel_ic = dm3_meta_ic.pxsize
    verify_p(pixel_smh[0], pixel_ic[0])
    verify_p_unit(pixel_smh[1].decode("ascii"), pixel_ic[1].decode("ascii"))
    data.SMGData.store(datastruct, 'ISMHexp', dm3_meta_smh.imagedata)
    data.SMGData.store(datastruct, 'p', pixel_smh[0])
    data.SMGData.store(datastruct, 'ICref', dm3_meta_ic.imagedata)
    data.SMGData.store(datastruct, 'pref', pixel_ic[0])
    print('Files loaded')
    print('Pixel size SMH: ', pixel_smh[0], 'nm')
    print('Pixel size Reference: ', pixel_ic[0], 'nm')


def verify_i(ismh, ic):
    """Verify if the input images ismh and ic are 2D arrays of real numbers"""
    for value in np.nditer(np.isreal(ismh)):
        if value is False:
            raise Exception('The STEM Moire hologram is not composed of real numbers.')
    for value in np.nditer(np.isreal(ic)):
        if value is False:
                raise Exception('The Reference Image is not composed of real numbers.')


def verify_p(p, pref):
    """Verify if the pixel size input p and pref are real numbers strictly positive and if there are different."""
    if p < 0 or isinstance(p, float) is False:
        raise Exception('The pixel size of the STEM Moire hologram is not a real number strictly positive.')
    if pref < 0 or isinstance(pref, float) is False:
        raise Exception('The pixel size of the Reference image is not a real number strictly positive.')
    if p == pref:
        print('The pixel size is the same for the STEM Moire hologram and the Reference image. The software '
              'is now running in classic HRSTEM GPA mode.')
    # Improve it with a raise warning but it doesn't continue


def verify_p_unit(unit_p, unit_pref):
    """Verify if the unit of the pixel size inputs unit_p and unit_pref are in nm"""
    if unit_p != 'nm':
        raise Exception('The pixel size of the STEM Moire hologram is not in nanometer.')
    if unit_pref != 'nm':
        raise Exception('The pixel size of the Reference image is not in nanometer.')
    if unit_p != unit_pref:
        raise Exception('The units used for the pixel size between the two images are different.')
