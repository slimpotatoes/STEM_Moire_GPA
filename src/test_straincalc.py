import pytest
import straincalc
import numpy as np
import data

# ----------------
# Test cases
# ---------------

# Test 27 from TestPlan.pdf
datastruct_0 = data.SMGData()
datastruct_0.create_branch('Mask1')
datastruct_0.create_branch('Mask2')
datastruct_0.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 2]]]),axes=(2,0,1))
g_c_uns_2 = np.transpose(np.array([[[3, 4]]]),axes=(2,0,1))
delta_g_1 = np.transpose(np.array([[[0, 0]]]),axes=(2,0,1))
delta_g_2 = np.transpose(np.array([[[0, 0]]]),axes=(2,0,1))
datastruct_0.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_0.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_0.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_0.store_g('Mask1', 'deltagM', delta_g_2)
test_case_0 = dict()
test_case_0['datastruct'] = datastruct_0
test_case_0['to_assert_strain'] = np.array([[0, 0],[0, 0]])

test_cases = [test_case_0]

@pytest.mark.parameterize("test_case", test_cases)
def test_strain_calc_easy(test_case):
    straincalc.strain_calculation('Mask1', 'Mask2', test_case['datastruct'])
    assert np.all(np.array([[test_case['datastruct'].load('Exx'), test_case['datastruct'].load('Eyy')],
                            [test_case['datastruct'].load('Exy'), test_case['datastruct'].load('Rxx')]])
                  ==test_case['to_assert_strain'])