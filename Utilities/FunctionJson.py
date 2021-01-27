import json
import os

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic.properties import QtWidgets
from sqlalchemy import create_engine


class FunctionJson:
    def __init__(self):
        self.PsScripFile = "PowerShell\\PsScrip.ps1"
        self.MainFolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\"
        self.SoftwareInventoryFolder = self.MainFolder + "\\SoftwareInventory\\"

        self.server_name = 'VNQN-TEST'
        self.database_name = 'Software'
        self.database_Software = 'Software'
        self.stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/'

    def JsonToList(self, File, Field):
        list = []
        with open(File) as f:
            data = json.load(f)
            for item in data:
                list.append(item[Field])
        return list

    def JsonGetListIventorySwOK(self):
        list = []
        try:
            with open(self.SoftwareInventoryFolder + "Log.JSON") as f:
                data = json.load(f)
                for item in data:
                    if item["Status"] == "OK":
                        list.append(item["ComputerName"])
        except:
            print("JsonGetListIventorySwOK\nERROR open file : ", self.SoftwareInventoryFolder + "Log.JSON")
        return list

    def JsonGetListIventorySwError(self):
        list = []
        try:
            with open(self.SoftwareInventoryFolder + "Log.JSON") as f:
                data = json.load(f)
                for item in data:
                    if item["Status"] == "Offline":
                        list.append(item["ComputerName"])
        except:
            print("JsonGetListIventorySwError\nERROR open file : ",self.SoftwareInventoryFolder + "Log.JSON")
        return list

    def JsonGetListIventorySwOffline(self):
        list = []
        try:
            with open(self.SoftwareInventoryFolder + "Log.JSON") as f:
                data = json.load(f)
                for item in data:
                    if item["Status"] == "ERROR":
                        list.append(item["ComputerName"])
        except:
            print("JsonGetListIventorySwOffline\nERROR open file : ", self.SoftwareInventoryFolder + "Log.JSON")
        return list

    def DropAllTableSW(self):
        engine = create_engine(self.stringConnection + self.database_name)
        listTable = engine.table_names()
        connection = engine.connect()
        for TableName in listTable:
            SQLCommandDropTable = "DROP TABLE dbo." + TableName
            connection.execute(SQLCommandDropTable)
            # print(" DROP", TableName)
        connection.close()

    def LoadSoftwareInstalledToTable(self, tableData, Computers):

        ResultList = list()
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        print("stringConnection : ", stringConnection)
        SQLCommand = 'SELECT  * FROM  dbo.' + Computers[0].replace("-", "_") + '$;'
        engine = create_engine(stringConnection)
        connection = engine.connect()
        HeaderList = ["Computer"] + connection.execute(SQLCommand).keys()

        for computer in Computers:
            SQLCommand = 'SELECT  * FROM  dbo.' + computer.replace("-", "_") + '$;'
            result = connection.execute(SQLCommand)
            computer.replace("_", "-")
            for rows in result.fetchall():
                row = list()
                row.append(computer)
                for field in rows:
                    row.append(field)
                ResultList.append(row)
            ResultList.append(["", "", "", "", ""])
        connection.close()
        tableData.setHorizontalHeaderLabels(HeaderList)
        tableData.setColumnCount(len(HeaderList))
        tableData.setRowCount(len(ResultList))
        print("len(ResultList)", len(ResultList))
        for i in range(len(ResultList)):
            for j in range(len(HeaderList)):
                item_str = str(ResultList[i][j])
                newItem = QTableWidgetItem(item_str)
                tableData.setItem(i, j, newItem)

        # return tableData

        # QTable.resizeColumnsToContents()

    def JsonGetFileSoftwareInstalledToListDictionary(self, computer ):
        data = []
        computer.upper()
        print("JsonGetFileSoftwareInstalledToListDictionary",computer)
        try:
            with open(self.SoftwareInventoryFolder + computer+".JSON") as f:
                for item in json.load(f):
                    if item["DisplayVersion"] is None or item["DisplayVersion"] == "null":
                        DisplayVersion = " "
                    else:
                        DisplayVersion = item["DisplayVersion"]

                    if item["installdate"] is None or item["installdate"] == "null":
                        installdate = " "
                    else:
                        installdate =  item["installdate"]

                    if item["uninstallstring"] is None or item["uninstallstring"] == "null":
                        uninstallstring = " "
                    else:
                        uninstallstring =  item["uninstallstring"]

                    if item["installlocation"] is None or item["installlocation"] == "null":
                        installlocation = " "
                    else:
                        installlocation = item["installlocation"]

                    softwareDictionary = {
                        "ComputerName": item["ComputerName"],
                        "ProgramName": item["ProgramName"],
                        "DisplayVersion": DisplayVersion,
                        "installdate": installdate,
                        "uninstallstring": uninstallstring,
                        "installlocation": installlocation
                    }

                    data.append(softwareDictionary)
        except:
            print("ERROR in FunctionJson - JsonGetFileSoftwareInstalledToListDictionary  ")
        return data