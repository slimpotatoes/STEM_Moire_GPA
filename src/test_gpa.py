# Test of GPA Module

import numpy as np
import data as data
import gpa as gpa
import matplotlib.pyplot as plt

# Test #2 in TestPlan document

data_test_2 = data.SMGData()    # Data structure for test 2

# STEM Moire hologram with a unique periodicity of 4 pixels along horizontal axis (easy case) !!

x = np.linspace(0, 255, 256)
y = np.linspace(0, 255, 256)
mx, my = np.meshgrid(x, y)
ismh = np.sin(mx * np.pi / 2)
ft_ismh = np.fft.fft2(ismh)

# Store data in datastructure

data_test_2.store('ISMHexp', ismh)
data_test_2.store('FTISMHexp', ft_ismh)

# Create branch for mask

data_test_2.create_branch('Mask1')

# Circle of radius 1 centered around coordinate (192, 128)
r = 1
center = (192, 128)
circle = center, r

# mask_test = mask.mask_classic(center, r, ismh.shape)

# Store mask properties into datastructure

data_test_2.store_g('Mask1', 'Mask', circle)

# Entering gpa

gpa.gpa('Mask1', data_test_2)

# Display data

# Input data



# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test = plt.figure()
fig_test.add_subplot(2, 2, 1).imshow(ismh, cmap='gray')
fig_test.add_subplot(2, 2, 2).imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh ** 2))), cmap='gray')
fig_test.add_subplot(2, 2, 3).imshow(data_test_2.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test.add_subplot(2, 2, 4).imshow(data_test_2.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)

# Input/Output data in 1D
fig_1d = plt.figure()
fig_1d.add_subplot(2, 2, 1).plot(ismh[128, :])
fig_1d.add_subplot(2, 2, 2).plot(x,np.log1p(np.fft.fftshift(np.abs(ft_ismh ** 2)))[128, :])
fig_1d.add_subplot(2, 2, 3).plot(x,data_test_2.load_g('Mask1', 'phaseraw')[128, :])
plt.ylim(-np.pi, np.pi)
fig_1d.add_subplot(2, 2, 4).plot(x,data_test_2.load_g('Mask1', 'phasegM')[128, :])
plt.ylim(-np.pi, np.pi)

plt.show()