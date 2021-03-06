# Test of GPA Module

import numpy as np
import math as math
import data as data
import gpa as gpa
import matplotlib.pyplot as plt
import statistics

# #######################################
# Test #2 in TestPlan document
# #######################################

data_test_2 = data.SMGData()    # Data structure for test 2

# Generated STEM Moire hologram (256x256 pixels) using numpy arrays with a unique periodicity of 16 pixels along
# horizontal axis. (Very easy test case)

x2 = np.linspace(0, 255, 256)
y2 = np.linspace(0, 255, 256)
mx2, my2 = np.meshgrid(x2, y2)
ismh2 = np.sin(mx2 * 2 * np.pi / 16)
ft_ismh2 = np.fft.fft2(ismh2)

# Store data in datastructure

data_test_2.store('ISMHexp', ismh2)
data_test_2.store('FTISMHexp', ft_ismh2)

# Create branch for mask

data_test_2.create_branch('Mask1')

# Circle of radius 1 centered around coordinate (192, 128)
r2 = 1
center2 = (144, 128)
circle2 = center2, r2

# Store mask properties into datastructure

data_test_2.store_g('Mask1', 'Mask', circle2)

# Entering gpa

gpa.gpa('Mask1', data_test_2)

# Display data

# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test2 = plt.figure(figsize=(13, 9))
fig_test2_ax1 = fig_test2.add_subplot(2, 3, 1)
fig_test2_ax2 = fig_test2.add_subplot(2, 3, 4)
fig_test2_ax3 = fig_test2.add_subplot(2, 3, 2)
fig_test2_ax4 = fig_test2.add_subplot(2, 3, 5)
fig_test2_ax5 = fig_test2.add_subplot(2, 3, 3)
fig_test2_ax6 = fig_test2.add_subplot(2, 3, 6)
fig_test2_ax1.imshow(ismh2, cmap='gray')
fig_test2_ax1.set_title('I_SMH')
fig_test2_ax2.imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh2 ** 2))), cmap='gray')
fig_test2_ax2.set_title('Fourier Transform of I_SMH')
fig_test2_ax3.imshow(data_test_2.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2_ax3.set_title('Raw Phase')
fig_test2_ax4.imshow(data_test_2.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2_ax4.set_title('Phase corrected')
fig_test2_ax5.imshow(data_test_2.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test2_ax5.set_title('Vertical component of Δg')
fig_test2_ax6.imshow(data_test_2.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)
fig_test2_ax6.set_title('Horizontal component of Δg')
fig_test2.savefig('/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/'
                  'Test_2_explanation.png', dpi=300, bbox_inches='tight')

# Input/Output data in 1D
fig_test2_1d = plt.figure(figsize=(13, 9))
fig_test2_1d_ax1 = fig_test2_1d.add_subplot(2, 3, 1)
fig_test2_1d_ax2 = fig_test2_1d.add_subplot(2, 3, 4)
fig_test2_1d_ax3 = fig_test2_1d.add_subplot(2, 3, 2)
fig_test2_1d_ax4 = fig_test2_1d.add_subplot(2, 3, 5)
fig_test2_1d_ax5 = fig_test2_1d.add_subplot(2, 3, 3)
fig_test2_1d_ax6 = fig_test2_1d.add_subplot(2, 3, 6)
fig_test2_1d_ax1.plot(ismh2[128, :])
fig_test2_1d_ax1.set_title('I_SMH')
fig_test2_1d_ax2.plot(x2, np.log1p(np.fft.fftshift(np.abs(ft_ismh2 ** 2)))[128, :])
fig_test2_1d_ax2.set_title('Fourier Transform of I_SMH')
fig_test2_1d_ax3.plot(x2, data_test_2.load_g('Mask1', 'phaseraw')[128, :])
fig_test2_1d_ax3.set_ylim(-np.pi, np.pi)
fig_test2_1d_ax3.set_title('Raw Phase')
fig_test2_1d_ax4.plot(x2, data_test_2.load_g('Mask1', 'phasegM')[128, :])
fig_test2_1d_ax4.set_ylim(-np.pi, np.pi)
fig_test2_1d_ax4.set_title('Phase corrected')
fig_test2_1d_ax5.plot(x2, data_test_2.load_g('Mask1', 'deltagM')[0, 128, :])
fig_test2_1d_ax5.set_ylim(-1, 1)
fig_test2_1d_ax5.set_title('Vertical component of Δg')
fig_test2_1d_ax6.plot(x2, data_test_2.load_g('Mask1', 'deltagM')[1, 128, :])
fig_test2_1d_ax6.set_ylim(-1, 1)
fig_test2_1d_ax6.set_title('Horizontal component of Δg')
fig_test2_1d.savefig('/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/'
                     'Test_2_explanation_1D.png', dpi=300, bbox_inches='tight')

plt.show()

# -------------------- Test #2 Improvement ---------------

# periodicity in pixels: q

q = [3, 4, 4.1, 4.2, 4.5, 16, 100]
data2 = []

for periodicity in q:
    ismh = np.sin(mx2 * 2 * np.pi / periodicity)
    ft_ismh = np.fft.fft2(ismh)
    circle = (128 + round(256 / periodicity), 128), r2
    data_i = data.SMGData()
    data_i.store('ISMHexp', ismh)
    data_i.store('FTISMHexp', ft_ismh)
    data_i.create_branch('Mask1')
    data_i.store_g('Mask1', 'Mask', circle)
    gpa.gpa('Mask1', data_i)
    data2.append(data_i)

fig_test2_multiple_q = plt.figure(figsize=(13, 6))
fig_test2_multiple_q_ax1 = fig_test2_multiple_q.add_subplot(1, 2, 1)
fig_test2_multiple_q_ax2 = fig_test2_multiple_q.add_subplot(1, 2, 2)
fig_test2_multiple_q_ismh = plt.figure(figsize=(13, 6))
fig_test2_multiple_q_ismh_ax1 = fig_test2_multiple_q_ismh.add_subplot(1, 2, 1)
fig_test2_multiple_q_ismh_ax2 = fig_test2_multiple_q_ismh.add_subplot(1, 2, 2)
fig_test2_error_delta_g = plt.figure(figsize=(13, 9))
fig_test2_error_delta_g_ax = fig_test2_error_delta_g.add_subplot(1, 1, 1)
count = 0
mean_test_2 = []
stand_dev_test_2 = []
for elements in data2:
    fig_test2_multiple_q_ax1.plot(x2, elements.load_g('Mask1', 'phasegM')[128, :], linewidth=3, label=str(q[count]))
    fig_test2_multiple_q_ax2.plot(x2, elements.load_g('Mask1', 'deltagM')[1, 128, :], linewidth=3, label=str(q[count]))
    fig_test2_multiple_q_ismh_ax1.plot(x2[160:180], elements.load('ISMHexp')[128, 160:180], linewidth=3,
                                       label=str(q[count]))
    fig_test2_multiple_q_ismh_ax2.plot(x2, np.log1p(np.fft.fftshift(np.abs(elements.load('FTISMHexp') ** 2)))[128, :],
                                       linewidth=3, label=str(q[count]))
    error_delta_g = np.abs(elements.load_g('Mask1', 'deltagM')[1, 128, :])
    fig_test2_error_delta_g_ax.plot(x2, error_delta_g, linewidth=3, label=str(q[count]))
    mean_test_2.append(statistics.mean(elements.load_g('Mask1', 'deltagM')[1, 128, :]))
    stand_dev_test_2.append(statistics.stdev(elements.load_g('Mask1', 'deltagM')[1, 128, :]))
    count += 1
fig_test2_multiple_q_ax1.set_ylim(-np.pi, np.pi)
fig_test2_multiple_q_ax1.legend()
fig_test2_multiple_q_ax1.set_title('Phase corrected')
fig_test2_multiple_q_ax2.set_title('Horizontal component of Δg')
fig_test2_multiple_q_ax2.set_ylim(-0.01, 0.01)
fig_test2_multiple_q_ismh_ax1.set_title('I_SMH')
fig_test2_multiple_q_ismh_ax2.set_title('Fourier Transform of I_SMH')
fig_test2_multiple_q_ismh_ax2.legend()
fig_test2_error_delta_g_ax.set_ylim(0, 0.0025)
fig_test2_error_delta_g_ax.legend()
fig_test2_error_delta_g_ax.set_title('Error of the horizontal component of Δg ')
fig_test2_multiple_q.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_test_results.png',
    dpi=300, bbox_inches='tight')
fig_test2_multiple_q_ismh.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_test_cases.png',
    dpi=300, bbox_inches='tight')
fig_test2_error_delta_g.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_test_error.png',
    dpi=300, bbox_inches='tight')
