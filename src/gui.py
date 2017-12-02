# STEM Moire GPA GUI Module
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
# import matplotlib.patches as patch
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from matplotlib_scalebar.scalebar import ScaleBar
import data as data
import numpy as np


class SMGGUI(object):

    def __init__(self):
        self.fig_GUIFlow = None
        self.event_input = None
        self.event_smhsim = None
        self.event_gpa = None
        self.event_ref = None
        self.event_convert = None
        self.event_strain = None
        self.fig_SMHexp = None
        self.fig_SMHSim = None
#        self.fig_GPA = plt.figure(num='GPA')
        self.fig_NM = None
#        self.fig_strain = plt.figure(num='Strain maps')

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

    def guismhexp(self, datastruct):
        self.fig_SMHexp = plt.figure(num='SMH and reference image')
        self.fig_SMHexp.add_axes(plt.subplot(self.fig_SMHexp.add_subplot(1, 2, 1))).imshow(
            data.SMGData.load(datastruct, 'ISMHexp'), cmap='gray')
        scalebar1 = ScaleBar(data.SMGData.load(datastruct, 'p') * 10 ** -9)
        plt.gca().add_artist(scalebar1)
        self.fig_SMHexp.add_axes(plt.subplot(self.fig_SMHexp.add_subplot(1, 2, 2))).imshow(
            data.SMGData.load(datastruct, 'ICref'), cmap='gray')
        scalebar2 = ScaleBar(data.SMGData.load(datastruct, 'pref') * 10 ** -9)
        plt.gca().add_artist(scalebar2)
        plt.show(block=False)

    def guismhsim(self, datastruct):
        self.fig_SMHsim = plt.figure(num='SMH Simulation')
        self.fig_SMHsim.add_axes(plt.subplot(self.fig_SMHsim.add_subplot(1, 2, 1))).imshow(
            np.log1p(self.fft_display(data.SMGData.load(datastruct, 'FTISMHexp'))), cmap='gray')
        self.fig_SMHsim.add_axes(plt.subplot(self.fig_SMHsim.add_subplot(1, 2, 2))).imshow(
            np.log1p(data.SMGData.load(datastruct, 'FTISMHsim')), cmap='gray')
        fticsquare = data.SMGData.load(datastruct, 'FTISMHsimDisplay')
        print('ftsqaure loaded')
        colormaps = self.generate_colormap_smhsim(fticsquare)
        ftsmhsim = plt.figure(num='Simulated SMH with colors')
        icsplit = plt.figure(num='Ic split into tiles')
# A cleaner
        ZERO = np.zeros(fticsquare[0][0].shape)
        ftsmhsimaxis = ftsmhsim.add_subplot(1,1,1)
        ftsmhsimaxis.imshow(ZERO, cmap="gray", alpha=1)
        max_general = np.max(np.max(np.max(np.max(np.log1p(fticsquare)))))
        print(max_general)
        count = 0
        for i in range(0, fticsquare.shape[0]):
            for j in range(0, fticsquare.shape[1]):
                # Threshold - Color on Moire FFT reconstructed
                # log_squares_in_HRES = np.log1p(fticsquare[i][j])
                # mask = log_squares_in_HRES[:, :] > (0.67 * max_general)
                # log_squares_corrected = log_squares_in_HRES
                # log_squares_corrected[np.invert(mask)] = np.nan
                bla = colors.LinearSegmentedColormap.from_list('my_cmap', colormaps[count])
                #ftsmhsimaxis.imshow(log_squares_corrected, cmap=bla, alpha=.7, clim=(10, 40))
                # Color on split HRES FFT
                icsplitaxis = icsplit.add_subplot(fticsquare.shape[0], fticsquare.shape[0], count + 1)
                icsplitaxis.imshow(np.log1p(fticsquare[i, j]), cmap=bla, clim=(27.5, 34.5))
                icsplitaxis.xaxis.set_visible(False)
                icsplitaxis.yaxis.set_visible(False)
                count += 1
        plt.show(block=False)

    @staticmethod
    def fft_display(fft):
        return np.fft.fftshift(np.abs(fft ** 2))

    @staticmethod
    def generate_colormap_smhsim(fticsquare):
        total_tiles = fticsquare.shape[0] * fticsquare.shape[1]
        initial_color_map = cm.get_cmap(name="jet")
        coef_weighted_color = np.arange(0, total_tiles).astype(float) / (total_tiles- 1)
        customized_color_map_max = []
        for elements in coef_weighted_color:
            customized_color_map_max.append(initial_color_map(elements))
        customized_color_maps = []
        for elements in customized_color_map_max:
            customized_color_maps.append([(0, 0, 0, 0.8), elements])
        return (customized_color_maps)

'''
# Generate the colormap
total_tiles_number = numpy.shape(matrix_squares_in_HRES)[0]*numpy.shape(matrix_squares_in_HRES)[1]
initial_color_map = cm.get_cmap(name="jet")
coef_weighted_color = numpy.arange(0,total_tiles_number).astype(float)/(total_tiles_number-1)
customized_color_map_max = []
for elements in coef_weighted_color:
    customized_color_map_max.append(initial_color_map(elements))
customized_color_maps = []
for elements in customized_color_map_max:
    customized_color_maps.append([(0,0,0,0.8), elements])
#print "avant =", customized_color_maps
#random.shuffle(customized_color_maps)
#print "apres =",customized_color_maps


# Initial image from the stack
ZERO = numpy.zeros(numpy.shape(matrix_squares_in_HRES[0][0]))
fig10ax1.imshow(ZERO, cmap = "gray", alpha=1)

max_general = numpy.max(numpy.max(numpy.max(numpy.max(numpy.log1p(matrix_squares_in_HRES)))))
print max_general

count = 0
for i in range(0, numpy.shape(matrix_squares_in_HRES)[0]):
    for j in range (0, numpy.shape(matrix_squares_in_HRES)[1]):
        # Threshold for fig 10 - Color on Moire FFT reconstructed
        log_squares_in_HRES = numpy.log1p(matrix_squares_in_HRES[i][j])
        mask = log_squares_in_HRES[:,:] > (0.67 * max_general)
        #log_squares_corrected = numpy.multiply(log_squares,index)
        log_squares_corrected = log_squares_in_HRES
        log_squares_corrected[numpy.invert(mask)] = numpy.nan
        bla = colors.LinearSegmentedColormap.from_list('my_cmap', customized_color_maps[count])
        fig10ax1.imshow(log_squares_corrected, cmap = bla, alpha = .7, clim=(10,40))
        #fig10ax1.imshow(log_squares_corrected, cmap = bla, alpha = .5, clim=(29.5,31.5))
        # Color on split HRES FFT
        fig11ax1 = fig11.add_subplot(number_square_per_lines_corr, number_square_per_lines_corr, count+1)
        fig11ax1.imshow(numpy.log1p(matrix_squares_in_HRES[i, j]), cmap=bla, clim=(27.5,34.5))
        fig11ax1.xaxis.set_visible(False)
        fig11ax1.yaxis.set_visible(False)
        #fig12ax1.hist(numpy.log1p(matrix_squares_in_HRES[i, j]), bins=10, normed=True)
        count += 1
        #print "count=", count
plt.draw()
'''