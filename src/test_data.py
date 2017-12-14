""" Tests of the SMGData class from data.py """

import pytest
import data

# Test setup

# SMGData instance

smgData = data.SMGData()

smgData.create_branch('Mask1')
smgData.create_branch('Mask2')

# This definition should have been provided by the SMGData interface
possibleKeys = [
        "ICref",
        "pref",
        "FTISMHexp",
        "FTISMHsim",
        "FTISMHsimDisplay",
        "Uref",
        "Exx",
        "Eyy",
        "Exy",
        "Rxy",
        ]

# This definition should have been provided by the SMGData interface
possibleKeysOfGuiIds = [
        "Mask",
        "gMuns",
        "deltagM",
        "phasegM",
        "shiftg",
        "gCuns",
        ]

possibleGuiIds = [
        "Mask1",
        "Mask2",
        ]

# -------------------------------------------------
# Test of positive (OK) cases of data stored
# -------------------------------------------------


@pytest.mark.parametrize("key", possibleKeys)
def test_data_store_load_ok(key):
    smgData.store(key, key)
    assert(smgData.SMGData[key] == key)

# -------------------------------------------------
# Test of positive (OK) cases of data stored in an existing branch
# -------------------------------------------------


@pytest.mark.parametrize("key", possibleKeysOfGuiIds)
@pytest.mark.parametrize("gui_id", possibleGuiIds)
def test_data_store_load_g_ok(gui_id, key):
    smgData.store_g(gui_id, key, key)
    assert(smgData.SMGData[gui_id][key] == key)
    assert(smgData.load_g(gui_id, key) == key)


# -------------------------------------------------
# Test of positive cases of data to load
# -------------------------------------------------


@pytest.mark.parametrize("key", possibleKeys)
def test_data_store_load_ok(key):
    smgData.store(key, key)
    assert (smgData.load(key) == key)


# -------------------------------------------------
# Test of positive cases of data to load from an existing branch
# -------------------------------------------------


@pytest.mark.parametrize("key", possibleKeysOfGuiIds)
@pytest.mark.parametrize("gui_id", possibleGuiIds)
def test_data_store_load_g_ok(gui_id, key):
    smgData.store_g(gui_id, key, key)
    assert (smgData.load_g(gui_id, key) == key)

# -------------------------------------------------
# Test of positive cases of non-string data to store
# -------------------------------------------------


def test_data_save_load_non_string_ok():
    smgData.store(possibleKeys[0], 1)                        # an integer
    assert(smgData.load(possibleKeys[0]) == 1)
    smgData.store(possibleKeys[1], 1.25)                     # a float
    assert(smgData.load(possibleKeys[1]) == 1.25)
    arr_len = 100000                                         # a big array
    my_array = [None] * arr_len
    for i in range(0, arr_len):
        my_array[i] = i
    smgData.store(possibleKeys[2], my_array)
    my_array2 = smgData.load(possibleKeys[2])
    assert(my_array == my_array2)

# -------------------------------------------------
# Test of negative (NOK) cases of data save and load
# -------------------------------------------------


def test_data_store_nok_illegal_key():
    with pytest.raises(Exception) as e_info:
        smgData.store('an illegal key', 0)
    assert(str(e_info.value) == 'Key does not exist in the data structure')


def test_data_load_nok_illegal_key():
    with pytest.raises(Exception) as e_info:
        smgData.load('an illegal key')
    assert(str(e_info.value) == 'Key does not exist in the data structure')