plt.show()
print('Mean test 2 = ', mean_test_2)
print('StDev test 2 = ', stand_dev_test_2)

# -------------------- Testing the vertical direction -------------------

data_test_2_v = data.SMGData()    # Data structure for test 2

# Generated STEM Moire hologram (256x256 pixels) using numpy arrays with a unique periodicity of 16 pixels along
# horizontal axis. (Very easy test case)

x2_v = np.linspace(0, 255, 256)
y2_v = np.linspace(0, 255, 256)
mx2_v, my2_v = np.meshgrid(x2_v, y2_v)
ismh2_v = np.sin(my2_v * 2 * np.pi / 16)
ft_ismh2_v = np.fft.fft2(ismh2_v)

# Store data in datastructure

data_test_2_v.store('ISMHexp', ismh2_v)
data_test_2_v.store('FTISMHexp', ft_ismh2_v)

# Create branch for mask

data_test_2_v.create_branch('Mask1')

# Circle of radius 1 centered around coordinate (192, 128)
r2_v = 1
center2_v = (128, 144)
circle2_v = center2_v, r2_v

# Store mask properties into datastructure

data_test_2_v.store_g('Mask1', 'Mask', circle2_v)

# Entering gpa

gpa.gpa('Mask1', data_test_2_v)

# Display data

# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test2_v = plt.figure(figsize=(13, 9))
fig_test2_ax1_v = fig_test2_v.add_subplot(2, 3, 1)
fig_test2_ax2_v = fig_test2_v.add_subplot(2, 3, 4)
fig_test2_ax3_v = fig_test2_v.add_subplot(2, 3, 2)
fig_test2_ax4_v = fig_test2_v.add_subplot(2, 3, 5)
fig_test2_ax5_v = fig_test2_v.add_subplot(2, 3, 3)
fig_test2_ax6_v = fig_test2_v.add_subplot(2, 3, 6)
fig_test2_ax1_v.imshow(ismh2_v, cmap='gray')
fig_test2_ax1_v.set_title('I_SMH')
fig_test2_ax2_v.imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh2_v ** 2))), cmap='gray')
fig_test2_ax2_v.set_title('Fourier Transform of I_SMH')
fig_test2_ax3_v.imshow(data_test_2_v.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2_ax3_v.set_title('Raw Phase')
fig_test2_ax4_v.imshow(data_test_2_v.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2_ax4_v.set_title('Phase corrected')
fig_test2_ax5_v.imshow(data_test_2_v.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test2_ax5_v.set_title('Vertical component of Δg')
fig_test2_ax6_v.imshow(data_test_2_v.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)
fig_test2_ax6_v.set_title('Horizontal component of Δg')
fig_test2_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_v_explanation.png',
    dpi=300, bbox_inches='tight')

# Input/Output data in 1D
fig_test2_1d_v = plt.figure(figsize=(13, 9))
fig_test2_1d_ax1_v = fig_test2_1d_v.add_subplot(2, 3, 1)
fig_test2_1d_ax2_v = fig_test2_1d_v.add_subplot(2, 3, 4)
fig_test2_1d_ax3_v = fig_test2_1d_v.add_subplot(2, 3, 2)
fig_test2_1d_ax4_v = fig_test2_1d_v.add_subplot(2, 3, 5)
fig_test2_1d_ax5_v = fig_test2_1d_v.add_subplot(2, 3, 3)
fig_test2_1d_ax6_v = fig_test2_1d_v.add_subplot(2, 3, 6)
fig_test2_1d_ax1_v.plot(ismh2_v[:, 128])
fig_test2_1d_ax1_v.set_title('I_SMH')
fig_test2_1d_ax2_v.plot(y2_v, np.log1p(np.fft.fftshift(np.abs(ft_ismh2_v ** 2)))[:, 128])
fig_test2_1d_ax2_v.set_title('Fourier Transform of I_SMH')
fig_test2_1d_ax3_v.plot(y2_v, data_test_2_v.load_g('Mask1', 'phaseraw')[:, 128])
fig_test2_1d_ax3_v.set_ylim(-np.pi, np.pi)
fig_test2_1d_ax3_v.set_title('Raw Phase')
fig_test2_1d_ax4_v.plot(y2_v, data_test_2_v.load_g('Mask1', 'phasegM')[:, 128])
fig_test2_1d_ax4_v.set_ylim(-np.pi, np.pi)
fig_test2_1d_ax4_v.set_title('Phase corrected')
fig_test2_1d_ax5_v.plot(y2_v, data_test_2_v.load_g('Mask1', 'deltagM')[0, :, 128])
fig_test2_1d_ax5_v.set_ylim(-1, 1)
fig_test2_1d_ax5_v.set_title('Vertical component of Δg')
fig_test2_1d_ax6_v.plot(y2_v, data_test_2_v.load_g('Mask1', 'deltagM')[1, :, 128])
fig_test2_1d_ax6_v.set_ylim(-1, 1)
fig_test2_1d_ax6_v.set_title('Horizontal component of Δg')
fig_test2_1d_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_v_explanation_1D.png',
    dpi=300, bbox_inches='tight')

plt.show()

# -------------------- Test #2 Improvement ---------------

# periodicity in pixels: q

q_v = [3, 4, 4.1, 4.2, 4.5, 16, 100]
data2_v = []

for periodicity in q_v:
    ismh_v = np.sin(my2_v * 2 * np.pi / periodicity)
    ft_ismh_v = np.fft.fft2(ismh_v)
    circle_v = (128, 128 + round(256 / periodicity)), r2_v
    data_i_v = data.SMGData()
    data_i_v.store('ISMHexp', ismh_v)
    data_i_v.store('FTISMHexp', ft_ismh_v)
    data_i_v.create_branch('Mask1')
    data_i_v.store_g('Mask1', 'Mask', circle_v)
    gpa.gpa('Mask1', data_i_v)
    data2_v.append(data_i_v)

fig_test2_multiple_q_v = plt.figure(figsize=(13, 6))
fig_test2_multiple_q_ax1_v = fig_test2_multiple_q_v.add_subplot(1, 2, 1)
fig_test2_multiple_q_ax2_v = fig_test2_multiple_q_v.add_subplot(1, 2, 2)
fig_test2_multiple_q_ismh_v = plt.figure(figsize=(13, 6))
fig_test2_multiple_q_ismh_ax1_v = fig_test2_multiple_q_ismh_v.add_subplot(1, 2, 1)
fig_test2_multiple_q_ismh_ax2_v = fig_test2_multiple_q_ismh_v.add_subplot(1, 2, 2)
fig_test2_error_delta_g_v = plt.figure(figsize=(13, 9))
fig_test2_error_delta_g_ax_v = fig_test2_error_delta_g_v.add_subplot(1, 1, 1)
count = 0
mean_test_2_v = []
stand_dev_test_2_v = []
for elements in data2_v:
    fig_test2_multiple_q_ax1_v.plot(y2_v, elements.load_g('Mask1', 'phasegM')[:, 128],
                                    linewidth=3, label=str(q[count]))
    fig_test2_multiple_q_ax2_v.plot(y2_v, elements.load_g('Mask1', 'deltagM')[0, :, 128],
                                    linewidth=3, label=str(q[count]))
    fig_test2_multiple_q_ismh_ax1_v.plot(y2_v[160:180], elements.load('ISMHexp')[160:180, 128],
                                         linewidth=3, label=str(q_v[count]))
    fig_test2_multiple_q_ismh_ax2_v.plot(y2_v,
                                         np.log1p(np.fft.fftshift(np.abs(elements.load('FTISMHexp') ** 2)))[:, 128],
                                         linewidth=3, label=str(q_v[count]))
    error_delta_g_v = np.abs(elements.load_g('Mask1', 'deltagM')[0, :, 128])
    fig_test2_error_delta_g_ax_v.plot(y2_v, error_delta_g_v, linewidth=3, label=str(q_v[count]))
    mean_test_2_v.append(statistics.mean(elements.load_g('Mask1', 'deltagM')[0, :, 128]))
    stand_dev_test_2_v.append(statistics.stdev(elements.load_g('Mask1', 'deltagM')[0, :, 128]))
    count += 1
fig_test2_multiple_q_ax1_v.set_ylim(-np.pi, np.pi)
fig_test2_multiple_q_ax1_v.legend()
fig_test2_multiple_q_ax1_v.set_title('Phase corrected')
fig_test2_multiple_q_ax2_v.set_title('Vertical component of Δg')
fig_test2_multiple_q_ax2_v.set_ylim(-0.01, 0.01)
fig_test2_multiple_q_ismh_ax1_v.set_title('I_SMH')
fig_test2_multiple_q_ismh_ax2_v.set_title('Fourier Transform of I_SMH')
fig_test2_multiple_q_ismh_ax2_v.legend()
fig_test2_error_delta_g_ax_v.set_ylim(0, 0.0025)
fig_test2_error_delta_g_ax_v.legend()
fig_test2_error_delta_g_ax_v.set_title('Error of the vertical component of Δg ')
fig_test2_multiple_q_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_v_test_results.png',
    dpi=300, bbox_inches='tight')
