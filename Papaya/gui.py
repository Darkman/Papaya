# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Python\Code\Papaya\gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.status_label.setFont(font)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.gridLayout.addWidget(self.status_label, 3, 0, 1, 2)
        self.blue_team_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.blue_team_label.setFont(font)
        self.blue_team_label.setStyleSheet("background-color: rgb(0, 0, 255)")
        self.blue_team_label.setAlignment(QtCore.Qt.AlignCenter)
        self.blue_team_label.setObjectName("blue_team_label")
        self.gridLayout.addWidget(self.blue_team_label, 1, 1, 1, 1)
        self.blue_team_score_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.blue_team_score_lcd.setObjectName("blue_team_score_lcd")
        self.gridLayout.addWidget(self.blue_team_score_lcd, 2, 1, 1, 1)
        self.red_team_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.red_team_label.setFont(font)
        self.red_team_label.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.red_team_label.setAlignment(QtCore.Qt.AlignCenter)
        self.red_team_label.setObjectName("red_team_label")
        self.gridLayout.addWidget(self.red_team_label, 1, 0, 1, 1)
        self.red_team_score_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.red_team_score_lcd.setObjectName("red_team_score_lcd")
        self.gridLayout.addWidget(self.red_team_score_lcd, 2, 0, 1, 1)
        self.red_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.red_checkbox.setObjectName("red_checkbox")
        self.gridLayout.addWidget(self.red_checkbox, 0, 0, 1, 1)
        self.blue_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.blue_checkbox.setObjectName("blue_checkbox")
        self.gridLayout.addWidget(self.blue_checkbox, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.status_label.setText(_translate("MainWindow", "No team has control"))
        self.blue_team_label.setText(_translate("MainWindow", "Blue Team"))
        self.red_team_label.setText(_translate("MainWindow", "Red Team"))
        self.red_checkbox.setText(_translate("MainWindow", "CheckBox"))
        self.blue_checkbox.setText(_translate("MainWindow", "CheckBox"))

