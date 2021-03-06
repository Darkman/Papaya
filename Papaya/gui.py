# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.showFullScreen()
        MainWindow.resize(800, 480)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Papaya/resources/doomsdaylogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.bluelabel = QtWidgets.QLabel(self.centralwidget)
        self.bluelabel.setGeometry(QtCore.QRect(400, 0, 400, 480))
        font = QtGui.QFont()
        font.setFamily("CutOutsFLF")
        font.setPointSize(26)
        font.setKerning(False)
        self.bluelabel.setFont(font)
        self.bluelabel.setStyleSheet("background-color: blue;\n"
"color: black;")
        self.bluelabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.bluelabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.bluelabel.setObjectName("bluelabel")
        self.redlabel = QtWidgets.QLabel(self.centralwidget)
        self.redlabel.setGeometry(QtCore.QRect(0, 0, 400, 480))
        font = QtGui.QFont()
        font.setFamily("CutOutsFLF")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.redlabel.setFont(font)
        self.redlabel.setStyleSheet("background-color: red;\n"
"color: black;")
        self.redlabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.redlabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.redlabel.setObjectName("redlabel")
        self.logo = QtWidgets.QFrame(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.logo.setStyleSheet("background-image: url(./Papaya/resources/doomsdaylogo.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")
        self.logo.setLineWidth(0)
        self.logo.setFrameShape(QtWidgets.QFrame.VLine)
        self.logo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.logo.setObjectName("logo")
        self.red_team_score_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.red_team_score_lcd.setGeometry(QtCore.QRect(70, 300, 200, 150))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.red_team_score_lcd.setFont(font)
        self.red_team_score_lcd.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.red_team_score_lcd.setLineWidth(0)
        self.red_team_score_lcd.setSmallDecimalPoint(False)
        self.red_team_score_lcd.setMode(QtWidgets.QLCDNumber.Dec)
        self.red_team_score_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.red_team_score_lcd.setProperty("value", 0.0)
        self.red_team_score_lcd.setObjectName("red_team_score_lcd")
        self.blue_team_score_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.blue_team_score_lcd.setGeometry(QtCore.QRect(530, 300, 200, 150))
        self.blue_team_score_lcd.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.blue_team_score_lcd.setLineWidth(0)
        self.blue_team_score_lcd.setSmallDecimalPoint(False)
        self.blue_team_score_lcd.setMode(QtWidgets.QLCDNumber.Dec)
        self.blue_team_score_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.blue_team_score_lcd.setProperty("value", 0.0)
        self.blue_team_score_lcd.setObjectName("blue_team_score_lcd")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(0, 410, 800, 70))
        font = QtGui.QFont()
        font.setFamily("CutOutsFLF")
        font.setPointSize(36)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: white;\n"
"text-shadow: -5px 0 black, 0 5px black, 5px 0 black, 0 -5px black;")
        self.status_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.status_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.status_label.setLineWidth(0)
        self.status_label.setText("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.status_label.setObjectName("status_label")
        self.red_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.red_checkbox.setGeometry(QtCore.QRect(70, 90, 71, 18))
        self.red_checkbox.setObjectName("red_checkbox")
        self.blue_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.blue_checkbox.setGeometry(QtCore.QRect(620, 90, 71, 18))
        self.blue_checkbox.setObjectName("blue_checkbox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PapayaProject"))
        self.bluelabel.setText(_translate("MainWindow", "SOVEREIGN STATES"))
        self.redlabel.setText(_translate("MainWindow", "FEDERAL COALITION"))
        self.red_checkbox.setText(_translate("MainWindow", "CheckBox"))
        self.blue_checkbox.setText(_translate("MainWindow", "CheckBox"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