fig_test2_multiple_q_ismh_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_v_test_cases.png',
    dpi=300, bbox_inches='tight')
fig_test2_error_delta_g_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_2_v_test_error.png',
    dpi=300, bbox_inches='tight')
plt.show()
print('Mean test 2 = ', mean_test_2_v)
print('StDev test 2 = ', stand_dev_test_2_v)


# #######################################
# Test #3 in TestPlan document
# #######################################

data_test_3 = data.SMGData()

# STEM Moire hologram with a unique periodicity of 4 pixels along horizontal axis on half image and a periodicity of
# 4.5 pixel along the same axis on the second half of the image (easy case). This leads to o a 'delta g' of
# 1/4-1/4.5 = 0.0277778.

x3a = np.linspace(0, 127, 128)
x3b = np.linspace(128, 255, 128)
y3 = np.linspace(0, 255, 256)
mx3a, my3a = np.meshgrid(x3a, y3)
mx3b, my3b = np.meshgrid(x3b, y3)
ismh3a = np.sin(mx3a * 2 * np.pi / 4)
ismh3b = np.sin(mx3b * 2 * np.pi / 4.5)
ismh3 = np.concatenate((ismh3a, ismh3b), axis=1)
ft_ismh3 = np.fft.fft2(ismh3)

# Store data in datastructure

