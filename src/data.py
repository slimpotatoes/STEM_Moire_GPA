# Data Structure Module
class SMGData(object):

    def __init__(self):
        self.SMGData = dict()
        self.SMGData['ISMHexp'] = None
        self.SMGData['p'] = None
        self.SMGData['ICref'] = None
        self.SMGData['pref'] = None
        self.SMGData['FTISMHexp'] = None
        self.SMGData['FTISMHsim'] = None
        self.SMGData['Uref'] = None
        self.SMGData['Exx'] = None
        self.SMGData['Eyy'] = None
        self.SMGData['Exy'] = None
        self.SMGData['Rxy'] = None

    def create_branch(self, gui_id):
        self.SMGData[gui_id] = dict()
        self.SMGData[gui_id]['Mask'] = None
        self.SMGData[gui_id]['gMuns'] = None
        self.SMGData[gui_id]['deltagM'] = None
        self.SMGData[gui_id]['phasegM'] = None
        self.SMGData[gui_id]['shiftg'] = None
        self.SMGData[gui_id]['gCuns'] = None

    def store(self, key, a):
        if key in self.SMGData.keys():
            self.SMGData[key] = a
        else:
            raise Exception('Key does not exist in the data structure')

    def load(self, key):
        if key in self.SMGData.keys():
            return self.SMGData[key]
        else:
            raise Exception('Key does not exist in the data structure')

    def store_g(self, gui_id, key, a):
        if gui_id in self.SMGData.keys():
            if key in self.SMGData[gui_id].keys():
                    self.SMGData[gui_id][key] = a
            else:
                raise Exception('Key is gui_id does not exist in the data structure')
        else:
            raise Exception('Gui id does not exist in the data structure')

    def load_g(self, gui_id, key):
        if gui_id in self.SMGData.keys():
            if key in self.SMGData[gui_id].keys():
                    return self.SMGData[gui_id][key]
            else:
                raise Exception('Key is gui_id does not exist in the data structure')
        else:
            raise Exception('Gui id does not exist in the data structure')
