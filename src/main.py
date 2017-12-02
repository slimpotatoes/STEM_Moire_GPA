# STEM Moire GPA Control Module)
import matplotlib.pyplot as plt
import gui as gui
import data as data
import userinput as userinput
import smhsimulation as smhsimu


def main():

    def flow_input(event):
        if not event.inaxes == smggui.event_input.ax:
            raise Exception('Improper input axis')
        smginput.load_files(smgdata)
        smggui.guismhexp(smgdata)

    def flow_smhsim(event):
        if not event.inaxes == smggui.event_smhsim.ax:
            raise Exception('Improper shmsim axis')
        smgsmhsim.smh_sim(smgdata)
        smggui.guismhsim(smgdata)

    def flow_gpa(event):
        if not event.inaxes == smggui.event_gpa.ax:
            raise Exception('Improper gpa axis')
        print('gpa')

    def flow_ref(event):
        if not event.inaxes == smggui.event_ref.ax:
            raise Exception('Improper ref axis')
        print('Uref')

    def flow_convert(event):
        if not event.inaxes == smggui.event_convert.ax:
            raise Exception('Improper convert axis')
        print('convert')

    def flow_strain(event):
        if not event.inaxes == smggui.event_strain.ax:
            raise Exception('Improper strain axis')
        print('strain')

    smggui = gui.SMGGUI()
    smgdata = data.SMGData()
    smginput = userinput.UserInput()
    smgsmhsim = smhsimu.SMHSim()

    smggui.guiconv()
    smggui.guiflow()

    smggui.event_input.on_clicked(flow_input)
    smggui.event_smhsim.on_clicked(flow_smhsim)
    smggui.event_gpa.on_clicked(flow_gpa)
    smggui.event_ref.on_clicked(flow_ref)
    smggui.event_convert.on_clicked(flow_convert)
    smggui.event_strain.on_clicked(flow_strain)

    plt.show()

if __name__ == "__main__":
    main()
