# ############################# #
#                               #
#    STEM Moire GPA Software    #
#                               #
# ############################# #
#
# #####################################################################################

# Python script calculating the 2D relative strain maps from a STEM Moire hologram.
# Alexandre POFELSKI <pofelska@mcmaster.ca>
# https://github.com/slimpotatoes/STEM_Moire_GPA
# v.1.0.0
# 12 December 2017
#
# #####################################################################################


# STEM Moire GPA control Module

import matplotlib.pyplot as plt
import gui as gui
import data as data
import userinput as userinput
import smhsimulation as smhsimu
import gpa as gpa
import unstrainref as uref
import conversion as conversion
import straincalc as strain


def main():
    """Connection of the different events (button clicked by user) with the process steps of
    STEM Moire GPA processing"""
    def flow_input(event):
        """Input Process"""
        if not event.inaxes == smggui.event_input.ax:
            raise Exception('Improper input axis')
        file_path_smh, file_path_ic= smggui.open_files()
        userinput.load_files(file_path_smh, file_path_ic, smgdata)
        smggui.guismhexp(smgdata)

    def flow_smhsim(event):
        """Simulation of the STEM Moire hologram Process"""
        if not event.inaxes == smggui.event_smhsim.ax:
            raise Exception('Improper shmsim axis')
        smhsimu.smh_sim(smgdata)
        smggui.guismhsim(smgdata)

    def flow_gpa(event):
        """Geometrical Phase Analysis Process"""
        if not event.inaxes == smggui.event_gpa.ax:
            raise Exception('Improper gpa axis')
        mask_selected = smggui.mask_selection()
        gpa.gpa(mask_selected, smgdata)
        smggui.guiphase(mask_selected, smgdata)

    def flow_ref(event):
        """Unstrained reference definition Process"""
        if not event.inaxes == smggui.event_ref.ax:
            raise Exception('Improper ref axis')
        for mask_id in ['Mask1', 'Mask2']:
            print('Flow ref mask id', mask_id)
            uref.update_zerostrain(mask_id, smgdata)
            smggui.update_phase(mask_id, smgdata)

    def flow_convert(event):
        """Moire to crystal data conversion Process"""
        if not event.inaxes == smggui.event_convert.ax:
            raise Exception('Improper convert axis')
        print(smggui.h_1)
        conversion.conversion('Mask1', smggui.h_1, smggui.v_1, smgdata)
        conversion.conversion('Mask2', smggui.h_2, smggui.v_2, smgdata)

    def flow_strain(event):
        """Strain tensor calculation from two non collinear crystalline wave vector Process"""
        if not event.inaxes == smggui.event_strain.ax:
            raise Exception('Improper strain axis')
        strain.strain_calculation('Mask1', 'Mask2', smgdata)
        smggui.guistrain(smgdata)

    """Creation of the GUI and the Data object"""
    smggui = gui.SMGGUI()
    smgdata = data.SMGData()

    """Call of the GUI module functions to pop up the initial windows for the user"""
    smggui.guiconv()
    smggui.guiflow()

    """Connection of the event "button clicked by the user" to a function"""
    smggui.event_input.on_clicked(flow_input)
    smggui.event_smhsim.on_clicked(flow_smhsim)
    smggui.event_gpa.on_clicked(flow_gpa)
    smggui.event_ref.on_clicked(flow_ref)
    smggui.event_convert.on_clicked(flow_convert)
    smggui.event_strain.on_clicked(flow_strain)

    plt.show()

if __name__ == "__main__":
    main()
