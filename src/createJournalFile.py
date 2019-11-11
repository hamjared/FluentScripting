import argparse
import os
import numpy
import typing

def main():
    parser = argparse.ArgumentParser(description= "Process options for creating Fluent Journal Files")
    parser.add_argument('--pressureSweep', type=int, nargs=2, required=True)
    parser.add_argument('--numSteps', type=int, nargs=1, default=10)
    parser.add_argument('--filename', help='specify journal file name', required=True)
    parser.add_argument('--filepath', help="Specify path of files to be saved by fluent")
    args = parser.parse_args()
    print(args.pressureSweep)
    createPressureSweepJournalFile(args.pressureSweep[0], args.pressureSweep[1], args.numSteps, args.filename, args.filepath)


def createPressureSweepJournalFile(minPres: int, maxPres: int, numSteps: int, filename, filePath):
    for curPressure in numpy.linspace(minPres, maxPres, numSteps):

        curfilePath = os.path.join(filePath, filename + "_" + "{0:.0f}".format(curPressure))
        print(curfilePath)

        writeSinglePressureCase(filename, curfilePath, curPressure, numIterations=200)


def writeSinglePressureCase(filename, filepath: typing.AnyStr, curPressure: int, numIterations: int):

    file = open(filename + ".jou", 'a')
    # --------------Outlet Boundary Condition Setting------------------------------------------------------------------
    fileContents = "//define/boundary-conditions/pressure-outlet \n" + "outlet\n" + "yes\n" + "no\n" + "{0:.0f}\n".format(curPressure)
    fileContents += "no\n" + "yes\n" +"no\n" + "no\n" + "yes\n"
    fileContents += str(5) + "\n" # Backflow turbulent intensity
    fileContents += str(10) + "\n" # Backflow turbulent viscosity ratio
    fileContents += "yes\n" + "no\n" + "no\n" + "no\n"

    # --------------Initialize Mesh-------------------------------------------------------------------------------------
    fileContents += "//solve/initialize/hyb-initialization\n" + "yes\n"
    # -------------- Solve ---------------------------------------------------------------------------------------------
    fileContents += "//solve/iterate " + str(numIterations) + "\n"
    # ------------- Create Boundary Flux file --------------------------------------------------------------------------
    fileContents += "//report/fluxes/mass-flow\n"
    fileContents += "yes\n" + "yes\n"
    fileContents += filepath + "_" + "boundary-mass-flow-" + "{0:.0f}".format(curPressure) + "\n"
    # -------------- Export case and data files as ensight gold --------------------------------------------------------
    fileContents += "//file/export/ensight-gold\n"
    fileContents += os.path.join(filepath, filename + "{0:.0f}".format(curPressure)) + "\n"
    fileContents += "pressure\n" + "velocity\n" + "done\n" + "yes\n" + "fluid\n\n\n" + "no\n"
    # -------------- Done creating this case ---------------------------------------------------------------------------
    file.write(fileContents)
    file.close()

if __name__ == '__main__':
    main()

