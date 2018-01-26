import data
import numpy as np
import conversion

datastruct = data.SMGData()
mask = 'Mask1'
datastruct.create_branch(mask)
# Create elements used by conversion in the data structure
# Test # 24 in TestPlan.pdf
datastruct.store('p', 1/3)
datastruct.store_g('Mask1', 'gMuns', np.transpose(np.array([[[1, 1]]]),axes=(2,0,1)))
n = 1
m = -2

def test_conversion():
    conversion.conversion(mask, n, m, datastruct)
    assert np.all(datastruct.load_g(mask, 'gCuns')==np.array([[[4, -5]]]))