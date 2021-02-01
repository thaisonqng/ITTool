

from PyQt5 import QtCore, QtGui, QtWidgets
from DB.db import *
from UI.LoadScan import LoadScan
from UI.NewCardUpdate import NewCardUpdate
from UI.UI_MainWindow import Ui_MainWindow
from UI.SoftwareInventory import SoftwareInventory

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.frame.setVisible(False)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showlcd)
        timer.start(1000)
        self.lcdNumber.setDigitCount(8)  # change the number of digits displayed
        self.db = DB()

        MainMenu = [ 'Card Management', 'Scanned Detail', 'IT Tools', 'Setting']

        index = 0
        for submenu in MainMenu:
            self.toolBoxMenu.setItemText(index, submenu)
            index += 1
        self.MenuCard.clicked.connect(self.MenuCardEvent)
        self.MenuScan.clicked.connect(self.MenuScanEvent)
        self.MenuIT.clicked.connect(self.MenuITEvent)

    def GetTableData(self):
        return self.tableData
    def showlcd(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.lcdNumber.display(text)

    def MenuITEvent(self):
        self.ClearLayoutofFrame(self.frame)
        select = self.MenuIT.currentItem().text()
        self.frame.setVisible(False)
        if select == 'Inventory software':
            self.SoftwareInventory = SoftwareInventory()
            self.frame.setLayout(self.SoftwareInventory.layout())
            self.frame.setVisible(True)


    def MenuCardEvent(self):
        self.ClearLayoutofFrame(self.frame)
        self.newCardUpdate = NewCardUpdate()
        select = self.MenuCard.currentItem().text()
        self.frame.setVisible(False)
        if select == 'All Card':
            self.db.LoadTable(self.tableData, 'Card')
        if select == 'All Staff':
            self.db.LoadTable(self.tableData, 'Staff')
        elif select == 'New - Update Card':

            self.frame.setLayout(self.newCardUpdate.layoutNewUpdateCard)
            self.frame.setVisible(True)

    def MenuScanEvent(self):
        self.ClearLayoutofFrame(self.frame)
        self.LoadScan = LoadScan()
        select = self.MenuScan.currentItem().text()
        if select == 'Scan Detail':
            self.db.LoadTable(self.tableData, 'ScanedDetail')
            self.frame.setLayout(self.LoadScan.layoutLoadScan)
            self.frame.setVisible(True)
        elif select == 'New Card33333':
            self.ShowFrameNewCard()


    def ClearLayoutofFrame(self,frame):
        if frame.layout() is not None:
            old_layout = frame.layout()
            for i in reversed(range(old_layout.count())):
                # print("Delete ", old_layout.itemAt(i).widget().objectName(), "At", i)
                old_layout.itemAt(i).widget().setParent(None)
            import sip
            sip.delete(old_layout)



