# Image Display module

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button, SpanSelector, TextBox
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.colorbar import Colorbar
from scipy.misc import imsave
import numpy as np
import guilinemanager
import skimage.measure
# import time
# import string
import collections


ButtonParams = collections.namedtuple('bp', ['text', 'x', 'y', 'functioncall'])


class GUIDisplay(object):
    """Display 2d arrays with interactive parameters:
                - Contrast
                - Colormap
                - Axis label
                - Legend
                - Calibration
                - Scalebar
                - Line profile
                - Export"""
    def __init__(self, data_to_display, cal=None):
        # 2D array to display with calibration cal in nm/pixel
        self.image_data = data_to_display
        # Window for image display + matplotlib parameters
        self.fig_image = plt.figure(figsize=(10, 7), dpi=100)
        # Layout figure
        self.gs_fig_image = gridspec.GridSpec(8, 8)

        # Make buttons and assign function calls
        buttons = (
            ButtonParams('Refresh', 0, 0, self.test),
            ButtonParams('Set\nColourmap', 1, 0, self.colourmap_button),
            ButtonParams('Calibration', 2, 0, self.test),
            ButtonParams('Scale bar', 3, 0, self.update_scalebar),
            ButtonParams('Line profile', 4, 0, self.line_profile),
            ButtonParams('Num 5', 5, 0, self.test),
            ButtonParams('Num 6', 6, 0, self.test),
            ButtonParams('Export', 7, 0, self.export_data)
        )
        self.fig_image_parameter = []

        # Assign button to subplot in figure
        for ii in buttons:
            button = Button(plt.subplot(self.gs_fig_image[ii.x, ii.y]), ii.text)
            button.on_clicked(ii.functioncall)
            self.fig_image_parameter.append(button)

        # Define image axis
        self.ax_image = plt.subplot(self.gs_fig_image[1:-1, 1:6])
        self.ax_image.set_axis_off()
        self.cmap = 'gray'
        self.image = self.ax_image.imshow(self.image_data, cmap=self.cmap)

        # Contrast histogram display and span selector
        self.ax_contrast = plt.subplot(self.gs_fig_image[0, 1:6])
        self.contrastbins = 256
        self.cmin = np.min(self.image_data)
        self.cmax = np.max(self.image_data)
        self.imhist, self.imbins = np.histogram(self.image_data, bins=self.contrastbins)
        self.ax_contrast_span = None
        self.plot_contrast_histogram()

        # Colormaps
        self.maps = sorted([m for m in plt.cm.datad if not m.endswith("_r")])
        self.cmapfig = None
        self.cmapaxes = None
        # (https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps)

        # Colourbar
        self.ax_colourbar = plt.subplot(self.gs_fig_image[1:-1, 7])
        self.colourbar = Colorbar(self.ax_colourbar, self.image)

        # Textbox for colormap
        self.ax_cmin = plt.axes([0.8, 0.85, 0.1, 0.05])
        self.ax_cmax = plt.axes([0.8, 0.8, 0.1, 0.05])
        self.text_cmin = TextBox(self.ax_cmin, label='min', initial="%.2f" % self.cmin, label_pad=0.25)
        self.text_cmax = TextBox(self.ax_cmax, label='max', initial="%.2f" % self.cmax, label_pad=0.25)
        self.text_cmin.on_submit(self.update_cmin)
        self.text_cmax.on_submit(self.update_cmax)

        # Calibration textbox
        self.cal = cal
        self.ax_cal = plt.axes([0.5, 0.1, 0.1, 0.05])
        if self.cal is None:
            self.text_cal = TextBox(self.ax_cal, label='Calibration (nm/pixel)', initial='', label_pad=0.25)
        else:
            self.text_cal = TextBox(self.ax_cal, label='Calibration (nm/pixel)', initial=self.cal, label_pad=0.25)
        self.text_cal.on_submit(self.update_calibration)

        # Scalebar
        self.state_scalebar = 0
        self.scalebar = None

        # Line profile
        self.line_prof = None
        self.line_prof_edit = 0
        self.fig_line_prof = None
        self.ax_fig_line_prof = None

        # Show the display window
        plt.show()

    @staticmethod
    def test(event):
        print(event)

    # Button to open colourmap selection window
    def colourmap_button(self, event):
        if event.inaxes == self.fig_image_parameter[1].ax:
            nummaps = len(self.maps)
            self.cmapfig = plt.figure('Colourmap options, pick one!', figsize=(5, 2 * nummaps))
            self.cmapaxes = {}
            gradient = np.linspace(0, 1, 100) * np.ones((3, 100))

            for mm in range(nummaps):
                corners = [0., mm / float(nummaps), 0.75, 1. / nummaps]
                self.cmapaxes[mm] = plt.axes(corners)
                self.cmapaxes[mm].annotate(self.maps[mm], xy=(0.77, (mm + 0.2) / float(nummaps)),
                                           xycoords='figure fraction', fontsize=11)
                self.cmapaxes[mm].set_axis_off()
                self.cmapaxes[mm].imshow(gradient, cmap=plt.get_cmap(self.maps[mm]))

            self.cmapfig.canvas.mpl_connect('button_press_event', self.colourmap_axis_select)

            plt.show()

    # Set colourmap based on clicking on an axis in the colourmap window
    def colourmap_axis_select(self, event):
        for aa in self.cmapaxes:
            if event.inaxes == self.cmapaxes[aa]:
                self.cmap = self.maps[aa]
                self.image.set_cmap(plt.get_cmap(self.cmap))
                self.update_colourmap()
                self.fig_image.canvas.draw()

    def line_profile(self, event):
        if event.inaxes == self.fig_image_parameter[4].ax:
            if self.line_prof_edit == 0:
                if self.line_prof is None:
                    print('create line')
                    self.line_prof_edit = 1
                    self.line_prof = guilinemanager.LineDraw(self.ax_image)
                    self.line_prof.ConnectDraw()
                else:
                    print('edit line')
                    self.line_prof_edit = 1
                    self.line_prof.ConnectMove()
            elif self.line_prof_edit == 1:
                print('disconect')
                self.line_prof_edit = 0
                self.line_prof.DisconnectDraw()
                self.line_prof.DisconnectMove()
                self.fig_line_prof = plt.figure()
                self.ax_fig_line_prof = self.fig_line_prof.add_subplot(1, 1, 1)
                print(self.line_prof.WidthData)
                first_postion = (self.line_prof.LineCoords[0][1], self.line_prof.LineCoords[0][0])
                second_postion = (self.line_prof.LineCoords[1][1], self.line_prof.LineCoords[1][0])
                line_profile = skimage.measure.profile_line(self.image_data, first_postion,
                                                            second_postion,
                                                            linewidth=int(self.line_prof.WidthData))
                self.ax_fig_line_prof.plot(line_profile)
                plt.show()
            else:
                return

    # Function to update image after changing it
    def update_image(self):
        self.image.set_clim(vmin=self.cmin, vmax=self.cmax)

    def update_colourmap(self):
        self.colourbar.update_bruteforce(self.image)

    def update_cm_textbox(self):
        self.text_cmin.set_val("%.2f" % self.cmin)
        self.text_cmax.set_val("%.2f" % self.cmax)

    def update_cmin(self, event):
        self.cmin = float(event)
        self.contrast_span(self.cmin, self.cmax)

    def update_cmax(self, event):
        self.cmax = float(event)
        self.contrast_span(self.cmin, self.cmax)

    # Calculates and plots image histogram and connects interactive spanselector
    def plot_contrast_histogram(self):
        self.ax_contrast.cla()
        self.ax_contrast.plot(self.imbins[:-1], self.imhist, color='k')
        self.ax_contrast.set_axis_off()
        self.ax_contrast_span = SpanSelector(self.ax_contrast, self.contrast_span, 'horizontal',
                                             span_stays=True, rectprops=dict(alpha=0.5, facecolor='green'))

    # Function for interactive spanselector for contrast histogram
    def contrast_span(self, cmin, cmax):
        self.cmin = cmin
        self.cmax = cmax
        self.update_image()
        self.update_colourmap()
        self.update_cm_textbox()

    def update_calibration(self, event):
        self.cal = float(event)

    def update_scalebar(self, event):
        if event.inaxes == self.fig_image_parameter[3].ax:
            if self.state_scalebar == 0:
                if self.cal is not None:
                    self.state_scalebar = 1
                    self.scalebar = self.ax_image.add_artist(ScaleBar(self.cal * 10 ** -9))
                    self.fig_image.canvas.draw()
            elif self.state_scalebar == 1:
                if self.cal is not None:
                    self.state_scalebar = 0
                    self.scalebar.remove()
                    self.fig_image.canvas.draw()
            else:
                raise Exception("Invalid parameter for scalebar")

    def export_data(self, event):
        if event.inaxes == self.fig_image_parameter[7].ax:
            print('export')
            '''Save image respecting the number of pixels of the origin image'''
            imsave('image_array.png', self.image_data)
            '''Save image without respecting the number of pixels of the origin image'''
            plt.ioff()
            fig_export = plt.figure(figsize=(10, 7), dpi=100)
            image_fig_export = fig_export.add_subplot(1, 1, 1).imshow(self.image_data,
                                                                      cmap=self.cmap,
                                                                      vmin=self.cmin,
                                                                      vmax=self.cmax
                                                                      )
            fig_export.colorbar(image_fig_export)
            fig_export.savefig('image.png')
            print('Image saved')
            plt.close(fig_export)
