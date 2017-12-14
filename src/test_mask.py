import pytest
import mask as mask
import numpy as np

# Test cases

center = (2, 3)
radius = 1

image_test_1 = np.ones(shape=(6, 6))
image_test_after_classic_mask_1 = np.zeros(image_test_1.shape) + np.array([[0, 0, 1, 0, 0, 0], [0, 1, 1, 1, 0, 0],
                                                                           [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                                                           [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
image_g_1 = np.array([np.zeros(image_test_1.shape), - 1 / 6 * image_test_1])

image_test_2 = np.ones(shape=(5, 5))
image_test_after_classic_mask_2 = np.zeros(image_test_2.shape) + np.array([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0],
                                                                           [0, 0, 1, 0, 0], [0, 0, 0, 0, 0],
                                                                           [0, 0, 0, 0, 0]])
image_g_2 = np.array([1 / 10 * image_test_2, - 1 / 10 * image_test_2])

image_test = [image_test_1, image_test_2]
image_test_after_classic_mask = [(image_test_after_classic_mask_1, image_g_1),
                                 (image_test_after_classic_mask_2, image_g_2)]

# -------------------------------------------------
# Test of classic mask on test cases
# -------------------------------------------------

@pytest.mark.parametrize('image, image_g', image_test_after_classic_mask)
def test_classic_mask(image, image_g):
    image_masked = mask.mask_classic(center, radius, image.shape)
    assert(image_masked[0].all() == image.all())
    assert(image_masked[1].all() == image_g.all())

# -------------------------------------------------
# Test of gaussian mask checking position of center and g_0 on test cases
# -------------------------------------------------

@pytest.mark.parametrize('image, image_g', image_test_after_classic_mask)
def test_gaussian_mask(image, image_g):
    image_masked = mask.mask_gaussian(center, radius, image.shape)
    assert(image_masked[0][3, 2] == 1)
    assert(image_masked[1].all() == image_g.all())