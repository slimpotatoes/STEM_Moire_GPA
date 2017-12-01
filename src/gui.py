# STEM Moire GPA GUI Module
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from matplotlib_scalebar.scalebar import ScaleBar
import data as data

class SMGGUI(object):

    def __init__(self):
        self.fig_GUIFlow = None
        self.event_input = None
        self.event_smhsim = None
        self.event_gpa = None
        self.event_ref = None
        self.event_convert = None
        self.event_strain = None
        self.fig_GUI_SMHexp = None
        #self.fig_SMHSim = plt.figure(num='SMH Simulation')
        #self.fig_GPA = plt.figure(num='GPA')
        self.fig_NM = None
        #self.fig_strain = plt.figure(num='Strain maps')

    def guiflow(self):
        self.fig_GUIFlow = plt.figure(num='SMG Flow', figsize=(2, 5))
        gs_button = grid.GridSpec(6, 1)
        self.event_input = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[0, 0])), 'Input')
        self.event_smhsim = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[1, 0])), 'SMHSim')
        self.event_gpa = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[2, 0])), 'GPA')
        self.event_ref = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[3, 0])), 'Ref')
        self.event_convert = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[4, 0])), 'Convert')
        self.event_strain = Button(self.fig_GUIFlow.add_axes(self.fig_GUIFlow.add_subplot(gs_button[5, 0])), 'Strain')

    def guiconv(self):
        self.fig_NM = plt.figure(num='(n,m) shift')
        TextBox(self.fig_NM.add_axes(plt.subplot(self.fig_NM.add_subplot(2, 1, 1))),
                'Horizontal shift', initial='0', label_pad=0.01)
        TextBox(self.fig_NM.add_axes(plt.subplot(self.fig_NM.add_subplot(2, 1, 2))),
                'Vertical shift', initial='0', label_pad=0.01)

    def guismhexp(self, a):
        self.fig_GUI_SMHexp = plt.figure(num='SMH and reference image')
        self.fig_GUI_SMHexp.add_axes(plt.subplot(self.fig_GUI_SMHexp.add_subplot(1, 2, 1))).imshow(
            data.SMGData.load(a, 'ISMHexp'), cmap='gray')
        ScaleBar1 = ScaleBar(data.SMGData.load(a, 'p') * 10 ** -9)
        plt.gca().add_artist(ScaleBar1)
        self.fig_GUI_SMHexp.add_axes(plt.subplot(self.fig_GUI_SMHexp.add_subplot(1, 2, 2))).imshow(
            data.SMGData.load(a, 'ICref'), cmap='gray')
        ScaleBar2 = ScaleBar(data.SMGData.load(a, 'pref') * 10 ** -9)
        plt.gca().add_artist(ScaleBar2)
        plt.show(block=False)
