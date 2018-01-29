# STEM Moire GPA GUI Module


import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.artist as artist
import matplotlib.patches as patch
from tkinter import filedialog
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from matplotlib_scalebar.scalebar import ScaleBar
import data as data
import numpy as np
import guimaskmanager as maskmanag
import guirectanglemanager as rectmanag


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
        self.fig_GPA_M1 = None
        self.fig_GPA_M2 = None
        self.fig_GPA_M1_ax = None
        self.fig_GPA_M2_ax= None
        self.rectangle_M1 = None
        self.rectangle_M2 = None
        self.fig_NM = None
        self.fig_strain = None
        self.mask =dict()
        self.mask_selected = None
        self.h_1 = 0
        self.h_2 = 0
        self.v_1 = 0
        self.v_2 = 0

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

        def collect_shift_h1(text):
            if text != '':
                if isinstance(int(text), int) == True:
                    self.h_1 = int(text)
                else:
                    return
            else:
                return

        def collect_shift_v1(text):
            if text != '':
                if isinstance(int(text), int) == True:
                    self.v_1 = int(text)
                else:
                    return
            else:
                return

        def collect_shift_h2(text):
            if text != '':
                if isinstance(int(text), int) == True:
                    self.h_2 = int(text)
                else:
                    return
            else:
                return

        def collect_shift_v2(text):
            if text != '':
                if isinstance(int(text), int) == True:
                    self.v_2 = int(text)
                else:
                    return
            else:
                return

        self.fig_NM = plt.figure(figsize=(1.2,2), num='(n,m) shift')
        fig_ax_text_1 = self.fig_NM.add_axes(plt.axes([0.1, 0.8, 0.8, 0.1]))
        fig_ax_text_2 = self.fig_NM.add_axes(plt.axes([0.1, 0.4, 0.8, 0.1]))
        fig_ax_text_1.set_axis_off()
        fig_ax_text_1.format_coord = lambda x, y: ""
        fig_ax_text_1.text(0, 0.2, 'Shift related to the Red mask')
        fig_ax_text_2.set_axis_off()
        fig_ax_text_2.text(0, 0.2, 'Shift related to the Blue mask')
        fig_ax_text_2.format_coord = lambda x, y: ""
        self.textbox_h_1 = TextBox(self.fig_NM.add_axes(plt.axes([0.6, 0.65, 0.2, 0.1])),
                                   'Horizontal shift :', initial='0', label_pad=.2)
        self.textbox_v_1 = TextBox(self.fig_NM.add_axes(plt.axes([0.6, 0.55, 0.2, 0.1])),
                                   'Vertical shift :', initial='0', label_pad=0.2)
        self.textbox_h_2 = TextBox(self.fig_NM.add_axes(plt.axes([0.6, 0.25, 0.2, 0.1])),
                                  'Horizontal shift :', initial='0', label_pad=.2)
        self.textbox_v_2 = TextBox(self.fig_NM.add_axes(plt.axes([0.6, 0.15, 0.2, 0.1])),
                                  'Vertical shift :', initial='0', label_pad=0.2)
        id1h = self.textbox_h_1.on_text_change(collect_shift_h1)
        id2h = self.textbox_h_2.on_text_change(collect_shift_h2)
        id1v = self.textbox_v_1.on_text_change(collect_shift_v1)
        id2v = self.textbox_v_2.on_text_change(collect_shift_v2)

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
        plt.show()

    def guismhsim(self, datastruct):

        def edit_mode(event):
            if event.key == 'e':
                print('Edit mode open, please edit your masks')
                for circle in self.circles:
                    circle.connect()
                for element in self.mask.keys():
                    data.SMGData.remove_branch(datastruct, element)

            if event.key == 'd':
                print('Edit mode closed, please select the mask for the GPA process')
                for circle in self.circles:
                    self.mask[artist.Artist.get_gid(circle.artist)] = (circle.artist.center, circle.artist.radius)
                    circle.disconnect_edit()
                for element in self.mask.keys():
                    data.SMGData.create_branch(datastruct, element)
                    data.SMGData.store_g(datastruct, element, 'Mask', self.mask[element])

        self.fig_SMHsim = plt.figure(num='SMH Simulation')
        self.fig_SMHsim.canvas.mpl_connect('key_press_event', edit_mode)
        #self.fig_SMHsim.add_axes(plt.subplot(self.fig_SMHsim.add_subplot(1, 2, 1))).imshow(
        #    np.log1p(self.fft_display(data.SMGData.load(datastruct, 'FTISMHexp'))), cmap='gray')
        self.fig_SMHsim_axis = self.fig_SMHsim.add_subplot(1,2,1)
        ftsmhexp = data.SMGData.load(datastruct, 'FTISMHexp')
        self.fig_SMHsim_axis.imshow(np.log1p(self.fft_display(ftsmhexp)), cmap='gray')
        self.fig_SMHsim.add_axes(plt.subplot(self.fig_SMHsim.add_subplot(1, 2, 2))).imshow(
            np.log1p(data.SMGData.load(datastruct, 'FTISMHsim')), cmap='gray')

        fticsquare = data.SMGData.load(datastruct, 'FTISMHsimDisplay')
        colormaps_Moire, colormaps_IC = self.generate_colormap_smhsim(fticsquare.shape[0] * fticsquare.shape[1])
        ftsmhsim = plt.figure(num='Simulated SMH with colors')
        icsplit = plt.figure(num='Ic split into tiles')
        # A cleaner
        ZERO = np.zeros(fticsquare[0][0].shape)
        ftsmhsimaxis = ftsmhsim.add_subplot(1,1,1)
        ftsmhsimaxis.imshow(ZERO, cmap="gray", alpha=1)
        max_general = np.max(np.max(np.max(np.max(np.log1p(fticsquare)))))

        count = 0
        for i in range(0, fticsquare.shape[0]):
            for j in range(0, fticsquare.shape[1]):
                # Threshold - Color on Moire FFT reconstructed
                Test = np.log1p(fticsquare[i, j])
                mask = Test[:, :] < (0.67 * max_general)
                Test[mask] = 0
                cmap_moire = colors.LinearSegmentedColormap.from_list('my_cmap', colormaps_Moire[count])
                cmap_ic = colors.LinearSegmentedColormap.from_list('my_cmap', colormaps_IC[count])
                ftsmhsimaxis.imshow(Test, cmap = cmap_moire, alpha = .7, clim=(20, 40))
                # Color on split HRES FFT
                icsplitaxis = icsplit.add_subplot(fticsquare.shape[0], fticsquare.shape[0], count + 1)
                icsplitaxis.imshow(np.log1p(fticsquare[i, j]), cmap=cmap_ic, clim=(27.5, 34.5))
                icsplitaxis.xaxis.set_visible(False)
                icsplitaxis.yaxis.set_visible(False)
                count += 1

        smgmaskcreate = maskmanag.MaskCreator(self.fig_SMHsim_axis,ftsmhexp)
        circle1 = smgmaskcreate.make_circle('Mask1')
        circle2 = smgmaskcreate.make_circle('Mask2', colored='b',off_center=(20,20))
        self.mask[circle1[0]] = circle1[1]
        self.mask[circle2[0]] = circle2[1]
        self.circles = []
        for el in self.fig_SMHsim_axis.artists:
            smgmaskedit = maskmanag.MaskEditor(el)
            self.circles.append(smgmaskedit)

        plt.show()

    def guiphase(self, mask_id, datastruct):

        def close_window(event):
            if event.canvas.figure == self.fig_GPA_M1:
                self.fig_GPA_M1.canvas.mpl_disconnect(cid1close)
                self.fig_GPA_M1.canvas.mpl_disconnect(cid1draw)
                self.fig_GPA_M1 = None
            elif event.canvas.figure == self.fig_GPA_M2:
                self.fig_GPA_M2.canvas.mpl_disconnect(cid2close)
                self.fig_GPA_M2.canvas.mpl_disconnect(cid2draw)
                self.fig_GPA_M2 = None

        def change_rectangle(event):
            if event.canvas.figure == self.fig_GPA_M1 and self.fig_GPA_M2 != None and self.phaseref.done == 1:
                self.phaseref.done = 0
                self.phaseref2.remove_rectangle()
                rectangle = self.fig_GPA_M1_ax.findobj(patch.Rectangle)[0]
                self.phaseref2.create_rectangle(rectangle)
                U = self.reference_extract(rectangle)
                data.SMGData.store(datastruct, 'Uref', U)
            elif event.canvas.figure == self.fig_GPA_M2 and self.fig_GPA_M1 != None and self.phaseref2.done == 1:
                self.phaseref2.done = 0
                self.phaseref.remove_rectangle()
                rectangle = self.fig_GPA_M2_ax.findobj(patch.Rectangle)[0]
                self.phaseref.create_rectangle(rectangle)
                U = self.reference_extract(rectangle)
                data.SMGData.store(datastruct, 'Uref', U)
            else:
                return


        if mask_id == 'Mask1':
            if self.fig_GPA_M1 == None:
                self.fig_GPA_M1 = plt.figure(num='GPA - Mask Red')
                self.fig_GPA_M1_ax = self.fig_GPA_M1.add_subplot(1, 1, 1)
                phase = data.SMGData.load_g(datastruct, mask_id, 'phasegM')
                self.image_mask_1 = self.fig_GPA_M1_ax.imshow(phase, cmap='gray')
                self.rectangle_M1 = rectmanag.make_rectangle(self.fig_GPA_M1_ax, phase)
                self.phaseref = rectmanag.RectEditor(self.fig_GPA_M1, self.fig_GPA_M1_ax, self.rectangle_M1)
                self.phaseref.connect()
                cid1close = self.fig_GPA_M1.canvas.mpl_connect('close_event', close_window)
                cid1draw = self.fig_GPA_M1.canvas.mpl_connect('draw_event', change_rectangle)
                plt.show()
            else:
                self.fig_GPA_M1_ax.imshow(data.SMGData.load_g(datastruct, mask_id, 'phasegM'), cmap='gray')
                plt.draw()
        if mask_id == 'Mask2':
            if self.fig_GPA_M2 == None:
                self.fig_GPA_M2 = plt.figure(num='GPA - Mask Blue')
                self.fig_GPA_M2_ax = self.fig_GPA_M2.add_subplot(1, 1, 1)
                phase = data.SMGData.load_g(datastruct, mask_id, 'phasegM')
                self.image_mask_2 = self.fig_GPA_M2_ax.imshow(phase, cmap='gray')
                self.rectangle_M2 = rectmanag.make_rectangle(self.fig_GPA_M2_ax, phase)
                self.phaseref2 = rectmanag.RectEditor(self.fig_GPA_M2, self.fig_GPA_M2_ax, self.rectangle_M2)
                self.phaseref2.connect()
                cid2close = self.fig_GPA_M2.canvas.mpl_connect('close_event', close_window)
                cid2draw = self.fig_GPA_M2.canvas.mpl_connect('draw_event', change_rectangle)
                plt.show()
            else:
                self.fig_GPA_M2_ax.imshow(data.SMGData.load_g(datastruct, mask_id, 'phasegM'), cmap='gray')
                plt.draw()
        else:
            return

    def guistrain(self, datastruct):
        self.fig_strain = plt.figure(num='Strain maps')
        fig_strain_ax_exx = self.fig_strain.add_subplot(2, 2, 1)
        fig_strain_ax_eyy = self.fig_strain.add_subplot(2, 2, 2)
        fig_strain_ax_exy = self.fig_strain.add_subplot(2, 2, 3)
        fig_strain_ax_rxy = self.fig_strain.add_subplot(2, 2, 4)
        fig_strain_ax_exx.imshow(data.SMGData.load(datastruct,'Exx'), cmap='bwr', vmin=-0.02, vmax=0.02)
        fig_strain_ax_eyy.imshow(data.SMGData.load(datastruct, 'Eyy'), cmap='bwr', vmin=-0.02, vmax=0.02)
        fig_strain_ax_exy.imshow(data.SMGData.load(datastruct, 'Exy'), cmap='bwr', vmin=-0.02, vmax=0.02)
        fig_strain_ax_rxy.imshow(data.SMGData.load(datastruct, 'Rxy'), cmap='bwr', vmin=-0.02,vmax=0.02)
        fig_strain_ax_exx.set_title('εxx')
        fig_strain_ax_eyy.set_title('εyy')
        fig_strain_ax_exy.set_title('εxy')
        fig_strain_ax_rxy.set_title('ωxy')
        plt.show()


    @staticmethod
    def fft_display(fft):
        return np.fft.fftshift(np.abs(fft ** 2))

    @staticmethod
    def generate_colormap_smhsim(total_tiles):
        initial_color_map = cm.get_cmap(name="jet")
        coef_weighted_color = np.arange(0, total_tiles).astype(float) / (total_tiles- 1)
        customized_color_map_max = []
        for elements in coef_weighted_color:
            customized_color_map_max.append(initial_color_map(elements))
        customized_color_maps_Moire = []
        customized_color_maps_Ic =[]
        for elements in customized_color_map_max:
            customized_color_maps_Moire.append([(0, 0, 0, 0.0), elements])
            customized_color_maps_Ic.append([(0, 0, 0, 0.8), elements])
        return customized_color_maps_Moire, customized_color_maps_Ic

    def mask_selection(self):
        for circle in self.circles:
            if circle.mask_selected is not None:
                self.mask_selected = circle.mask_selected
                print('Mask selected')
                return self.mask_selected

    def reference_extract(self, rectangle):
        x0, y0 = rectangle.get_xy()
        x1, y1 = x0 + rectangle.get_width(), y0 + rectangle.get_height()
        print(int(x0), int(y0), int(x1), int(y1))
        return int(x0), int(y0), int(x1), int(y1)

    def update_phase(self, mask_id, datastruct):
        if mask_id == 'Mask1':
            phase = data.SMGData.load_g(datastruct, mask_id, 'phasegM')
            print('Mask 1 update')
            #print(self.image_mask_1)
            #self.image_mask_1.remove()
            self.fig_GPA_M1_ax.imshow(phase, cmap='gray')
            self.fig_GPA_M1.canvas.draw()
        elif mask_id == 'Mask2':
            print('Mask 2 update')
            phase = data.SMGData.load_g(datastruct, mask_id, 'phasegM')
            #print(self.image_mask_2)
            #self.image_mask_2.remove()
            self.fig_GPA_M2_ax.imshow(phase, cmap='gray')
            self.fig_GPA_M2.canvas.draw()
        else:
            pass

    @staticmethod
    def open_files():
        file_path_smh = filedialog.askopenfilename(title="Load the STEM Moire hologram")
        file_path_ic = filedialog.askopenfilename(title="Load the reference image")
        return file_path_smh, file_path_ic