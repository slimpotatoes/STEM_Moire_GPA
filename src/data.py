# Data Structure Module


class SMGData(object):
    """Module storing and loading intermediate data used during the processing"""

    def __init__(self):
        self.SMGData = dict()
        self.SMGData['ISMHexp'] = None
        self.SMGData['p'] = None
        self.SMGData['ICref'] = None
        self.SMGData['pref'] = None
        self.SMGData['FTISMHexp'] = None
        self.SMGData['FTISMHsim'] = None
        self.SMGData['FTISMHsimDisplay'] = None
        self.SMGData['Uref'] = None
        self.SMGData['Exx'] = None
        self.SMGData['Eyy'] = None
        self.SMGData['Exy'] = None
        self.SMGData['Rxy'] = None

    def create_branch(self, gui_id):
        """Create a (sub)dictionary in dictionary SMGData associated with the string key gui_id
        representing the id of a the mask GUI object."""
        if gui_id not in self.SMGData.keys():
            self.SMGData[gui_id] = dict()
            self.SMGData[gui_id]['Mask'] = None
            self.SMGData[gui_id]['gMuns'] = None
            self.SMGData[gui_id]['phaseraw'] = None
            self.SMGData[gui_id]['deltagM'] = None
            self.SMGData[gui_id]['phasegM'] = None
            self.SMGData[gui_id]['shiftg'] = None
            self.SMGData[gui_id]['gCuns'] = None
        else:
            raise Exception('Key gui_id already exists, branch creation aborted')

    def remove_branch(self, gui_id):
        """Remove the (sub)dictionary in dictionary SMGData associated with the string key gui_id
                representing the id of a the mask GUI object."""
        if gui_id in self.SMGData.keys():
            del self.SMGData[gui_id]
        else:
            return
            # raise Warning('Key gui_id does not exist, the deletion process did not occur')

    def store(self, key, a):
        """Store in dictionary SMGData an object a associated with the string key."""
        if key in self.SMGData.keys():
            self.SMGData[key] = a
        else:
            raise Exception('Key does not exist in the data structure')

    def load(self, key):
        """Return from dictionary SMGData the object associated with the string key."""
        if key in self.SMGData.keys():
            return self.SMGData[key]
        else:
            raise Exception('Key does not exist in the data structure')

    def store_g(self, gui_id, key, a):
        """Store in (sub)dictionary SMGData[gui_id] an object a associated with the string key."""
        if gui_id in self.SMGData.keys():
            if key in self.SMGData[gui_id].keys():
                    self.SMGData[gui_id][key] = a
            else:
                raise Exception('Key is gui_id does not exist in the data structure')
        else:
            raise Exception('Gui id does not exist in the data structure')

    def load_g(self, gui_id, key):
        """Return from dictionary SMGData[gui_id] the object associated with the string key."""
        if gui_id in self.SMGData.keys():
            if key in self.SMGData[gui_id].keys():
                    return self.SMGData[gui_id][key]
            else:
                raise Exception('Key is gui_id does not exist in the data structure')
        else:
            raise Exception('Gui id does not exist in the data structure')
