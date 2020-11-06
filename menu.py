# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import sys

class Menu(QWidget):

    def __init__(self,direc,quitFn):
        super().__init__()
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setupUi(direc)
        self.addListeners()
        self.quitFn = quitFn


    def setupUi(self,direc):
        self.setObjectName("Form")
        self.resize(270, 150)
        self.setWindowOpacity(0.6)
        self.setWindowIcon(QtGui.QIcon(direc+"\icon.ico"))
        
        self.btnQuit = QtWidgets.QPushButton(self)
        self.btnQuit.setGeometry(QtCore.QRect(20, 20, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnQuit.setFont(font)
        self.btnQuit.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.btnQuit.setObjectName("btnQuit")
        self.btnChangeType = QtWidgets.QPushButton(self)
        self.btnChangeType.setGeometry(QtCore.QRect(100, 109, 75, 23))
        self.btnChangeType.setObjectName("btnChangeType")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(100, 80, 69, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(5, 80, 50, 50))
        self.label.setText("Invaders: ")
        self.invaderText = QtWidgets.QLabel(self)
        self.invaderText.setGeometry(QtCore.QRect(55, 80, 50, 50))
        self.invaderText.setText("1000")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def addListeners(self):
        self.btnQuit.clicked.connect(self.quit)
        

    def change(self,obj):
        text = self.comboBox.currentText()
        obj.changeTaskType(text)

    def updateInvaderCount(self,number):
        self.invaderText.setText(str(number))

    def quit(self):
        self.quitFn()
        sys.exit()
        self.close()

    def setButtonAction(self,obj):
        self.btnChangeType.clicked.connect(lambda: self.change(obj))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Menu"))
        self.btnQuit.setText(_translate("Form", "QUIT"))
        self.btnChangeType.setText(_translate("Form", "Change Type"))
        self.comboBox.setItemText(0, _translate("Form", "Personal"))
        self.comboBox.setItemText(1, _translate("Form", "Premium"))
        self.comboBox.setItemText(2, _translate("Form", "Clan"))


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = Menu("","")
#     window.show()
#     sys.exit(app.exec_())
