import pathlib
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from DB.db import DB
from DB.card import Card
from DB.staff import Staff
from UI.UI_LoadScan import Ui_FrameLoadScan
from UI.UI_NewUpdateCard import Ui_FrameNewUpdateCard


class NewCardUpdate(QtWidgets.QFrame, Ui_FrameNewUpdateCard):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        Ui_FrameNewUpdateCard.__init__(self)
        self.setupUi(self)
        self.db = DB()
        self.dirPicture = '\\\\vnqn-test\\DataBase\\Card\\Picture\\'
        self.lineEditCardID.setVisible(False)
        self.lineEditStaffID.setFocus()
        self.lineEditStaffID.installEventFilter(self)
        self.lineEditCardID.installEventFilter(self)
        self.btnSaveCard.clicked.connect(self.Save)
        self.ShowPicture('avatar')
        self.CollumsCard = ["StaffID", "CardID", "FullName", "Position", "Department", "Date", "Picture"]
        self.Values = []
        self.cardAlready = False
        self.currentCard = Card("", "", "", "", "", "", "")
        self.currentStaff = Staff("", "", "", "")
        self.currentStaffID = 0
        self.newOrUpdate = 'new'

    def Save(self):
        cardID = self.lineEditCardID.text()
        # currentStaff = self.db.SelectStaff('currentStaffID', self.currentStaffID)
        print('currentStaff :' + self.currentStaff.FullName)
        print('New Card ID :' + cardID)
        if self.currentStaffID == '' or cardID == "":
            return
        self.currentCard = Card(staffID=self.currentStaff.StaffID,
                                cardID=cardID,
                                fullName=self.currentStaff.FullName,
                                position=self.currentStaff.JobTitle,
                                department=self.currentStaff.Department,
                                date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                picture=self.dirPicture + str(self.currentStaff.StaffID) + '.png'
                                )
        self.Values = self.currentCard.toList()
        if self.newOrUpdate == 'update':
            self.db.UpdateTable("Card", self.CollumsCard, self.Values, "StaffID = " + str(self.currentStaff.StaffID))
            # MainWindow.labelInform.setText("Card ID " + str(self.currentStaffID) + "- Staff ID " + str(self.currentStaff.StaffID) + " : Update OK")

        if self.newOrUpdate == 'new':
            self.db.InsertInto("Card", self.CollumsCard, self.Values)
            # MainWindow.labelInform.setText("Card ID " + str(self.currentCard.cardID) + "- Staff ID " + str(self.currentStaff.StaffID) + " : Create new OK")

        self.lineEditCardID.setVisible(False)
        self.lineEditStaffID.setFocus()

    def eventFilter(self, obj, event):
        # Qt.Key_Enter = 16777221
        # Qt.Key_Tab = 16777217
        if obj is self.lineEditStaffID and event.type() == 7:  # QtCore.QEvent.KeyRelease = 7
            if len(self.lineEditStaffID.text()) == 0:
                return super().eventFilter(obj, event)
            if event.key() == 16777221 or event.key() == 16777217:
                self.currentStaffID = self.lineEditStaffID.text()
                db = DB()
                listStaffID = db.GetCollumnToList('Staff', 'StaffID')
                if not int(self.currentStaffID) in listStaffID:
                    self.showdialog("Staff ID " + self.currentStaffID + " Not available in Data Base")
                    self.lineEditStaffID.clear()
                else:
                    self.lineEditCardID.setVisible(True)
                    self.lineEditCardID.clear()
                    self.lineEditCardID.setFocus()
                    self.ShowPicture(self.currentStaffID)
                    self.currentStaff = self.db.SelectStaff('StaffID',  self.currentStaffID)
                    self.labelFullName.setText( self.currentStaff.FullName)
                    self.labelPosition.setText( self.currentStaff.JobTitle)
                    self.labelDepatment.setText( self.currentStaff.Department)
                    try:
                        self.currentCard = self.db.SelectCard('StaffID', self.currentStaffID)
                        if (self.currentCard.cardID):
                            self.newOrUpdate = 'update'
                            print('currentCard -update: ',self.currentCard.staffID)
                            self.lineEditCardID.setText(str(self.currentCard.cardID))
                    except:
                            self.newOrUpdate = 'new'

        elif obj is self.lineEditCardID and event.type() == 7:  # QtCore.QEvent.KeyRelease = 7
            if event.key() == 16777221 or event.key() == 16777217:
                self.Save()

        return super().eventFilter(obj, event)

    def ShowPicture(self, staffID):
        image_path = self.dirPicture + staffID + ".png"
        file = pathlib.Path(image_path)
        if not file.exists():
            image_path = "avatar.png"
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap(image_path)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.graphicsViewPicture.setScene(scene)

    def ShowInfoStaff(self, staffID):
        list = self.db.SelectStaff('StaffID', staffID)
        self.labelFullName.setText(list[1])
        self.labelPosition.setText(list[2])
        self.labelDepatment.setText(list[3])

    def showdialog(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setText("This is a message box")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.exec_()
