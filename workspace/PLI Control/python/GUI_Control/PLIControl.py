# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PLIControl.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnGo = QtWidgets.QPushButton(self.centralwidget)
        self.btnGo.setGeometry(QtCore.QRect(90, 350, 121, 111))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(237, 9, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 9, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 9, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.btnGo.setPalette(palette)
        self.btnGo.setObjectName("btnGo")
        self.btnHome = QtWidgets.QPushButton(self.centralwidget)
        self.btnHome.setGeometry(QtCore.QRect(90, 460, 121, 51))
        self.btnHome.setObjectName("btnHome")
        self.textStatus = QtWidgets.QTextBrowser(self.centralwidget)
        self.textStatus.setGeometry(QtCore.QRect(20, 20, 461, 321))
        self.textStatus.setObjectName("textStatus")
        self.btnLeft = QtWidgets.QPushButton(self.centralwidget)
        self.btnLeft.setGeometry(QtCore.QRect(300, 430, 41, 31))
        self.btnLeft.setObjectName("btnLeft")
        self.btnRight = QtWidgets.QPushButton(self.centralwidget)
        self.btnRight.setGeometry(QtCore.QRect(350, 430, 41, 31))
        self.btnRight.setObjectName("btnRight")
        self.btnReset = QtWidgets.QPushButton(self.centralwidget)
        self.btnReset.setGeometry(QtCore.QRect(300, 470, 91, 41))
        self.btnReset.setObjectName("btnReset")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PLI Controller - v0.1"))
        self.btnGo.setText(_translate("MainWindow", "GO"))
        self.btnHome.setText(_translate("MainWindow", "Home"))
        self.btnLeft.setText(_translate("MainWindow", "<<"))
        self.btnRight.setText(_translate("MainWindow", ">>"))
        self.btnReset.setText(_translate("MainWindow", "Reset"))

