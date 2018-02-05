# GUI Display module inspired from I. Bicket. Generic tools for the user to modify how the data is displayed
# on the screen.

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button, SpanSelector
import matplotlib.colorbar as cbar
from matplotlib_scalebar.scalebar import ScaleBar
import numpy as np
import time
import string
import collections

'''
Beautiful dreams:
Colourmap cycle - yay! it's really slow, though...
Axis labels on/off + enter text
Legend on/off + entries
Title on/off + enter text
Contrast slider - DONE!
Scalebar on/off
'''

ButtonParams = collections.namedtuple('bp', ['text', 'x', 'y', 'functioncall'])


class GUIDisplay(object):
    def __init__(self, data_to_display):
        self.image_data = data_to_display
        # Window for image display + matplotlib parameters
        self.fig_image = plt.figure(figsize=(10, 7), dpi=100)
        # Layout figure
        self.gs_fig_image = gridspec.GridSpec(8, 8)

        # Make buttons and assign function calls
        BUTTONS = (
            ButtonParams('Refresh', 0, 0, self.test),
            ButtonParams('Set\nColourmap', 1, 0, self.ColourmapButton),
            ButtonParams('Num 2', 2, 0, self.test),
            ButtonParams('Num 3', 3, 0, self.test),
            ButtonParams('Num 4', 4, 0, self.test),
            ButtonParams('Num 5', 5, 0, self.test),
            ButtonParams('Num 6', 6, 0, self.test),
            ButtonParams('Export', 7, 0, self.test)
        )
        self.fig_image_parameter = []

        # Assign button to subplot in figure
        for ii in BUTTONS:
            button = Button(plt.subplot(self.gs_fig_image[ii.x, ii.y]), ii.text)
            button.on_clicked(ii.functioncall)
            self.fig_image_parameter.append(button)

        # self.ax_parameter_1 = plt.subplot(self.gs_fig_image[0, 0])
        #		self.fig_image_parameter_1 = Button(self.ax_parameter_1, 'Refresh')
        #		self.ax_parameter_2 = plt.subplot(self.gs_fig_image[1, 0])
        #		self.fig_image_parameter_2 = Button(self.ax_parameter_2, 'Set\nColourmap')
        #		self.ax_parameter_3 = plt.subplot(self.gs_fig_image[2, 0])
        #		self.fig_image_parameter_3 = Button(self.ax_parameter_3, 'Param 3')
        #		self.ax_parameter_4 = plt.subplot(self.gs_fig_image[3, 0])
        #		self.fig_image_parameter_4 = Button(self.ax_parameter_4, 'Param 4')
        #		self.ax_parameter_5 = plt.subplot(self.gs_fig_image[4, 0])
        #		self.fig_image_parameter_5 = Button(self.ax_parameter_5, 'Param 5')
        #		self.ax_parameter_6 = plt.subplot(self.gs_fig_image[5, 0])
        #		self.fig_image_parameter_6 = Button(self.ax_parameter_6, 'Param 6')
        #		self.ax_parameter_7 = plt.subplot(self.gs_fig_image[6, 0])
        #		self.fig_image_parameter_7 = Button(self.ax_parameter_7, 'Param 7')
        #		self.ax_parameter_8 = plt.subplot(self.gs_fig_image[7, 0])
        #		self.fig_image_parameter_8 = Button(self.ax_parameter_8, 'Export')
        self.ax_image = plt.subplot(self.gs_fig_image[1 : 6, 1 :-1])
        self.ax_image.set_axis_off()

        # Function of each axes
        #		self.fig_image_parameter_1.on_clicked(self.test)
        #		self.fig_image_parameter_2.on_clicked(self.ColourmapButton)
        #		self.fig_image_parameter_3.on_clicked(self.test)
        #		self.fig_image_parameter_4.on_clicked(self.test)
        #		self.fig_image_parameter_5.on_clicked(self.test)
        #		self.fig_image_parameter_6.on_clicked(self.test)
        #		self.fig_image_parameter_7.on_clicked(self.test)
        #		self.fig_image_parameter_8.on_clicked(self.test)
        self.image = self.ax_image.imshow(self.image_data, cmap='gray')

        # Contrast histogram display and span selector
        self.ax_contrast = plt.subplot(self.gs_fig_image[0, 1:6])
        self.contrastbins = 256
        self.cmin = np.min(self.image_data)
        self.cmax = np.max(self.image_data)
        self.PlotContrastHistogram()

        # Colourmaps
        self.maps = sorted([m for m in plt.cm.datad if not m.endswith("_r")])
        # (https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps)

        # Show the display window
        plt.show()

    def test(self, event):
        print(event)

    # Button to open colourmap selection window
    def ColourmapButton(self, event):
        nummaps = len(self.maps)
        self.cmapfig = plt.figure('Colourmap options, pick one!', figsize=(5, 2 * nummaps))
        self.cmapaxes = {}
        gradient = np.linspace(0, 1, 100) * np.ones((3, 100))

        for mm in range(nummaps):
            corners = [0., mm / float(nummaps), 0.75, 1. / nummaps]
            self.cmapaxes[mm] = plt.axes(corners)  # this line is slow right now, don't know how to make it better
            self.cmapaxes[mm].annotate(self.maps[mm], xy=(0.77, (mm + 0.2) / float(nummaps)),
                                       xycoords='figure fraction', fontsize=11)
            self.cmapaxes[mm].set_axis_off()
            self.cmapaxes[mm].imshow(gradient, cmap=plt.get_cmap(self.maps[mm]))

        cmap_key = self.cmapfig.canvas.mpl_connect('button_press_event',
                                                   self.ColourmapAxisSelect)

        plt.show()

    # Set colourmap based on clicking on an axis in the colourmap window
    def ColourmapAxisSelect(self, event):
        for aa in self.cmapaxes:
            if event.inaxes == self.cmapaxes[aa]:
                self.image.set_cmap(plt.get_cmap(self.maps[aa]))
                self.fig_image.canvas.draw()

    # Function to update image after changing it
    def UpdateImage(self):
        self.image.set_clim(vmin=self.cmin, vmax=self.cmax)


    # Calculates and plots image histogram and connects interactive spanselector
    def PlotContrastHistogram(self):
        self.imhist, self.imbins = np.histogram(self.image_data, bins=self.contrastbins)
        self.ax_contrast.cla()
        self.ax_contrast.plot( self.imbins[:-1], self.imhist, color='k')
        self.ax_contrast.set_axis_off()
        self.contrast_span = SpanSelector(self.ax_contrast, self.ContrastSpan, 'horizontal',
                                          span_stays=True, rectprops=dict(alpha=0.5, facecolor='green'))

    # Function for interactive spanselector for contrast histogram
    def ContrastSpan(self, cmin, cmax):
        self.cmin = cmin
        self.cmax = cmax
        self.UpdateImage()
