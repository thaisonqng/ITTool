import os
import sys
from PyQt5 import QtWidgets
from UI.MainWindow import MainWindow, DB


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    PsScripFile = "PowerShell\\PsScrip.ps1"
    MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
    SoftwareInventoryFolder = MainFolder + "\\SoftwareInventory\\"
    if not os.path.exists(MainFolder):
        os.makedirs(MainFolder)
    if not os.path.exists(SoftwareInventoryFolder):
        os.makedirs(SoftwareInventoryFolder)

    try :
        DB().InitAllDB()
    except:
        print("")

    main()

