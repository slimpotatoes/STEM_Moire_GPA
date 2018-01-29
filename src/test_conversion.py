import pytest
import data
import numpy as np
import conversion

mask = 'Mask1'

# Create elements used by conversion in the data structure

# -------------------------------
# Test cases
# -------------------------------

# Test 24 in TestPlan.pdf
test_case_0 = dict()
datastruct_0 = data.SMGData()
datastruct_0.create_branch(mask)
datastruct_0.store('p', 1/3)
datastruct_0.store_g(mask, 'gMuns', np.transpose(np.array([[[1, -1]]]), axes=(2, 0, 1)))
test_case_0['datastruct'] = datastruct_0
test_case_0['n_horizontal'] = 1
test_case_0['m_vertical'] = 2
test_case_0['to_assert'] = np.transpose(np.array([[[-1, 0]]]), axes=(2, 0, 1))

test_case_1 = dict()
datastruct_1 = data.SMGData()
datastruct_1.create_branch(mask)
datastruct_1.store('p', 1/3)
datastruct_1.store_g(mask, 'gMuns', np.transpose(np.array([[[1, -1]]]), axes=(2, 0, 1)))
test_case_1['datastruct'] = datastruct_1
test_case_1['n_horizontal'] = -1
test_case_1['m_vertical'] = -2
test_case_1['to_assert'] = np.transpose(np.array([[[3, -2]]]), axes=(2, 0, 1))

test_case_2 = dict()
datastruct_2 = data.SMGData()
datastruct_2.create_branch(mask)
datastruct_2.store('p', 1/3)
datastruct_2.store_g(mask, 'gMuns', np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1)))
test_case_2['datastruct'] = datastruct_2
test_case_2['n_horizontal'] = 0
test_case_2['m_vertical'] = -2
test_case_2['to_assert'] = np.transpose(np.array([[[3, 0]]]), axes=(2, 0, 1))

test_case_3 = dict()
datastruct_3 = data.SMGData()
datastruct_3.create_branch(mask)
datastruct_3.store('p', 1/3)
datastruct_3.store_g(mask, 'gMuns', np.transpose(np.array([[[-1, 0]]]), axes=(2, 0, 1)))
test_case_3['datastruct'] = datastruct_3
test_case_3['n_horizontal'] = 0
test_case_3['m_vertical'] = 2
test_case_3['to_assert'] = np.transpose(np.array([[[-3, 0]]]), axes=(2, 0, 1))

test_cases = [test_case_0, test_case_1, test_case_2, test_case_3]


@pytest.mark.parametrize("test_case", test_cases)
def test_conversion(test_case):
    conversion.conversion(mask, test_case['n_horizontal'], test_case['m_vertical'], test_case['datastruct'])
    assert np.all(np.array(test_case['datastruct'].load_g(mask, 'gCuns')) == test_case['to_assert'])
