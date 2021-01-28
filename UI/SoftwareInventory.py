import os
import subprocess
from datetime import datetime

import wmi
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QGraphicsView, QAction
from PyQt5.uic.properties import QtCore
from sqlalchemy import create_engine

from DB.DBSoftware import DBSoftware
from PSTools.PSToolsFunction import PSToolsFunction
from Utilities.FunctionJson import FunctionJson
from PowerShell.FunctionsPS import FunctionsPS
from UI.UI_SoftwareInventory import  Ui_FrameSoftwareInventory
from PyQt5 import QtWidgets

from Utilities.MyFile import MyFile


class SoftwareInventory(QtWidgets.QFrame, Ui_FrameSoftwareInventory):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        Ui_FrameSoftwareInventory.__init__(self)
        self.setupUi(self)
        self.functionsPS = FunctionsPS()
        self.functionJson = FunctionJson()
        self.DBSoftware = DBSoftware()
        self.PsScripFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\ScriptPS"
        self.PsScripFile = self.PsScripFolder + "\\PsScrip.ps1"
        self.GetRemoteProgram = self.PsScripFolder + "GetRemoteProgram.ps1"
        self.Folder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\SoftwareInventory\\"
        self.MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
        self.SoftwareInventoryFolder = self.MainFolder + "\\SoftwareInventory\\"
        self.ComputersAD = list()
        self.ComputersInventory = list()
        self.ComputersOK = list()
        self.ComputersError = list()
        self.ComputersOffline = list()
        self.ListCheckboxComputer = list()
        self.Init()

        self.btnLoadComputersName.clicked.connect(self.ButtonLoadComputersEvent)
        self.btnInventory.clicked.connect(self.ButtonInventoryEvent)
        self.checkBoxSelectAll.installEventFilter(self)

        ### This property holds how the widget shows a context menu
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # +++
        ### This signal is emitted when the widget's contextMenuPolicy is Qt::CustomContextMenu,
        ### and the user has requested a context menu on the widget.
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)  # +++
        self.tableWidget.viewport().installEventFilter(self)


        self.server_name = 'VNQN-TEST'
        self.database_name = 'Software'
        self.database_Software = 'Software'
        self.stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/'
    def Init(self):

        self.functionsPS.RunPowerShellScript("GetADComputerToJson", self.lineEditPCname.text())
        self.ComputersAD = self.functionJson.JsonToList(self.MainFolder + "Computers.json", "Name")
        self.SetCheckBoxComputers()
        self.ComputersInventory = []
        self.HeaderList = ["ComputerName", "ProgramName", "DisplayVersion", "installdate", "uninstallstring"]
        for i in range(len(self.ComputersAD)):
            if self.ListCheckboxComputer[i].isChecked():
                self.ComputersInventory.append(self.ComputersAD[i])

    def ButtonLoadComputersEvent(self):
        self.ListCheckboxComputer=[]
        self.functionsPS.GetADComputerToJson(self.lineEditPCname.text())
        self.ComputersAD = self.functionJson.JsonToList(self.MainFolder + "Computers.json", "Name")
        self.btnInventory.show()
        self.checkBoxSelectAll.show()
        self.SetCheckBoxComputers()




    def ButtonInventoryEvent(self):
        MyFile().RemoveAllFile(self.SoftwareInventoryFolder)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.ComputersInventory = []
        self.ComputersOK = []
        self.ComputersOffline = []
        self.ComputersError = []
        for i in range(len(self.ComputersAD)):
            if self.ListCheckboxComputer[i].isChecked():
                self.ComputersInventory.append(self.ComputersAD[i])
        if (not len(self.ComputersInventory)):
            return
        self.tableWidget.setHorizontalHeaderLabels(self.HeaderList)
        self.tableWidget.setColumnCount(len(self.HeaderList))
        start  =  datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        param = "-Computers '"
        i=0
        while  i < len(self.ComputersInventory) -1:
            param += self.ComputersInventory[i] + ","
            i += 1
        param += self.ComputersInventory[i] + "'"
        if self.comboBoxType.currentText() == 'Scan':
            self.functionsPS.RunPowerShellScript("GetRemoteProgram", param)
            self.ComputersOK = self.functionJson.JsonGetListIventorySwOK()
            self.ComputersOffline = self.functionJson.JsonGetListIventorySwOffline()
            self.ComputersError = self.functionJson.JsonGetListIventorySwError()
            for computer in self.ComputersInventory:
                self.DBSoftware.DropTableSW(computer)
                data = self.functionJson.JsonGetFileSoftwareInstalledToListDictionary(computer)
                if len(data):
                    self.DBSoftware.WriteDataSoftwareInstalledToDB(computer, data)
                    self.LoadDBToTable(computer)
        else:
            for computer in self.ComputersInventory:
                self.LoadDBToTable(computer)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,400)
        end = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print("start :", start, "\nend : ", end)


    def SetCheckBoxComputers(self):
        for item in  self.ComputersAD:
            checkBox = QtWidgets.QCheckBox()
            checkBox.setChecked(False)
            checkBox.setObjectName( "checkBoxPC"+item.lower())
            checkBox.setText( item.upper())
            self.layoutComputers.addWidget(checkBox)
            checkBox.installEventFilter(self)
            self.ListCheckboxComputer.append(checkBox)

    def eventFilter(self, source, event):
        # Qt.Key_Enter = 16777221
        # Qt.Key_Tab = 16777217
        if (source is self.checkBoxSelectAll and
            event.type() == QEvent.MouseButtonPress):
            for cb in self.ListCheckboxComputer:
                cb.setChecked( not self.checkBoxSelectAll.isChecked())
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton:
                # print("Simple mouse motion")
                ey_Enter = 16777221
            elif event.buttons() == Qt.LeftButton:
                print("Left click drag")
            elif event.buttons() == Qt.RightButton:
                print("Right click drag")
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                print("Press LeftButton!")
            elif (event.button() == Qt.RightButton and
                source is self.tableWidget.viewport()):
                print("Press RightButton!")
                self.item = self.tableWidget.itemAt(event.pos())
                print('Global Pos:', event.globalPos())
                print("item", self.item.text())
                if len(self.item.text()) :
                    print('Table Item:', self.item.row(), self.item.column())
                    self.menu = QMenu(self.tableWidget)
                    Action = self.menu.addAction("Remove")
                    Action.triggered.connect(self.actionRemoveSW)


        return super().eventFilter(source, event)
    def actionRemoveSW(self):
        currentRow = self.item.row()
        sw=self.tableWidget.item(currentRow, 4).text()
        computer = self.tableWidget.item(self.item.row(), 0).text()
        if not len(sw):
            return
        # FunctionsPS.RemoveSoftwareUninstallString(self,computer,sw)
        self.labelInform.setText("REMOVED "+sw + " FROM " + computer)
        self.DBSoftware.DeleteSoftware(computer,sw)
        self.tableWidget.removeRow(currentRow)

    def generateMenu(self, pos):
        print("pos======", pos)
        self.menu.exec_(self.tableWidget.mapToGlobal(pos))  # +++

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.NoButton:
            print("Simple mouse motion")
        elif event.buttons() == QtCore.Qt.LeftButton:
            print("Left click drag")
        elif event.buttons() == QtCore.Qt.RightButton:
            print("Right click drag")
        super(SoftwareInventory, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print("Press!")
        super(SoftwareInventory, self).mousePressEvent(event)


    def LoadDBToTable(self, computer):
        sumRows = self.tableWidget.rowCount()
        # if sumRows <1 :
        #     self.tableWidget.setHorizontalHeaderLabels(self.HeaderList)
        self.tableWidget.setColumnCount(len(self.HeaderList))

        listData = self.DBSoftware.GetTableSWData(computer)

        self.tableWidget.setRowCount(sumRows + len(listData))
        for i in range(len(listData)):
            for j in range(len(self.HeaderList)):
                item_str = str(listData[i][j])
                newItem = QTableWidgetItem(item_str)
                self.tableWidget.setItem(sumRows + i, j, newItem)
