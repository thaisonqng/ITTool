import os

from sqlalchemy import create_engine
import pymssql


class DBSoftware:
    def __init__(self):
        self.server_name = 'VNQN-TEST'
        self.database_Software = 'Software'
        self.stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/'
        self.SoftwareInventoryFolder= os.environ['USERPROFILE'] + "\\AppData\\Local\\ITTool\\SoftwareInventory\\"

    def DeleteSoftware(self,computer,software):
        tableName = computer.replace("-", "_")
        SQLCommandDelete = "DELETE FROM dbo."+ tableName +"$ WHERE uninstallstring = '" + software + "';"
        with create_engine(self.stringConnection + self.database_Software).connect() as connection:
            connection.execute(SQLCommandDelete)
            print("SQLCommandDelete :", SQLCommandDelete)
    def WriteDataSoftwareInstalledToDB(self, computer, data):
        tableName = computer.replace("-","_")
        SQLCommandCreateTable = "CREATE TABLE " + tableName + "$ ( " \
                                                                  "ComputerName varchar(255) NOT NULL, " \
                                                                  "ProgramName varchar(255), " \
                                                                  "DisplayVersion varchar(255), " \
                                                                  "installdate varchar(255), " \
                                                                  "uninstallstring varchar(255), " \
                                                                  "installlocation varchar(255)); "

        with create_engine(self.stringConnection + self.database_Software).connect() as connection:
            connection.execute(SQLCommandCreateTable)
            print("SQLCommandCreateTable :", SQLCommandCreateTable)
            for item in data:
                values = ""
                collumns = "ComputerName, ProgramName, DisplayVersion, installdate, uninstallstring, installlocation"
                values += "'" + item["ComputerName"] + "', "
                values += "'" + item["ProgramName"] + "', "
                values += "'" + item["DisplayVersion"] + "', "
                values += "'" + str(item["installdate"]) + "', "
                values += "'" + item["uninstallstring"] + "', "
                values += "'" + item["installlocation"] +"'"

                SQLCommandINSERT = "INSERT INTO dbo." + tableName + "$" + "(" + collumns + ") VALUES (" + values + ");"

                connection.execute(SQLCommandINSERT)


    def GetSoftwareInstalledFromDBToList(self,Computer):
        ResultList = list()
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_Software
        print("stringConnection : ", stringConnection)
        SQLCommand = 'SELECT  * FROM  dbo.' + Computer.replace("-","_") + '$;'
        with create_engine(stringConnection).connect() as connection:
            HeaderList =connection.execute(SQLCommand).keys()
            Computer.replace("-", "_")
            SQLCommand = 'SELECT  * FROM  dbo.' + Computer + '$;'
            result = connection.execute(SQLCommand)
            Computer.replace("_", "-")
            for rows in result.fetchall():
                row = list()
                row.append(Computer)
                for field in rows:
                    row.append(field)
                ResultList.append(row)
        return ResultList


    def DropTableSW(self,tableName):
        print("DropTableSW : ",tableName)
        listTableinDB = create_engine(self.stringConnection + self.database_Software).table_names()
        with create_engine(self.stringConnection + self.database_Software).connect() as connection:
            try:
                # if tableName in listTableinDB:
                SQLCommandDropTable = "DROP TABLE dbo." + tableName.replace("-","_") + "$"
                print(" SQLCommandDropTable : ", SQLCommandDropTable)
                connection.execute(SQLCommandDropTable)
            except:
                print("DropTableSW : Cannot drop the table :",tableName.replace("-","_"))
    def DropAllTableSW(self):
        print("DropAllTableSW")
        listTableinDB = create_engine(self.stringConnection +self.database_Software).table_names()
        print("listTableinDB",listTableinDB)
        with create_engine(self.stringConnection + self.database_Software).connect() as connection:
            try:
                for table in listTableinDB:
                # if tableName in listTableinDB:
                    SQLCommandDropTable = "DROP TABLE dbo." + table
                    connection.execute(SQLCommandDropTable)
            except:
                print("DropAllTableSW : Cannot drop DropAllTableSW")

    def GetTableSWData(self, computer):
        ResultList = list()
        with create_engine(self.stringConnection + self.database_Software ).connect() as connection:
            SQLCommand = 'SELECT  * FROM  dbo.' + computer.replace("-", "_") + '$;'
            try:
                result = connection.execute(SQLCommand)
                for rows in result.fetchall():
                    row = list()
                    for field in rows:
                        row.append(field)
                    ResultList.append(row)
            except:
                print("EROR at GetTableSWData :",computer.replace("-", "_"))
        return ResultList
