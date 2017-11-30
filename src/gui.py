import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from matplotlib.widgets import Button

class SMGGUI(object):

    def __init__(self):
        pass

    def guiflow(self):
        fig = plt.figure()
        gs_button = grid.GridSpec(8, 1)
        ax_button_input = plt.subplot(gs_button[0, 0])
        fig_button_input = Button(ax_button_input, 'Input')
        ax_button_smhsim = plt.subplot(gs_button[1, 0])
        fig_button_smhsim = Button(ax_button_smhsim, 'SMHSim')
        ax_button_gpa = plt.subplot(gs_button[2, 0])
        fig_button_gpa = Button(ax_button_gpa, 'GPA')
        ax_button_ref = plt.subplot(gs_button[3, 0])
        fig_button_ref = Button(ax_button_ref, 'Ref')
        ax_button_convert = plt.subplot(gs_button[4, 0])
        fig_button_convert = Button(ax_button_convert, 'Convert')
        ax_button_strain = plt.subplot(gs_button[5, 0])
        fig_button_strain = Button(ax_button_strain, 'Strain')
        plt.draw()

    def test(self):
        print('bla')
