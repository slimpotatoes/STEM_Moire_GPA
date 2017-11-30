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