data_test_3.store('ISMHexp', ismh3)
data_test_3.store('FTISMHexp', ft_ismh3)

# Create branch for mask

data_test_3.create_branch('Mask1')

# Circle of radius R centered around coordinate (192, 128)
r3 = 20
center3 = (192, 128)
circle3 = center3, r3

# Store mask properties into datastructure

data_test_3.store_g('Mask1', 'Mask', circle3)

# Entering gpa

gpa.gpa('Mask1', data_test_3)

# Display data

# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test3 = plt.figure(figsize=(13, 9))
fig_test3_ax1 = fig_test3.add_subplot(2, 3, 1)
fig_test3_ax2 = fig_test3.add_subplot(2, 3, 4)
fig_test3_ax3 = fig_test3.add_subplot(2, 3, 2)
fig_test3_ax4 = fig_test3.add_subplot(2, 3, 5)
fig_test3_ax5 = fig_test3.add_subplot(2, 3, 3)
fig_test3_ax6 = fig_test3.add_subplot(2, 3, 6)
fig_test3_ax1.imshow(ismh3, cmap='gray')
fig_test3_ax2.imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh3 ** 2))), cmap='gray')
fig_test3_ax3.imshow(data_test_3.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3_ax4.imshow(data_test_3.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3_ax5.imshow(data_test_3.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test3_ax6.imshow(data_test_3.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)
fig_test3_ax1.set_title('I_SMH')
fig_test3_ax2.set_title('Fourier Transform of I_SMH')
fig_test3_ax3.set_title('Raw Phase')
fig_test3_ax4.set_title('Phase corrected')
fig_test3_ax5.set_title('Vertical component of Δg')
fig_test3_ax6.set_title('Horizontal component of Δg')
fig_test3.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_explanation.png',
    dpi=300, bbox_inches='tight')


# Input/Output data in 1D
fig_test3_1d = plt.figure(figsize=(13, 9))
fig_test3_1d_ax1 = fig_test3_1d.add_subplot(2, 3, 1)
fig_test3_1d_ax2 = fig_test3_1d.add_subplot(2, 3, 4)
fig_test3_1d_ax3 = fig_test3_1d.add_subplot(2, 3, 2)
fig_test3_1d_ax4 = fig_test3_1d.add_subplot(2, 3, 5)
fig_test3_1d_ax5 = fig_test3_1d.add_subplot(2, 3, 3)
fig_test3_1d_ax6 = fig_test3_1d.add_subplot(2, 3, 6)
fig_test3_1d_ax1.plot(x2[50:206], ismh3[128, 50:206])
fig_test3_1d_ax2.plot(x2, np.log1p(np.fft.fftshift(np.abs(ft_ismh3 ** 2)))[128, :])
fig_test3_1d_ax3.plot(x2, data_test_3.load_g('Mask1', 'phaseraw')[128, :])
fig_test3_1d_ax3.set_ylim(-np.pi, np.pi)
fig_test3_1d_ax4.plot(x2, data_test_3.load_g('Mask1', 'phasegM')[128, :])
fig_test3_1d_ax4.set_ylim(-np.pi, np.pi)
fig_test3_1d_ax5.plot(x2, data_test_3.load_g('Mask1', 'deltagM')[0, 128, :])
fig_test3_1d_ax5.set_ylim(-0.1, 0.1)
fig_test3_1d_ax6.plot(x2, data_test_3.load_g('Mask1', 'deltagM')[1, 128, :])
fig_test3_1d_ax6.set_ylim(-0.1, 0.1)
fig_test3_1d_ax1.set_title('I_SMH')
fig_test3_1d_ax2.set_title('Fourier Transform of I_SMH')
fig_test3_1d_ax3.set_title('Raw Phase')
fig_test3_1d_ax4.set_title('Phase corrected')
fig_test3_1d_ax5.set_title('Vertical component of Δg')
fig_test3_1d_ax6.set_title('Horizontal component of Δg')
fig_test3_1d.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_explanation_1D.png',
    dpi=300, bbox_inches='tight')

plt.show()

# -------------------- Test #3 Improvement ---------------

# Different strain level: dg
dg = [1/4 - 1/3, 1/4 - 1/3.8, 1/4 - 1/3.9, 1/4 - 1/4, 1/4 - 1/4.1, 1/4 - 1/4.2, 1/4 - 1/5]

# Different strain periodicity
dq = [3, 3.8, 3.9, 4, 4.1, 4.2, 5]

data3 = []

for strain in dq:
    ismhb = np.sin(mx3b * 2 * np.pi / strain)
    ismh = np.concatenate((ismh3a, ismhb), axis=1)
    ft_ismh = np.fft.fft2(ismh)
    circle = (128 + round(256 / 4), 128), r3
    print(circle)
    data_i = data.SMGData()
    data_i.store('ISMHexp', ismh)
    data_i.store('FTISMHexp', ft_ismh)
    data_i.create_branch('Mask1')
    data_i.store_g('Mask1', 'Mask', circle)
    gpa.gpa('Mask1', data_i)
    data3.append(data_i)

fig_test3_multiple_dq = plt.figure(figsize=(13, 6))
fig_test3_multiple_dq_ax1 = fig_test3_multiple_dq.add_subplot(1, 2, 1)
fig_test3_multiple_dq_ax2 = fig_test3_multiple_dq.add_subplot(1, 2, 2)
count = 0
strain_values = []
for elements in data3:
    fig_test3_multiple_dq_ax1.plot(x2[100:200], elements.load_g('Mask1', 'phasegM')[128, 100:200],
                                   linewidth=3, label=str(dq[count]))
    fig_test3_multiple_dq_ax2.plot(x2, elements.load_g('Mask1', 'deltagM')[1, 128, :],
                                   linewidth=3, label=str(dq[count]))
    strain_value = elements.load_g('Mask1', 'deltagM')[1, 128, 200]
    strain_values.append(strain_value)
    count += 1
fig_test3_multiple_dq_ax1.set_ylim(-np.pi, np.pi)
fig_test3_multiple_dq_ax1.legend()
fig_test3_multiple_dq_ax1.set_title('Raw phase')
fig_test3_multiple_dq_ax2.set_title('Horizontal component of Δg')
fig_test3_multiple_dq_ax2.set_ylim(-0.1, 0.1)
fig_test3_multiple_dq.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_test_results.png',
    dpi=300, bbox_inches='tight')
