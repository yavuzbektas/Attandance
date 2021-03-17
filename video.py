# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(614, 541)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 571, 401))
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 460, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 500, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 500, 311, 31))
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(330, 420, 261, 51))
        self.label_3.setObjectName("label_3")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(290, 460, 41, 31))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("images/hes.JPG"))
        self.label_28.setScaledContents(True)
        self.label_28.setObjectName("label_28")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(460, 470, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(340, 470, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(420, 460, 31, 31))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("images/temp.JPG"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setGeometry(QtCore.QRect(510, 460, 51, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(30, 255, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 255, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.doubleSpinBox.setPalette(palette)
        self.doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox.setProperty("value", 0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setGeometry(QtCore.QRect(380, 470, 21, 21))
        self.label_30.setText("")
        self.label_30.setPixmap(QtGui.QPixmap("images/ok.JPG"))
        self.label_30.setScaledContents(True)
        self.label_30.setObjectName("label_30")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Camera ON"))
        self.pushButton_2.setText(_translate("Dialog", "Camera OFF"))
        self.label_2.setText(_translate("Dialog", "Bulunan_isimler"))
        self.label_3.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-weight:600;\">Kayıt İçin Lütfen &quot;S&quot; Tusuna Basınız</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "Sıcaklık:"))
        self.label_5.setText(_translate("Dialog", "HES:"))
