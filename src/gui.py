import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox


class SMGGUI(object):

    def __init__(self):
        self.fig_GUIFlow = None
        self.event_input = None
        self.event_smhsim = None
        self.event_gpa = None
        self.event_ref = None
        self.event_convert = None
        self.event_strain = None
        #self.fig_SMHSim = plt.figure(num='SMH Simulation')
        #self.fig_GPA = plt.figure(num='GPA')
        self.fig_NM = None
        #self.fig_strain = plt.figure(num='Strain maps')

    def guiflow(self):
        self.fig_GUIFlow = plt.figure(num='SMG Flow', figsize=(2, 5))
        gs_button = grid.GridSpec(6, 1)
        self.event_input = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[0, 0])), 'Input')
        self.event_input.on_clicked(self.flow)
        self.event_smhsim = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[1, 0])), 'SMHSim')
        self.event_smhsim.on_clicked(self.flow)
        self.event_gpa = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[2, 0])), 'GPA')
        self.event_gpa.on_clicked(self.flow)
        self.event_ref = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[3, 0])), 'Ref')
        self.event_ref.on_clicked(self.flow)
        self.event_convert = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[4, 0])), 'Convert')
        self.event_convert.on_clicked(self.flow)
        self.event_strain = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[5, 0])), 'Strain')
        self.event_strain.on_clicked(self.flow)
        plt.draw()

    def flow(self, event):
        if event.inaxes == self.event_input.ax:
            print('bla')
        elif event.inaxes == self.event_smhsim.ax:
            print('blo')
        elif event.inaxes == self.event_gpa.ax:
            print('ble')
        elif event.inaxes == self.event_ref:
            print('bling')
        elif event.inaxes == self.event_convert:
            print('bang')
        elif event.inaxes == self.event_strain:
            print('bang')

    def guiconv(self):
        self.fig_NM = plt.figure(num='(n,m) shift')
        TextBox(self.fig_NM.add_axes(plt.subplot(self.fig_NM.add_subplot(2, 1, 1))),
                'Horizontal shift', initial='0', label_pad=0.01)
        TextBox(self.fig_NM.add_axes(plt.subplot(self.fig_NM.add_subplot(2, 1, 2))),
                'Vertical shift', initial='0', label_pad=0.01)
        plt.draw()