print('dg = ', dg)
print('strain = ', strain_values)
print('error = ', np.abs(np.array(dg)-np.array(strain_values)))
plt.show()

# -----------------------  Test vertical component ----------------------

data_test_3_v = data.SMGData()

# STEM Moire hologram with a unique periodicity of 4 pixels along horizontal axis on half image and a periodicity of
# 4.5 pixel along the same axis on the second half of the image (easy case). This leads to o a 'delta g' of
# 1/4-1/4.5 = 0.0277778.

y3a_v = np.linspace(0, 127, 128)
y3b_v = np.linspace(128, 255, 128)
x3_v = np.linspace(0, 255, 256)
mx3a_v, my3a_v = np.meshgrid(x3_v, y3a_v)
mx3b_v, my3b_v = np.meshgrid(x3_v, y3b_v)
ismh3a_v = np.sin(my3a_v * 2 * np.pi / 4)
ismh3b_v = np.sin(my3b_v * 2 * np.pi / 4.5)
ismh3_v = np.concatenate((ismh3a_v, ismh3b_v), axis=0)
ft_ismh3_v = np.fft.fft2(ismh3_v)

# Store data in datastructure

data_test_3_v.store('ISMHexp', ismh3_v)
data_test_3_v.store('FTISMHexp', ft_ismh3_v)

# Create branch for mask

data_test_3_v.create_branch('Mask1')

# Circle of radius R centered around coordinate (192, 128)
r3_v = 20
center3_v = (128, 192)
circle3_v = center3_v, r3_v

# Store mask properties into datastructure

data_test_3_v.store_g('Mask1', 'Mask', circle3_v)

# Entering gpa

