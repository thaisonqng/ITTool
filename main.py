import os
import shutil
import sys
from PyQt5 import QtWidgets
from UI.MainWindow import MainWindow, DB


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
    SoftwareInventoryFolder = MainFolder + "\\SoftwareInventory\\"
    projectFolderScriptPS = "PowerShell\\"
    srvFolderScriptPS = "\\\\vnqn-test\\DataBase\\PowerShell\\"
    localFolderScriptPS = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\ScriptPS\\"

    if not os.path.exists(MainFolder):
        os.makedirs(MainFolder)
    if not os.path.exists(localFolderScriptPS):
        os.makedirs(localFolderScriptPS)
    if not os.path.exists(SoftwareInventoryFolder):
        os.makedirs(SoftwareInventoryFolder)

    if os.path.exists(projectFolderScriptPS):
        shutil.rmtree(srvFolderScriptPS)
        shutil.copytree(projectFolderScriptPS, srvFolderScriptPS)
    shutil.rmtree(localFolderScriptPS)
    shutil.copytree(srvFolderScriptPS, localFolderScriptPS)
    try:
        DB().InitAllDB()
    except:
        print("")

    main()