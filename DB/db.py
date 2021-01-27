from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem
from DB.card import Card
from DB.staff import Staff
from sqlalchemy import create_engine

class DB():
    def __init__(self):
        self.server_name = 'VNQN-TEST'
        self.database_name = 'db'
        self.database_Software = 'Software'
        self.database_Network = 'Network'
        self.stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/'
    def InitAllDB(self):
        self.CreateDb("db")
        self.CreateDb("Software")
        self.CreateDb("Network")
    def CheckDbExits(self,DbName):
        with create_engine(self.stringConnection).connect() as connection:
            rows = connection.execute("select name FROM sys.databases;")
            for row in rows:
                name = row["name"]
                if DbName == name:
                    print("DATABASE ",DbName+" is Exits")
                    return True
        print("DATABASE ",DbName + " is NOT Exits")
        return False
    def CreateDb(self,DbName):
        SQLCommand = "CREATE DATABASE "+ DbName + ";"
        if not self.CheckDbExits(DbName):
            with create_engine(self.stringConnection, isolation_level='AUTOCOMMIT').connect() as connection:
                connection.execute(SQLCommand)
                print("Create DB :",DbName)

    def DropAllTableSW(self):
        engine = create_engine(self.stringConnection + self.database_Software)
        listTable = engine.table_names()
        connection = engine.connect()
        for TableName in listTable:
            SQLCommandDropTable = "DROP TABLE dbo." + TableName
            connection.execute(SQLCommandDropTable)
            # print(" DROP", TableName)
        connection.close()

    def CreatTableSW_Computer(self, TableName, DbName,ListData):
        Table=TableName
        TableName=""
        for i in range(len(Table)):
            if not Table[i]=="-":
                TableName += Table[i]
            else:
                TableName += "_"
        SQLCommandCreateTable =  "CREATE TABLE "+ TableName + "$ ( " \
                                                   "Software varchar(255) NOT NULL, " \
                                                   "Vendor varchar(255), " \
                                                   "Version varchar(255) );"
        # print("SQLCommandCreateTable :", SQLCommandCreateTable)
        engine = create_engine(self.stringConnection+DbName)
        connection = engine.connect()
        connection.execute(SQLCommandCreateTable)
        for item in ListData:
            if item["Software"] is None:
                break
            SQLCommand  = "INSERT INTO dbo."+ TableName + "$" + \
                          " (Software, Vendor, Version) " \
                        "VALUES ('" + item["Software"] + "'"+\
                          ", "+ "'" + item["Vendor"] + "'" +\
                          ", '"+item["Version"]+\
                          "' );"
            # print("execute ",SQLCommand)
            connection.execute(SQLCommand)
        connection.close()

    def LoadTable(self, QTable, TableName):
        ResultList = list()
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        print("stringConnection : ",stringConnection)
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = 'SELECT  * FROM  dbo.' + TableName + '$'
        result = connection.execute(SQLCommand)
        for rows in result.fetchall():
            row = list()
            for field in rows:
                row.append(field)
            ResultList.append(row)
        HeaderList = connection.execute(SQLCommand).keys()
        print(HeaderList)
        connection.close()
        i = 0
        QTable.setColumnCount(len(HeaderList))
        QTable.setRowCount(len(ResultList))
        QTable.setHorizontalHeaderLabels(HeaderList)
        for row in ResultList:
            j = 0
            for item in row:
                if (type(item) == type(datetime.today())):
                    item_str = item.strftime("%m/%d/%Y, %H:%M:%S")
                    print(item_str)
                else:
                    item_str = str(item)
                newItem = QTableWidgetItem(item_str)
                QTable.setItem(i, j, newItem)
                j += 1
            i += 1
        QTable.resizeColumnsToContents()

    def GetCollumnToList(self, TableName, Column):
        ResultList = list()
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = 'SELECT ' + Column + ' FROM  dbo.' + TableName + '$'
        result = connection.execute(SQLCommand)
        for item in result.fetchall():
            ResultList.append(item[0])
        connection.close()
        return ResultList

    def Select(self, key, value, TableName):
        ResultList = list()
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = 'SELECT * FROM  dbo.' + TableName + '$  WHERE ' + key + ' = ' + value
        result = connection.execute(SQLCommand)

        for item in result.fetchall():
            ResultList.append(item)
        connection.close()
        return ResultList

    def SelectStaff(self, key, value):
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = 'SELECT * FROM  dbo.Staff$  WHERE ' + key + ' = ' + value
        SQLResult = connection.execute(SQLCommand).fetchall()
        # ID, FullName, Position, Department, JobTitle, JobDescription
        Result = Staff(SQLResult[0][0], SQLResult[0][1], SQLResult[0][2], SQLResult[0][3])
        connection.close()
        print('SelectStaff SQLCommand :' + SQLCommand)

        return Result

    def SelectCard(self, key, value):
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = 'SELECT * FROM  dbo.Card$  WHERE ' + key + ' = ' + value
        SQLResult = connection.execute(SQLCommand).fetchall()

        # [CardID]      ,[StaffID]      ,[FullName]      ,[Position]      ,[Department]      ,[Date]      ,[Picture]
        Result = Card(SQLResult[0][0], SQLResult[0][1], SQLResult[0][2], SQLResult[0][3], SQLResult[0][4],
                      SQLResult[0][5], SQLResult[0][6])
        connection.close()
        print('SelectCard SQLCommand :' + SQLCommand)

        return Result

    def InsertInto(self, Table, Columns, Values, ):
        if len(Columns) != len(Values):
            return
        col = ""
        val = ""
        index = 0
        while index < len(Columns):
            col += Columns[index]
            if index < len(Columns) - 1:
                col += ", "

            if type(Values[index] == str):
                val += "N'" + str(Values[index]) + "'"
            else:
                val += "'" + Values[index] + "'"
            if index < len(Values) - 1:
                val += ", "
            index += 1
        SQLCommand = "INSERT INTO db.dbo." + Table + "$" + "(" + col + ") VALUES (" + val + ");"
        print('InsertInto : ERROR \n SQLCommand :', SQLCommand)
        try:
            connection = self.GetConnection()
            connection.execute(SQLCommand)
            connection.close()
            return True
        except:
            print('InsertInto : ERROR \n SQLCommand :', SQLCommand)
            return False

    def GetConnection(self):
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        return create_engine(stringConnection).connect()

    def SaveNewCard(self, CurentCard):
        stringConnection = 'mssql+pymssql://' + self.server_name + '\SQLEXPRESS/' + self.database_name
        engine = create_engine(stringConnection)
        connection = engine.connect()
        SQLCommand = "INSERT INTO db.dbo.Card$ (CardID, StaffID, FullName, Position, Department,Date, Picture ) " \
                     "VALUES (" \
                     + str(CurentCard.cardID) + "," \
                     + str(CurentCard.staffID) + "," \
                     + "N" + "'" + str(CurentCard.fullName) + "'" + "," \
                     + "'" + str(CurentCard.position) + "'" + "," \
                     + "'" + str(CurentCard.department) + "'" + "," \
                     + "'" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "'" + "," \
                     + "'" + str(CurentCard.picture) + "'" + ");"
        SQLResult = connection.execute(SQLCommand)
        # print(SQLResult)

    def UpdateTable(self, TableName, Columns, Values, Condition):
        if len(Columns) != len(Values):
            return
        index = 0
        colval = " "
        while index < len(Columns):
            if index < len(Columns) - 1:
                colval  = colval + (str(Columns[index]) + " = N'" + str(Values[index]) + "', ")
            else:
                colval  = colval + (str(Columns[index]) + " = N'" + str(Values[index])) +"'"
            index += 1
        SQLCommand = "UPDATE db.dbo." + TableName + "$ SET " + colval + "  WHERE " + Condition + " ;"
        try:
            connection = self.GetConnection()
            connection.execute(SQLCommand)
            connection.close()
            return True
        except:
            print('UpdateTable : ERROR \n SQLCommand :', SQLCommand)
            return False


