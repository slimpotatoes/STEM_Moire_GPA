# Input Module
from tkinter import filedialog
import dm3_lib as dm3_lib

class UserInput(object):

    def __init__(self):
        pass

    @staticmethod
    def load_files(datastruct):
        file_path_smh = filedialog.askopenfilename(title="Load the STEM Moire hologram")
        file_path_ic = filedialog.askopenfilename(title="Load the reference image")
        dm3_meta_smh = dm3_lib.DM3(file_path_smh)
        dm3_meta_ic = dm3_lib.DM3(file_path_ic)
        datastruct.store('ISMHexp', dm3_meta_smh.imagedata)
        datastruct.store('ICref', dm3_meta_ic.imagedata)
        print('Files loaded')
