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
g_c_uns_1 = np.transpose(np.array([[[1, 2]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[3, 4]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[0, 0]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0, 0]]]), axes=(2, 0, 1))
datastruct_0.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_0.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_0.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_0.store_g('Mask2', 'deltagM', delta_g_2)
test_case_0 = dict()
test_case_0['datastruct'] = datastruct_0
test_case_0['to_assert_strain'] = np.array([[[0]], [[0]], [[0]], [[0]]])

# Test 28 from TestPlan.pdf
datastruct_1 = data.SMGData()
datastruct_1.create_branch('Mask1')
datastruct_1.create_branch('Mask2')
datastruct_1.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[0, 1]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[-0.1, 0]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0, 0]]]), axes=(2, 0, 1))
datastruct_1.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_1.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_1.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_1.store_g('Mask2', 'deltagM', delta_g_2)
test_case_1 = dict()
test_case_1['datastruct'] = datastruct_1
test_case_1['to_assert_strain'] = np.array([[[0]], [[1/9]], [[0]], [[0]]])

datastruct_2 = data.SMGData()
datastruct_2.create_branch('Mask1')
datastruct_2.create_branch('Mask2')
datastruct_2.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[0, 1]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[0, 0]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0, 0.1]]]), axes=(2, 0, 1))
datastruct_2.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_2.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_2.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_2.store_g('Mask2', 'deltagM', delta_g_2)
test_case_2 = dict()
test_case_2['datastruct'] = datastruct_2
test_case_2['to_assert_strain'] = np.array([[[-1/11]], [[0]], [[0]], [[0]]])

datastruct_3 = data.SMGData()
datastruct_3.create_branch('Mask1')
datastruct_3.create_branch('Mask2')
datastruct_3.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[0, 1]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[0.1, 0]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0, -0.1]]]), axes=(2, 0, 1))
datastruct_3.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_3.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_3.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_3.store_g('Mask2', 'deltagM', delta_g_2)
test_case_3 = dict()
test_case_3['datastruct'] = datastruct_3
test_case_3['to_assert_strain'] = np.array([[[1/9]], [[-1/11]], [[0]], [[0]]])

datastruct_4 = data.SMGData()
datastruct_4.create_branch('Mask1')
datastruct_4.create_branch('Mask2')
datastruct_4.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[0, 1]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[0, 0.01]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0.01, 0]]]), axes=(2, 0, 1))
datastruct_4.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_4.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_4.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_4.store_g('Mask2', 'deltagM', delta_g_2)
test_case_4 = dict()
test_case_4['datastruct'] = datastruct_4
test_case_4['to_assert_strain'] = np.array([[[0]], [[0]], [[1/0.9999*1/100]], [[0]]])

datastruct_5 = data.SMGData()
datastruct_5.create_branch('Mask1')
datastruct_5.create_branch('Mask2')
datastruct_5.store('p', 1)
g_c_uns_1 = np.transpose(np.array([[[1, 0]]]), axes=(2, 0, 1))
g_c_uns_2 = np.transpose(np.array([[[0, 1]]]), axes=(2, 0, 1))
delta_g_1 = np.transpose(np.array([[[0, -0.01]]]), axes=(2, 0, 1))
delta_g_2 = np.transpose(np.array([[[0.01, 0]]]), axes=(2, 0, 1))
datastruct_5.store_g('Mask1', 'gCuns', g_c_uns_1)
datastruct_5.store_g('Mask2', 'gCuns', g_c_uns_2)
datastruct_5.store_g('Mask1', 'deltagM', delta_g_1)
datastruct_5.store_g('Mask2', 'deltagM', delta_g_2)
test_case_5 = dict()
test_case_5['datastruct'] = datastruct_5
test_case_5['to_assert_strain'] = np.array([[[0]], [[0]], [[0]], [[-1/1.0001*1/100]]])

test_cases = [test_case_0, test_case_1, test_case_2, test_case_3, test_case_4, test_case_5]


@pytest.mark.parametrize("test_case", test_cases)
def test_strain_calc_easy(test_case):
    straincalc.strain_calculation('Mask1', 'Mask2', test_case['datastruct'])
    results = np.array([test_case['datastruct'].load('Exx'), test_case['datastruct'].load('Eyy'),
                    test_case['datastruct'].load('Exy'), test_case['datastruct'].load('Rxy')])
    print(results)
    print(test_case['to_assert_strain'])
    assert np.all(np.isclose(results, test_case['to_assert_strain'], atol=0.001))