gpa.gpa('Mask1', data_test_3_v)

# Display data

# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test3_v = plt.figure(figsize=(13, 9))
fig_test3_ax1_v = fig_test3_v.add_subplot(2, 3, 1)
fig_test3_ax2_v = fig_test3_v.add_subplot(2, 3, 4)
fig_test3_ax3_v = fig_test3_v.add_subplot(2, 3, 2)
fig_test3_ax4_v = fig_test3_v.add_subplot(2, 3, 5)
fig_test3_ax5_v = fig_test3_v.add_subplot(2, 3, 3)
fig_test3_ax6_v = fig_test3_v.add_subplot(2, 3, 6)
fig_test3_ax1_v.imshow(ismh3_v, cmap='gray')
fig_test3_ax2_v.imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh3_v ** 2))), cmap='gray')
fig_test3_ax3_v.imshow(data_test_3_v.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3_ax4_v.imshow(data_test_3_v.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3_ax5_v.imshow(data_test_3_v.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test3_ax6_v.imshow(data_test_3_v.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)
fig_test3_ax1_v.set_title('I_SMH')
fig_test3_ax2_v.set_title('Fourier Transform of I_SMH')
fig_test3_ax3_v.set_title('Raw Phase')
fig_test3_ax4_v.set_title('Phase corrected')
fig_test3_ax5_v.set_title('Vertical component of Δg')
fig_test3_ax6_v.set_title('Horizontal component of Δg')
fig_test3_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_v_explanation.png',
    dpi=300, bbox_inches='tight')


# Input/Output data in 1D
fig_test3_1d_v = plt.figure(figsize=(13, 9))
fig_test3_1d_ax1_v = fig_test3_1d_v.add_subplot(2, 3, 1)
fig_test3_1d_ax2_v = fig_test3_1d_v.add_subplot(2, 3, 4)
fig_test3_1d_ax3_v = fig_test3_1d_v.add_subplot(2, 3, 2)
fig_test3_1d_ax4_v = fig_test3_1d_v.add_subplot(2, 3, 5)
fig_test3_1d_ax5_v = fig_test3_1d_v.add_subplot(2, 3, 3)
fig_test3_1d_ax6_v = fig_test3_1d_v.add_subplot(2, 3, 6)
fig_test3_1d_ax1_v.plot(x2[50:206], ismh3_v[50:206, 128])
fig_test3_1d_ax2_v.plot(x2, np.log1p(np.fft.fftshift(np.abs(ft_ismh3_v ** 2)))[:, 128])
fig_test3_1d_ax3_v.plot(x2, data_test_3_v.load_g('Mask1', 'phaseraw')[:, 128])
fig_test3_1d_ax3_v.set_ylim(-np.pi, np.pi)
fig_test3_1d_ax4_v.plot(x2, data_test_3_v.load_g('Mask1', 'phasegM')[:, 128])
fig_test3_1d_ax4_v.set_ylim(-np.pi, np.pi)
fig_test3_1d_ax5_v.plot(x2, data_test_3_v.load_g('Mask1', 'deltagM')[0, :, 128])
fig_test3_1d_ax5_v.set_ylim(-0.1, 0.1)
fig_test3_1d_ax6_v.plot(x2, data_test_3_v.load_g('Mask1', 'deltagM')[1, :, 128])
fig_test3_1d_ax6_v.set_ylim(-0.1, 0.1)
fig_test3_1d_ax1_v.set_title('I_SMH')
fig_test3_1d_ax2_v.set_title('Fourier Transform of I_SMH')
fig_test3_1d_ax3_v.set_title('Raw Phase')
fig_test3_1d_ax4_v.set_title('Phase corrected')
fig_test3_1d_ax5_v.set_title('Vertical component of Δg')
fig_test3_1d_ax6_v.set_title('Horizontal component of Δg')
fig_test3_1d_v.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_v_explanation_1D.png',
    dpi=300, bbox_inches='tight')

# -------------------- Test #3 Improvement ---------------

# Different strain level: dg
dg = [1/4 - 1/3, 1/4 - 1/3.8, 1/4 - 1/3.9, 1/4 - 1/4, 1/4 - 1/4.1, 1/4 - 1/4.2, 1/4 - 1/5]

# Different strain periodicity
dq = [3, 3.8, 3.9, 4, 4.1, 4.2, 5]

data3 = []

for strain in dq:
    ismhb = np.sin(mx3b * 2 * np.pi / strain)
    ismh = np.concatenate((ismh3a, ismhb), axis=1)
    ft_ismh = np.fft.fft2(ismh)
    circle = (128 + round(256 / 4), 128), r3
    print(circle)
    data_i = data.SMGData()
    data_i.store('ISMHexp', ismh)
    data_i.store('FTISMHexp', ft_ismh)
    data_i.create_branch('Mask1')
    data_i.store_g('Mask1', 'Mask', circle)
    gpa.gpa('Mask1', data_i)
    data3.append(data_i)

fig_test3_multiple_dq = plt.figure(figsize=(13, 6))
fig_test3_multiple_dq_ax1 = fig_test3_multiple_dq.add_subplot(1, 2, 1)
fig_test3_multiple_dq_ax2 = fig_test3_multiple_dq.add_subplot(1, 2, 2)
count = 0
strain_values = []
for elements in data3:
    fig_test3_multiple_dq_ax1.plot(x2[100:200], elements.load_g('Mask1', 'phasegM')[128, 100:200],
                                   linewidth=3, label=str(dq[count]))
    fig_test3_multiple_dq_ax2.plot(x2, elements.load_g('Mask1', 'deltagM')[1, 128, :],
                                   linewidth=3, label=str(dq[count]))
    strain_value = elements.load_g('Mask1', 'deltagM')[1, 128, 200]
    strain_values.append(strain_value)
    count += 1
fig_test3_multiple_dq_ax1.set_ylim(-np.pi, np.pi)
fig_test3_multiple_dq_ax1.legend()
fig_test3_multiple_dq_ax1.set_title('Raw phase')
fig_test3_multiple_dq_ax2.set_title('Horizontal component of Δg')
fig_test3_multiple_dq_ax2.set_ylim(-0.1, 0.1)
fig_test3_multiple_dq.savefig(
    '/media/alex/Work/PhD/Course/CAS 741/project/STEM_Moire_GPA/Doc/TestReport/Figures/Test_3_test_results.png',
    dpi=300, bbox_inches='tight')
print('dg = ', dg)
print('strain = ', strain_values)
print('error = ', np.abs(np.array(dg)-np.array(strain_values)))

plt.show()

# #######################################
# Test #4 in TestPlan document
# #######################################

data_test_4 = data.SMGData()

# STEM Moire hologram with a unique periodicity of 4 pixels along horizontal axis on half image and a periodicity of
# 4.5 pixel along the same axis on the second half of the image (easy case). This leads to o a 'delta g' of
# 1/4-1/4.5 = 0.0277778.

x4a = np.linspace(0, 127, 128)
x4b = np.linspace(128, 255, 128)
y4 = np.linspace(0, 255, 256)
mx4a, my4a = np.meshgrid(x4a, y4)
mx4b, my4b = np.meshgrid(x4b, y4)
ismh4a = np.sin(mx4a * 2 * np.pi / 4)
ismh4b = np.sin(mx4b * 2 * np.pi / 4.5)
ismh4 = np.concatenate((ismh4a, ismh4b), axis=1)
ft_ismh4 = np.fft.fft2(ismh4)

# Store data in datastructure

data_test_4.store('ISMHexp', ismh4)
data_test_4.store('FTISMHexp', ft_ismh4)

# Mask parameter

r4 = [1, 2, 4, 8, 16, 32, 64, 128, 256]
center4 = (192, 128)

# Create the amount of branches corresponding the the radius tested and store the mask properties
for radius in r4:
    data_test_4.create_branch(str(radius))
    circle4 = center4, radius
    data_test_4.store_g(str(radius), 'Mask', circle4)


# Looping on the various radius into gpa
for radius in r4:
    gpa.gpa(str(radius), data_test_4)

count = 1
fig_test4 = plt.figure()
fig_test4_1d = plt.figure()
fig_test4_deltag_1d = plt.figure()
N_sublpot = math.ceil(math.sqrt(len(r4)))
print(math.ceil(math.sqrt(len(r4))))
for element in r4:
    fig_test4.add_subplot(N_sublpot, N_sublpot, count).imshow(data_test_4.load_g(
        str(element), 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
    fig_ax = fig_test4_1d.add_subplot(N_sublpot, N_sublpot, count)
    fig_ax.plot(x2, data_test_4.load_g(str(element), 'phasegM')[128, :])
    fig_ax.set_ylim(-np.pi, np.pi)
    fig_ax_g = fig_test4_deltag_1d.add_subplot(N_sublpot, N_sublpot, count)
    fig_ax_g.plot(x2, data_test_4.load_g(
        str(element), 'deltagM')[1, 128, :])
    fig_ax_g.set_ylim(-0.1, 0.1)
    count += 1

plt.show()
