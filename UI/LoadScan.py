from UI.UI_LoadScan import  Ui_FrameLoadScan
from PyQt5 import QtWidgets

class LoadScan(QtWidgets.QFrame, Ui_FrameLoadScan):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        Ui_FrameLoadScan.__init__(self)
        self.setupUi(self)