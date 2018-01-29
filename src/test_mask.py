import pytest
import mask as mask
import numpy as np

# Test cases

test_case_0 = dict()
test_case_0['center'] = (2, 3)
test_case_0['radius'] = 1
test_case_0['image_test'] = np.ones(shape=(6, 6))
test_case_0['image_to_assert'] = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
test_case_0['g0'] = np.array([0, -1/6])

test_case_1 = dict()
test_case_1['center'] = (2, 3)
test_case_1['radius'] = 1
test_case_1['image_test'] = np.ones(shape=(5, 5))
test_case_1['image_to_assert'] = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0], [0, 0, 1, 0, 0],
                                            [0, 0, 0, 0, 0]])
test_case_1['g0'] = np.array([1/10, -1/10])

test_case_2 = dict()
test_case_2['center'] = (3, 2)
test_case_2['radius'] = 1
test_case_2['image_test'] = np.ones(shape=(6, 6))
test_case_2['image_to_assert'] = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
test_case_2['g0'] = np.array([-1/6, 0])

test_case_3 = dict()
test_case_3['center'] = (4, 3)
test_case_3['radius'] = 1
test_case_3['image_test'] = np.ones(shape=(6, 6))
test_case_3['image_to_assert'] = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
test_case_3['g0'] = np.array([0, 1/6])

test_case_4 = dict()
test_case_4['center'] = (3, 4)
test_case_4['radius'] = 1
test_case_4['image_test'] = np.ones(shape=(6, 6))
test_case_4['image_to_assert'] = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]])
test_case_4['g0'] = np.array([1/6, 0])

test_cases = [test_case_0, test_case_1, test_case_2, test_case_3, test_case_4]

# -------------------------------------------------
# Test of classic mask on test cases
# -------------------------------------------------


# -------------------------------------------------
# Test of gaussian mask checking position of center and g_0 on test cases
# -------------------------------------------------


'''@pytest.mark.parametrize('image, image_g', image_test_after_classic_mask)
def test_gaussian_mask(image, image_g):
    image_masked = mask.mask_gaussian(center, radius, image.shape)
    assert(image_masked[0][3, 2] == 1)
    assert(np.all(image_masked[1] == image_g))'''

@pytest.mark.parametrize("test_case", test_cases)
def test_classic_masking(test_case):
    image_masked = np.array(mask.mask_classic(test_case['center'], test_case['radius'],
                                     np.shape(test_case['image_test']))[0])
    #print(image_masked)
    #print(test_case['image_to_assert'])
    assert np.all(image_masked==test_case['image_to_assert'])

@pytest.mark.parametrize("test_case", test_cases)
def test_classic_g0(test_case):
    image_masked = np.array(mask.mask_classic(test_case['center'], test_case['radius'],
                                     np.shape(test_case['image_test']))[1][:,0,0])
    #print(image_masked)
    #print(test_case['g0'])
    assert np.all(image_masked==test_case['g0'])

@pytest.mark.parametrize("test_case", test_cases)
def test_gaussian_g0(test_case):
    image_masked = np.array(mask.mask_gaussian(test_case['center'], test_case['radius'],
                                     np.shape(test_case['image_test']))[1][:,0,0])
    #print(image_masked)
    #print(test_case['g0'])
    assert np.all(image_masked==test_case['g0'])