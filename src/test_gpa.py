# Test of GPA Module

import numpy as np
import math as math
import data as data
import gpa as gpa
import matplotlib.pyplot as plt

# #######################################
# Test #2 in TestPlan document
# #######################################

data_test_2 = data.SMGData()    # Data structure for test 2

# STEM Moire hologram with a unique periodicity of 4 pixels along horizontal axis (easy case) !!

x2 = np.linspace(0, 255, 256)
y2 = np.linspace(0, 255, 256)
mx2, my2 = np.meshgrid(x2, y2)
ismh2 = np.sin(mx2 * 2 * np.pi / 4)
ft_ismh2 = np.fft.fft2(ismh2)

# Store data in datastructure

data_test_2.store('ISMHexp', ismh2)
data_test_2.store('FTISMHexp', ft_ismh2)

# Create branch for mask

data_test_2.create_branch('Mask1')

# Circle of radius 1 centered around coordinate (192, 128)
r2 = 1
center2 = (192, 128)
circle2 = center2, r2

# mask_test = mask.mask_classic(center, r, ismh.shape)

# Store mask properties into datastructure

data_test_2.store_g('Mask1', 'Mask', circle2)

# Entering gpa

gpa.gpa('Mask1', data_test_2)

# Display data

# Input/Output data - Phase is supposed to be constant and equal to 0, anything different from 0 represents the error.
fig_test2 = plt.figure()
fig_test2.add_subplot(2, 3, 1).imshow(ismh2, cmap='gray')
fig_test2.add_subplot(2, 3, 4).imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh2 ** 2))), cmap='gray')
fig_test2.add_subplot(2, 3, 2).imshow(data_test_2.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2.add_subplot(2, 3, 5).imshow(data_test_2.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test2.add_subplot(2, 3, 3).imshow(data_test_2.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test2.add_subplot(2, 3, 6).imshow(data_test_2.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)

# Input/Output data in 1D
fig_test2_1d = plt.figure()
fig_test2_1d.add_subplot(2, 3, 1).plot(ismh2[128, :])
fig_test2_1d.add_subplot(2, 3, 4).plot(x2, np.log1p(np.fft.fftshift(np.abs(ft_ismh2 ** 2)))[128, :])
fig_test2_1d.add_subplot(2, 3, 2).plot(x2, data_test_2.load_g('Mask1', 'phaseraw')[128, :])
plt.ylim(-np.pi, np.pi)
fig_test2_1d.add_subplot(2, 3, 5).plot(x2, data_test_2.load_g('Mask1', 'phasegM')[128, :])
plt.ylim(-np.pi, np.pi)
fig_test2_1d.add_subplot(2, 3, 3).plot(x2, data_test_2.load_g('Mask1', 'deltagM')[0, 128, :])
plt.ylim(-1, 1)
fig_test2_1d.add_subplot(2, 3, 6).plot(x2, data_test_2.load_g('Mask1', 'deltagM')[1, 128, :])
plt.ylim(-1, 1)

plt.show()

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
fig_test3 = plt.figure()
fig_test3.add_subplot(2, 3, 1).imshow(ismh3, cmap='gray')
fig_test3.add_subplot(2, 3, 4).imshow(np.log1p(np.fft.fftshift(np.abs(ft_ismh3 ** 2))), cmap='gray')
fig_test3.add_subplot(2, 3, 2).imshow(data_test_3.load_g('Mask1', 'phaseraw'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3.add_subplot(2, 3, 5).imshow(data_test_3.load_g('Mask1', 'phasegM'), cmap='gray', vmin=-np.pi, vmax=np.pi)
fig_test3.add_subplot(2, 3, 3).imshow(data_test_3.load_g('Mask1', 'deltagM')[0], cmap='gray', vmin=-1, vmax=1)
fig_test3.add_subplot(2, 3, 6).imshow(data_test_3.load_g('Mask1', 'deltagM')[1], cmap='gray', vmin=-1, vmax=1)

# Input/Output data in 1D
fig_test3_1d = plt.figure()
fig_test3_1d.add_subplot(2, 3, 1).plot(ismh3[128, :])
fig_test3_1d.add_subplot(2, 3, 4).plot(x2, np.log1p(np.fft.fftshift(np.abs(ft_ismh3 ** 2)))[128, :])
fig_test3_1d.add_subplot(2, 3, 2).plot(x2, data_test_3.load_g('Mask1', 'phaseraw')[128, :])
plt.ylim(-np.pi, np.pi)
fig_test3_1d.add_subplot(2, 3, 5).plot(x2, data_test_3.load_g('Mask1', 'phasegM')[128, :])
plt.ylim(-np.pi, np.pi)
fig_test3_1d.add_subplot(2, 3, 3).plot(x2, data_test_3.load_g('Mask1', 'deltagM')[0, 128, :])
plt.ylim(-1, 1)
fig_test3_1d.add_subplot(2, 3, 6).plot(x2, data_test_3.load_g('Mask1', 'deltagM')[1, 128, :])
plt.ylim(-1, 1)

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
